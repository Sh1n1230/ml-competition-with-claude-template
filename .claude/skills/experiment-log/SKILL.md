---
name: experiment-log
description: 実験結果を logs/EXPERIMENTS.md に一行一実験で記録し、CV と LB を対応付けて管理する。スコアが出た直後・提出直後・実験を振り返るときに使用。
---

# Experiment Log — 一行一実験

コンペで最も失われやすい資産は「何を試して、どうだったか」。
**スコアが出たら必ず記録する。記録していない実験は存在しなかったのと同じ。**

## 記録先

`logs/EXPERIMENTS.md`（`logs/` は `.gitignore` 対象外にしてある = コミットしてよい）。

## テンプレート（`/setup` で作成）

```markdown
# EXPERIMENTS

Metric: <metric> (<Maximize|Minimize>) / CV: <fold scheme, n_folds, seed>

| # | date | what changed | model / config | CV | LB(public) | 判定 | notes |
|---|------|--------------|----------------|----|-----------|------|-------|
| 1 | 2026-08-21 | baseline | LGB default, SKF5 seed42 | 0.8123 | 0.8098 | keep | 起点 |

## 効かなかったこと（再試行禁止リスト）

- （例）PL: 自信度0.99以上のtestを追加 → CV -0.0021。合成データでは自己強化するだけ。

## 現在のベスト

- 構成: 
- CV / LB: 
- 生成コマンド: 
```

## 記録ルール

1. **1行 = 1つの変更**。同時に2箇所変えたら、どちらが効いたか永久に分からない。
2. **CV と LB は必ずペア**で書く。片方だけの行は判断材料にならない。
3. **fold と seed を固定**し、行ごとに明記する。fold が違う CV 同士は比較できない。
4. 判定は `keep` / `drop` / `hold`（保留・要再検証）の3値。`drop` は理由を notes に。
5. 効かなかったことは「再試行禁止リスト」に移す。数日後の自分が同じ穴を掘る。
6. 提出したら LB を追記する。提出 note にも同じ実験番号を書いて対応付ける。

## CV と LB が食い違ったとき

原則（詳細は `docs/agent/statistical-and-ml-guidelines.md` 参照）:

- **n の大きい方を信じる**。honest CV (n=数百〜数千) > public LB (n=数十)。
- CV↑ / LB↓ が続くなら、LB へのフィッティングではなく **CV 設計のリーク**をまず疑う。
- 後付け最適化（blend重み・閾値・pool構成）は nested-CV ゲートを通してから採用する。

## 集計

```bash
# ベスト構成の再現コマンドを探す
grep -n "keep" logs/EXPERIMENTS.md | tail -20
```

節目（提出前・日次まとめ）では、`analysis-reporting` スキルの構成
（結論 → 事実 → 仮定 → 解釈 → 制約）で日本語サマリをユーザーに返す。
