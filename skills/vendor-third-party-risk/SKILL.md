---
name: vendor-third-party-risk
description: Performs third-party and vendor risk assessments for compliance programs—security questionnaires, SOC 2 report review, control inheritance, and ongoing monitoring—for LLM, cloud, MCP, and GRC tool vendors (Vanta/Drata alternative operational mindset). Trigger when onboarding vendors, annual vendor reviews, or assessing subprocessor risk for HIPAA, PCI, and SOC 2. Do not use for BAA clause legal analysis (use hipaa-baa-vendor-assessment) or MCP technical hardening (use mcp-compliance-integration).
---

# Vendor Third-Party Risk

## Overview

This skill implements **third-party risk management (TPRM)** for compliance programs—operating with the rigor of GRC platforms (Vanta, Drata, Secureframe) but **without assuming a specific vendor tool**. It complements `hipaa-baa-vendor-assessment` (legal BAA focus) with **operational security assessment**:

- Inherent/residual **risk scoring**
- **SOC 2 Type II report** review (bridge letters, subservice orgs)
- **Security questionnaire** mapping (SIG Lite, CAIQ, custom)
- **Continuous monitoring** of vendor status (breach news, certification expiry)
- **Control inheritance** decisions for SOC 2 carve-out reports

Applies to LLM providers, cloud hosts, MCP operators, observability SaaS, and identity providers.

## When to Use

Use this skill when:

- **Onboarding** a new vendor processing customer data, ePHI, or CHD
- **Annual vendor recertification** in compliance calendar
- Reviewing vendor **SOC 2 report** for subservice organization reliance
- Completing **security questionnaires** sent to/from vendors
- Assessing **LLM/AI vendor** risk beyond BAA (model security, logging, subprocessors)
- Building **vendor risk register** for SOC 2 CC9.2 and HIPAA §164.308(b)
- Evaluating **GRC automation tools** themselves as vendors

Do **not** use this skill when:

- Drafting BAA legal clause analysis (use `hipaa-baa-vendor-assessment`)
- MCP OAuth configuration (use `mcp-compliance-integration`)
- Internal employee access reviews (use `access-control-identity-audit`)

## Core Process

Execute steps **in order**.

### Step 1: Vendor tiering

1. Classify vendors by **inherent risk**:

| Tier | Criteria | Review depth | Examples |
| --- | --- | --- | --- |
| T1 Critical | ePHI/CHD processing, production access | Full assessment + SOC 2 + annual onsite/virtual | LLM with BAA, cloud prod, MCP host |
| T2 High | Confidential data, internal network access | SOC 2 + questionnaire | SIEM, IdP, ticketing |
| T3 Medium | Limited data, no prod access | Questionnaire + certification check | Marketing SaaS |
| T4 Low | No sensitive data | Lightweight attestation | Office supplies |

2. Document tier in vendor risk register.

### Step 2: Due diligence data collection

For each in-scope vendor, collect:

1. **SOC 2 Type II report** (≤12 months old) + bridge letter if gap period
2. **ISO 27001/SOC 1** if relevant to service type
3. Completed **security questionnaire** (map to TSC controls)
4. **Pen test summary** or redacted executive summary
5. **Subprocessor list** and change notification process
6. **Insurance** (cyber liability) certificates where required
7. For LLM vendors: data retention, training policy, region, incident history

Store with SHA-256 hashes; redact customer references if sharing internally.

### Step 3: SOC 2 report review methodology

1. Verify report scope covers **services in use** (not just corporate IT).
2. Review **exceptions** and **management responses**—unresolved exceptions = gap.
3. Map **subservice organizations** (carve-out vs inclusive):
   - Carve-out: obtain subservice SOC 2 and map to your CC9.2 monitoring
4. Check **period of time** covers full examination window needed.
5. Document **complementary user entity controls (CUECs)** you must implement.

### Step 4: Control mapping and gaps

