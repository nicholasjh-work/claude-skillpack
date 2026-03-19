#!/usr/bin/env python3
"""
tools/build_all.py

Packages every skill in skills/ into dist/ using package_skill.py logic.
Creates dist/ if it doesn't exist.

Usage:
    python tools/build_all.py
    python tools/build_all.py --skills-dir skills/ --output dist/
    python tools/build_all.py --force   # package even if lint errors

Exit codes:
    0 - all skills packaged successfully
    1 - one or more skills failed to package
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from package_skill import package_skill


def main():
    parser = argparse.ArgumentParser(
        description="Package all skills in skills/ into dist/ as .skill files."
    )
    parser.add_argument(
        "--skills-dir",
        default="skills",
        metavar="DIR",
        help="Directory containing skill subdirectories (default: skills/)",
    )
    parser.add_argument(
        "--output",
        default="dist",
        metavar="DIR",
        help="Output directory for .skill files (default: dist/)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Package skills even if lint errors are present",
    )
    args = parser.parse_args()

    skills_dir = Path(args.skills_dir)
    output_dir = Path(args.output)

    if not skills_dir.is_dir():
        print(f"ERROR: skills directory not found: {skills_dir}", file=sys.stderr)
        sys.exit(1)

    # Find all skill directories (any subdir containing SKILL.md)
    skill_dirs = sorted(
        d for d in skills_dir.iterdir()
        if d.is_dir() and (d / "SKILL.md").exists()
    )

    if not skill_dirs:
        print(f"ERROR: No skill directories found in {skills_dir}", file=sys.stderr)
        sys.exit(1)

    print(f"Building {len(skill_dirs)} skills -> {output_dir}/\n")

    packaged = []
    failed = []

    for skill_dir in skill_dirs:
        try:
            output_path = package_skill(skill_dir, output_dir, force=args.force)
            print(f"  OK  {skill_dir.name} -> {output_path.name}")
            packaged.append(skill_dir.name)
        except SystemExit:
            print(f"  FAIL  {skill_dir.name}")
            failed.append(skill_dir.name)
        except Exception as e:
            print(f"  ERROR  {skill_dir.name}: {e}")
            failed.append(skill_dir.name)

    print(f"\n{'='*50}")
    print(f"Packaged: {len(packaged)}   Failed: {len(failed)}")
    if failed:
        print(f"Failed skills: {', '.join(failed)}")
        sys.exit(1)
    else:
        print(f"All {len(packaged)} skills packaged successfully.")
        sys.exit(0)


if __name__ == "__main__":
    main()
