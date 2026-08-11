# Copyright 2026 CoalOmit Authors.
# Licensed under the Apache License, Version 2.0.

from dataclasses import dataclass
import time
from typing import Tuple
import torch
import torch.nn as nn


@dataclass
class LatencyResult:
    """Latency measurement statistics in milliseconds."""
    mean_ms: float
    p50_ms: float
    p99_ms: float
    std_ms: float


def measure_latency(
    model: nn.Module,
    sample_input: Tuple[torch.Tensor, ...],
    n_runs: int = 100,
    warmup: int = 10
) -> LatencyResult:
    """Measure inference latency with warmup and percentiles."""
    model.eval()
    if not isinstance(sample_input, tuple):
        sample_input = (sample_input,)

    with torch.no_grad():
        # Warmup runs
        for _ in range(warmup):
            model(*sample_input)

        timings = []
        for _ in range(n_runs):
            t0 = time.perf_counter_ns()
            model(*sample_input)
            t1 = time.perf_counter_ns()
            timings.append((t1 - t0) / 1e6)  # convert to ms

    timings.sort()
    mean_ms = sum(timings) / len(timings)
    p50_idx = int(len(timings) * 0.50)
    p99_idx = int(len(timings) * 0.99)
    p50_ms = timings[p50_idx]
    p99_ms = timings[min(p99_idx, len(timings) - 1)]
    variance = sum((x - mean_ms) ** 2 for x in timings) / len(timings)
    std_ms = variance ** 0.5

    return LatencyResult(
        mean_ms=round(mean_ms, 3),
        p50_ms=round(p50_ms, 3),
        p99_ms=round(p99_ms, 3),
        std_ms=round(std_ms, 3)
    )
