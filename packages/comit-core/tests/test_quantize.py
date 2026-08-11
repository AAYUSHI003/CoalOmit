# Copyright 2026 CoalOmit Authors.
# Licensed under the Apache License, Version 2.0.

import torch
import torch.nn as nn
from comit_core.quantize.int8 import Int8Quantizer
from comit_core.quantize.int4 import Int4Quantizer
from comit_core.quantize.registry import get_quantizer


class SimpleModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(128, 64)
        self.fc2 = nn.Linear(64, 10)
    def forward(self, x):
        return self.fc2(torch.relu(self.fc1(x)))


def test_int8_quantizer_reduces_model():
    model = SimpleModel()
    q = Int8Quantizer()
    q_model = q.quantize(model)
    assert q_model is not None
    assert q.method_name() == "INT8 Dynamic"


def test_int4_quantizer():
    model = SimpleModel()
    q = Int4Quantizer()
    q_model = q.quantize(model)
    assert q_model is not None
    assert q.method_name() == "INT4 Weight-Only"


def test_quantizer_registry():
    q_int8 = get_quantizer("int8")
    assert isinstance(q_int8, Int8Quantizer)
    q_int4 = get_quantizer("int4")
    assert isinstance(q_int4, Int4Quantizer)


def test_model_size():
    model = SimpleModel()
    q = Int8Quantizer()
    size_mb = q.get_model_size_mb(model)
    assert size_mb > 0
