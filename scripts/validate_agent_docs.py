"""エージェント向け文書とスキルが揃っているか点検するスクリプト。

既定では **欠けていても警告して終了コード 0 を返す**。テンプレートからファイルを
削る／差し替えるのは正当な使い方なので、それで CI を落とさないため。

``--strict`` を付けると欠損を失敗として扱う（このリポジトリ自身の CI 用）。
有償ツール依存の混入だけは、既定でも常に失敗させる。
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

SKILLS = [
    # コンペ運用
    "competition-workflow",
    "competition-platforms",
    "setup",
    "experiment-log",
    "submit",
    "free-gpu",
    "web-research",
    # プラットフォーム
    "kaggle-competition",
    "kaggle-datasets",
    "kaggle-discussions",
    "kaggle-leaderboard",
    "kaggle-notebooks",
    "kaggle-submit",
    "signate",
    # エンジニアリング規律
    "python-project-ops",
    "python-style",
    "path-and-io",
    "safe-data-handling",
    "dataframe-polars",
    "notebook-workflow",
    "visualization",
    "statistical-ml-review",
    "analysis-reporting",
    "sql-analysis",
]

DOCS = [
    "project-overview",
    "repository-structure",
    "data-catalog",
    "metrics-and-definitions",
    "competition-workflow",
    "statistical-and-ml-guidelines",
    "validation-and-testing",
    "reporting-guidelines",
    "security-and-privacy",
    "agent-behavior",
]

REQUIRED_FILES = [
    "CLAUDE.md",
    "AGENTS.md",
    "README.md",
    "README.ja.md",
    "LICENSE",
    "CONTRIBUTING.md",
    "create_structure.sh",
    "scripts/validate_submission.py",
    "scripts/check_no_raw_data_commit.py",
    "scripts/check_no_sensitive_patterns.py",
    "src/commons/paths.py",
    *[f".claude/skills/{name}/SKILL.md" for name in SKILLS],
    *[f"docs/agent/{name}.md" for name in DOCS],
]

# 有償ツール依存を持ち込まないためのガード（スキル名 / パス片）
FORBIDDEN_PATHS = [
    ".claude/skills/codex",
    ".claude/skills/vast-gpu-train",
    ".claude/skills/vast-gpu-download",
]


def main() -> None:
    """メイン処理。"""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--strict",
        action="store_true",
        help="欠損ファイルを失敗として扱う（既定は警告のみ）",
    )
    args = parser.parse_args()

    repo_root = Path(".")
    missing = [f for f in REQUIRED_FILES if not (repo_root / f).exists()]
    forbidden = [f for f in FORBIDDEN_PATHS if (repo_root / f).exists()]

    if missing:
        label = "ERROR" if args.strict else "WARNING"
        print(f"{label}: {len(missing)} of {len(REQUIRED_FILES)} agent files are missing:")
        for m in missing:
            print(f"  - {m}")
        if not args.strict:
            print(
                "  (テンプレートから削った／差し替えたなら想定どおり。"
                "揃っていることを強制したいときは --strict)"
            )

    # 有償ツール依存だけは --strict に関係なく失敗させる。
    if forbidden:
        print("ERROR: Paid-tool skills must not exist in this template:")
        for f in forbidden:
            print(f"  - {f}")
        sys.exit(1)

    if missing and args.strict:
        sys.exit(1)

    if not missing:
        print(f"OK: All {len(REQUIRED_FILES)} agent files exist, no paid-tool skills.")


if __name__ == "__main__":
    main()
