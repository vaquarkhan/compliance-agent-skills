#!/usr/bin/env python3
"""Sync VERSION file to package manifests (single source of truth)."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VERSION_FILE = ROOT / "VERSION"

TARGETS: list[tuple[Path, str, str]] = [
    (ROOT / "registry" / "assets.json", r'"version": "[^"]+"', '"version": "{v}"'),
    (ROOT / "vscode-extension" / "package.json", r'"version": "[^"]+"', '"version": "{v}"'),
    (
        ROOT / "jetbrains-plugin" / "gradle.properties",
        r"pluginVersion = .+",
        "pluginVersion = {v}",
    ),
]


def read_version() -> str:
    version = VERSION_FILE.read_text(encoding="utf-8").strip()
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        raise SystemExit(f"Invalid VERSION: {version!r} (expected semver x.y.z)")
    return version


def sync_file(path: Path, pattern: str, replacement_template: str, version: str) -> None:
    text = path.read_text(encoding="utf-8")
    replacement = replacement_template.format(v=version)
    new_text, count = re.subn(pattern, replacement, text, count=1)
    if count != 1:
        raise SystemExit(f"Could not update version in {path}")
    path.write_text(new_text, encoding="utf-8")
    print(f"Synced {path.relative_to(ROOT)} -> {version}")


def main() -> int:
    version = read_version()
    for path, pattern, template in TARGETS:
        if not path.exists():
            print(f"SKIP missing {path}", file=sys.stderr)
            continue
        sync_file(path, pattern, template, version)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
