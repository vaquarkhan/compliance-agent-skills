# CCPA / CPRA Compliance Checklist

Use with skill `ccpa-cpra-privacy-rights`. California Civil Code §1798.100 et seq.

## Consumer rights

- [ ] Right to know — categories and specific PI collected
- [ ] Right to delete — verifiable deletion workflow
- [ ] Right to correct — inaccurate PI correction process
- [ ] Right to opt-out of sale/share (including cross-context behavioral advertising)
- [ ] Right to limit use of sensitive personal information
- [ ] Right to non-discrimination for exercising rights
- [ ] Global Privacy Control (GPC) honored as opt-out signal

## Notices and transparency

- [ ] Privacy policy updated for CPRA (retention, sale/share, sensitive PI)
- [ ] Notice at collection for each data category
- [ ] Cookie / tracking disclosure where applicable

## DSAR operations

- [ ] Intake channel (web form, email) documented
- [ ] Identity verification procedure (not excessive)
- [ ] 45-day response timeline with extension policy
- [ ] DSAR log with request ID, type, status, completion date
- [ ] Agent/LLM pipelines excluded from retaining raw DSAR identity in model logs

## Service providers and contractors

- [ ] Written contracts prohibit selling PI and limit use to specified purpose
- [ ] Subprocessor list maintained and disclosed
- [ ] LLM vendors classified (service provider vs third party)

## AI agent specifics

- [ ] PI minimization in prompts (parallel HIPAA minimum necessary)
- [ ] No training on consumer PI without opt-in where required
- [ ] Automated decision-making disclosures if applicable (§1798.185)

## Record keeping

- [ ] 24-month retention of consumer requests and responses
- [ ] Metrics: requests received, fulfilled, denied with reason

---

## Authoritative sources

- California Consumer Privacy Act (CCPA) as amended by CPRA: [California OAG CCPA](https://oag.ca.gov/privacy/ccpa)
- CPRA regulations: [California Privacy Protection Agency](https://cppa.ca.gov/)

## Provenance

| Field | Value |
|-------|-------|
| **Source document** | California CCPA/CPRA (Civil Code §1798.100 et seq.) |
| **Version / effective** | Current California statutes as of 2026-06-13 |
| **Last reviewed** | 2026-06-13 |
| **Reviewer** | Repository maintainer |
| **Next review due** | 2026-12-13 |
| **Notes** | Consumer rights and service-provider subset; not CPRA regulations text |
