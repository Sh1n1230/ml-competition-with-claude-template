---
name: setup
description: Initialize a competition project (deps, dirs, references, CLAUDE.md) for any platform — Kaggle, SIGNATE, atmaCup/guruguru, Nishika, ProbSpace. Use when starting a new competition or when the user invokes /setup.
argument-hint: [competition-url-or-name]
---

# Project Setup (All-in-One, platform-agnostic)

## When to Use

- Starting a new competition project (any platform)
- User invokes `/setup` or `/setup <competition-url-or-name>`

## Step 0: Identify the Platform

Infer from the URL (or ask the user):

| Platform | URL pattern | Data / submit path |
|----------|-------------|--------------------|
| Kaggle | `kaggle.com/competitions/<slug>` | Kaggle MCP (`kaggle-*` skills) |
| SIGNATE | `signate.jp/competitions/<id>` | `signate` CLI (`signate` skill) |
| atmaCup / guruguru | `guruguru.science/competitions/<id>` | manual download + web UI |
| Nishika | `competition.nishika.com/competitions/<slug>` | manual download + web UI |
| ProbSpace | `comp.probspace.com/competitions/<slug>` | manual download + web UI |

Record the platform in `.references/COMPETITION.md` — every later skill routes on it.

## Step 1: Install Dependencies

```bash
uv sync
```

Optional groups: `uv sync --group nn` (PyTorch for neural network models),
`uv sync --group jp` (SIGNATE CLI + 日本語フォント).

## Step 2: Create Directory Structure

```bash
bash create_structure.sh
```

## Step 3: Fetch Competition Info

If a competition URL/name is given, follow `references/fetch-competition.md`.
It writes facts-only documents:

- `.references/COMPETITION.md` — platform, rules, timeline, submission limits
- `.references/DATASET.md` — files, columns, sizes, submission format
- `.references/METRIC.md` — metric definition, direction, scoring code

If nothing is provided, skip Steps 3–4.

## Step 4: Generate CLAUDE.md

Follow `references/create-claude-md.md` to rewrite `CLAUDE.md` with competition-specific
context (task type, metric, CV strategy, submission format), keeping the Hard Rules and
Skill Routing sections intact.

## Step 5: Initialize the Experiment Log

Create `logs/EXPERIMENTS.md` from the template in the `experiment-log` skill.
Every scored run goes there from now on.

## Report Results

| Step | Status |
|------|--------|
| Dependencies installed | ✅ / ❌ |
| Directories created | ✅ / ❌ |
| Competition info fetched | ✅ / ❌ / ⏭️ |
| CLAUDE.md generated | ✅ / ❌ |
| Experiment log initialized | ✅ / ❌ |

## Next Steps Guidance

1. Download data into `data/raw/` (`kaggle-datasets` or `signate` skill).
2. `/eda` on the training data.
3. Build a simple baseline model (`/baseline`) and verify submission format.

## Notes

- If `uv sync` fails, report the error and suggest a fix; do not silently continue.
- Existing directories are left untouched.
- API tokens live in the user's home directory, outside this repository.
  Never copy a token into the project or print its contents.
