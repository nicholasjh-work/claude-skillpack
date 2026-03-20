#!/usr/bin/env python3
"""
tools/check_gotcha_coverage.py
-------------------------------
Verifies that every target skill has gotcha rules defined,
every rule ID referenced in a SKILL.md exists in gotchas.json,
and all 8 target skills have updated Runtime Configuration blocks.

Exit code 0 = all checks pass.
Exit code 1 = one or more checks fail.

Usage:
    python tools/check_gotcha_coverage.py
    python tools/check_gotcha_coverage.py --skills-dir path/to/skills
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
GOTCHAS_JSON = REPO_ROOT / "shared" / "sql-data-gotcha-pack" / "gotchas.json"

TARGET_SKILLS = [
    "sql-report-builder",
    "schema-join-risk-reviewer",
    "data-integrity-investigator",
    "python-data-investigator",
    "python-report-validation",
    "python-reconciliation-engine",
    "kpi-definition-governance",
    "requirements-to-report-spec",
]

RULE_ID_PATTERN = re.compile(r"\bG\d{3}\b")
RUNTIME_CONFIG_PATTERN = re.compile(r"gotcha_pack:\s*\"sql-data-gotcha-pack\"")


def load_registry(path: Path) -> dict[str, dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return {r["id"]: r for r in data}


def check_registry_integrity(registry: dict[str, dict]) -> list[str]:
    errors: list[str] = []
    ids = list(registry.keys())
    seen: set[str] = set()
    for rule_id in ids:
        if rule_id in seen:
            errors.append(f"Duplicate rule ID in registry: {rule_id}")
        seen.add(rule_id)
    return errors


def check_skill_coverage(registry: dict[str, dict]) -> list[str]:
    errors: list[str] = []
    skill_to_rules: dict[str, list[str]] = {s: [] for s in TARGET_SKILLS}

    for rule_id, rule in registry.items():
        for skill in rule["skills"]:
            if skill in skill_to_rules:
                skill_to_rules[skill].append(rule_id)

    for skill, rule_ids in skill_to_rules.items():
        if not rule_ids:
            errors.append(f"COVERAGE: No rules scoped to skill '{skill}'")
            continue
        high_rules = [
            rid for rid in rule_ids if registry[rid]["severity"] == "HIGH"
        ]
        if not high_rules:
            errors.append(f"COVERAGE: No HIGH severity rules for skill '{skill}'")

    return errors


def check_skill_md_references(
    skills_dir: Path,
    registry: dict[str, dict],
) -> list[str]:
    errors: list[str] = []
    valid_ids = set(registry.keys())

    for skill in TARGET_SKILLS:
        skill_md = skills_dir / skill / "SKILL.md"
        if not skill_md.exists():
            errors.append(f"SKILL.md not found: {skill_md}")
            continue

        content = skill_md.read_text(encoding="utf-8")

        # Check runtime config block is present
        if not RUNTIME_CONFIG_PATTERN.search(content):
            errors.append(
                f"RUNTIME_CONFIG: '{skill}' SKILL.md missing gotcha_pack runtime config"
            )

        # Check all rule IDs referenced in the file exist in the registry
        referenced_ids = set(RULE_ID_PATTERN.findall(content))
        for ref_id in referenced_ids:
            if ref_id not in valid_ids:
                errors.append(
                    f"DEAD_REF: '{skill}' SKILL.md references unknown rule ID '{ref_id}'"
                )

        # Check that at least one rule ID scoped to this skill is referenced
        expected_ids = {
            rid for rid, rule in registry.items() if skill in rule["skills"]
        }
        referenced_and_expected = expected_ids & referenced_ids
        if not referenced_and_expected:
            errors.append(
                f"COVERAGE: '{skill}' SKILL.md has no rule IDs from its scope "
                f"(expected any of {sorted(expected_ids)})"
            )

    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check gotcha pack coverage.")
    parser.add_argument(
        "--skills-dir",
        type=Path,
        default=REPO_ROOT / "skills",
        help="Path to the skills/ directory (default: repo_root/skills)",
    )
    args = parser.parse_args(argv)

    if not GOTCHAS_JSON.exists():
        print(f"ERROR: gotchas.json not found at {GOTCHAS_JSON}", file=sys.stderr)
        return 1

    registry = load_registry(GOTCHAS_JSON)
    all_errors: list[str] = []

    all_errors.extend(check_registry_integrity(registry))
    all_errors.extend(check_skill_coverage(registry))
    all_errors.extend(check_skill_md_references(args.skills_dir, registry))

    if all_errors:
        print(f"\nGotcha coverage check FAILED ({len(all_errors)} issues):\n")
        for err in all_errors:
            print(f"  [FAIL] {err}")
        print()
        return 1

    rule_count = len(registry)
    skill_count = len(TARGET_SKILLS)
    print(
        f"Gotcha coverage check PASSED: "
        f"{rule_count} rules across {skill_count} skills, all references valid."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
