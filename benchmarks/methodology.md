# Carbon Lens — Full Implementation Plan

Build the entire Carbon Lens (CAC) project from its current scaffold state to a working, installable toolkit.

## User Review Required

> [!IMPORTANT]
> **Licensing**: The plan uses **Apache 2.0** for open-source packages and a proprietary placeholder for enterprise. Confirm this is your intended license.

> [!IMPORTANT]
> **Scope**: This plan implements the full open-source toolkit (`cac-core`, `cac-cli`, `cac-action`) plus docs and tests. The **enterprise tier** (dashboard, API, billing, compliance) is left as placeholder directories since it requires infrastructure decisions (database, hosting, frontend framework) that should be a separate project.

## Open Questions

> [!WARNING]
> **GPU vs CPU focus**: The current plan targets **CPU-based quantization** (PyTorch native) for simplicity. GPU quantization (bitsandbytes, GPTQ, AWQ) can be added later as optional backends. Is this acceptable for v0.1?

> [!WARNING]
> **Grid intensity data**: The plan uses a **static JSON dataset** of national/regional carbon intensity averages as the default, with optional live API support (Electricity Maps) for real-time data. Is this approach okay, or do you want live API only?

---

## Proposed Changes

### Phase 1: Structure Cleanup & Fixes

Quick fixes to the existing scaffold before building.

#### [MODIFY] Rename `benchmarks/methodolgy.md` → `benchmarks/methodology.md`
- Fix the typo in the filename

#### [DELETE] `packages/cac_core/` (underscore variant)
- Remove the duplicate directory; keep only `packages/cac-core/`

#### [MODIFY] Rename `carbon/grid-intensity.py` → `carbon/grid_intensity.py`
- Hyphens are invalid in Python module names

#### [NEW] Add `__init__.py` files to all Python packages
- `packages/cac-core/src/cac_core/__init__.py`
- `packages/cac-core/src/cac_core/quantize/__init__.py`
- `packages/cac-core/src/cac_core/benchmark/__init__.py`
- `packages/cac-core/src/cac_core/carbon/__init__.py`
- `packages/cac-cli/src/cac_cli/__init__.py`
- `packages/cac-cli/src/cac_cli/formatters/__init__.py`

---

### Phase 2: cac-core — The Engine

The heart of the project. 3 submodules + 2 top-level modules.

#### [MODIFY] [config.py](file:///c:/Users/hp/carbon_lens/packages/cac-core/src/cac_core/config.py)
Configuration dataclass for a CAC run:
```python
@dataclass
class CACConfig:
    model_path: str                    # Path to the model script/file
    methods: list[str]                 # ["int8", "int4"]
    n_inference_runs: int = 100        # Number of inference runs for benchmarking
    region: str = "GLOBAL"             # Region code for grid intensity
    monthly_inferences: int = 1_000_000  # Projected monthly inference volume
    output_format: str = "table"       # "table", "markdown", "json"
    device: str = "cpu"                # Target device
```

---

#### Quantization Submodule (`quantize/`)

#### [MODIFY] [base.py](file:///c:/Users/hp/carbon_lens/packages/cac-core/src/cac_core/quantize/base.py)
Abstract base class for all quantization backends:
```python
class Quantizer(ABC):
    @abstractmethod
    def quantize(self, model: nn.Module) -> nn.Module: ...
    @abstractmethod
    def method_name(self) -> str: ...
    def get_model_size_mb(self, model: nn.Module) -> float: ...
```

#### [MODIFY] [int8.py](file:///c:/Users/hp/carbon_lens/packages/cac-core/src/cac_core/quantize/int8.py)
INT8 dynamic quantization using `torch.ao.quantization`:
```python
class Int8Quantizer(Quantizer):
    def quantize(self, model):
        return torch.ao.quantization.quantize_dynamic(
            model, {nn.Linear, nn.LSTM, nn.GRU}, dtype=torch.qint8
        )
```

#### [MODIFY] [int4.py](file:///c:/Users/hp/carbon_lens/packages/cac-core/src/cac_core/quantize/int4.py)
INT4 weight-only quantization. Uses simulated 4-bit packing (CPU-compatible) without requiring `torchao`/`bitsandbytes` as hard dependencies:
- Packs weights into 4-bit representation
- Provides a fallback that works on CPU
- Optional: detect and use `torchao.quantization.int4_weight_only()` if available

