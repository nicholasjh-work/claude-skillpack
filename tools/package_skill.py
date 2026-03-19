#!/usr/bin/env python3
"""
tools/package_skill.py

Packages a skill folder into a .skill file (zip archive) for Claude.ai upload.
Validates with skill_linter before packaging. Refuses to package if lint fails.

Usage:
    python tools/package_skill.py skills/email-writer
    python tools/package_skill.py skills/email-writer --output dist/
    python tools/package_skill.py skills/email-writer --output dist/ --force
"""

import argparse
import sys
import zipfile
from pathlib import Path

# Allow importing from the tools/ directory itself
sys.path.insert(0, str(Path(__file__).parent))
from skill_linter import collect_skill_files, lint_file


def package_skill(skill_dir: Path, output_dir: Path, force: bool = False) -> Path:
    """
    Lint and package a skill directory into a .skill zip archive.

    Returns the path to the created .skill file.
    Raises SystemExit(1) if lint fails.
    """
    skill_dir = skill_dir.resolve()

    if not skill_dir.is_dir():
        print(f"ERROR: Not a directory: {skill_dir}", file=sys.stderr)
        sys.exit(1)

    skill_files = collect_skill_files(skill_dir)
    if not skill_files:
        print(f"ERROR: No SKILL.md found in {skill_dir}", file=sys.stderr)
        sys.exit(1)

    # Lint check
    all_pass = True
    for path in skill_files:
        violations, _ = lint_file(path, fix=False)
        errors = [v for v in violations if v.level == "error"]
        if errors:
            print(f"LINT FAIL: {path}")
            for v in errors:
                print(str(v))
            all_pass = False

    if not all_pass and not force:
        print(
            f"\nPackaging refused: lint errors found in {skill_dir.name}. "
            f"Fix errors or use --force to override.",
            file=sys.stderr,
        )
        sys.exit(1)

    if not all_pass and force:
        print(f"WARNING: packaging {skill_dir.name} despite lint errors (--force)")

    # Build the archive
    output_dir.mkdir(parents=True, exist_ok=True)
    skill_name = skill_dir.name
    output_path = output_dir / f"{skill_name}.skill"

    with zipfile.ZipFile(output_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for file_path in sorted(skill_dir.rglob("*")):
            if file_path.is_file():
                # Store as skill_name/relative_path so it unpacks cleanly
                arcname = skill_name / file_path.relative_to(skill_dir)
                zf.write(file_path, arcname)

    return output_path


def main():
    parser = argparse.ArgumentParser(
        description="Package a skill folder into a .skill file for Claude.ai upload."
    )
    parser.add_argument("skill_dir", help="Path to the skill directory")
    parser.add_argument(
        "--output",
        default="dist",
        metavar="DIR",
        help="Output directory for the .skill file (default: dist/)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Package even if lint errors are present",
    )
    args = parser.parse_args()

    skill_dir = Path(args.skill_dir)
    output_dir = Path(args.output)

    output_path = package_skill(skill_dir, output_dir, force=args.force)
    print(output_path)


if __name__ == "__main__":
    main()
