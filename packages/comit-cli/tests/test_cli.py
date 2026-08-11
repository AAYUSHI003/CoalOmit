# Copyright 2026 CoalOmit Authors.
# Licensed under the Apache License, Version 2.0.

from click.testing import CliRunner
from comit_cli.main import cli


def test_cli_help():
    runner = CliRunner()
    res = runner.invoke(cli, ["--help"])
    assert res.exit_code == 0
    assert "Carbon-Aware Compression CLI" in res.output


def test_cli_version():
    runner = CliRunner()
    res = runner.invoke(cli, ["--version"])
    assert res.exit_code == 0
    assert "0.1.0" in res.output
