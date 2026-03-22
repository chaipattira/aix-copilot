<!-- ABOUTME: Guides students through loading, merging, cleaning, and freezing the analytic dataset -->
<!-- ABOUTME: Uses hard gates, Socratic questioning, and plan approval before code generation -->
---
name: data-preparation
description: "Use when `analysis/research-question.md` exists but the frozen analytic file has not yet been saved"
---

## When to Use
The student has an approved research question (`analysis/research-question.md` exists) and is ready to prepare the analytic dataset.

## Gate In
Read `analysis/research-question.md`. If it does not exist, tell the student:
> "Before preparing your data, you need to define your research question. Please use the `research-question` skill first."
Do not proceed.

If `analysis/data-preparation.md` already exists, acknowledge it, read its contents, and ask which part the student wants to revisit. Overwrite on gate-out.

## Non-negotiable Rules
- Do not write any code until the student has answered all Socratic questions and explicitly approved the data preparation plan.
- Do not modify the frozen analytic file once it is saved — any changes require saving a new versioned file (e.g., `analytic_v2.rds`).

## Socratic Questions
Ask these questions ONE AT A TIME. Wait for the student's answer before proceeding. Do not answer these questions yourself.

1. What is your unit of observation (person, visit, region…)?
2. How many datasets do you need, and how do they link to each other?
3. What inclusion and exclusion criteria apply to your analytic sample?
4. For each variable in your research question: how is it measured in the raw data, and does it need transformation to best operationalize the concept?
5. What missingness do you expect, and how will you handle it?

## Plan Gate
Based on the student's answers, write a step-by-step data preparation plan covering: merge logic, restriction criteria, variable derivations, and error checks. Present this plan and wait for the student's explicit approval before writing any code.

## Code Pattern
Write code in this order, for both R and SAS.

**R:**
1. Load raw dataset(s)
2. Merge datasets (if needed): `dplyr::left_join()` or `merge()`
3. Apply inclusion/exclusion criteria: `dplyr::filter()` or base R subsetting
4. Error checks:
   - Duplicates: `sum(duplicated(df$id))`
   - Range checks: `range(df$age, na.rm = TRUE)`
   - Missingness: `colSums(is.na(df))`
5. Create derived variables
6. Save frozen analytic file: `saveRDS(analytic_df, "data/analytic.rds")`

**SAS:**
1. Load raw dataset(s) with `PROC IMPORT` or `LIBNAME`
2. Merge with `DATA` step `MERGE` or `PROC SQL JOIN`
3. Apply inclusion/exclusion criteria with `WHERE` or `IF` statements
4. Error checks:
   - Duplicates: `PROC SORT NODUPKEY` with `_ERROR_` check or `PROC FREQ`
   - Range checks: `PROC MEANS MIN MAX`
   - Missingness: `PROC MEANS NMISS`
5. Create derived variables in a `DATA` step
6. Save frozen analytic file to a permanent SAS library (e.g., `LIBNAME mylib 'path'; DATA mylib.analytic; ...`)

## Gate Out
Ask the student to confirm:
1. The frozen analytic file is saved to disk
2. The final sample size after all exclusions
3. The count excluded at each step

Save these to `analysis/data-preparation.md`:

```markdown
# Data Preparation Summary

**Frozen analytic file:** [filename and path]
**Final sample size:** [N]

**Exclusion counts:**
| Criterion | N excluded | N remaining |
|---|---|---|
| Starting N | — | [N] |
| [criterion 1] | [N] | [N] |

**Variables created:**
- [variable name]: [derivation description]
```

The next skill (`descriptive-analysis`) will not begin until this file exists.

## Common Mistakes
- Writing analysis code against raw data instead of the frozen analytic file
- Skipping error checks ("I'll check it later")
- Modifying the frozen analytic file after it is saved — save a new versioned file instead
