# ABOUTME: Unit tests for the simulation helper functions in simulate.py
# ABOUTME: Tests cover file loading, sentinel detection, and chatlog formatting

import sys
import pytest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from simulate import load_pdf_text, load_skill, SENTINEL_INSTRUCTION, SKILLS_DIR, LAB_DIR, detect_sentinel, strip_sentinel, build_transition_note
from simulate import format_skill_section, format_chatlog


def test_load_pdf_text_returns_string():
    text = load_pdf_text(LAB_DIR / "SAS_Lab11 2025.docx.pdf")
    assert isinstance(text, str)
    assert len(text) > 100


def test_load_pdf_text_contains_lab_content():
    text = load_pdf_text(LAB_DIR / "SAS_Lab11 2025.docx.pdf")
    # Lab 11 is about effect measure modification
    assert "vaccine" in text.lower() or "effect" in text.lower()


def test_load_skill_contains_skill_content():
    content = load_skill("research-question")
    assert len(content) > 100


def test_load_skill_has_sentinel_prefix():
    content = load_skill("research-question")
    assert "SKILL_COMPLETE: research-question" in content


def test_load_skill_sentinel_is_prepended():
    content = load_skill("data-preparation")
    # Sentinel instruction appears before the skill content
    sentinel_pos = content.find("SKILL_COMPLETE: data-preparation")
    skill_content_start = content.find("---")  # SKILL.md files start with frontmatter
    assert sentinel_pos != -1 and sentinel_pos < skill_content_start


def test_detect_sentinel_matches_last_line():
    response = "Here is my analysis.\n\nSKILL_COMPLETE: research-question"
    assert detect_sentinel(response, "research-question") is True


def test_detect_sentinel_fails_when_not_last_line():
    response = "SKILL_COMPLETE: research-question\n\nSome trailing text."
    assert detect_sentinel(response, "research-question") is False


def test_detect_sentinel_fails_wrong_skill():
    response = "Some text.\nSKILL_COMPLETE: data-preparation"
    assert detect_sentinel(response, "research-question") is False


def test_detect_sentinel_fails_no_sentinel():
    response = "Just a normal response with no sentinel."
    assert detect_sentinel(response, "research-question") is False


def test_strip_sentinel_removes_last_line():
    response = "Some analysis.\n\nSKILL_COMPLETE: research-question"
    stripped = strip_sentinel(response)
    assert "SKILL_COMPLETE" not in stripped
    assert "Some analysis." in stripped


def test_strip_sentinel_noop_without_sentinel():
    response = "Just a normal response."
    assert strip_sentinel(response) == response


def test_build_transition_note_contains_both_skills():
    note = build_transition_note("research-question", "data-preparation")
    assert "research-question" in note
    assert "data-preparation" in note


def test_format_skill_section_has_header():
    section = format_skill_section("research-question", [("Hi", "Hello")])
    assert "## Skill 1: Research Question" in section


def test_format_skill_section_has_exchanges():
    section = format_skill_section("research-question", [("student msg", "ext msg")])
    assert "**Student:**" in section
    assert "student msg" in section
    assert "**Extension:**" in section
    assert "ext msg" in section


def test_format_skill_section_skill_number():
    # data-preparation is skill 2
    section = format_skill_section("data-preparation", [("q", "a")])
    assert "## Skill 2:" in section


def test_format_chatlog_has_both_parts():
    sections = ["## Skill 1: Research Question\n\n**Student:** hi\n\n**Extension:** hey"]
    control = [("hello", "world")]
    chatlog = format_chatlog(sections, control, "Great critique.")
    assert "Part 1: Student A" in chatlog
    assert "Part 2: Student B" in chatlog
    assert "Critic" in chatlog


def test_format_chatlog_baseline_uses_assistant_label():
    chatlog = format_chatlog([], [("student q", "assistant a")], "critique")
    assert "**Student:**" in chatlog
    assert "**Assistant:**" in chatlog
    assert "student q" in chatlog
    assert "assistant a" in chatlog


def test_format_chatlog_has_date():
    from datetime import date
    chatlog = format_chatlog([], [], "critique")
    assert str(date.today().year) in chatlog
