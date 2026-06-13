---
name: sox-itgc-audit
description: Performs Sarbanes-Oxley Act (SOX) IT General Controls (ITGC) audits aligned to COSO Internal Control—Integrated Framework and PCAOB AS 2201—covering access to programs and data, program change management, program development, and computer operations relevant to financial reporting systems. Trigger when preparing SOX 404 management assessment, supporting external auditor ITGC reliance, testing change tickets for financially relevant applications, or auditing segregation of duties in ERP and cloud financial systems. Do not use for FedRAMP authorization packages (use fedramp-moderate-baseline), PCI cardholder environments (use pci-dss-network-segmentation), or HIPAA ePHI controls without financial reporting scope (use hipaa-technical-safeguards).
---

# SOX IT General Controls Audit

## Overview

This skill implements **IT General Controls (ITGC)** testing for **Sarbanes-Oxley Act Section 404** management assessment of internal control over financial reporting (ICFR). ITGCs provide the **foundation** upon which automated application controls and manual controls depend.

| ITGC domain | Scope | Typical systems |
| --- | --- | --- |
| **Access to programs and data** | User provisioning, privileged access, SoD, password/MFA | ERP (SAP, Oracle), HCM/payroll interfaces, cloud IAM |
| **Program change management** | SDLC, change approval, testing, migration to production | Git repos, CI/CD, ERP transports, config changes |
| **Program development** | New system implementation, project governance | ERP rollouts, custom report development |
| **Computer operations** | Batch jobs, backups, incident management, monitoring | Job schedulers, backup tools, SIEM alerts |

**Regulatory and professional framework references**:

| Source | Relevance |
| --- | --- |
| **SOX Section 404** (15 U.S.C. §7262) | Management assessment of ICFR; auditor attestation |
| **SEC Rule 13a-15 / 15d-15** | Management evaluation and disclosure requirements |
| **COSO 2013 Framework** | Control environment, risk assessment, control activities, information & communication, monitoring |
| **PCAOB AS 2201** | Audit of internal control over financial reporting integrated with financial statement audit |
| **PCAOB AS 2315** | Audit sampling for ITGC testing |

**Key principle**: ITGC deficiencies rated **deficiency**, **significant deficiency**, or **material weakness** based on **likelihood and magnitude** of misstatement to financial statements—not generic security severity alone.

Cross-skill mapping: access and logging domains leverage `access-control-identity-audit` and `audit-logging-integrity`; change automation leverages `compliance-as-code-governance`.

## When to Use

Use this skill when:

- **SOX 404** annual cycle: scoping financially relevant systems and testing ITGCs
- **External auditor** requests ITGC walkthroughs and sample testing for reliance
- Auditing **ERP/cloud financial** systems (Workday Financials, NetSuite, SAP S/4HANA)
- Reviewing **change management** for financially relevant applications and interfaces
- Assessing **segregation of duties (SoD)** in provisioning and developer access
- Evaluating **computer operations** controls for batch processing and backup/recovery
- Testing **CI/CD and IaC** changes affecting financial reporting infrastructure

Do **not** use this skill when:

- FedRAMP or federal cloud authorization (use `fedramp-moderate-baseline`)
- PCI-DSS payment card controls (use `pci-dss-script-audit`, `pci-dss-network-segmentation`)
- SOC 2-only audits without ICFR scope (use `soc2-trust-services-criteria`)
- GLBA Safeguards Rule for customer information at financial institutions (use `glba-ffiec-financial-privacy`)

## Core Process

Execute steps **in order**.

### Step 1: SOX scoping and financial relevance

1. Identify **in-scope systems** using risk-based scoping:
   - Systems that **initiate, authorize, record, process, or report** financial transactions
   - Interfaces feeding general ledger, revenue recognition, inventory, payroll-to-GL
2. Document **locations and entities** (domestic, international) in scope for 404.
3. Classify applications:
   - **Tier 1**: Direct GL impact (ERP core modules)
   - **Tier 2**: Indirect or supporting (reporting warehouses, integration middleware)
4. Exclude non-financial systems with documented rationale and management sign-off.
5. Artifact: `sox-it-scope-{id}.json`.

### Step 2: COSO control environment and risk assessment

1. Walkthrough **Control Environment** (COSO principle 1–5):
   - Tone at top, board/audit committee oversight, organizational structure
   - HR policies, fraud risk factors, accountability for ITGC performance
2. Document **Risk Assessment** (principle 6–9) for IT changes and access—link IT risks to financial assertion risks (existence, completeness, accuracy, cutoff, authorization).
3. Identify **key reports** and **data used in controls** (parameter tables, master data) requiring ITGC coverage.
4. Note **management override** paths and monitoring controls.

### Step 3: Access to programs and data (ITGC Domain 1)

1. Execute `access-control-identity-audit` with SOX mapping:

| ITGC control objective | Test approach |
| --- | --- |
| New user provisioning | Sample hire tickets; verify approval and role assignment |
| User modification | Sample role changes; verify authorization |
| Termination | Sample terminations; verify **timely** deprovisioning (same-day standard) |
| Privileged access | Admin/super-user inventory; MFA; logging |
| Segregation of duties | SoD matrix; conflict reports (e.g., create vendor + approve payment) |

2. Test **application-layer** access separately from **OS/database** layers for Tier 1 systems.
3. Verify **periodic access recertification** by business owners (quarterly or per policy).
4. Use **Postgres MCP** read-only for role assignment queries where financial DB evidence resides.

### Step 4: Program change management (ITGC Domain 2)

