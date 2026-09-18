"""Turn saved test predictions into a submission, then check it.

    python examples/quickstart/inference.py

The example also scores the submission against the held-out answers, which a real
competition would not let you do. It is here to make one habit visible: the
out-of-fold score and the leaderboard score are different numbers, and the gap
between them is information you should be tracking from day one.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
from sklearn.metrics import roc_auc_score

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from commons.paths import get_repo_root, preds_dir  # noqa: E402

DATA_DIR = Path(__file__).resolve().parent / "data"
NAME = "quickstart_hgb"
ID, TARGET = "id", "target"
THRESHOLD = 0.5


def main() -> None:
    """Write submission.csv next to the example data and report the held-out score."""
    pred = pd.read_csv(preds_dir() / f"test_{NAME}.csv")
    sub = pd.DataFrame({ID: pred[ID], TARGET: (pred["pred"] >= THRESHOLD).astype(int)})
    path = DATA_DIR / "submission.csv"
    sub.to_csv(path, index=False)
    print(f"wrote {path}  (positive rate {sub[TARGET].mean():.3f})")

    answers = pd.read_csv(DATA_DIR / "answers.csv")
    merged = answers.merge(pred, on=ID)
    print(f'"leaderboard" AUC : {roc_auc_score(merged[TARGET], merged["pred"]):.5f}')
    print("  ^ compare with the OOF AUC from train.py. Track the gap, not just the number.")

    root = get_repo_root()
    print(f"\nnow validate it:\n  uv run python {root / 'scripts' / 'validate_submission.py'} \\")
    print(f"      {path} --sample {DATA_DIR / 'sample_submit.csv'}")


if __name__ == "__main__":
    main()
