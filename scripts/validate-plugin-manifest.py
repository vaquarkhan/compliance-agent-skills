#!/usr/bin/env python3
"""Ensure install-manifest.json paths exist and vscode/jetbrains copies stay in sync."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "registry" / "install-manifest.json"
VSCODE_COPY = ROOT / "vscode-extension" / "install-manifest.json"
JETBRAINS_COPY = ROOT / "jetbrains-plugin" / "src" / "main" / "resources" / "install-manifest.json"


def collect_paths(data: dict) -> list[str]:
    paths: list[str] = list(data.get("core_files", []))
    paths.extend(data.get("skill_files", []))
    for group in (
        data.get("agent_adapters", {}),
        data.get("starter_packs", {}),
        data.get("mcp_templates", {}),
        data.get("runnable_examples", {}),
    ):
        for files in group.values():
            paths.extend(files)
    for extra in data.get("full_toolkit_extra", []):
        paths.append(extra.rstrip("/"))
    return sorted(set(paths))


def main() -> int:
    errors: list[str] = []

    if not MANIFEST.exists():
        print(f"ERROR: missing {MANIFEST}", file=sys.stderr)
        return 1

    if not VSCODE_COPY.exists():
        errors.append("vscode-extension/install-manifest.json missing (copy from registry/)")
    elif MANIFEST.read_text(encoding="utf-8") != VSCODE_COPY.read_text(encoding="utf-8"):
        errors.append(
            "vscode-extension/install-manifest.json out of sync with registry/install-manifest.json"
        )

    if not JETBRAINS_COPY.exists():
        errors.append("jetbrains-plugin install-manifest.json missing (copy from registry/)")
    elif MANIFEST.read_text(encoding="utf-8") != JETBRAINS_COPY.read_text(encoding="utf-8"):
        errors.append(
            "jetbrains-plugin install-manifest.json out of sync with registry/install-manifest.json"
        )

    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    missing = [p for p in collect_paths(data) if not (ROOT / p).exists()]
    for path in missing:
        errors.append(f"missing path: {path}")
        print(f"MISSING  {path}")

    for path in collect_paths(data):
        if (ROOT / path).exists():
            print(f"OK       {path}")

    if errors:
        print(f"\nPlugin manifest validation failed ({len(errors)} issue(s)):", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    print(f"\nValidated {len(collect_paths(data))} install path(s); manifest copies in sync.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
