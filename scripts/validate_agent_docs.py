"""エージェント向け文書とスキルの必須ファイルが揃っているか検証するスクリプト。"""

from __future__ import annotations

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
    repo_root = Path(".")
    missing = [f for f in REQUIRED_FILES if not (repo_root / f).exists()]
    forbidden = [f for f in FORBIDDEN_PATHS if (repo_root / f).exists()]

    if missing:
        print("ERROR: The following required agent files are missing:")
        for m in missing:
            print(f"  - {m}")
    if forbidden:
        print("ERROR: Paid-tool skills must not exist in this template:")
        for f in forbidden:
            print(f"  - {f}")

    if missing or forbidden:
        sys.exit(1)

    print(f"OK: All {len(REQUIRED_FILES)} required agent files exist, no paid-tool skills.")


if __name__ == "__main__":
    main()
