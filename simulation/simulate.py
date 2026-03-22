# ABOUTME: Orchestrates two student simulations (with/without the extension) on Lab 11
# ABOUTME: and produces a comparative chatlog showing the extension's pedagogical value

import anthropic
import pdfplumber
from datetime import date
from pathlib import Path

LAB_DIR = Path(__file__).parent.parent / "lab exercise"
SKILLS_DIR = Path(__file__).parent.parent / "skills"

SKILLS = [
    "research-question",
    "data-preparation",
    "descriptive-analysis",
    "statistical-analysis",
    "interpretation",
]

SENTINEL_INSTRUCTION = """
ORCHESTRATION NOTE: When you have completed this skill and are ready to save the artifact,
emit exactly the following as the very last line of your response, with no trailing text:
SKILL_COMPLETE: {skill_name}
"""

STUDENT_SYSTEM = """\
You are a tired, overworked grad student in an epidemiology methods course. You know
what effect measure modification is and you've done logistic regression before. You want
to finish this lab assignment as fast as possible. You'll try to shortcut the process
whenever you can — asking the assistant to just write the code, saying you already know
your research question, skipping Socratic questions with short non-answers. You use R
(not SAS). When the assistant holds firm and won't just do it for you, you'll grumble
but eventually answer the minimum required to move forward.

When asked for your dataset schema, use this pre-loaded str() output:

'data.frame':  2847 obs. of  4 variables:
 $ covid_clinicvisit: int  1 0 0 1 0 0 0 1 0 0 ...
 $ vaccine          : int  0 1 0 2 1 0 1 0 2 1 ...
 $ age              : num  34 52 28 71 45 60 38 55 41 29 ...
 $ agecat           : int  1 2 1 3 2 3 1 2 2 1 ...\
"""

BASELINE_SYSTEM = "You are a helpful AI assistant."

MODEL = "claude-sonnet-4-6"
MAX_TURNS_PER_SKILL = 10
MAX_TURNS_CONTROL = 20


def load_pdf_text(path: Path) -> str:
    with pdfplumber.open(path) as pdf:
        return "\n".join(
            page.extract_text() or "" for page in pdf.pages
        )


def load_skill(skill_name: str) -> str:
    skill_path = SKILLS_DIR / skill_name / "SKILL.md"
    skill_content = skill_path.read_text()
    prefix = SENTINEL_INSTRUCTION.format(skill_name=skill_name)
    return prefix + "\n" + skill_content


def detect_sentinel(response: str, skill_name: str) -> bool:
    raise NotImplementedError


def strip_sentinel(response: str) -> str:
    raise NotImplementedError


def build_transition_note(prev_skill: str, next_skill: str) -> str:
    raise NotImplementedError


def format_skill_section(skill_name: str, exchanges: list[tuple[str, str]]) -> str:
    raise NotImplementedError


def format_chatlog(
    skill_sections: list[str],
    control_exchanges: list[tuple[str, str]],
    critique: str,
) -> str:
    raise NotImplementedError


def run_extension_simulation(
    client: anthropic.Anthropic, lab_text: str
) -> tuple[list[str], list[tuple[str, str]]]:
    raise NotImplementedError


def run_control_simulation(
    client: anthropic.Anthropic, lab_text: str
) -> list[tuple[str, str]]:
    raise NotImplementedError


def run_critic(
    client: anthropic.Anthropic,
    part_a_text: str,
    part_b_text: str,
    answer_key: str,
) -> str:
    raise NotImplementedError


def main() -> None:
    raise NotImplementedError


if __name__ == "__main__":
    main()
