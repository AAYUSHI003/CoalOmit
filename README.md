# Carbon-Aware Compression (CAC) 🌍⚡

**See the carbon cost of your model — before you ship it.**

CAC is a developer-first toolkit that measures the **accuracy, latency, energy, and carbon** trade-offs of model compression (quantization, pruning, distillation) so ML engineers can make energy-aware decisions the same way they already track accuracy and latency.

```bash
cac run model.py
```

```
                     Baseline (FP16)     INT8            INT4
Accuracy             94.2%               93.8% (-0.4)    91.1% (-3.1)
Latency (p50)        42ms                27ms  (-36%)    18ms  (-57%)
Energy / 1k infer.   0.021 kWh           0.014 kWh       0.009 kWh
Est. CO2 / month*    128 kg              84 kg (-34%)    55 kg (-57%)

*at your current traffic + regional grid intensity
```
## ♻️ Why CAC?

Today, most ML teams track:

- Accuracy
- Latency
- Memory

But very few track:

- Energy consumption
- Carbon emissions

CAC helps developers make energy-aware deployment decisions by exposing these metrics alongside traditional performance benchmarks.

## 🚨 The Problem

- **ML engineers** can measure accuracy and latency on every PR — but are completely blind to the carbon delta of a model change.
- **Sustainability/ESG teams** only see aggregate cloud bills, not workload-level emissions — they can't tell which model, which team, or which PR is driving energy use.
- Result: "carbon bloat" accumulates silently across ML pipelines until it shows up in a corporate audit, months too late to act on.

CAC bridges this gap: bottom-up, workload-specific carbon metrics generated directly in the developer's environment, feeding into enterprise-grade reporting.

## ✨ Features

- **`cac-core`** — the compression + measurement engine. Supports multiple quantization backends (INT8, INT4, GPTQ, AWQ, ONNX) behind a common interface, plus accuracy, latency, and energy/FLOP-based benchmarking.
- **`cac-cli`** — the free developer entry point: `cac run model.py` → terminal table, Markdown, or JSON output.
- **`cac-action`** — a GitHub Action that posts the before/after comparison table directly as a PR comment.
- **Carbon projection** — per-inference results projected to monthly kg CO2 using regional grid-intensity data.
- **Enterprise dashboard** *(proprietary)* — historical trends, org-wide reporting, and CSRD/SB253-formatted compliance exports.

## 🧩 Supported

Frameworks

- PyTorch
- ONNX Runtime
- Hugging Face Transformers

Compression

- Dynamic Quantization
- Static Quantization
- GPTQ
- AWQ
- Pruning
- Distillation

Coming Soon

- TensorRT
- TensorFlow

## 📦 Project Structure

```
carbon-aware-compression/
├── packages/           # open source — cac-core (engine), cac-cli, cac-action
├── enterprise/         # proprietary — dashboard, hosted API, compliance exports, billing
├── benchmarks/         # the data corpus — per-model/hardware/method results + methodology
├── examples/           # quickstart notebooks (BERT, LLaMA) + GitHub Action demo
├── docs/               # getting started, methodology, CI/CD integration, API reference
└── scripts/            # e.g. refreshing public grid-intensity data
```

## 🚀 Quickstart

```bash
git clone https://github.com/AAYUSHI003/carbon_lens.git
cd carbon-aware-compression
pip install -e packages/cac-core
pip install -e packages/cac-cli

cac run path/to/your_model.py
```

See [`examples/quickstart_bert.ipynb`](./examples/quickstart_bert.ipynb) or [`examples/quickstart_llama.ipynb`](./examples/quickstart_llama.ipynb) for a full walkthrough.

## 🔧 CI/CD Integration

Add the GitHub Action to get a comparison table posted on every PR — see [`examples/github_action_demo`](./examples/github_action_demo) and [`docs/ci-cd-integration.md`](./docs/ci-cd-integration.md).

## 📊 Benchmarks

Per-model, per-hardware, per-method results live in [`benchmarks/models/`](./benchmarks/models). We're transparent about what's measured vs. estimated — see [`benchmarks/methodology.md`](./benchmarks/methodology.md).

## 🎯 Why It Matters

Regulatory frameworks — the EU CSRD, SEC climate disclosure rules, and India's BRSR (moving toward mandatory Scope 3 disclosure) — are turning granular carbon reporting into a compliance requirement. CAC gives engineering teams the workload-level data those reports actually need, instead of relying on aggregate cloud billing as a proxy.

## 🤝 Contributing

Contributions to the open-core packages are welcome! Please read [CONTRIBUTING.md](./CONTRIBUTING.md) and our [Code of Conduct](./CODE_OF_CONDUCT.md) first.

## 🔒 Security

Found a vulnerability? See [SECURITY.md](./SECURITY.md) for reporting instructions.

## 📄 License

