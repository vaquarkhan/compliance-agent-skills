---
name: gdpr-us-multinational
description: Implements GDPR compliance workflows for US-headquartered multinationals—EU/EEA/UK data subjects, Articles 5-7 lawful basis, Article 30 records of processing, Article 32 security, Articles 33-34 breach notification (72 hours), Article 35 DPIA, Standard Contractual Clauses, EU-US Data Privacy Framework adequacy, and DPA/subprocessor governance for agent/LLM cross-border transfers. Trigger when US companies process EU residents' data, deploying agents in EU regions, assessing LLM vendor international transfers, or preparing RoPA/DPIA for multinational privacy programs. Do not use for US state laws only (use us-state-privacy-laws or ccpa-cpra-privacy-rights), HIPAA PHI (use hipaa-technical-safeguards), or UK-only post-Brexit without EU scope (note UK GDPR parallels in references).
---

# GDPR for US Multinationals

## Overview

**General Data Protection Regulation (EU) 2016/679** applies to US companies when they **offer goods/services to EU/EEA data subjects** or **monitor their behavior**—regardless of US headquarters. Agent/LLM systems processing EU user prompts, support chat, or analytics fall in scope.

| GDPR topic | Article | US multinational focus |
| --- | --- | --- |
| Principles | **Art. 5** | Lawfulness, minimization, storage limitation for agent logs |
| Lawful basis | **Art. 6** | Consent vs legitimate interest for AI features |
| Special categories | **Art. 9** | Health, biometric in prompts—explicit consent or Art. 9(2) exception |
| Records of processing | **Art. 30** | RoPA must list LLM/MCP subprocessors and transfers |
| Security | **Art. 32** | Encryption, redaction gate, MCP access controls |
| Breach notification | **Art. 33-34** | **72 hours** to supervisory authority; data subject notice if high risk |
| DPIA | **Art. 35** | Required for systematic profiling, large-scale special categories |
| Transfers | **Art. 44-49** | SCCs, DPF, or adequacy for US LLM processing |
| DPO | **Art. 37-39** | Required for large-scale special category or systematic monitoring |
| Rights | **Art. 15-22** | Access, erasure, portability—LLM vendor deletion complexity |

**Transfer mechanisms (2024+):**

- **EU-US Data Privacy Framework (DPF)** — US entities self-certify; verify LLM vendor DPF status
- **Standard Contractual Clauses (2021 SCCs)** — Module 2 controller-processor for LLM vendors
- **UK IDTA / Addendum** — if UK data subjects included

Reference: `references/gdpr-article-checklist.md`, template `templates/gdpr-ropa-template.yaml`

## When to Use

Use this skill when:

- US company processes **EU/EEA (or UK) residents'** personal data in products or agents
- Assessing **cross-border transfers** to US-based LLM APIs (OpenAI, Anthropic, etc.)
- Building **Article 30 RoPA** including agent/MCP processing activities
- **DPIA** for agent profiling, automated decisions, or health-related prompts
- **72-hour breach notification** to lead supervisory authority (cross-border one-stop-shop)
- Drafting **DPA/SCCs** with LLM and MCP subprocessors
- **DPO consultation** on high-risk AI agent deployment in EU market

Do **not** use this skill when:

- US-only processing (use `us-state-privacy-laws`, `ccpa-cpra-privacy-rights`)
- HIPAA-covered PHI for US treatment/payment (HIPAA may apply; GDPR may also apply for EU patients—dual track)
- FedRAMP/CMMC without EU data (use respective skills)

## Core Process

Execute steps **in order**.

### Step 1: Territorial scope and roles

1. Confirm **Art. 3** applicability: EU establishment, offering goods/services to EU, or monitoring behavior.
2. Identify **controller**, **joint controller**, **processor** roles:
   - US SaaS with EU customers → typically **controller**
   - LLM API → **processor** (or subprocessor)
3. Determine **lead supervisory authority** (Art. 56) if main establishment in EU; US-only establishment → identify EU member state of most data subjects or first contact.
4. Artifact: scope JSON with establishment map.

### Step 2: Lawful basis (Art. 6)

For each agent processing activity, document lawful basis:

| Activity | Typical basis | Notes |
| --- | --- | --- |
| Customer support agent | Contract Art. 6(1)(b) | Necessary for service |
| Product analytics on prompts | Legitimate interest Art. 6(1)(f) | LIA required; opt-out where applicable |
| Marketing personalization agent | Consent Art. 6(1)(a) | Granular, withdrawable |
| Compliance audit agent | Legal obligation Art. 6(1)(c) | Document statute |

1. **Special category data (Art. 9)** in prompts—health, biometric: explicit consent or documented Art. 9(2) exception; default deny without basis.
2. Apply `redaction.py` **before** US LLM transfer as technical minimization (Art. 5(1)(c)).

### Step 3: Records of processing (Art. 30)

Populate `templates/gdpr-ropa-template.yaml`:

