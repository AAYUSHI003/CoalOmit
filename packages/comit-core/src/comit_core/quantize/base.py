# Copyright 2026 CoalOmit Authors.
# Licensed under the Apache License, Version 2.0.

from abc import ABC, abstractmethod
import torch
import torch.nn as nn


class Quantizer(ABC):
    """Abstract base class for model quantizers."""

    @abstractmethod
    def quantize(self, model: nn.Module) -> nn.Module:
        """Quantize the given PyTorch model."""
        pass

    @abstractmethod
    def method_name(self) -> str:
        """Return the name of the quantization method."""
        pass

    def get_model_size_mb(self, model: nn.Module) -> float:
        """Calculate total parameter size of the model in Megabytes."""
        param_size = 0
        for param in model.parameters():
            param_size += param.nelement() * param.element_size()
        buffer_size = 0
        for buffer in model.buffers():
            buffer_size += buffer.nelement() * buffer.element_size()
        size_all_mb = (param_size + buffer_size) / (1024 ** 2)
        return float(round(size_all_mb, 4))
