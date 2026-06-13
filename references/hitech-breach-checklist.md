# HITECH Breach Notification Checklist

Operational checklist for HITECH Act breach workflows. Not legal advice.

## Unsecured PHI

- [ ] PHI elements identified (types, volume, individuals)
- [ ] Encryption at rest/in transit assessed against NIST SP 800-111 or equivalent
- [ ] Key compromise evaluated—encryption safe harbor documented or rejected
- [ ] Paper/electronic media destruction status verified

## Four-factor risk assessment (45 CFR §164.402(2))

- [ ] Nature and extent of PHI documented
- [ ] Unauthorized recipient identified
- [ ] Acquisition/view evidence collected (logs, vendor attestation)
- [ ] Mitigation steps documented
- [ ] Privacy officer signed breach vs non-breach determination

## Notification timelines (from discovery)

- [ ] Individual notice: ≤60 calendar days (§164.404)
- [ ] HHS OCR: ≥500 → portal without unreasonable delay; <500 → annual log
- [ ] Media: >500 in state/jurisdiction → prominent outlets ≤60 days
- [ ] BA to CE: ≤60 days if BA discovered (§164.410)

## OCR portal data elements

- [ ] Covered entity / BA name and contact
- [ ] Breach discovery and occurrence dates
- [ ] Individuals affected count
- [ ] Types of unsecured PHI
- [ ] Safeguards in place before breach
- [ ] Description and mitigation
- [ ] Submission confirmation retained

## Business associates (LLM/MCP/cloud)

- [ ] BAA breach notification clause verified
- [ ] Subprocessor chain mapped
- [ ] Vendor deletion/retention certificates requested
- [ ] CE notification received with individual identifiers if known

## Penalty tier documentation (42 U.S.C. §1320d-5)

- [ ] Tier 1–4 analysis for management (unknowing → willful neglect)
- [ ] Corrective action plan with owners and dates

## Accounting of disclosures (§164.528)

- [ ] Disclosure log updated for affected individuals
- [ ] Agent/MCP log exports hashed and access-controlled

## Agent-specific

- [ ] `redaction.py` gate failure root cause documented
- [ ] `agent.py` deanonymize authorization audit trail reviewed
- [ ] MCP OAuth tokens revoked; rogue tools removed
- [ ] LLM vendor prompt retention status confirmed

---

## Authoritative sources

- HITECH Act breach notification: [45 CFR §164.400–414](https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-164/subpart-D)
- HHS OCR Breach Portal: [HHS Breach Reporting](https://ocrportal.hhs.gov/ocr/breach/wizard_breach.jsf)

## Provenance

| Field | Value |
|-------|-------|
| **Source document** | HITECH Act / HIPAA Breach Notification Rule |
| **Version / effective** | Current eCFR as of 2026-06-13 |
| **Last reviewed** | 2026-06-13 |
| **Reviewer** | Repository maintainer |
| **Next review due** | 2026-09-13 |
| **Notes** | Breach/OCR subset; use with breach-incident-response skill |
