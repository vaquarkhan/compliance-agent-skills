---
name: glba-ffiec-financial-privacy
description: Implements Gramm-Leach-Bliley Act (GLBA) Safeguards Rule (16 CFR Part 314) and Privacy Rule (16 CFR Part 313) compliance aligned to FFIEC IT Examination Handbook modules for financial institutions—customer information protection, risk assessments, access controls, vendor oversight, and GLBA privacy notices (initial, annual, opt-out). Trigger when auditing banks, credit unions, fintech lenders, or insurance entities for GLBA Safeguards, preparing FFIEC cybersecurity examinations, reviewing customer information security programs, or harmonizing GLBA with state privacy laws. Do not use for California CPRA consumer rights alone (use ccpa-cpra-privacy-rights), PCI cardholder data controls (use pci-dss-encryption-key-management), or SOX 404 ITGC without GLBA customer information scope (use sox-itgc-audit).
---

# GLBA / FFIEC Financial Privacy

## Overview

This skill operationalizes **Gramm-Leach-Bliley Act (GLBA)** requirements for financial institutions and **non-bank financial companies** subject to FTC or federal functional regulator oversight, aligned to **FFIEC IT Examination Handbook** guidance.

| GLBA component | Regulation | Core obligation |
| --- | --- | --- |
| **Financial Privacy Rule** | 16 CFR **Part 313** (Regulation P) | Privacy notices, opt-out for information sharing with nonaffiliated third parties |
| **Safeguards Rule** | 16 CFR **Part 314** | Written information security program (WISP) protecting **customer information** |
| **Pretexting provisions** | 15 U.S.C. **§6821–6827** | Limit obtaining customer info under false pretenses (supporting controls) |

**Safeguards Rule** (amended 2021, effective 2023 phases) requires:

- **Qualified individual** overseeing the information security program
- **Risk assessment** identifying threats to customer information
- **Safeguards** matched to risk: access controls, encryption, MFA, secure development, logging, disposal
- **Service provider oversight** via contract and periodic assessment
- **Program evaluation** at least annually
- **Incident response plan** with notification where applicable

**Customer information** includes personally identifiable financial information provided by a consumer or obtained in connection with providing a financial product or service—not limited to deposit accounts (includes mortgage, lending, financial advisory, certain fintech).

**FFIEC IT Examination Handbook** modules (relevant cross-refs):

| Booklet | Application |
| --- | --- |
| **Information Security** | Governance, access, cryptography, logging |
| **Management** | Board oversight, risk appetite, audit |
| **Outsourcing Technology Services** | Vendor/cloud due diligence |
| **Business Continuity Management** | Resilience for customer data systems |
| **Audit** | Independent review of security program |

Cross-skill mapping: vendor oversight → `vendor-third-party-risk`; access controls → `access-control-identity-audit`; California resident overlap → `ccpa-cpra-privacy-rights`.

