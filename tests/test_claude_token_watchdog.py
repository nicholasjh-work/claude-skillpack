"""
SPDX-License-Identifier: MIT
Copyright (c) 2026 Nick Hidalgo

Tests for the claude-token-watchdog skill.

Verifies the SKILL.md file conforms to repo standards (ASCII, frontmatter
position, line count) and contains the structural elements documented in
the skill (threshold tiers, delegation to claude-session-handoff, platform
behavior, output-only contract).
"""

from pathlib import Path

import pytest

SKILL_PATH = (
    Path(__file__).resolve().parents[1]
    / "core"
    / "claude-token-watchdog"
    / "SKILL.md"
)


@pytest.fixture(scope="module")
def skill_text() -> str:
    return SKILL_PATH.read_text(encoding="utf-8")


def test_skill_file_exists():
    assert SKILL_PATH.exists(), f"SKILL.md missing at {SKILL_PATH}"


def test_skill_starts_with_frontmatter_delimiter(skill_text: str):
    assert skill_text.startswith("---\n"), "SKILL.md must start with frontmatter delimiter"


def test_skill_is_ascii_only(skill_text: str):
    non_ascii = [(i, ch) for i, ch in enumerate(skill_text) if ord(ch) > 127]
    assert not non_ascii, f"Non-ASCII characters found: {non_ascii[:5]}"


def test_skill_under_500_lines(skill_text: str):
    line_count = skill_text.count("\n")
    assert line_count < 500, f"SKILL.md has {line_count} lines, must be under 500"


def test_skill_has_required_frontmatter(skill_text: str):
    assert "\nname: claude-token-watchdog\n" in skill_text
    assert '\nversion: "1.0.0"\n' in skill_text
    assert "\ndescription: \"" in skill_text


def test_skill_has_mit_license_header(skill_text: str):
    assert "SPDX-License-Identifier: MIT" in skill_text
    assert "Copyright (c) 2026 Nick Hidalgo" in skill_text


def test_skill_documents_manual_trigger(skill_text: str):
    # Watchdog's only manual trigger is /watchdog-check
    # Other handoff phrases route to claude-session-handoff
    assert "/watchdog-check" in skill_text


def test_skill_delegates_to_session_handoff(skill_text: str):
    # The delegation contract must be explicit
    assert "claude-session-handoff" in skill_text
    assert "delegate" in skill_text.lower() or "delegates" in skill_text.lower()


def test_skill_documents_threshold_tiers(skill_text: str):
    # All three tiers must be documented with their thresholds
    assert "15" in skill_text and "soft" in skill_text.lower()
    assert "20" in skill_text and "strong" in skill_text.lower()
    assert "25" in skill_text and "forced" in skill_text.lower()


def test_skill_documents_dense_mode(skill_text: str):
    # Dense-mode adjustment must be present
    assert "12" in skill_text
    assert "dense" in skill_text.lower()


def test_skill_covers_all_three_platforms(skill_text: str):
    assert "Claude web" in skill_text
    assert "Claude Cowork" in skill_text
    assert "Claude Code" in skill_text


def test_skill_does_not_produce_brief_itself(skill_text: str):
    # The architecture must explicitly say watchdog does NOT produce briefs
    text_lower = skill_text.lower()
    assert "does not produce briefs" in text_lower or "do not produce" in text_lower or "never produce a brief" in text_lower


def test_skill_is_output_only_no_side_effects(skill_text: str):
    assert "Never write files" in skill_text or "no file writes" in skill_text.lower()
    assert "Never run commands" in skill_text or "no commands" in skill_text.lower()
    assert "modify the repo" in skill_text
