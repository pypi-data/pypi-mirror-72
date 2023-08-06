from functools import partial
from typing import Dict

import numpy as np
import torch
import torch.nn as nn

__all__ = ['ResSeries']


class ResSeries:
    """
    The extractors for ResNet.

    Hyper-Parameters
        extract_features (list): indicates which feature maps to output. See available_features for available feature maps.
            If it is ["all"], then all available features will be output.
    """
    default_hyper_params = {
        "extract_features": ["pool5"],
    }

    available_features = ["pool5", "pool4", "pool3"]

    def __init__(self, model):
        """
        Args:
            model (nn.Module): the model for extracting features.
        """
        children = list(model.children())
        feature_modules = {
            "pool5": children[-3][-1].relu,
            "pool4": children[-4][-1].relu,
            "pool3": children[-5][-1].relu
        }
        assert len(self.default_hyper_params["extract_features"]) > 0

        self.model = model.eval()
        if torch.cuda.is_available():
            self.model.cuda()
            if torch.cuda.device_count() > 1:
                self.model = nn.DataParallel(self.model)
        self.feature_modules = feature_modules
        self.feature_buffer = dict()

        if self.default_hyper_params["extract_features"][0] == "all":
            self.default_hyper_params["extract_features"] = self.available_features
        for fea in self.default_hyper_params["extract_features"]:
            self.feature_buffer[fea] = dict()

        self._register_hook()

    def _register_hook(self) -> None:
        """
        Register hooks to output inner feature map.
        """

        def hook(feature_buffer, feature_name, module, input, output):
            feature_buffer[feature_name][str(output.device)] = output.data

        for feature in self.default_hyper_params["extract_features"]:
            assert feature in self.feature_modules, 'unknown feature {}!'.format(feature)
            self.feature_modules[feature].register_forward_hook(partial(hook, self.feature_buffer, feature))

    def __call__(self, x: torch.tensor) -> Dict:
        with torch.no_grad():
            self.model(x)
            ret = dict()
            for fea in self.default_hyper_params["extract_features"]:
                ret[fea] = list()
                devices = list(self.feature_buffer[fea].keys())
                devices = np.sort(devices)
                for d in devices:
                    ret[fea].append(self.feature_buffer[fea][d])
                ret[fea] = torch.cat(ret[fea], dim=0)
        return ret
