---
name: iso27001-annex-a-controls
description: Implements ISO/IEC 27001:2022 Annex A control assessment—93 controls across Organizational, People, Physical, and Technological themes—covering Statement of Applicability (SoA), risk treatment, and implementation evidence. Trigger when building or auditing an ISMS, mapping Annex A to existing controls, preparing ISO 27001 certification, or assessing agent/MCP systems against ISO 27002:2022 guidance. Do not use for SOC 2 TSC mapping alone (use soc2-trust-services-criteria), IAM-only reviews (use access-control-identity-audit), or vendor SOC report review without ISO scope (use vendor-third-party-risk).
---

# ISO 27001 Annex A Controls

## Overview

This skill performs **ISO/IEC 27001:2022** Annex A control assessments aligned with **ISO/IEC 27002:2022** implementation guidance. Annex A contains **93 controls** organized in four themes:

| Theme | Control count | Examples |
| --- | --- | --- |
| **Organizational** (A.5) | 37 | Policies, asset management, supplier relationships, incident management |
| **People** (A.6) | 8 | Screening, terms of employment, awareness, remote working |
| **Physical** (A.7) | 14 | Secure areas, equipment, clear desk, cabling security |
| **Technological** (A.8) | 34 | Access control, cryptography, logging, secure development, cloud services |

ISO 27001 **Clause 6.1.3** requires a **Statement of Applicability (SoA)** documenting which Annex A controls apply, justification for exclusions, and implementation status. **Clause 8.1** requires operational control implementation with evidence.

This skill **cross-maps** to existing repository skills:

- **A.5.15–A.5.18, A.8.2–A.8.5** → `access-control-identity-audit` (IAM, privileged access, authentication)
- **A.8.15, A.8.16** → `audit-logging-integrity` (logging, monitoring, SIEM)
- **A.5.19–A.5.23** → `vendor-third-party-risk` (supplier and cloud service security)
- **A.8.24, A.8.9** → `pci-dss-encryption-key-management` (cryptography, configuration management)
- **A.8.25–A.8.28** → `mcp-compliance-integration` (secure development, application security for agents)

## When to Use

Use this skill when:

- **Building or auditing an ISMS** for ISO 27001:2022 certification or surveillance audit
- Drafting or validating the **Statement of Applicability (SoA)**
- Performing **risk treatment** and mapping controls to identified risks (Clause 6.1.2)
- **Gap assessing** agent/MCP infrastructure against Annex A Technological controls
- **Harmonizing** ISO 27001 with SOC 2, HIPAA, or PCI programs already in this repository
- Collecting **implementation evidence** for certification body or internal audit

Do **not** use this skill when:

- SOC 2-only TSC evidence binders without ISO scope (use `soc2-evidence-collection`)
- PCI CDE network segmentation (use `pci-dss-network-segmentation`)
- California consumer privacy rights (use `ccpa-cpra-privacy-rights`)
- NIST CSF function-based gap analysis without ISO SoA deliverable (use `nist-csf-2-assessment`)

## Core Process

Execute steps **in order**.

### Step 1: ISMS scope and context (Clauses 4.1–4.3)

1. Document **ISMS scope** boundary: legal entities, locations, systems, processes, data types.
2. Identify **interested parties** and their requirements (customers, regulators, certification body).
3. For AI/agent systems, explicitly include:
   - Compliance agent runtime (`agent.py`)
   - MCP servers (Playwright, Postgres, Presidio, Terraform)
   - LLM vendor subprocessors processing redacted or raw data
4. Artifact: `isms-scope-{id}.json` with UTC timestamp and approver.

### Step 2: Risk assessment (Clause 6.1.2)

1. Identify information security risks within scope using asset-threat-vulnerability methodology.
2. Rate likelihood and impact; assign risk owners.
3. Select treatment options: **mitigate**, **transfer**, **avoid**, **accept** (with documented acceptance criteria).
4. Map each treated risk to one or more **Annex A controls** as treatment actions.
5. Artifact: `risk-register-{id}.csv` with risk ID, treatment, linked control IDs (e.g., A.8.5).

### Step 3: Statement of Applicability (SoA) — Clause 6.1.3

1. List all **93 Annex A controls** from ISO/IEC 27001:2022 Annex A.
2. For each control, record:

| Field | Content |
| --- | --- |
| Control ID | e.g., A.5.15 |
| Applicable? | Yes / No |
| Justification if excluded | Required for "No" |
| Implementation status | Implemented / Partial / Planned / N/A |
| Implementation reference | Policy ID, procedure, technical control |
| Evidence location | File path, system, audit ID |

3. **No control may be excluded without justification**—certification bodies reject blank SoA rows.
4. For agent systems, typically **mandatory** controls include A.5.9 (asset inventory), A.5.23 (cloud services), A.8.2 (privileged access), A.8.15 (logging), A.8.28 (secure coding).
5. Artifact: `statement-of-applicability-{id}.yaml`.

### Step 4: Theme-by-theme control assessment

Assess each theme with evidence requirements per ISO/IEC 27002:2022:

**Organizational (A.5):**
- A.5.1: Information security policy approved by top management
- A.5.2: Roles and responsibilities documented (include agent/MCP owners)
- A.5.7: Threat intelligence process
- A.5.24–A.5.28: Incident management (cross-ref `breach-incident-response`)
- A.5.29–A.5.30: Business continuity

