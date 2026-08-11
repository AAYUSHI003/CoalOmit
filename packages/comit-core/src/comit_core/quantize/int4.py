# Copyright 2026 CoalOmIT Authors.
# Licensed under the Apache License, Version 2.0.

import copy
import torch
import torch.nn as nn
from comit_core.quantize.base import Quantizer


class Int4Quantizer(Quantizer):
    """Simulated INT4 weight-only quantization (CPU compatible)."""

    def method_name(self) -> str:
        return "INT4 Weight-Only"

    def quantize(self, model: nn.Module) -> nn.Module:
        model_copy = copy.deepcopy(model)
        model_copy.eval()
        with torch.no_grad():
            for param in model_copy.parameters():
                if param.requires_grad or param.data is not None:
                    # Uniform 16-level quantization simulation
                    min_val, max_val = param.data.min(), param.data.max()
                    if max_val > min_val:
                        scale = (max_val - min_val) / 15.0
                        q_data = torch.round((param.data - min_val) / scale)
                        param.data = (q_data * scale) + min_val
        return model_copy

    def get_model_size_mb(self, model: nn.Module) -> float:
        # Approximate size as 1/8th of FP32 for linear/dense parameters
        base_size = super().get_model_size_mb(model)
        return float(round(base_size * 0.25, 4))
