# Copyright 2026 CoalOmit Authors.
# Licensed under the Apache License, Version 2.0.

from comit_core.report import COMITReport


def format_markdown(report: COMITReport) -> str:
    """Format report into markdown table representation."""
    rows = report.to_rows()
    md = []
    md.append(f"### Carbon-Aware Compression Report (Region: {report.config.region})\n")
    md.append("| Strategy | Accuracy | Latency (p50) | Energy / 1k | Est. CO2 / Mo | Size (MB) |")
    md.append("|---|:---:|---:|---:|---:|---:|")
    for r in rows:
        md.append(f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} | {r[5]} |")
    md.append(f"\n_*Projected for {report.config.monthly_inferences:,} monthly inferences._\n")

    output = "\n".join(md)
    print(output)
    return output
