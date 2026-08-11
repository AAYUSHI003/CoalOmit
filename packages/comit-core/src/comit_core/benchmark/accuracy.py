# Copyright 2026 CoalOmIT Authors.
# Licensed under the Apache License, Version 2.0.

from dataclasses import dataclass
from typing import Callable, Optional
import torch
import torch.nn as nn


@dataclass
class AccuracyResult:
    """Accuracy measurement result."""
    value: float
    delta: float = 0.0
    delta_pct: float = 0.0


def measure_accuracy(
    model: nn.Module,
    dataloader: Optional[object] = None,
    metric_fn: Optional[Callable] = None
) -> AccuracyResult:
    """Measure model accuracy using dataloader and metric function."""
    if dataloader is None or metric_fn is None:
        return AccuracyResult(value=-1.0, delta=0.0, delta_pct=0.0)

    model.eval()
    correct = 0
    total = 0
    with torch.no_grad():
        for inputs, targets in dataloader:
            outputs = model(inputs)
            acc = metric_fn(outputs, targets)
            correct += acc * len(targets)
            total += len(targets)

    final_val = float(correct / total) if total > 0 else 0.0
    return AccuracyResult(value=final_val, delta=0.0, delta_pct=0.0)


def compare_accuracy(baseline_acc: float, quantized_acc: float) -> AccuracyResult:
    """Compare baseline accuracy against quantized accuracy."""
    if baseline_acc < 0 or quantized_acc < 0:
        return AccuracyResult(value=quantized_acc, delta=0.0, delta_pct=0.0)
    delta = quantized_acc - baseline_acc
    delta_pct = (delta / baseline_acc * 100.0) if baseline_acc > 0 else 0.0
    return AccuracyResult(value=quantized_acc, delta=round(delta, 4), delta_pct=round(delta_pct, 2))
