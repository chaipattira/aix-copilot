# Data Analysis Workflow Plugin Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a Claude Code plugin with 5 skills that guide epidemiology students through data analysis using hard gates, Socratic questions, and plan-approval before code.

**Architecture:** Five `SKILL.md` files in `skills/<name>/SKILL.md`, each enforcing a strict gate-in (check for artifact file), Socratic questioning, plan approval, code generation, and gate-out (write artifact file). Skills chain in order: `research-question → data-preparation → descriptive-analysis → statistical-analysis → interpretation`. Artifact files live in the student's `analysis/` directory.

**Tech Stack:** Markdown (SKILL.md), YAML frontmatter, Claude Code plugin system, R and SAS (code examples inside skill files)

---

## File Map

| File | Action | Purpose |
|---|---|---|
| `package.json` | Create | Plugin manifest |
| `README.md` | Create | Project overview and progress log |
| `skills/research-question/SKILL.md` | Create | Skill 1: define research question |
| `skills/data-preparation/SKILL.md` | Create | Skill 2: prepare analytic dataset |
| `skills/descriptive-analysis/SKILL.md` | Create | Skill 3: Table 1 and population description |
| `skills/statistical-analysis/SKILL.md` | Create | Skill 4: primary analysis (branching by question type) |
| `skills/interpretation/SKILL.md` | Create | Skill 5: visualizations, sensitivity analyses, write-up scaffold |

---

## Task 1: Plugin Skeleton

**Files:**
- Create: `package.json`
- Create: `README.md`

- [ ] **Step 1: Create `package.json`**

```json
{
  "name": "aix-data-analysis",
  "version": "0.1.0",
  "description": "Claude Code plugin for epidemiology data analysis workflows"
}
```

- [ ] **Step 2: Create `README.md`**

```markdown
# aix-data-analysis

A Claude Code plugin that guides students through epidemiological data analysis.

## Skills

| Skill | Purpose |
|---|---|
| `research-question` | Define research question, exposure, outcome, and DAG |
| `data-preparation` | Load, merge, clean, and freeze the analytic dataset |
| `descriptive-analysis` | Produce Table 1 and describe the study population |
| `statistical-analysis` | Run crude and adjusted models (branches by question type) |
| `interpretation` | Visualize results, run sensitivity analyses, scaffold write-up |

## Usage

Students invoke skills in order. Each skill enforces a hard gate: it checks for the prior skill's artifact file before proceeding.

## Progress Log

- 2026-03-22: Plugin skeleton and all 5 skill files created
```

- [ ] **Step 3: Verify both files exist**

```bash
ls package.json README.md
```
Expected: both files listed.

- [ ] **Step 4: Commit**

```bash
git add package.json README.md
git commit -m "feat: add plugin manifest and README"
```

---

## Task 2: `research-question` Skill

**Files:**
- Create: `skills/research-question/SKILL.md`

- [ ] **Step 1: Create the directory and skill file**

```bash
mkdir -p skills/research-question
```

Write `skills/research-question/SKILL.md`:

````markdown
---
name: research-question
description: "Use when the student has a dataset but has not yet written a research question in `analysis/research-question.md`"
---

## When to Use
The student has a dataset and a vague or unstated research question. No prior skill output is required.

## Gate In
Check whether `analysis/research-question.md` exists in the project directory.
- If it exists: acknowledge it, read its contents, and ask which part the student wants to revisit. Overwrite the file on gate-out.
- If it does not exist: ask the student to paste their dataset schema (`str()` output in R or `PROC CONTENTS` output in SAS) before asking any other questions. Do not proceed until the schema is provided.

## Non-negotiable Rules
- Do not begin the Socratic questions until the student has shared the dataset schema.
- Do not define the research question for the student — ask, don't tell.

## Socratic Questions
Ask these questions ONE AT A TIME. Wait for the student's answer before proceeding. Do not answer these questions yourself.

1. What phenomenon are you trying to understand with this data?
2. What type of research question is this — descriptive (what is the prevalence/distribution?), predictive (what predicts my outcome?), associational (is X associated with Y?), or causal (does X cause Y)?
3. What is your primary outcome of interest? Looking at the column list you shared, how is it measured in the data?
4. (If associational or causal) What is your primary exposure of interest?
5. (If associational or causal) Draw a DAG: what variables might confound the relationship between your exposure and outcome?
6. (If associational or causal) Are there effect modifiers or mediators you want to examine?

