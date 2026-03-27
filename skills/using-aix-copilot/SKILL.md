---
name: using-aix-copilot
description: Use when starting any conversation with a student or when a student asks for help with data analysis, epidemiology, or their assignment — establishes that a workflow skill MUST be invoked before any tutoring response
---

<EXTREMELY-IMPORTANT>
Before responding to any student message, you MUST invoke the appropriate workflow skill using the Skill tool.

This is not optional. This is not negotiable. Even for a clarifying question, invoke the skill first.

If you think there is even a 1% chance a workflow skill applies, YOU MUST invoke it.
</EXTREMELY-IMPORTANT>

## Skill Routing

Check which artifact files exist in the student's `analysis/` directory, then invoke the first matching skill:

| Condition | Invoke this skill |
|---|---|
| No `analysis/` artifacts exist yet | `research-question` |
| `analysis/research-question.md` exists, `analysis/data-preparation.md` does not | `data-preparation` |
| `analysis/data-preparation.md` exists, `analysis/table1-interpretation.md` does not | `descriptive-analysis` |
| `analysis/table1-interpretation.md` exists, `analysis/model-interpretation.md` does not | `statistical-analysis` |
| `analysis/model-interpretation.md` exists | `interpretation` |

If you cannot check the filesystem, default to `research-question`.

After invoking the skill, follow its instructions exactly — do not blend in default assistant behavior.
