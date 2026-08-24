# ML Competition with Claude Code（日本語版）

Claude Code とともに、機械学習コンペティション（Kaggle / SIGNATE / atmaCup / Nishika / ProbSpace 等）を高い再現性と規律を持って進めるためのオープンソース・テンプレートリポジトリです。

[English Documentation](README.md)

---

## これは何か

Kaggle / SIGNATE / atmaCup / Nishika / ProbSpace などの機械学習コンペを、再現性と
安全性を保ちながら進めるためのオープンソース・ワークスペーステンプレートです。
リークを避けたCV、実験ログ、提出ファイル検証、Claude Code向けの手順を最初から備えます。

## 主な特徴

- **規律重視のワークフロー**: リークのないCV設計、1実験1変更のログ記録（`logs/EXPERIMENTS.md`）、提出前フォーマット検証（`scripts/validate_submission.py`）、多様性のあるアンサンブル。
- **完全無料・オープンソース完結**: 有償APIや有償GPUレンタルを前提とせず、ローカル計算資源（NVIDIA CUDA / Apple Silicon MPS / CPU）および無料プラットフォーム（Kaggle Notebooks GPU/TPU、Google Colab 無料枠）で動作。
- **エンジニアリング規律の組み込み**: `uv` による高速な依存関係管理、`ruff` / `mypy` / `pytest` による静的検証、配布データ保護チェック・秘密情報検出スクリプトを完備。
- **Claude Code向けスキル・MCP連携**: 各種プラットフォーム操作（Kaggle MCP、SIGNATE CLI）、自動セットアップ（`/setup`）、EDA（`/eda`）、ベースライン構築（`/baseline`）などのスキルを内包。

---

## ディレクトリ構成

```text
.
├── .claude/skills/        # Claude Code用スキル定義
├── .references/           # コンペの一次情報・評価指標（/setup が自動生成）
├── src/commons/           # 共通パス・ユーティリティ
├── src/<solution-name>/     # 安定した解法モデル
├── ai-src/                # Claude Codeの作業場（日付・タスクごとに作成）
├── data/
│   ├── raw/               # 不変の配布データ（gitignore対象）
│   ├── external/          # 不変の外部データ（gitignore対象）
│   ├── interim/           # 中間加工データ
│   └── processed/         # 特徴量・予測値（data/processed/preds/ に OOF/test 予測）
├── outputs/               # 図・集計表・レポート
├── configs/               # 実験設定ファイル
├── logs/                  # 実験管理ログ（logs/EXPERIMENTS.md）
├── scripts/               # 提出ファイル検証・品質チェックスクリプト
├── tests/                 # ユニットテスト（pytest）
└── docs/agent/            # Claude Code向け規約・設計ガイドライン
```

---

## クイックスタート

```bash
git clone https://github.com/<owner>/ml-competition-with-claude-template.git my-competition
cd my-competition
uv sync --group dev
```

Claude Codeでコンペを初期化します:

```bash
/setup https://www.kaggle.com/competitions/<competition-name>
# または
/setup https://signate.jp/competitions/<id>
```

`/setup` はプラットフォームを判定し、`.references/` とコンペ用構成を準備します。
コンペ固有情報は `.references/` に記録し、Claude Codeから各コマンドを実行します。追加機能は `uv sync --group nn`（PyTorch）、
`uv sync --group jp`（SIGNATE向け）で導入できます。

既存のコンペプロジェクトへ同梱スキルを一括導入するには、次を実行します:

```bash
bash scripts/install_ml_skills.sh /path/to/my-competition
```

同名の同梱ファイルだけを更新し、独自スキルやその他のプロジェクトファイルは削除しません。

---

## コンペ進行フェーズ

1. **P0: データ理解 & リーク検査** (`/eda`) — 行順、ID相関、分布差、時間構造を検証
2. **P1: CV設計の固定** — StratifiedKFold / GroupKFold / TimeSeriesSplit とシードを固定
3. **P2: ベースライン構築** (`/baseline`) — GBDT等でシンプルなモデルを作成し `data/processed/preds/` に保存
4. **P3: 特徴量エンジニアリング** — 1実験1変更で効果を検証
5. **P4: モデルの多様性** — 異なるモデル（GBDT複数種 + NN）を追加
6. **P5: アンサンブル & Stacking** — 予測値のブレンディングと決定ルール（閾値等）の最適化
7. **P6: 提出ファイル検証 & 提出** (`/submit`) — フォーマットを検証（`scripts/validate_submission.py`）して投稿

---

## 品質・セキュリティチェック

以下のコマンドでリポジトリ全体の品質チェックを一括実行できます:

```bash
bash scripts/run_quality_checks.sh
```

- **リント & フォーマット**: `uv run ruff check .` / `uv run ruff format --check .`
- **型検査**: `uv run mypy src scripts`
- **テスト**: `uv run pytest`
- **データ保護検査**: `uv run python scripts/check_no_raw_data_commit.py`
- **秘密情報検査**: `uv run python scripts/check_no_sensitive_patterns.py`
- **ドキュメント整合性検査**: `uv run python scripts/validate_agent_docs.py`

---

## コントリビューションと安全性

改善提案は歓迎します。まず [CONTRIBUTING.md](CONTRIBUTING.md) を確認してください。
配布データ、認証情報、APIキー、個人情報はコミットしないでください。
脆弱性の報告方法は [SECURITY.md](SECURITY.md) を参照してください。

---

## ライセンス

本リポジトリは [MIT License](LICENSE) のもとで公開されています。
