#!/usr/bin/env python3
"""
Adds a Compatibility section to claude-token-watchdog SKILL.md.

Inserts the section between the badge header and the existing
"What this does" section. Idempotent.
"""

import sys
from pathlib import Path

SKILL = Path("core/claude-token-watchdog/SKILL.md")

if not SKILL.exists():
    print("ERROR: SKILL.md not found. Run from repo root.", file=sys.stderr)
    sys.exit(1)

text = SKILL.read_text(encoding="utf-8")

if "### Compatibility" in text:
    print("Compatibility section already exists. No change.")
    sys.exit(0)

COMPATIBILITY_BLOCK = """### Compatibility

This skill is built on the Claude SKILL.md format and works on the three Anthropic surfaces that support it.

| Platform | Supported |
|---|---|
| Claude.ai (web and desktop apps) | Yes |
| Claude Cowork | Yes |
| Claude Code (CLI) | Yes |
| ChatGPT, Gemini, Copilot, or any non-Anthropic LLM | No - SKILL.md is Anthropic-specific |
| LangChain, LiteLLM, or other orchestration frameworks | Not directly - the watchdog logic could be ported as a Python module, but that is a separate implementation |

The skill activates the same way on all three Anthropic surfaces: Claude reads the frontmatter, decides whether to load the full instructions based on the trigger phrases, and applies the threshold logic to the visible conversation. Output is identical across surfaces. Platform-specific behavior (described below) covers minor differences in how the continuation brief is consumed (paste into a new chat for web/Cowork, paste into a new Claude Code session for CLI).

---

"""

# Insert before "### What this does"
anchor = "### What this does"
if anchor not in text:
    print(f"ERROR: anchor '{anchor}' not found in SKILL.md", file=sys.stderr)
    sys.exit(2)

new_text = text.replace(anchor, COMPATIBILITY_BLOCK + anchor, 1)
SKILL.write_text(new_text, encoding="utf-8")
print("Added Compatibility section to claude-token-watchdog/SKILL.md")
