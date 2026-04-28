#!/usr/bin/env python3
"""
Converts the four category skill tables (Core, Data Engineering, Writing,
Career) from markdown tables to HTML tables with fixed column widths.

This fixes GitHub's auto-sized rendering, which makes badges in shorter
columns (Core) appear cropped while longer columns (Data Engineering)
display badges at full width.

Idempotent: safe to run multiple times. Detects already-converted tables
and skips them.

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

# Categories to convert, in the order they appear
CATEGORIES = ["Core", "Data Engineering", "Writing", "Career"]

# Column widths: badge column fixed, description column auto-fills
COL_BADGE_WIDTH = "290px"


def parse_markdown_table(table_block):
    """Parse a markdown table block into list of (badge_cell, desc_cell) tuples."""
    rows = []
    lines = table_block.strip().split("\n")
    # Skip header row and separator row
    data_lines = [
        line for line in lines[2:]
        if line.strip().startswith("|") and line.strip().endswith("|")
    ]
    for line in data_lines:
        # Split on | but preserve content; first and last cells are empty
        cells = line.split("|")[1:-1]
        if len(cells) >= 2:
            badge = cells[0].strip()
            desc = "|".join(cells[1:]).strip()  # rejoin in case description had pipes
            rows.append((badge, desc))
    return rows


def build_html_table(rows):
    """Build an HTML table with fixed column widths from parsed rows."""
    parts = []
    parts.append("<table>")
    parts.append("<colgroup>")
    parts.append(f'<col style="width:{COL_BADGE_WIDTH}">')
    parts.append('<col>')
    parts.append("</colgroup>")
    parts.append("<thead>")
    parts.append("<tr><th>Skill</th><th>What it does</th></tr>")
    parts.append("</thead>")
    parts.append("<tbody>")
    for badge, desc in rows:
        parts.append(f"<tr><td>{badge}</td><td>{desc}</td></tr>")
    parts.append("</tbody>")
    parts.append("</table>")
    return "\n".join(parts)


def convert_category(text, category_name):
    """Convert one category's markdown table to HTML in-place."""

    # Idempotency: if the section already has an HTML table, skip
    section_pattern = re.compile(
        rf"^### {re.escape(category_name)}\n.*?(?=^### |\Z)",
        re.MULTILINE | re.DOTALL,
    )
    section_match = section_pattern.search(text)
    if not section_match:
        print(f"  WARNING: section '### {category_name}' not found, skipping",
              file=sys.stderr)
        return text, False

    section = section_match.group(0)

    if "<table>" in section and "<colgroup>" in section:
        print(f"  {category_name}: already converted (HTML table present), skipping")
        return text, False

    # Find the markdown table inside this section
    table_pattern = re.compile(
        r"^\| Skill \| What it does \|\n\|[-\s|]+\|\n((?:\|.*?\|\n)+)",
        re.MULTILINE,
    )
    table_match = table_pattern.search(section)
    if not table_match:
        print(f"  WARNING: no markdown table found in {category_name}, skipping",
              file=sys.stderr)
        return text, False

    full_md_table = "| Skill | What it does |\n" + section[
        table_match.start() + len("| Skill | What it does |\n"):table_match.end()
    ]
    rows = parse_markdown_table(full_md_table)
    if not rows:
        print(f"  WARNING: parsed 0 rows from {category_name}, skipping",
              file=sys.stderr)
        return text, False

    html_table = build_html_table(rows)

    # Replace the markdown table with the HTML table in the full text
    new_section = section[:table_match.start()] + html_table + "\n" + section[
        table_match.end():
    ]
    new_text = text.replace(section, new_section, 1)
    print(f"  {category_name}: converted {len(rows)} rows to HTML table")
    return new_text, True


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

print("Converting category tables to fixed-width HTML...")
changes = 0
for category in CATEGORIES:
    text, changed = convert_category(text, category)
    if changed:
        changes += 1

if changes == 0:
    print("\nNo changes needed. README.md already has all category tables in HTML.")
    sys.exit(0)

README.write_text(text, encoding="utf-8")
print(f"\nUpdated README.md ({changes}/{len(CATEGORIES)} categories converted).")
