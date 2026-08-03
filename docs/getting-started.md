# Getting Started with Carbon Lens (CAC)

Carbon Lens is an open-source toolkit that profiles the accuracy, latency, energy, and carbon emissions of PyTorch models under different quantization strategies.

## 1. Installation

```bash
# Clone the repository
git clone https://github.com/AAYUSHI003/carbon_lens.git
cd carbon_lens

# Install core engine & CLI in editable mode
pip install -e packages/cac-core -e packages/cac-cli
```

## 2. Quickstart Usage

Create a model script `my_model.py`:

```python
import torch
import torch.nn as nn

class MyModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc = nn.Linear(128, 10)
    def forward(self, x):
        return self.fc(x)

model = MyModel()
sample_input = (torch.randn(1, 128),)
```

Run the `cac` CLI command:

```bash
cac run my_model.py --methods int8,int4 --region US --traffic 1000000
```

## 3. Command Options

- `--methods`, `-m`: Comma-separated quantization methods (`int8`, `int4`).
- `--region`, `-r`: ISO country code (`US`, `EU`, `IN`, `FR`, `DE`, `JP`, etc.).
- `--traffic`, `-t`: Projected monthly inference traffic volume (default: 1,000,000).
- `--format`, `-f`: Output format (`table`, `markdown`, `json`).
