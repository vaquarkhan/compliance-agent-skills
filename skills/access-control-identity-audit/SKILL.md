---
name: access-control-identity-audit
description: Audits identity and access management—least privilege, RBAC, MFA, privileged access, joiner-mover-leaver—for SOC 2 CC6.1–CC6.8, HIPAA §164.312(a), and PCI Req 7/8. Trigger when reviewing IAM policies, agent/MCP service accounts, access certifications, or admin console permissions. Do not use for network firewall segmentation (use pci-dss-network-segmentation) or tamper-evident logging design (use audit-logging-integrity).
---

# Access Control Identity Audit

## Overview

This skill performs **identity and access management (IAM) audits** mapped to:

- **SOC 2 CC6.1–CC6.8**: logical access, credential management, access removal
- **HIPAA §164.312(a)(1)**: access control implementation specifications
- **PCI-DSS Req 7**: restrict access to CHD by business need-to-know
- **PCI-DSS Req 8**: identify and authenticate users

AI agent deployments introduce **non-human identities**: MCP service accounts, LLM API keys, agent runtime roles, and deanonymization tools. These require the same rigor as human admin accounts.

## When to Use

Use this skill when:

- **Quarterly access reviews** or SOC 2 CC6.2/CC6.3 evidence collection
- Auditing **cloud IAM** (AWS IAM, Azure RBAC, GCP IAM) for least privilege
- Reviewing **MCP OAuth scopes** and agent tool permissions
- **Joiner-mover-leaver (JML)** process validation
- **MFA coverage** assessment for privileged and ePHI/CDE access
- Investigating ** excessive permissions** on service accounts running agents

Do **not** use this skill when:

- Network segmentation and firewall rules (use `pci-dss-network-segmentation`)
- BAA legal review (use `hipaa-baa-vendor-assessment`)
- Log integrity architecture (use `audit-logging-integrity`)

## Core Process

Execute steps **in order**.

### Step 1: Identity inventory

1. Export all identities from authoritative IdP and cloud IAM:
   - Human users, groups, roles
   - Service accounts, API keys, OAuth clients (MCP, agent, CI/CD)
2. Classify each identity:
   - **Human standard**, **Human privileged**, **Non-human service**, **Emergency break-glass**
3. Tag data access scope: **ePHI**, **CHD**, **Confidential**, **Public**
4. Artifact: `identity-inventory-{id}.csv`.

### Step 2: SOC 2 CC6 mapping

| Criterion | Audit action |
| --- | --- |
| CC6.1 | Logical access security software/infrastructure |
| CC6.2 | User registration and authorization before issuance |
| CC6.3 | User modification and removal on role change |
| CC6.4 | Access restrictions to confidential information |
| CC6.5 | Protection against unauthorized access during transmission/session |
| CC6.6 | System boundaries and segmentation (cross-ref network skill) |
| CC6.7 | Transmission, movement, removal restrictions |
| CC6.8 | Prevention of unauthorized software |

Document PASS/FAIL per criterion with evidence source.

### Step 3: Least privilege analysis

For each identity with ePHI, CHD, or admin access:

1. Export effective permissions (policy simulation, IAM analyzer).
2. Compare to **role baseline** (intended permission set).
3. Flag:
   - `*` actions on `*` resources
   - Unused permissions (90-day access advisor idle)
   - Direct user policies instead of group/role-based access
   - Shared API keys across multiple services
4. Severity: CRITICAL for CDE/PHI over-permission; HIGH for admin; MEDIUM for stale access.

### Step 4: MFA and authentication (PCI Req 8, HIPAA §164.312(d))

1. Verify MFA enforced for:
   - All privileged human accounts
   - Remote access to CDE/ePHI systems
   - Agent admin consoles and deanonymization functions
2. Verify service accounts use **key rotation**, **short-lived tokens**, or **workload identity**—not long-lived static keys in repos.
3. Test: password-only login to privileged console must **fail**.

### Step 5: MCP and agent-specific access

1. Inventory MCP server credentials:
   - OAuth clients: scopes, redirect URIs, PKCE requirement
   - Postgres MCP: DB roles, read-only vs write, schema limits
   - Playwright MCP: target URL allowlist, no arbitrary navigation
2. Inventory agent tools:
   - `deanonymize_response`: restricted to authorized roles
   - `redaction_status`: read-only, logged
3. Verify **no shared** agent runtime credential across prod and dev.

### Step 6: Joiner-mover-leaver validation

1. Sample HR-triggered access tickets (hire, transfer, terminate) from examination period.
2. Verify:
   - Provisioning within SLA with manager approval
   - Transfer: old permissions removed within SLA
   - Termination: **same-day** disable of all accounts and API keys
3. FAIL if terminated user retains MCP or cloud access.

### Step 7: Access certification (recertification)

1. Run quarterly certification campaign:
   - Managers attest direct reports' access
   - Service account owners attest non-human identities
2. Export certification completion rate; unreviewed accounts → revoke or escalate.
3. Store signed attestation for `soc2-evidence-collection`.

### Step 8: Remediation and evidence

1. Remediation priorities: CRITICAL revoked within 24h, HIGH within 7 days.
2. Package: IAM exports, MFA report, JML samples, certification exports, hashes.

## Common Rationalizations

| Excuse the agent might generate | Required rebuttal |
| --- | --- |
| "Service accounts don't need MFA." | Non-human identities need **equivalent controls**: workload identity, key rotation, scope limitation—not passwordless permanence. |
| "Admin needs *.* for emergencies." | Break-glass accounts must be **named, logged, time-bound**—standing admin *.* is a CC6.1 FAIL. |
| "MCP OAuth scopes are dev-only convenience." | Production MCP scopes are **in-scope** for CC6.4 and HIPAA access control. |
| "We'll remove terminated user access next week." | PCI/HIPAA/SOC 2 require **timely** deprovisioning—same-day is industry standard for termination. |
| "Access review is HR's job, not IT security." | CC6.3 requires **demonstrable** removal/modification process with evidence. |
| "API key in repo is fine if private." | Keys in git are **credential management failures** (CC6.1)—rotate and use secret manager. |

## Red Flags

- Terminated employee active in IAM or MCP OAuth sessions
- Deanonymization tool callable without role check
- Postgres MCP service account has SUPERUSER or write on PHI/CDE tables
- MFA optional for cloud root/admin accounts
- Shared long-lived API key for agent and CI pipeline
- Access certification completion below 95% with no revocation follow-up
- Break-glass account used without post-use review log entry

## Verification

- [ ] Complete identity inventory with human/non-human classification
- [ ] CC6.1–CC6.8 assessed with PASS/FAIL and evidence per criterion
- [ ] Least privilege analysis completed with over-permission findings prioritized
- [ ] MFA enforced and tested for all privileged and remote access paths
- [ ] MCP OAuth scopes and agent tool permissions documented and restricted
- [ ] JML sample validated with timely deprovisioning evidence
- [ ] Quarterly access certification completed or gaps flagged with revocation plan
- [ ] CRITICAL findings remediated or under emergency exception with expiry
- [ ] Evidence exports hashed and mapped to control IDs
- [ ] Service account key rotation policy verified (no stale keys >90 days)
