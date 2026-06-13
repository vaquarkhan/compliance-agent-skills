#!/usr/bin/env python3
"""Validate registry/assets.json — ensure all referenced paths exist."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "registry" / "assets.json"


def collect_paths(data: dict) -> list[tuple[str, str]]:
    paths: list[tuple[str, str]] = []

    for item in data.get("templates", []):
        paths.append(("templates", item["path"]))
    for item in data.get("starter_packs", []):
        paths.append(("starter_packs", item["path"]))
    for item in data.get("examples", []):
        paths.append(("examples", item["path"]))
    for item in data.get("mcp_templates", []):
        paths.append(("mcp_templates", item["path"]))
    for item in data.get("plugin_packages", []):
        paths.append(("plugin_packages", item["path"]))
    for key in ("presets", "references", "agents", "core_scripts"):
        for p in data.get(key, []):
            paths.append((key, p))
    for item in data.get("install_surfaces", []):
        for p in item.get("paths", []):
            paths.append(("install_surfaces", p.rstrip("/")))

    return paths


def main() -> int:
    if not ASSETS.exists():
        print(f"ERROR: {ASSETS} not found", file=sys.stderr)
        return 1

    data = json.loads(ASSETS.read_text(encoding="utf-8"))
    paths = collect_paths(data)
    missing: list[str] = []
    checked = 0

    for section, rel in paths:
        full = ROOT / rel
        checked += 1
        if not full.exists():
            missing.append(f"[{section}] {rel}")
            print(f"MISSING  {rel}")
        else:
            print(f"OK       {rel}")

    print(f"\nChecked {checked} path(s), {len(missing)} missing")
    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
