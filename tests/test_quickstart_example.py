"""Smoke test: the quickstart example runs end to end and produces a valid submission."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples" / "quickstart"
DATA = EXAMPLE / "data"


def _run(script: Path, *args: str) -> None:
    proc = subprocess.run(
        [sys.executable, str(script), *args], cwd=ROOT, capture_output=True, text=True
    )
    assert proc.returncode == 0, f"{script.name} failed:\n{proc.stdout}\n{proc.stderr}"


def test_quickstart_end_to_end() -> None:
    """make_data -> train -> inference -> validate_submission, all green."""
    _run(EXAMPLE / "make_data.py", "--rows", "180")
    _run(EXAMPLE / "train.py")
    _run(EXAMPLE / "inference.py")

    submission = pd.read_csv(DATA / "submission.csv")
    sample = pd.read_csv(DATA / "sample_submit.csv")
    assert list(submission.columns) == list(sample.columns)
    assert len(submission) == len(sample)
    assert submission["target"].isin([0, 1]).all()

    _run(
        ROOT / "scripts" / "validate_submission.py",
        str(DATA / "submission.csv"),
        "--sample",
        str(DATA / "sample_submit.csv"),
    )