Open-core project: `packages/` is licensed under [LICENSE](./LICENSE); `enterprise/` is proprietary — see [LICENSE-COMMERCIAL](./LICENSE-COMMERCIAL).

## 📌 Changelog

See [CHANGELOG.md](./CHANGELOG.md).



# Carbon Lens — Project Analysis & Summary

## What Is It?

**Carbon Lens** (formally **Carbon-Aware Compression / CAC**) is a developer-first toolkit designed to measure the **accuracy, latency, energy, and CO₂ trade-offs** of ML model compression techniques (quantization, pruning, distillation). It lets ML engineers see the carbon cost of their models *before* shipping them — the same way they already track accuracy and latency.

The project is structured as an **open-core** product:
- An **open-source** developer toolkit (free CLI + core engine)
- A **proprietary enterprise** tier (dashboard, hosted API, compliance exports, billing)

---

## The Problem It Solves

| Stakeholder | Pain Point |
|---|---|
| **ML Engineers** | Can measure accuracy & latency on every PR, but are completely blind to the carbon delta of a model change |
| **Sustainability / ESG Teams** | Only see aggregate cloud bills, not workload-level emissions — can't attribute energy use to a specific model, team, or PR |
| **Result** | "Carbon bloat" silently accumulates across ML pipelines until it appears in a corporate audit, months too late to act on |

CAC bridges the gap with bottom-up, workload-specific carbon metrics generated directly in the developer's environment and feeding into enterprise-grade reporting.

---

## Intended Features

### Open-Source Packages (`packages/`)

#### 1. `cac-core` — Compression & Measurement Engine
The heart of the project. Planned modules:

