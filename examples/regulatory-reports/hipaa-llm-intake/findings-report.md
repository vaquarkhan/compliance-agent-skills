# Regulatory Findings Report — HIPAA Security Rule — LLM intake pipeline assessment

**Report ID:** RPT-2026-HIPAA-001  
**Engagement:** ENG-2026-LLM-001  
**Framework:** HIPAA-Security-Rule  
**Period:** 2026-01-01 – 2026-06-30  
**Classification:** confidential  
**Prepared:** 2026-06-13 by compliance-agent-skills (synthetic example)

> **Disclaimer:** Synthetic example report. Not legal advice or OCR attestation.

## 1. Executive summary

**Overall posture:** Gaps identified — remediation required

Point-in-time review of the LLM agent gateway handling potential ePHI found Presidio redaction active upstream with opt-in deanonymization. Two medium findings require remediation before production attestation.


### Top risks

- **R-001** (high): Deanonymize flag enabled in non-production config drift — _45 CFR §164.312(a)(1)_
- **R-002** (medium): BAA gap for LLM subprocessors not fully documented — _45 CFR §164.308(b)(1)_

### Limitations

- Synthetic corpus only; no production log sampling
- SME legal review of checklist mappings pending
## 2. Scope recap

### In scope

- LLM Agent Gateway (agent.py)
- Presidio redaction gate (redaction.py)
- MCP Postgres evidence export

### Out of scope

- Legacy fax intake
- Production EHR direct integration

### Data classifications

- ePHI
- confidential

## 3. Findings detail

| ID | Severity | Control | Observation | Recommendation | Status |
| --- | --- | --- | --- | --- | --- |
| F-001 | high | §164.312(a)(1) | COMPLIANCE_AGENT_DEANONYMIZE documented in runbooks but no role-based gate tying flag to Privacy Officer approval workflow.
 | Require break-glass ticket ID in env var; log all deanonymize sessions to SIEM.
 | open |
| F-002 | medium | §164.308(b)(1) | Subprocessor list for MCP host missing from BAA exhibit B. | Execute BAAs and flow-down terms for all LLM/MCP vendors touching ePHI flows. | open |

## 4. Evidence index

Manifest: `examples/soc2-evidence-bundle/evidence-manifest.yaml`

- `art-redaction-config`
- `art-baa-register`

## 5. Remediation tracker

| Finding | Action | Owner | Due | Status |
| --- | --- | --- | --- | --- |
| F-001 | Implement deanonymize break-glass workflow and SIEM logging | security-engineering | 2026-07-15 | planned |
| F-002 | Complete BAA subprocessor exhibit for MCP/LLM vendors | privacy-office | 2026-08-01 | planned |

## 6. Methodology

- **Sampling:** Full review of redaction.py and agent.py; synthetic PHI corpus
- **Tools:** compliance_tests synthetic corpus, scripts/demo_agent.py
- **Redaction profile:** balanced
- **Deanonymize in report path:** False

## 7. Sign-off

- **Compliance Lead:** — (HIPAA Privacy Officer) — pending
- **Technical Lead:** — (Security Engineering Lead) — pending
