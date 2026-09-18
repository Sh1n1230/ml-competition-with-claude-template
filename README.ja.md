# ML Competition with Claude Code

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Claude Code が「コンペの進め方」を最初から知っている状態**で始めるためのワークスペースです。

このリポジトリの中身はほとんどコードではありません。24 のスキルと 3 つのコマンドが
あなたとエージェントの間に入り、**コンペを静かに壊すもの** — リークした fold、
ノイズより小さい「改善」、行順がずれた提出ファイル — を、まだ安いうちに捕まえます。

Kaggle / SIGNATE / atmaCup / Nishika / ProbSpace と、同じ形をしたものに使えます。

[English README](README.md)

## まず動かしてみる（アカウント不要・ダウンロード不要・ネットワーク不要）

```bash
git clone https://github.com/<owner>/ml-competition-with-claude-template.git my-competition
cd my-competition
uv sync --group dev

uv run python examples/quickstart/make_data.py    # 同梱データからコンペ形式の CSV を作る
uv run python examples/quickstart/train.py        # 反復層化CV -> OOF と test の予測を保存
uv run python examples/quickstart/inference.py    # 予測 -> submission.csv
uv run python scripts/validate_submission.py \
    examples/quickstart/data/submission.csv \
    --sample examples/quickstart/data/sample_submit.csv
```

4コマンド・十数秒で一周します。各ステップが何を実演しているかは
[`examples/quickstart/README.md`](examples/quickstart/README.md) に書いてあります。

## スキルが実際に防いでいるもの

それぞれのスキルは、「高くつくのに踏みやすい失敗」に対応しています。

| スキル | 何を止めるためのものか |
|---|---|
| `competition-workflow` | **そもそも正しくなかった fold の上でモデルを調整すること。** 特徴量より先に CV 設計を置き、リーク検査表を通し、定石を鵜呑みにせず**測ってから**採用させる |
| `experiment-log` | 「それは前に試した」が**どの条件で**か残っていない状態。`drop` には規模・前処理・受け手・効果量を必ず書かせるので、行き止まりが**天井に化けない** |
| `statistical-ml-review` | 前提・リークの危険・ベースラインを添えずに数字だけ報告すること |
| `safe-data-handling` | `data/raw/` への書き込み。配布データは不変で、その保証はコメントではなくコードにある |
| `path-and-io` | 自分の機械でしか動かない絶対パス。入出力は全て `commons.paths` を通す |
| `submit` / `validate_submission.py` | ID の順序が sample と微妙に違う提出で1日を溶かすこと |
| `competition-platforms` | LB の分割・投稿回数制限・ファイル形式がどこも同じだと思い込むこと |
| `free-gpu` | 無料ノートブック環境を使い切る前に有償計算へ行くこと |
| `python-style` / `python-project-ops` / `notebook-workflow` / `dataframe-polars` / `sql-analysis` / `visualization` / `analysis-reporting` | 書いた本人にしか再実行できないコードと成果物 |
| `kaggle-*`（6本） / `signate` / `web-research` | コンペ情報・規約・LB 状態の手作業コピー |

`/setup <url>` がコンペページから `.references/` を埋め、`/eda` と `/baseline` は
推測ではなくその事実から動きます。

## 実際のコンペで始める

```text
/setup https://www.kaggle.com/competitions/<competition-name>
/setup https://signate.jp/competitions/<id>
```

ダウンロードしたファイルを `data/raw/` に置き、`/eda` → `/baseline` と進みます。

任意の追加:

```bash
uv sync --group nn                 # PyTorch / tabular NN
uv sync --group jp                 # SIGNATE CLI と日本語フォント
cp .mcp.json.example .mcp.json     # Kaggle / context7 / serena の MCP を有効化
```

`kaggle-*` の6スキルは Kaggle MCP サーバを使うので、最後の1行が必要です。
それ以外は無しでも動きます。

すでに始めたプロジェクトにスキルだけ入れる場合:

```bash
bash scripts/install_ml_skills.sh /path/to/my-competition
```

同梱の `.claude/skills` と `.claude/commands` だけを更新し、自分で足したスキルには触りません。

## ワークフロー

1. `/eda` でデータを理解し、リークの可能性を点検する
2. モデルを触る前に、**誠実な CV** と seed を固定する
3. `/baseline` でベースラインを作り、OOF と test 予測を保存する
4. **一度に1つだけ変え**、結果を `logs/EXPERIMENTS.md` に記録する
5. 検証済みで**多様な**モデルだけを結合し、コンペの指標を最適化する
6. `scripts/validate_submission.py` を通してから提出する

飛ばされがちなのは 4 です。**5 を可能にしているのは 4 の記録**です。

## ディレクトリ構成

```text
.
├── .claude/               # Claude Code のコマンドとスキル
├── .references/           # /setup が生成するコンペ事実
├── examples/quickstart/   # ネットワーク不要の実行可能サンプル
├── src/commons/           # 共通のパス・ユーティリティ
├── src/<solution-name>/   # 安定した解法（ユーザー所有）
├── ai-src/                # 日付つきの作業場
├── data/
│   ├── raw/               # 配布データ（不変・コミット禁止）
│   ├── external/          # 外部データ（不変・コミット禁止）
│   ├── interim/           # 中間生成物
│   └── processed/         # 特徴量と予測
├── outputs/               # 図・表・レポート
├── configs/               # 実験設定
├── logs/                  # 実験ログ
├── scripts/               # 検証と品質チェック
├── tests/                 # テスト
└── docs/agent/            # ワークフローと安全指針
```

## 品質チェック

```bash
bash scripts/run_quality_checks.sh                              # ruff / mypy / pytest / ガード
uv run python scripts/validate_submission.py path/to/submission.csv
```

`validate_agent_docs.py` は既定では欠損を**警告**として報告します。テンプレートの一部を
削る・差し替えるのは正当な使い方で、それでビルドを落とすべきではないからです。
全ファイルを必須にしたいときは `--strict`（本リポジトリ自身の CI はこちら）。

Python 3.10 以上。既存環境に載せやすいよう、依存の下限は意図的に緩めてあります。

## 貢献と安全性

貢献を歓迎します。まず [CONTRIBUTING.md](CONTRIBUTING.md) をお読みください。
コンペのデータセット・認証情報・API キー・個人情報は絶対にコミットしないでください。
脆弱性の報告は [SECURITY.md](SECURITY.md) を参照してください。

## クレジットとライセンス

本ワークフローは OSS データサイエンス／Kaggle コミュニティの一般的な実践に基づいています。
ライセンスは MIT（[LICENSE](LICENSE)）。
