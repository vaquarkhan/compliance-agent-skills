#!/usr/bin/env python3
"""Validate audit evidence manifest YAML structure and SHA-256 hashes."""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Install PyYAML: pip install pyyaml", file=sys.stderr)
    raise SystemExit(1)

ROOT = Path(__file__).resolve().parent.parent


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return f"sha256:{digest.hexdigest()}"


def validate_manifest(manifest_path: Path, *, strict_hashes: bool = False) -> list[str]:
    errors: list[str] = []
    data = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        return ["manifest root must be a mapping"]

    required = ["manifest_id", "framework", "artifacts"]
    for key in required:
        if key not in data:
            errors.append(f"missing required key: {key}")

    artifacts = data.get("artifacts") or []
    if not artifacts:
        errors.append("artifacts list is empty")

    base = manifest_path.parent
    for idx, item in enumerate(artifacts):
        if not isinstance(item, dict):
            errors.append(f"artifacts[{idx}] must be a mapping")
            continue
        for field in ("id", "path", "sha256"):
            if field not in item:
                errors.append(f"artifacts[{idx}] missing {field}")
        rel = item.get("path")
        if not rel:
            continue
        artifact_path = (base / rel).resolve()
        if not artifact_path.exists():
            errors.append(f"artifact file not found: {rel}")
            continue
        expected = item.get("sha256", "")
        if expected.startswith("sha256:placeholder") or expected == "sha256:placeholder":
            if strict_hashes:
                errors.append(f"artifacts[{idx}] still has placeholder hash for {rel}")
            continue
        if expected.startswith("sha256:") and len(expected) > 15:
            actual = sha256_file(artifact_path)
            if actual != expected:
                errors.append(f"hash mismatch for {rel}: expected {expected}, got {actual}")

    return errors


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Validate evidence manifest YAML")
    parser.add_argument("manifest", nargs="?", default=str(ROOT / "examples/soc2-evidence-bundle/evidence-manifest.yaml"))
    parser.add_argument("--strict", action="store_true", help="Fail on placeholder hashes")
    args = parser.parse_args()

    path = Path(args.manifest)
    if not path.exists():
        print(f"ERROR: {path} not found", file=sys.stderr)
        return 1

    errors = validate_manifest(path, strict_hashes=args.strict)
    if errors:
        print("Validation failed:")
        for err in errors:
            print(f"  - {err}")
        return 1

    print(f"OK: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
