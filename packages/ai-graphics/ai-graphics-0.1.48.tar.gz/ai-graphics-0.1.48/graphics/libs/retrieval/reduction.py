from typing import List

import numpy as np
from sklearn.decomposition import PCA as SKPCA
from sklearn.preprocessing import normalize

from .dataset import feature_loader

__all__ = ['PCA',
           'L2Normalize']


class PCA:
    """
    Do the PCA transformation for dimension reduction.

    Hyper-Params:
        proj_dim (int): the dimension after reduction. If it is 0, then no reduction will be done.
        whiten (bool): whether do whiten.
        train_feature_dir (str): the path of features for training PCA.
        l2 (bool): whether do l2-normalization for the training features.
    """
    default_hyper_params = {
        "proj_dim": 512,
        "whiten": False,
        "train_feature_dir": "../datasets/features/caltech/gallery",
        "l2": True,
    }

    def __init__(self, feature_names: List[str]):
        self.feature_names = feature_names
        self.pca = SKPCA(n_components=self.default_hyper_params["proj_dim"], whiten=self.default_hyper_params["whiten"])
        self._train(self.default_hyper_params["train_feature_dir"])

    def _train(self, feature_dir: str) -> None:
        """
        Train the PCA.

        Args:
            feature_dir (str): the path of features for training PCA.
        """
        train_feature, _, _ = feature_loader.load(feature_dir, self.feature_names)
        if self.default_hyper_params["l2"]:
            train_feature = normalize(train_feature, norm="l2")
        self.pca.fit(train_feature)

    def __call__(self, feature: np.ndarray) -> np.ndarray:
        ori_feature = feature
        proj_feature = self.pca.transform(ori_feature)
        return proj_feature


class L2Normalize:
    """
    L2 normalize the features.
    """
    default_hyper_params = dict()

    def __init__(self, feature_names: List[str]):
        self.feature_names = feature_names
        pass

    def __call__(self, feature: np.ndarray) -> np.ndarray:
        return normalize(feature, norm="l2")
