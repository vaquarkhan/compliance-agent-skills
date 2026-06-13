# Claude Setup

Configure **Claude Code** or **Claude Desktop** for compliance-agent-skills.

## Quick install

```bash
./bootstrap.sh --target claude
```

Copies:

- `CLAUDE.md` — Claude entry point
- `.claude/commands/` — lifecycle slash commands
- Skills to `~/.claude/skills/compliance-agent-skills/`

## Entry documents

Read order:

1. [CLAUDE.md](../CLAUDE.md)
2. [AGENTS.md](../AGENTS.md)
3. [skills-index.md](../skills-index.md)

## Slash commands

| Command | File | Purpose |
| --- | --- | --- |
| `/scope` | `.claude/commands/scope.md` | Engagement scoping |
| `/audit` | `.claude/commands/audit.md` | Control testing |
| `/evidence` | `.claude/commands/evidence.md` | Artifact collection |
| `/remediate` | `.claude/commands/remediate.md` | Gap remediation |
| `/report` | `.claude/commands/report.md` | Findings report |

## MCP for Claude Desktop

Add servers from `mcp/` to Claude Desktop MCP config. Use OAuth where supported; store tokens in OS keychain, not repo files.

## PHI redaction

Claude sessions must treat `<PERSON_1>`-style tokens as intentional masks. For programmatic redaction, use:

```bash
python agent.py "your prompt"
```

## Presets

Load industry context from `presets/*/PRESET.md` at engagement start.

## See also

- [getting-started.md](getting-started.md)
- [mcp-compliance-patterns.md](../references/mcp-compliance-patterns.md)
