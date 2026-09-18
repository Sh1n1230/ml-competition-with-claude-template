"""Baseline for the quickstart example: repeated stratified CV, OOF saved for later.

    python examples/quickstart/train.py

What this demonstrates (and what `/baseline` asks you to reproduce on real data):

* the fold scheme is chosen first and stated in one place,
* every transform is fitted **inside** the fold,
* out-of-fold and test predictions are written in the same shape, so any later
  blending step can pick them up without re-running anything,
* the score reported is the out-of-fold score, never a fitted-on-everything score.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import RepeatedStratifiedKFold

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from commons.paths import ensure_parent_dir, preds_dir  # noqa: E402

DATA_DIR = Path(__file__).resolve().parent / "data"
NAME = "quickstart_hgb"
ID, TARGET = "id", "target"
N_SPLITS, N_REPEATS, SEED = 5, 3, 42


def main() -> None:
    """Fit under CV, report the out-of-fold score, save OOF and test predictions."""
    train = pd.read_csv(DATA_DIR / "train.csv")
    test = pd.read_csv(DATA_DIR / "test.csv")
    y = train[TARGET].to_numpy()
    x = train.drop(columns=[ID, TARGET])
    x_test = test.drop(columns=[ID])[x.columns]

    oof = np.zeros(len(y))
    test_pred = np.zeros(len(x_test))
    fold_scores: list[float] = []

    cv = RepeatedStratifiedKFold(n_splits=N_SPLITS, n_repeats=N_REPEATS, random_state=SEED)
    for tr, va in cv.split(x, y):
        model = HistGradientBoostingClassifier(max_iter=200, learning_rate=0.06, random_state=SEED)
        model.fit(x.iloc[tr], y[tr])
        p_va = model.predict_proba(x.iloc[va])[:, 1]
        oof[va] += p_va / N_REPEATS
        test_pred += model.predict_proba(x_test)[:, 1] / (N_SPLITS * N_REPEATS)
        fold_scores.append(roc_auc_score(y[va], p_va))

    print(f"OOF AUC          : {roc_auc_score(y, oof):.5f}")
    print(f"fold AUC mean/sd : {np.mean(fold_scores):.5f} / {np.std(fold_scores):.5f}")
    print("  ^ report the sd too. A gain smaller than this is not a gain.")

    out = preds_dir()
    ensure_parent_dir(out / "x")
    pd.DataFrame({ID: train[ID], "pred": oof}).to_csv(out / f"oof_{NAME}.csv", index=False)
    pd.DataFrame({ID: test[ID], "pred": test_pred}).to_csv(out / f"test_{NAME}.csv", index=False)
    print(f"saved -> {out}/oof_{NAME}.csv, {out}/test_{NAME}.csv")
    print("next: record one line in logs/EXPERIMENTS.md, then run inference.py")


if __name__ == "__main__":
    main()
