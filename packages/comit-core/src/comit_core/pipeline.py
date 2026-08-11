# Copyright 2026 CoalOmit Authors.
# Licensed under the Apache License, Version 2.0.

from typing import Optional, Tuple, Callable
import torch
import torch.nn as nn
from comit_core.config import COMITConfig
from comit_core.quantize.base import Quantizer
from comit_core.quantize.registry import get_quantizer
from comit_core.benchmark.accuracy import measure_accuracy, compare_accuracy
from comit_core.benchmark.latency import measure_latency
from comit_core.benchmark.energy import estimate_energy
from comit_core.carbon.grid_intensity import get_grid_intensity
from comit_core.carbon.projector import project_monthly_co2
from comit_core.report import CompressionResult, COMITReport


class BaselineQuantizer(Quantizer):
    def method_name(self) -> str:
        return "Baseline (FP32)"
    def quantize(self, model: nn.Module) -> nn.Module:
        return model


def run_pipeline(
    model: nn.Module,
    sample_input: Tuple[torch.Tensor, ...],
    config: COMITConfig,
    dataloader: Optional[object] = None,
    metric_fn: Optional[Callable] = None
) -> COMITReport:
    """Orchestrate full evaluation pipeline for baseline and compressed models."""
    grid_intensity = get_grid_intensity(config.region)
    results = []

    # 1. Evaluate Baseline
    baseline_q = BaselineQuantizer()
    base_size = baseline_q.get_model_size_mb(model)
    base_acc = measure_accuracy(model, dataloader, metric_fn)
    base_lat = measure_latency(model, sample_input, n_runs=config.n_inference_runs)
    base_energy = estimate_energy(model, sample_input, precision="fp32")
    base_carbon = project_monthly_co2(
        base_energy.energy_per_inference_wh,
        config.monthly_inferences,
        grid_intensity
    )

    results.append(CompressionResult(
        method="Baseline (FP32)",
        accuracy=base_acc,
        latency=base_lat,
        energy=base_energy,
        carbon=base_carbon,
        model_size_mb=base_size
    ))

    # 2. Evaluate Requested Compression Backends
    for method_name in config.methods:
        try:
            quantizer = get_quantizer(method_name)
            q_model = quantizer.quantize(model)
            q_size = quantizer.get_model_size_mb(q_model)
            q_acc_raw = measure_accuracy(q_model, dataloader, metric_fn)
            q_acc = compare_accuracy(base_acc.value, q_acc_raw.value)
            q_lat = measure_latency(q_model, sample_input, n_runs=config.n_inference_runs)
            precision_key = "int8" if "8" in method_name else "int4"
            q_energy = estimate_energy(q_model, sample_input, precision=precision_key)
            q_carbon = project_monthly_co2(
                q_energy.energy_per_inference_wh,
                config.monthly_inferences,
                grid_intensity
            )

            results.append(CompressionResult(
                method=quantizer.method_name(),
                accuracy=q_acc,
                latency=q_lat,
                energy=q_energy,
                carbon=q_carbon,
                model_size_mb=q_size
            ))
        except Exception as e:
            print(f"Warning: Failed to run quantization '{method_name}': {e}")

    return COMITReport(results=results, config=config)
