---
name: statistical-analysis
description: "Use when `analysis/table1-interpretation.md` exists but `analysis/model-interpretation.md` does not — guides model selection, confounder justification, and interpretation branched by research question type"
---

## When to Use
The student has reviewed their population (`analysis/table1-interpretation.md` exists) and is ready to run their primary analysis.

## Gate In
Read `analysis/table1-interpretation.md` and `analysis/research-question.md`. If `table1-interpretation.md` does not exist, tell the student:
> "Before running your primary analysis, you need to describe your population. Please use the `descriptive-analysis` skill first."

Check the `Question type` field in `analysis/research-question.md` — it determines which branching path to follow.

If `analysis/model-interpretation.md` already exists, acknowledge it and ask which part the student wants to revisit. Overwrite on gate-out.

## Non-negotiable Rules
- Do not write any code until the student has answered the relevant Socratic questions and the model specification has been explicitly approved.
- (Associational/causal path) Always write and run the crude model before the adjusted model.
- (Associational/causal path) Do not adjust for a variable unless the student can justify why it belongs in the model.
- Ask questions ONE AT A TIME.

---

## Branching by Research Question Type

| Question type | Path |
|---|---|
| Descriptive | Summarize distributions, prevalence/incidence; no exposure-outcome model |
| Predictive | Model with selected predictors; evaluate fit metrics (AUC, RMSE, R², pseudo-R²) |
| Associational or Causal | Crude model → adjusted model → optional EMM/mediation |

---

## Socratic Dialogue

### All Paths

**Q1 — Outcome variable type:**
> "What type of variable is your outcome — dichotomous (binary), continuous, count/rate, or ordinal? What are the possible values, and how is it coded in your frozen analytic file?"

_Good answer:_ Names the type, the coding, and connects it to model selection ("cancer_dx is binary, coded 0/1. That means logistic regression is appropriate and I'll get odds ratios").

_Weak answer:_ "It's binary" without coding details or without connecting to model family.

_Probing:_ "What are the possible values of your outcome variable in the frozen file? Does the coding match how you defined it in your research question?"

_Concept Block trigger:_ Student conflates ordinal with continuous, or doesn't connect outcome type to model family.
> ★ Concept: The outcome variable type determines the model family. Binary outcomes → logistic regression (binomial, logit link) for odds ratios, or log-binomial (binomial, log link) for risk ratios. Continuous outcomes → linear regression (Gaussian). Count outcomes → Poisson regression (Poisson, log link). Ordinal outcomes → ordinal logistic regression. Using the wrong model family produces biased estimates and incorrect standard errors.

---

**Q2 — Model choice:**
> "Given your outcome type and research question, which statistical model is appropriate? What does that model estimate — what specific quantity will it produce?"

_Good answer:_ Names the model, the estimand, and connects both to the research question ("Logistic regression estimates odds ratios. My question is about the association between smoking and cancer — an odds ratio is the right quantity for a binary outcome in an associational question").

_Weak answer:_ "Logistic regression because my outcome is binary" without naming the estimand or confirming it answers the question.

_Probing:_ "What specific quantity does that model output — an odds ratio, a mean difference, a risk ratio? Is that the quantity you need to answer your research question?"

_Concept Block trigger:_ Student chooses logistic regression but describes wanting risk ratios.
> ★ Concept: Logistic regression estimates odds ratios (OR), which approximate risk ratios (RR) when the outcome is rare (prevalence < 10%) but diverge as prevalence increases. If you want risk ratios directly, use log-binomial regression (`family = binomial(link = "log")` in R; `DIST=BIN LINK=LOG` in SAS PROC GENMOD) or Poisson regression with robust standard errors. Decide on the estimand before fitting the model.

---

### Associational/Causal Path

**Q3 — Sample size for confounder adjustment:**
> "You've identified [N] confounders to adjust for. How many outcome events are in your dataset? Divide that by the number of covariates you plan to include — what do you get?"

_Good answer:_ Counts outcome events (not total N), calculates events-per-variable (EPV), and assesses adequacy ("I have 124 cases and 8 covariates — EPV ≈ 15. That meets the 10 EPV guideline. I'll also check cell sizes within key strata").

_Weak answer:_ "I have 500 observations so it should be fine" — confuses total sample size with event count.

_Probing:_ "For binary outcomes, statistical power depends on the number of *events*, not total observations. Run `table(analytic_df$outcome)` (R) or `PROC FREQ` (SAS) — how many outcome events do you have? Divide by your number of covariates."

