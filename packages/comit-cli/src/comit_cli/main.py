# Copyright 2026 CoalOmit Authors.
# Licensed under the Apache License, Version 2.0.

import importlib.util
import os
import sys
import click
import torch
from comit_core.config import COMITConfig
from comit_core.pipeline import run_pipeline
from comit_cli.formatters.table import format_table
from comit_cli.formatters.markdown import format_markdown
from comit_cli.formatters.json_fmt import format_json


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """COMIT: Carbon-Aware Compression CLI."""
    pass


@cli.command()
@click.argument("model_path", type=click.Path(exists=True))
@click.option("--methods", "-m", default="int8,int4", help="Comma-separated quantization methods.")
@click.option("--region", "-r", default="GLOBAL", help="Region code for grid intensity.")
@click.option("--traffic", "-t", default=1_000_000, type=int, help="Monthly inference volume.")
@click.option("--format", "-f", "fmt", type=click.Choice(["table", "markdown", "json"]), default="table")
@click.option("--runs", "-n", default=100, type=int, help="Inference benchmark runs.")
def run(model_path, methods, region, traffic, fmt, runs):
    """Run COMIT profiling on a PyTorch model file."""
    click.echo(f"Loading model script: {model_path}")
    spec = importlib.util.spec_from_file_location("user_model_module", model_path)
    if spec is None or spec.loader is None:
        click.echo(f"Error: Could not load module at {model_path}", err=True)
        sys.exit(1)

    module = importlib.util.module_from_spec(spec)
    sys.path.insert(0, os.path.dirname(os.path.abspath(model_path)))
    spec.loader.exec_module(module)

    model = getattr(module, "model", None) or (getattr(module, "get_model", lambda: None)())
    sample_input = getattr(module, "sample_input", None)

    if model is None:
        click.echo("Error: Model file must define a top-level 'model' or 'get_model()' function.", err=True)
        sys.exit(1)

    if sample_input is None:
        sample_input = (torch.randn(1, 128),)

    methods_list = [m.strip() for m in methods.split(",") if m.strip()]
    config = COMITConfig(
        model_path=model_path,
        methods=methods_list,
        n_inference_runs=runs,
        region=region,
        monthly_inferences=traffic,
        output_format=fmt
    )

    report = run_pipeline(model, sample_input, config)

    if fmt == "table":
        format_table(report)
    elif fmt == "markdown":
        format_markdown(report)
    elif fmt == "json":
        format_json(report)


if __name__ == "__main__":
    cli()
