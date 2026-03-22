# aix-data-analysis

A comprehensive workflow for coding agents to guide students through epidemiological data analysis.

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
- 2026-03-22: Implemented load_pdf_text and load_skill in simulation/simulate.py; all 5 load tests pass
- 2026-03-22: Implemented detect_sentinel, strip_sentinel, and build_transition_note in simulation/simulate.py; all 12 tests pass
- 2026-03-22: Implemented format_skill_section and format_chatlog in simulation/simulate.py; all 18 tests pass
- 2026-03-22: Implemented run_extension_simulation, run_control_simulation, and run_critic in simulation/simulate.py; all 18 tests pass