## Plan Gate
Based on the student's answers, write a one-sentence research question statement, a variable list (outcome, exposure if applicable, confounders if applicable), and the question type. Present this plan and wait for the student's explicit approval.

Do not save the artifact until the student confirms the plan is correct.

## Code Pattern
No code in this skill.

## Gate Out
Save the approved content to `analysis/research-question.md` using this template:

```markdown
# Research Question

**Question type:** [descriptive | predictive | associational | causal]

**Research question:** [one sentence]

**Variables:**
- Outcome: [variable name and how it's measured]
- Exposure: [variable name and how it's measured, or N/A]
- Confounders: [list, or N/A]
- Effect modifiers / mediators: [list, or N/A]
```

The next skill (`data-preparation`) will not begin until this file exists.

## Common Mistakes
- Claude answers the Socratic questions instead of asking them
- Student says "just run the analysis" — decline and explain that defining the question first prevents wasted effort
- Proceeding without the dataset schema — leads to generic, useless variable questions
- Letting data availability drive the research question instead of scientific reasoning
````

- [ ] **Step 2: Verify the file has all required sections**

```bash
grep -c "## " skills/research-question/SKILL.md
```
Expected: 7 or more (When to Use, Gate In, Non-negotiable Rules, Socratic Questions, Plan Gate, Code Pattern, Gate Out, Common Mistakes).

- [ ] **Step 3: Commit**

```bash
git add skills/research-question/SKILL.md
git commit -m "feat: add research-question skill"
```

---

## Task 3: `data-preparation` Skill

**Files:**
- Create: `skills/data-preparation/SKILL.md`

- [ ] **Step 1: Create the directory and skill file**

```bash
mkdir -p skills/data-preparation
```

Write `skills/data-preparation/SKILL.md`:

````markdown
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
````

- [ ] **Step 2: Verify the file has all required sections**

```bash
grep -c "## " skills/data-preparation/SKILL.md
```
Expected: 7 or more.

- [ ] **Step 3: Commit**

```bash
git add skills/data-preparation/SKILL.md
git commit -m "feat: add data-preparation skill"
```

---

## Task 4: `descriptive-analysis` Skill

**Files:**
- Create: `skills/descriptive-analysis/SKILL.md`

- [ ] **Step 1: Create the directory and skill file**

```bash
mkdir -p skills/descriptive-analysis
```

Write `skills/descriptive-analysis/SKILL.md`:

````markdown
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
````

- [ ] **Step 2: Verify the file has all required sections**

```bash
grep -c "## " skills/descriptive-analysis/SKILL.md
```
Expected: 7 or more.

- [ ] **Step 3: Commit**

```bash
git add skills/descriptive-analysis/SKILL.md
git commit -m "feat: add descriptive-analysis skill"
```

---

## Task 5: `statistical-analysis` Skill

**Files:**
- Create: `skills/statistical-analysis/SKILL.md`

- [ ] **Step 1: Create the directory and skill file**

```bash
mkdir -p skills/statistical-analysis
```

Write `skills/statistical-analysis/SKILL.md`:

````markdown
---
name: statistical-analysis
description: "Use when `analysis/table1-interpretation.md` exists but `analysis/model-interpretation.md` does not"
---

## When to Use
The student has reviewed their population (`analysis/table1-interpretation.md` exists) and is ready to run their primary analysis.

## Gate In
Read `analysis/table1-interpretation.md` and `analysis/research-question.md`. If `table1-interpretation.md` does not exist, tell the student:
> "Before running your primary analysis, you need to describe your population. Please use the `descriptive-analysis` skill first."

Check the `Question type` field in `analysis/research-question.md` — it determines which branching path to follow (see Branching below).

If `analysis/model-interpretation.md` already exists, acknowledge it and ask which part the student wants to revisit. Overwrite on gate-out.

## Non-negotiable Rules
- Do not write any code until the student has answered the relevant Socratic questions and the model specification has been explicitly approved.
- (Associational/causal path) Always write and run the crude model before the adjusted model.
- (Associational/causal path) Do not adjust for a variable unless the student can justify why it belongs in the model.

## Branching by Research Question Type

The question type from `analysis/research-question.md` determines the path:

| Question type | Path |
|---|---|
| Descriptive | Summarize distributions, prevalence/incidence; no exposure-outcome model |
| Predictive | Model with selected predictors; evaluate fit metrics (AUC, RMSE) |
| Associational or Causal | Crude model → adjusted model → optional EMM/mediation |

