---
name: mcp-compliance-integration
description: Hardens Model Context Protocol (MCP) server integrations for compliance—OAuth 2.1, PKCE, scoped tool sets, transport security, and patterns for Playwright, Postgres, Slack, and Presidio MCP servers in audit workflows. Trigger when deploying, configuring, or auditing MCP servers for HIPAA, PCI, or SOC 2 agent architectures. Do not use for general IAM reviews without MCP focus (use access-control-identity-audit) or PCI script DOM audits (use pci-dss-script-audit).
---

# MCP Compliance Integration

## Overview

This skill secures **Model Context Protocol (MCP)** integrations used by the compliance agent. MCP servers expose **tools** (Playwright browser automation, Postgres queries, Slack notifications, Presidio DLP) to the agent runtime. Misconfiguration creates pathways for **ePHI exfiltration, unauthorized CDE access, and unlogged actions**.

Security baseline:

- **OAuth 2.1** with **PKCE** for user-delegated MCP access
- **Tool allowlists**—principle of least functionality
- **TLS 1.2+** for all MCP transport
- **Structured audit logging** without cleartext PHI (see `audit-logging-integrity`)
- **BAA coverage** for MCP operators processing ePHI (see `hipaa-baa-vendor-assessment`)

## When to Use

Use this skill when:

- **Deploying** new MCP servers for compliance workflows
- **Auditing** existing MCP configurations (scopes, tools, network placement)
- Implementing **OAuth 2.1 + PKCE** for MCP authorization
- Defining **tool sets** per role (auditor vs read-only vs emergency)
- Integrating **Playwright, Postgres, Slack, Presidio** MCP patterns from this repository
- **Incident response** for compromised MCP tokens or rogue tools

Do **not** use this skill when:

- Writing PCI script inventory logic (use `pci-dss-script-audit`—references Playwright MCP)
- Presidio entity tuning without MCP (use `hipaa-phi-redaction-pipeline`)
- Enterprise vendor risk programs without MCP (use `vendor-third-party-risk`)

## Core Process

Execute steps **in order**.

### Step 1: MCP server inventory

1. List all MCP servers connected to compliance agent:

| Server | Package/source | Data sensitivity | Operator |
| --- | --- | --- | --- |
| Playwright | `@playwright/mcp` | URLs, DOM (may contain PHI in page) | Self/hosted |
| Postgres | Official/community postgres MCP | Query results (PHI/CDE risk) | Self/hosted |
| Slack | Slack MCP | Messages (notification only) | Vendor |
| Presidio | Custom/REST wrapper | Raw text (PHI) | Self/hosted |

2. Document version, deployment location, network zone, BAA status.
3. Artifact: `mcp-inventory-{id}.json`.

### Step 2: OAuth 2.1 and PKCE configuration

1. Register OAuth client per MCP server with:
   - **Exact redirect URI** allowlist (no wildcards)
   - **Authorization code flow** with **PKCE S256** (OAuth 2.1 requirement)
   - **Short-lived access tokens** (≤1 hour) and refresh token rotation
2. Prohibit implicit flow and password grant.
3. Bind tokens to **audience** (specific MCP server resource identifier).
4. Test: authorization without PKCE challenge → **must fail**.

### Step 3: Tool set design (least functionality)

For each MCP server, define **role-based tool sets**:

#### Playwright MCP pattern (PCI 6.4.3 / 11.6.1)

- **Allowed tools**: `browser_navigate`, `browser_snapshot`, `browser_take_screenshot`
- **URL allowlist**: payment page URLs only—block `file://`, internal IPs unless scoped
- **Prohibited**: arbitrary JavaScript execution beyond documented audit scripts
- **Evidence**: DOM snapshots stored with SHA-256; no PAN fields in stored HTML if avoidable

#### Postgres MCP pattern (baselines, evidence)

- **Read-only role** on `compliance` schema only
- **Prohibited**: `DROP`, `UPDATE`, production PHI/CDE tables
- **Parameterized queries** only; no arbitrary SQL from model without template allowlist
- **Row limits** on exports (e.g., max 10,000 rows)

