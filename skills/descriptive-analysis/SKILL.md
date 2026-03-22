<!-- ABOUTME: Guides students to produce Table 1 and describe the study population -->
<!-- ABOUTME: Uses hard gates, Socratic questioning, and plan approval before code generation -->
---
name: descriptive-analysis
description: "Use when `analysis/data-preparation.md` exists but `analysis/table1-interpretation.md` does not"
---

## When to Use
The frozen analytic file is confirmed (`analysis/data-preparation.md` exists) and the student is ready to describe their study population.

## Gate In
Read `analysis/data-preparation.md` and `analysis/research-question.md`. If `data-preparation.md` does not exist, tell the student:
> "Before running descriptive analyses, you need to prepare your analytic file. Please use the `data-preparation` skill first."

If `analysis/table1-interpretation.md` already exists, acknowledge it, read its contents, and ask which part the student wants to revisit. Overwrite on gate-out.

## Non-negotiable Rules
- Do not write any code until the student has answered all Socratic questions and the Table 1 structure has been explicitly approved.
- Do not advance to `statistical-analysis` until the student has written their Table 1 interpretation and it has been saved to `analysis/table1-interpretation.md`.

## Socratic Questions
Ask these questions ONE AT A TIME. Wait for the student's answer before proceeding. Do not answer these questions yourself.

1. What does your analytic sample look like — who is included, who is excluded, and why?
2. What characteristics should Table 1 display? Should it be stratified by exposure or another variable?
3. Are there any distributional assumptions you should check before modeling (e.g., skewness of continuous variables)?

## Plan Gate
Based on the student's answers, write a Table 1 structure: rows (variables), columns (overall ± strata), and the summary statistic for each variable type (mean/SD for continuous, N/% for categorical). Present this and wait for explicit approval before writing code.

## Code Pattern
Write code in this order, for both R and SAS.

**R:**
1. Load frozen analytic file: `analytic_df <- readRDS("data/analytic.rds")`
2. Table 1: `gtsummary::tbl_summary()` or `tableone::CreateTableOne()`
3. Distribution checks: `hist()` or `ggplot2::geom_histogram()` for continuous variables
4. Missingness summary: `colSums(is.na(analytic_df))`

**SAS:**
1. Load frozen analytic file from permanent library
2. Table 1: `PROC FREQ` (categorical) and `PROC MEANS` (continuous), or a `%table1` macro if available in the student's environment
3. Distribution checks: `PROC UNIVARIATE` with `HISTOGRAM` statement
4. Missingness summary: `PROC MEANS NMISS`

## Gate Out
Ask the student: "What does this table tell you about your population? Write 2–3 sentences in your own words." Wait for their response. Do not write the interpretation for them.

Save the student's interpretation to `analysis/table1-interpretation.md`:

```markdown
# Table 1 Interpretation

[Student's 2–3 sentence interpretation]
```

The next skill (`statistical-analysis`) will not begin until this file exists.

## Common Mistakes
- Generating Table 1 without discussing what it should show
- Moving to modeling without saving the written Table 1 interpretation
- Not checking missingness in key variables before modeling
