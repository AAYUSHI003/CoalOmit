# Python API Reference

## `comit_core.pipeline`

### `run_pipeline(model, sample_input, config, dataloader=None, metric_fn=None) -> COMITReport`

Orchestrates evaluation across baseline and requested quantization backends.

## `comit_core.config.COMITConfig`

Dataclass configuring model path, methods, region, traffic, and output format.
