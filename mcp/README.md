# MCP Server Templates

Pre-configured MCP server definitions for compliance audit workflows. Copy into your IDE MCP config (Cursor, Claude Desktop, VS Code) and replace placeholder secrets via environment variables.

## Templates

| File | Server | Purpose |
| --- | --- | --- |
| [playwright.mcp.json](playwright.mcp.json) | `@playwright/mcp` | Payment-page script/DOM audits (PCI 6.4.3) |
| [postgres.mcp.json](postgres.mcp.json) | Postgres read-only | Evidence queries, access reviews |
| [presidio.mcp.json](presidio.mcp.json) | Custom Presidio bridge | Extended DLP entity detection |
| [slack.mcp.json](slack.mcp.json) | Slack | Incident/audit notifications |
| [github.mcp.json](github.mcp.json) | GitHub | Change management evidence (CC8.1) |
| [terraform.mcp.json](terraform.mcp.json) | Terraform | IaC drift scans |

## Security requirements

1. **OAuth 2.1 + PKCE** for remote MCP servers
2. **Least-privilege tool scopes** — review each server's tool allowlist
3. **No production secrets in JSON** — use env vars or secret manager
4. **Audit logging** for every tool call (see `references/mcp-compliance-patterns.md`)

## Installation

```bash
./bootstrap.sh --target cursor
# or manually merge mcp/*.mcp.json into your MCP config
```

## Skill

Load `mcp-compliance-integration` when configuring or auditing MCP deployments.

## Registry

Indexed in [registry/assets.json](../registry/assets.json) under `mcp_templates`.