## Socratic Questions
Ask only the questions relevant to the student's question type. Ask ONE AT A TIME.

**All paths:**
1. What type is your outcome variable — dichotomous, categorical, count/rate, or continuous?
2. Given your outcome type and research question, which statistical model (or summary approach) is appropriate and why?

**Associational/causal path only:**
3. Which confounders from your DAG will you adjust for in the adjusted model?
4. Will you test for effect modification? If so, by which variable, and why?
5. Is mediation in scope? If so, what is the hypothesized pathway?

**Predictive path only:**
3. Which predictors will you include, and why? (Do not frame predictors as confounders — that applies causal logic to a predictive question.)

## Plan Gate
Write a model specification appropriate to the path and wait for explicit approval:
- Descriptive: list the summary statistics and stratifications
- Predictive: model formula, outcome type, fit metric(s) to report
- Associational/causal: crude model formula, adjusted model formula, any EMM/mediation models

Do not write any code until the student approves.

## Code Pattern

**Descriptive path — R:**
```r
# Load frozen analytic file
analytic_df <- readRDS("data/analytic.rds")

# Prevalence / proportions
table(analytic_df$outcome)
prop.table(table(analytic_df$outcome))

# Stratified summary
library(dplyr)
analytic_df |>
  group_by(stratum_var) |>
  summarise(n = n(), prevalence = mean(outcome, na.rm = TRUE))
```

**Descriptive path — SAS:**
```sas
/* Load frozen analytic file */
LIBNAME mylib 'path/to/data';

/* Frequency table */
PROC FREQ DATA=mylib.analytic;
  TABLES outcome / NOCUM;
RUN;

/* Stratified summary */
PROC FREQ DATA=mylib.analytic;
  TABLES stratum_var * outcome / NOCUM NOPERCENT;
RUN;
```

**Predictive path — R:**
```r
analytic_df <- readRDS("data/analytic.rds")

# Fit model (example: logistic for binary outcome)
model <- glm(outcome ~ predictor1 + predictor2,
             data = analytic_df, family = binomial)
summary(model)

# AUC (binary)
library(pROC)
roc_obj <- roc(analytic_df$outcome, fitted(model))
auc(roc_obj)
```

**Predictive path — SAS:**
```sas
PROC LOGISTIC DATA=mylib.analytic;
  MODEL outcome(EVENT='1') = predictor1 predictor2;
  ROC; /* prints AUC */
RUN;
```

**Associational/causal path — R:**
```r
analytic_df <- readRDS("data/analytic.rds")

# Crude model
crude <- glm(outcome ~ exposure,
             data = analytic_df, family = binomial)
summary(crude)
exp(coef(crude))          # OR
exp(confint(crude))       # 95% CI

# Adjusted model
adjusted <- glm(outcome ~ exposure + confounder1 + confounder2,
                data = analytic_df, family = binomial)
summary(adjusted)
exp(coef(adjusted))
exp(confint(adjusted))

# EMM (if applicable)
emm_model <- glm(outcome ~ exposure * modifier + confounder1,
                 data = analytic_df, family = binomial)
summary(emm_model)
```

**Associational/causal path — SAS:**
```sas
/* Crude model */
PROC LOGISTIC DATA=mylib.analytic;
  MODEL outcome(EVENT='1') = exposure;
  ODDSRATIO exposure;
RUN;

/* Adjusted model */
PROC LOGISTIC DATA=mylib.analytic;
  MODEL outcome(EVENT='1') = exposure confounder1 confounder2;
  ODDSRATIO exposure;
RUN;

/* EMM (if applicable) */
PROC LOGISTIC DATA=mylib.analytic;
  MODEL outcome(EVENT='1') = exposure modifier exposure*modifier confounder1;
  ODDSRATIO exposure / AT (modifier = 0 1);
RUN;
```

## Gate Out
Ask the student to interpret their results in plain language. Prompt varies by path:
- Descriptive: "Summarize the key distributional findings in 2–3 sentences."
- Predictive: "How well does your model predict the outcome? What does that mean practically?"
- Associational/causal: "What is the point estimate and confidence interval? What does it mean substantively? Does it support your hypothesis?"

Wait for the student's response. Do not write the interpretation for them.

Save to `analysis/model-interpretation.md`:

