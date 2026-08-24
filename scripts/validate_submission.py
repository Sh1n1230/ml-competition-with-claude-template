"""提出ファイルを sample submission と突合して検証するスクリプト。

使い方:
    uv run python scripts/validate_submission.py submission.csv
    uv run python scripts/validate_submission.py sub.csv --sample data/raw/sample_submission.csv
    uv run python scripts/validate_submission.py submission.tsv --no-header --sep '\t'

検証内容: 行数 / 列数・列名 / ID 集合・順序 / NaN・inf / 値域。
1つでも失敗したら exit code 1 を返す（= 提出してはいけない）。
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

SAMPLE_GLOBS = (
    "**/sample_submission*.csv",
    "**/sample_submit*.csv",
    "**/sample*.csv",
    "**/sample_submission*.tsv",
    "**/sample_submit*.tsv",
)


def find_sample(raw_dir: Path) -> Path | None:
    """`data/raw/` から sample submission らしきファイルを探す。

    Args:
        raw_dir: 生データディレクトリ。

    Returns:
        見つかったパス。無ければ None。
    """
    for pattern in SAMPLE_GLOBS:
        hits = sorted(raw_dir.glob(pattern))
        if hits:
            return hits[0]
    return None


def read_csv(path: Path, sep: str, header: bool) -> pd.DataFrame:
    """CSV/TSV を読み込む。

    Args:
        path: 読み込むファイル。
        sep: 区切り文字。
        header: ヘッダ行があるか。

    Returns:
        読み込んだ DataFrame。
    """
    return pd.read_csv(path, sep=sep, header=0 if header else None)


def check(condition: bool, ok_msg: str, ng_msg: str, failures: list[str]) -> None:
    """検証結果を出力し、失敗なら失敗リストに追加する。

    Args:
        condition: 検証条件。
        ok_msg: 成功時のメッセージ。
        ng_msg: 失敗時のメッセージ。
        failures: 失敗メッセージの蓄積先。
    """
    if condition:
        print(f"  OK   {ok_msg}")
    else:
        print(f"  FAIL {ng_msg}")
        failures.append(ng_msg)


def main() -> None:
    """メイン処理。"""
    parser = argparse.ArgumentParser(description="Validate a submission file before submitting.")
    parser.add_argument("submission", type=Path)
    parser.add_argument("--sample", type=Path, default=None, help="sample submission path")
    parser.add_argument("--sep", default=",", help="delimiter (default: ',')")
    parser.add_argument("--no-header", action="store_true", help="files have no header row")
    parser.add_argument(
        "--prob", action="store_true", help="predictions are probabilities: check [0, 1]"
    )
    args = parser.parse_args()

    header = not args.no_header
    sub_path: Path = args.submission
    if not sub_path.exists():
        print(f"ERROR: submission not found: {sub_path}")
        sys.exit(1)

    sub = read_csv(sub_path, args.sep, header)
    print(f"submission: {sub_path}  shape={sub.shape}")

    failures: list[str] = []

    # ── sample submission との突合 ──────────────────────────────────────────
    sample_path = args.sample or find_sample(Path("data/raw"))
    if sample_path is None:
        print("WARNING: sample submission not found")
        print("         形式は .references/DATASET.md で手動確認すること")
    else:
        sample = read_csv(sample_path, args.sep, header)
        print(f"sample:     {sample_path}  shape={sample.shape}")

        check(
            len(sub) == len(sample),
            f"rows match ({len(sub)})",
            f"row count differs: submission={len(sub)} sample={len(sample)}",
            failures,
        )
        check(
            sub.shape[1] == sample.shape[1],
            f"column count matches ({sub.shape[1]})",
            f"column count differs: submission={sub.shape[1]} sample={sample.shape[1]}",
            failures,
        )
        if header:
            check(
                list(sub.columns) == list(sample.columns),
                "column names match",
                f"column names differ: {list(sub.columns)} != {list(sample.columns)}",
                failures,
            )
        # ID 列（先頭列）の集合と順序
        if len(sub) == len(sample) and sub.shape[1] == sample.shape[1]:
            sid, mid = sub.iloc[:, 0], sample.iloc[:, 0]
            check(
                set(sid.astype(str)) == set(mid.astype(str)),
                "ID set matches",
                "ID set differs from sample submission",
                failures,
            )
            check(
                list(sid.astype(str)) == list(mid.astype(str)),
                "ID order matches",
                "ID order differs from sample submission (多くのコンペで許容されるが要確認)",
                failures,
            )

    # ── 値の健全性 ────────────────────────────────────────────────────────
    values = sub.iloc[:, 1:]
    n_nan = int(values.isna().sum().sum())
    check(n_nan == 0, "no NaN", f"{n_nan} NaN values found", failures)

    numeric = values.select_dtypes(include=[np.number])
    if not numeric.empty:
        n_inf = int(np.isinf(numeric.to_numpy()).sum())
        check(n_inf == 0, "no inf", f"{n_inf} inf values found", failures)
        lo, hi = float(numeric.to_numpy().min()), float(numeric.to_numpy().max())
        print(f"  INFO value range: [{lo:.6g}, {hi:.6g}]")
        if args.prob:
            check(
                lo >= 0.0 and hi <= 1.0,
                "probabilities within [0, 1]",
                f"probabilities out of range: [{lo}, {hi}]",
                failures,
            )

    n_dup = int(sub.iloc[:, 0].duplicated().sum())
    check(n_dup == 0, "no duplicated IDs", f"{n_dup} duplicated IDs", failures)

    print()
    if failures:
        print(f"NG: {len(failures)} check(s) failed — 提出しないこと")
        sys.exit(1)
    print("OK: submission looks valid")


if __name__ == "__main__":
    main()
