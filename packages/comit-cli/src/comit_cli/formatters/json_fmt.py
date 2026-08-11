# Copyright 2026 CoalOmit Authors.
# Licensed under the Apache License, Version 2.0.

import json
from comit_core.report import COMITReport


def format_json(report: COMITReport) -> str:
    """Format report into pretty-printed JSON."""
    output = json.dumps(report.to_dict(), indent=2)
    print(output)
    return output