1. Processing activity name (e.g., "EU Customer Support Agent")
2. Purposes, categories of data subjects and personal data
3. Recipients including **US LLM subprocessors**
4. Transfers to third countries + safeguards (SCCs, DPF)
5. Retention periods; security measures (Art. 32 cross-ref)
6. **Do not** store raw special category data in RoPA—reference categories only.

### Step 4: International transfers (Chapter V)

1. Inventory transfers to **US** for LLM inference, logging, training:
   - Vendor DPF certification status ([DataPrivacyFramework.gov](https://www.dataprivacyframework.gov/))
   - If no DPF: execute **2021 SCCs** Module 2 (controller-processor) + UK Addendum if needed
2. **Transfer impact assessment (TIA)** for US surveillance laws post-Schrems II:
   - Supplementary measures: encryption in transit, redaction, contractual audit, data residency EU region if offered
3. MCP servers in US: document as subprocessor transfers.

### Step 5: Data subject rights (Arts. 15-22)

| Right | Agent/LLM implementation |
| --- | --- |
| Access Art. 15 | Export prompts/logs; redact third-party PI |
| Erasure Art. 17 | Delete from DB, vector store; vendor deletion SLA |
| Portability Art. 20 | JSON export of agent session data |
| Object Art. 21 | Stop profiling-based agent features |
| Restrict Art. 18 | Flag account—no LLM processing pending review |

1. **One-month** response (extendable 2 months)—stricter than many US states.
2. Route DSARs without sending full request to US LLM unredacted.

### Step 6: Security (Art. 32)

1. Align with `hipaa-phi-redaction-pipeline` and `access-control-identity-audit` where applicable.
2. Document: pseudonymization (Presidio tokens), encryption, MCP OAuth, resilience testing.
3. **Deanonymization opt-in** in `agent.py` supports Art. 32 minimization—default redacted output.

### Step 7: DPIA (Art. 35)

Required when processing likely **high risk**—systematic profiling, large-scale special categories, public monitoring:

1. Describe agent processing, necessity, proportionality
2. Risk to data subjects: incorrect automated decisions, US transfer exposure
3. Mitigations: human review, redaction, EU region deployment, SCCs
4. Consult **DPO** (Art. 35(2)); seek supervisory authority opinion if residual high risk (Art. 36)

### Step 8: Breach notification (Arts. 33-34)

1. **72 hours** from awareness to supervisory authority—not 60 days like HIPAA.
2. If high risk to individuals: communicate breach to data subjects without undue delay (Art. 34).
3. Cross-border: notify **lead authority**; cooperate with concerned authorities (Art. 33(2)).
4. Use `breach-incident-response` for containment; this skill for **GDPR clock and content**.
5. Document processor notification from LLM vendor (Art. 33(2) processor→controller without undue delay).

### Step 9: Processor agreements (Art. 28)

LLM/MCP DPA must include:

- Subject matter, duration, nature/purpose, data types, controller instructions
- Confidentiality, security Art. 32, subprocessor authorization
- Assistance with DSAR, DPIA, breach notification
- Deletion/return at end of service
- Audit and inspection rights

### Step 10: Documentation and accountability (Art. 5(2))

1. Maintain RoPA, DPIA, LIA, SCCs, DPF certifications, training records.
2. **Evidence manifest** with SHA-256 for audit readiness.
3. Disclaim: operational readiness—not legal opinion; engage EU privacy counsel for binding interpretation.

## Common Rationalizations

| Excuse | Rebuttal |
| --- | --- |
| "We're US-only company—GDPR doesn't apply." | **Art. 3(2)** applies if offering services to EU data subjects—SaaS with EU users triggers GDPR. |
| "LLM vendor handles GDPR—we're processor only." | SaaS owner is usually **controller** for customer relationship—cannot outsource accountability. |
| "HIPAA compliance satisfies GDPR." | GDPR has **broader rights**, 72-hour breach, DPIA, and transfer rules—separate program required. |
| "Redaction means no transfer of personal data." | If re-identification possible or tokens map stored, still personal data—document transfer mechanism. |
| "SCCs alone are enough post-Schrems II." | **TIA + supplementary measures** required—document encryption and access controls. |

## Red Flags

- EU user prompts sent to US LLM without SCCs/DPF/TIA
- No RoPA entry for agent processing activities
- Art. 9 special category data in prompts without documented basis
- Breach response plan uses HIPAA 60-day timeline only
- No DPO involvement in agent DPIA despite profiling
- Deanonymization enabled by default in production EU path (violates minimization)

## Verification

- [ ] Art. 3 applicability and controller/processor roles documented
- [ ] Lawful basis (and Art. 9 if applicable) for each agent activity
- [ ] Art. 30 RoPA populated including US transfers and subprocessors
- [ ] Transfer mechanism verified (DPF/SCCs) with TIA on file
- [ ] DSAR workflow meets one-month deadline with LLM vendor chain
- [ ] Art. 32 security measures mapped to technical controls
- [ ] DPIA completed for high-risk agent processing; DPO consulted
- [ ] 72-hour breach notification playbook integrated
- [ ] Art. 28 processor DPAs executed with LLM/MCP vendors
