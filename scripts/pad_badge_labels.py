#!/usr/bin/env python3
"""
Pads shields.io badge labels with leading and trailing non-breaking spaces
so every badge across all four categories renders at the same physical width.

Why: shields.io's `for-the-badge` style sizes badges to fit the label text.
Different label lengths produce different badge widths. Even labels of the
same character count can differ slightly because letterspacing varies by
character. This script pads every label to a fixed character target so
all badges render at consistent width.

How: shields.io URL-encodes label text. Replacing the existing badge
label-name segment with a padded version (using %C2%A0 for non-breaking
spaces) forces the SVG renderer to pad the badge to a uniform width.

The padding target is the longest skill name in the repo (32 chars,
technical-to-business-summarizer). Every shorter label gets padded to
match.

Idempotent: re-running on already-padded labels is a no-op.

Run from repo root.
"""

import re
import sys
from pathlib import Path

README = Path("README.md")

if not README.exists():
    print("ERROR: README.md not found. Run from repo root.", file=sys.stderr)
    sys.exit(1)

text = README.read_text(encoding="utf-8")

# Target label width: longest skill name across all categories
TARGET_WIDTH = 32

# Non-breaking space URL-encoded (does not collapse in SVG)
NBSP = "%C2%A0"

# Pattern: shields.io badge URL with a skill-name label
# Matches: https://img.shields.io/badge/<skill-name-with-double-dashes>-<color>?style=for-the-badge
# The label segment is everything between /badge/ and the last `-<color>?` segment.
#
# In shields.io, double dashes `--` in the URL render as a single dash `-`.
# A 24-char skill name like "claude-operator-standard" appears in the URL as
# "claude--operator--standard" (each hyphen doubled). So when we count
# characters, we count the displayed label, not the URL-encoded form.
PATTERN = re.compile(
    r"https://img\.shields\.io/badge/([a-z0-9\-]+)-([0-9a-f]{6})\?style=for-the-badge"
)


def url_label_to_display(url_label: str) -> str:
    """Convert shields.io URL label to displayed text.

    In shields.io URLs, `--` represents a literal `-` in the displayed badge.
    """
    return url_label.replace("--", "-")


def already_padded(url_label: str) -> bool:
    """Check if a label already has non-breaking-space padding."""
    return "%C2%A0" in url_label or url_label.startswith("%20") or url_label.endswith("%20")


def pad_label(url_label: str) -> str:
    """Pad a URL-encoded label to TARGET_WIDTH displayed characters."""
    if already_padded(url_label):
        return url_label

    display = url_label_to_display(url_label)
    current = len(display)

    if current >= TARGET_WIDTH:
        return url_label

    pad_total = TARGET_WIDTH - current
    pad_left = pad_total // 2
    pad_right = pad_total - pad_left

    # Build padded label: NBSP * pad_left + original URL-encoded label + NBSP * pad_right
    return (NBSP * pad_left) + url_label + (NBSP * pad_right)


def replace_badge(match):
    full_match = match.group(0)
    url_label = match.group(1)
    color = match.group(2)

    new_label = pad_label(url_label)
    if new_label == url_label:
        return full_match  # already padded or already at target

    new_url = f"https://img.shields.io/badge/{new_label}-{color}?style=for-the-badge"
    return new_url


# Skip Spotlight section badges (intentionally have prefix labels like "this week-")
# and skip footer badges (LinkedIn, Website, Email — they have different label patterns).
# We only target shields.io badges in the four category tables, identified by:
# label format `<skill-name-doubled-dashes>` (no other prefix/suffix beyond the color).

# Find badge URLs and replace only those matching the simple skill-name pattern.
# The shields.io URL pattern in our category tables: /badge/<dashes>-<color>?style=for-the-badge
# Spotlight badges have labels like "this%20week-claude--token--watchdog" with a space-separated prefix.
# Those won't match our PATTERN because of the %20 encoding (PATTERN doesn't allow %).

new_text, count = PATTERN.subn(replace_badge, text)

if count == 0:
    print("No badges found to pad. Check README structure.")
    sys.exit(1)

if new_text == text:
    print("All badges already at target width or already padded. No changes.")
    sys.exit(0)

README.write_text(new_text, encoding="utf-8")
print(f"Processed {count} badge URLs.")
print(f"Padded labels to {TARGET_WIDTH} displayed characters with non-breaking spaces.")
