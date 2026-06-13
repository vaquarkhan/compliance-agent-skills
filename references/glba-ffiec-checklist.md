# GLBA Safeguards Rule and FFIEC Checklist

Use with skill `glba-ffiec-financial-privacy`. 16 CFR Part 314 (Safeguards), Part 313 (Privacy).

## GLBA Safeguards Rule (2023 updates)

- [ ] Qualified Individual designated for information security program
- [ ] Risk assessment covering customer information
- [ ] Safeguards designed and implemented to control identified risks
- [ ] Service provider oversight (contracts, due diligence)
- [ ] Program evaluation at least annually
- [ ] Incident response plan including customer notification where required

## Privacy Rule

- [ ] Initial privacy notice to customers
- [ ] Annual privacy notice (or exception criteria met)
- [ ] Opt-out for information sharing with non-affiliated third parties
- [ ] Accurate privacy notice reflecting actual practices

## FFIEC IT examination alignment

- [ ] Information security governance and board reporting
- [ ] Asset inventory including AI/agent systems processing customer data
- [ ] Encryption for data in transit and at rest
- [ ] Vendor management program
- [ ] Business continuity and disaster recovery tested

## Agent / fintech specifics

- [ ] Customer PI not sent to non-GLBA-compliant LLM providers
- [ ] Model outputs do not expose account numbers or authentication secrets
- [ ] Audit trail for automated decisions affecting customer accounts

---

## Authoritative sources

- Gramm-Leach-Bliley Act: [15 U.S.C. §6801 et seq.](https://www.ftc.gov/legal-library/browse/statutes/gramm-leach-bliley-act)
- FFIEC IT Examination Handbook: [FFIEC Infobase](https://ithandbook.ffiec.gov/)

## Provenance

| Field | Value |
|-------|-------|
| **Source document** | GLBA / FFIEC IT Handbook |
| **Version / effective** | Current statutes and FFIEC guidance as of 2026-06-13 |
| **Last reviewed** | 2026-06-13 |
| **Reviewer** | Repository maintainer |
| **Next review due** | 2026-12-13 |
| **Notes** | Safeguards Rule and agent subset; not regulatory examination |
