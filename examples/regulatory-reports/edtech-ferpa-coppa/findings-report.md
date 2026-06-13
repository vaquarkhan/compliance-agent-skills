# Regulatory Findings Report — FERPA + COPPA — EdTech youth privacy combined review

**Report ID:** RPT-2026-EDTECH-001  
**Engagement:** ENG-2026-EDTECH-001  
**Framework:** multi  
**Period:** 2026-01-01 – 2026-06-30  
**Classification:** confidential  
**Prepared:** 2026-06-13 by compliance-agent-skills (synthetic example)

> **Disclaimer:** Synthetic example. Not FTC or ED official guidance.

## 1. Executive summary

**Overall posture:** Gaps identified — remediation required

School-official and VPC templates validated. Direct notice URL placeholder; parental consent log retention policy not yet operationalized.


### Top risks

- **R-001** (medium): COPPA direct notice not published at production URL — _16 CFR §312.4_
- **R-002** (low): FERPA disclosure log fields incomplete in MCP Postgres schema — _34 CFR §99.32_

### Limitations

- No under-13 user acceptance testing performed
## 2. Scope recap

### In scope

- EdTech tutoring agent (under-13 capable)
- templates/ferpa-school-official.yaml
- templates/coppa-parental-consent.yaml

### Out of scope

_Not specified._


### Data classifications

- education_records
- children_pi

## 3. Findings detail

| ID | Severity | Control | Observation | Recommendation | Status |
| --- | --- | --- | --- | --- | --- |
| F-001 | medium | COPPA-312.4 | Parent notice URL in template is placeholder; not reachable in staging. | Publish COPPA direct notice before child-directed features go live. | open |
| F-002 | low | FERPA-99.32 | MCP Postgres disclosure log missing recipient purpose field. | Align log schema with templates/ferpa-school-official.yaml fields. | open |

## 4. Evidence index

Manifest: `templates/ferpa-school-official.yaml`

- `art-coppa-notice`
- `art-ferpa-log-schema`

## 5. Remediation tracker

| Finding | Action | Owner | Due | Status |
| --- | --- | --- | --- | --- |
| F-001 | Publish COPPA direct notice at production URL | privacy-office | 2026-07-01 | planned |
| F-002 | Extend disclosure log schema with recipient and purpose | data-engineering | 2026-07-15 | planned |

## 6. Methodology

- **Sampling:** Template validation scripts + configuration review
- **Tools:** examples/ferpa-education-records/validate_ferpa_scope.py, examples/coppa-parental-consent/validate_consent.py
- **Redaction profile:** balanced
- **Deanonymize in report path:** False

## 7. Sign-off

- **Compliance Lead:** — (School Privacy Officer) — pending
- **Technical Lead:** — (EdTech Engineering) — pending
