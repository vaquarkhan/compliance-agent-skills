# Security Incident Runbook

## Purpose

Operational runbook for security incidents affecting HIPAA ePHI, PCI cardholder data, or SOC 2 in-scope systems—including AI agent and MCP-specific scenarios.

## Severity classification

| Level | Criteria | Response SLA |
| --- | --- | --- |
| **SEV-1** | Confirmed PHI/CHD exfiltration, production CDE compromise | 15 min |
| **SEV-2** | Suspected unauthorized MCP access, failed redaction gate | 1 hour |
| **SEV-3** | Policy violation, misconfigured tool scope | 4 hours |
| **SEV-4** | Informational anomaly | Next business day |

## Roles

- **Incident Commander (IC)** — coordinates response, declares SEV level
- **Privacy Officer** — HIPAA breach assessment, notification decisions
- **Forensics Lead** — log preservation, MCP session replay
- **Communications** — internal/external messaging (Legal approval required)

## Phase 1: Detect and triage (0–30 min)

1. Acknowledge alert in PagerDuty / Slack `#security-incidents`.
2. IC assigns roles; create incident ticket `INC-{YYYY}-{NNNN}`.
3. **Preserve evidence** — do not delete agent logs, MCP traces, or Presidio audit output.
4. Determine if **Presidio redaction was bypassed** (`redaction.py` session logs).
5. Classify severity; notify Legal/Privacy for SEV-1/2.

## Phase 2: Contain (30 min – 4 hr)

1. Revoke compromised MCP OAuth tokens and API keys.
2. Disable affected agent tools via policy-as-code emergency deny rule.
3. Block egress from suspected MCP servers at network layer if needed.
4. Snapshot relevant databases **read-only** — avoid destructive queries on evidence.

## Phase 3: Eradicate and recover

1. Patch root cause (misconfigured MCP scope, missing redaction hook, etc.).
2. Re-deploy with `compliance-as-code-governance` CI gates passing.
3. Validate PHI redaction with `examples/hipaa-phi-redaction/run_redaction.py`.
4. Monitor for recurrence 72 hours minimum.

## Phase 4: HIPAA breach assessment

If ePHI involved, Privacy Officer completes **four-factor risk assessment** within 24 hours.

- Document in `templates/breach-notification-plan.yaml`
- If breach confirmed: begin individual/HHS/media notification clocks

## Phase 5: Post-incident

1. Blameless postmortem within 5 business days.
2. Update skills/runbooks with lessons learned.
3. Tabletop exercise if SEV-1 or missed SLA.

## Agent/MCP-specific checks

- [ ] Were raw prompts logged before Presidio pass?
- [ ] Did `deanonymize_response` run on outputs stored in logs?
- [ ] MCP tool list match approved manifest (`mcp-compliance-integration`)?
- [ ] Playwright MCP used only on authorized checkout URLs?

## Contacts

| Role | Contact |
| --- | --- |
| Incident Commander | on-call rotation |
| Privacy Officer | privacy@example.com |
| Legal | legal@example.com |
| PCI QSA (retainer) | qsa@example.com |

## References

- Skill: `breach-incident-response`
- Template: `templates/breach-notification-plan.yaml`
- Hook: `hooks/audit-mode.sh`
