---
name: descriptive-analysis
description: "Use when `analysis/data-preparation.md` exists but `analysis/table1-interpretation.md` does not — guides the student through Table 1 design, summary statistic choices, and distributional checks before writing any code"
---

## When to Use
The frozen analytic file is confirmed (`analysis/data-preparation.md` exists) and the student is ready to describe their study population.

## Gate In
Read `analysis/data-preparation.md` and `analysis/research-question.md`. If `data-preparation.md` does not exist, tell the student:
> "Before running descriptive analyses, you need to prepare your analytic file. Please use the `data-preparation` skill first."

If `analysis/table1-interpretation.md` already exists, acknowledge it, read its contents, and ask which part the student wants to revisit. Overwrite on gate-out.

## Non-negotiable Rules
- Do not write any code until the student has answered all Socratic questions and the Table 1 structure has been explicitly approved.
- Ask questions ONE AT A TIME. Do not ask the next question until the student has answered the current one.
- Do not write the student's Table 1 interpretation for them — ask for it and wait.
- Do not advance to `statistical-analysis` until the student has written their interpretation and it has been saved to `analysis/table1-interpretation.md`.

---

## Socratic Dialogue

### Phase 1: Analytic Sample Review

**Q1 — Sample confirmation:**
> "Let's start by reviewing your analytic sample. According to your data-preparation summary, what is the final N, and who is included? Can you confirm that the row count in your frozen analytic file matches?"

_Good answer:_ Reports the final N, mentions who was excluded, and verifies the count against the file ("My summary says N=1,842. I ran `nrow(analytic_df)` and confirmed it's 1,842 — they match").

_Weak answer:_ Restates the exclusion criteria from data-preparation without checking the actual file count.

_Probing:_ "Does `nrow(analytic_df)` (R) or `PROC CONTENTS` (SAS) match the final N in `analysis/data-preparation.md`? Load the file and verify."

---

### Phase 2: Table 1 Design

**Q2 — Variables and stratification:**
> "What characteristics should Table 1 display? List the variables that should appear as rows, and tell me: should the table be stratified by any variable? If so, which one and why?"

_Good answer:_ Lists specific variable names and explains the column structure ("I'll show age, sex, race, BMI, comorbidity index, and smoking status — stratified by my exposure `smoking_status` so readers can see whether exposed and unexposed groups are balanced on covariates").

_Weak answer:_ "The usual demographics" or "all the variables" without naming specific columns or justifying stratification.

_Probing:_ "Which specific variables from your frozen analytic file should appear in the table? Should the columns be overall only, or split by a variable — and if so, which one and why?"

---

**Q2.1 — Central tendency for continuous variables:**
> "For your continuous variables — [list them by name from the schema] — will you summarize each with mean or median? Why?"

_Good answer:_ Chooses per-variable and justifies by expected distribution ("BMI tends to be approximately symmetric so mean/SD; income is typically right-skewed so I'll use median/IQR").

_Weak answer:_ "Mean for all of them" without considering whether distributions are symmetric.

_Probing:_ "What do you expect the distribution of [variable] to look like? If it's right-skewed, the mean is pulled toward the high end — does that represent the typical patient?"

_Concept Block trigger:_ Student applies mean to a clearly skewed variable (income, hospital costs, length of stay).
> ★ Concept: Use mean/SD for approximately symmetric distributions. Use median/IQR for skewed distributions or when outliers are present — the median is resistant to extreme values and better represents the central observation. You don't need a formal normality test; a histogram is sufficient to judge.

---

**Q2.2 — Missing data in Table 1:**
> "For variables with missing data, will you report the percent missing as a separate category, or exclude observations with missing values from those rows? How does that connect to the missing data approach you chose during data preparation?"

_Good answer:_ States a consistent approach and ties it to the data-preparation plan ("I assumed MCAR and used complete cases, so I'll exclude missing from each row — but I'll note the denominator per variable so readers can see how many observations contributed").

