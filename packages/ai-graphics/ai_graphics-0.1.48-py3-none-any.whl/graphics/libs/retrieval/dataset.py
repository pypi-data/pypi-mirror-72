import os
import pickle
from typing import Dict, List

import numpy as np
import torch
from PIL import Image
from torch.utils.data.dataloader import default_collate
from torchvision import transforms

__all__ = ['PadResize',
           'ToTensor',
           'Normalize',
           'CollateFn',
           'Folder',
           'feature_loader']


class PadResize:
    """
    Resize image's longer edge to target size, and then pad the shorter edge to target size.

    Hyper-Params
        size (int): desired output size of the longer edge.
        padding_v (sequence): padding pixel value.
        interpolation (int): desired interpolation.
    """
    default_hyper_params = {
        "size": 224,
        "padding_v": [124, 116, 104],
        "interpolation": Image.BILINEAR,
    }

    def __init__(self):
        pass

    def __call__(self, img: Image) -> Image:
        target_size = self.default_hyper_params["size"]
        padding_v = tuple(self.default_hyper_params["padding_v"])

        w, h = img.size
        if w > h:
            img = img.resize((int(target_size), int(h * target_size * 1.0 / w)), Image.BILINEAR)
        else:
            img = img.resize((int(w * target_size * 1.0 / h), int(target_size)), Image.BILINEAR)

        ret_img = Image.new("RGB", (target_size, target_size), padding_v)
        w, h = img.size
        st_w = int((ret_img.size[0] - w) / 2.0)
        st_h = int((ret_img.size[1] - h) / 2.0)
        ret_img.paste(img, (st_w, st_h))
        return ret_img


class ToTensor:
    """
    A wrapper from ToTensor in pytorch, see torchvision.transformers.ToTensor for explanation.
    """

    def __init__(self):
        self.t_transformer = transforms.ToTensor()

    def __call__(self, imgs: Image or tuple) -> torch.Tensor:
        if not isinstance(imgs, tuple):
            imgs = [imgs]
        ret_tensor = list()
        for img in imgs:
            ret_tensor.append(self.t_transformer(img))
        ret_tensor = torch.stack(ret_tensor, dim=0)
        return ret_tensor


class Normalize:
    """
    Normalize a tensor image with mean and standard deviation.

    Hyper-Params
        mean (sequence): sequence of means for each channel.
        std (sequence): sequence of standard deviations for each channel.
    """
    default_hyper_params = {
        "mean": [0.485, 0.456, 0.406],
        "std": [0.229, 0.224, 0.225],
    }

    def __init__(self):
        for v in ["mean", "std"]:
            self.__dict__[v] = np.array(self.default_hyper_params[v])[None, :, None, None]
            self.__dict__[v] = torch.from_numpy(self.__dict__[v]).float()

    def __call__(self, tensor: torch.tensor) -> torch.tensor:
        assert tensor.ndimension() == 4
        tensor.sub_(self.mean).div_(self.std)
        return tensor


class CollateFn:
    """
    A wrapper for torch.utils.data.dataloader.default_collate.
    """
    default_hyper_params = dict()

    def __init__(self):
        pass

    def __call__(self, batch: List[Dict]) -> Dict[str, torch.tensor]:
        assert isinstance(batch, list)
        assert isinstance(batch[0], dict)
        return default_collate(batch)


