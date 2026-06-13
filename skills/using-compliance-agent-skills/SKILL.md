---
name: using-compliance-agent-skills
description: Meta entry skill for the USA compliance agent repository. Routes tasks to HIPAA, HITECH, PCI-DSS, SOC 2, ISO 27001, NIST CSF 2.0, CCPA/CPRA, US state privacy, GDPR, FedRAMP, SOX, CMMC, and GLBA skills; configures presets, MCP servers, and the audit lifecycle (/scope, /audit, /evidence, /remediate, /report). Trigger when starting any compliance engagement, choosing which skill to load, onboarding a new auditor, or orchestrating multi-framework workflows. Do not use when a specific framework skill already matches the task (load that skill directly instead).
---

# Using Compliance Agent Skills

## Overview

This skill is the **routing and orchestration layer** for the compliance-agent-skills repository. It teaches the agent how to discover, load, and chain specialized skills without inventing regulatory steps. The repository implements progressive disclosure via Pydantic AI `SkillsCapability`: only load skills whose scope matches the user's task.

The compliance agent enforces a **mandatory PHI redaction gate** (`redaction.py` / Presidio) before any user text reaches the LLM. Skills operate on redacted input; authorized outputs may be deanonymized via the `deanonymize_response` tool.

**Lifecycle commands** (user-facing or scripted):

| Command | Purpose |
| --- | --- |
| `/scope` | Define in-scope systems, data flows, frameworks, and exclusions |
| `/audit` | Execute framework-specific control testing |
| `/evidence` | Collect, hash, and package artifacts for auditors |
| `/remediate` | Draft remediation plans with owners and deadlines |
| `/report` | Produce executive and technical findings summaries |

## When to Use

Use this skill when:

- The user asks a **broad compliance question** without naming a framework ("Are we compliant?")
- You need to **select among framework skills** (HIPAA, PCI-DSS, SOC 2, ISO 27001, NIST CSF, CCPA, FedRAMP, SOX, CMMC, GLBA)
- Configuring **MCP servers** (Playwright, Postgres, Slack, Presidio) for an audit run
- Starting a **new engagement** and defining scope before deep work
- Chaining skills (e.g., scope → PHI redaction → PCI script audit → evidence bundle)
- The user references **presets** or lifecycle commands (`/scope`, `/audit`, etc.)

Do **not** use this skill when:

- The task maps cleanly to one specialized skill (load it directly)
- The user needs only PHI redaction configuration (use `hipaa-phi-redaction-pipeline`)
- The task is pure third-party vendor review (use `hipaa-baa-vendor-assessment` or `vendor-third-party-risk`)

## Core Process

Execute the following steps **in order** for every new engagement.

### Step 1: Intake and framework detection

1. Parse the user request for:
   - **Framework signals**: HIPAA (PHI, BAA), PCI-DSS (CDE, PAN, scripts), SOC 2 (TSC), ISO 27001 (Annex A, SoA), NIST CSF (Govern/Identify/Protect), CCPA/CPRA (DSAR, opt-out), FedRAMP (SSP, 800-53), SOX (ITGC, 404), CMMC (CUI, 800-171), GLBA (NPI, Safeguards)
   - **Artifact type**: policy review, technical control test, incident, vendor assessment
   - **Environment**: production vs staging, cloud provider, MCP availability
2. If multiple frameworks apply, list them explicitly and propose a **sequenced plan** (scope first, then deepest-risk skill).
3. Record engagement metadata: UTC timestamp, auditor/run ID, target systems, authorization to scan.

### Step 2: Scope definition (`/scope`)

1. Document **in-scope**:
   - Systems, URLs, databases, MCP servers, identity providers
   - Data classifications (ePHI, CHD/SAD, confidential processing data)
   - Applicable regulations and TSC categories
2. Document **out-of-scope** with rationale (reduces audit creep and false positives).
3. Identify **blocking dependencies**: missing BAA, no scan authorization, Playwright MCP offline.
4. Emit a scope artifact: `scope-{engagement-id}.json` with version and approver field.

### Step 3: Skill routing matrix

Load **exactly one primary skill** per audit thread; add secondary skills only when scope requires:

| User intent | Primary skill | Common secondary skills |
| --- | --- | --- |
| Payment page / checkout scripts | `pci-dss-script-audit` | `mcp-compliance-integration`, `soc2-evidence-collection` |
| CDE network / firewall | `pci-dss-network-segmentation` | `access-control-identity-audit` |
| PHI in prompts / LLM pipeline | `hipaa-phi-redaction-pipeline` | `hipaa-technical-safeguards` |
| Access controls, MFA, IAM | `access-control-identity-audit` | `soc2-trust-services-criteria` |
| Log tampering / audit trails | `audit-logging-integrity` | `hipaa-technical-safeguards` |
| SOC 2 control mapping | `soc2-trust-services-criteria` | `soc2-evidence-collection` |
| Continuous monitoring | `soc2-ccm-continuous-monitoring` | `compliance-as-code-governance` |
| LLM/cloud vendor legal | `hipaa-baa-vendor-assessment` | `vendor-third-party-risk` |
| MCP server hardening | `mcp-compliance-integration` | `access-control-identity-audit` |
| PCI encryption, PAN, key management | `pci-dss-encryption-key-management` | `audit-logging-integrity` |
| HIPAA minimum necessary / de-id | `hipaa-privacy-minimum-necessary` | `hipaa-phi-redaction-pipeline` |
| ISO 27001 Annex A / SoA | `iso27001-annex-a-controls` | `soc2-trust-services-criteria` |
| NIST CSF 2.0 assessment | `nist-csf-2-assessment` | `compliance-as-code-governance` |
| CCPA/CPRA consumer rights | `ccpa-cpra-privacy-rights` | `hipaa-privacy-minimum-necessary` |
| FedRAMP cloud authorization | `fedramp-moderate-baseline` | `nist-csf-2-assessment` |
| SOX ITGC / SOX 404 | `sox-itgc-audit` | `access-control-identity-audit` |
| CMMC / CUI / defense | `cmmc-nist-800-171` | `fedramp-moderate-baseline` |
| GLBA / banking / fintech | `glba-ffiec-financial-privacy` | `vendor-third-party-risk` |
| HITECH breach / OCR portal | `hitech-breach-notification` | `breach-incident-response` |
| US state privacy (VCDPA, CPA, TX) | `us-state-privacy-laws` | `ccpa-cpra-privacy-rights` |
| GDPR / EU transfers | `gdpr-us-multinational` | `us-state-privacy-laws` |
| Breach / incident | `breach-incident-response` | `audit-logging-integrity` |
| Policy-as-code / IaC | `compliance-as-code-governance` | `soc2-evidence-collection` |

