# Copyright 2026 CoalOmIT Authors.
# Licensed under the Apache License, Version 2.0.

import copy
import torch
import torch.nn as nn
from comit_core.quantize.base import Quantizer


class Int8Quantizer(Quantizer):
    """INT8 dynamic quantization using PyTorch's native dynamic quantizer."""

    def method_name(self) -> str:
        return "INT8 Dynamic"

    def quantize(self, model: nn.Module) -> nn.Module:
        model_copy = copy.deepcopy(model)
        model_copy.eval()
        try:
            quantized_model = torch.ao.quantization.quantize_dynamic(
                model_copy,
                {nn.Linear, nn.LSTM, nn.GRU},
                dtype=torch.qint8
            )
            return quantized_model
        except Exception:
            return model_copy
