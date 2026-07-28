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
