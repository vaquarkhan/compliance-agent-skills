# FedRAMP Moderate Baseline Checklist

Use with skill `fedramp-moderate-baseline`. NIST SP 800-53 Rev 5 (Moderate baseline).

## Authorization package

- [ ] System Security Plan (SSP) current and approved
- [ ] Authorization boundary diagram (network, data flows, interconnections)
- [ ] Privacy Impact Assessment if PII processed
- [ ] Rules of Behavior signed by users
- [ ] Plan of Action and Milestones (POA&M) with risk ratings

## Control families (sample high-priority)

### Access Control (AC)

- [ ] AC-2 Account management (JML, periodic review)
- [ ] AC-3 Access enforcement (least privilege)
- [ ] AC-6 Least privilege
- [ ] AC-17 Remote access (MFA, encryption)

### Audit and Accountability (AU)

- [ ] AU-2 Audit events defined
- [ ] AU-3 Content of audit records
- [ ] AU-6 Audit review and analysis
- [ ] AU-9 Protection of audit information

### Configuration Management (CM)

- [ ] CM-2 Baseline configuration
- [ ] CM-6 Configuration settings (hardening benchmarks)
- [ ] CM-8 System component inventory

### Continuous monitoring

- [ ] Monthly POA&M updates
- [ ] Annual security assessment (3PAO or agency equivalent)
- [ ] Ongoing vulnerability scanning (monthly)
- [ ] Significant change notifications per FedRAMP guidance

## Cloud shared responsibility

- [ ] CSP vs customer control inheritance documented in SSP
- [ ] Customer-configurable controls tested (IAM, encryption keys, logging)

---

## Authoritative sources

- FedRAMP Program: [fedramp.gov](https://www.fedramp.gov/)
- NIST SP 800-53 Rev 5 (Moderate baseline): [NIST CSRC SP 800-53](https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final)

## Provenance

| Field | Value |
|-------|-------|
| **Source document** | FedRAMP Moderate baseline (NIST SP 800-53 Rev 5) |
| **Version / effective** | FedRAMP Rev 5 baseline (ongoing) |
| **Last reviewed** | 2026-06-13 |
| **Reviewer** | Repository maintainer (pending 3PAO/ISSO sign-off) |
| **Next review due** | 2026-12-13 |
| **Notes** | SSP/ConMon subset; not FedRAMP authorization |
