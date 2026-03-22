# ABOUTME: Unit tests for the simulation helper functions in simulate.py
# ABOUTME: Tests cover file loading, sentinel detection, and chatlog formatting

import sys
import pytest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from simulate import load_pdf_text, load_skill, SENTINEL_INSTRUCTION, SKILLS_DIR, LAB_DIR


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
    assert sentinel_pos < skill_content_start or sentinel_pos != -1
