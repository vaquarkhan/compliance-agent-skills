---
name: hipaa-technical-safeguards
description: Implements HIPAA Security Rule technical safeguards (45 CFR §164.312)—access control, audit controls, integrity, person/entity authentication, and transmission security—for AI agents, MCP servers, and LLM pipelines. Trigger when assessing ePHI handling in agent architectures, MCP tool authorization, encryption in transit/at rest, or mapping HIPAA controls to technical implementations. Do not use for BAA legal review (use hipaa-baa-vendor-assessment) or Presidio tokenization setup (use hipaa-phi-redaction-pipeline).
---

# HIPAA Technical Safeguards

## Overview

This skill implements the **HIPAA Security Rule Technical Safeguards** at 45 CFR **§164.312**:

| Standard | Regulation | Agent/MCP focus |
| --- | --- | --- |
| Access control | §164.312(a)(1) | Unique user IDs, emergency access, automatic logoff, encryption/decryption |
| Audit controls | §164.312(b) | Tamper-evident logs of ePHI access via agents and MCP tools |
| Integrity | §164.312(c)(1) | Mechanisms to authenticate ePHI is not improperly altered or destroyed |
| Person or entity authentication | §164.312(d) | Verify identity of persons/systems accessing ePHI |
| Transmission security | §164.312(e)(1) | Integrity controls and encryption for ePHI in transit to LLMs and MCP |

AI agents introduce novel attack surfaces: tool calls may exfiltrate ePHI, MCP servers may log prompts, and LLM providers may process data outside BAA coverage. This skill produces a **control-by-control assessment** with evidence, not generic "HIPAA checklist" advice.

## When to Use

Use this skill when:

- Designing or auditing an **AI agent** that may touch ePHI
- Evaluating **MCP server** access to databases, files, or APIs containing PHI
- Reviewing **encryption** (TLS 1.2+, at-rest) for agent-to-LLM and agent-to-MCP paths
- Mapping **§164.312** implementation specifications (required vs addressable) to your stack
- Assessing **audit logging** for agent sessions and tool invocations
- Validating **authentication** (OAuth 2.1, MFA, service accounts) for ePHI systems

Do **not** use this skill when:

- Legal review of Business Associate Agreements (use `hipaa-baa-vendor-assessment`)
- Configuring Presidio redaction pipelines (use `hipaa-phi-redaction-pipeline`)
- PCI payment card data controls (use PCI skills)
- SOC 2 TSC mapping without HIPAA overlay (use `soc2-trust-services-criteria`)

## Core Process

Execute steps **in order**. Reference **45 CFR §164.312** explicitly in findings.

### Step 1: ePHI data flow inventory

1. Diagram all paths where ePHI may enter, transit, or exit the agent system:
   - User prompts, uploaded documents, MCP query results, LLM responses
   - Logging, monitoring, error reporting, third-party analytics
2. Classify each hop: **creates**, **reads**, **updates**, **transmits**, or **stores** ePHI.
3. Identify **Business Associates** at each hop (LLM vendor, cloud host, MCP operator).
4. Save artifact: `ephi-data-flow-{id}.json`.

### Step 2: Access control (§164.312(a)(1))

For each system component (agent runtime, MCP servers, LLM API, evidence store):

1. **Unique user identification (Required)**: Verify every human and service account has a unique ID; no shared credentials for ePHI access.
2. **Emergency access procedure (Required)**: Document break-glass accounts; verify logging and time-bound elevation.
3. **Automatic logoff (Addressable)**: Session timeout on agent consoles and MCP admin interfaces.
4. **Encryption and decryption (Addressable)**: At-rest encryption for evidence DB, prompt caches, MCP config secrets.

Record PASS/FAIL/ADDRESSABLE-GAP per implementation specification with evidence (IAM export, policy doc ID).

### Step 3: Audit controls (§164.312(b))

1. Verify **tamper-evident** audit logs capture:
   - Agent session start/end, user/service identity
   - MCP tool invocations (tool name, target resource, timestamp—not raw ePHI in logs unless encrypted)
   - ePHI access events (read/write scope)
   - Failed authentication attempts
2. Confirm log retention meets organizational policy (minimum 6 years for HIPAA-related records is common practice; cite org policy).
3. Test log integrity: append-only storage, WORM, or hash-chained logs.
4. Cross-reference `audit-logging-integrity` skill if SIEM integration is in scope.