#### Slack MCP pattern (SOC alerts)

- **Channel allowlist**: `#soc-alerts`, `#compliance-audit`—no DMs to personal accounts
- **Message template**: URL, diff summary, severity—**no raw ePHI or PAN**
- **Prohibited**: file uploads containing evidence bundles with PHI

#### Presidio MCP pattern (DLP)

- **Mirror** `redaction.py` entity types and thresholds
- **Process locally** where possible—avoid sending text to third-party Presidio SaaS without BAA
- **Do not log** input text in MCP server logs
- **Fail closed** if Presidio unavailable—agent must not bypass redaction

### Step 4: Transport and network security

1. Enforce **HTTPS/TLS 1.2+** for remote MCP; mTLS for sidecar deployments.
2. Place MCP servers in **dedicated subnet**; NSC rules per `pci-dss-network-segmentation`.
3. No MCP admin interfaces on public Internet without VPN/ZTNA.

### Step 5: Authentication and session binding

1. Map MCP OAuth identity to **agent session correlation_id**.
2. Revoke tokens on session end.
3. Service-to-service MCP: use workload identity (SPIFFE, cloud IAM)—not static API keys in `agent.py`.

### Step 6: Logging and monitoring

1. Log per tool invocation: `timestamp`, `actor`, `tool_name`, `resource`, `result`, `correlation_id`.
2. Exclude raw tool **arguments** containing PHI from logs—or encrypt at field level.
3. Alert on: new tool registered, auth failure spike, Postgres query outside allowlist.

### Step 7: Deployment and change control (CC8)

1. MCP server updates via CI/CD with `compliance-as-code-governance` policy scans.
2. Pin MCP server versions; hash container images.
3. Require approval for tool manifest changes.

### Step 8: Compliance testing

1. **Negative tests**:
   - Attempt disallowed URL in Playwright → deny
   - Attempt SQL write via Postgres MCP → deny
   - Attempt Slack post to non-allowlisted channel → deny
2. **Positive tests**: PCI script audit workflow end-to-end with evidence hashes.
3. Document results in `mcp-security-test-{id}.json`.

## Common Rationalizations

| Excuse the agent might generate | Required rebuttal |
| --- | --- |
| "MCP is local, OAuth is unnecessary overhead." | Local MCP still processes sensitive data—**authentication and tool allowlists** prevent lateral abuse from compromised agent. |
| "Postgres MCP needs write for convenience." | Write access to evidence DB must use **separate controlled pipeline**—not general MCP write tools. |
| "Slack alerts need full DOM for context." | Full DOM may contain **PHI/PAN**—send diff summaries and artifact IDs only. |
| "PKCE is optional for confidential clients." | OAuth 2.1 mandates PKCE for **all** clients—including confidential. |
| "We trust the model to pick safe tools." | Models are **not authorization layers**—enforce tool sets server-side. |
| "Presidio MCP can fall back to no redaction." | Fail **closed**—unredacted PHI to LLM is a critical violation. |

## Red Flags

- MCP server accepts connections without authentication
- Postgres MCP connected to production CDE or clinical database
- Playwright MCP without URL allowlist (arbitrary navigation)
- Slack MCP posting evidence with cleartext PHI
- OAuth redirect URI wildcard (`https://*.example.com/callback`)
- MCP server logs store full tool arguments
- New MCP tool added without change ticket and security review

## Verification

- [ ] MCP inventory complete with operator, version, zone, and BAA status
- [ ] OAuth 2.1 + PKCE configured and negative-tested (no PKCE fails)
- [ ] Role-based tool sets documented and enforced server-side
- [ ] Playwright URL allowlist configured for payment audit URLs only
- [ ] Postgres MCP read-only on compliance schema; write paths prohibited
- [ ] Slack MCP restricted to allowlisted channels with PHI-free templates
- [ ] Presidio MCP aligned with redaction.py; fail-closed tested
- [ ] TLS/mTLS and network segmentation verified
- [ ] Tool invocation audit logs configured without cleartext PHI arguments
- [ ] Negative and positive security tests completed with hashed evidence
