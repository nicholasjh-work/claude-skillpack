#!/usr/bin/env python3
"""
tools/check_pattern_coverage.py

Checks that patterns P1 through P38 are each mentioned at least once
somewhere in the scholar-editor skill tree (skills/scholar-editor/ and
shared/scholar-editor/).

This is a static coverage check over documentation -- it does not run
the live detector.

Usage:
    python tools/check_pattern_coverage.py
    python tools/check_pattern_coverage.py --total 38

Exit codes:
    0 - all patterns covered
    1 - one or more patterns missing
"""

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent

SEARCH_ROOTS = [
    REPO_ROOT / "skills" / "scholar-editor",
    REPO_ROOT / "shared" / "scholar-editor",
    REPO_ROOT / "shared" / "scholar_editor",
    REPO_ROOT / "shared" / "ai-pattern-scrubber",
]

SCAN_EXTENSIONS = {".md", ".py", ".json", ".txt"}

PATTERN_MENTION_RE = re.compile(
    r"""
    (?:
        \bP\s*-?\s*(\d{1,2})\b
        | \bpattern\s+(\d{1,2})\b
        | "rule_id":\s*(\d{1,2})\b
        | \brule_id['":\s]+(\d{1,2})\b
        | "id":\s*(\d{1,2})\b
    )
    """,
    re.VERBOSE | re.IGNORECASE,
)


def find_mentioned_patterns(roots, total):
    mentions = {i: [] for i in range(1, total + 1)}
    for root in roots:
        if not root.exists():
            continue
        for path in sorted(root.rglob("*")):
            if not path.is_file() or path.suffix not in SCAN_EXTENSIONS:
                continue
            try:
                content = path.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue
            for match in PATTERN_MENTION_RE.finditer(content):
                id_str = next(g for g in match.groups() if g is not None)
                pid = int(id_str)
                if 1 <= pid <= total:
                    rel = str(path.relative_to(REPO_ROOT))
                    if rel not in mentions[pid]:
                        mentions[pid].append(rel)
    return mentions


def main():
    parser = argparse.ArgumentParser(
        description="Check that patterns P1-PN are all mentioned in the scholar-editor skill tree."
    )
    parser.add_argument("--total", type=int, default=38,
                        help="Total number of patterns to check (default: 38)")
    args = parser.parse_args()

    total = args.total
    print(f"Checking P1-P{total} coverage across scholar-editor skill tree...\n")

    mentions = find_mentioned_patterns(SEARCH_ROOTS, total)
    covered = sorted(pid for pid, files in mentions.items() if files)
    missing = sorted(pid for pid, files in mentions.items() if not files)

    print(f"{'='*60}")
    print(f"Pattern Coverage Report")
    print(f"{'='*60}")
    print(f"Total patterns:   P1-P{total} ({total})")
    print(f"Covered:          {len(covered)} -- {covered}")
    if missing:
        print(f"Missing:          {len(missing)} -- {missing}")
    print(f"Coverage:         {len(covered)}/{total} ({len(covered)/total:.0%})")
    print(f"{'='*60}")

    if not missing:
        print(f"PASS -- all {total} patterns covered.")
        sys.exit(0)
    else:
        print(f"\nFAIL -- {len(missing)} pattern(s) not found: {missing}", file=sys.stderr)
        print(f"Add P{missing[0]}-P{missing[-1]} to skills/scholar-editor/ or shared/scholar-editor/",
              file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
