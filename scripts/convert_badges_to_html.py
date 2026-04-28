#!/usr/bin/env python3
"""
Converts markdown badge links inside HTML table cells to pure HTML.

GitHub does not reliably parse markdown image+link syntax `[![alt](url)](path)`
when it's inside an HTML <td> cell. The markdown renders as visible raw text
instead of a clickable badge image.

This script converts every such cell to use raw HTML <a><img></a> instead,
which renders correctly inside HTML tables.

Idempotent: safe to run multiple times. Detects already-converted cells and
skips them.

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

# Pattern: markdown image+link inside a <td> cell
# Matches: <td>[![alt-text](image-url)](link-path)</td>
# Captures: alt-text, image-url, link-path
pattern = re.compile(
    r"<td>\[!\[([^\]]+)\]\(([^)]+)\)\]\(([^)]+)\)</td>",
    re.MULTILINE,
)

def replace_cell(match):
    alt = match.group(1)
    img_url = match.group(2)
    link_path = match.group(3)
    return f'<td><a href="{link_path}"><img src="{img_url}" alt="{alt}"></a></td>'

new_text, count = pattern.subn(replace_cell, text)

if count == 0:
    print("No markdown badge cells found. Either already converted or no tables present.")
    sys.exit(0)

README.write_text(new_text, encoding="utf-8")
print(f"Converted {count} markdown badge cells to HTML.")
