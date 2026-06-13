#!/usr/bin/env python3
"""Copy registry/install-manifest.json to VS Code and JetBrains plugin bundles."""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "registry" / "install-manifest.json"
TARGETS = [
    ROOT / "vscode-extension" / "install-manifest.json",
    ROOT / "jetbrains-plugin" / "src" / "main" / "resources" / "install-manifest.json",
]


def main() -> int:
    if not SRC.exists():
        print(f"ERROR: {SRC} not found", file=sys.stderr)
        return 1
    for target in TARGETS:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(SRC, target)
        print(f"Synced -> {target.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