_Concept Block trigger:_ Student uses total sample size to assess adequacy for logistic regression.
> ★ Concept: For logistic regression, the effective sample size is the number of *outcome events* (the rarer category), not total observations. A common guideline is 10–20 events per predictor variable (EPV). Below 10 EPV, coefficient estimates become unstable and confidence intervals widen. Also check multivariate cell sizes — if any covariate strata have fewer than 5 events, consider collapsing categories or reducing the covariate set.

---

**Q4 — Effect modification:**
> "Do you have a scientific hypothesis that the effect of your exposure on your outcome might differ across levels of any particular variable? If so, which variable and why?"

_Good answer:_ Names a specific variable with a prior scientific justification ("I hypothesize the smoking–cancer association is stronger in older patients due to cumulative exposure — I'll test the smoking × age interaction term").

_Weak answer:_ "I'll check a few interactions and see what's significant" — exploratory without prior hypothesis.

_Probing:_ "What is your scientific basis for expecting the effect to differ in that subgroup? Testing interactions without a prior hypothesis inflates the false-positive rate."

_Concept Block trigger:_ Student confuses effect modification with confounding.
> ★ Concept: Effect modification (interaction) means the magnitude of the exposure-outcome association differs across strata of a third variable — it is a substantive finding to report, not bias to remove. Confounding is a nuisance to adjust away. Unlike confounders, effect modifiers are part of your answer. Test for interaction only when you have a prior scientific hypothesis — not as a fishing expedition.

---

**Q5 — Mediation (if in scope):**
> "Is there a variable you believe is on the causal pathway from your exposure to your outcome — something through which the exposure has its effect? Walk me through the hypothesized pathway and the temporal ordering."

_Good answer:_ Names the mediator, describes the pathway with temporal ordering, and confirms it is measured in the dataset ("Smoking → airway inflammation → cancer. Inflammation is measured at baseline before cancer diagnosis, and smoking precedes it. I want to decompose the total effect into direct and indirect").

_Weak answer:_ "I think [variable] might be in between" without temporal ordering or a mechanistic argument.

_Probing:_ "Does the exposure causally affect [mediator]? Does [mediator] independently affect [outcome] controlling for exposure? Are there any unmeasured variables that cause both [mediator] and [outcome]?"

_Concept Block trigger:_ Student proposes mediation with cross-sectional data or without temporal ordering.
> ★ Concept: Mediation analysis requires temporal ordering — exposure precedes mediator, mediator precedes outcome — and that no confounder of the mediator-outcome relationship was itself caused by the exposure (no treatment-induced confounding). With cross-sectional data, these conditions cannot be verified and mediation analysis is generally not defensible.

---

### Predictive Path

**Q3 — Predictor selection:**
> "Which variables will you include to predict your outcome? For each predictor, what is your evidence or reasoning that it will have predictive value?"

_Good answer:_ Lists specific column names with reasoning based on prior literature or domain knowledge, not causal language ("Age is a well-established predictor of cancer incidence; comorbidity index is included based on clinical evidence").

_Weak answer:_ Lists the confounders from the DAG, or says "the usual covariates," or justifies predictors in causal terms ("to adjust for confounding").

_Probing:_ "Why do you expect [predictor] to improve prediction of [outcome]? Is this based on prior literature or domain knowledge — not causal reasoning?"

_Concept Block trigger:_ Student selects predictors by consulting the DAG or using confounder language.
> ★ Concept: In predictive modeling, variables are included because they improve prediction accuracy — not because of their causal role. A mediator can be an excellent predictor even though adjusting for it would bias a causal estimate. Conversely, a strong confounder may add little predictive value. Select predictors based on expected contribution to prediction, not their position in the DAG.

---

## Plan Gate

Write the model specification for the student's path and wait for explicit approval:

**Descriptive path:**
```
Summary statistics to report: [list with measure type]
Stratifications: [list, or none]
```

**Predictive path:**
```
Model: [logistic | linear | Poisson | other]
Formula: outcome ~ predictor1 + predictor2 + ...
Fit metrics: [AUC | R² | RMSE | as appropriate for outcome type]
```