_Weak answer:_ "I'll just exclude them" without connecting the decision to the data-preparation summary or thinking about transparency to readers.

_Probing:_ "If you silently exclude missing observations, readers won't know how many observations each row is based on. How can you make that transparent in the table?"

---

### Phase 3: Distribution Checks

**Q3 — Distributional assumptions:**
> "Before moving to your primary analysis, which continuous variables are worth inspecting for distributional problems — severe skewness, bimodal patterns, or outliers? What would you do if you found a problem?"

_Good answer:_ Names specific variables (particularly continuous predictors and a continuous outcome if applicable), says what they're looking for, and has a response plan ("If age-at-diagnosis is severely right-skewed I'd consider a log transformation before including it in the model").

_Weak answer:_ "I'll run histograms on everything" without saying what they're checking for or what they'd do about it.

_Probing:_ "For [variable], what shape in a histogram would tell you something needs to change before modeling?"

_Concept Block trigger:_ Student plans to skip distribution checks or doesn't connect them to modeling.
> ★ Concept: Many statistical models assume continuous variables are approximately normally distributed (or that residuals are). Severe right-skew may warrant a log transformation; bimodal distributions may indicate subgroups worth examining separately. These checks inform modeling decisions — they are not just exploratory.

---

## Plan Gate

Based on the student's answers, present this structure and wait for explicit approval before writing any code:

```
Table 1 rows:
  - [varname]: [continuous | categorical]
  - ...

Columns: [Overall only | Stratified by: varname]

Summary statistics:
  - Continuous: [mean (SD) | median (IQR)] — note per-variable if mixed
  - Categorical: [N (%) | N (%) with missing as separate row]

Distribution checks before modeling: [list continuous variables to inspect]
```

Do not write any code until the student says "yes" or otherwise explicitly confirms.

---

## Code Pattern

Write code in this order. Ask the student to review the output at each step before continuing.

**R:**
1. Load frozen analytic file: `analytic_df <- readRDS("data/analytic.rds")`
2. Confirm row count: `nrow(analytic_df)` — should match `analysis/data-preparation.md`
3. Missingness summary: `colSums(is.na(analytic_df))` — review before interpreting Table 1
4. Table 1: `gtsummary::tbl_summary()` or `tableone::CreateTableOne()` with the approved variable list and stratification
5. Distribution checks: `hist()` or `ggplot2::geom_histogram()` for each continuous variable flagged in Phase 3

**SAS:**
1. Load frozen analytic file from permanent library
2. Confirm row count: `PROC CONTENTS DATA=mylib.analytic; RUN;`
3. Missingness summary: `PROC MEANS DATA=mylib.analytic NMISS; VAR _NUMERIC_; RUN;`
4. Table 1: `PROC FREQ` (categorical) and `PROC MEANS` (continuous), or `PROC TABULATE` to combine both. `PROC REPORT` or `PROC SQL` for formatted output.
5. Distribution checks: `PROC UNIVARIATE DATA=mylib.analytic; HISTOGRAM; RUN;` or `PROC SGPLOT; HISTOGRAM varname; RUN;`

---

## Gate Out

Ask the student: "What does this table tell you about your population? Write 2–3 sentences in your own words." Wait for their response. Do not write the interpretation for them.

If the response is too brief or generic, probe: "What is surprising or noteworthy? How does the distribution of your exposure variable look across the sample?"

Save the student's interpretation to `analysis/table1-interpretation.md`:

```markdown
# Table 1 Interpretation

[Student's 2–3 sentence interpretation]
```

The next skill (`statistical-analysis`) will not begin until this file exists.

---

## Common Mistakes
- Generating Table 1 without first agreeing on which variables to include and whether to stratify
- Using mean for skewed variables without checking distributions first
- Silently excluding missing observations without noting the denominator per row
- Moving to modeling without saving the written Table 1 interpretation
- Not checking missingness in key variables before modeling
