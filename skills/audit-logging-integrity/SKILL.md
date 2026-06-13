---
name: audit-logging-integrity
description: Designs and validates tamper-evident audit logging, SIEM integration, and log retention for HIPAA §164.312(b) audit controls, SOC 2 CC7.2/CC7.3, and PCI Req 10. Trigger when assessing agent/MCP audit trails, log tampering risks, centralized logging, or forensic readiness. Do not use for IAM permission reviews (use access-control-identity-audit) or breach notification workflows (use breach-incident-response).
---

# Audit Logging Integrity

## Overview

This skill ensures **audit logs are generated, protected, retained, and reviewable** per:

- **HIPAA §164.312(b)**: Audit controls—hardware, software, procedural mechanisms to record and examine activity in systems containing ePHI
- **SOC 2 CC7.2/CC7.3**: System monitoring, anomaly detection, security event analysis
- **PCI-DSS Req 10**: Log and monitor all access to network resources and cardholder data

AI agents and MCP servers must emit **structured, tamper-evident** audit events without logging raw ePHI/CHD in cleartext.

## When to Use

Use this skill when:

- Designing **agent session audit trails** (prompt metadata, tool calls, redaction counts)
- Validating **MCP server logging** (tool invocations, auth events)
- Integrating logs with **SIEM** (Splunk, Elastic, Datadog, Sentinel)
- Testing **log integrity** (append-only, WORM, hash chains)
- Preparing **PCI Req 10** or HIPAA audit control evidence
- Investigating **gaps** in security event review (daily log review, alerting)

Do **not** use this skill when:

- Identity access certification (use `access-control-identity-audit`)
- Breach customer notification letters (use `breach-incident-response`)
- Initial SOC 2 TSC mapping (use `soc2-trust-services-criteria`)

## Core Process

Execute steps **in order**.

### Step 1: Audit event inventory

1. List all systems requiring audit logs:
   - Agent runtime, MCP servers, IdP, cloud control plane, CDE/ePHI databases
   - Evidence store, deanonymization tool invocations
2. Define required events per system:

| System | Required events |
| --- | --- |
| Agent | session_start, session_end, skill_loaded, tool_called, redaction_count |
| MCP | oauth_token_issued, tool_invoke, auth_failure, config_change |
| IdP | login_success, login_failure, mfa_challenge, account_lockout |
| DB | query (metadata only), connection, privilege_change |

3. Artifact: `audit-event-catalog-{id}.json`.

### Step 2: Log content standards

1. Each event must include **minimum fields**:
   - `timestamp_utc`, `event_id`, `actor_id`, `action`, `resource`, `result`, `source_ip`, `correlation_id`
2. **Prohibited in logs** (or require field-level encryption):
   - Raw ePHI, PAN, CVV, secrets, full prompts with PHI
3. Acceptable alternatives:
   - Redacted prompt hash, token counts, resource IDs without patient identifiers
4. Verify agent logs `entity_count` from redaction, not original values.

### Step 3: Tamper evidence

1. Implement one or more:
   - **Append-only** log storage (S3 Object Lock, immutability flags)
   - **Hash chaining** per log batch (prev_hash in each entry)
   - **WORM** SIEM index with retention lock
2. Restrict log deletion to break-glass role with **dual control** and post-use review.
3. Test: attempt delete/modify historical log as standard admin → must **fail** or generate alert.

### Step 4: Centralization and SIEM integration

1. Forward all cataloged sources to SIEM within **24 hours** (PCI Req 10.3).
2. Normalize to common schema (ECS, CEF, or OCSF).
3. Configure parsers for agent/MCP JSON logs.
4. Verify **clock synchronization** (NTP) across sources—PCI Req 10.4.

### Step 5: Monitoring and review (CC7.3, PCI 10.6)

1. **Daily automated review** of security events (failed auth spikes, new MCP tools, deanonymize calls).
2. Alert thresholds documented with runbooks.
3. Sample weekly manual review with analyst sign-off for evidence.
4. Cross-link alerts to `breach-incident-response` playbooks.

### Step 6: Retention and availability

1. Define retention per regulation and policy:
   - HIPAA: often **6 years** for relevant documentation (org policy governs)
   - PCI Req 10.5: **12 months** minimum, 3 months immediately available
   - SOC 2: examination period plus auditor request window
2. Test log search performance for incident queries across retention window.

### Step 7: Agent/MCP forensic readiness

1. Verify `correlation_id` propagates: user session → agent run → MCP tool calls.
2. Test forensic reconstruction without raw PHI:
   - "Who invoked deanonymize_response at T?" → actor_id, justification ticket
3. Ensure MCP servers log **authorization decision** (allow/deny) per tool call.

### Step 8: Gap analysis and remediation

1. Map gaps to §164.312(b), CC7.x, Req 10.x.
2. Prioritize: missing deanonymize audit = CRITICAL; delayed SIEM ingest = HIGH.
3. Package test results and sample log exports (redacted) for evidence.

## Common Rationalizations

| Excuse the agent might generate | Required rebuttal |
| --- | --- |
| "We log full prompts for debugging." | Full prompts with ePHI in logs **violate minimum necessary** and create secondary PHI store—log metadata only. |
| "Application logs on disk are enough." | Disk logs without **tamper protection** fail integrity requirements—implement append-only or SIEM immutability. |
| "MCP is stateless, no logging needed." | MCP tool calls accessing ePHI/CDE are **audit-relevant events** under HIPAA and PCI. |
| "Weekly log review is sufficient." | PCI requires **daily** security log review (10.6.1)—SOC 2 CC7 expects systematic monitoring. |
| "Deanonymization is internal—no audit trail." | Re-identification of PHI is **high-risk**—mandatory logged with actor and authorization. |
| "SIEM ingestion delay is acceptable." | PCI 10.3 requires timely centralization—>24h delay is a finding. |

## Red Flags

- Deanonymize tool invocations not logged
- MCP auth failures not forwarded to SIEM
- Logs contain cleartext SSN, PAN, or clinical notes
- Standard admin can delete production SIEM indices
- Agent sessions lack correlation_id across tool calls
- No daily security log review process or evidence
- Clock skew >5 minutes between agent and SIEM timestamps

## Verification

- [ ] Audit event catalog complete for agent, MCP, IdP, and data systems
- [ ] Log field standards enforced—no raw ePHI/CHD in sample exports
- [ ] Tamper-evidence mechanism tested (modify/delete attempt fails or alerts)
- [ ] All sources forwarding to SIEM within PCI 24-hour requirement
- [ ] NTP/clock sync verified across logging infrastructure
- [ ] Daily automated security review configured with alert runbooks
- [ ] Retention policy documented and technically enforced (Object Lock/WORM)
- [ ] Correlation_id forensic test successfully traces session to MCP tools
- [ ] Deanonymization and privileged tool calls appear in audit samples
- [ ] Gap remediation plan mapped to HIPAA, SOC 2, and PCI requirements
