#!/usr/bin/env python3
"""Validate FERPA school-official template — ferpa-education-records example."""

from __future__ import annotations

import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Install PyYAML: pip install pyyaml", file=sys.stderr)
    raise SystemExit(1)

ROOT = Path(__file__).resolve().parent.parent.parent
TEMPLATE = ROOT / "templates" / "ferpa-school-official.yaml"
REQUIRED_TOP = {
    "school_official",
    "legitimate_educational_interest",
    "technical_controls",
}


def main() -> int:
    data = yaml.safe_load(TEMPLATE.read_text(encoding="utf-8"))
    missing = REQUIRED_TOP - set(data.keys())
    if missing:
        print(f"Missing required sections: {', '.join(sorted(missing))}")
        return 1

    controls = data.get("technical_controls", {})
    if not controls.get("llm_redaction"):
        print("FERPA EdTech control: llm_redaction must be true for agent workflows")
        return 1
    if controls.get("deanonymize_production"):
        print("WARN: deanonymize_production=true — ensure LEI authorization for production")

    print("=== FERPA School Official Example ===")
    print(f"Template: {TEMPLATE.relative_to(ROOT)}")
    print("Required sections present; llm_redaction enforced.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
