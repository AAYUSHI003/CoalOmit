# Contributing to CarbonLens

Thanks for your interest in contributing! This guide covers how to get set up, what we expect from contributions, and how the review process works.

CarbonLens is an open-core project: contributions here apply to the open-source packages under `packages/` (`cac-core`, `cac-cli`, `cac-action`), plus `benchmarks/`, `examples/`, `docs/`, and `scripts/`. The `enterprise/` directory is proprietary and not open to external contributions — see [LICENSE-COMMERCIAL](./LICENSE-COMMERCIAL).

Please also read our [Code of Conduct](./CODE_OF_CONDUCT.md) before participating.

## Ways to Contribute

- **Bug reports** — open an issue with steps to reproduce, expected vs. actual behavior, and your environment (OS, Python version, hardware/accelerator if relevant).
- **Feature requests** — open an issue describing the use case, not just the implementation you have in mind. We'll discuss approach before any code is written.
- **Bug fixes and features** — see the workflow below.
- **New quantization/compression backends** — these usually need a design discussion first (open an issue) since they touch the shared `cac-core` interface.
- **Benchmarks** — additions to `benchmarks/models/` are especially welcome; see `benchmarks/methodology.md` for what's expected in terms of reproducibility.
- **Documentation** — fixes to `docs/`, docstrings, or example notebooks are always appreciated, even small ones.

## Getting Started

```bash
git clone https://github.com/AAYUSHI003/carbon_lens.git
cd carbon-aware-compression

# Install the open-source packages in editable mode
pip install -e packages/cac-core
pip install -e packages/cac-cli

# Install development dependencies
pip install -e ".[dev]"
```

Run the test suite before making changes, to confirm your environment is set up correctly:

```bash
pytest
```

## Development Workflow

1. **Fork** the repository and create a branch off `main`:
   ```bash
   git checkout -b fix/short-description
   ```
2. **Make your changes**, keeping commits focused and scoped to a single logical change.
3. **Add tests** for any new behavior or bug fix. PRs that change measurable outputs (accuracy, latency, energy estimates) should include a rationale for the change in the PR description, not just in code comments.
4. **Run the full test suite and linters** locally before opening a PR:
   ```bash
   pytest
   ruff check .
   ```
5. **Update documentation** if your change affects public APIs, CLI flags, or the GitHub Action's inputs/outputs.
6. **Open a pull request** against `main`, filling out the PR template. Link any related issue.

## Pull Request Guidelines

- Keep PRs focused — one fix or feature per PR is easier to review and safer to revert if needed.
- Write a clear PR description: what changed, why, and how you tested it.
- New public functions, classes, and CLI commands should have docstrings and, where relevant, an entry in `docs/`.
- If you're adding a new compression backend or benchmark, include the methodology/assumptions so results are reproducible (see `benchmarks/methodology.md`).
- Be responsive to review feedback — PRs that go quiet for a long time may be closed and can be reopened when you're ready to pick it back up.
- CI must pass before merge. If CI is failing for reasons unrelated to your change, mention it in the PR and a maintainer will take a look.

## Commit Messages

We don't enforce a strict format, but please write commit messages that explain *why* a change was made, not just what changed. Reference issue numbers where relevant (e.g. `Fixes #42`).

## Code Style

- Python code is formatted and linted with `ruff`; please run it before submitting.
- Match the existing style and structure of the module you're editing rather than introducing a new pattern.
- Prefer clear, explicit code over cleverness — this is measurement/benchmarking infrastructure, and readability matters for trust in the numbers it produces.

## Reporting Security Issues

Please do **not** open a public issue for security vulnerabilities. Follow the process in [SECURITY.md](./SECURITY.md) instead.

## Questions

If something in this guide is unclear, or you're not sure whether a change is a good fit, open an issue or start a discussion before investing time in a PR — we're happy to help you find the right place to contribute.