4. Call `load_skill` for the primary skill and **follow its Core Process verbatim**.

### Step 4: MCP preset configuration

Before `/audit`, confirm MCP servers required by the loaded skill:

| MCP server | Typical use | Compliance relevance |
| --- | --- | --- |
| Playwright (`@playwright/mcp`) | DOM, headers, screenshots | PCI 6.4.3, 11.6.1; SOC 2 CC7.x |
| Postgres | Baselines, inventory, evidence store | Script hashes, control status |
| Slack | SOC alerts, approval workflows | Incident notification |
| Presidio (custom or REST) | DLP entity detection | HIPAA §164.312(e), minimum necessary |

If a required MCP is unavailable, **stop** and document a blocking finding—do not substitute undocumented tools.

### Step 5: Execute audit (`/audit`)

1. Ensure upstream PHI redaction ran (agent default in `agent.py`).
2. Execute the loaded skill's Core Process without skipping steps.
3. Log each step completion with artifact IDs in UTC.

### Step 6: Evidence packaging (`/evidence`)

1. Collect artifacts from all executed skills.
2. Apply SHA-256 to each file; record in manifest.
3. Store with immutable audit ID suitable for QSA or SOC 2 auditor review.
4. Cross-reference controls to evidence items (control ID → artifact path → hash).

### Step 7: Remediation (`/remediate`)

1. For each FAIL or UNKNOWN finding, draft:
   - Root cause, compensating controls (if any), remediation owner, target date
   - Residual risk if deferred
2. Prioritize by regulatory severity (e.g., PCI IOC, HIPAA transmission gap, SOC 2 CC6.1 MFA gap).

### Step 8: Report (`/report`)

1. Produce:
   - **Executive summary**: scope, frameworks, pass/fail counts, top risks
   - **Technical appendix**: control-by-control status with evidence links
   - **Open items**: remediation backlog with owners
2. Deanonymize only for authorized recipients via `deanonymize_response`; never include raw PHI in reports sent to unapproved channels.

## Common Rationalizations

| Excuse the agent might generate | Required rebuttal |
| --- | --- |
| "I'll answer from general compliance knowledge without loading a skill." | Skills contain **mandatory sequences** and exit criteria. General knowledge bypasses verifiable evidence requirements. |
| "Scope can be implied; no need for `/scope`." | Undefined scope causes false positives and **audit failures**. Scope artifacts are required for multi-framework engagements. |
| "I'll load multiple primary skills in parallel without sequencing." | Parallel primary skills duplicate work and conflict on MCP usage. One primary skill per thread; secondaries only when scoped. |
| "MCP is optional if I can curl the URL." | Specialized skills (e.g., PCI script audit) **require** documented MCP tools for rendered DOM and baselines. |
| "Evidence can be summarized without hashes." | Auditors require **integrity-verified** artifacts (SHA-256 manifest). Summaries alone are insufficient. |
| "Remediation can wait until after the report." | `/report` must include open findings **and** remediation owners for FAIL items. |
| "I'll deanonymize tokens to make the report readable." | Deanonymization is **authorization-gated**. Redacted tokens in LLM context must not be reconstructed without approval. |

## Red Flags

- Engagement proceeds without documented scope or scan authorization
- User text bypasses PHI redaction before reaching the model
- Agent invents control IDs or regulatory citations not in loaded skills
- Primary skill skipped in favor of generic advice
- Evidence bundle missing hashes or UTC timestamps
- Deanonymized PHI appears in Slack or unencrypted channels
- PCI IOC or breach indicators routed to `/report` without `/remediate` and incident skills

## Verification

Do not mark this skill complete until **all** exit criteria are confirmed:

- [ ] Framework(s) identified and documented in scope artifact
- [ ] `/scope` completed with in-scope/out-of-scope systems and data classifications
- [ ] Primary skill selected via routing matrix and loaded successfully
- [ ] Required MCP servers confirmed available or blocking finding recorded
- [ ] PHI redaction gate confirmed active for all user-provided text
- [ ] Loaded skill's Core Process executed (not abbreviated)
- [ ] `/evidence` manifest includes SHA-256 for every artifact
- [ ] FAIL/UNKNOWN findings have remediation entries with owners and dates
- [ ] `/report` delivered with executive summary and evidence cross-reference
- [ ] Deanonymization applied only where authorization is documented
