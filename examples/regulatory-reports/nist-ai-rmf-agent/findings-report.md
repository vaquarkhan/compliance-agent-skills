# Regulatory Findings Report — NIST AI RMF 1.0 — LLM agent deployment profile review

**Report ID:** RPT-2026-AIRMF-001  
**Engagement:** ENG-2026-AI-GOV-001  
**Framework:** NIST-AI-RMF  
**Period:** 2026-01-01 – 2026-06-30  
**Classification:** confidential  
**Prepared:** 2026-06-13 by compliance-agent-skills (synthetic example)

> **Disclaimer:** Synthetic example. Not NIST conformity assessment.

## 1. Executive summary

**Overall posture:** Gaps identified — remediation required

GOVERN/MAP profile complete for compliance agent; MEASURE TEVV corpus defined but production monitoring for hallucinated regulatory citations not yet automated.


### Top risks

- **R-001** (medium): No automated regression for skill citation drift — _NIST AI RMF MEASURE / TEVV_

### Limitations

- Self-assessment only; not third-party AI audit
## 2. Scope recap

### In scope

- compliance-agent-skills agent.py
- 30 Agent Skills library
- MCP tool integrations

### Out of scope

_Not specified._


### Data classifications

- ePHI (redacted upstream)
- confidential

## 3. Findings detail

| ID | Severity | Control | Observation | Recommendation | Status |
| --- | --- | --- | --- | --- | --- |
| F-001 | medium | MEASURE-TEVV | Skill validators run in CI but no scheduled production prompt regression against golden audit questions.
 | Add weekly TEVV job with fixed prompt corpus; alert on citation or step drift.
 | open |

## 4. Evidence index

Manifest: `templates/nist-ai-rmf-profile.yaml`

- `art-ai-rmf-profile`

## 5. Remediation tracker

| Finding | Action | Owner | Due | Status |
| --- | --- | --- | --- | --- |
| F-001 | Implement scheduled TEVV prompt regression in CI/CD | ai-risk-owner | 2026-08-15 | planned |

## 6. Methodology

- **Sampling:** Profile document review + CI validator output
- **Tools:** scripts/validate-skills.py, examples/nist-ai-rmf-profile/validate_profile.py
- **Redaction profile:** balanced
- **Deanonymize in report path:** False

## 7. Sign-off

- **Compliance Lead:** — (AI Risk Owner) — pending
- **Technical Lead:** — (ML Platform Lead) — pending