**Associational/causal path:**
```
Crude model:    outcome ~ exposure
Adjusted model: outcome ~ exposure + confounder1 + confounder2 + ...

Confounders justified:
  - [confounder1]: [one-line rationale from DAG]
  - ...

EMM (if applicable):     outcome ~ exposure * modifier + confounders
Mediation (if in scope): [pathway description]
```

Do not write any code until the student says "yes" or otherwise explicitly confirms.

---

## Code Pattern

**Descriptive path — R:**
```r
analytic_df <- readRDS("data/analytic.rds")

# Proportions / prevalence
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
LIBNAME mylib 'path/to/data';

PROC FREQ DATA=mylib.analytic;
  TABLES outcome / NOCUM;
RUN;

PROC FREQ DATA=mylib.analytic;
  TABLES stratum_var * outcome / NOCUM NOPERCENT;
RUN;
```

---

**Predictive path — R:**
```r
analytic_df <- readRDS("data/analytic.rds")

# Binary outcome: logistic regression (odds ratios)
model <- glm(outcome ~ predictor1 + predictor2,
             data = analytic_df, family = binomial(link = "logit"))
summary(model)
exp(coef(model))       # OR
exp(confint(model))    # 95% CI

# Continuous outcome: linear regression
# model <- lm(outcome ~ predictor1 + predictor2, data = analytic_df)
# summary(model)       # R-squared in summary output

# Count outcome: Poisson regression (rate ratios)
# model <- glm(outcome ~ predictor1 + predictor2,
#              data = analytic_df, family = poisson(link = "log"))
# exp(coef(model))     # Rate ratios

# AUC (binary outcomes only)
library(pROC)
roc_obj <- roc(analytic_df$outcome, fitted(model))
auc(roc_obj)
```

**Predictive path — SAS:**
```sas
/* Binary outcome: logistic regression */
PROC LOGISTIC DATA=mylib.analytic;
  MODEL outcome(EVENT='1') = predictor1 predictor2;
  ROC; /* prints AUC */
RUN;

/* Continuous outcome: linear regression */
/* PROC REG DATA=mylib.analytic;
     MODEL outcome = predictor1 predictor2;
   RUN; */

/* Count outcome: Poisson regression */
/* PROC GENMOD DATA=mylib.analytic;
     MODEL outcome = predictor1 predictor2 / DIST=POISSON LINK=LOG;
   RUN; */
```

---

**Associational/causal path — R:**
```r
analytic_df <- readRDS("data/analytic.rds")

# Crude model (always run first)
crude <- glm(outcome ~ exposure,
             data = analytic_df, family = binomial(link = "logit"))
summary(crude)
exp(coef(crude))       # OR
exp(confint(crude))    # 95% CI

# Adjusted model
adjusted <- glm(outcome ~ exposure + confounder1 + confounder2,
                data = analytic_df, family = binomial(link = "logit"))
summary(adjusted)
exp(coef(adjusted))
exp(confint(adjusted))

# EMM (if applicable)
emm_model <- glm(outcome ~ exposure * modifier + confounder1,
                 data = analytic_df, family = binomial(link = "logit"))
summary(emm_model)
```

**Associational/causal path — SAS:**
```sas
/* Crude model (always run first) */
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

---

## Gate Out

Ask the student to interpret their results in plain language. The prompt varies by path:
- **Descriptive:** "Summarize the key distributional findings in 2–3 sentences."
- **Predictive:** "How well does your model predict the outcome? What does the fit metric tell you practically?"
- **Associational/causal:** "What is the point estimate and confidence interval? What does it mean substantively? Does the direction and magnitude support your hypothesis?"

Wait for the student's response. Do not write the interpretation for them.

If the response focuses only on significance ("p < 0.05, so it's significant"), probe: "What is the direction and size of the effect? What does that mean for a real patient or population?"

Save to `analysis/model-interpretation.md`:

```markdown
# Model Interpretation

**Research question type:** [from research-question.md]

[Student's plain-language interpretation]
```

The next skill (`interpretation`) will not begin until this file exists.

---

## Common Mistakes
- Running the adjusted model without first running the crude model (associational/causal path)
- Adjusting for a collider or mediator without the student justifying why it belongs in the model
- Interpreting p-value significance without discussing effect size and direction
- Applying DAG/confounder framing to a predictive question
- Using total sample size (not event count) to assess adequacy for logistic regression
- Specifying `link` as a standalone argument to `glm()` — the link must be inside `family()`, e.g. `family = binomial(link = "logit")`, not `family = binomial, link = "logit"`
