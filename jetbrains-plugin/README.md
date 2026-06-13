# Compliance Agent Skills — JetBrains Plugin

This plugin installs the USA compliance skill pack (HIPAA, PCI-DSS, SOC 2) into the current project for IntelliJ-based IDEs such as:

- IntelliJ IDEA
- PyCharm
- WebStorm
- DataGrip
- GoLand
- PhpStorm

## Commands

Available under **Tools → Compliance Agent Skills**:

- Install Full Toolkit
- Install Core Pack
- Install Agent Adapters
- Install Starter Pack
- Install MCP Templates
- Scaffold Runnable Example

## What It Installs

Depending on the command, the plugin can place:

- `AGENTS.md`, `CLAUDE.md`, `skills-index.md`
- `agent.py`, `redaction.py`, `requirements.txt`
- `registry/assets.json`
- `templates/` — scope, audit, evidence, remediation templates
- `hooks/` — PHI redaction, audit, and evidence integrity guards
- `scripts/` — install helpers and evidence validation
- `skills/` — HIPAA, PCI-DSS, and SOC 2 Agent Skills
- `.cursor/rules/`, `.claude/commands/`, `.github/copilot-instructions.md`
- `starter-packs/` and `mcp/` templates
- runnable example folders under `examples/`

## Source Resolution

During local development, the plugin loads files from the repository checkout (parent of `jetbrains-plugin/`).

For packaged usage, it falls back to the raw GitHub source at:

```text
https://raw.githubusercontent.com/vaquarkhan/compliance-agent-skills/main
```

## Build

```bash
./gradlew buildPlugin
```

## Local Run

```bash
./gradlew runIde
```
