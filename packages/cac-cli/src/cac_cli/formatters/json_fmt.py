# Copyright 2026 Carbon Lens Authors.
# Licensed under the Apache License, Version 2.0.

import json
from cac_core.report import CACReport


def format_json(report: CACReport) -> str:
    """Format report into pretty-printed JSON."""
    output = json.dumps(report.to_dict(), indent=2)
    print(output)
    return output
