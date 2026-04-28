#!/usr/bin/env python3
"""
Reverts two failed visual experiments while keeping the structural fixes:

1. Strips %C2%A0 non-breaking-space padding from shields.io badge URLs.
   The padding was meant to force uniform badge widths across categories
   but did not render visibly in GitHub.

2. Removes <colgroup> column-width constraints from category tables.
   The 290px width was meant to normalize column widths but combined with
   the padding hack made Core badges look small relative to other categories.

Keeps:
- HTML <table> structure (still solves the markdown table column-cropping issue)
- HTML <a><img></a> badge format (required for badges to render inside HTML cells)

Result: each category table renders with auto-sized columns and natural
shields.io badge widths. Slight width variation between categories is
accepted as a tradeoff for visible, clean badges.

Idempotent: re-running on already-reverted README is a no-op.

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
original = text

# ---------------------------------------------------------------------------
# Step 1: Strip %C2%A0 padding from shields.io badge URLs
# ---------------------------------------------------------------------------

# Match shields.io badge URLs and strip leading/trailing %C2%A0 from the label
# Pattern: /badge/<padding><label><padding>-<color>?style=for-the-badge
# The label itself contains [a-z0-9-] characters (including the doubled --).
def strip_padding(match):
    full = match.group(0)
    # Remove all %C2%A0 sequences from the URL
    cleaned = full.replace("%C2%A0", "")
    return cleaned

# Match any shields.io badge URL that has %C2%A0 in it
padding_pattern = re.compile(
    r"https://img\.shields\.io/badge/[^\"\)]*?%C2%A0[^\"\)]*?\?style=for-the-badge"
)
text, padding_count = padding_pattern.subn(strip_padding, text)

# ---------------------------------------------------------------------------
# Step 2: Remove <colgroup>...</colgroup> blocks from category tables
# ---------------------------------------------------------------------------

# Match the colgroup block including surrounding whitespace
colgroup_pattern = re.compile(
    r"\n<colgroup>\n<col style=\"width:\d+px\">\n<col>\n</colgroup>",
    re.MULTILINE,
)
text, colgroup_count = colgroup_pattern.subn("", text)

# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------

if text == original:
    print("No changes needed. README already reverted.")
    sys.exit(0)

README.write_text(text, encoding="utf-8")
print(f"Stripped padding from {padding_count} badge URLs.")
print(f"Removed {colgroup_count} <colgroup> blocks.")
print("Category tables now use auto-sized columns and natural badge widths.")
