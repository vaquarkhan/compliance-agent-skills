#!/usr/bin/env python3
"""Validate COPPA consent template — coppa-children-privacy example."""

from __future__ import annotations

import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Install PyYAML: pip install pyyaml", file=sys.stderr)
    raise SystemExit(1)

ROOT = Path(__file__).resolve().parent.parent.parent
TEMPLATE = ROOT / "templates" / "coppa-parental-consent.yaml"


def main() -> int:
    data = yaml.safe_load(TEMPLATE.read_text(encoding="utf-8"))
    errors: list[str] = []

    if not data.get("verifiable_parental_consent", {}).get("required"):
        errors.append("verifiable_parental_consent.required must be true for under-13 services")

    security = data.get("security", {})
    if not security.get("redaction_before_llm"):
        errors.append("security.redaction_before_llm must be true before LLM processing")
    if security.get("deanonymize_enabled"):
        errors.append("COPPA: deanonymize_enabled should remain false for child PI")

    restricted = data.get("restricted", {})
    if restricted.get("targeted_ads"):
        errors.append("restricted.targeted_ads must be false under COPPA")

    if errors:
        for e in errors:
            print(f"FAIL: {e}")
        return 1

    print("=== COPPA Parental Consent Example ===")
    print(f"Template: {TEMPLATE.relative_to(ROOT)}")
    print("VPC, redaction, and restricted-use controls validated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
