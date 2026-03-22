<!-- ABOUTME: Guides students through visualizations, sensitivity analyses, and final write-up scaffold -->
<!-- ABOUTME: Terminal skill — produces final-interpretation.md with no downstream gate -->
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
Write one plot and the relevant sensitivity analyses for both R and SAS.

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