#### [NEW] [quantize/registry.py](file:///c:/Users/hp/carbon_lens/packages/cac-core/src/cac_core/quantize/registry.py)
Registry pattern to look up quantizers by name:
```python
QUANTIZERS = {"int8": Int8Quantizer, "int4": Int4Quantizer}
def get_quantizer(method: str) -> Quantizer: ...
```

---

#### Benchmark Submodule (`benchmark/`)

#### [MODIFY] [accuracy.py](file:///c:/Users/hp/carbon_lens/packages/cac-core/src/cac_core/benchmark/accuracy.py)
Measure accuracy delta between baseline and quantized models:
```python
def measure_accuracy(model, dataloader, metric_fn) -> float: ...
def compare_accuracy(baseline_acc, quantized_acc) -> AccuracyResult: ...
```
- `AccuracyResult` dataclass with `value`, `delta`, `delta_pct`
- Supports custom metric functions (default: top-1 accuracy)

#### [MODIFY] [latency.py](file:///c:/Users/hp/carbon_lens/packages/cac-core/src/cac_core/benchmark/latency.py)
Measure inference latency with warmup and statistics:
```python
def measure_latency(model, sample_input, n_runs=100, warmup=10) -> LatencyResult: ...
```
- `LatencyResult` dataclass: `mean_ms`, `p50_ms`, `p99_ms`, `std_ms`
- Uses `time.perf_counter_ns()` for high-resolution timing
- Warmup runs to stabilize measurements

#### [MODIFY] [energy.py](file:///c:/Users/hp/carbon_lens/packages/cac-core/src/cac_core/benchmark/energy.py)
Estimate energy consumption using FLOP counting:
```python
def estimate_energy(model, sample_input, n_inferences=1000, precision="fp32") -> EnergyResult: ...
```
- Uses `torch.utils.flop_counter.FlopCounterMode` for accurate FLOP counting
- Energy formula: `energy_wh = (flops * energy_per_flop_j + idle_power_w * time_s) / 3600`
- Per-precision energy constants: FP32 ~5e-14 J/FLOP, INT8 ~1.25e-14 J/FLOP, INT4 ~0.8e-14 J/FLOP
- `EnergyResult` dataclass: `total_flops`, `energy_per_inference_wh`, `energy_per_1k_kwh`

---

#### Carbon Submodule (`carbon/`)

#### [MODIFY] [grid_intensity.py](file:///c:/Users/hp/carbon_lens/packages/cac-core/src/cac_core/carbon/grid_intensity.py)
(Renamed from `grid-intensity.py`)

Regional carbon intensity lookup:
```python
def get_grid_intensity(region: str = "GLOBAL") -> float:  # gCO2/kWh
```
- Ships with a **static JSON dataset** (`data/grid_intensity.json`) of ~50 country/region averages
- Supports optional live lookup via Electricity Maps API (if `CAC_ELECTRICITY_MAPS_TOKEN` env var is set)
- Fallback: Global average ~475 gCO2/kWh

#### [NEW] [carbon/data/grid_intensity.json](file:///c:/Users/hp/carbon_lens/packages/cac-core/src/cac_core/carbon/data/grid_intensity.json)
Static dataset with entries like:
```json
{
  "GLOBAL": 475,
  "US": 380,
  "EU": 250,
  "IN": 630,
  "FR": 55,
  "DE": 350,
  "GB": 200,
  "CN": 555,
  "SE": 15,
  "NO": 10,
  ...
}
```

#### [MODIFY] [projector.py](file:///c:/Users/hp/carbon_lens/packages/cac-core/src/cac_core/carbon/projector.py)
Project per-inference energy to monthly CO2:
```python
def project_monthly_co2(
    energy_per_inference_wh: float,
    monthly_inferences: int,
    grid_intensity_gco2_kwh: float
) -> CarbonProjection: ...
```
- `CarbonProjection` dataclass: `monthly_kwh`, `monthly_kg_co2`, `annual_kg_co2`

---

#### Top-Level Modules

#### [MODIFY] [report.py](file:///c:/Users/hp/carbon_lens/packages/cac-core/src/cac_core/report.py)
Aggregate results from all submodules into a structured report:
```python
@dataclass
class CompressionResult:
    method: str           # "baseline", "int8", "int4"
    accuracy: AccuracyResult
    latency: LatencyResult
    energy: EnergyResult
    carbon: CarbonProjection
    model_size_mb: float

class CACReport:
    results: list[CompressionResult]
    config: CACConfig
    def to_dict(self) -> dict: ...
    def to_rows(self) -> list[list[str]]: ...  # For table rendering
```

