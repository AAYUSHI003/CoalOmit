# Copyright 2026 CoalOmIT Authors.
# Licensed under the Apache License, Version 2.0.

import torch
import torch.nn as nn
from comit_core.benchmark.latency import measure_latency
from comit_core.benchmark.energy import estimate_energy


class SimpleModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc = nn.Linear(128, 10)
    def forward(self, x):
        return self.fc(x)


def test_measure_latency():
    model = SimpleModel()
    sample = (torch.randn(1, 128),)
    res = measure_latency(model, sample, n_runs=20, warmup=2)
    assert res.p50_ms >= 0
    assert res.mean_ms >= 0


def test_estimate_energy():
    model = SimpleModel()
    sample = (torch.randn(1, 128),)
    res = estimate_energy(model, sample, precision="fp32")
    assert res.total_flops >= 0
    assert res.energy_per_inference_wh >= 0


def test_latency_warmup():
    model = SimpleModel()
    sample = (torch.randn(1, 128),)
    res = measure_latency(model, sample, n_runs=10, warmup=5)
    assert res.std_ms >= 0
