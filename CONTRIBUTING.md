# Contributing to ML Competition Template

Thank you for your interest in contributing! This project provides a robust, discipline-first template for competitive machine learning workflows powered by Claude Code.

Please keep pull requests focused. Do not include competition datasets, generated model
artifacts, credentials, API keys, or personal information.

## Development Workflow

1. **Prerequisites**
   - Python >= 3.12
   - [uv](https://docs.astral.sh/uv/)

2. **Setup**
   ```bash
   uv sync --all-groups
   ```

3. **Running Quality Checks**
   Before submitting a PR, ensure all checks pass:
   ```bash
   bash scripts/run_quality_checks.sh
   ```
   This runs:
   - `ruff check .` and `ruff format --check .`
   - `mypy src scripts`
   - `pytest`
   - Data protection and sensitive pattern checks (`scripts/check_no_raw_data_commit.py`, `scripts/check_no_sensitive_patterns.py`)
   - Agent documentation integrity check (`scripts/validate_agent_docs.py`)

## Pull requests

Before opening a PR:

- Explain the user-facing problem and the smallest complete solution.
- Add or update tests and documentation when behavior changes.
- Run `bash scripts/run_quality_checks.sh`.
- Confirm that no files under `data/raw/` or `data/external/` are included.

By contributing, you agree that your work is provided under this repository's MIT License.

## Core Principles

- **Zero-Cost Priority**: Default workflows and tools must not require paid GPU rentals or paid proprietary APIs.
- **Data Protection**: Never commit dataset files (`data/raw/`, `data/external/`) or secrets/tokens.
- **Discipline & Reproducibility**: CV-first validation over public LB fitting.
