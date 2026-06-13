# Regulatory Findings Report — SOC 2 Type II — CC6 logical access (Q2 2026)

**Report ID:** RPT-2026-SOC2-001  
**Engagement:** ENG-2026-SOC2-Q2  
**Framework:** SOC2-TSC  
**Period:** 2026-04-01 – 2026-06-30  
**Classification:** confidential  
**Prepared:** 2026-06-13 by compliance-agent-skills (synthetic example)

> **Disclaimer:** Synthetic example. Not a CPA attestation report.

## 1. Executive summary

**Overall posture:** Controls operating effectively (point-in-time)

Quarterly access review and policy artifacts packaged with SHA-256 manifest. One low finding on MFA exception documentation.


### Top risks

- **R-001** (low): MFA exception ticket missing approver field — _CC6.1_

### Limitations

- Sample-based IAM export; not full population
## 2. Scope recap

### In scope

- Identity provider (Okta synthetic export)
- Agent service accounts

### Out of scope

_Not specified._


### Data classifications

- confidential

## 3. Findings detail

| ID | Severity | Control | Observation | Recommendation | Status |
| --- | --- | --- | --- | --- | --- |
| F-001 | low | CC6.1 | One break-glass account exception lacks documented approver in ticket sample. | Enforce required approver field on MFA exception workflow. | open |

## 4. Evidence index

Manifest: `examples/soc2-evidence-bundle/evidence-manifest.yaml`

- `cc6-access-policy`
- `iam-export`

## 5. Remediation tracker

| Finding | Action | Owner | Due | Status |
| --- | --- | --- | --- | --- |
| F-001 | Update IdP exception workflow required fields | it-operations | 2026-07-30 | planned |

## 6. Methodology

- **Sampling:** 25-user IAM export sample; policy document review
- **Tools:** examples/soc2-evidence-bundle/hash_evidence.py
- **Redaction profile:** balanced
- **Deanonymize in report path:** False

## 7. Sign-off

- **Compliance Lead:** — (GRC Manager) — pending
- **Technical Lead:** — (IT Operations) — pending
