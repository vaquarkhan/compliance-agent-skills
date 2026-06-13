#!/usr/bin/env python3
"""Run compliance hooks defined in hooks/hooks.json."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HOOKS_JSON = ROOT / "hooks" / "hooks.json"


def run_hook(relative_command: str) -> int:
    cmd_path = ROOT / relative_command.lstrip("./")
    if not cmd_path.exists():
        print(f"ERROR: hook not found: {cmd_path}", file=sys.stderr)
        return 1

    if cmd_path.suffix == ".ps1":
        proc = subprocess.run(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(cmd_path)],
            cwd=ROOT,
            input=sys.stdin.read() if not sys.stdin.isatty() else None,
            text=True,
        )
    else:
        proc = subprocess.run([str(cmd_path)], cwd=ROOT, text=True)
    return proc.returncode


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Run a compliance hook by name")
    parser.add_argument("hook", choices=["sessionStart", "beforeSubmitPrompt", "audit_mode", "release_guard"])
    args = parser.parse_args()

    if not HOOKS_JSON.exists():
        print(f"ERROR: {HOOKS_JSON} not found", file=sys.stderr)
        return 1

    config = json.loads(HOOKS_JSON.read_text(encoding="utf-8"))
    hooks = config.get("hooks", {})
    optional = config.get("optional_hooks", {})

    if args.hook in hooks:
        entries = hooks[args.hook]
        if not entries:
            print(f"No hooks registered for {args.hook}")
            return 0
        code = 0
        for entry in entries:
            code = run_hook(entry["command"]) or code
        return code

    if args.hook in optional:
        return run_hook(optional[args.hook])

    print(f"ERROR: unknown hook {args.hook}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
