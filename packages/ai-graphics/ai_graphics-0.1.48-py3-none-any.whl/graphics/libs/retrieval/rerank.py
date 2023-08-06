import torch

__all__ = ['ReRanker']


class ReRanker:
    """
    Directly return features without any re-rank operations.
    """
    default_hyper_params = dict()

    def __init__(self):
        pass

    def __call__(self, query_feature: torch.tensor, gallery_feature: torch.tensor, dis: torch.tensor or None = None,
                 sorted_index: torch.tensor or None = None) -> torch.tensor:
        if sorted_index is None:
            sorted_index = torch.argsort(dis, dim=1)
        return sorted_index
