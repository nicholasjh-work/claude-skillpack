"""
SPDX-License-Identifier: MIT
Copyright (c) 2026 Nick Hidalgo

Tests for the token-control skill.

Verifies the SKILL.md file conforms to repo standards (ASCII, frontmatter
position, line count) and contains the structural elements documented in
the skill (trigger phrases, output sections, platform blocks, and the
companion-skill relationship to claude-session-handoff).
"""

from pathlib import Path

import pytest

SKILL_PATH = Path(__file__).resolve().parents[1] / "core" / "token-control" / "SKILL.md"


@pytest.fixture(scope="module")
def skill_text() -> str:
    return SKILL_PATH.read_text(encoding="utf-8")


def test_skill_file_exists():
    assert SKILL_PATH.exists(), f"SKILL.md missing at {SKILL_PATH}"


def test_skill_starts_with_frontmatter_delimiter(skill_text: str):
    # Repo linter requires file to start with ---
    assert skill_text.startswith("---\n"), "SKILL.md must start with frontmatter delimiter"


def test_skill_is_ascii_only(skill_text: str):
    # Repo standard: no em dashes, curly quotes, or Unicode arrows
    non_ascii = [(i, ch) for i, ch in enumerate(skill_text) if ord(ch) > 127]
    assert not non_ascii, f"Non-ASCII characters found: {non_ascii[:5]}"


def test_skill_under_500_lines(skill_text: str):
    line_count = skill_text.count("\n")
    assert line_count < 500, f"SKILL.md has {line_count} lines, must be under 500"


def test_skill_has_required_frontmatter(skill_text: str):
    assert "\nname: token-control\n" in skill_text
    assert '\nversion: "1.0.0"\n' in skill_text
    assert "\ndescription: \"" in skill_text


def test_skill_has_mit_license_header(skill_text: str):
    assert "SPDX-License-Identifier: MIT" in skill_text
    assert "Copyright (c) 2026 Nick Hidalgo" in skill_text


def test_skill_documents_manual_trigger(skill_text: str):
    # Token-control's manual surface is intentionally narrow: only /chat-continuation.
    # Other handoff phrases route to claude-session-handoff.
    assert "/chat-continuation" in skill_text


def test_skill_defers_natural_language_to_session_handoff(skill_text: str):
    # The differentiation rule must be documented
    assert "claude-session-handoff" in skill_text
    assert "Manual intent wins" in skill_text or "defer to claude-session-handoff" in skill_text.lower()


def test_skill_documents_threshold_tiers(skill_text: str):
    assert "15" in skill_text and "soft" in skill_text.lower()
    assert "20" in skill_text and "strong" in skill_text.lower()
    assert "25" in skill_text and "forced" in skill_text.lower()


def test_skill_covers_all_three_platforms(skill_text: str):
    assert "Claude web" in skill_text
    assert "Claude Cowork" in skill_text
    assert "Claude Code" in skill_text


def test_skill_includes_required_output_sections(skill_text: str):
    required_sections = [
        "Current Goal",
        "Decisions Already Made",
        "Files / Repos / Paths Involved",
        "Commands Already Run",
        "Current State",
        "Known Issues",
        "Next Best Action",
        "Constraints / User Preferences",
        "Last Completed Task",
        "Next Task",
        "Exact Prompt to Paste Into New Chat",
    ]
    missing = [s for s in required_sections if s not in skill_text]
    assert not missing, f"Missing output sections: {missing}"


def test_skill_is_output_only_no_side_effects(skill_text: str):
    assert "Do not create files" in skill_text
    assert "Do not run commands" in skill_text
    assert "modify the repo" in skill_text
