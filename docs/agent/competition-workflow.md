# コンペ進行ワークフロー

判断ルールの詳細は `.claude/skills/competition-workflow/SKILL.md`。

## 1. 開始時

- [ ] `/setup <url>` で `.references/` と `CLAUDE.md` を生成
- [ ] データを `data/raw/` に取得（`kaggle-datasets` / `signate` スキル）
- [ ] 規約確認（外部データ・外部コード・データ持ち出しの可否）
- [ ] `logs/EXPERIMENTS.md` を作成

## 2. EDA と CV 設計

- [ ] `/eda` を実行
- [ ] リーク検査チェックリストを通す
- [ ] fold 方式と seed を決めてプロジェクト設定に固定

## 3. baseline

- [ ] `src/<solution-name>/` 等でベースラインモデルを作成し OOF/test を出す
- [ ] `logs/EXPERIMENTS.md` に記録
- [ ] 初回提出で LB と CV の関係を測る

## 4. 改善ループ（1回1変更）

- [ ] 特徴量 → 同fold同モデルで delta 測定
- [ ] 多様な base 追加（NN / GBDT 複数種）
- [ ] stacking と決定ルール調整
- [ ] nested-CV ゲートを通してから採用

## 5. 終盤

- [ ] 最終提出2枠を「CV最良」「頑健」で分ける
- [ ] `scripts/validate_submission.py` を通す
- [ ] 終了後、効いたこと・効かなかったことを振り返る
