# Copyright 2026 Carbon Lens Authors.
# Licensed under the Apache License, Version 2.0.

from dataclasses import dataclass, field
from typing import List


@dataclass
class CACConfig:
    """Configuration options for a Carbon-Aware Compression run."""

    model_path: str = ""
    methods: List[str] = field(default_factory=lambda: ["int8", "int4"])
    n_inference_runs: int = 100
    region: str = "GLOBAL"
    monthly_inferences: int = 1_000_000
    output_format: str = "table"  # "table", "markdown", "json"
    device: str = "cpu"