| Submodule | Files | Purpose |
|---|---|---|
| `quantize/` | [base.py](file:///c:/Users/hp/carbon_lens/packages/cac-core/src/cac_core/quantize/base.py), [int8.py](file:///c:/Users/hp/carbon_lens/packages/cac-core/src/cac_core/quantize/int8.py), [int4.py](file:///c:/Users/hp/carbon_lens/packages/cac-core/src/cac_core/quantize/int4.py) | Apply INT8 / INT4 quantization to models, with a pluggable base class for GPTQ, AWQ, ONNX backends |
| `benchmark/` | [accuracy.py](file:///c:/Users/hp/carbon_lens/packages/cac-core/src/cac_core/benchmark/accuracy.py), [latency.py](file:///c:/Users/hp/carbon_lens/packages/cac-core/src/cac_core/benchmark/latency.py), [energy.py](file:///c:/Users/hp/carbon_lens/packages/cac-core/src/cac_core/benchmark/energy.py) | Measure accuracy drop, p50/p99 latency, and energy (kWh) per inference batch |
| `carbon/` | [grid-intensity.py](file:///c:/Users/hp/carbon_lens/packages/cac-core/src/cac_core/carbon/grid-intensity.py), [projector.py](file:///c:/Users/hp/carbon_lens/packages/cac-core/src/cac_core/carbon/projector.py) | Look up regional grid carbon intensity (gCO₂/kWh) and project per-inference energy to monthly kg CO₂ |
| Top-level | [config.py](file:///c:/Users/hp/carbon_lens/packages/cac-core/src/cac_core/config.py), [report.py](file:///c:/Users/hp/carbon_lens/packages/cac-core/src/cac_core/report.py) | Configuration management and report generation |

#### 2. `cac-cli` — Developer CLI
- Entry point: [main.py](file:///c:/Users/hp/carbon_lens/packages/cac-cli/src/cac_cli/main.py)
- Planned `formatters/` directory for terminal table, Markdown, and JSON output
- Usage: `cac run model.py` → prints a comparison table (baseline vs. compressed variants)

#### 3. `cac-action` — GitHub Action
- [action.yml](file:///c:/Users/hp/carbon_lens/packages/cac-action/action.yml) + [Dockerfile](file:///c:/Users/hp/carbon_lens/packages/cac-action/Dockerfile)
- Posts a before/after carbon comparison table as a PR comment on every pull request

### Enterprise Tier (`enterprise/`) — Proprietary

| Component | Purpose |
|---|---|
| `api/` | Hosted API for ingesting and querying carbon metrics at scale |
| `dashboard-web/` | Web dashboard for historical trends and org-wide carbon reporting |
| `compliance-export/` | CSRD / SB253 / BRSR-formatted compliance report exports |
| `billing/` | Usage-based billing for the hosted service |

### Supporting Directories

| Directory | Purpose |
|---|---|
| `benchmarks/` | Pre-computed per-model/hardware/method results + [methodology](file:///c:/Users/hp/carbon_lens/benchmarks/methodolgy.md) documentation |
| `examples/` | Quickstart notebooks (BERT, LLaMA) + [GitHub Action demo](file:///c:/Users/hp/carbon_lens/examples/github_action_demo) |
| `docs/` | [Getting started](file:///c:/Users/hp/carbon_lens/docs/getting-started.md), [Methodology](file:///c:/Users/hp/carbon_lens/docs/methodology.md), [CI/CD integration](file:///c:/Users/hp/carbon_lens/docs/ci-cd-integration.md), [API reference](file:///c:/Users/hp/carbon_lens/docs/api-reference.md) |
| `scripts/` | [update_grid_intensity_data.py](file:///c:/Users/hp/carbon_lens/scripts/update_grid_intensity_data.py) — refreshes public grid-intensity data |

---

## Architecture Overview

```mermaid
graph TD
    subgraph "Open Source"
        CLI["cac-cli<br/>Developer CLI"]
        CORE["cac-core<br/>Engine"]
        ACTION["cac-action<br/>GitHub Action"]
        
        CLI --> CORE
        ACTION --> CORE
        
        CORE --> Q["quantize/<br/>INT8 · INT4 · GPTQ · AWQ"]
        CORE --> B["benchmark/<br/>accuracy · latency · energy"]
        CORE --> C["carbon/<br/>grid-intensity · projector"]
    end
    
    subgraph "Enterprise (Proprietary)"
        API["Hosted API"]
        DASH["Dashboard Web"]
        COMP["Compliance Export<br/>CSRD · SB253 · BRSR"]
        BILL["Billing"]
        
        API --> DASH
        API --> COMP
        API --> BILL
    end
    
    CORE -.->|metrics feed| API
```

---

## Current Implementation Status

> [!CAUTION]
> **The project is a scaffolding / skeleton only.** Every single source code file (`.py`, `.toml`, `.yml`, `Dockerfile`) is **empty** (0 bytes). No actual implementation code exists yet.

### What exists (with content):
| File | Status |
|---|---|
| [README.md](file:///c:/Users/hp/carbon_lens/README.md) | ✅ Fully written (4.5 KB) — excellent project pitch with clear problem statement, feature list, and quickstart |
| [SECURITY.md](file:///c:/Users/hp/carbon_lens/SECURITY.md) | ✅ Fully written (3.2 KB) — comprehensive security policy |
| [CODE_OF_CONDUCT.md](file:///c:/Users/hp/carbon_lens/CODE_OF_CONDUCT.md) | ✅ Fully written (2.6 KB) — based on Contributor Covenant v2.1 |
| [.gitignore](file:///c:/Users/hp/carbon_lens/.gitignore) | ✅ Standard Python gitignore |

### What is empty (0 bytes):
- **All 14 Python source files** across `cac-core`, `cac-cli`
- **All configuration files**: `pyproject.toml` (root + cac-core), `action.yml`, `Dockerfile`
- **All 4 documentation files** in `docs/`
- **All supporting files**: `CONTRIBUTING.md`, `CHANGELOG.md`, `LICENSE`, `LICENSE-COMMERCIAL`, `benchmarks/methodolgy.md`
- **All enterprise directories**: `api/`, `billing/`, `compliance-export/`, `dashboard-web/` — completely empty
- **All test directories**: empty
- **GitHub workflows & issue templates**: directories exist but are empty

---

## Regulatory Context

The README calls out three regulatory frameworks driving demand:

| Framework | Scope |
|---|---|
| **EU CSRD** | Corporate Sustainability Reporting Directive — mandatory granular carbon reporting for EU companies |
| **SEC Climate Disclosure** | US Securities and Exchange Commission climate risk disclosure rules |
| **India BRSR** | Business Responsibility and Sustainability Reporting — moving toward mandatory Scope 3 disclosure |

CAC positions itself as providing the workload-level data these compliance reports actually need, rather than relying on aggregate cloud billing as a proxy.

---

## Technology Stack (Planned)

- **Language**: Python
- **Package manager**: pip with `pyproject.toml`
- **Model compression**: INT8, INT4, GPTQ, AWQ, ONNX backends
- **CI/CD**: GitHub Actions (Docker-based)
- **Licensing**: Open-core (open-source packages + proprietary enterprise)

---

## Summary Assessment

| Dimension | Assessment |
|---|---|
| **Concept** | 🟢 Strong — addresses a real, growing gap between ML engineering and sustainability reporting |
| **Architecture** | 🟢 Well-designed — clean separation into core engine, CLI, GitHub Action, and enterprise tiers |
| **Documentation** | 🟡 Partially done — excellent README and security policy, but all technical docs are empty stubs |
| **Implementation** | 🔴 Not started — every source file is 0 bytes; this is purely a project scaffold |
| **Maturity** | 📐 **Skeleton / Blueprint stage** — ready for implementation to begin |

> [!IMPORTANT]
> This is a well-conceived project blueprint with a professional repository structure and excellent README.
