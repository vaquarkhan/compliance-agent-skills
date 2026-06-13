# Compliance Agent Skills for VS Code Family

This extension installs the repository's USA compliance skill pack (HIPAA, PCI-DSS, SOC 2) into the current workspace.

Compatible editors:

- VS Code
- Cursor
- Windsurf
- VSCodium

## Commands

- `Compliance Agent Skills: Install Full Toolkit`
- `Compliance Agent Skills: Install Core Pack`
- `Compliance Agent Skills: Install Agent Adapters`
- `Compliance Agent Skills: Install Starter Pack`
- `Compliance Agent Skills: Install MCP Templates`
- `Compliance Agent Skills: Scaffold Runnable Example`

## What It Installs

Depending on the command, the extension can write:

- `AGENTS.md`, `CLAUDE.md`, `skills-index.md`
- `agent.py`, `redaction.py`, `requirements.txt`
- `registry/assets.json`
- `templates/` — scope, audit, evidence, remediation, and control-mapping templates
- `hooks/` — PHI redaction, audit, evidence integrity, and incident guards
- `scripts/` — install helpers, evidence validation, hook runner
- `skills/` — HIPAA, PCI-DSS, and SOC 2 Agent Skills
- `.cursor/rules/`, `.claude/commands/`, `.github/copilot-instructions.md`
- `.gemini/commands/`, `.kiro/steering/`, `.opencode/`
- `starter-packs/` — HIPAA Healthcare, PCI-DSS Ecommerce, SOC2 SaaS, Regulated AI Agents
- `mcp/` — Playwright, Postgres, Presidio, Slack, GitHub, Terraform templates
- runnable example folders under `examples/`

## Starter Packs

| Pack | Use case |
| --- | --- |
| HIPAA Healthcare | PHI handling, BAA workflows, technical safeguards |
| PCI-DSS Ecommerce | Checkout scripts, CDE segmentation, payment flows |
| SOC2 SaaS | Trust Services Criteria, evidence collection, CCM |
| Regulated AI Agents | PHI redaction gates, MCP hardening, audit lifecycle |

## Runnable Examples

| Example | Description |
| --- | --- |
| pci-checkout-audit | Playwright-driven PCI-DSS 6.4.3 script inventory |
| hipaa-phi-redaction | Presidio PHI redaction pipeline with agent integration |
| soc2-evidence-bundle | Evidence hashing, manifest, and auditor handoff |

## Source Resolution

During local development, the extension loads files from the repository checkout (parent of `vscode-extension/`).

For packaged usage, it falls back to the raw GitHub source using the `complianceAgentSkills.rawBaseUrl` setting.

Default base URL:

```text
https://raw.githubusercontent.com/vaquarkhan/compliance-agent-skills/main
```

## Local Development

1. Open the `vscode-extension/` folder in VS Code.
2. Press `F5` to launch the Extension Development Host.
3. Run the commands from the command palette in a test workspace.
