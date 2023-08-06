import torch

from .metric import KNN


class DBA:
    """
    Every feature in the database is replaced with a weighted sum of the point’s own value and those of its top k nearest neighbors (k-NN).
    c.f. https://www.robots.ox.ac.uk/~vgg/publications/2012/Arandjelovic12/arandjelovic12.pdf

    Hyper-Params:
        enhance_k (int): number of the nearest points to be calculated.
    """
    default_hyper_params = {
        "enhance_k": 10,
    }

    def __init__(self):
        knn_hps = {
            "top_k": self.default_hyper_params["enhance_k"] + 1,
        }
        self.knn = KNN(knn_hps)

    def __call__(self, feature: torch.tensor) -> torch.tensor:
        _, sorted_idx = self.knn(feature, feature)
        sorted_idx = sorted_idx[:, 1:].reshape(-1)

        arg_fea = feature[sorted_idx].view(feature.shape[0], -1, feature.shape[1]).sum(dim=1)
        feature = feature + arg_fea

        feature = feature / torch.norm(feature, dim=1, keepdim=True)

        return feature
