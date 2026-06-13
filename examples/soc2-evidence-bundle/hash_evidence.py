#!/usr/bin/env python3
"""Compute SHA-256 hashes for SOC 2 evidence bundle artifacts and update manifest."""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Install PyYAML: pip install pyyaml", file=sys.stderr)
    raise SystemExit(1)

BUNDLE_DIR = Path(__file__).resolve().parent
MANIFEST = BUNDLE_DIR / "evidence-manifest.yaml"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return f"sha256:{h.hexdigest()}"


def bundle_hash_from_artifacts(artifacts: list[dict]) -> str:
    combined = "".join(a.get("sha256", "") for a in artifacts)
    return f"sha256:{hashlib.sha256(combined.encode()).hexdigest()}"


def main() -> int:
    data = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    updated = 0
    for item in data.get("artifacts", []):
        rel = item.get("path")
        if not rel:
            continue
        artifact = BUNDLE_DIR / rel
        if not artifact.exists():
            print(f"WARN: missing artifact {rel}", file=sys.stderr)
            continue
        item["sha256"] = sha256_file(artifact)
        item["size_bytes"] = artifact.stat().st_size
        updated += 1

    if updated:
        data["bundle_hash"] = bundle_hash_from_artifacts(data.get("artifacts", []))
        MANIFEST.write_text(yaml.dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")

    print(f"Updated {updated} artifact hash(es) in {MANIFEST.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
