<!-- ABOUTME: Project overview and progress log for the aix-data-analysis Claude Code plugin -->
<!-- ABOUTME: Documents the 5 skills, usage instructions, and change history -->
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

- 2026-03-22: Plugin skeleton created (package.json and README.md)
- 2026-03-22: All 5 skill files verified (research-question, data-preparation, descriptive-analysis, statistical-analysis, interpretation)
