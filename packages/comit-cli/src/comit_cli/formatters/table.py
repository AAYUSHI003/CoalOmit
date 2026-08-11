# Copyright 2026 CoalOmit Authors.
# Licensed under the Apache License, Version 2.0.

from rich.console import Console
from rich.table import Table
from comit_core.report import COMITReport


def format_table(report: COMITReport) -> None:
    """Render report as a rich terminal table."""
    console = Console()
    table = Table(
        title=f"Carbon-Aware Compression Report (Region: {report.config.region})",
        header_style="bold cyan",
        border_style="bright_blue"
    )

    table.add_column("Strategy", style="bold white", no_wrap=True)
    table.add_column("Accuracy", justify="center")
    table.add_column("Latency (p50)", justify="right", style="magenta")
    table.add_column("Energy / 1k", justify="right", style="yellow")
    table.add_column("Est. CO2 / Mo", justify="right", style="bold green")
    table.add_column("Size (MB)", justify="right", style="dim")

    rows = report.to_rows()
    for row in rows:
        table.add_row(*row)

    console.print()
    console.print(table)
    console.print(f"[dim]* Projected based on {report.config.monthly_inferences:,} monthly inferences.[/dim]")
    console.print()
