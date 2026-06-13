---
name: cmmc-nist-800-171
description: Implements CMMC 2.0 Level 2 assessments aligned to NIST SP 800-171 Revision 2 (110 security requirements across 14 families) for Controlled Unclassified Information (CUI) protection in the Defense Industrial Base (DIB), including SPRS score self-assessment, POA&M management, and government contract flow-down obligations under DFARS 252.204-7012/7019/7020. Trigger when preparing for CMMC Level 2 certification, calculating SPRS scores, auditing CUI enclaves, or mapping 800-171 practices to cloud and on-prem implementations. Do not use for FedRAMP Moderate federal cloud authorization (use fedramp-moderate-baseline), SOX financial ITGCs (use sox-itgc-audit), or HIPAA PHI workflows (use hipaa-technical-safeguards).
---

# CMMC NIST SP 800-171 (Level 2)

## Overview

This skill implements **Cybersecurity Maturity Model Certification (CMMC) 2.0 Level 2** readiness aligned to **NIST SP 800-171 Revision 2** (*Protecting Controlled Unclassified Information in Nonfederal Systems and Organizations*, February 2020). Level 2 applies to contractors handling **CUI** and requires **110 security requirements** (including enhanced requirements from NIST SP 800-171A assessment objectives).

| CMMC 2.0 level | NIST alignment | Assessment type |
| --- | --- | --- |
| Level 1 | FAR 52.204-21 (17 practices) | Annual self-assessment |
| **Level 2** | **NIST SP 800-171 Rev 2 (110 practices)** | **Triennial C3PAO assessment** (priority acquisitions) or self-assessment per contract |
| Level 3 | NIST SP 800-172 (advanced) | Government-led assessment |

**CUI** is government-created or -owned information requiring safeguarding per **32 CFR Part 2002** and the **CUI Registry**. Contractual obligations flow from **DFARS 252.204-7012** (Safeguarding Covered Defense Information), **252.204-7019** (NIST SP 800-171 DoD Assessment), and **252.204-7020** (NIST SP 800-171 DoD Assessment Requirements).

**SPRS (Supplier Performance Risk System)** score:

- Submit self-assessment score to SPRS at [https://piee.eb.mil/](https://piee.eb.mil/) (PIEE)
- Score calculation: **−110 + (5 × MET) + (3 × NOT APPLICABLE)** per DoD methodology—document each practice status
- Minimum score expectations vary by solicitation; **110 MET** is target for full compliance

**14 NIST 800-171 requirement families**: AC, AT, AU, CM, IA, IR, MA, MP, PS, PE, RA, CA, SC, SI.

Cross-skill mapping: cloud and boundary patterns overlap `fedramp-moderate-baseline`; access and identity testing uses `access-control-identity-audit`.

Reference documents: [CMMC AB](https://cyberab.org/), [NIST SP 800-171 Rev 2](https://csrc.nist.gov/publications/detail/sp/800-171/rev-2/final), [NIST SP 800-171A](https://csrc.nist.gov/publications/detail/sp/800-171a/final) (assessment objectives).

## When to Use

Use this skill when:

- **Preparing for CMMC Level 2** C3PAO assessment or self-assessment per contract
- Calculating or validating **SPRS score** and POA&M for DoD contracts
- Defining **CUI boundary** (enclave) and marking/handling procedures
- Mapping **800-171 practices** to Microsoft GCC High, AWS GovCloud, or on-prem environments
- Responding to **DFARS 7012** incident reporting and cyber incident obligations
- Harmonizing CMMC with existing **FedRAMP inherited** or **commercial cloud** architectures

Do **not** use this skill when:

- FedRAMP Moderate SSP/POA&M for agency cloud ATO (use `fedramp-moderate-baseline`)
- SOX 404 ITGC for financial reporting (use `sox-itgc-audit`)
- PCI payment card environments (use `pci-dss-network-segmentation`)
- Export-controlled ITAR technical data without CUI scoping analysis (consult legal/export compliance)

## Core Process

Execute steps **in order**.

### Step 1: CUI scoping and enclave definition

1. Identify **CUI categories** from contract DD Form 254, contract clauses, and CUI Registry entries.
2. Define **CMMC assessment scope** (enclave):
   - Systems storing, processing, or transmitting CUI
   - Security Protection Assets (SPAs) supporting the enclave
   - Contractor Risk Managed Assets (CRMAs) if applicable per CMMC scoping guidance
3. Document **data flows**: email, file share, ERP, engineering (CAD/PLM), cloud SaaS, subcontractor portals.
4. Verify **CUI marking** per 32 CFR 2002 and DoD CUI marking handbook.
5. Artifact: `cui-enclave-boundary-{id}.json`.

### Step 2: Practice baseline and 800-171A assessment objectives

1. Load all **110 NIST SP 800-171 Rev 2** requirements.
2. For each practice, map **NIST SP 800-171A** assessment objectives (determine if MET, NOT MET, or N/A).
3. Status definitions:
   - **MET**: fully satisfied with evidence
   - **NOT MET**: gap requiring POA&M
   - **NOT APPLICABLE**: justified exclusion (document rationale; affects SPRS score)
4. Priority families for DIB environments:

| Family | Examples | Cross-skill |
| --- | --- | --- |
| AC | AC.L2-3.1.1–3.1.22 authorized access, remote access | `access-control-identity-audit` |
| IA | IA.L2-3.5.1–3.5.11 authenticator management | `access-control-identity-audit` |
| AU | AU.L2-3.3.1–3.3.9 audit records, review, protection | `audit-logging-integrity` |
| SC | SC.L2-3.13.1–3.13.16 boundary protection, crypto | `fedramp-moderate-baseline` (SC mapping) |
| IR | IR.L2-3.6.1–3.6.3 incident handling | `breach-incident-response` |

5. Artifact: `800-171-assessment-{id}.csv`.

### Step 3: SPRS score calculation and submission readiness

1. Calculate SPRS score using DoD formula; verify each practice scored consistently with evidence.
2. Prepare **System Security Plan (SSP)** or equivalent documentation per organization size—Level 2 expects documented implementation narratives.
3. Identify **minimum score** required by active solicitations; gap analysis if below threshold.
4. Document **assessment date**, **scope**, and **point of contact** for SPRS entry.
5. Plan **annual self-assessment** updates even when C3PAO certification is valid.

### Step 4: Access control and identification (AC, IA families)

1. Execute `access-control-identity-audit` with 800-171 mapping:
   - AC.L2-3.1.5 (least privilege), AC.L2-3.1.12 (monitoring remote access)
   - AC.L2-3.1.3 (control CUI flow), AC.L2-3.1.20 (external connections)
   - IA.L2-3.5.3 (MFA for privileged and network access)
2. Verify **local account** restrictions on enclave systems (AC.L2-3.1.1).
3. Test **session lock** and **encryption** for CUI at rest and in transit (SC family coordination).
4. Document **subcontractor** access paths and flow-down clauses (DFARS 7012 paragraph (m)).

### Step 5: Audit and accountability (AU family)

1. Execute `audit-logging-integrity` mapped to AU.L2-3.3.x:
   - Audit record content, retention, review, and protection
   - Time synchronization (AU.L2-3.3.7) via NTP configuration evidence
2. Verify **non-repudiation** for critical CUI access where required.
3. Use **Postgres MCP** or SIEM exports for log retention and review cadence evidence.

### Step 6: Configuration, system integrity, and boundary (CM, SI, SC families)

1. Verify **baseline configurations** (CM.L2-3.4.1–3.4.9): inventories, change control, security settings.
2. **Malware protection** (SI.L2-3.14.2–3.14.7): AV/EDR, updates, scans.
3. **Boundary protection** (SC.L2-3.13.1–3.13.16): firewalls, network segmentation, encryption.
4. Cross-ref `fedramp-moderate-baseline` Step 1 for boundary diagram patterns; adapt to CUI enclave (not full FedRAMP baseline).
5. Use **Terraform MCP** for IaC evidence of security group and encryption configurations.

### Step 7: Incident response and DFARS 7012 reporting

1. Verify **incident handling** (IR.L2-3.6.1–3.6.3) capability per `breach-incident-response`.
2. Document **72-hour** reporting obligation to DoD CIO for **cyber incidents** affecting covered defense information (DFARS 252.204-7012(c)).
3. Maintain **media preservation** and forensic procedures for CUI incidents.
4. Tabletop exercise evidence for IR plan within assessment period.

### Step 8: POA&M and remediation planning

1. For each NOT MET practice, create POA&M entry:
   - Weakness, risk, milestones, resources, scheduled completion
2. POA&M items **do not** count as MET for SPRS until remediated and reverified.
3. Prioritize: AC, IA, SC gaps affecting CUI exfiltration; IR gaps affecting 7012 compliance.
4. Artifact: `cmmc-poam-{id}.yaml`.

### Step 9: C3PAO readiness and evidence packaging

1. Organize evidence binder by 800-171 family:
   - Policies, procedures, screenshots, configs, interview notes, test results
2. Prepare personnel for **C3PAO assessor** interviews (PS, AT practices).
3. Cross-walk partial overlap to **FedRAMP CRM** if using authorized cloud—document inherited vs organizational controls.
4. Package with SHA-256 hashes per `templates/audit-evidence-manifest.yaml`.
5. Emit findings:

```yaml
id: FIND-CMMC-001
severity: HIGH
control_id: 3.5.3
observation: "MFA not enforced for non-privileged remote access to CUI enclave"
recommendation: "Enable MFA for all VPN and cloud console access to CUI systems per IA.L2-3.5.3"
owner: ""
due_date: null
status: open
```

## Common Rationalizations

| Excuse the agent might generate | Required rebuttal |
| --- | --- |
| "Commercial cloud is FedRAMP, so CMMC is automatic." | **FedRAMP ≠ CMMC**—contractor must implement 800-171 in tenant config; CRM/inheritance gaps are common C3PAO findings. |
| "SPRS score uses self-attestation—we can mark all MET." | **False attestation** risks False Claims Act exposure—each MET requires evidence per 800-171A objectives. |
| "CUI is only on one laptop—not in scope." | CUI on any contractor system triggers **enclave scoping**—unmarked/uncontrolled CUI expands assessment scope. |
| "POA&M items count toward certification." | Open POA&M means practice is **NOT MET** for SPRS until closed with verification. |
| "Subcontractor CUI is their problem." | DFARS **7012 flow-down** requires prime to verify subcontractor compliance—prime liability remains. |
| "Level 1 practices cover us for CUI." | CUI contracts require **Level 2 / 800-171**—17 FAR practices are insufficient for 110 requirements. |

## Red Flags

- CUI stored in commercial SaaS without BAA-equivalent/data protection agreement and encryption
- SPRS score submitted without documented 800-171A objective evidence
- No defined CUI enclave boundary; CUI mixed with FCI-only systems without segmentation
- Remote access to CUI without MFA (IA.L2-3.5.3)
- Missing DFARS 7012 incident reporting procedure or 72-hour contact list
- Audit logs modifiable by users being audited (AU.L2-3.3.8)
- POA&M older than 180 days with no milestone progress for high-risk gaps
- Subcontractor handling CUI without flow-down clause verification
- Assessment uses outdated NIST SP 800-171 Rev 1 control numbering

## Verification

- [ ] CUI categories identified; enclave boundary and SPA/CRMA scoping documented
- [ ] All 110 NIST SP 800-171 Rev 2 practices assessed against 800-171A objectives
- [ ] SPRS score calculated with MET/N/A/NOT MET documentation per practice
- [ ] AC/IA and AU families tested via access-control and audit-logging skills
- [ ] CM, SI, SC configuration and boundary evidence collected
- [ ] IR plan includes DFARS 7012 cyber incident reporting procedure
- [ ] POA&M current for all NOT MET practices with milestones
- [ ] Subcontractor flow-down and CUI marking procedures verified
- [ ] C3PAO evidence binder organized by family with interview readiness
- [ ] Evidence manifest complete with SHA-256 hashes and engagement ID
