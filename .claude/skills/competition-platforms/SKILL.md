---
name: competition-platforms
description: プラットフォームごとの違い（提出形式・回数制限・LB分割・データ取得手段・規約）を確認する。Kaggle / SIGNATE / atmaCup(guruguru) / Nishika / ProbSpace のどれかで作業する際、提出前・セットアップ時に参照。
---

# Competition Platforms — 差分早見表

`.references/COMPETITION.md` の `Platform` 行でルーティングする。**提出形式の思い込みが
最大の事故要因**（Kaggle 慣れ → SIGNATE でヘッダ付き提出 → 0 点）なので、初回提出前に必ずここを読む。

| | Kaggle | SIGNATE | atmaCup / guruguru | Nishika | ProbSpace |
|---|---|---|---|---|---|
| データ取得 | Kaggle MCP / CLI | `signate` CLI | 手動DL | 手動DL | 手動DL |
| 提出 | MCP / CLI / Notebook | `signate submit` | Web UI | Web UI | Web UI |
| 提出ファイル | ヘッダ付き CSV が基本 | **ヘッダ無し CSV/TSV が多い** | コンペ規定 | ヘッダ付き CSV が基本 | ヘッダ付き CSV が基本 |
| 1日の上限 | コンペ規定（5 が多い） | コンペ規定（5 が多い） | 少なめ（開催中は要確認） | コンペ規定 | コンペ規定 |
| Public/Private | ほぼ常に分割 | 分割ありなし両方 | 分割あり（終了直前に隠す運用も） | 分割あり | 分割あり |
| 最終提出の選択 | 自分で2件選ぶ形式が多い | 自動 or 選択（要確認） | 要確認 | 要確認 | 要確認 |
| 時刻基準 | UTC | JST | JST | JST | JST |
| 外部データ | コンペ規定 | 原則禁止のことが多い | 規定に従う | 規定に従う | 規定に従う |
| 賞金/入賞条件 | 解法提出・コード公開義務あり | 上位者にコード提出義務あり | 主にコミュニティ | 規定 | 規定 |

## 共通の提出前チェック（プラットフォーム非依存）

```
[ ] 行数が test と一致
[ ] ID 列の集合・順序が sample_submission と一致
[ ] ヘッダ有無・区切り文字・小数桁が規定どおり
[ ] NaN / inf なし、値域が妥当（確率なら [0,1]、合計1が要求されるなら正規化済み）
[ ] ファイル名・拡張子が規定どおり
[ ] 提出 note に CV スコアと構成を明記
[ ] 残り提出回数を確認（使い切ると当日詰む）
```

## 日本語コンペ特有の注意

- 締切は **JST**。Kaggle の UTC 表記と混ぜない。
- 規約で**配布データの外部持ち出し・再配布が禁止**なことが多い。クラウド GPU への
  アップロードや公開 notebook への貼り付けは、規約を確認してから。
- 日本語カラム名・全角数字・Shift_JIS が普通に出てくる。読み込みは
  `pl.read_csv(path, encoding="shift-jis")` などエンコーディングを明示する。
- 図に日本語ラベルを使う場合は `japanize_matplotlib`（`visualization` スキル参照）。

## ルーティング

| 目的 | スキル |
|------|--------|
| Kaggle のメタ情報 / データ / 提出 / LB / notebook | `kaggle-competition`, `kaggle-datasets`, `kaggle-submit`, `kaggle-leaderboard`, `kaggle-notebooks`, `kaggle-discussions` |
| SIGNATE のデータ / 提出 | `signate` |
| その他プラットフォームの情報収集 | `web-research` |
| 提出直前の共通チェック | `submit` |
