---
name: us-state-privacy-laws
description: Implements comprehensive US state comprehensive privacy law assessments—Virginia VCDPA (Va. Code §59.1-575), Colorado CPA (C.R.S. §6-1-1301), Connecticut CTDPA, Utah UCPA, Texas TDPSA, Oregon OCPA, Montana MCDPA, Iowa ICDPA, Delaware DPDPA, New Jersey, and harmonized multi-state consumer rights programs—for agent/LLM data flows, opt-out, DSAR, and data protection assessments. Trigger when operating nationally beyond California CPRA, mapping state-by-state obligations, building unified US privacy programs, or auditing agent systems for VCDPA/CPA-style rights. Do not use for California-only CPRA (use ccpa-cpra-privacy-rights), HIPAA PHI (use hipaa-privacy-minimum-necessary), or EU GDPR (use gdpr-us-multinational).
---

# US State Privacy Laws

## Overview

After California CPRA, **comprehensive state privacy laws** form a patchwork of consumer rights, controller/processor roles, and assessment requirements. This skill operationalizes **multi-state compliance** for organizations processing US residents' personal data—including **agent prompts, MCP logs, and LLM vendor chains**.

| State | Law | Effective | Notable scope threshold |
| --- | --- | --- | --- |
| Virginia | **VCDPA** Va. Code §59.1-575 | 2023 | 100k consumers or 25k + 50% revenue from PI sale |
| Colorado | **CPA** C.R.S. §6-1-1301 | 2023 | 100k consumers or 25k + revenue from PI sale |
| Connecticut | **CTDPA** | 2023 | Similar to VCDPA |
| Utah | **UCPA** | 2023 | 100k consumers or 25k + 50% revenue from sale |
| Texas | **TDPSA** | 2024 | Broad—no revenue threshold; SBO threshold |
| Oregon | **OCPA** | 2024 | 100k consumers or 25k + 25% revenue from sale |
| Montana | **MCDPA** | 2024 | 50k consumers |
| Iowa | **ICDPA** | 2024 | 100k consumers |
| Delaware | **DPDPA** | 2025 | 35k consumers or 10k + 20% revenue from sale |
| New Jersey | **NJDPA** | 2025 | 100k consumers or 25k + revenue from sale |

**Harmonized rights** (most states): access, delete, correct, portability, opt-out of **targeted advertising**, **sale**, and **profiling** for significant decisions; **sensitive data** consent; **DPIA/assessment** for high-risk processing (varies by state).

Reference: `references/us-state-privacy-matrix.md`

## When to Use

Use this skill when:

- Operating **nationally** and need state-by-state gap analysis beyond California
- Building **unified US privacy program** (single notice, multi-state DSAR, GPC/opt-out)
- Agent/LLM systems process **state residents' PI** in prompts, embeddings, or analytics
- **Data protection assessments** required (Colorado, Virginia, Connecticut, etc.)
- **Universal opt-out** (Global Privacy Control, state-specific links) implementation review
- Vendor contracts for LLM/MCP need **processor** terms aligned to VCDPA/CPA
- **Texas TDPSA** small business exemption or SBO analysis

Do **not** use this skill when:

- California-only scope (use `ccpa-cpra-privacy-rights`—deeper CPRA detail)
- HIPAA-covered entity PHI workflows (HIPAA may preempt for PHI)
- EU data subjects (use `gdpr-us-multinational`)
- Breach notification only (use `hitech-breach-notification` or `breach-incident-response`)

## Core Process

Execute steps **in order**.

### Step 1: Applicability matrix

1. For each state in `references/us-state-privacy-matrix.md`, evaluate:
   - Consumer count thresholds
   - Revenue/sale thresholds
   - Exemptions: GLBA-covered, HIPAA-covered, FERPA, B2B employee data (varies)
2. Mark entity as **controller**, **processor**, or **third party** per state definitions.
3. Artifact: `templates/state-privacy-assessment.yaml` — applicability grid.

### Step 2: Data inventory for agent systems

1. Map PI categories in agent pipeline:
   - Prompts, session logs, MCP Postgres, Slack notifications, GitHub evidence
2. Flag **sensitive data** per state (biometric, geolocation, health, minors):
   - Health data in agent prompts may trigger **consent** even outside HIPAA
3. Identify **sale**, **share**, and **targeted advertising** (analytics SDKs, ad IDs in agent telemetry).

