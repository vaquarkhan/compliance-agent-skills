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
