# Changelog

All notable changes to CarbonLens will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial public repository structure: `packages/` (cac-core, cac-cli, cac-action), `enterprise/`, `benchmarks/`, `examples/`, `docs/`, and `scripts/`.
- Core compression + measurement engine (`cac-core`) with support for INT8, INT4, GPTQ, AWQ, and ONNX quantization backends.
- Command-line entry point (`cac-cli`): `cac run model.py` for terminal, Markdown, or JSON output.
- GitHub Action (`cac-action`) that posts before/after comparison tables as PR comments.
- Carbon projection based on regional grid-intensity data, reporting estimated monthly CO2 impact per model.
- Quickstart notebooks for BERT and LLaMA under `examples/`.
- Contribution guidelines, code of conduct, and security policy.

### Changed
- N/A (first tracked release cycle).

### Fixed
- N/A (first tracked release cycle).

---

## Release Notes Format

Each released version below should follow this structure:

```
## [X.Y.Z] - YYYY-MM-DD

### Added
- New features.

### Changed
- Changes to existing functionality.

### Deprecated
- Features that will be removed in an upcoming release.

### Removed
- Features removed in this release.

### Fixed
- Bug fixes.

### Security
- Vulnerability fixes (see SECURITY.md for reporting).
```

[Unreleased]: https://github.com/AAYUSHI003/carbon_lens/compare/v0.1.0...HEAD
