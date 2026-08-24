# リポジトリ構成

| ディレクトリ | 役割 | 誰が書くか |
|-------------|------|-----------|
| `.references/` | コンペの一次情報（事実のみ） | `/setup` が生成 |
| `src/commons/` | 共通ユーティリティ（paths 等） | 人間 |
| `src/<solution-name>/` | 安定した解法コード | 人間（Claude Codeは明示指示がある時のみ） |
| `ai-src/YYYYMMDD_<task>/` | Claude Codeの作業場。実験コード・使い捨てスクリプト | Claude Code |
| `notebook/` | 探索用 Notebook | 双方 |
| `data/raw/` | 配布データ（**不変**・gitignore） | 誰も書き換えない |
| `data/external/` | 外部データ（**不変**・gitignore） | 誰も書き換えない |
| `data/interim/` | 中間生成物 | 双方 |
| `data/processed/` | 加工済み特徴量、`preds/` に OOF/test 予測 | 双方 |
| `outputs/figures,tables,reports/` | 図・集計表・レポート | 双方 |
| `configs/` | 実験設定ファイル | 双方 |
| `logs/` | `EXPERIMENTS.md` と学習ログ | 双方 |
| `scripts/` | 検証・品質チェックスクリプト | 人間 |
| `tests/` | pytest | 双方 |
| `docs/agent/` | Claude Code向けプロジェクト文書 | 双方 |
