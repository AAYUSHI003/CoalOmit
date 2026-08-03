# Copyright 2026 Carbon Lens Authors.
# Licensed under the Apache License, Version 2.0.

from dataclasses import dataclass


@dataclass
class CarbonProjection:
    """Monthly and annual CO2 projections."""
    monthly_kwh: float
    monthly_kg_co2: float
    annual_kg_co2: float


def project_monthly_co2(
    energy_per_inference_wh: float,
    monthly_inferences: int,
    grid_intensity_gco2_kwh: float
) -> CarbonProjection:
    """Project monthly energy and carbon emissions."""
    total_wh = energy_per_inference_wh * monthly_inferences
    monthly_kwh = total_wh / 1000.0
    monthly_g_co2 = monthly_kwh * grid_intensity_gco2_kwh
    monthly_kg_co2 = monthly_g_co2 / 1000.0
    annual_kg_co2 = monthly_kg_co2 * 12.0

    return CarbonProjection(
        monthly_kwh=round(monthly_kwh, 4),
        monthly_kg_co2=round(monthly_kg_co2, 2),
        annual_kg_co2=round(annual_kg_co2, 2)
    )
