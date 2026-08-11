# Copyright 2026 CoalOmit Authors.
# Licensed under the Apache License, Version 2.0.

from typing import Dict, Type
from comit_core.quantize.base import Quantizer
from comit_core.quantize.int8 import Int8Quantizer
from comit_core.quantize.int4 import Int4Quantizer

QUANTIZERS: Dict[str, Type[Quantizer]] = {
    "int8": Int8Quantizer,
    "int4": Int4Quantizer,
}


def get_quantizer(method: str) -> Quantizer:
    """Lookup and instantiate a quantizer backend by method name."""
    method_key = method.lower().strip()
    if method_key not in QUANTIZERS:
        raise ValueError(f"Unknown quantization method '{method}'. Available: {list(QUANTIZERS.keys())}")
    return QUANTIZERS[method_key]()
