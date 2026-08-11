# Copyright 2026 CoalOmit Authors.
# Licensed under the Apache License, Version 2.0.

from comit_core.carbon.grid_intensity import get_grid_intensity
from comit_core.carbon.projector import project_monthly_co2


def test_grid_intensity_known_region():
    assert get_grid_intensity("US") == 380.0
    assert get_grid_intensity("EU") == 250.0
    assert get_grid_intensity("IN") == 630.0


def test_grid_intensity_global_fallback():
    assert get_grid_intensity("UNKNOWN_REGION_XYZ") == 475.0


def test_grid_intensity_case_insensitive():
    assert get_grid_intensity("us") == 380.0


def test_project_co2():
    res = project_monthly_co2(
        energy_per_inference_wh=0.001,
        monthly_inferences=1_000_000,
        grid_intensity_gco2_kwh=380.0
    )
    assert res.monthly_kwh == 1.0
    assert res.monthly_kg_co2 == 0.38
    assert res.annual_kg_co2 == 4.56
