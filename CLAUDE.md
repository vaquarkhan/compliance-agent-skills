# CLAUDE.md — Claude Code Entry Point

Claude-specific instructions for the **compliance-agent-skills** repository.

## Identity

You are assisting with **USA compliance auditing** (HIPAA, PCI-DSS v4.0, SOC 2) in an agent-skills repository. You must follow loaded skills exactly and never invent regulatory steps.

## First actions

1. Read [AGENTS.md](AGENTS.md) for routing.
2. If the task is broad, load skill **`using-compliance-agent-skills`**.
3. Apply PHI redaction mentally: treat `<ENTITY_N>` tokens as intentional masks—do not guess original values.
4. Check for an applicable **preset** in `presets/` when the user names healthcare, fintech, SaaS, or a cloud provider.

## Lifecycle commands

Slash commands in `.claude/commands/`:

| Command | File |
| --- | --- |
| `/scope` | `.claude/commands/scope.md` |
| `/audit` | `.claude/commands/audit.md` |
| `/evidence` | `.claude/commands/evidence.md` |
| `/remediate` | `.claude/commands/remediate.md` |
| `/report` | `.claude/commands/report.md` |

Run them in order for full engagements unless the user requests a subset.

## Skill discovery

- Index: [skills-index.md](skills-index.md)
- Validation: `python scripts/validate-skills.py`

## MCP

When the user needs browser audits, DB evidence, or IaC scans, reference templates in `mcp/` and skill `mcp-compliance-integration`. Require OAuth 2.1 + PKCE and least-privilege tool scopes.

## Output standards

- Scope artifacts: JSON with engagement ID, UTC timestamp, approver
- Evidence: YAML manifest with SHA-256 per file (`templates/audit-evidence-manifest.yaml`)
- Findings: severity, control ID, observation, recommendation, owner, due date
- Never include raw PHI/PAN in final reports unless explicitly authorized and redaction is disabled for that export path

## References

Quick checklists live in `references/`:

- `hipaa-security-rule-checklist.md`
- `pci-dss-v4-checklist.md`
- `soc2-trust-services-criteria-checklist.md`

## Python agent

For programmatic runs:

```bash
pip install -r requirements.txt
python agent.py "Your audit prompt"
```

The agent applies Presidio redaction before your reasoning equivalent in the SDK path.
