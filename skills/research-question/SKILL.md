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
