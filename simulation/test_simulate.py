# ABOUTME: Unit tests for the simulation helper functions in simulate.py
# ABOUTME: Tests cover file loading, sentinel detection, and chatlog formatting

import sys
import pytest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from simulate import load_pdf_text, load_skill, SENTINEL_INSTRUCTION, SKILLS_DIR, LAB_DIR, detect_sentinel, strip_sentinel, build_transition_note


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
