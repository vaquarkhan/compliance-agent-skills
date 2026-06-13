# MCP Compliance Patterns

Security patterns for Model Context Protocol servers in HIPAA, PCI, and SOC 2 audit architectures.

## Transport and authentication

| Pattern | Requirement | Implementation |
| --- | --- | --- |
| TLS everywhere | SOC 2 CC6.7, HIPAA §164.312(e) | Terminate TLS at gateway; no plain HTTP |
| OAuth 2.1 + PKCE | MCP spec best practice | No implicit grant; rotate refresh tokens |
| Scoped tools | Least privilege | Export allowlist in manifest; deny by default |
| mTLS (optional) | High-risk CDE | Client certs for MCP in PCI segments |

## Server-specific guidance

### Playwright MCP (`mcp/playwright.mcp.json`)

- **Use:** PCI script inventory, DOM snapshots
- **Deny:** form submission with real PAN, script injection
- **Evidence:** screenshot hashes in evidence manifest

### Postgres MCP (`mcp/postgres.mcp.json`)

- **Use:** Read-only evidence queries, access reviews
- **Deny:** `INSERT`, `UPDATE`, `DELETE`, `COPY TO PROGRAM`
- **HIPAA:** Row-level security; no SELECT * on clinical tables

### Presidio MCP (`mcp/presidio.mcp.json`)

- **Use:** Pre-flight entity detection beyond bundled `redaction.py`
- **Deploy:** Custom server template — run inside VPC, no external egress

### Slack MCP (`mcp/slack.mcp.json`)

- **Use:** Incident notifications, audit status
- **Deny:** Posting raw findings with PHI to public channels

### GitHub MCP (`mcp/github.mcp.json`)

- **Use:** Change tickets, PR approvals (CC8.1)
- **Scope:** Read-only PAT or GitHub App with minimal permissions

### Terraform MCP (`mcp/terraform.mcp.json`)

- **Use:** Drift detection, compliance-as-code scans
- **Deny:** `terraform apply` in production without break-glass

## Audit logging

Log every MCP tool invocation:

```json
{
  "timestamp": "ISO-8601",
  "server": "playwright",
  "tool": "browser_snapshot",
  "user_id": "agent-session-id",
  "args_hash": "sha256",
  "result_status": "success"
}
```

## Skill mapping

Primary: `mcp-compliance-integration`

Templates: `mcp/*.mcp.json`

Hook: `hooks/phi-redaction-guard.sh` before session MCP enablement
