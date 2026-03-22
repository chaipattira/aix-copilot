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
    last_line = response.rstrip().split("\n")[-1].strip()
    return last_line == f"SKILL_COMPLETE: {skill_name}"


def strip_sentinel(response: str) -> str:
    lines = response.rstrip().split("\n")
    if lines and lines[-1].strip().startswith("SKILL_COMPLETE:"):
        lines = lines[:-1]
    return "\n".join(lines).rstrip()


def build_transition_note(prev_skill: str, next_skill: str) -> str:
    return (
        f"The {prev_skill} skill has completed. "
        f"The extension has loaded the {next_skill} skill. "
        "Continue as the same tired student — you still want to get this done fast."
    )


_SKILL_DISPLAY_NAMES = {
    "research-question": "Research Question",
    "data-preparation": "Data Preparation",
    "descriptive-analysis": "Descriptive Analysis",
    "statistical-analysis": "Statistical Analysis",
    "interpretation": "Interpretation",
}


def format_skill_section(skill_name: str, exchanges: list[tuple[str, str]]) -> str:
    skill_number = SKILLS.index(skill_name) + 1
    display_name = _SKILL_DISPLAY_NAMES[skill_name]
    lines = [f"## Skill {skill_number}: {display_name}\n"]
    for student_msg, ext_msg in exchanges:
        lines.append(f"**Student:** {student_msg}\n")
        lines.append(f"**Extension:** {ext_msg}\n")
    return "\n".join(lines)


def format_chatlog(
    skill_sections: list[str],
    control_exchanges: list[tuple[str, str]],
    critique: str,
) -> str:
    today = date.today().isoformat()
    parts = [
        f"# AIX Copilot Simulation — Lab 11: Effect Measure Modification",
        f"*Date: {today}*\n",
        "---\n",
        "# Part 1: Student A — With Extension (aix-data-analysis v0.1.0)\n",
    ]
    parts.extend(skill_sections)
    parts.append("\n---\n")
    parts.append("# Part 2: Student B — Baseline LLM (No Extension)\n")
    for student_msg, asst_msg in control_exchanges:
        parts.append(f"**Student:** {student_msg}\n")
        parts.append(f"**Assistant:** {asst_msg}\n")
    parts.append("\n---\n")
    parts.append("# Critic's Comparative Commentary\n")
    parts.append(critique)
    return "\n".join(parts)


def run_extension_simulation(
    client: anthropic.Anthropic, lab_text: str
) -> tuple[list[str], list[tuple[str, str]]]:
    """Returns (skill_sections, all_exchanges).
    skill_sections: formatted markdown strings, one per skill.
    all_exchanges: raw (student, extension) pairs across all skills.
    """
    opening = (
        "Hey, I need to complete Lab 11 for my epi methods class. "
        f"Here's the assignment:\n\n{lab_text}\n\n"
        "I want to use R. Can you help me just get through this?"
    )

    messages: list[dict] = []
    skill_sections: list[str] = []
    all_exchanges: list[tuple[str, str]] = []

    for i, skill_name in enumerate(SKILLS):
        skill_system = load_skill(skill_name)
        exchanges: list[tuple[str, str]] = []

        if i == 0:
            student_msg = opening
        else:
            # Student continues naturally; transition note already injected
            student_msg = client.messages.create(
                model=MODEL,
                max_tokens=512,
                system=STUDENT_SYSTEM,
                messages=messages,
            ).content[0].text

        for turn in range(MAX_TURNS_PER_SKILL):
            # Student turn (turn 0 uses the pre-computed student_msg; subsequent turns generate new ones)
            if turn == 0:
                current_student_msg = student_msg
            else:
                current_student_msg = client.messages.create(
                    model=MODEL,
                    max_tokens=512,
                    system=STUDENT_SYSTEM,
                    messages=messages,
                ).content[0].text

            messages.append({"role": "user", "content": current_student_msg})

            # Extension turn
            ext_response = client.messages.create(
                model=MODEL,
                max_tokens=1024,
                system=skill_system,
                messages=messages,
            ).content[0].text

            sentinel_found = detect_sentinel(ext_response, skill_name)
            clean_response = strip_sentinel(ext_response)

            if not sentinel_found and turn == MAX_TURNS_PER_SKILL - 1:
                clean_response += "\n\n*[SKILL TIMEOUT — forced advance]*"

            messages.append({"role": "assistant", "content": clean_response})
            exchanges.append((current_student_msg, clean_response))
            all_exchanges.append((current_student_msg, clean_response))

            if sentinel_found:
                break

        skill_sections.append(format_skill_section(skill_name, exchanges))

        # Inject transition note before next skill
        if i < len(SKILLS) - 1:
            note = build_transition_note(skill_name, SKILLS[i + 1])
            messages.append({"role": "assistant", "content": note})

    return skill_sections, all_exchanges


def run_control_simulation(
    client: anthropic.Anthropic, lab_text: str
) -> list[tuple[str, str]]:
    opening = (
        "Hey, I need to complete Lab 11 for my epi methods class. "
        f"Here's the assignment:\n\n{lab_text}\n\n"
        "I want to use R. Can you help me just get through this?"
    )

    messages: list[dict] = [{"role": "user", "content": opening}]
    exchanges: list[tuple[str, str]] = []

    # First assistant response
    asst_response = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        system=BASELINE_SYSTEM,
        messages=messages,
    ).content[0].text
    messages.append({"role": "assistant", "content": asst_response})
    exchanges.append((opening, asst_response))

    for _ in range(MAX_TURNS_CONTROL - 1):
        student_msg = client.messages.create(
            model=MODEL,
            max_tokens=512,
            system=STUDENT_SYSTEM,
            messages=messages,
        ).content[0].text
        messages.append({"role": "user", "content": student_msg})

        asst_response = client.messages.create(
            model=MODEL,
            max_tokens=1024,
            system=BASELINE_SYSTEM,
            messages=messages,
        ).content[0].text
        messages.append({"role": "assistant", "content": asst_response})
        exchanges.append((student_msg, asst_response))

    return exchanges


def run_critic(
    client: anthropic.Anthropic,
    part_a_text: str,
    part_b_text: str,
    answer_key: str,
) -> str:
    system = (
        "You are a pedagogical observer comparing two epidemiology students doing the same lab:\n"
        "- Student A used the aix-data-analysis extension (structured, gate-kept, Socratic)\n"
        "- Student B used a baseline AI assistant with no structure\n\n"
        "Your critique should cover:\n"
        "1. Each moment either student tried to shortcut the process (quote the conversation)\n"
        "2. How each assistant responded — did the extension hold its guardrails? Did the baseline just comply?\n"
        "3. Whether Student A's work shows deeper scientific reasoning than Student B's\n"
        "4. Whether the overall pedagogical goals (thinking before coding, Socratic dialogue, plan approval before code) were achieved by the extension\n"
        "5. Quality of the final interpretations for both students, compared against the answer key\n\n"
        "## Answer Key\n\n"
        "```sas\n"
        f"{answer_key}\n"
        "```"
    )

    user_content = (
        "## Student A (Extension)\n\n"
        f"{part_a_text}\n\n"
        "## Student B (Baseline)\n\n"
        f"{part_b_text}"
    )

    response = client.messages.create(
        model=MODEL,
        max_tokens=2048,
        system=system,
        messages=[{"role": "user", "content": user_content}],
    )
    return response.content[0].text


def main() -> None:
    raise NotImplementedError


if __name__ == "__main__":
    main()
