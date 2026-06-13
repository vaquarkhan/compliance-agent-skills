---
name: nist-csf-2-assessment
description: Performs NIST Cybersecurity Framework 2.0 gap assessments across six Functions—Govern, Identify, Protect, Detect, Respond, Recover—using CSF 2.0 categories, subcategories, Implementation Tiers, and Organizational Profiles. Trigger when benchmarking security posture, preparing executive risk reporting, assessing AI/agent system controls against NIST CSF, or harmonizing CSF with ISO 27001 or SOC 2 programs. Do not use for ISO 27001 SoA certification work (use iso27001-annex-a-controls), PCI CDE scoping (use pci-dss-network-segmentation), or HIPAA Privacy Rule minimum necessary (use hipaa-privacy-minimum-necessary).
---

# NIST CSF 2.0 Assessment

## Overview

This skill implements **NIST Cybersecurity Framework (CSF) 2.0** (NIST CSWP 29, February 2024) gap assessments. CSF 2.0 organizes outcomes into **six Functions**:

| Function | Purpose | Example categories |
| --- | --- | --- |
| **GOVERN (GV)** | Enterprise risk management, strategy, supply chain | GV.OC, GV.RM, GV.SC |
| **IDENTIFY (ID)** | Asset management, risk assessment, improvement | ID.AM, ID.RA, ID.IM |
| **PROTECT (PR)** | Identity, awareness, data security, platform security | PR.AA, PR.AT, PR.DS, PR.PS |
| **DETECT (DE)** | Continuous monitoring, adverse event analysis | DE.CM, DE.AE |
| **RESPOND (RS)** | Incident management, analysis, mitigation, communication | RS.MA, RS.AN, RS.MI, RS.CO |
| **RECOVER (RC)** | Recovery planning, execution, communication | RC.RP, RC.CO |

**Implementation Tiers** (Partial → Risk Informed → Repeatable → Adaptive) describe organizational maturity—not control pass/fail.

**Profiles** document Current vs Target state for prioritized improvement. CSF 2.0 adds explicit **supply chain (GV.SC)** and **governance (GV)** emphasis relevant to **LLM vendors, MCP servers, and agent toolchains**.

