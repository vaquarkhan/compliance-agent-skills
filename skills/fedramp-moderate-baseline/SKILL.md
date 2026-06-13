---
name: fedramp-moderate-baseline
description: Implements FedRAMP Moderate baseline assessments using NIST SP 800-53 Revision 5 controls—authorization boundary definition, System Security Plan (SSP), Plan of Action and Milestones (POA&M), and continuous monitoring (ConMon)—with Cloud Service Provider (CSP) and agency customer responsibility matrices. Trigger when preparing FedRAMP authorization packages, assessing cloud offerings for federal customers, mapping 800-53 Rev 5 controls to CSF outcomes, or auditing ConMon deliverables (monthly POA&M, annual assessments). Do not use for CMMC/CUI defense contractor assessments (use cmmc-nist-800-171), SOX ITGC financial reporting controls (use sox-itgc-audit), or generic CSF gap analysis without FedRAMP artifacts (use nist-csf-2-assessment).
---

# FedRAMP Moderate Baseline

## Overview

This skill implements **FedRAMP Moderate** authorization readiness and assessment workflows aligned to **NIST SP 800-53 Revision 5** (September 2020, updated per FedRAMP baselines). FedRAMP Moderate applies to cloud systems where loss of confidentiality, integrity, or availability would have **serious adverse effect** on agency operations.

| Artifact | Purpose | Primary reference |
| --- | --- | --- |
| **Authorization boundary** | Defines system components, data flows, and trust zones | FedRAMP SSP Section 9; NIST SP 800-37 Rev 2 |
| **System Security Plan (SSP)** | Documents control implementation per 800-53 Rev 5 | FedRAMP SSP template (Moderate baseline) |
| **Security Assessment Plan (SAP)** | Defines assessor test procedures | FedRAMP SAP template |
| **Security Assessment Report (SAR)** | Documents findings and risk | FedRAMP SAR template |
| **POA&M** | Tracks deficiencies, milestones, risk ratings | FedRAMP POA&M template |
| **ConMon** | Ongoing vulnerability scanning, POA&M updates, annual assessment | FedRAMP ConMon Strategy Guide |

**Moderate baseline** includes approximately **323 controls** from NIST SP 800-53 Rev 5 (including enhancements where applicable). Control families span AC, AU, AT, CM, CP, IA, IR, MA, MP, PE, PL, PS, RA, CA, SC, SI, SR, and others per FedRAMP baseline documentation.

**Responsibility split**:

| Party | Typical responsibilities |
| --- | --- |
| **CSP (Cloud Service Provider)** | Physical/data center security, hypervisor, platform controls, FedRAMP package maintenance, customer responsibility matrix |
| **Agency customer** | Identity federation configuration, data classification, endpoint protection for agency users, configuration within customer-managed layers (IaaS/PaaS/SaaS dependent) |
| **Leveraged authorizations** | Agency inherits CSP controls via FedRAMP ATO; must document **customer responsibility matrix (CRM)** gaps |

Cross-walk: FedRAMP controls map to **NIST CSF 2.0** outcomes—use `nist-csf-2-assessment` for executive profiles; this skill produces **FedRAMP-specific authorization artifacts**.

