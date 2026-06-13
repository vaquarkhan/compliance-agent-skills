# SOX IT General Controls Checklist

Use with skill `sox-itgc-audit`. COSO / PCAOB AS 2201 alignment.

## ITGC domains

### Access to programs and data

- [ ] User provisioning with approval workflow
- [ ] Role-based access aligned to job function
- [ ] Periodic access recertification (quarterly/semi-annual)
- [ ] Privileged access separately managed and logged
- [ ] Termination removes access within SLA (e.g., 24 hours)

### Program change management

- [ ] Change request, approval, and testing documented
- [ ] Segregation: developers cannot deploy to production unilaterally
- [ ] Emergency change process with post-implementation review
- [ ] Version control and release tags for financial system changes

### Program development

- [ ] SDLC with security and SOX control requirements
- [ ] UAT sign-off from business owner before production
- [ ] Migration controls for data affecting financial reporting

### Computer operations

- [ ] Batch job monitoring and failure alerting
- [ ] Backup and recovery tested
- [ ] Incident management for systems affecting IPE/ICFR

## Evidence for external auditors

- [ ] Control matrix linking ITGC to financial assertion risks
- [ ] Sample of 25+ access changes tested per audit period
- [ ] Sample of 25+ production changes tested
- [ ] No unmitigated deficiencies in scope of reliance

---

## Authoritative sources

- Sarbanes-Oxley Act Section 404: [SEC SOX summary](https://www.sec.gov/news/studies/sox404study.pdf)
- PCAOB AS 2201 (ICFR audit): [PCAOB standards](https://pcaobus.org/oversight/standards/auditing-standards)

## Provenance

| Field | Value |
|-------|-------|
| **Source document** | SOX §404 / PCAOB AS 2201 ITGC |
| **Version / effective** | Current PCAOB standards as of 2026-06-13 |
| **Last reviewed** | 2026-06-13 |
| **Reviewer** | Repository maintainer (pending CPA sign-off) |
| **Next review due** | 2026-12-13 |
| **Notes** | ITGC subset for financial reporting systems; not audit opinion |
