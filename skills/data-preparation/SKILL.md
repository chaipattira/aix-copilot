---
name: data-preparation
description: "Use when `analysis/research-question.md` exists but the frozen analytic file has not yet been saved — guides the student through dataset structure, sample definition, variable operationalization, and missing data before writing any code"
---

## When to Use
The student has an approved research question (`analysis/research-question.md` exists) and is ready to prepare the analytic dataset.

## Gate In
Read `analysis/research-question.md`. If it does not exist, tell the student:
> "Before preparing your data, you need to define your research question. Please use the `research-question` skill first."
Do not proceed.

If `analysis/data-preparation.md` already exists, acknowledge it, read its contents, and ask which part the student wants to revisit. Overwrite on gate-out.

## Non-negotiable Rules
- Do not ask any Socratic question until the student has shared their dataset schema. If they try to skip it, say: "Before we work on your data preparation, I need to see your dataset's variables. Please paste the output of `str()` (R) or `PROC CONTENTS` (SAS) for each dataset you're using."
- Ask questions ONE AT A TIME. Do not ask the next question until the student has answered the current one.
- Do not write any code until the student has answered all Socratic questions and explicitly approved the data preparation plan.
- Do not modify the frozen analytic file once it is saved — any changes require saving a new versioned file (e.g., `analytic_v2.rds`).
- If the student gives a vague or one-word answer: probe with a follow-up. Do not accept "it looks fine" and move on.

---

## Socratic Dialogue

### Phase 1: Schema (always required first)

Check whether `analysis/research-question.md` contains the dataset schema. If it does, use it and skip this step. Otherwise, ask:

> "To help you prepare your analytic dataset, I need to see the variables in each dataset you'll be using. Please paste the output of `str()` (R) or `PROC CONTENTS` (SAS) for each dataset."

Wait for the schema. Do not proceed until it is provided.

---

### Phase 2: Dataset Structure

**Q1 — Unit of observation:**
> "What is your unit of observation — what does one row represent in your raw data? For example: one person, one clinical visit, one geographic region. And is the unit consistent across all the datasets you're using?"

_Good answer:_ Names the entity and its identifier ("Each row is one participant, identified by `PATID`. Both datasets use the same structure").

_Weak answer:_ "People" or "patients" — too vague, doesn't address whether the unit is consistent across datasets.

_Probing:_ "What does one row represent in each of your raw datasets? Could a single patient appear in more than one row — for example, one row per visit?"

_Concept Block trigger:_ Student confuses the unit of observation with the unit of analysis (e.g., says "patients" when the raw data has one row per visit).
> ★ Concept: The unit of observation is what one row represents in the raw data. The unit of analysis is the entity you draw conclusions about. If your raw data has one row per hospital visit but you're studying patients, you'll need to collapse visits to one row per patient before analysis. Mismatching these inflates your sample size and introduces statistical dependence.

---

**Q2 — Variable sources and merge keys:**
> "Which variables in your research question come from which datasets? And what is the unique identifier that links your datasets together?"

_Good answer:_ Lists specific column names from each dataset, names the join key, and states whether the key is unique in both datasets ("Exposure `smoking_status` is in `cohort.csv`, outcome `cancer_dx` is in `claims.csv`, joined on `PATID` which is unique in both").

_Weak answer:_ "I'll merge them by patient ID" — doesn't confirm which datasets, which columns, or whether the key is unique.

_Probing:_ "Is the join key guaranteed to be unique in both datasets? What do you expect the cardinality to be — one row per patient in each dataset, or could one patient have multiple rows in either?"

_Concept Block trigger:_ Student assumes the merge will produce the right number of rows without checking.
> ★ Concept: Before merging, always verify whether the join key is unique in each dataset. A one-to-many join (one row in dataset A matches multiple rows in dataset B) silently multiplies rows and inflates your sample size. Check for duplicates on the join key before merging, then check the row count after — it should match your expectation.

---

### Phase 3: Sample Definition

**Q3 — Inclusion and exclusion criteria:**
> "What inclusion and exclusion criteria define your analytic sample? For each criterion, which specific variable captures it, and what value or range defines the cutoff?"

_Good answer:_ Lists criteria with specific variable names and values, in the order they'll be applied ("Include adults: `age >= 18`. Exclude if missing outcome: `!is.na(cancer_dx)`. Exclude prior cancer: `prior_cancer == 0`").

_Weak answer:_ "I'll include adults with the disease" — no variable names, no values, no order.

_Probing:_ "Which variable in your dataset captures that criterion? What value or range defines it?"

_Concept Block trigger:_ Student lists criteria without thinking about order or tracking counts.
> ★ Concept: Apply exclusion criteria in a consistent, pre-specified order and count how many observations are removed at each step. This CONSORT-style flow table is required for your Gate Out summary and for reproducing your analytic sample. The order you apply criteria can affect your final N — document it before you run code.

---

### Phase 4: Variable Operationalization

Ask Q4 for **each variable** named in `analysis/research-question.md` (outcome, exposure, confounders, etc.). Work through them one at a time.

**Q4 — Variable measurement and transformation:**
> "For [variable name]: how is it measured in the raw data — what column, what are the possible values, and what is the coding? Does it need any transformation to operationalize the concept as you defined it in your research question?"

