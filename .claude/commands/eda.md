---
description: Run EDA on the competition data and save reusable code + figures/tables (no external paid tools)
argument-hint: [target-file-path]
---

# EDA (Exploratory Data Analysis)

**Target:** $ARGUMENTS （空なら `data/raw/` の train ファイルを対象にする）

## Context

- @.references/COMPETITION.md
- @.references/DATASET.md
- @.references/METRIC.md

関連スキル: `safe-data-handling`, `dataframe-polars`, `visualization`, `path-and-io`,
`statistical-ml-review`, `competition-workflow`。

## Rules

- `data/raw/` は **不変**。読み込むだけ。書き込みは `data/processed/` か `outputs/` へ。
- 再利用するロジックは `src/commons/` に関数として置き、実行スクリプトは `ai-src/YYYYMMDD_eda/` に置く。
- 図は `outputs/figures/`、集計表は `outputs/tables/` に保存する（`visualization` スキルの規約に従う）。
- 大きいデータは `pl.scan_*` で遅延読み込みし、必要列だけ取る。

## 手順

### 1. 形の把握

- 行数・列数・dtype・メモリ
- 欠損率（列ごと、上位を表で）
- 基本統計量（数値列 / カテゴリ列を分けて）
- 重複行・重複ID

### 2. 目的変数

- 分布（分類ならクラス比、回帰ならヒストグラム + 歪度）
- クラス不均衡の度合い → metric との相性（`.references/METRIC.md` と突き合わせる）

### 3. リーク・CV 設計のための確認 ← コンペで最重要

- ID 列と目的変数の関係（行順・id の単調性に情報が乗っていないか）
- 同一エンティティの重複（ユーザー/レース/セッション単位のグループ有無）
- 時間列の有無と train/test の期間関係
- **train と test の分布差**（列ごとの平均・分位点比較、必要なら adversarial validation）

結論として **採用すべき fold 方式とその理由** を明記すること（`competition-workflow` の表を使う）。

### 4. 特徴量の当たり付け

- 主要特徴量と目的変数の関係（数値は分位ビン別平均、カテゴリは水準別平均）
- 相関の高い列ペア（冗長性）
- 外れ値・打ち切り・センチネル値（-999 等）

### 5. 提出形式の確認

sample submission を読み、列名・型・ヘッダ有無・行数を `.references/DATASET.md` と照合する。
ズレがあれば `.references/DATASET.md` を修正する。

## 出力

1. `outputs/figures/*.png`, `outputs/tables/*.csv`
2. 必要なら `notebook/eda.ipynb`（`notebook-workflow` スキルの構成に従う。クリーンカーネルで再実行可能に）
3. **日本語のサマリ**を `analysis-reporting` の構成（結論 → 事実 → 仮定 → 解釈 → 制約）で返す。
   最後に必ず含めるもの:
   - 推奨 CV 方式とその理由
   - 見つかったリーク候補
   - 次に作るべき特徴量の候補 3〜5 個
