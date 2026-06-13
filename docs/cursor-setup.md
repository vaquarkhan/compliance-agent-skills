# Cursor Setup

Install compliance-agent-skills into **Cursor** for rules, hooks, MCP templates, and skills.

## Quick install

From the repository root:

```bash
./bootstrap.sh --target cursor
```

Or on Windows:

```powershell
.\bootstrap.ps1 --target cursor
```

## What gets installed

| Component | Source | Destination |
| --- | --- | --- |
| Agent rules | `.cursor/rules/` | Project `.cursor/rules/` |
| Skills | `skills/` | `.cursor/skills/compliance-agent-skills/` |
| Hooks | `hooks/` | Project `hooks/` + merge `hooks.json` |
| MCP templates | `mcp/` | Merge into Cursor MCP settings |

## Rules overview

| Rule | Purpose |
| --- | --- |
| `00-compliance-agent-core.mdc` | Core mission and PHI gate |
| `10-deterministic-audit.mdc` | No invented regulatory steps |
| `20-phi-redaction-first.mdc` | Presidio before LLM reasoning |
| `30-framework-routing.mdc` | HIPAA / PCI / SOC 2 skill routing |

## MCP configuration

1. Open **Cursor Settings → MCP**
2. Import servers from `mcp/*.mcp.json`
3. Set environment variables (e.g. `POSTGRES_EVIDENCE_RO_URL`, `GITHUB_COMPLIANCE_READ_TOKEN`)

See [mcp/README.md](../mcp/README.md).

## Hooks

Merge [hooks/hooks.json](../hooks/hooks.json) into your Cursor hooks config. Hooks enforce:

- Session engagement ID
- Presidio availability when `COMPLIANCE_PHI_REDACTION=required`

## Lifecycle commands

Claude commands in `.claude/commands/` work in Cursor when copied or referenced. Use `/scope`, `/audit`, etc.

## Environment variables

```bash
export COMPLIANCE_ENGAGEMENT_ID=ENG-2026-001
export COMPLIANCE_PHI_REDACTION=required
export COMPLIANCE_AUDIT_MODE=false
```

Enable audit mode: `source hooks/audit-mode.sh`

## Validation

```bash
python scripts/validate-skills.py
python scripts/validate-assets.py
```

## See also

- [AGENTS.md](../AGENTS.md)
- [getting-started.md](getting-started.md)
