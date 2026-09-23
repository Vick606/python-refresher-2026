<div align="center">

# Python Refresher 2026

**A test-backed Python refresher for developers who know the syntax and want the engineering habits required to ship reliable, observable, reproducible software.**

[![CI](https://github.com/Vick606/python-refresher-2026/actions/workflows/ci.yml/badge.svg)](https://github.com/Vick606/python-refresher-2026/actions/workflows/ci.yml)
[![Python 3.14+](https://img.shields.io/badge/python-3.14%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![uv](https://img.shields.io/badge/uv-managed-DE5FE9)](https://docs.astral.sh/uv/)
[![License: MIT](https://img.shields.io/badge/license-MIT-EAB308)](LICENSE)

</div>

---

## The gap

Python tutorials teach syntax. Professional work also requires reproducible environments, dependency locking, regression tests, static analysis, debugging, performance awareness, CI, and deliberate concurrency choices.

This repository is a practical refresher for that gap: the space between *I can write Python* and *I can ship Python that another developer can reproduce, inspect, and trust*.

## Current foundation

The project baseline is live and enforced in GitHub Actions:

- Python 3.14 is pinned for the project.
- Dependencies are managed with `uv`.
- `uv.lock` records exact resolved dependencies for reproducible installs.
- Ruff checks lint and formatting rules.
- pytest verifies the project runtime contract.
- CI runs linting, format checks, and tests on every push and pull request.

```powershell
uv sync
uv run ruff check .
uv run ruff format --check .
uv run pytest
```

## What the published units will demonstrate

| Area | Focus |
|---|---|
| Professional baseline | Project reproducibility, testing, type contracts, static analysis, and CI |
| Runtime reasoning | Names and objects, data-structure cost, iteration, functions, errors, and the data model |
| Operating code | Debugging, profiling, concurrency decisions, and high-value standard-library tools |
| Modern Python | The practical Python 3.8 to 3.14 changes that affect how code is written and reviewed |

Each unit will begin with a realistic failure, constraint, or boundary. It will include a runnable example, a test for the non-obvious behaviour, and links to the primary documentation.

## Security-aware by design

The examples will favour boundaries that matter in production and later AI-security work: untrusted input, structured data, file handling, subprocesses, hashing, secrets, timeouts, logging, cancellation, and reproducible evidence from tests.

This is not an AI-security project. It is the Python foundation required to build those projects well.

## Intentionally out of scope

This is not a beginner course. It deliberately skips:

- basic syntax and introductory `for` / `while` material;
- list-method walkthroughs and to-do applications;
- OOP taught through animal examples;
- notebooks, data-science exercises, machine-learning projects, and web frameworks.

Those resources already exist everywhere. This repository focuses on the reasoning and engineering practice that follows.

## Principles

1. **Evidence over claims.** If a behaviour matters, make it runnable and test it.
2. **Primary sources over folklore.** Link to official Python, uv, pytest, Ruff, and GitHub Actions documentation.
3. **One meaningful change per commit.** The history should explain how the project became reliable.
4. **No filler units.** If a topic does not improve reasoning, reliability, observability, or reproducibility, it does not belong here.

## Status

Foundation complete. Learning units are being added incrementally.

## License

MIT