Reference document: [NIST CSF 2.0](https://www.nist.gov/cyberframework) (CSWP 29).

## When to Use

Use this skill when:

- **Executive or board-level** cybersecurity posture reporting using NIST CSF taxonomy
- **Gap assessing** AI agent deployments (compliance agent, MCP tools, LLM APIs)
- Building **Current and Target Profiles** for a 12–24 month roadmap
- **Harmonizing** CSF outcomes with ISO 27001 Annex A or SOC 2 TSC (cross-walk, not replacement)
- **Vendor/customer** questionnaires referencing NIST CSF 2.0
- **Continuous improvement** cycles (ID.IM) after incidents or audits

Do **not** use this skill when:

- Legal attestation under PCI-DSS or HIPAA alone (use framework-specific skills)
- Detailed IAM permission analysis (use `access-control-identity-audit`)
- PHI redaction pipeline tuning (use `hipaa-phi-redaction-pipeline`)
- California consumer DSAR processing (use `ccpa-cpra-privacy-rights`)

## Core Process

Execute steps **in order**.

### Step 1: Profile scope and tier selection

1. Define assessment scope: business units, systems, data types (ePHI, CHD, PII, model prompts).
2. Explicitly include **agent architecture**:
   - `agent.py` runtime and skills loader
   - MCP servers per `mcp/README.md`
   - LLM provider APIs and data retention terms
3. Select target **Implementation Tier** per Function (document rationale):
   - Tier 1 Partial: ad hoc, reactive
   - Tier 2 Risk Informed: approved practices, some sharing
   - Tier 3 Repeatable: formal policies, organization-wide
   - Tier 4 Adaptive: continuous improvement, predictive
4. Artifact: `csf-profile-scope-{id}.json`.

### Step 2: Asset and system inventory (ID.AM)

1. Inventory hardware, software, data, users, services—including **non-human identities** (MCP OAuth clients, API keys).
2. Map dependencies: agent → MCP → database → LLM vendor.
3. Classify data sensitivity per `ID.AM-5` (data classification).
4. Cross-ref `access-control-identity-audit` Step 1 for identity inventory reuse.

### Step 3: Subcategory assessment worksheet

1. Download CSF 2.0 Core subcategory list from NIST (106 subcategories).
2. For each subcategory in scope, record:

| Subcategory | Current status | Tier | Evidence | Gap | Target date |
| --- | --- | --- | --- | --- | --- |
| PR.DS-01 | Partial | 2 | S3 encryption policy | Key rotation gap | Q3 |
| GV.SC-04 | Not met | 1 | No LLM vendor SCRM | Missing BAA/DPAs | Q2 |
| DE.CM-01 | Met | 3 | CloudTrail + SIEM | — | — |

3. **AI/agent priority subcategories** (assess even if scope is narrow):

| Subcategory | Agent relevance |
| --- | --- |
| GV.OC-03 | Legal/regulatory requirements for AI data handling |
| GV.SC-07 | Third-party incident reporting (LLM breach notification) |
| PR.AA-01 | Identity management for MCP service accounts |
| PR.DS-10 | Data in use—PHI in prompts; redaction gate |
| PR.PS-04 | Resource management—agent compute isolation |
| DE.CM-09 | Monitoring MCP tool invocations |
| RS.MA-02 | Incident triage for agent data leakage |
| ID.IM-04 | Improvement from redaction false-negative tests |

4. Status values: **Met**, **Partial**, **Not Met**, **Not Applicable** (with justification).

### Step 4: Govern and supply chain deep dive (GV.*)

1. **GV.RM**: Map enterprise risk register to CSF; include model hallucination, prompt injection, data exfiltration via MCP.
2. **GV.SC-04–GV.SC-10**: Supplier cyber risk for:
   - LLM providers (data retention, training use, subprocessors)
   - MCP package maintainers
   - Cloud hosting
3. Reuse `vendor-third-party-risk` and `hipaa-baa-vendor-assessment` evidence where applicable.
4. Document **SRMA** (Supply Chain Risk Management Agreement) gaps for agent stack.

### Step 5: Protect function — agent-specific controls (PR.*)

1. **PR.AA** (Identity Management, Authentication, Access Control):
   - MFA, least privilege, MCP OAuth scopes → `access-control-identity-audit`
2. **PR.DS** (Data Security):
   - Encryption at rest/transit → `pci-dss-encryption-key-management`
   - PHI redaction → `hipaa-phi-redaction-pipeline`
3. **PR.PS** (Platform Security):
   - Secure configuration, patch management → `compliance-as-code-governance`
   - MCP hardening → `mcp-compliance-integration`
4. **PR.AT** (Awareness and Training):
   - Agent operators trained on minimum necessary and token handling

### Step 6: Detect, Respond, Recover (DE.*, RS.*, RC.*)

1. **DE.CM**: Verify logging covers agent sessions, MCP calls, deanonymization—`audit-logging-integrity`.
2. **DE.AE**: SIEM correlation rules for anomalous MCP query volume or new OAuth clients.
3. **RS.MA–RS.CO**: Incident playbooks for prompt leakage, rogue MCP tool—`breach-incident-response`.
4. **RC.RP**: Recovery procedures for agent config compromise, token map exposure.

### Step 7: Implementation Tier scoring

1. For each Function, assign **Current Tier** (1–4) based on NIST tier characteristics—not average of subcategories.
2. Compare Current vs Target Tier; document gap narrative for executives.
3. Avoid **tier inflation**: Tier 4 requires adaptive, organization-wide practices with supply chain integration.

### Step 8: Target Profile and roadmap

1. Select prioritized subcategories for Target Profile (typically 15–30 for first cycle).
2. Assign owners, milestones, and dependencies.
3. Link remediation items to existing skills and presets (`presets/regulated-ai-agents-starter.yaml` if applicable).
4. Artifact: `csf-target-profile-{id}.yaml` with Current vs Target comparison.

### Step 9: Evidence packaging

1. Collect evidence per Met/Partial subcategory with SHA-256 hashes.
2. Use `templates/audit-evidence-manifest.yaml` structure.
3. Optional: **Terraform MCP** for PR.PS infrastructure evidence; **Postgres MCP** read-only for configuration queries.

## Common Rationalizations

| Excuse the agent might generate | Required rebuttal |
| --- | --- |
| "CSF is voluntary, so Partial everywhere is fine." | Voluntary ≠ **meaningless**—Partial without Target Profile and roadmap fails the assessment purpose and customer expectations. |
| "We can skip GOVERN— we're a engineering team." | CSF 2.0 **elevates GOVERN** as foundational—GV.RM and GV.SC are mandatory for credible profiles. |
| "LLM vendor security is their problem (GV.SC)." | **GV.SC-04** requires your organization to manage supplier risk—you own vendor selection and contract terms. |
| "Redaction covers PR.DS, no other data controls needed." | PR.DS spans **at rest, in transit, in use, and disposal**—redaction is one control, not the whole subcategory. |
| "Tier 4 is our target for everything." | Tiers reflect **actual maturity**—claiming Tier 4 without evidence is misrepresentation to executives and customers. |
| "CSF 1.1 mapping still works." | CSF 2.0 added **GOVERN**, restructured categories—remap; do not reuse deprecated 1.1 IDs. |

## Red Flags

- Assessment excludes GV function entirely
- LLM/MCP vendors absent from ID.AM and GV.SC inventory
- All subcategories marked Met without evidence references
- No Target Profile or all gaps marked "future consideration" without dates
- DE.CM has no agent/MCP logging coverage
- RS playbooks do not address AI-specific incidents (prompt injection, token reconstruction)
- Tier 3–4 claimed with ad hoc policies and no measurement
- CSF 1.1 category IDs used instead of CSF 2.0 taxonomy

## Verification

- [ ] Profile scope includes agent runtime, MCP servers, and LLM vendors
- [ ] Implementation Tier targets documented per Function with rationale
- [ ] All in-scope CSF 2.0 subcategories assessed with Met/Partial/Not Met/N/A
- [ ] AI/agent priority subcategories (GV.SC, PR.DS, PR.AA, DE.CM) explicitly evaluated
- [ ] GOVERN and supply chain assessment completed with vendor evidence cross-refs
- [ ] Current Tier scored per Function; gap narrative prepared for executives
- [ ] Target Profile defined with prioritized subcategories, owners, and milestones
- [ ] Cross-skill evidence reused from access-control, audit-logging, vendor, MCP skills
- [ ] Evidence manifest complete with SHA-256 hashes and engagement ID
- [ ] Improvement plan (ID.IM) links findings to remediation trackers
