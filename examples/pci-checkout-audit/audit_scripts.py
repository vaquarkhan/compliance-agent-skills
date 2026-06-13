#!/usr/bin/env python3
"""Validate PCI checkout script baseline and compare against a local script list."""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path
from urllib.parse import urljoin, urlparse

try:
    import yaml
except ImportError:
    print("Install PyYAML: pip install pyyaml", file=sys.stderr)
    raise SystemExit(1)

BASELINE = Path(__file__).resolve().parent / "config" / "baseline.yaml"


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_baseline() -> dict:
    return yaml.safe_load(BASELINE.read_text(encoding="utf-8"))


def validate_baseline_structure(data: dict) -> list[str]:
    errors: list[str] = []
    for key in ("baseline_id", "target_url", "scripts"):
        if key not in data:
            errors.append(f"baseline missing required key: {key}")
    scripts = data.get("scripts") or []
    if not scripts:
        errors.append("baseline scripts list is empty")
    for idx, script in enumerate(scripts):
        for field in ("script_id", "type", "integrity_algorithm", "integrity_value"):
            if field not in script:
                errors.append(f"scripts[{idx}] missing {field}")
    return errors


def compare_script_ids(data: dict, discovered_ids: list[str]) -> dict:
    authorized = {s["script_id"] for s in data.get("scripts", [])}
    discovered = set(discovered_ids)
    return {
        "authorized_only": sorted(authorized - discovered),
        "unauthorized": sorted(discovered - authorized),
        "matched": sorted(authorized & discovered),
    }


def fetch_scripts_from_url(url: str) -> list[dict]:
    """Fetch HTML and extract script tags (stdlib only — no Playwright required for CI)."""
    import urllib.request

    req = urllib.request.Request(url, headers={"User-Agent": "compliance-agent-skills/1.0"})
    html = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", errors="replace")
    scripts: list[dict] = []
    for match in re.finditer(r'<script[^>]*\ssrc=["\']([^"\']+)["\']', html, re.I):
        src = match.group(1)
        absolute = urljoin(url, src)
        scripts.append({"script_id": sha256_text(absolute)[:16], "src": absolute, "type": "external"})
    for idx, match in enumerate(re.finditer(r"<script(?![^>]*\ssrc=)[^>]*>(.*?)</script>", html, re.I | re.S)):
        body = match.group(1).strip()
        if body:
            scripts.append({"script_id": sha256_text(body)[:16], "src": f"inline:{idx}", "type": "inline"})
    return scripts


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description="PCI checkout script baseline validator")
    parser.add_argument("--baseline", type=Path, default=BASELINE)
    parser.add_argument("--url", help="Optional live URL to compare script inventory")
    parser.add_argument("--discovered", nargs="*", help="Script IDs discovered by Playwright MCP audit")
    args = parser.parse_args()

    data = yaml.safe_load(args.baseline.read_text(encoding="utf-8"))
    errors = validate_baseline_structure(data)
    if errors:
        print("Baseline validation failed:")
        for err in errors:
            print(f"  - {err}")
        return 1

    print(f"OK: baseline structure valid ({args.baseline.name})")
    print(f"  baseline_id: {data.get('baseline_id')}")
    print(f"  authorized scripts: {len(data.get('scripts', []))}")

    discovered_ids: list[str] = list(args.discovered or [])
    if args.url:
        try:
            live = fetch_scripts_from_url(args.url)
            discovered_ids.extend(s["script_id"] for s in live)
            print(f"  live fetch: {len(live)} script(s) from {args.url}")
        except Exception as exc:
            print(f"WARN: could not fetch {args.url}: {exc}", file=sys.stderr)

    if discovered_ids:
        diff = compare_script_ids(data, discovered_ids)
        print(f"  matched: {len(diff['matched'])}")
        if diff["unauthorized"]:
            print(f"  UNAUTHORIZED: {diff['unauthorized']}")
            return 2
        if diff["authorized_only"]:
            print(f"  missing from page: {diff['authorized_only']}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
