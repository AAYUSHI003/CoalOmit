# Copyright 2026 CoalOmit Authors.
# Licensed under the Apache License, Version 2.0.

from dataclasses import dataclass
from typing import Tuple
import torch
import torch.nn as nn
from torch.utils.flop_counter import FlopCounterMode


@dataclass
class EnergyResult:
    """FLOP and energy consumption statistics."""
    total_flops: int
    energy_per_inference_wh: float
    energy_per_1k_kwh: float


# Energy per FLOP constants in Joules per FLOP by precision
ENERGY_PER_FLOP_JOULES = {
    "fp32": 5.0e-14,
    "fp16": 2.5e-14,
    "int8": 1.25e-14,
    "int4": 0.8e-14,
}


def estimate_energy(
    model: nn.Module,
    sample_input: Tuple[torch.Tensor, ...],
    n_inferences: int = 1000,
    precision: str = "fp32"
) -> EnergyResult:
    """Estimate FLOPs and energy footprint using FlopCounterMode."""
    model.eval()
    if not isinstance(sample_input, tuple):
        sample_input = (sample_input,)

    total_flops = 0
    try:
        flop_counter = FlopCounterMode(display=False)
        with flop_counter:
            with torch.no_grad():
                model(*sample_input)
        total_flops = flop_counter.get_total_flops()
    except Exception:
        # Fallback estimation based on linear/conv module parameter counts
        total_flops = sum(p.numel() * 2 for p in model.parameters())

    e_j = ENERGY_PER_FLOP_JOULES.get(precision.lower(), 5.0e-14)
    energy_per_inference_joules = total_flops * e_j
    energy_per_inference_wh = energy_per_inference_joules / 3600.0
    energy_per_1k_kwh = (energy_per_inference_wh * 1000.0) / 1000.0

    return EnergyResult(
        total_flops=total_flops,
        energy_per_inference_wh=float(round(energy_per_inference_wh, 8)),
        energy_per_1k_kwh=float(round(energy_per_1k_kwh, 6))
    )