1. Define **change population** for examination period: emergency, normal, infrastructure (IaC).
2. For each sample change affecting financial systems, verify:
   - **Request and approval** (change advisory board or equivalent)
   - **Development and testing** separate from production
   - **Migration authorization** and backout plan
   - **Post-implementation review** for significant changes
3. Cross-ref `compliance-as-code-governance`:
   - **GitHub MCP** (`mcp/github.mcp.json`) for PR approvals, branch protection, CI status checks
   - Terraform/IaC changes mapped to change tickets
4. **Emergency change** samples: verify retroactive approval and enhanced monitoring.
5. FAIL if unaudited direct production edits or developer standing prod access without compensating controls.

### Step 5: Program development (ITGC Domain 3)

1. For **new financially relevant implementations** in period:
   - Project charter, business case, steering committee oversight
   - Requirements sign-off, UAT with business users, conversion controls
   - Migration cutover checklist and hypercare support
2. Distinguish **major projects** (full SDLC testing) from **minor enhancements** routed through change management.
3. Verify **segregation**: developers lack production deploy rights without independent migration approval.

### Step 6: Computer operations (ITGC Domain 4)

1. Test **batch job** controls:
   - Job schedules, success/failure monitoring, restart procedures
   - Reconciliation of batch output to control totals where applicable
2. Test **backup and recovery**:
   - Backup success logs, periodic restore tests, RTO/RPO alignment with BCP
3. Execute `audit-logging-integrity` subset for **operations logging**:
   - Job failure alerts, privileged command logging, incident tickets
4. Verify **problem/incident management** links to change management when root cause requires fix.

### Step 7: IT-dependent manual controls and automated controls linkage

1. Identify **IT-dependent manual controls** (ITDMCs) relying on ITGCs (e.g., report parameters, user lists).
2. Map **automated application controls** (e.g., three-way match) to underlying ITGC prerequisites.
3. Document **compensating controls** where ITGC design gaps exist—must be evaluated by management and auditors for effectiveness.

### Step 8: Deficiency evaluation and SOX 404 reporting

1. Classify deficiencies per **PCAOB AS 2201** / company policy:
   - **Control deficiency**: design or operation failure
   - **Significant deficiency**: less severe than material weakness; important enough to merit attention
   - **Material weakness**: reasonable possibility of material misstatement not prevented/detected timely
2. Aggregate deficiencies—multiple low-risk access issues may combine to significant deficiency.
3. Prepare **management assessment** narrative: scope, methods, results, remediation plans.
4. Coordinate with **external auditors** on reliance: provide walkthrough docs, population definitions, sample selections.

### Step 9: Evidence packaging and remediation tracking

1. Emit findings with SOX/COSO context:

```yaml
id: FIND-SOX-001
severity: HIGH
control_id: SOX-ITGC-CHANGE-02
observation: "3 of 25 sampled ERP transports lacked independent migration approval"
recommendation: "Enforce dual approval workflow in change tool; remediate standing developer prod access"
owner: ""
due_date: null
status: open
```

2. Package: scope memo, walkthrough notes, sample workpapers, SoD reports, change tickets, access recertification exports.
3. Hash evidence per `templates/audit-evidence-manifest.yaml`.

## Common Rationalizations

| Excuse the agent might generate | Required rebuttal |
| --- | --- |
| "SOC 2 Type II covers SOX ITGCs." | SOC 2 CC6/CC8 overlap is **partial**—SOX requires **financial relevance scoping**, SoD matrices, and PCAOB sampling standards auditors accept. |
| "Developers need prod access for agile velocity." | Standing prod write access without **compensating controls** is a classic ITGC deficiency—use separate migration role with ticketed approval. |
| "Emergency changes don't need retroactive approval." | Emergency process **requires** documented retroactive review within defined SLA—missing retro approval fails change ITGC. |
| "Cloud IAM replaces application access controls." | **Both layers** must be tested—cloud admin access to financial DB without application SoD still risks unauthorized transactions. |
| "Access recertification is IT-only." | SOX expects **business owner attestation** of financial system access—not IT self-certification alone. |
| "Immaterial system—skip testing." | Scoping memo must document **exclusion rationale**; auditors may challenge systems feeding Tier 1 interfaces. |

## Red Flags

- Terminated employees with active ERP or financial reporting admin accounts
- Production changes deployed without tickets or with self-approval by developer
- SoD conflicts (create + approve same transaction type) without compensating monitoring
- No batch job failure alerting for GL close processes
- Backup restore never tested for financial database tier
- GitHub/terraform changes affecting financial infra without change record linkage
- Management override accounts without enhanced logging and periodic review
- ITGC walkthroughs not performed before detail testing (PCAOB expectation)
- Deficiencies closed without retest evidence in same SOX cycle

## Verification

- [ ] Financial relevance scoping documented with Tier 1/2 classification and sign-off
- [ ] COSO control environment and risk assessment walkthrough completed
- [ ] Access ITGCs tested: provisioning, modification, termination, privileged, SoD, recertification
- [ ] Change management samples verified for approval, testing, migration, emergency retro review
- [ ] Program development projects in scope assessed for SDLC and UAT controls
- [ ] Computer operations tested: batch monitoring, backup/restore, incident linkage
- [ ] ITDMC and automated control dependencies mapped to ITGC results
- [ ] Deficiencies classified (deficiency / significant deficiency / material weakness)
- [ ] External auditor reliance materials prepared (populations, samples, walkthroughs)
- [ ] Evidence manifest complete with SHA-256 hashes and engagement ID