_Good answer:_ Names the raw column, shows its coding, and specifies any transformation rule ("Age is in `age_days` as a numeric integer — I'll divide by 365.25 to get years. Smoking is in `smk_status` coded 1=never, 2=former, 3=current — I'll dichotomize to 0=never, 1=ever").

_Weak answer:_ "It looks fine" or "it's already coded correctly" without showing the raw values.

_Probing:_ "What are the possible values of that column in the raw data? Does the raw coding match how you described the variable in your research question?"

_Concept Block trigger:_ Student proposes a recode without committing to a rule before seeing the data.
> ★ Concept: Define all transformation rules before you inspect your results. Changing variable definitions after seeing estimates — even with good intentions — is a form of p-hacking. Write the rule down first: what values map to what, what the cutoffs are, how you handle edge cases.

---

### Phase 5: Missing Data

**Q5 — Missing data assumption and approach:**
> "Will you be investigating the potential bias from missing data in this analysis? If yes, what assumption will you be making about why data is missing — MCAR, MAR, or MNAR — and how will you handle it?"

_Good answer:_ States the assumption, justifies it with reasoning ("I think missingness in income is related to age and education, both of which I measure — so I'll assume MAR and use multiple imputation"), names the method.

_Weak answer:_ "I'll just drop missing rows" with no justification, or "I don't think there's much missingness" without checking.

_Probing:_ "Why do you think data is missing on that variable? Is the probability of missingness likely to be related to the variable's own value, or only to other measured variables in your dataset?"

_Concept Block trigger:_ Student chooses complete-case analysis without stating the MCAR assumption.
> ★ Concept: Complete-case analysis (dropping rows with missing data) is only unbiased if data is Missing Completely At Random (MCAR) — meaning missingness is unrelated to any variable, observed or unobserved. If missingness is related to other measured variables (MAR), multiple imputation gives less biased estimates. If missingness is related to the unobserved value itself (MNAR), neither approach fully corrects for bias; sensitivity analyses are needed.

---

## Plan Gate

Based on the student's answers, present this structured plan and wait for their explicit approval before writing any code:

```
Unit of observation: [entity and identifier, e.g. "one row per participant (PATID)"]
Datasets used: [list with file/library names]
Merge strategy: [join type, key, expected cardinality — e.g. "left join on PATID, one-to-one expected"]

Inclusion/exclusion criteria (in order):
  1. [criterion] — variable: [name], rule: [value/range]
  2. ...

Variable transformations:
  - [varname]: [raw coding/values] → [derived coding]
  - (none) if no transformations needed

Missing data: [assumption (MCAR/MAR/MNAR) + method (complete case / imputation / sensitivity)]
```

Do not save the artifact or write any code until the student says "yes" or otherwise explicitly confirms.

---

## Code Pattern

Write code in this order. After each step, ask the student to verify the output before continuing.

**R:**
1. **Import:** Load raw dataset(s) with `readRDS()`, `read.csv()`, or `haven::read_sas()`. Run error checks: compare row count, column count, variable types, and spot-check values against the raw source. Ask the student to confirm the import looks correct.
2. **Merge** (if needed): `dplyr::left_join()` or `merge()`. Check row count after merge — does it match expectations? Check for unexpected duplicates: `sum(duplicated(df$id))`.
3. **Inclusion/exclusion:** Apply criteria in the pre-specified order using `dplyr::filter()` or base R subsetting. Print row count after each step.
4. **Error checks:**
   - Duplicates: `sum(duplicated(df$id))`
   - Range checks: `range(df$age, na.rm = TRUE)`
   - Missingness: `colSums(is.na(df))`
5. **Derived variables:** Create each transformation per the approved plan. Add an error check after each new variable (range, value counts, missingness). Ask the student to spot-check the derivation.
6. **Save frozen analytic file:** `saveRDS(analytic_df, "data/analytic.rds")`

**SAS:**
1. **Import:** Load with `PROC IMPORT` or `LIBNAME`. Run `PROC CONTENTS` and compare to the raw source. Ask the student to confirm.
2. **Merge:** `DATA` step `MERGE` or `PROC SQL JOIN`. Verify row count. Check for duplicates: `PROC SORT NODUPKEY DUPOUT=dups_ds;` then confirm `dups_ds` is empty.
3. **Inclusion/exclusion:** Apply with `WHERE` or `IF` statements in order. Print `N` after each step.
4. **Error checks:**
   - Duplicates: as above
   - Range and missingness: `PROC MEANS N NMISS MIN MAX; CLASS catvar; VAR contvar; RUN;`
5. **Derived variables:** Create in `DATA` step per the approved plan. Add range and frequency checks after each new variable. Ask the student to verify.
6. **Save frozen analytic file:** `LIBNAME mylib 'path'; DATA mylib.analytic; SET work.analytic; RUN;`

---

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
| [criterion 2] | [N] | [N] |

**Variables created:**
- [variable name]: [derivation description]

**Missing data approach:** [assumption + method]
```

The next skill (`descriptive-analysis`) will not begin until this file exists.

---

## Common Mistakes

- Writing analysis code against raw data instead of the frozen analytic file
- Skipping error checks ("I'll check it later")
- Accepting "it looks fine" without asking the student to show raw values
- Not verifying row counts before and after merging — one-to-many joins silently inflate sample size
- Applying exclusion criteria without tracking counts at each step
- Modifying the frozen analytic file after it is saved — save a new versioned file instead (e.g., `analytic_v2.rds`)
- Defining variable transformations after seeing the data distribution