Reference documents: [FedRAMP.gov](https://www.fedramp.gov/), [NIST SP 800-53 Rev 5](https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final), [NIST SP 800-37 Rev 2](https://csrc.nist.gov/publications/detail/sp/800-37/rev-2/final).

## When to Use

Use this skill when:

- **Preparing or reviewing** a FedRAMP Moderate authorization package (SSP, SAP, SAR, POA&M)
- Defining or validating the **authorization boundary** for a cloud offering (SaaS, PaaS, IaaS)
- Assessing **CSP vs agency customer** control inheritance and CRM completeness
- Auditing **continuous monitoring** deliverables (monthly ConMon, annual assessment, significant change requests)
- Mapping **800-53 Rev 5** control implementations for federal sales or ATO inheritance
- Harmonizing FedRAMP controls with existing **IAM** and **logging** programs

Do **not** use this skill when:

- CMMC Level 2 / NIST SP 800-171 for CUI in defense supply chain (use `cmmc-nist-800-171`)
- SOX IT general controls for financial reporting (use `sox-itgc-audit`)
- PCI CDE or cardholder data environments (use `pci-dss-network-segmentation`)
- HIPAA BAA vendor legal review without FedRAMP scope (use `hipaa-baa-vendor-assessment`)

## Core Process

Execute steps **in order**.

### Step 1: Authorization boundary and system categorization

1. Document **FIPS 199** security categorization (confidentiality, integrity, availability impact levels)—Moderate typically **Moderate/Moderate/Moderate** or equivalent.
2. Draw authorization boundary diagram:
   - CSP-managed infrastructure, tenant isolation, managed services
   - Customer-managed components (IdP federation, endpoints, custom configs)
   - External interfaces: API gateways, FedRAMP-approved interconnections
3. Identify **leveraged services** (e.g., AWS GovCloud, Azure Government) with existing FedRAMP authorizations.
4. Artifact: `fedramp-boundary-{id}.json` with component inventory and data flow descriptions.

### Step 2: Control baseline selection and CRM

1. Load **FedRAMP Moderate baseline** control list (800-53 Rev 5).
2. For each control, assign implementation status per CRM:
   - **CSP inherited**, **CSP fully responsible**, **Customer responsible**, **Shared**, **Not applicable** (with justification)
3. Priority families for cloud audits:
   - **AC** (Access Control) → `access-control-identity-audit`
   - **AU** (Audit and Accountability) → `audit-logging-integrity`
   - **IA** (Identification and Authentication)
   - **SC** (System and Communications Protection)
   - **SI** (System and Information Integrity)
   - **CA** (Assessment, Authorization, and Monitoring)
4. Artifact: `crm-matrix-{id}.csv` linked to SSP Part C.

### Step 3: SSP development or gap review

1. For each in-scope control, document per FedRAMP SSP format:
   - Control description and responsible role
   - Implementation narrative (how, not just policy reference)
   - **Implementation status**: Implemented, Partially Implemented, Planned, Alternative Implementation, Not Applicable
2. Cross-reference **NIST SP 800-53A Rev 5** assessment procedures for testability of narratives.
3. Validate **AI/agent components** if in boundary:
   - LLM API data handling, MCP tool scopes, logging of automated decisions
   - Map to AC-3, AU-2, AU-12, SI-4, SR controls
4. Use **Terraform MCP** (`mcp/terraform.mcp.json`) for IaC evidence supporting SC and CM families.

### Step 4: Access control and identity (AC, IA families)

1. Execute `access-control-identity-audit` Steps 1–5 against FedRAMP AC/IA control mapping:
   - AC-2 (Account Management), AC-3 (Access Enforcement), AC-6 (Least Privilege)
   - IA-2 (Identification and Authentication), IA-5 (Authenticator Management)
2. Verify **PIV/CAC federation** or approved alternative for agency users where CRM assigns customer responsibility.
3. Verify **privileged access** (PAM), MFA, and service account governance for CSP operations staff.
4. Document findings with 800-53 control IDs (e.g., `AC-6(10)` for privileged function restrictions).

### Step 5: Audit logging and accountability (AU family)

1. Execute `audit-logging-integrity` against AU controls:
   - AU-2 (Event Logging), AU-3 (Content of Audit Records), AU-6 (Audit Review)
   - AU-9 (Protection of Audit Information), AU-11 (Audit Record Retention)
2. Verify logs cover authorization boundary components; **centralized SIEM** with tamper protection.
3. Use **Postgres MCP** read-only queries for log retention configuration evidence where applicable.
4. Confirm **agency access** to audit records per CRM and AU-6 requirements.

### Step 6: Security assessment planning and testing

1. Build or review **SAP** with test cases mapped to 800-53A procedures.
2. Sampling methodology for Moderate: document population, sample size, pass/fail criteria.
3. Test categories:
   - **Technical**: vulnerability scans (authenticated), penetration testing per FedRAMP requirements
   - **Operational**: incident response tabletop, backup restoration
   - **Administrative**: policy review, training records, PS-3 personnel screening
4. Record results in SAR format with **risk ratings** (Low, Moderate, High per FedRAMP guidance).

### Step 7: POA&M management

1. For each deficiency, create POA&M entry:
   - Weakness description, risk level, milestones, scheduled completion date, responsible official
2. **Operational requirements**: update POA&M **at least monthly**; close items only with evidence of remediation.
3. Flag **high-risk open items** approaching milestone breach—escalate to authorizing official.
4. Artifact: `poam-{id}.yaml` aligned to FedRAMP POA&M template fields.

### Step 8: Continuous monitoring (ConMon)

1. Verify ConMon strategy implementation:
   - **Monthly**: OS/infrastructure/database vulnerability scanning; POA&M updates
   - **Annual**: full security assessment or continuous assessment approach per FedRAMP guidance
   - **Significant change requests (SCR)** for material architecture or control changes
2. Cross-ref `soc2-ccm-continuous-monitoring` for shared monitoring patterns (adapt to FedRAMP ConMon deliverables).
3. Integrate **threat intelligence** (SI-5), **configuration drift** detection (CM family)—`compliance-as-code-governance` for IaC drift scans.

### Step 9: Authorization decision support and evidence packaging

1. Prepare **authorization package** summary for AO/Authorizing Official Designated Representative (AODR):
   - Boundary, categorization, CRM, open POA&M risk summary, ConMon status
2. Map residual gaps to **NIST CSF 2.0** for executive reporting via `nist-csf-2-assessment` cross-walk table.
3. Package evidence with SHA-256 hashes per `templates/audit-evidence-manifest.yaml`.
4. Emit findings:

```yaml
id: FIND-FEDRAMP-001
severity: HIGH
control_id: AU-6
observation: "No documented procedure for monthly review of privileged user audit logs"
recommendation: "Implement AU-6 review SOP with SIEM dashboard and sign-off records"
owner: ""
due_date: null
status: open
```

## Common Rationalizations

| Excuse the agent might generate | Required rebuttal |
| --- | --- |
| "We inherit FedRAMP from AWS/Azure, so no SSP needed." | **Leveraged authorization requires CRM**—customer must document inherited vs customer-implemented controls; inheritance is not blanket exemption. |
| "800-53 Rev 4 narratives still apply." | FedRAMP baseline is **800-53 Rev 5**—control IDs, enhancements, and assessment procedures changed; remap all references. |
| "POA&M items can stay open indefinitely with accepted risk." | FedRAMP requires **milestones and AO tracking**—permanent open POA&M without AO acceptance is authorization deficiency. |
| "ConMon is just vulnerability scanning." | ConMon includes **POA&M updates, inventory maintenance, incident reporting, significant change management**—not scans alone. |
| "Moderate baseline is the same as SOC 2 Type II." | Overlap exists but **FedRAMP artifacts, 800-53 Rev 5 baseline, CRM, and ConMon** are distinct—SOC 2 report does not substitute for SSP/SAR. |
| "Agency customer owns all access controls." | CRM defines split—**CSP must implement AC/IA for platform layers**; vague CRM is a common SAR finding. |

## Red Flags

- Authorization boundary excludes multi-tenant isolation components or LLM/MCP data processors
- CRM marks all controls "CSP inherited" without customer responsibility documentation
- SSP narratives cite policy titles without implementation evidence (AU, AC families)
- POA&M not updated within 30 days; high-risk items past milestone without AO approval
- Vulnerability scans missing authenticated credentials or scope gaps vs boundary
- No SCR process for major releases affecting security posture
- AU-9 audit log protection inadequate (customer or operator can alter own logs)
- 800-53 Rev 4 control references in current authorization package
- ConMon deliverables missing monthly cadence evidence

## Verification

- [ ] FIPS 199 categorization documented; authorization boundary diagram current
- [ ] FedRAMP Moderate baseline (800-53 Rev 5) control list loaded and scoped
- [ ] Customer Responsibility Matrix complete with inherited/shared/customer assignments
- [ ] SSP control narratives assessed for implementation status and testability
- [ ] AC/IA and AU families audited via access-control and audit-logging skills
- [ ] SAP/SAR test procedures executed with risk-rated findings documented
- [ ] POA&M current within 30 days with milestones and responsible officials
- [ ] ConMon strategy evidence: monthly scans, annual assessment, SCR process
- [ ] Cross-walk to nist-csf-2-assessment completed for executive gap reporting
- [ ] Evidence manifest complete with SHA-256 hashes and engagement ID
