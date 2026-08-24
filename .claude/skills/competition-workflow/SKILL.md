---
name: competition-workflow
description: コンペ全体の進め方（フェーズ順序・CV設計・リーク検査・多様性のあるアンサンブル・最終提出の選択）を決める。新しいコンペを始めるとき、次に何をやるか迷ったとき、伸び悩んだときに使用。
---

# Competition Workflow — 何を、どの順で

コンペティション進行の順序と判断ルールを定義します。

## フェーズ（tabular）

```
P0 データ理解  EDA: 欠損/外れ値/分布/ID列リーク/train-test分布差。metricと提出形式を確認
P1 CV設計     folds を先に固定する（下記）。以降 全モデルで同一 fold・同一 seed
P2 baseline   src/ でシンプルなベースライン構築 → OOF/test を data/processed/preds/ へ
P3 特徴量     特徴量生成・前処理。同fold同モデルで delta 測定
P4 多様性     GBDT (LightGBM/XGBoost/CatBoost) + NN 等、誤り方の違う base を足す ← 最重要
P5 結合       アンサンブル / Stacking + 決定ルール（閾値等）の最適化
P6 honest検証 局所的改善や閾値調整は nested-CV をゲートに採否判定
P7 最終提出   分布を目視 → scripts/validate_submission.py → submit スキル
```

## P1: CV 設計を最初に固定する（最重要）

**間違った CV の上に積んだ改善は全部無駄になる。** 特徴量より先にここを決める。

| データの性質 | fold |
|--------------|------|
| i.i.d. 分類 | StratifiedKFold |
| i.i.d. 回帰 | KFold（歪んだ目的変数は binned stratify） |
| 同一エンティティが複数行（ユーザー/患者/レース/店舗） | GroupKFold / StratifiedGroupKFold |
| 時系列で test が未来 | TimeSeriesSplit or 時間基準の holdout |
| train/test の分布が違う | adversarial validation → fold選択 or 重み付け |

決めた fold と seed をプロジェクト設定に固定し、`.references/` と `CLAUDE.md` にも残す。

## リーク検査チェックリスト（P0 で必ず）

```
[ ] ID 列・行順に目的変数の情報が乗っていないか（id と target の相関、行順ソート）
[ ] 未来情報の混入（集計特徴を train 全体で作って fold をまたいでいないか）
[ ] 同一エンティティが train と valid に分かれていないか
[ ] test にしか無い / train にしか無いカテゴリ
[ ] 目的変数から算出された列が特徴量に混ざっていないか
[ ] target encoding は fold 内で fit しているか
```

疑わしい improvement（CV が急に跳ねる）は、まずリークを疑う。

## 伸び悩んだときの優先順位

1. **CV 設計を疑う**（リーク・fold 不一致）
2. **多様性を足す**（trees だけなら NN、NN だけなら trees。誤り方が違う base）
3. **metric に合わせた決定ルール**（閾値・クラス重み・順位変換）を nested-CV で調整
4. **特徴量**（比・差・相互作用、ドメイン指標、cyclic encoding、集約統計）
5. ハイパラ探索 ← 効果が最も小さい。ここから始めない

## 時間配分の目安

コンペ期間の
- 前半 25%: EDA + CV 設計 + baseline（ここを急ぐと後で全部やり直し）
- 中盤 50%: 特徴量 + 多様な base モデル
- 終盤 25%: 結合・決定ルール・honest 検証・最終提出の選択

**最終提出の2枠は「CV最良」と「頑健（分散が小さい / 単純）」に分けて確保する**
（`docs/agent/statistical-and-ml-guidelines.md`）。

## 毎ステップの規律

- 変更は一度に1つ。`experiment-log` スキルで `logs/EXPERIMENTS.md` に記録。
- 提出前は `submit` スキルの検証を通す。
- 提出枠を使い切らない。CV で選別してから投げる。
