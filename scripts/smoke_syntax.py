#!/usr/bin/env python3
"""AST syntax check for Python entrypoints (no third-party imports)."""

from __future__ import annotations

import ast
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENTRYPOINTS = [
    ROOT / "agent.py",
    ROOT / "redaction.py",
    ROOT / "scripts" / "validate-skills.py",
    ROOT / "scripts" / "validate-assets.py",
]


def main() -> int:
    errors = 0
    for path in ENTRYPOINTS:
        try:
            ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            print(f"OK   {path.relative_to(ROOT)}")
        except SyntaxError as exc:
            print(f"FAIL {path}: {exc}", file=sys.stderr)
            errors += 1
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
