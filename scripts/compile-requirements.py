#!/usr/bin/env python3
"""Compile requirements.in to requirements-lock.txt using pip-tools."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REQ_IN = ROOT / "requirements.in"
REQ_LOCK = ROOT / "requirements-lock.txt"


def main() -> int:
    if not REQ_IN.exists():
        print(f"Missing {REQ_IN}", file=sys.stderr)
        return 1
    cmd = [
        sys.executable,
        "-m",
        "piptools",
        "compile",
        str(REQ_IN),
        "-o",
        str(REQ_LOCK),
        "--strip-extras",
        "--generate-hashes",
        "--allow-unsafe",
        "--resolver=backtracking",
    ]
    print("Running:", " ".join(cmd))
    return subprocess.call(cmd, cwd=ROOT)


if __name__ == "__main__":
    raise SystemExit(main())
