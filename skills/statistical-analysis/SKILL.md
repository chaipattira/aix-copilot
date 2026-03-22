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
