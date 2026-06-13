#!/usr/bin/env python3
"""Install compliance-agent-skills into IDE and agent config directories."""

from __future__ import annotations

import argparse
import json
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "registry" / "assets.json"

SKILL_DIRS = ["skills"]
CORE_FILES = ["agent.py", "redaction.py", "requirements.txt", "AGENTS.md", "CLAUDE.md"]
COPY_DIRS = {
    "cursor": [".cursor/rules", "hooks", "mcp"],
    "claude": [".claude/commands", "skills"],
    "vscode": [".github"],
    "python": ["skills", "templates", "references", "presets"],
}
OPTIONAL_ALL = ["templates", "starter-packs", "presets", "references", "agents", "examples"]


def detect_targets(explicit: list[str] | None) -> list[str]:
    if explicit:
        return explicit
    targets: list[str] = ["python"]
    if os.environ.get("CURSOR_TRACE_ID") or (Path.home() / ".cursor").exists():
        targets.append("cursor")
    if shutil.which("code"):
        targets.append("vscode")
    if (Path.home() / ".claude").exists():
        targets.append("claude")
    if any((Path.home() / d).exists() for d in [".IntelliJIdea", ".PyCharm", ".idea"]):
        targets.append("jetbrains")
    return list(dict.fromkeys(targets))


def copy_tree(src: Path, dst: Path, *, dry_run: bool = False) -> None:
    if not src.exists():
        print(f"  skip missing: {src}")
        return
    if dry_run:
        print(f"  would copy: {src} -> {dst}")
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    if src.is_dir():
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
    else:
        shutil.copy2(src, dst)
    print(f"  copied: {src.relative_to(ROOT)} -> {dst}")


def install_python(deps: bool, dry_run: bool) -> None:
    print("\n[python-agent] Core agent files")
    for name in CORE_FILES:
        copy_tree(ROOT / name, ROOT / name, dry_run=dry_run)  # validate presence
    for dirname in SKILL_DIRS + OPTIONAL_ALL:
        src = ROOT / dirname
        if src.exists():
            print(f"  present: {dirname}/")
    if deps and not dry_run:
        req = ROOT / "requirements.txt"
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", str(req)])


def install_cursor(project: Path, dry_run: bool) -> None:
    print("\n[cursor] Rules, hooks, MCP templates")
    dest_root = project
    for rel in COPY_DIRS["cursor"]:
        copy_tree(ROOT / rel, dest_root / rel, dry_run=dry_run)
    skills_dest = dest_root / ".cursor" / "skills" / "compliance-agent-skills"
    copy_tree(ROOT / "skills", skills_dest, dry_run=dry_run)


def install_claude(project: Path, dry_run: bool) -> None:
    print("\n[claude] Commands and CLAUDE.md")
    claude_home = Path.home() / ".claude"
    for rel in COPY_DIRS["claude"]:
        src = ROOT / rel
        dst = claude_home / Path(rel).name if rel.startswith(".claude") else project / rel
        if rel == "skills":
            dst = claude_home / "skills" / "compliance-agent-skills"
        copy_tree(src, dst, dry_run=dry_run)
    copy_tree(ROOT / "CLAUDE.md", project / "CLAUDE.md", dry_run=dry_run)


def install_vscode(project: Path, dry_run: bool) -> None:
    print("\n[vscode] Copilot instructions")
    copy_tree(ROOT / ".github" / "copilot-instructions.md", project / ".github" / "copilot-instructions.md", dry_run=dry_run)
    ext = ROOT / "vscode-extension"
    if ext.exists():
        print(f"  extension source: {ext.relative_to(ROOT)}/")


def install_jetbrains(dry_run: bool) -> None:
    print("\n[jetbrains] Plugin build instructions")
    plugin = ROOT / "jetbrains-plugin"
    if plugin.exists():
        print(f"  build with: cd {plugin} && ./gradlew buildPlugin")
    if dry_run:
        return


def validate_assets() -> bool:
    if not ASSETS.exists():
        print("WARN: registry/assets.json not found")
        return False
    data = json.loads(ASSETS.read_text(encoding="utf-8"))
    missing: list[str] = []
    for section in ("templates", "starter_packs", "examples", "mcp_templates"):
        for item in data.get(section, []):
            path = item.get("path") if isinstance(item, dict) else item
            if path and not (ROOT / path).exists():
                missing.append(path)
    if missing:
        print("Missing asset paths:")
        for m in missing:
            print(f"  - {m}")
        return False
    print("Asset registry: all referenced paths exist")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Install compliance-agent-skills toolkit")
    parser.add_argument("--target", action="append", dest="targets", help="cursor|claude|vscode|jetbrains|python")
    parser.add_argument("--project", type=Path, default=ROOT, help="Destination project directory")
    parser.add_argument("--no-deps", action="store_true", help="Skip pip install")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()

    print(f"compliance-agent-skills installer")
    print(f"  root: {ROOT}")
    print(f"  platform: {platform.system()} {platform.release()}")

    if args.validate_only:
        ok = validate_assets()
        return 0 if ok else 1

    targets = detect_targets(args.targets)
    print(f"  targets: {', '.join(targets)}")

    if "python" in targets:
        install_python(deps=not args.no_deps, dry_run=args.dry_run)
    if "cursor" in targets:
        install_cursor(args.project, args.dry_run)
    if "claude" in targets:
        install_claude(args.project, args.dry_run)
    if "vscode" in targets:
        install_vscode(args.project, args.dry_run)
    if "jetbrains" in targets:
        install_jetbrains(args.dry_run)

    validate_assets()
    print("\nDone.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
