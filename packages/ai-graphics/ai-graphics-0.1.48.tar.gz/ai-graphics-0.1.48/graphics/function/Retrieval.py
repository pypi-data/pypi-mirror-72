import os
import pickle
import shutil
import time
from shutil import copyfile
from typing import Dict, List

import matplotlib.pyplot as plt
import numpy as np
import torch
from PIL import Image
from torch.utils.data import DataLoader
from torchvision import transforms
from torchvision.models.utils import load_state_dict_from_url
from tqdm import tqdm

from ..libs.retrieval.aggregator import GeM
from ..libs.retrieval.dataset import PadResize, ToTensor, Normalize, CollateFn, Folder, feature_loader
from ..libs.retrieval.extract import ResSeries
from ..libs.retrieval.metric import KNN
from ..libs.retrieval.reduction import PCA, L2Normalize
from ..libs.retrieval.rerank import ReRanker
from ..libs.retrieval.evaluate import OverAll
from ..libs.retrieval.resnet import resnet50, model_urls

__all__ = ['split_dataset',
           'make_data_json',
           'Retrieval']


def split_dataset(dataset_path="datasets", split_file="caltech_split.txt"):
    """
    按照指定规则对数据集分类
    :param dataset_path: 数据集路径
    :param split_file: 指定分类规则文件
    """
    with open(split_file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            path = line.strip('\n').split(' ')[0]
            is_gallery = line.strip('\n').split(' ')[1]
            if is_gallery == '0':
                src = os.path.join(dataset_path, path)
                dst = src.replace(path.split('/')[0], 'query')
                dst_index = len(dst.split('/')[-1])
                dst_dir = dst[:len(dst) - dst_index]
                if not os.path.isdir(dst_dir):
                    os.makedirs(dst_dir)
                if not os.path.exists(dst):
                    copyfile(src, dst)
            elif is_gallery == '1':
                src = os.path.join(dataset_path, path)
                dst = src.replace(path.split('/')[0], 'gallery')
                dst_index = len(dst.split('/')[-1])
                dst_dir = dst[:len(dst) - dst_index]
                if not os.path.isdir(dst_dir):
                    os.makedirs(dst_dir)
                if not os.path.exists(dst):
                    copyfile(src, dst)


def make_data_json(dataset_path="datasets/gallery", save_path="caltech_gallery.json"):
    """
    生成数据json文件
    :param dataset_path: 数据集路径
    :param save_path: 保持json文件路径
    """
    info_dicts, label_list, label_to_idx = list(), list(), dict()
    img_dirs = os.listdir(dataset_path)
    for dir in img_dirs:
        for root, _, files in os.walk(os.path.join(dataset_path, dir)):
            for file in files:
                info_dict = dict()
                info_dict['path'] = os.path.join(root, file)
                if dir not in label_list:
                    label_to_idx[dir] = len(label_list)
                    label_list.append(dir)
                info_dict['label'] = dir
                info_dict['label_idx'] = label_to_idx[dir]
                info_dicts += [info_dict]
    with open(save_path, 'wb') as f:
        pickle.dump({'nr_class': len(img_dirs), 'path_type': 'absolute_path', 'info_dicts': info_dicts}, f)


class Identity:
    """
    Directly return feature maps without any operations.
    """
    default_hyper_params = dict()

    def __init__(self):
        pass

    def __call__(self, features: torch.tensor) -> torch.tensor:
        return features


class ExtractHelper:
    """
    A helper class to extract feature maps from model, and then aggregate them.
    """

    def __init__(self, assemble, extractor, splitter, aggregators):
        """
        Args:
            assemble (int): way to assemble features if transformers produce multiple images (e.g. TwoFlip, TenCrop).
            extractor (Extractor): a extractor class for extracting features.
            splitter (Splitter): a splitter class for splitting features.
            aggregators (list): a list of extractor classes for aggregating features.
        """
        self.assemble = assemble
        self.extractor = extractor
        self.splitter = splitter
        self.aggregators = aggregators

    def _save_part_features(self, datainfo: Dict, save_feature: List, save_path: str) -> None:
        """
        Save features in a json file.

        Args:
            datainfo (dict): the dataset information contained the data json file.
            save_feature (list): a list of features to be saved.
            save_path (str): the save path for the extracted features.
        """
        save_json = dict()
        for key in datainfo:
            if key != "info_dicts":
                save_json[key] = datainfo[key]
        save_json["info_dicts"] = save_feature

        with open(save_path, "wb") as f:
            pickle.dump(save_json, f)

    def extract_one_batch(self, batch: Dict) -> Dict:
        """
        Extract features for a batch of images.

        Args:
            batch (dict): a dict containing several image tensors.

        Returns:
            all_feature_dict (dict): a dict containing extracted features.
        """
        img = batch["img"]
        if torch.cuda.is_available():
            img = img.cuda()
        # img is in the shape (N, IMG_AUG, C, H, W)
        batch_size, aug_size = img.shape[0], img.shape[1]
        img = img.view(-1, img.shape[2], img.shape[3], img.shape[4])

        features = self.extractor(img)
        features = self.splitter(features)

        all_feature_dict = dict()
        for aggregator in self.aggregators:
            fea_dict = aggregator(features)
            all_feature_dict.update(fea_dict)

        # PyTorch will duplicate inputs if batch_size < n_gpu
        for key in all_feature_dict.keys():
            if self.assemble == 0:
                features = all_feature_dict[key][:img.shape[0], :]
                features = features.view(batch_size, aug_size, -1)
                features = features.view(batch_size, -1)
                all_feature_dict[key] = features
            elif self.assemble == 1:
                features = all_feature_dict[key].view(batch_size, aug_size, -1)
                features = features.sum(dim=1)
                all_feature_dict[key] = features

        return all_feature_dict

    def do_extract(self, dataloader: DataLoader, save_path: str, save_interval: int = 5000) -> None:
        """
        Extract features for a whole dataset and save features in json files.

        Args:
            dataloader (DataLoader): a DataLoader class for loading images for training.
            save_path (str): the save path for the extracted features.
            save_interval (int, optional): number of features saved in one part file.
        """
        datainfo = dataloader.dataset.data_info
        pbar = tqdm(range(len(dataloader)))
        save_feature = list()
        part_cnt = 0
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        start = time.time()
        for _, batch in zip(pbar, dataloader):
            feature_dict = self.extract_one_batch(batch)
            for i in range(len(batch["img"])):
                idx = batch["idx"][i]
                save_feature.append(datainfo["info_dicts"][idx])
                single_feature_dict = dict()
                for key in feature_dict:
                    single_feature_dict[key] = feature_dict[key][i].tolist()
                save_feature[-1]["feature"] = single_feature_dict
                save_feature[-1]["idx"] = int(idx)

            if len(save_feature) >= save_interval:
                self._save_part_features(datainfo, save_feature,
                                         os.path.join(save_path, "part_{}.json".format(part_cnt)))
                part_cnt += 1
                del save_feature
                save_feature = list()
        end = time.time()
        print('time: ', end - start)

        if len(save_feature) >= 1:
            self._save_part_features(datainfo, save_feature, os.path.join(save_path, "part_{}.json".format(part_cnt)))

    def do_single_extract(self, img: torch.Tensor) -> [Dict]:
        """
        Extract features for a single image.

        Args:
            img (torch.Tensor): a single image tensor.

        Returns:
            [fea_dict] (sequence): the extract features of the image.
        """
        batch = dict()
        batch["img"] = img.view(1, img.shape[0], img.shape[1], img.shape[2], img.shape[3])
        feature_dict = self.extract_one_batch(batch)

        return [feature_dict]


class IndexHelper:
    """
    A helper class to index features.
    """

    def __init__(
            self,
            dim_processors,
            feature_enhancer,
            metric,
            re_ranker,
    ):
        """
        Args:
            dim_processors (list):
            feature_enhancer (EnhanceBase):
            metric (MetricBase):
            re_ranker (ReRankerBase):
        """
        self.dim_procs = dim_processors
        self.feature_enhance = feature_enhancer
        self.metric = metric
        self.re_rank = re_ranker

    def show_topk_retrieved_images(self, single_query_info: Dict, topk: int, gallery_info: List[Dict]) -> None:
        """
        Show the top-k retrieved images of one query.

        Args:
            single_query_info (dict): a dict of single query information.
            topk (int): number of the nearest images to be showed.
            gallery_info (list): a list of gallery set information.
        """
        query_idx = single_query_info["ranked_neighbors_idx"]
        query_topk_idx = query_idx[:topk]

        for idx in query_topk_idx:
            img_path = gallery_info[idx]["path"]
            plt.figure()
            plt.imshow(img_path)
            plt.show()

    def save_topk_retrieved_images(self, save_path: str, single_query_info: Dict, topk: int,
                                   gallery_info: List[Dict]) -> None:
        """
        Save the top-k retrieved images of one query.

        Args:
            save_path (str): the path to save the retrieved images.
            single_query_info (dict): a dict of single query information.
            topk (int): number of the nearest images to be saved.
            gallery_info (list): a list of gallery set information.
        """
        query_idx = single_query_info["ranked_neighbors_idx"]
        query_topk_idx = query_idx[:topk]

        for idx in query_topk_idx:
            img_path = gallery_info[idx]["path"]
            shutil.copy(img_path, os.path.join(save_path, str(idx) + '.png'))

    def do_index(self, query_feature: np.ndarray, query_info: List, gallery_feature: np.ndarray) -> (
            List, np.ndarray, np.ndarray):
        """
        Index the query features.

        Args:
            query_feature (np.ndarray): query set features.
            query_info (list): a list of gallery set information.
            gallery_feature (np.ndarray): gallery set features.

        Returns:
            tuple(List, np.ndarray, np.ndarray): query feature information, query features and gallery features after process.
        """
        for dim_proc in self.dim_procs:
            query_feature, gallery_feature = dim_proc(query_feature), dim_proc(gallery_feature)

        query_feature, gallery_feature = torch.Tensor(query_feature), torch.Tensor(gallery_feature)
        if torch.cuda.is_available():
            query_feature = query_feature.cuda()
            gallery_feature = gallery_feature.cuda()

        gallery_feature = self.feature_enhance(gallery_feature)
        dis, sorted_index = self.metric(query_feature, gallery_feature)

        sorted_index = self.re_rank(query_feature, gallery_feature, dis=dis, sorted_index=sorted_index)
        for i, info in enumerate(query_info):
            info["ranked_neighbors_idx"] = sorted_index[i].tolist()

        return query_info, query_feature, gallery_feature


class EvaluateHelper:
    """
    A helper class to evaluate query results.
    """

    def __init__(self, evaluator):
        """
        Args:
            evaluator: a evaluator class.
        """
        self.evaluator = evaluator
        self.recall_k = evaluator.default_hyper_params["recall_k"]

    def show_results(self, mAP: float, recall_at_k: Dict) -> None:
        """
        Show the evaluate results.

        Args:
            mAP (float): mean average precision.
            recall_at_k (Dict): recall at the k position.
        """
        repr_str = "mAP: {:.1f}\n".format(mAP)

        for k in self.recall_k:
            repr_str += "R@{}: {:.1f}\t".format(k, recall_at_k[k])

        print('--------------- Retrieval Evaluation ------------')
        print(repr_str)

    def do_eval(self, query_result_info: List, gallery_info: List) -> (float, Dict):
        """
        Get the evaluate results.

        Args:
            query_result_info (list): a list of indexing results.
            gallery_info (list): a list of gallery set information.

        Returns:
            tuple (float, Dict): mean average precision and recall for each position.
        """
        mAP, recall_at_k = self.evaluator(query_result_info, gallery_info)

        return mAP, recall_at_k


class Retrieval:
    def __init__(self, model_name="resnet50-19c8e357.pth", ctx_id=-1):
        self.model_name = model_name
        self.device = torch.device("cuda:" + str(ctx_id)) if ctx_id > -1 else torch.device("cpu")
        self.model = self.load_model()
        pass

    def load_model(self):
        model = resnet50()
        if os.path.exists(self.model_name):
            state_dict = torch.load(self.model_name, map_location=None if torch.cuda.is_available() else 'cpu')
        else:
            state_dict = load_state_dict_from_url(model_urls["resnet50"],
                                                  map_location=None if torch.cuda.is_available() else 'cpu',
                                                  progress=True)

        model.load_state_dict(state_dict, strict=False)
        if torch.cuda.is_available():
            model = model.to(self.device)

        return model

    @staticmethod
    def create_extract_helper(model):
        assemble = 0
        extractor = ResSeries(model)
        splitter = Identity()
        aggregators = [GeM()]

        extract_helper = ExtractHelper(assemble, extractor, splitter, aggregators)
        return extract_helper

    def extract_features(self,
                         data_json="caltech_gallery.json",
                         save_path="features/caltech/gallery/",
                         save_interval=1000):
        transform = transforms.Compose([PadResize(),
                                        ToTensor(),
                                        Normalize()])
        dataset = Folder(data_json, transform)
        data_loader = DataLoader(dataset, batch_size=16, collate_fn=CollateFn(), num_workers=8, pin_memory=True)
        extract_helper = self.create_extract_helper(self.model)
        extract_helper.do_extract(data_loader, save_path, save_interval)
        return

    @staticmethod
    def create_index_helper(feature_names=["pool5_GeM"]):

        dim_processors = [L2Normalize(feature_names),
                          PCA(feature_names),
                          L2Normalize(feature_names)]

        metric = KNN()
        feature_enhancer = Identity()
        re_ranker = ReRanker()
        helper = IndexHelper(dim_processors, feature_enhancer, metric, re_ranker)
        return helper

    def search_index(self,
                     path='../datasets/query/airplanes/image_0004.jpg',
                     gallery_feature_dir="../datasets/features/caltech/gallery",
                     feature_names=["pool5_GeM"]):
        # build transformers
        transform = transforms.Compose([PadResize(),
                                        ToTensor(),
                                        Normalize()])

        # read image and convert it to tensor
        img = Image.open(path).convert("RGB")
        img_tensor = transform(img)

        extract_helper = self.create_extract_helper(self.model)
        img_feature_info = extract_helper.do_single_extract(img_tensor)

        stacked_feature = list()
        for name in feature_names:
            assert name in img_feature_info[0], "invalid feature name: {} not in {}!".format(name,
                                                                                             img_feature_info[0].keys())
            stacked_feature.append(img_feature_info[0][name])
        img_feature = np.concatenate(stacked_feature, axis=1)

        # load gallery features
        gallery_feature, gallery_info, _ = feature_loader.load(gallery_feature_dir, feature_names)

        # build helper and single index feature
        index_helper = self.create_index_helper(feature_names)
        index_result_info, query_feature, gallery_feature = index_helper.do_index(img_feature, img_feature_info,
                                                                                  gallery_feature)

        index_helper.save_topk_retrieved_images('../datasets/retrieved_images/', index_result_info[0], 5, gallery_info)
        print('single index have done!')
        return

    def evaluate(self,
                 query_feature_dir="../datasets/features/caltech/query",
                 gallery_feature_dir="../datasets/features/caltech/gallery",
                 feature_names=["pool5_GeM"]):
        # load features
        query_feature, query_info, _ = feature_loader.load(query_feature_dir, feature_names)
        gallery_feature, gallery_info, _ = feature_loader.load(gallery_feature_dir, feature_names)

        # build helper and index features
        index_helper = self.create_index_helper(feature_names)
        index_result_info, query_feature, gallery_feature = index_helper.do_index(query_feature, query_info,
                                                                                  gallery_feature)

        # build helper and evaluate results
        evaluator = OverAll()
        evaluate_helper = EvaluateHelper(evaluator)
        mAP, recall_at_k = evaluate_helper.do_eval(index_result_info, gallery_info)

        # show results
        evaluate_helper.show_results(mAP, recall_at_k)
