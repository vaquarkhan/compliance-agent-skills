#!/usr/bin/env python3
"""Validate NIST AI RMF profile scaffold — nist-ai-rmf-governance example."""

from __future__ import annotations

import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Install PyYAML: pip install pyyaml", file=sys.stderr)
    raise SystemExit(1)

ROOT = Path(__file__).resolve().parent.parent.parent
TEMPLATE = ROOT / "templates" / "nist-ai-rmf-profile.yaml"
FUNCTIONS = ("govern", "map", "measure", "manage")


def main() -> int:
    data = yaml.safe_load(TEMPLATE.read_text(encoding="utf-8"))
    missing = [f for f in FUNCTIONS if f not in data]
    if missing:
        print(f"Missing AI RMF functions: {', '.join(missing)}")
        return 1

    govern = data.get("govern", {})
    if not govern.get("inventory"):
        print("govern.inventory must list AI systems (including MCP tools)")
        return 1

    measure = data.get("measure", {})
    if not measure.get("tevv"):
        print("measure.tevv required for test/eval/verification/validation")
        return 1

    print("=== NIST AI RMF Profile Example ===")
    print(f"Template: {TEMPLATE.relative_to(ROOT)}")
    print("GOVERN/MAP/MEASURE/MANAGE scaffold present.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
