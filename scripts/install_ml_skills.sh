#!/usr/bin/env bash

set -euo pipefail

usage() {
  cat <<'EOF'
Install the bundled ML competition skills and commands into a project.

Usage:
  bash scripts/install_ml_skills.sh [target-directory]

The target defaults to the current directory. Existing files with the same
path are updated; unrelated skills and project files are left untouched.
EOF
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

if [[ $# -gt 1 ]]; then
  usage >&2
  exit 2
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
TARGET_ROOT="$(cd "${1:-.}" && pwd)"

if [[ "$TARGET_ROOT" == "$SOURCE_ROOT" ]]; then
  printf 'Skills are already installed in %s\n' "$TARGET_ROOT"
  exit 0
fi

for directory in ".claude/skills" ".claude/commands"; do
  source_directory="$SOURCE_ROOT/$directory"
  target_directory="$TARGET_ROOT/$directory"

  if [[ ! -d "$source_directory" ]]; then
    printf 'ERROR: Bundled directory not found: %s\n' "$source_directory" >&2
    exit 1
  fi

  mkdir -p "$target_directory"
  cp -R "$source_directory/." "$target_directory/"
  printf 'Installed %s into %s\n' "$directory" "$TARGET_ROOT"
done

printf 'ML competition skills are ready in %s\n' "$TARGET_ROOT"
