#!/usr/bin/env python3
"""
Updates README.md to:
1. Add a Skill of the Week / Month spotlight section above the inventory tables.
2. Add the claude-token-watchdog row to the Core skills table.

Idempotent: safe to run multiple times.

Run from the repo root.
"""

import re
import sys
from pathlib import Path

README = Path("README.md")

if not README.exists():
    print("ERROR: README.md not found. Run from repo root.", file=sys.stderr)
    sys.exit(1)

text = README.read_text(encoding="utf-8")

# ----------------------------------------------------------------------
# Step 1: Add the spotlight section above the Core inventory
# ----------------------------------------------------------------------

SPOTLIGHT_BLOCK = """### Spotlight

<table>
<tr>
<td width="50%" align="center">

**Skill of the Week**

[![claude-token-watchdog](https://img.shields.io/badge/this%20week-claude--token--watchdog-0550ae?style=for-the-badge)](core/claude-token-watchdog/)

Watches conversation length and auto-fires a continuation handoff before you hit the token limit. Companion to `claude-session-handoff`.

</td>
<td width="50%" align="center">

**Skill of the Month**

[![scholar-editor](https://img.shields.io/badge/april%202026-scholar--editor-b35900?style=for-the-badge)](writing/ai-prose-humanizer/)

Detects and removes 38 documented AI writing patterns. Two modes: CLEAN for professional docs, VOICE for creative writing.

</td>
</tr>
</table>

> Updating the spotlight: edit this section in `README.md`. Replace the badge `label-name-color` and the description paragraph. Keep the `for-the-badge` style and category color (Core `0550ae`, Data Engineering `0d6e3f`, Writing `b35900`, Career `6f42c1`).

---

"""

if "### Spotlight" in text:
    print("Spotlight section already exists. Skipping spotlight insert.")
else:
    spotlight_anchor = "### Core\n"
    if spotlight_anchor not in text:
        print("ERROR: '### Core' header not found in README.", file=sys.stderr)
        sys.exit(2)
    text = text.replace(spotlight_anchor, SPOTLIGHT_BLOCK + spotlight_anchor, 1)
    print("Added Spotlight section above Core inventory.")

# ----------------------------------------------------------------------
# Step 2: Add claude-token-watchdog row to the Core table
# ----------------------------------------------------------------------

core_row_marker = "Watches conversation length and fires a continuation handoff"
if core_row_marker in text:
    print("README already contains claude-token-watchdog row. Skipping row insert.")
else:
    new_row = (
        "| [![claude-token-watchdog]"
        "(https://img.shields.io/badge/claude--token--watchdog-0550ae?style=for-the-badge)]"
        "(core/claude-token-watchdog/) "
        "| Watches conversation length and fires a continuation handoff at three thresholds "
        "(15 / 20 / 25 messages). Delegates to claude-session-handoff at the forced threshold "
        "to avoid hitting Claude token or context limits. Manual command: `/watchdog-check`. |"
    )
    anchor_pattern = re.compile(
        r"^\| \[!\[claude-session-handoff\].*?\| .*?\|$",
        re.MULTILINE,
    )
    match = anchor_pattern.search(text)
    if not match:
        print("ERROR: claude-session-handoff row not found in Core table.", file=sys.stderr)
        sys.exit(3)
    anchor_line = match.group(0)
    text = text.replace(anchor_line, anchor_line + "\n" + new_row, 1)
    print("Added claude-token-watchdog row to Core table.")

# ----------------------------------------------------------------------
# Step 3: Strengthen the multi-category framing in the lede
# ----------------------------------------------------------------------

old_lede = "Claude Skillforge is a library of 30 battle-tested Claude Skills built for enterprise analytics, data engineering, professional writing, and career tools. Every skill in this repo has been used in production workflows, not written as a demo."
new_lede = "Claude Skillforge is a multi-category library of production-ready Claude Skills. It is not a writing-skills repo. It spans foundational operating standards, data engineering, professional writing, and career tools - every skill battle-tested in real workflows, not written as a demo."

if old_lede in text:
    text = text.replace(old_lede, new_lede, 1)
    print("Updated lede with stronger multi-category framing.")
elif new_lede in text:
    print("Lede already updated. Skipping.")
else:
    print("WARNING: Original lede not found. Manual review needed.", file=sys.stderr)

# ----------------------------------------------------------------------
# Write back
# ----------------------------------------------------------------------

README.write_text(text, encoding="utf-8")
print("README.md updated successfully.")
