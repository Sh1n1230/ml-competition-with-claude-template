---
description: Create a baseline (CV-correct training + inference) using recipes/, and record it in the experiment log
argument-hint: [solution-dir-name]
---

# Baseline

**Output:** `src/$ARGUMENTS`（空なら `src/Solution1`）

## Context

- @.references/COMPETITION.md
- @.references/DATASET.md
- @.references/METRIC.md

関連スキル: `competition-workflow`（フェーズと CV 設計）, `experiment-log`, `python-style`,
`safe-data-handling`, `submit`。

## Baseline 作成の流れ

1. `src/<solution-dir>/`（既定値は `src/Solution1`）にベースラインを構築。
2. データ読み込み、CV設計（Stratified/Group/TimeSeries等）、特徴量変換、GBDT等のモデル学習を実装。
3. OOF（Out-of-Fold）予測と test 予測を `data/processed/preds/` に保存。
4. CV スコアを `logs/EXPERIMENTS.md` に記録する。

## 実装要件

`src/<Solution>/` に:

- `train.py`
  - データ読み込み（`commons.paths` 経由。絶対パス禁止）
  - 前処理（欠損補完・エンコーディング。**fold 内で fit** すること）
  - CV（`.references/` とデータ性質から選んだ fold 方式。理由をコメントに書く）
  - モデル学習 → OOF 予測を保存
  - `.references/METRIC.md` の実装で CV スコアを算出・表示
  - モデル保存
- `inference.py`
  - 保存済みモデルの読み込み → test 予測 → `submission.csv`
  - 提出形式（ヘッダ有無・列名・行順）は `.references/DATASET.md` に厳密に従う

必須:

- **seed 固定**（numpy / random / フレームワーク / fold）
- **OOF と test 予測を同じ形式で保存**（`data/processed/preds/{oof_,test_}<name>.csv`）
  → 後でアンサンブルや stacking にそのまま利用可能
- ログ出力（fold ごとのスコアと全体 CV）
- コードコメントは英語、ユーザーへの説明は日本語
- 出力ディレクトリは自動作成（`commons.paths.ensure_parent_dir`）

## 完了時

1. CV スコアと fold ごとのばらつきを報告する。
2. `logs/EXPERIMENTS.md` に1行追加する（`experiment-log` スキル）。
3. `uv run python scripts/validate_submission.py submission.csv` を通す。
4. 次の一手を提案する（通常は `competition-workflow` の P3 特徴量 → P4 多様性）。