1. Map vendor controls to your TSC/HIPAA/PCI requirements:

| Your control need | Vendor evidence | Gap? |
| --- | --- | --- |
| CC6.1 MFA | SOC 2 CC6.1 no exceptions | No |
| HIPAA encryption | BAA + SOC C1 | Verify region |
| PCI segmentation | Not in vendor scope | **You** implement |

2. Gaps become **compensating controls** or **remediation conditions** before production use.

### Step 5: Risk scoring

1. Calculate **inherent risk** (data sensitivity × access level × criticality).
2. Calculate **residual risk** after vendor controls and your CUECs.
3. Score 1–5 or Low/Med/High; T1 vendors with High residual risk **block production** until remediated.
4. Privacy officer / security committee approval for T1 High residual.

### Step 6: Contractual and operational requirements

1. Ensure contracts include:
   - Right to audit / SOC 2 delivery annually
   - Breach notification SLA (≤24–72 hours to you)
   - Subprocessor notification and objection rights
   - Data return/destruction at termination
2. For LLM: no training on customer data, zero retention option documented.
3. Cross-reference `hipaa-baa-vendor-assessment` for BAA execution.

### Step 7: Ongoing monitoring (continuous TPRM)

1. **Quarterly** for T1: recheck SOC 2 expiry, subprocessor changes, breach news (RSS, CISA).
2. **Annually** for T2–T3: full reassessment refresh.
3. Integrate with `soc2-ccm-continuous-monitoring`:
   - Alert on vendor certification expiry 90 days out
   - Auto-create reassessment ticket
4. Off-boarding: verify access revoked, data deleted, tokens rotated.

### Step 8: Risk register and reporting

1. Maintain vendor risk register: tier, score, last review, next review, open gaps.
2. Executive dashboard: T1 vendor health, overdue reviews, open findings.
3. Export evidence for SOC 2 CC9.2 and auditor requests.

## Common Rationalizations

| Excuse the agent might generate | Required rebuttal |
| --- | --- |
| "Big vendor is safe—skip questionnaire." | T1 vendors require **evidence-based** assessment regardless of brand—SOC 2 exceptions happen at scale vendors too. |
| "SOC 2 report from 2 years ago is fine." | Reports **>12 months** without bridge letter fail freshness standards for T1 vendors. |
| "Carve-out means we ignore subservice risk." | Carve-out shifts **monitoring obligation** to you (CC9.2)—obtain and review subservice SOC 2. |
| "Questionnaire completed by sales engineer is sufficient." | Security assessments require **validated** responses mapped to controls—not marketing answers. |
| "We use Vanta/Drata—they manage vendors." | GRC tools **orchestrate** workflows—you still own risk decisions and evidence quality. |
| "LLM vendor passed our pen test." | Your vendor pen test ≠ **their** production security—require their SOC 2 and subprocessors review. |

## Red Flags

- T1 vendor in production without current SOC 2 or equivalent
- Unresolved SOC 2 exceptions for controls you rely on
- Subprocessor added with ePHI access and no review within 90 days
- Vendor breach in news with no impact assessment documented
- Residual risk High with no committee approval
- Vendor access still active after contract termination
- Security questionnaire answers contradict SOC 2 report scope

## Verification

- [ ] All vendors tiered T1–T4 in risk register
- [ ] T1/T2 due diligence package complete (SOC 2, questionnaire, subprocessors)
- [ ] SOC 2 reports reviewed for scope, exceptions, period, and CUECs
- [ ] Control gaps documented with compensating controls or blockers
- [ ] Inherent and residual risk scores calculated with approval for high residual T1
- [ ] Contractual security clauses verified (audit rights, breach SLAs, termination)
- [ ] BAA cross-reference completed for ePHI vendors
- [ ] Ongoing monitoring schedule configured with expiry alerts
- [ ] Off-boarding checklist defined and tested for sample vendor
- [ ] Risk register exported with evidence hashes for SOC 2 CC9.2