Reference documents: [FTC Safeguards Rule](https://www.ftc.gov/business-guidance/privacy-security/gramm-leach-bliley-act), [FFIEC Infobase](https://ithandbook.ffiec.gov/), 16 CFR Part 313 and Part 314.

## When to Use

Use this skill when:

- Auditing **GLBA Safeguards Rule** compliance for banks, credit unions, lenders, or fintech
- Preparing for **FFIEC IT examination** (state regulator or federal functional regulator)
- Developing or reviewing **Written Information Security Program (WISP)**
- Assessing **privacy notices** (initial, annual, revised) and **opt-out** processes under Regulation P
- Evaluating **service provider** contracts for customer information handling
- Harmonizing GLBA with **state privacy laws** (CPRA overlap for California customers)
- Reviewing **core banking, loan origination, or mobile banking** security controls

Do **not** use this skill when:

- CPRA-only consumer rights program without GLBA financial institution scope (use `ccpa-cpra-privacy-rights`)
- SOX 404 ITGC for public company financial reporting (use `sox-itgc-audit`)
- HIPAA-covered health plan PHI (use `hipaa-technical-safeguards`)
- PCI DSS cardholder data environment (use `pci-dss-network-segmentation`)

## Core Process

Execute steps **in order**.

### Step 1: Entity classification and regulatory mapping

1. Determine **GLBA applicability**:
   - Financial institution under GLBA §6801(b) or non-bank financial company under FTC jurisdiction
   - Identify **functional regulator**: OCC, FDIC, FRB, NCUA, SEC, state, or FTC
2. Map **customer information** data flows:
   - Core systems, CRM, mobile apps, call center recordings, cloud analytics
   - **Nonpublic personal information (NPI)** vs publicly available information
3. Identify **affiliates** and **nonaffiliated third parties** for Privacy Rule sharing analysis.
4. Artifact: `glba-data-inventory-{id}.json`.

### Step 2: Risk assessment (Safeguards Rule §314.4(b))

1. Conduct or review **written risk assessment** identifying:
   - Internal and external threats to customer information security, confidentiality, integrity
   - Likelihood and potential damage; criteria for evaluating risks
2. Update risk assessment upon **material operational changes** (new cloud core, API banking, AI chatbots).
3. Map risks to **safeguard categories** in §314.4(c): access controls, data inventory, encryption, secure development, authentication, monitoring, disposal.
4. Cross-ref `nist-csf-2-assessment` for structured risk taxonomy if institution uses CSF internally.

### Step 3: Written Information Security Program (WISP)

1. Verify WISP includes required elements per **16 CFR §314.4**:
   - Designated **qualified individual** (may be vendor CISO with board reporting line)
   - Risk assessment, safeguards, service provider oversight, evaluation, incident response
2. Board or senior management **approval** and annual review evidence.
3. Map WISP sections to FFIEC Information Security booklet expectations.
4. Artifact: `wisp-gap-analysis-{id}.md`.

### Step 4: Access controls and authentication (§314.4(c)(1), (c)(8))

1. Execute `access-control-identity-audit` with GLBA mapping:
   - Role-based access to customer information systems
   - **MFA** for access to customer information (Safeguards Rule explicit requirement)
   - Privileged access management for administrators and vendor support accounts
2. Verify **physical access** controls for facilities housing customer information (FFIEC PE expectations).
3. Test **session termination** and **encryption** for data in transit (§314.4(c)(3)).
4. Use **Postgres MCP** read-only for customer DB role assignments where permitted in audit scope.

### Step 5: Data inventory, encryption, and disposal (§314.4(c)(2)–(c)(4), (c)(7))

1. Maintain **inventory** of customer information systems, data classification, and retention.
2. Verify **encryption at rest** for customer information on portable media and in storage (risk-based where not feasible).
3. Verify **secure disposal** procedures for hardware, paper, and media sanitization.
4. Cross-ref `pci-dss-encryption-key-management` for key management patterns where encryption overlaps payment data.

### Step 6: Monitoring and logging (§314.4(c)(8))

1. Execute `audit-logging-integrity`:
   - Logging of access to customer information systems
   - Log review, retention, and protection from tampering
2. FFIEC expects **security event monitoring** and anomaly detection for internet-facing banking.
3. Use **Terraform MCP** for cloud logging infrastructure evidence (CloudTrail, Azure Activity Log).

### Step 7: Service provider oversight (§314.4(f))

1. Execute `vendor-third-party-risk` for all **service providers** receiving customer information:
   - Due diligence at selection; contract requiring security controls
   - Periodic assessment of service provider practices
2. Core processors, cloud hosts, SaaS CRM, LLM/chatbot vendors handling customer data in scope.
3. Verify contracts address **subcontractors**, **breach notification**, and **return/destruction** of data.
4. Distinguish **service provider** vs **joint arrangement** for Privacy Rule notice requirements.

### Step 8: Privacy Rule — notices and opt-out (16 CFR Part 313)

1. Review **initial privacy notice** at customer relationship establishment (§313.4).
2. Review **annual privacy notice** distribution requirements (§313.5)—delivery methods and content.
3. Verify **opt-out notice** and **reasonable opt-out methods** before sharing NPI with nonaffiliated third parties (§313.7, §313.10).
4. Map exceptions: **§313.14–313.15** (service provider, joint marketing, etc.)—document reliance basis.
5. For **California customers**, cross-ref `ccpa-cpra-privacy-rights` for CPRA rights that may exceed GLBA (do not assume GLBA preempts all CPRA obligations—coordinate with counsel).

### Step 9: Program evaluation, incident response, and evidence packaging

1. Verify **annual program evaluation** (§314.4(d)): internal audit, penetration test, or third-party review results.
2. Review **incident response plan** including customer notification triggers (state breach laws, regulator guidance).
3. Emit findings:

```yaml
id: FIND-GLBA-001
severity: HIGH
control_id: GLBA-314.4(c)(8)
observation: "MFA not enforced for all employees accessing loan origination system with customer NPI"
recommendation: "Deploy MFA for all interactive access; document exception process with risk acceptance"
owner: ""
due_date: null
status: open
```

4. Package: WISP, risk assessment, privacy notices, vendor assessments, access reviews, pen test summary, board minutes.
5. Hash evidence per `templates/audit-evidence-manifest.yaml`.

## Common Rationalizations

| Excuse the agent might generate | Required rebuttal |
| --- | --- |
| "We're a fintech partner bank handles compliance." | **GLBA applies to entities collecting customer information**—partner arrangements require contractual safeguards and often direct regulatory oversight. |
| "Privacy Rule allows sharing—no opt-out needed." | **Exceptions are narrow**—sharing outside §313.14/313.15 requires opt-out notice and reasonable opt-out methods. |
| "MFA is recommended, not required." | **2023 Safeguards Rule explicitly requires MFA** for access to customer information—absence is a regulatory gap, not best practice. |
| "Vendor SOC 2 replaces GLBA oversight." | §314.4(f) requires **periodic assessment**—SOC 2 review is evidence, not substitute for ongoing oversight program. |
| "CPRA preempts GLBA for California." | **GLBA and CPRA interaction is nuanced**—financial institutions may have GLBA-aligned exemptions for some CPRA provisions; assess per CPPA guidance with counsel. |
| "Annual privacy notice is obsolete—skip it." | Verify **current Regulation P delivery rules** and institution regulator expectations—many still require annual notice or alternative model compliance. |

## Red Flags

- No designated qualified individual or unclear reporting line to board/senior management
- Risk assessment missing or not updated after cloud core conversion
- Customer information accessible without MFA (employees or vendors)
- Service provider contracts lack security and breach notification clauses
- No inventory of systems storing customer NPI
- Privacy notices missing required Reg P content or opt-out methods
- Sharing NPI with marketing partners without opt-out compliance
- Logs of customer data access not reviewed or easily tampered with
- WISP not approved by senior management or board
- AI/chatbot vendor processes customer NPI without vendor oversight documentation

## Verification

- [ ] GLBA applicability and functional regulator identified
- [ ] Customer information data inventory and NPI flows documented
- [ ] Written risk assessment current and mapped to §314.4(c) safeguards
- [ ] WISP complete with qualified individual, board approval, annual review
- [ ] Access controls and MFA verified via access-control-identity-audit
- [ ] Encryption, disposal, and data inventory controls assessed
- [ ] Logging and monitoring verified via audit-logging-integrity
- [ ] Service provider oversight completed via vendor-third-party-risk
- [ ] Privacy notices (initial, annual) and opt-out processes reviewed per Part 313
- [ ] CPRA overlap assessed for California customers via ccpa-cpra-privacy-rights
- [ ] Annual program evaluation and incident response plan documented
- [ ] Evidence manifest complete with SHA-256 hashes and engagement ID