### Step 3: Consumer rights harmonization

Build **lowest-common-denominator + state overlays** program:

| Right | Harmonized approach | State overlays |
| --- | --- | --- |
| Access | 45-day response; secure portal | CO/VCDPA appeal process |
| Delete | Cascade to LLM vendor per contract | Document exceptions |
| Correct | Source-of-truth update + re-index | CT explicit right |
| Opt-out sale/targeted ads | GPC + "Your Privacy Choices" link | TX universal opt-out |
| Profiling opt-out | Agent automated decisions disclosure | CO, CT assessments |
| Sensitive PI | Opt-in consent before collection | UT narrower sensitive list |

1. **Do not** route DSARs through unredacted LLM—use Postgres MCP read-only queries.
2. Log in `templates/dsar-request-log.yaml` with state of residency field.

### Step 4: Privacy notices and transparency

1. **Privacy policy** must list states covered and rights per state (or unified section with state addenda).
2. **Notice at collection** for agent chat widgets—categories, purposes, retention, automated decision-making.
3. **Processor/subprocessor list** includes LLM and MCP vendors.

### Step 5: Data protection assessments (DPA)

States requiring DPIA/assessment for high-risk processing (e.g., CO CPA, VCDPA profiling, sensitive data):

1. Assess agent use cases: automated eligibility, health inferences, large-scale profiling.
2. Document: processing description, necessity, risks, mitigations (redaction gate, retention limits).
3. Cross-link `gdpr-us-multinational` if EU subjects also processed.

### Step 6: Processor contracts

1. LLM/MCP vendors as **processors**—contract must include:
   - Processing instructions, confidentiality, deletion/return, subprocessors, audit rights
2. Align to **Colorado/Virginia** mandatory terms where applicable.
3. Use `vendor-third-party-risk` for SOC report + state addendum review.

### Step 7: Universal opt-out and signals

1. Honor **Global Privacy Control (GPC)** where required (CO, CT, CA, MT, etc.).
2. Texas **universal opt-out mechanism** for sale/targeted advertising/sharing.
3. Agent telemetry: disable ad identifiers when opt-out flag set in session context.

### Step 8: Children's and sensitive data

1. Knowingly process **13–16** (varies) minors—parental consent states differ.
2. Sensitive PI in agent prompts requires **opt-in** in most comprehensive states.
3. Apply `hipaa-phi-redaction-pipeline` before LLM—state health PI ≠ HIPAA exempt path.

### Step 9: Enforcement readiness

1. Document AG notification contacts per state (breach may overlap `breach-incident-response`).
2. Maintain **30-day cure** awareness (repealed in some states—verify current law).
3. Evidence package for regulatory inquiry: data map, DPAs, DSAR logs, opt-out stats.

## Common Rationalizations

| Excuse | Rebuttal |
| --- | --- |
| "We're B2B—state laws don't apply." | Many laws exempt **pure B2B** contact PI but not **consumer** agent users—verify per state. |
| "CPRA covers us nationally." | CPRA is **California-only**; TX, VA, CO have independent obligations. |
| "LLM vendor is processor—we're fine." | Controller remains liable for **assessment, notice, and DSAR**—vendor contract must enable compliance. |
| "One privacy policy is enough." | State-specific **appeal rights, sensitive data, and TDPSA** disclosures may require addenda. |
| "Agent logs aren't personal data." | Prompts with names, emails, or IDs are **PI** under all comprehensive state laws. |

## Red Flags

- No state applicability analysis documented
- DSAR responses include other consumers' PI from shared agent logs
- Targeted advertising in agent SDK without opt-out
- Sensitive health PI in prompts without consent
- Texas operations without TDPSA SBO/threshold review
- No DPA for agent profiling use case in Colorado

## Verification

- [ ] State applicability matrix completed with thresholds and exemptions
- [ ] Agent/LLM data map includes PI categories and sensitive flags
- [ ] Harmonized consumer rights program with state overlays documented
- [ ] Privacy notices updated for multi-state rights and subprocessors
- [ ] Data protection assessments completed for high-risk agent processing
- [ ] Processor contracts reviewed for VCDPA/CPA mandatory terms
- [ ] GPC/universal opt-out implemented and tested
- [ ] DSAR log includes state residency and response deadlines
- [ ] Evidence retained for regulatory inquiry readiness
