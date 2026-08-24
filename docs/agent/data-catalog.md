# データカタログ

> 詳細な列定義は `.references/DATASET.md`（`/setup` が生成）。ここには**運用上の注意**を書く。

## ファイル一覧

| ファイル | 行数 | 粒度（1行=何か） | 備考 |
|---------|------|-----------------|------|
| `data/raw/train.csv` | | | |
| `data/raw/test.csv` | | | |
| `data/raw/sample_submission.csv` | | | |

## 注意点

<!-- 例: エンコーディングが Shift_JIS、日本語カラム名、-999 がセンチネル値、
     同一ユーザーが複数行（GroupKFold 必須）、train と test で期間が違う など -->

## 派生データ

| パス | 生成元スクリプト | 内容 |
|------|-----------------|------|
| `data/processed/preds/oof_*.csv` | `src/...` | 各baseモデルのOOF予測 |
| `data/processed/preds/test_*.csv` | `src/...` | 各baseモデルのtest予測 |
