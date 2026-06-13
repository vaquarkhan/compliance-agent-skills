# /remediate — Remediation Planning

Draft actionable remediation for open audit findings.

## Prerequisites

- Findings from `/audit` with severity and control IDs
- Evidence gaps identified in `/evidence`

## Instructions

For each **open** finding:

1. **Root cause** — technical or process gap (1–2 sentences).
2. **Recommendation** — specific, actionable fix aligned to control requirement.
3. **Owner** — named role or individual.
4. **Due date** — based on severity:
   - CRITICAL/HIGH: 30 days
   - MEDIUM: 90 days
   - LOW: next audit cycle
5. **Verification** — how to re-test (link to skill step or test procedure).
6. **Status** — open → in_progress → closed.

## Output format

```yaml
remediation_plan:
  engagement_id: ENG-2026-001
  items:
    - finding_id: FIND-001
      owner: security-engineering
      due_date: "2026-07-13"
      action: "Add SRI hashes for all payment-page third-party scripts"
      verification: "Re-run pci-dss-script-audit Req 6.4.3 checklist"
      status: open
```

## Policy-as-code

Where applicable, link to `compliance-as-code-governance` — OPA policies, Terraform fixes, CI gates.

## Release guard

Open **HIGH** findings block releases via `hooks/release-guard.sh`.

## Next command

Proceed to `/report` after remediation plan is approved.