#### [NEW] [pipeline.py](file:///c:/Users/hp/carbon_lens/packages/cac-core/src/cac_core/pipeline.py)
Orchestrator that ties everything together:
```python
def run_pipeline(model, sample_input, config: CACConfig,
                 dataloader=None, metric_fn=None) -> CACReport: ...
```
1. Measure baseline (FP16/FP32)
2. For each compression method: quantize → benchmark → project carbon
3. Return `CACReport` with all results

---

### Phase 3: cac-cli — Developer CLI

#### [MODIFY] [main.py](file:///c:/Users/hp/carbon_lens/packages/cac-cli/src/cac_cli/main.py)
Click-based CLI with `cac run` command:
```python
@click.group()
@click.version_option(version="0.1.0")
def cli(): ...

@cli.command()
@click.argument("model_path", type=click.Path(exists=True))
@click.option("--methods", "-m", default="int8,int4", help="Comma-separated quantization methods")
@click.option("--region", "-r", default="GLOBAL", help="Region code for grid intensity")
@click.option("--traffic", "-t", default=1_000_000, help="Monthly inference count")
@click.option("--format", "-f", "fmt", type=click.Choice(["table", "markdown", "json"]), default="table")
def run(model_path, methods, region, traffic, fmt): ...
```

#### [NEW] [formatters/table.py](file:///c:/Users/hp/carbon_lens/packages/cac-cli/src/cac_cli/formatters/table.py)
Rich terminal table formatter:
- Color-coded columns (green for improvements, red for degradation)
- Shows accuracy, latency (p50), energy/1k inferences, est. CO2/month
- Includes delta percentages vs. baseline

#### [NEW] [formatters/markdown.py](file:///c:/Users/hp/carbon_lens/packages/cac-cli/src/cac_cli/formatters/markdown.py)
Markdown table output (for PR comments, docs):
```markdown
| Metric | Baseline (FP16) | INT8 | INT4 |
|--------|-----------------|------|------|
| Accuracy | 94.2% | 93.8% (-0.4) | 91.1% (-3.1) |
...
```

#### [NEW] [formatters/json_fmt.py](file:///c:/Users/hp/carbon_lens/packages/cac-cli/src/cac_cli/formatters/json_fmt.py)
JSON output for programmatic consumption.

---

### Phase 4: Packaging & Configuration

#### [MODIFY] [pyproject.toml](file:///c:/Users/hp/carbon_lens/pyproject.toml) (root)
Workspace-level metadata only (not installable itself).

#### [MODIFY] [pyproject.toml](file:///c:/Users/hp/carbon_lens/packages/cac-core/pyproject.toml) (cac-core)
```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "cac-core"
version = "0.1.0"
description = "Carbon-Aware Compression engine for ML models"
requires-python = ">=3.9"
dependencies = [
    "torch>=2.0.0",
    "requests>=2.28.0",
]

[project.optional-dependencies]
dev = ["pytest>=7.0", "pytest-cov"]
```

#### [NEW] [pyproject.toml](file:///c:/Users/hp/carbon_lens/packages/cac-cli/pyproject.toml) (cac-cli)
```toml
[project]
name = "cac-cli"
version = "0.1.0"
dependencies = [
    "cac-core>=0.1.0",
    "click>=8.1.0",
    "rich>=13.0.0",
]

[project.scripts]
cac = "cac_cli.main:cli"
```

---

### Phase 5: Documentation & Governance

#### [MODIFY] [docs/getting-started.md](file:///c:/Users/hp/carbon_lens/docs/getting-started.md)
Installation instructions, first run, interpreting output.

#### [MODIFY] [docs/methodology.md](file:///c:/Users/hp/carbon_lens/docs/methodology.md)
How energy and carbon are estimated: FLOP counting, per-precision energy constants, grid intensity data sources, and what's measured vs. estimated.

#### [MODIFY] [docs/ci-cd-integration.md](file:///c:/Users/hp/carbon_lens/docs/ci-cd-integration.md)
How to add the GitHub Action to your workflow.

#### [MODIFY] [docs/api-reference.md](file:///c:/Users/hp/carbon_lens/docs/api-reference.md)
Python API reference for `cac-core` public classes and functions.

#### [MODIFY] [LICENSE](file:///c:/Users/hp/carbon_lens/LICENSE)
Apache License 2.0 full text.

