"""Turn a dataset bundled with scikit-learn into a competition-shaped folder.

No network access is needed. The point is not the dataset -- it is that the
rest of the template (CV design, experiment log, submission validation) can be
exercised end to end before you have real competition data.

    python examples/quickstart/make_data.py

Writes into ``examples/quickstart/data/``:

* ``train.csv``          features + ``target``
* ``test.csv``           features only
* ``sample_submit.csv``  the shape a submission must have
* ``answers.csv``        held-out truth, so the example can also show a "LB" score
                         (a real competition never gives you this)
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split

DATA_DIR = Path(__file__).resolve().parent / "data"
ID = "id"
TARGET = "target"


def build(test_size: float = 0.35, seed: int = 42, n_rows: int | None = None) -> None:
    """Write the competition-shaped files.

    Args:
        test_size: Fraction held out as the "test" split.
        seed: Split seed, fixed so the example is reproducible.
        n_rows: Optional cap on rows, used by the test suite to keep it fast.
    """
    frame = load_breast_cancer(as_frame=True).frame
    frame = frame.rename(columns=lambda c: str(c).replace(" ", "_"))
    if n_rows is not None:
        frame = frame.head(n_rows)
    frame.insert(0, ID, range(len(frame)))

    train, test = train_test_split(
        frame, test_size=test_size, random_state=seed, stratify=frame[TARGET]
    )
    train = train.sort_values(ID).reset_index(drop=True)
    test = test.sort_values(ID).reset_index(drop=True)

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    train.to_csv(DATA_DIR / "train.csv", index=False)
    test.drop(columns=[TARGET]).to_csv(DATA_DIR / "test.csv", index=False)
    pd.DataFrame({ID: test[ID], TARGET: 0}).to_csv(DATA_DIR / "sample_submit.csv", index=False)
    test[[ID, TARGET]].to_csv(DATA_DIR / "answers.csv", index=False)

    print(f"train {train.shape} / test {test.shape} -> {DATA_DIR}")
    print(f"positive rate in train: {train[TARGET].mean():.3f}")


def main() -> None:
    """Entry point."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rows", type=int, default=None, help="cap the number of rows")
    args = parser.parse_args()
    build(n_rows=args.rows)


if __name__ == "__main__":
    main()