**People (A.6):**
- A.6.3: Security awareness including AI/agent data handling
- A.6.7: Remote working controls for agents accessing production evidence

**Physical (A.7):**
- A.7.4: Physical security monitoring (data center, office)
- A.7.10: Storage media (evidence drives, backup tapes)

**Technological (A.8):**
- Delegate deep dives to cross-cutting skills (see Overview mapping)
- A.8.11: Data masking (cross-ref `hipaa-phi-redaction-pipeline`)
- A.8.12: DLP (Presidio gate in `redaction.py`)
- A.8.23: Web filtering (MCP URL allowlists)

Document PASS/FAIL/PARTIAL per control with observation and evidence hash.

### Step 5: Cross-framework mapping

1. Build traceability matrix linking Annex A to in-repo frameworks:

| Annex A | SOC 2 | HIPAA | PCI-DSS |
| --- | --- | --- | --- |
| A.8.2 | CC6.1 | §164.312(a) | Req 7 |
| A.8.15 | CC7.2 | §164.312(b) | Req 10 |
| A.5.19 | CC9.2 | BAA | Req 12.8 |
| A.8.24 | CC6.1 | §164.312(a)(2)(iv) | Req 3/4 |

2. Reuse evidence from existing audits—do not duplicate collection without gap analysis.
3. Flag controls with **no cross-map** requiring ISO-specific evidence.

### Step 6: MCP and agent evidence collection

1. Use **Postgres MCP** (read-only) to query asset/configuration tables for A.5.9, A.8.9 evidence.
2. Use **Terraform MCP** (`mcp/terraform.mcp.json`) for A.8.9 configuration baseline drift.
3. Use **Playwright MCP** only for documented URLs—capture screenshots for A.8.20 (network security) where applicable.
4. Never store unredacted PHI or PAN in ISO evidence binders—apply `redaction.py` before LLM analysis.
5. Hash all evidence files (SHA-256) per `templates/audit-evidence-manifest.yaml`.

### Step 7: Internal audit and management review prep (Clauses 9.2, 9.3)

1. Sample **10% of applicable controls** for deep evidence testing.
2. Prepare management review inputs: open risks, SoA changes, nonconformities, audit findings.
3. Document corrective actions for FAIL/PARTIAL controls with owner and due date.

### Step 8: Findings and remediation tracker

1. Emit findings in standard format:

```yaml
id: FIND-ISO-001
severity: HIGH
control_id: A.8.5
observation: "MCP service account lacks periodic access review"
recommendation: "Implement quarterly recertification per A.8.5; use access-control-identity-audit Step 7"
owner: ""
due_date: null
status: open
```

2. Prioritize: CRITICAL (certification blocker), HIGH (major nonconformity), MEDIUM (minor), LOW (observation).

## Common Rationalizations

| Excuse the agent might generate | Required rebuttal |
| --- | --- |
| "We're SOC 2 certified, so ISO 27001 is automatic." | SOC 2 TSC **does not cover all 93 Annex A controls**—SoA must address each control individually with ISO-specific evidence. |
| "We excluded all Physical controls because we're cloud-only." | Cloud-only orgs still need applicable A.7 controls for **offices, laptops, and media**—blanket exclusion fails certification. |
| "Annex A is guidance only; we don't need evidence." | ISO 27001 **requires** implemented controls for all applicable Annex A entries—27002 is implementation guidance, not optional. |
| "Agent infrastructure is out of ISMS scope." | If agents process scoped data or access production systems, they are **in scope**—A.8.25–A.8.28 apply. |
| "SoA can mark everything 'Planned' for year one." | Certification bodies expect **Implemented** or justified **Partial** with remediation plan—all-Planned SoA rows are rejected. |
| "Vendor SOC 2 report replaces A.5.19 assessment." | SOC report is **input** to supplier review, not replacement—A.5.19–A.5.22 require your organization's due diligence. |

## Red Flags

- SoA with unexplained "No" for >20% of controls without risk-based justification
- No risk register or risks not linked to Annex A treatment controls
- Agent/MCP credentials absent from A.5.9 asset inventory
- A.8.15 logging not covering MCP tool invocations and deanonymization events
- Cloud LLM vendor missing from A.5.19 supplier register
- Evidence binder contains raw ePHI or PAN without redaction
- Internal audit sampled only Organizational theme, skipped Technological (A.8)
- Management review not conducted within 12 months of certification cycle

## Verification

- [ ] ISMS scope documented including agent/MCP and LLM subprocessors
- [ ] Risk register complete with treatment actions mapped to Annex A controls
- [ ] Statement of Applicability covers all 93 controls with justification for exclusions
- [ ] Each applicable control assessed PASS/FAIL/PARTIAL with evidence reference and SHA-256 hash
- [ ] Cross-framework mapping matrix completed against SOC 2, HIPAA, PCI where in scope
- [ ] Technological controls (A.8) assessed using access-control, audit-logging, vendor skills
- [ ] MCP evidence collected via read-only tools without cleartext PHI/PAN in artifacts
- [ ] Internal audit sample (≥10% applicable controls) executed with findings logged
- [ ] Remediation tracker populated for FAIL/PARTIAL with owners and due dates
- [ ] Management review inputs prepared per Clause 9.3
