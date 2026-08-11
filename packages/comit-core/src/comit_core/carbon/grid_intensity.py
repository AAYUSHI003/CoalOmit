# Copyright 2026 CoalOmIT Authors.
# Licensed under the Apache License, Version 2.0.

import json
from pathlib import Path

_DATA_FILE = Path(__file__).parent / "data" / "grid_intensity.json"


def get_grid_intensity(region: str = "GLOBAL") -> float:
    """Retrieve carbon intensity (gCO2/kWh) for a given region."""
    region_clean = region.strip().upper()
    if _DATA_FILE.exists():
        try:
            with open(_DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return float(data.get(region_clean, data.get("GLOBAL", 475)))
        except Exception:
            pass
    return 475.0
