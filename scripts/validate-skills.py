#!/usr/bin/env python3
"""Validate all SKILL.md files for required frontmatter and sections."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"

REQUIRED_FRONTMATTER = ("name", "description")
REQUIRED_SECTIONS = (
    "## Overview",
    "## When to Use",
    "## Core Process",
)


def parse_frontmatter(content: str) -> dict[str, str]:
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if not match:
        return {}
    result: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" in line:
            key, _, value = line.partition(":")
            result[key.strip()] = value.strip()
    return result


def validate_skill(path: Path) -> list[str]:
    errors: list[str] = []
    content = path.read_text(encoding="utf-8")
    fm = parse_frontmatter(content)
    for key in REQUIRED_FRONTMATTER:
        if key not in fm or not fm[key]:
            errors.append(f"missing frontmatter '{key}'")
        elif key == "name" and fm[key] != path.parent.name:
            errors.append(f"name '{fm[key]}' != directory '{path.parent.name}'")
    for section in REQUIRED_SECTIONS:
        if section not in content:
            errors.append(f"missing section '{section}'")
    return errors


def main() -> int:
    if not SKILLS_DIR.is_dir():
        print(f"ERROR: skills directory not found: {SKILLS_DIR}", file=sys.stderr)
        return 1

    skill_files = sorted(SKILLS_DIR.glob("*/SKILL.md"))
    if not skill_files:
        print("ERROR: no SKILL.md files found", file=sys.stderr)
        return 1

    total_errors = 0
    for skill_path in skill_files:
        errs = validate_skill(skill_path)
        if errs:
            total_errors += len(errs)
            print(f"FAIL {skill_path.relative_to(ROOT)}")
            for e in errs:
                print(f"  - {e}")
        else:
            print(f"OK   {skill_path.relative_to(ROOT)}")

    print(f"\nValidated {len(skill_files)} skill(s), {total_errors} error(s)")
    return 1 if total_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