```markdown
# Model Interpretation

**Research question type:** [from research-question.md]

[Student's plain-language interpretation]
```

The next skill (`interpretation`) will not begin until this file exists.

## Common Mistakes
- Running the adjusted model without first running the crude model (associational/causal path)
- Adjusting for colliders or mediators without the student justifying why
- Interpreting p-value significance without discussing effect size and direction
- Applying DAG/confounder framing to a descriptive or predictive question
````

- [ ] **Step 2: Verify the file has all required sections**

```bash
grep -c "## " skills/statistical-analysis/SKILL.md
```
Expected: 8 or more (includes Branching section).

- [ ] **Step 3: Commit**

```bash
git add skills/statistical-analysis/SKILL.md
git commit -m "feat: add statistical-analysis skill"
```

---

## Task 6: `interpretation` Skill

**Files:**
- Create: `skills/interpretation/SKILL.md`

- [ ] **Step 1: Create the directory and skill file**

```bash
mkdir -p skills/interpretation
```

Write `skills/interpretation/SKILL.md`:

````markdown
---
name: interpretation
description: "Use when `analysis/model-interpretation.md` exists but `analysis/final-interpretation.md` does not"
---

## When to Use
The student has run their primary analysis and written a plain-language interpretation (`analysis/model-interpretation.md` exists). They are ready to finalize their interpretation, produce a visualization, and run sensitivity analyses.

## Gate In
Read `analysis/model-interpretation.md` and `analysis/research-question.md`. If `model-interpretation.md` does not exist, tell the student:
> "Before finalizing your interpretation, you need to complete your primary analysis. Please use the `statistical-analysis` skill first."

Check the question type in `analysis/research-question.md` — it determines which plot and sensitivity analyses apply.

If `analysis/final-interpretation.md` already exists, acknowledge it and ask which part the student wants to revisit. Overwrite on gate-out.

## Non-negotiable Rules
- Do not produce visualizations or sensitivity analyses until the student has answered all Socratic questions and the plan has been explicitly approved.
- Do not write the interpretation for the student — provide a scaffold with labeled sections. The student fills in the prose.

## Socratic Questions
Ask these questions ONE AT A TIME. Wait for the student's answer before proceeding.

1. Do your results support, partially support, or contradict your original hypothesis? Why?
2. What are the main threats to internal validity in this study (confounding, selection bias, information bias)?
3. What sensitivity analyses would strengthen your conclusions?
4. What are the key strengths and limitations of this analysis?

## Plan Gate
Based on the student's answers, write a list of: (1) one summary plot, (2) any sensitivity analyses. Present this plan and wait for explicit approval before writing any code.

## Code Pattern
Write one plot and any sensitivity analyses for both R and SAS. Plot choice and sensitivity analyses depend on question type (read from `analysis/research-question.md`).

**Descriptive path — R:**
```r
library(ggplot2)
analytic_df <- readRDS("data/analytic.rds")

# Bar chart or histogram for key variable distribution
ggplot(analytic_df, aes(x = key_variable)) +
  geom_bar() +
  labs(title = "Distribution of [variable]", x = "[label]", y = "Count")
```

**Descriptive path — SAS:**
```sas
PROC SGPLOT DATA=mylib.analytic;
  VBAR key_variable;
  TITLE "Distribution of [variable]";
RUN;
```

**Predictive path — R:**
```r
library(pROC)
# ROC curve (binary outcome)
roc_obj <- roc(analytic_df$outcome, fitted(model))
plot(roc_obj, main = paste("AUC =", round(auc(roc_obj), 3)))
```

**Predictive path — SAS:**
```sas
/* ROC curve output from PROC LOGISTIC */
PROC LOGISTIC DATA=mylib.analytic;
  MODEL outcome(EVENT='1') = predictor1 predictor2;
  ROC;
RUN;
```

**Associational/causal path — R:**
```r
library(broom)
library(ggplot2)

# Coefficient plot (crude and adjusted side by side)
crude_tidy    <- tidy(crude_model,    conf.int = TRUE, exponentiate = TRUE)
adjusted_tidy <- tidy(adjusted_model, conf.int = TRUE, exponentiate = TRUE)

crude_tidy$model    <- "Crude"
adjusted_tidy$model <- "Adjusted"

plot_data <- rbind(
  crude_tidy[crude_tidy$term == "exposure", ],
  adjusted_tidy[adjusted_tidy$term == "exposure", ]
)

ggplot(plot_data, aes(x = estimate, y = model, xmin = conf.low, xmax = conf.high)) +
  geom_point() +
  geom_errorbarh(height = 0.2) +
  geom_vline(xintercept = 1, linetype = "dashed") +
  labs(title = "Crude and Adjusted Estimates", x = "Odds Ratio (95% CI)", y = "")
```

