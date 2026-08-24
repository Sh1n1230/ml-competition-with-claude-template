#!/usr/bin/env bash
# PostToolUse hook: Python ファイルの編集後に ruff (fix + format) と mypy を実行する。
# Claude Code は hook 入力を JSON で stdin に渡す。
set -uo pipefail

payload=$(cat)
file=$(printf '%s' "$payload" | python3 -c '
import json, sys
try:
    data = json.load(sys.stdin)
except Exception:
    print("")
else:
    print(data.get("tool_input", {}).get("file_path", ""))
')

case "$file" in
  *.py) ;;
  *) exit 0 ;;
esac

[ -f "$file" ] || exit 0

uv run ruff check --fix "$file" || true
uv run ruff format "$file" || true
uv run mypy "$file" || true
exit 0
