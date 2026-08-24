# Regenerate CLAUDE.md for the competition

Read `.references/COMPETITION.md`, `DATASET.md`, `METRIC.md` and the actual project tree,
then rewrite the **competition-specific sections** of `CLAUDE.md`.

## Context

- @.references/COMPETITION.md
- @.references/DATASET.md
- @.references/METRIC.md
- Current tree: !`find . -maxdepth 2 -not -path '*/.*' -not -path './data/*' -not -path './.venv/*'`

## Rules

1. **Preserve** these sections verbatim — they are the template's spine, not competition data:
   - `## Hard Rules`
   - `## Directory Roles`
   - `## Skill Routing`
   - `## Project Context (docs/agent)`
2. **Regenerate** these sections from the reference docs:
   - `## Competition Summary` table (platform, task type, metric, direction, deadline,
     daily submission limit, submission style)
   - `## Problem Description`
   - `## Key Constraints`
   - `## Role Definition` — specialize to the task type and modality
   - `## CV Strategy` — the fold scheme implied by the data
     (StratifiedKFold / GroupKFold / StratifiedGroupKFold / TimeSeriesSplit) and *why*
   - `## Submission Format` — exact columns, dtype, header presence, delimiter, row order
3. Write `CLAUDE.md` in English (comments/docs in code stay English; user-facing reports 日本語).
4. Never delete the `Skill Routing` table entries; add rows if new skills were created.

## CV Strategy — how to choose (state the reason in CLAUDE.md)

| Data property | Fold scheme |
|---------------|-------------|
| i.i.d. rows, classification | `StratifiedKFold` |
| i.i.d. rows, regression | `KFold` (+ binned stratification for skewed targets) |
| repeated entity (user/patient/session/race) | `GroupKFold` / `StratifiedGroupKFold` |
| temporal, test is the future | `TimeSeriesSplit` or a fixed time-based holdout |
| train/test distribution differs | adversarial validation → weight or select folds |

Record the chosen scheme in your project config / baseline script too, so every base model shares identical folds.

## Execution

Overwrite `CLAUDE.md` with the merged result and show the user a diff summary of what changed.
