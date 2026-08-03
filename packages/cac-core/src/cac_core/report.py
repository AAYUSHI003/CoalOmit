# Copyright 2026 Carbon Lens Authors.
# Licensed under the Apache License, Version 2.0.

from dataclasses import dataclass, asdict
from typing import List, Dict, Any
from cac_core.config import CACConfig
from cac_core.benchmark.accuracy import AccuracyResult
from cac_core.benchmark.latency import LatencyResult
from cac_core.benchmark.energy import EnergyResult
from cac_core.carbon.projector import CarbonProjection


@dataclass
class CompressionResult:
    """Consolidated result for a single compression strategy."""
    method: str
    accuracy: AccuracyResult
    latency: LatencyResult
    energy: EnergyResult
    carbon: CarbonProjection
    model_size_mb: float


class CACReport:
    """Aggregated compression report containing results for all evaluated strategies."""

    def __init__(self, results: List[CompressionResult], config: CACConfig):
        self.results = results
        self.config = config

    def to_dict(self) -> Dict[str, Any]:
        """Convert report to dictionary format."""
        return {
            "config": asdict(self.config),
            "results": [asdict(r) for r in self.results]
        }

    def to_rows(self) -> List[List[str]]:
        """Return tabulated string rows for table formatters."""
        rows = []
        baseline = self.results[0] if self.results else None
        baseline_latency = baseline.latency.p50_ms if baseline else 1.0
        baseline_carbon = baseline.carbon.monthly_kg_co2 if baseline else 1.0

        for r in self.results:
            lat_savings = 0.0
            if baseline_latency > 0:
                lat_savings = ((baseline_latency - r.latency.p50_ms) / baseline_latency) * 100.0

            co2_savings = 0.0
            if baseline_carbon > 0:
                co2_savings = ((baseline_carbon - r.carbon.monthly_kg_co2) / baseline_carbon) * 100.0

            acc_str = f"{r.accuracy.value * 100:.1f}%" if r.accuracy.value >= 0 else "N/A"
            if r.accuracy.delta != 0:
                acc_str += f" ({r.accuracy.delta * 100:+.1f}%)"

            lat_str = f"{r.latency.p50_ms:.1f}ms"
            if lat_savings != 0:
                lat_str += f" ({lat_savings:+.0f}%)"

            co2_str = f"{r.carbon.monthly_kg_co2:.1f} kg"
            if co2_savings != 0:
                co2_str += f" ({co2_savings:+.0f}%)"

            rows.append([
                r.method,
                acc_str,
                lat_str,
                f"{r.energy.energy_per_1k_kwh:.4f} kWh",
                co2_str,
                f"{r.model_size_mb:.2f} MB"
            ])
        return rows
