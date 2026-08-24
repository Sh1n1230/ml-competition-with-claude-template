#!/usr/bin/env bash

set -euo pipefail

# Resolve repository root based on this script's location.
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

dirs=(
  "configs"
  "data/raw"
  "data/external"
  "data/interim"
  "data/processed/preds"
  "src/commons"
  "src/Solution1"
  "ai-src"
  "notebook"
  "logs"
  "outputs/figures"
  "outputs/tables"
  "outputs/reports"
  "scripts"
  "tests"
  "docs/agent"
  ".references"
)

for dir in "${dirs[@]}"; do
  mkdir -p "$ROOT/$dir"
done

printf "Project structure ensured under %s\n" "$ROOT"