### Step 4: Integrity (§164.312(c)(1))

1. Identify mechanisms preventing unauthorized alteration of ePHI:
   - Database constraints, checksums, digital signatures on exports
   - Version control for agent instructions/skills affecting ePHI handling
2. Verify agent **cannot modify source ePHI** via MCP unless explicitly authorized (least-privilege tool sets).
3. Document integrity verification for evidence artifacts (SHA-256 manifest).

### Step 5: Person or entity authentication (§164.312(d))

1. Verify all ePHI access paths require authentication:
   - Human users: MFA where accessing agent admin or deanonymization functions
   - Service-to-service: mTLS, OAuth client credentials, or signed JWTs
   - MCP servers: OAuth 2.1 + PKCE for user-delegated access (see `mcp-compliance-integration`)
2. Test: unauthenticated MCP or agent API calls must **fail closed**.

### Step 6: Transmission security (§164.312(e)(1))

1. **Integrity controls (Addressable)**: TLS with cert validation; reject downgrade; HSTS where applicable.
2. **Encryption (Addressable)**: ePHI encrypted in transit to LLM APIs, MCP endpoints, and evidence stores.
3. Verify **no ePHI in query strings**, referrer headers, or client-side logs.
4. Confirm PHI redaction gate runs **before** LLM transmission (`redaction.py` upstream of `compliance_agent.run`).

### Step 7: MCP-specific control matrix

For each connected MCP server, complete:

| Control | Test |
| --- | --- |
| Tool allowlist | Only approved tools enabled; no blanket `*` permissions |
| Scope limitation | Postgres MCP limited to compliance schema; no production PHI tables unless scoped |
| Logging | MCP access logged without logging raw ePHI |
| Transport | TLS 1.2+; cert pinning where supported |
| BAA | Vendor covered under executed BAA |

### Step 8: Findings and remediation

1. Map each gap to §164.312 implementation specification.
2. Distinguish **Required** vs **Addressable**—addressable gaps need documented risk analysis if not implemented.
3. Assign severity: CRITICAL (unencrypted ePHI to non-BAA LLM), HIGH (missing audit logs), MEDIUM (addressable not implemented without RA).

## Common Rationalizations

| Excuse the agent might generate | Required rebuttal |
| --- | --- |
| "PHI redaction replaces transmission encryption." | Redaction reduces exposure but **§164.312(e)** still requires integrity and encryption controls for any remaining ePHI in transit. |
| "MCP is internal, so authentication is optional." | Internal MCP servers processing ePHI require **§164.312(d)** authentication; network location is not a safeguard. |
| "Addressable means optional—we can skip it." | Addressable specifications require **documented risk analysis** if not implemented; they are not optional by default. |
| "Agent logs don't need HIPAA audit controls." | Any system that accesses ePHI needs **§164.312(b)** audit controls on that access. |
| "We'll add MFA later." | MFA gaps for ePHI admin access are **HIGH** severity until remediated with compensating controls documented. |
| "LLM vendor handles security; we don't assess transmission." | Covered entities remain responsible for **BAA-covered subprocessors** and transmission paths they configure. |

## Red Flags

- Raw ePHI sent to LLM API without redaction or BAA-covered encryption path
- MCP Postgres tool with read access to clinical/production PHI tables without scope restriction
- Shared service account used for agent and human ePHI access
- Audit logs stored in mutable files without integrity protection
- Deanonymization tool available without authentication
- ePHI in Slack/email alerts from agent or MCP monitoring
- No risk analysis documented for waived addressable implementations

## Verification

- [ ] ePHI data flow diagram completed for all agent/MCP/LLM hops
- [ ] §164.312(a) access control assessed for each implementation specification
- [ ] §164.312(b) audit controls verified with sample log queries and retention policy
- [ ] §164.312(c) integrity mechanisms documented and tested
- [ ] §164.312(d) authentication tested (unauthenticated access fails)
- [ ] §164.312(e) transmission security verified (TLS, no ePHI in URLs/logs)
- [ ] MCP control matrix completed for every connected server
- [ ] Required gaps flagged CRITICAL/HIGH with remediation owners
- [ ] Addressable gaps have risk analysis reference or remediation plan
- [ ] Evidence artifacts hashed and stored with audit ID