**Associational/causal path — SAS:**
```sas
/* Extract OR and CI from ODS output, then plot */
ODS OUTPUT OddsRatios=or_table;
PROC LOGISTIC DATA=mylib.analytic;
  MODEL outcome(EVENT='1') = exposure confounder1 confounder2;
  ODDSRATIO exposure;
RUN;
ODS OUTPUT CLOSE;

PROC SGPLOT DATA=or_table;
  SCATTER X=OddsRatioEst Y=Effect /
    XERRORLOWER=LowerCL XERRORUPPER=UpperCL
    MARKERATTRS=(SYMBOL=CircleFilled);
  REFLINE 1 / AXIS=X LINEATTRS=(PATTERN=Dash);
  TITLE "Crude and Adjusted Odds Ratios";
RUN;
```

**Sensitivity analyses (associational/causal path only) — R:**
```r
library(EValue)
# For an odds ratio (use evalues.RR for risk ratios, evalues.RD for risk differences)
evalues.OR(est = [point_estimate], lo = [lower_CI], hi = [upper_CI], rare = FALSE)
```

**Sensitivity analyses (associational/causal path only) — SAS:**
```sas
/* E-value formula: E = estimate + sqrt(estimate * (estimate - 1))  */
/* where estimate is the OR/RR. Compute manually: */
DATA evalue;
  OR   = [point_estimate];
  Eval = OR + SQRT(OR * (OR - 1));
  PUT "E-value: " Eval;
RUN;
```

## Gate Out
Terminal skill. Provide this scaffold and ask the student to fill it in:

```markdown
# Final Interpretation

**Main finding:** [1–2 sentences: what did you find?]

**Direction and magnitude:** [What was the effect size? Is it clinically or practically meaningful?]

**Threats to validity:** [What are the main limitations — confounding, selection bias, information bias?]

**Sensitivity analysis results:** [What did the sensitivity analysis show? Does it strengthen or weaken your conclusion?]

**Strengths:** [What does this study do well?]

**Limitations:** [What would you do differently with more time or data?]

**Conclusion:** [1 sentence: what should a reader take away from this analysis?]
```

Save the completed scaffold to `analysis/final-interpretation.md`.

## Common Mistakes
- Writing the interpretation for the student instead of scaffolding it
- Jumping to visualizations before running any sensitivity analyses
- Listing limitations as a separate afterthought rather than connecting them to specific results
- Offering E-value to descriptive or predictive question students (E-value only applies to associational/causal questions)
````

- [ ] **Step 2: Verify the file has all required sections**

```bash
grep -c "## " skills/interpretation/SKILL.md
```
Expected: 7 or more.

- [ ] **Step 3: Commit**

```bash
git add skills/interpretation/SKILL.md
git commit -m "feat: add interpretation skill"
```

---

## Task 7: Final Verification

- [ ] **Step 1: Confirm all 5 skills exist**

```bash
find skills -name "SKILL.md" | sort
```
Expected output:
```
skills/data-preparation/SKILL.md
skills/descriptive-analysis/SKILL.md
skills/interpretation/SKILL.md
skills/research-question/SKILL.md
skills/statistical-analysis/SKILL.md
```

- [ ] **Step 2: Confirm all skills have required frontmatter**

```bash
grep -l "^name:" skills/*/SKILL.md
grep -l "^description:" skills/*/SKILL.md
```
Expected: all 5 files listed for each command.

- [ ] **Step 3: Confirm all gate artifact filenames are consistent with the spec**

```bash
grep -h "analysis/" skills/*/SKILL.md | grep -E "\.(md)" | sort -u
```
Expected: references to `analysis/research-question.md`, `analysis/data-preparation.md`, `analysis/table1-interpretation.md`, `analysis/model-interpretation.md`, `analysis/final-interpretation.md` — and no others.

- [ ] **Step 4: Update README.md progress log**

Add to `README.md`:
```markdown
- 2026-03-22: All 5 skill files verified
```

- [ ] **Step 5: Commit**

```bash
git add README.md
git commit -m "chore: verify all skills and update progress log"
```
