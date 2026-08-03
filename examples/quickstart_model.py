# Copyright 2026 Carbon Lens Authors.
# Licensed under the Apache License, Version 2.0.

import torch
import torch.nn as nn


class SampleClassifier(nn.Module):
    """Sample PyTorch Neural Network for CAC Profiling."""
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(512, 256)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(256, 64)
        self.fc3 = nn.Linear(64, 10)

    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        return self.fc3(x)


# CAC auto-detects 'model' and 'sample_input'
model = SampleClassifier()
sample_input = (torch.randn(1, 512),)
