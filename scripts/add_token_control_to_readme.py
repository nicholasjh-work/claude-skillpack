#!/usr/bin/env python3
"""
Adds token-control to the Core skills table in README.md.

Idempotent: safe to run multiple times. If the row already exists, exits 0
without modifying the file.
"""

import sys
from pathlib import Path

README = Path(__file__).resolve().parents[1] / "README.md" if "__file__" in dir() else Path("README.md")

# Allow running from repo root
if not README.exists():
    README = Path("README.md")

if not README.exists():
    print("ERROR: README.md not found. Run from repo root.", file=sys.stderr)
    sys.exit(1)

text = README.read_text(encoding="utf-8")

# Idempotency check
if "/core/token-control" in text:
    print("README already contains token-control row. No change.")
    sys.exit(0)

# The row to insert
NEW_ROW = "| [token-control](https://github.com/nicholasjh-work/claude-skillforge/blob/main/core/token-control) | Automatic, threshold-based companion to claude-session-handoff. Generates a Chat Continuation Brief when a conversation is approaching a context or usage limit. Triggers on `/chat-continuation` or automatically at 15/20/25 message thresholds. |"

# Insert immediately after the claude-session-handoff row in the Core table
ANCHOR = "| [claude-session-handoff](https://github.com/nicholasjh-work/claude-skillforge/blob/main/core/claude-session-handoff) | Generates a structured handoff block that captures full technical state so a conversation can continue in a new window with zero re-explanation. |"

if ANCHOR not in text:
    print("ERROR: anchor row (claude-session-handoff) not found in README.", file=sys.stderr)
    print("README structure may have changed. Aborting to avoid corrupt insert.", file=sys.stderr)
    sys.exit(2)

new_text = text.replace(ANCHOR, ANCHOR + "\n" + NEW_ROW, 1)

README.write_text(new_text, encoding="utf-8")
print(f"Added token-control row to {README}")