class Folder:
    """
    A folder function for loading images.

    Hyper-Params:
        use_bbox: bool, whether use bbox to crop image. When set to true,
            make sure that bbox attribute is provided in your data json and bbox format is [x1, y1, x2, y2].
    """
    default_hyper_params = {
        "use_bbox": False,
    }

    def __init__(self, data_json_path, transformer):
        """
        Args:
            data_json_path (str): the path for data json file.
            transformer (callable): a list of data augmentation operations.
        """
        with open(data_json_path, "rb") as f:
            self.data_info = pickle.load(f)

        self.data_json_path = data_json_path
        self.transformer = transformer
        self.classes, self.class_to_idx = self.find_classes(self.data_info["info_dicts"])

    def find_classes(self, info_dicts: Dict) -> (List, Dict):
        """
        Get the class names and the mapping relations.

        Args:
            info_dicts (dict): the dataset information contained the data json file.

        Returns:
            tuple (list, dict): a list of class names and a dict for projecting class name into int label.
        """
        classes = list()
        for i in range(len(info_dicts)):
            if info_dicts[i]["label"] not in classes:
                classes.append(info_dicts[i]["label"])
        classes.sort()
        class_to_idx = {classes[i]: i for i in range(len(classes))}
        return classes, class_to_idx

    def read_img(self, path: str) -> Image:
        """
        Load image.

        Args:
            path (str): the path of the image.

        Returns:
            image (Image): shape (H, W, C).
        """
        try:
            img = Image.open(path)
            img = img.convert("RGB")
            return img
        except Exception as e:
            print('[DataSet]: WARNING image can not be loaded: {}'.format(str(e)))
            return None

    def __len__(self) -> int:
        """
        Get the number of total training samples.

        Returns:
            length (int): the number of total training samples.
        """
        return len(self.data_info["info_dicts"])

    def __getitem__(self, idx: int) -> Dict:
        """
        Load the image and convert it to tensor for training.

        Args:
            idx (int): the serial number of the image.

        Returns:
            item (dict): the dict containing the image after augmentations, serial number and label.
        """
        info = self.data_info["info_dicts"][idx]
        img = self.read_img(info["path"])
        if self.default_hyper_params["use_bbox"]:
            assert info["bbox"] is not None, 'image {} does not have a bbox'.format(info["path"])
            x1, y1, x2, y2 = info["bbox"]
            box = map(int, (x1, y1, x2, y2))
            img = img.crop(box)
        img = self.transformer(img)
        return {"img": img, "idx": idx, "label": self.class_to_idx[info["label"]]}


class FeatureLoader:
    """
    A class for load features and information.
    """

    def __init__(self):
        self.feature_cache = dict()

    def _load_from_cache(self, fea_dir: str, feature_names: List[str]) -> (np.ndarray, Dict, Dict):
        """
        Load feature and its information from cache.

        Args:
            fea_dir (str): the path of features to be loaded.
            feature_names (list): a list of str indicating which feature will be output.

        Returns:
            tuple (np.ndarray, Dict, Dict): a stacked feature, a list of dicts which describes the image information of each feature,
                and a dict map from feature name to its position.
        """
        assert fea_dir in self.feature_cache, "feature in {} not cached!".format(fea_dir)

        feature_dict = self.feature_cache[fea_dir]["feature_dict"]
        info_dicts = self.feature_cache[fea_dir]["info_dicts"]
        stacked_feature = list()
        pos_info = dict()

        if len(feature_names) == 1 and feature_names[0] == "all":
            feature_names = list(feature_dict.keys())
        feature_names = np.sort(feature_names)

        st_idx = 0
        for name in feature_names:
            assert name in feature_dict, "invalid feature name: {} not in {}!".format(name, feature_dict.keys())
            stacked_feature.append(feature_dict[name])
            pos_info[name] = (st_idx, st_idx + stacked_feature[-1].shape[1])
            st_idx = st_idx + stacked_feature[-1].shape[1]
        stacked_feature = np.concatenate(stacked_feature, axis=1)

        print("[LoadFeature] Success, total {} images, \n feature names: {}".format(
            len(info_dicts),
            pos_info.keys())
        )
        return stacked_feature, info_dicts, pos_info

    def load(self, fea_dir: str, feature_names: List[str]) -> (np.ndarray, Dict, Dict):
        """
        Load and concat feature from feature directory.

        Args:
            fea_dir (str): the path of features to be loaded.
            feature_names (list): a list of str indicating which feature will be output.

        Returns:
            tuple (np.ndarray, Dict, Dict): a stacked feature, a list of dicts which describes the image information of each feature,
                and a dict map from feature name to its position.

        """
        assert os.path.exists(fea_dir), "non-exist feature path: {}".format(fea_dir)

        if fea_dir in self.feature_cache:
            return self._load_from_cache(fea_dir, feature_names)

        feature_dict = dict()
        info_dicts = list()

        for root, dirs, files in os.walk(fea_dir):
            for file in files:
                if file.endswith(".json"):
                    print("[LoadFeature]: loading feature from {}...".format(os.path.join(root, file)))
                    with open(os.path.join(root, file), "rb") as f:
                        part_info = pickle.load(f)
                        for info in part_info["info_dicts"]:
                            for key in info["feature"].keys():
                                if key not in feature_dict:
                                    feature_dict[key] = list()
                                feature_dict[key].append(info["feature"][key])
                            del info["feature"]
                            info_dicts.append(info)
        for key, fea in feature_dict.items():
            fea = np.array(fea)
            feature_dict[key] = fea

        self.feature_cache[fea_dir] = {
            "feature_dict": feature_dict,
            "info_dicts": info_dicts
        }

        return self._load_from_cache(fea_dir, feature_names)


feature_loader = FeatureLoader()
