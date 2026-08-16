<div align="center">

# CØ CoalØmit
### REDUCE NOW SUSTAIN FOREVER

[![Live Website](https://img.shields.io/badge/🌐_Live_Website-aayushi003.github.io%2FCoalOmit-FF6E00?style=for-the-badge)](https://aayushi003.github.io/CoalOmit/)
[![Live Presentation](https://img.shields.io/badge/📊_Interactive_Deck-Pitch_Deck-D97706?style=for-the-badge)](https://aayushi003.github.io/CoalOmit/pitch_deck.html)
[![License](https://img.shields.io/badge/License-Apache_2.0-FF6E00?style=for-the-badge&logo=apache)](LICENSE)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.x_Native-D97706?style=for-the-badge&logo=pytorch&logoColor=white)](https://pytorch.org/)

**Quantify, Compare & Eliminate the Carbon Footprint of AI Models in Seconds**

</div>

---

## ⚡ What Is CoalØmit?

**CoalØmit** is an open-source Green AI platform and developer toolkit designed to measure and reduce the **accuracy, latency, energy, and CO₂ trade-offs** of AI model compression techniques (quantization, pruning, distillation). 

It lets ML engineers see the carbon cost of their models *before* shipping them — right inside their existing workflow.

---

## 🎯 The Problem It Solves

| Stakeholder | Pain Point | CoalØmit Solution |
| :--- | :--- | :--- |
| **ML Engineers** | Can measure accuracy & latency on every PR, but are completely blind to carbon emissions | Runs `cac run model.py` to output a real-time Pareto trade-off matrix across Accuracy, Latency, and CO₂ |
| **Sustainability / ESG Teams** | Only see aggregate annual cloud bills — can't attribute energy use to specific models or PRs | Automates bottom-up engineering telemetry with instant exports for EU CSRD & SEC ESG reporting |
| **Enterprise Impact** | "Carbon bloat" silently accumulates across ML clusters until expensive annual audits | **`cac-action`** GitHub Action automatically comments carbon comparison tables on PRs before code merges |

---

## 🚀 Key Impact Metrics

- **57% Avg. CO₂ Reduction per Model:** Achieved via INT4 Weight-Only Quantization
- **2.3x Inference Speedup:** p50 latency improved from 42ms to 18ms
- **87% Model Memory Savings:** Footprint reduced from 440MB to 55MB
- **35+ Regional Power Grids Mapped:** Live gCO₂/kWh grid intensity coverage

---

## 💻 Quickstart — Run Locally in 5 Seconds

```bash
# Clone the repository
git clone https://github.com/AAYUSHI003/CoalOmit.git
cd CoalOmit

# Run the CLI carbon trade-off report on your model
python -m cac_cli run model.py --methods int8,int4 --region IN
```

### 📊 Terminal Output Preview:
```
❯ cac run model.py --methods int8,int4 --region IN
Loading model script: model.py

  CoalØmit Report (Region: IN — 708 gCO2/kWh)

  Strategy              Accuracy    Latency (p50)   Energy / 1k     Est. CO2 / Mo   Size (MB)
  ──────────────────────────────────────────────────────────────────────────────────────────────
  Baseline (FP32)       94.2%       42ms            0.021 kWh       128 kg          440 MB
  INT8 Dynamic          93.8%       27ms (-36%)     0.014 kWh       84 kg (-34%)    110 MB
  INT4 Weight-Only      91.1%       18ms (-57%)     0.009 kWh       55 kg (-57%)    55 MB

  * Projected for 1,000,000 monthly inferences.
```

---

## 🌐 Live Links & Resources

- 🌐 **Live Production Website:** [https://aayushi003.github.io/CoalOmit/](https://aayushi003.github.io/CoalOmit/)
- 📊 **Interactive Pitch Deck:** [https://aayushi003.github.io/CoalOmit/pitch_deck.html](https://aayushi003.github.io/CoalOmit/pitch_deck.html)
- 📄 **PowerPoint Deck (.pptx):** [`CoalOmIT_Pitch_Deck.pptx`](file:///c:/Users/hp/CoalOmIT/CoalOmIT_Pitch_Deck.pptx)

---

## 📜 License

Distributed under the Apache 2.0 License. See `LICENSE` for more information.
