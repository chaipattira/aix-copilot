# aix-data-analysis

A comprehensive workflow for coding agents to guide students through epidemiological data analysis.

## Skills

| Skill | Purpose |
|---|---|
| `research-question` | Define research question, exposure, outcome, and DAG (uses draw-a-dag) |
| `draw-a-dag` | Auxiliary: guide student through building a causal DAG; outputs mermaid diagram |
| `data-preparation` | Load, merge, clean, and freeze the analytic dataset |
| `descriptive-analysis` | Produce Table 1 and describe the study population |
| `statistical-analysis` | Run crude and adjusted models (branches by question type) |
| `interpretation` | Visualize results, run sensitivity analyses, scaffold write-up |

## Plugin Structure

```
.claude-plugin/plugin.json   # Claude Code plugin manifest
hooks/
  hooks.json                 # SessionStart hook registration
  session-start.sh           # Injects Socratic Tutoring Style at session start
  socratic-style.md          # Dialogue pacing rules shared by all skills
skills/
  research-question/
  draw-a-dag/
  data-preparation/
  descriptive-analysis/
  statistical-analysis/
  interpretation/
```

## Usage

Students invoke skills in order. Each skill enforces a hard gate: it checks for the prior skill's artifact file before proceeding.

The Socratic Tutoring Style (voice/pacing, Concept Blocks, probing phrases) is injected via the SessionStart hook and applies to all skills automatically.

## Progress Log

- 2026-03-22: Plugin skeleton created (package.json and README.md)
- 2026-03-22: All 5 skill files verified (research-question, data-preparation, descriptive-analysis, statistical-analysis, interpretation)
- 2026-03-22: Implemented load_pdf_text and load_skill in simulation/simulate.py; all 5 load tests pass
- 2026-03-22: Implemented detect_sentinel, strip_sentinel, and build_transition_note in simulation/simulate.py; all 12 tests pass
- 2026-03-22: Implemented format_skill_section and format_chatlog in simulation/simulate.py; all 18 tests pass
- 2026-03-22: Implemented run_extension_simulation, run_control_simulation, and run_critic in simulation/simulate.py; all 18 tests pass
- 2026-03-22: Implemented main entrypoint; end-to-end simulation completed successfully, producing simulation/chatlog-2026-03-22.md (1622 lines, all 5 skills, Student A + B + critic commentary)
- 2026-03-26: Rewrote research-question skill with explicit branching tree, strengthened non-negotiable rules, and updated artifact template to include mermaid DAG section; created draw-a-dag auxiliary skill with 6-step Socratic DAG-building process; added AUXILIARY_SKILLS to simulate.py so draw-a-dag is concatenated into research-question system prompt; all 20 tests pass
- 2026-03-26: Added Socratic Tutoring Style (voice/pacing, Concept Blocks, probing phrases) to claude.md as plugin-wide default; enriched research-question skill with per-question answer guidance, probing patterns, and ★ Concept Block triggers for all 7 questions
- 2026-03-26: Enriched data-preparation, descriptive-analysis, and statistical-analysis skills with phased Socratic dialogue (good/weak/probing/Concept Blocks per question, structured Plan Gate templates); fixed glm() link argument bug in statistical-analysis code pattern
- 2026-03-26: Packaged as Claude plugin — added .claude-plugin/plugin.json and SessionStart hook that injects Socratic Tutoring Style into every session; style moved from claude.md to hooks/socratic-style.md
