# テスト・検証方針

## コード品質

```bash
uv run ruff check .        # リント
uv run ruff format .       # 整形
uv run mypy src            # 型チェック
uv run pytest              # テスト
bash scripts/run_quality_checks.sh   # 一括
```

## 提出物の検証

```bash
uv run python scripts/validate_submission.py submission.csv
```

行数 / ID / 列 / NaN・inf / 値域を sample submission と突合する。**提出前に必須。**

## データ保護の検証

```bash
uv run python scripts/check_no_raw_data_commit.py     # 配布データのコミット防止
uv run python scripts/check_no_sensitive_patterns.py  # 認証情報パターンの検出
```

## Notebook

- クリーンカーネルから再実行できること
- 出力に配布データの中身や個人情報を残さない

## テスト対象の優先順位

1. 特徴量生成関数（リーク混入の検出）
2. metric 実装（公式定義との一致）
3. 提出ファイル生成（形式）

学習ループ自体の単体テストは費用対効果が低い。小さいサンプルでの smoke test で足りる。
