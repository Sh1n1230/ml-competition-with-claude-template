# Quickstart example

A complete run of the workflow this template encodes — **without a competition account,
without a download, without network access.** It exists so you can see the pieces move
before you point them at real data.

```bash
uv sync
uv run python examples/quickstart/make_data.py    # competition-shaped CSVs from a bundled dataset
uv run python examples/quickstart/train.py        # repeated stratified CV -> OOF + test predictions
uv run python examples/quickstart/inference.py    # predictions -> submission.csv
uv run python scripts/validate_submission.py \
    examples/quickstart/data/submission.csv \
    --sample examples/quickstart/data/sample_submit.csv
```

Expected: an out-of-fold AUC around 0.989, a submission of 200 rows, and
`OK: submission looks valid`.

## What each step is showing you

| Step | The habit it demonstrates |
|---|---|
| `make_data.py` | Inputs are read-only and live in one place. Nothing downstream writes to them. |
| `train.py` | The fold scheme is decided first and stated once. Every transform is fitted **inside** the fold. The number reported is out-of-fold, and it comes with a fold standard deviation — **a gain smaller than that sd is not a gain.** |
| `train.py` (outputs) | OOF and test predictions are saved in the same shape, so a later blending step needs no re-runs. |
| `inference.py` | The example scores the submission against held-out answers — something a real competition will not let you do. It is here to make the **out-of-fold score vs leaderboard score gap** visible from day one. |
| `validate_submission.py` | Row count, columns, ID set and order, NaN/inf, value range — checked before anything is submitted. |

## Moving to a real competition

1. `/setup <competition-url>` fills `.references/COMPETITION.md`, `DATASET.md`, `METRIC.md`.
2. Put the downloaded files in `data/raw/` (immutable — nothing writes back there).
3. `/eda`, then `/baseline`, which builds `src/Solution1/` along the lines of `train.py`
   and `inference.py` here, but with the fold scheme and metric your competition needs.
4. One line per experiment in `logs/EXPERIMENTS.md`.

The dataset here is a plain binary classification problem, so `StratifiedKFold` is the right
fold scheme. **It usually will not be yours.** Grouped entities, time ordering and
distribution shift each demand a different split, and getting that wrong invalidates every
experiment stacked on top of it — see the `competition-workflow` skill, phase P1.
