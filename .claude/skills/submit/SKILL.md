---
name: submit
description: 提出ファイルを検証してからプラットフォームへ投稿する（Kaggle / SIGNATE / その他は手動）。submission.csv を作った直後・提出したいときに使用。
argument-hint: [submission-file] [note]
---

# Submit — 検証してから投げる

**検証を通さない提出は禁止。** 1日の投稿枠は有限で、形式ミスの 0 点は丸一日を失う。

## Step 1: フォーマット検証（必須）

```bash
uv run python scripts/validate_submission.py <submission-file>
```

このスクリプトは `data/raw/` の sample submission と突合して以下を確認する:
行数 / ID 集合・順序 / 列名・列数 / NaN・inf / 値域。失敗したら **提出しない**。

sample submission が無いコンペでは `.references/DATASET.md` の
「Submission format」節に従って手作業で確認し、確認内容をユーザーに報告する。

## Step 2: 妥当性の目視

- 分類: 予測クラス分布を train の分布・過去提出と比較（極端な偏りは決定ルールのバグ）
- 回帰: 予測値の分布・最小最大を train と比較（外挿の暴走を検出）
- 直前の提出との相関: 0.999 超なら「実質同じもの」を投げようとしている

## Step 3: 投稿

### Kaggle

`kaggle-submit` スキルに従う（ファイル提出 / code competition の notebook 提出）。

### SIGNATE

```bash
uv run signate submit --task_key=<tkey> --path=<submission-file> --memo="<note>"
```

`task_key` は `signate task-list --competition_key=<ckey>` で得る（`signate` スキル参照）。

### atmaCup / Nishika / ProbSpace など

CLI が無いので **ユーザーに Web UI からアップロードしてもらう**。
エージェントは提出ファイルのパスと、note に貼るテキスト（CV スコア・構成）を用意する。

## Step 4: 記録

`experiment-log` スキルに従い、`logs/EXPERIMENTS.md` に **CV と LB を必ずペアで**記録する。
CV と LB の乖離が続く場合は `docs/agent/statistical-and-ml-guidelines.md` の判定に従い、
LB ではなく CV を信じる（n の大きい方が正しい）。

## Step 5: 残枠の管理

提出後、残り投稿回数をユーザーに伝える。枠が残り1回なら、
「最後の1回は現時点のベスト CV 構成に使う」ことを提案する。
