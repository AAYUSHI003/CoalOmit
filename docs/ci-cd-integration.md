# CI/CD Integration Guide

CoalOmit provides a ready-to-use GitHub Action (`comit-action`) to evaluate model PRs automatically.

## Workflow Example (`.github/workflows/comit.yml`)

```yaml
name: Carbon Compression Check

on:
  pull_request:
    branches: [ main ]

jobs:
  carbon-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run CoalOmit Check
        uses: ./packages/comit-action
        with:
          model_path: 'models/classifier.py'
          region: 'US'
          traffic: '5000000'
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```
