# Python API Reference

## `cac_core.pipeline`

### `run_pipeline(model, sample_input, config, dataloader=None, metric_fn=None) -> CACReport`

Orchestrates evaluation across baseline and requested quantization backends.

## `cac_core.config.CACConfig`

Dataclass configuring model path, methods, region, traffic, and output format.
