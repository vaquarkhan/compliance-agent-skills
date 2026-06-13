#!/usr/bin/env python3
"""Validate SME provenance footers on regulatory reference checklists."""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REFERENCES = ROOT / "references"

REQUIRED_SECTIONS = ("## Authoritative sources", "## Provenance")
REQUIRED_ROWS = (
    "Source document",
    "Version / effective",
    "Last reviewed",
    "Reviewer",
    "Next review due",
)
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def checklist_paths() -> list[Path]:
    return sorted(REFERENCES.glob("*checklist*.md"))


def validate_file(path: Path, *, strict_dates: bool) -> list[str]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")

    for section in REQUIRED_SECTIONS:
        if section not in text:
            errors.append(f"{path.name}: missing section {section!r}")

    provenance_idx = text.find("## Provenance")
    if provenance_idx == -1:
        return errors

    provenance_block = text[provenance_idx:]
    for row in REQUIRED_ROWS:
        if f"**{row}**" not in provenance_block:
            errors.append(f"{path.name}: provenance missing row {row!r}")

    due_match = re.search(r"\*\*Next review due\*\*\s*\|\s*([^\|\n]+)", provenance_block)
    if due_match:
        due_raw = due_match.group(1).strip()
        if not DATE_RE.match(due_raw):
            errors.append(f"{path.name}: Next review due must be YYYY-MM-DD, got {due_raw!r}")
        elif strict_dates:
            due = date.fromisoformat(due_raw)
            if due < date.today():
                errors.append(f"{path.name}: Next review due {due_raw} is overdue")

    sources_idx = text.find("## Authoritative sources")
    if sources_idx != -1:
        sources_block = text[sources_idx:provenance_idx]
        if "http" not in sources_block and "ecfr.gov" not in sources_block:
            if not re.search(r"\[.*\]\(.*\)", sources_block):
                errors.append(f"{path.name}: Authoritative sources should include at least one link")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate SME provenance on reference checklists")
    parser.add_argument(
        "--strict-dates",
        action="store_true",
        help="Fail when Next review due is in the past",
    )
    args = parser.parse_args()

    paths = checklist_paths()
    if not paths:
        print("No checklist files found under references/", file=sys.stderr)
        return 1

    all_errors: list[str] = []
    for path in paths:
        all_errors.extend(validate_file(path, strict_dates=args.strict_dates))

    if all_errors:
        print("SME provenance validation failed:")
        for err in all_errors:
            print(f"  - {err}")
        return 1

    print(f"OK: SME provenance valid on {len(paths)} checklist(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
