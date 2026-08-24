# Fetch Competition Info (any platform)

Research the target competition and write `.references/COMPETITION.md`, `DATASET.md`, `METRIC.md`.

> **Rule: facts only.** No opinions, tips, or strategy in `.references/` — those belong in
> `logs/EXPERIMENTS.md` and modeling scripts. Reference docs must stay trustworthy.

---

## Method A — Kaggle (Kaggle MCP, preferred)

1. **Metadata**

   ```
   mcp__kaggle__get_competition({ request: { competitionName: "<slug>" } })
   ```

   Extract: title, description, category, reward, deadline, evaluation_metric,
   max_daily_submissions, max_team_size, is_kernels_submissions_only.

2. **Data files**

   ```
   mcp__kaggle__get_competition_data_files_summary({ request: { competitionName: "<slug>" } })
   mcp__kaggle__list_competition_data_files({ request: { competitionName: "<slug>", hasPageSize: true, pageSize: 50 } })
   ```

3. **Discussions** (facts about data quirks / leaks / official clarifications only)

   ```
   mcp__kaggle__list_forum_topics({ request: { hasSearchQuery: true, searchQuery: "<slug>", sortBy: "Hot", category: "Competitions" } })
   ```

---

## Method B — SIGNATE (`signate` CLI + web page)

1. Competition list / metadata:

   ```bash
   uv run signate competition-list                    # コンペ一覧 → competition_key
   uv run signate task-list --competition_key=<ckey>  # タスク一覧 → task_key
   uv run signate file-list --task_key=<tkey>         # 配布ファイルとサイズ → file_key
   ```

   得られた `competition_key` / `task_key` / `file_key` を `COMPETITION.md` に記録する
   （`download` と `submit` が要求するのは **`task_key`**）。

2. Rules, metric, submission format are only on the web page — read it with `WebFetch`
   (`https://signate.jp/competitions/<id>`) and, if login is required for the full text,
   ask the user to paste the relevant section rather than automating a login.

3. Note SIGNATE specifics in `COMPETITION.md`:
   - 1日あたりの投稿回数上限（コンペごとに異なる。多くは 5 回/日）
   - 提出ファイル形式（多くは **ヘッダ無し CSV / TSV**。Kaggle と違う点なので必ず確認）
   - 順位表は Public / Private 分割ありか、最終評価の対象提出の選び方

---

## Method C — atmaCup / guruguru, Nishika, ProbSpace (browser / manual)

1. Read the public overview pages with `WebFetch` first — it needs no login and is cheapest.
2. If the page requires a login, use the built-in browser tools
   (`mcp__Claude_Browser__navigate` / `read_page` / `get_page_text`) in the user's session,
   **or** simply ask the user to paste the rules and metric text.
   - Never enter credentials yourself; ask the user to log in.
3. Data download is manual on these platforms — instruct the user to place the archive under
   `data/raw/` and confirm the file list before proceeding.

---

## Step: Validate Against the Actual Data

Once files exist in `data/raw/`, cross-check the documents against reality:

```bash
uv run python - <<'PY'
import polars as pl
from commons.paths import raw_dir

for p in sorted(raw_dir().glob("*.csv")):
    df = pl.read_csv(p, n_rows=200)
    print(p.name, df.shape, df.columns[:15])
PY
```

Fix any mismatch in `DATASET.md` (column names, dtypes, row counts, submission columns).

---

## Document Templates

### `.references/COMPETITION.md`

```markdown
# Competition

| Item | Value |
|------|-------|
| Platform | Kaggle / SIGNATE / atmaCup / Nishika / ProbSpace |
| Name / ID | |
| URL | |
| Task type | Classification / Regression / Ranking / Segmentation / ... |
| Deadline (JST) | |
| Daily submission limit | |
| Final submissions selectable | |
| Team size limit | |
| Submission style | file upload / notebook (code competition) |
| External data allowed | yes / no / conditional |
| Prize / license terms | |

## Description
## Rules that constrain modeling
## Timeline
```

### `.references/DATASET.md`

```markdown
# Dataset

| File | Rows | Cols | Size | Note |
|------|------|------|------|------|

## Columns
| Column | Type | Description | Missing |

## Target
## Submission format
（列名・型・行数・ヘッダの有無・区切り文字・ID の順序制約）
## Known data quirks (facts only)
```

### `.references/METRIC.md`

```markdown
# Metric

| Item | Value |
|------|-------|
| Metric | |
| Direction | Maximize / Minimize |
| Prediction type | label / probability / numeric |

## Definition
（数式）

## Reference implementation
```python
# scikit-learn 等で厳密に再現できる実装。CV でこれを使う。
```

## Implications for CV / decision rule
（例: balanced accuracy なら per-class 閾値調整が必要、など事実ベースの帰結のみ）
```

---

## Final Step

Report which sections could not be filled and why (login wall, unclear rules), so the user
can supply the missing facts. Do not invent values.
