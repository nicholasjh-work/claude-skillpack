#!/usr/bin/env python3
"""
tools/skill_linter.py

Validates SKILL.md files for publication readiness.

Usage:
    python tools/skill_linter.py skills/email-writer/SKILL.md
    python tools/skill_linter.py skills/
    python tools/skill_linter.py skills/ --json
    python tools/skill_linter.py skills/ --fix   # auto-fix em dashes and curly quotes
    python tools/skill_linter.py skills/ --strict # fail on warnings too

Exit codes:
    0 - all files pass
    1 - one or more files fail
"""

import argparse
import json
import re
import sys
from pathlib import Path

import yaml

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

ALLOWED_FRONTMATTER_KEYS = {
    "name",
    "description",
    "allowed-tools",
    "compatibility",
    "license",
    "metadata",
    "version",
}

# Non-ASCII characters that are banned in skill body prose
NON_ASCII_CHARS = {
    "\u2014": "em dash (U+2014)",
    "\u2013": "en dash (U+2013)",
    "\u2018": "left single curly quote (U+2018)",
    "\u2019": "right single curly quote (U+2019)",
    "\u201c": "left double curly quote (U+201C)",
    "\u201d": "right double curly quote (U+201D)",
    "\u2192": "right arrow (U+2192)",
    "\u2190": "left arrow (U+2190)",
    "\u2026": "ellipsis (U+2026)",
}

NON_ASCII_FIX_MAP = {
    "\u2014": "-",
    "\u2013": "-",
    "\u2018": "'",
    "\u2019": "'",
    "\u201c": '"',
    "\u201d": '"',
    "\u2192": "->",
    "\u2190": "<-",
    "\u2026": "...",
}

MAX_BODY_LINES = 500


# ---------------------------------------------------------------------------
# Result types
# ---------------------------------------------------------------------------

class Violation:
    def __init__(self, level: str, code: str, message: str, line: int = 0):
        self.level = level  # "error" | "warning"
        self.code = code
        self.message = message
        self.line = line

    def __str__(self):
        loc = f"  line {self.line}: " if self.line else "  "
        return f"  [{self.level.upper()}] {self.code}: {loc}{self.message}"

    def to_dict(self):
        return {
            "level": self.level,
            "code": self.code,
            "line": self.line,
            "message": self.message,
        }


def err(code, message, line=0):
    return Violation("error", code, message, line)

def warn(code, message, line=0):
    return Violation("warning", code, message, line)


# ---------------------------------------------------------------------------
# Core lint logic
# ---------------------------------------------------------------------------

def strip_code_blocks(text: str) -> str:
    """Remove fenced code blocks and inline code from text."""
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    text = re.sub(r"`[^`\n]*`", "", text)
    return text


def parse_frontmatter(content: str):
    """
    Parse YAML frontmatter between leading --- delimiters.
    Returns (fm_dict, body_str) or raises ValueError.
    """
    if not content.startswith("---"):
        raise ValueError("File does not start with --- frontmatter delimiter")
    parts = content.split("---", 2)
    if len(parts) < 3:
        raise ValueError("Could not find closing --- for frontmatter")
    fm_raw = parts[1]
    body = parts[2]
    fm = yaml.safe_load(fm_raw)
    if not isinstance(fm, dict):
        raise ValueError("Frontmatter did not parse as a YAML mapping")
    return fm, body


def check_version_in_body(body: str) -> bool:
    """Check for version in a Runtime Configuration code block in the body."""
    # Match ```yaml or ``` blocks containing version: ...
    blocks = re.findall(r"```[^\n]*\n(.*?)```", body, re.DOTALL)
    for block in blocks:
        if re.search(r"^\s*version\s*:", block, re.MULTILINE):
            return True
    # Also accept bare `version: X.Y.Z` anywhere in body (not in frontmatter)
    if re.search(r"^\s*version\s*:\s*\S", body, re.MULTILINE):
        return True
    return False


