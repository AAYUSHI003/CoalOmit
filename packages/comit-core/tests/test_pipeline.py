# Copyright 2026 CoalOmIT Authors.
# Licensed under the Apache License, Version 2.0.

import torch
import torch.nn as nn
from comit_core.config import COMITConfig
from comit_core.pipeline import run_pipeline


class SimpleModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc = nn.Linear(128, 10)
    def forward(self, x):
        return self.fc(x)


def test_run_pipeline():
    model = SimpleModel()
    sample = (torch.randn(1, 128),)
    cfg = COMITConfig(methods=["int8", "int4"], n_inference_runs=5)
    report = run_pipeline(model, sample, cfg)
    assert len(report.results) == 3  # Baseline + int8 + int4
    rows = report.to_rows()
    assert len(rows) == 3