#### [MODIFY] [LICENSE-COMMERCIAL](file:///c:/Users/hp/carbon_lens/LICENSE-COMMERCIAL)
Proprietary license placeholder for the enterprise tier.

#### [MODIFY] [CONTRIBUTING.md](file:///c:/Users/hp/carbon_lens/CONTRIBUTING.md)
How to contribute: branching strategy, PR process, code style, testing requirements.

#### [MODIFY] [CHANGELOG.md](file:///c:/Users/hp/carbon_lens/CHANGELOG.md)
Initial v0.1.0 changelog entry.

---

### Phase 6: cac-action — GitHub Action

#### [MODIFY] [action.yml](file:///c:/Users/hp/carbon_lens/packages/cac-action/action.yml)
GitHub Action definition:
```yaml
name: 'Carbon-Aware Compression Check'
description: 'Run CAC and post carbon comparison table as a PR comment'
inputs:
  model_path:
    description: 'Path to model script'
    required: true
  methods:
    description: 'Quantization methods (comma-separated)'
    default: 'int8,int4'
  region:
    description: 'Region code for grid intensity'
    default: 'GLOBAL'
runs:
  using: 'docker'
  image: 'Dockerfile'
```

#### [MODIFY] [Dockerfile](file:///c:/Users/hp/carbon_lens/packages/cac-action/Dockerfile)
Docker image based on Python 3.12 slim, installs cac-core + cac-cli, runs entrypoint.

#### [NEW] [src/entrypoint.py](file:///c:/Users/hp/carbon_lens/packages/cac-action/src/entrypoint.py)
Runs `cac run` with markdown output, posts result as a PR comment using GitHub API.

---

### Phase 7: Tests

#### [NEW] `packages/cac-core/tests/test_quantize.py`
- Test INT8 quantizer on a simple `nn.Linear` model
- Test INT4 quantizer produces smaller model
- Test quantizer registry lookup

#### [NEW] `packages/cac-core/tests/test_benchmark.py`
- Test latency measurement returns valid statistics
- Test energy estimation returns positive values
- Test accuracy measurement with a dummy metric

#### [NEW] `packages/cac-core/tests/test_carbon.py`
- Test grid intensity lookup for known regions
- Test CO2 projection math (known inputs → expected outputs)

#### [NEW] `packages/cac-core/tests/test_pipeline.py`
- End-to-end test: run pipeline on a small model, verify report structure

#### [NEW] `packages/cac-cli/tests/test_cli.py`
- Test CLI `--help` output
- Test `cac run` with a simple model file
- Test each output format (table, markdown, json)

---

### Phase 8: CI/CD

#### [NEW] `.github/workflows/ci.yml`
```yaml
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.9", "3.10", "3.11", "3.12"]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
      - run: pip install -e packages/cac-core[dev]
      - run: pip install -e packages/cac-cli
      - run: pytest packages/cac-core/tests/ packages/cac-cli/tests/ -v --cov
```

#### [NEW] `.github/ISSUE_TEMPLATE/bug_report.md`
#### [NEW] `.github/ISSUE_TEMPLATE/feature_request.md`

---

## Dependency Summary

| Package | cac-core | cac-cli | cac-action |
|---------|----------|---------|------------|
| `torch>=2.0` | Yes | (via cac-core) | (via cac-core) |
| `requests>=2.28` | Yes | (via cac-core) | (via cac-core) |
| `click>=8.1` | No | Yes | No |
| `rich>=13.0` | No | Yes | No |
| `pytest>=7.0` | Dev only | Dev only | No |

---

## Verification Plan

### Automated Tests
```bash
# Install packages in dev mode
pip install -e packages/cac-core[dev]
pip install -e packages/cac-cli

# Run all tests
pytest packages/cac-core/tests/ packages/cac-cli/tests/ -v --cov

# Test CLI manually
cac run examples/quickstart_model.py --methods int8,int4 --region IN --format table
cac run examples/quickstart_model.py --format markdown
cac run examples/quickstart_model.py --format json
```

### Manual Verification
- Verify `pip install -e packages/cac-core` succeeds cleanly
- Verify `pip install -e packages/cac-cli` succeeds and `cac` command is available
- Verify `cac run` produces a formatted comparison table in the terminal
- Verify markdown output matches the format shown in the README
- Verify JSON output is valid and parseable
- Verify grid intensity lookup works for multiple regions
- Verify the GitHub Action Dockerfile builds successfully