def lint_file(path: Path, fix: bool = False) -> tuple[list[Violation], bool]:
    """
    Lint a single SKILL.md file.
    Returns (violations, was_fixed).
    """
    violations = []
    was_fixed = False

    try:
        content = path.read_text(encoding="utf-8")
    except Exception as e:
        return [err("READ_ERROR", str(e))], False

    # --- 1. Frontmatter parse ------------------------------------------------
    try:
        fm, body = parse_frontmatter(content)
    except ValueError as e:
        return [err("FRONTMATTER_PARSE", str(e))], False

    # --- 2. Required keys ----------------------------------------------------
    for key in ("name", "description"):
        if key not in fm:
            violations.append(err("MISSING_REQUIRED_KEY", f"'{key}' is required in frontmatter"))

    # --- 3. description must be a single-line quoted string ------------------
    desc = fm.get("description", "")
    if desc:
        desc_str = str(desc)
        if "\n" in desc_str:
            violations.append(
                err("MULTILINE_DESCRIPTION",
                    "description must be a single-line string, not a multi-line block (> or |)")
            )

    # --- 4. Disallowed frontmatter keys (warn, not error) --------------------
    # scholar-editor and other skills use extended frontmatter keys for their
    # own runtime config; we warn but do not fail on unknown keys
    extra_keys = set(fm.keys()) - ALLOWED_FRONTMATTER_KEYS
    if extra_keys:
        violations.append(
            warn("EXTRA_FRONTMATTER_KEYS",
                 f"Non-standard frontmatter keys (consider moving to Runtime Configuration block): "
                 f"{sorted(extra_keys)}")
        )

    # --- 5. Version presence -------------------------------------------------
    has_version_fm = "version" in fm
    has_version_body = check_version_in_body(body)
    if not has_version_fm and not has_version_body:
        violations.append(
            err("MISSING_VERSION",
                "No 'version' field in frontmatter and no version in Runtime Configuration block")
        )

    # --- 6. Body line count --------------------------------------------------
    body_lines = body.splitlines()
    total_lines = len(content.splitlines())
    if total_lines > MAX_BODY_LINES:
        violations.append(
            err("FILE_TOO_LONG",
                f"File is {total_lines} lines; maximum is {MAX_BODY_LINES}")
        )

    # --- 7. Non-ASCII characters in prose ------------------------------------
    # Strip code blocks before checking so examples inside ``` are exempt
    prose = strip_code_blocks(body)

    fixed_content = content
    for char, label in NON_ASCII_CHARS.items():
        if char in prose:
            count = prose.count(char)
            if fix:
                replacement = NON_ASCII_FIX_MAP[char]
                fixed_content = fixed_content.replace(char, replacement)
                violations.append(
                    warn("NON_ASCII_FIXED",
                         f"Auto-fixed {count}x {label} -> '{replacement}'")
                )
                was_fixed = True
            else:
                violations.append(
                    err("NON_ASCII",
                        f"Found {count}x {label} in prose (outside code blocks)")
                )

    if fix and was_fixed:
        path.write_text(fixed_content, encoding="utf-8")

    # --- 8. Dangling file references -----------------------------------------
    # Find paths in backticks like `path/to/file.ext` that look like file refs
    skill_dir = path.parent
    backtick_refs = re.findall(r"`([^`\n]+\.[a-zA-Z0-9]{1,6})`", body)
    for ref in backtick_refs:
        # Skip if it looks like code (contains spaces, parens, brackets, operators)
        if any(c in ref for c in " ()[]{}=><|&"):
            continue
        # Skip URLs, module paths (dots not slashes), template variables
        if ref.startswith("http") or "{" in ref or ref.startswith("."):
            continue
        # Only check paths that contain a slash (actual file paths)
        if "/" not in ref and "\\" not in ref:
            continue
        candidate = skill_dir / ref
        if not candidate.exists():
            violations.append(
                warn("DANGLING_REFERENCE",
                     f"Referenced path does not exist relative to skill dir: {ref}")
            )

    return violations, was_fixed


# ---------------------------------------------------------------------------
# Directory walk
# ---------------------------------------------------------------------------

def collect_skill_files(target: Path) -> list[Path]:
    if target.is_file():
        return [target]
    paths = []
    for p in sorted(target.rglob("SKILL.md")):
        paths.append(p)
    return paths


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

def print_result(path: Path, violations: list[Violation], fixed: bool, strict: bool) -> bool:
    """Print result for one file. Returns True if the file passes."""
    errors = [v for v in violations if v.level == "error"]
    warnings = [v for v in violations if v.level == "warning"]
    fails = errors + (warnings if strict else [])

    status = "PASS" if not fails else "FAIL"
    label = f"  {status}  {path}"
    if fixed:
        label += "  [auto-fixed]"
    print(label)
    for v in violations:
        print(str(v))
    return status == "PASS"


def output_json(results: list[dict]):
    print(json.dumps(results, indent=2))


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Lint SKILL.md files for publication readiness."
    )
    parser.add_argument(
        "target",
        help="Path to a SKILL.md file or a directory to scan recursively",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output machine-readable JSON instead of human text",
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Auto-fix em dashes and curly quotes in-place",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat warnings as failures (exit 1)",
    )
    args = parser.parse_args()

    target = Path(args.target)
    if not target.exists():
        print(f"ERROR: path not found: {target}", file=sys.stderr)
        sys.exit(1)

    skill_files = collect_skill_files(target)
    if not skill_files:
        print(f"ERROR: no SKILL.md files found under {target}", file=sys.stderr)
        sys.exit(1)

    if not args.json:
        print(f"Linting {len(skill_files)} SKILL.md file(s)...\n")

    all_results = []
    pass_count = 0
    fail_count = 0

    for path in skill_files:
        violations, fixed = lint_file(path, fix=args.fix)
        errors = [v for v in violations if v.level == "error"]
        warnings = [v for v in violations if v.level == "warning"]
        fails = errors + (warnings if args.strict else [])
        passed = not fails

        if passed:
            pass_count += 1
        else:
            fail_count += 1

        result = {
            "file": str(path),
            "status": "PASS" if passed else "FAIL",
            "fixed": fixed,
            "errors": [v.to_dict() for v in errors],
            "warnings": [v.to_dict() for v in warnings],
        }
        all_results.append(result)

        if not args.json:
            print_result(path, violations, fixed, args.strict)

    if args.json:
        output_json(all_results)
    else:
        print(f"\n{pass_count}/{len(skill_files)} PASS", end="")
        if fail_count:
            print(f", {fail_count} FAIL")
        else:
            print()

    sys.exit(0 if fail_count == 0 else 1)


if __name__ == "__main__":
    main()
