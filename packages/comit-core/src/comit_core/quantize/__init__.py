# Copyright 2026 CoalOmit Authors.
# Licensed under the Apache License, Version 2.0.

"""Quantization module for model compression backends."""

from comit_core.quantize.base import Quantizer
from comit_core.quantize.int8 import Int8Quantizer
from comit_core.quantize.int4 import Int4Quantizer
from comit_core.quantize.registry import get_quantizer, QUANTIZERS

__all__ = [
    "Quantizer",
    "Int8Quantizer",
    "Int4Quantizer",
    "get_quantizer",
    "QUANTIZERS",
]
