---
name: signate
description: SIGNATE のコンペ一覧取得・データダウンロード・投稿を signate CLI で行う。SIGNATE のコンペに参加する / データを落とす / 提出する ときに使用。
argument-hint: [competition-key]
---

# SIGNATE (無料 CLI)

SIGNATE には MCP サーバがないため、公式 Python CLI（無料）を使う。
検証時点のバージョンは **0.12.0**（Python 3.8+）。

## 前提

```bash
uv add --group jp signate     # 依存に追加済みなら不要
uv run signate --version
```

認証設定は **ユーザーが対話的に実行する**（パスワード入力が必要なため、エージェントは実行しない）:

```bash
uv run signate token -e <登録メールアドレス>   # パスワードを対話入力 → トークンが保存される
```

トークンは `~/.signate/signate.json` に保存される。**リポジトリ内には置かない・内容を表示しない。**
未設定なら手順だけ案内してユーザーに実施してもらう。

## コマンド（0.12.0 系）

```bash
uv run signate competition-list                      # 参加可能なコンペ一覧（competition_key を得る）
uv run signate task-list --competition_key=<ckey>    # コンペ内の投稿可能タスク（task_key を得る）
uv run signate file-list --task_key=<tkey>           # 配布ファイル一覧（file_key・サイズ）
uv run signate download --task_key=<tkey> --file_key=<fkey> --path=data/raw/train.csv
uv run signate submit --task_key=<tkey> --path=./submission.csv --memo="lgbm cv0.8123"
```

**キーは3階層**: `competition_key` → `task_key` → `file_key`。
`download` / `submit` が要求するのは **`task_key`**（competition ではない）。
最初に `competition-list` → `task-list` → `file-list` の順で辿り、
得られたキーを `.references/COMPETITION.md` に記録しておく（毎回引き直さない）。

**`--path` は保存先の「ファイルパス」であり、ディレクトリではない**（実測）。
`--path=data/raw` のようにディレクトリを渡すと
`[Errno 21] Is a directory: 'data/raw.part' -> 'data/raw'` で失敗し、
`data/raw.part` というゴミが残る（消してから再実行する）。
`download` はファイル単位なので、`file-list` の各 `file_key` について
保存先ファイル名を明示して繰り返す:

```bash
uv run signate download --task_key=<tkey> --file_key=<k1> --path=data/raw/train.csv
uv run signate download --task_key=<tkey> --file_key=<k2> --path=data/raw/test.csv
uv run signate download --task_key=<tkey> --file_key=<k3> --path=data/raw/sample_submit.csv
```

## 提出ワークフロー

1. `.references/DATASET.md` の提出フォーマットを再確認する。
   **SIGNATE はヘッダ無し CSV/TSV が多い** — Kaggle の癖で `header=True` にすると 0 点になる。

   ```python
   # 例: ヘッダ無し・index無し・id昇順
   sub.write_csv("submission.csv", include_header=False)
   ```

2. 提出前チェック（必須）:

   ```bash
   uv run python scripts/validate_submission.py submission.csv --no-header
   ```

   行数 / ID 集合・順序 / 列数 / NaN・inf / 値域を sample と突合する。
3. `--memo` には **CV スコアと構成** を書く（`logs/EXPERIMENTS.md` の実験番号と対応付ける）。
4. 提出後、`experiment-log` スキルに従って CV と LB を並べて記録する。

## 注意

- **1日の投稿上限**はコンペごとに違う（多くは 5 回/日）。残り回数を意識し、CV で選別してから投げる。
- 順位表は Public/Private 分割があるコンペとないコンペがある。分割なしなら LB への
  フィッティングが即 shake につながるため、`docs/agent/statistical-and-ml-guidelines.md` の判断規律に従う。
- 締切は **JST**。Kaggle（UTC）と混同しない。
- ルール・評価指標・提出形式は CLI から取れない。Web ページ（`https://signate.jp/competitions/<id>`）
  を `WebFetch` で読むか、ユーザーに該当箇所を貼ってもらう（`setup` スキルの Method B）。
- 利用規約上、配布データの再配布・公開リポジトリへのコミットは禁止。`data/raw/` は
  `.gitignore` 済みだが、notebook 出力にデータを貼り付けないこと。
  外部GPU（Kaggle Datasets へのアップロード等）への持ち出しも規約確認が必要（`free-gpu` スキル）。
