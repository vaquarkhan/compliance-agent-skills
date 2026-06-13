---
name: soc2-trust-services-criteria
description: Maps organizational controls and evidence to AICPA SOC 2 Trust Services Criteria (2017 TSC with 2022 revisions)—Security (CC), Availability (A), Confidentiality (C), Processing Integrity (PI), and Privacy (P). Trigger when scoping SOC 2 audits, gap assessments, control design reviews, or mapping agent/MCP architecture to TSC. Do not use for evidence collection mechanics (use soc2-evidence-collection) or continuous monitoring dashboards (use soc2-ccm-continuous-monitoring).
---

# SOC 2 Trust Services Criteria

## Overview

This skill maps technical and operational controls to **AICPA Trust Services Criteria (TSC)** used in SOC 2 examinations. The **Security** category (Common Criteria CC1.0–CC9.0) is **mandatory** for all SOC 2 reports. Additional categories apply based on report scope:

| Category | Prefix | When in scope |
| --- | --- | --- |
| Security | CC | Always |
| Availability | A | Uptime/performance commitments |
| Confidentiality | C | Confidential information protection |
| Processing Integrity | PI | Complete/valid processing |
| Privacy | P | Personal information lifecycle |

For AI agent and MCP architectures, focus areas include **CC6** (logical access), **CC7** (system operations/monitoring), **CC8** (change management), **CC9** (risk mitigation), and category-specific criteria when processing customer or PHI-adjacent data.

## When to Use

Use this skill when:

- **Scoping** a SOC 2 audit or readiness assessment
- **Gap analysis** against TSC for agent platforms, MCP integrations, or compliance tooling
- Mapping existing controls (IAM, logging, change management) to **CC/A/C/PI/P** points of focus
- Preparing **control narratives** for auditors
- Determining which TSC categories apply to a product or internal system
- Cross-walking HIPAA or PCI controls to SOC 2 for unified compliance programs

Do **not** use this skill when:

- Collecting screenshots and exports (use `soc2-evidence-collection`)
- Implementing CCM dashboards (use `soc2-ccm-continuous-monitoring`)
- HIPAA BAA legal review (use `hipaa-baa-vendor-assessment`)

## Core Process

Execute steps **in order**.

### Step 1: Report scope definition

1. Document **system description** boundaries:
   - Agent runtime, skills repository, MCP servers, evidence store, identity provider
   - Cloud regions, subservice organizations (carve-out vs inclusive method)
2. Select TSC categories in scope (minimum: **Security**).
3. Define **trust boundaries**: where customer data enters, processes, exits.
4. Artifact: `soc2-scope-{id}.json`.

### Step 2: Security (CC) — mandatory mapping

Map controls to each Common Criteria series:

| Series | Focus | Agent/MCP examples |
| --- | --- | --- |
| CC1 | Control environment | Security policies, roles for agent admins |
| CC2 | Communication | Internal security awareness, customer security docs |
| CC3 | Risk assessment | LLM vendor risk, MCP tool risk assessments |
| CC4 | Monitoring | CCM alerts, quarterly access reviews |
| CC5 | Control activities | Skill validation, redaction gate enforcement |
| CC6 | Logical access | MFA, RBAC, MCP OAuth scopes |
| CC7 | System operations | Logging, incident response, capacity |
| CC8 | Change management | Skill/MCP deployment approval, CI/CD |
| CC9 | Risk mitigation | Vendor management, insurance, BCP |

For each CC point of focus (e.g., CC6.1, CC6.2), record:
- Control description
- Control owner
- Evidence source (link to `soc2-evidence-collection` artifacts)
- Design effectiveness: PASS / FAIL / NOT IMPLEMENTED

### Step 3: Availability (A) — if in scope

1. Map **A1.x** criteria: capacity planning, recovery, environmental protections.
2. Document SLAs for agent API and MCP availability.
3. Test failover for critical MCP dependencies (Playwright, Postgres evidence DB).

### Step 4: Confidentiality (C) — if in scope

1. Map **C1.x** criteria: confidential information identification, disposal, access restriction.
2. Align with PHI redaction pipeline and encryption standards.
3. Verify confidential data (API keys, tokens) not in agent logs or Slack alerts.

### Step 5: Processing Integrity (PI) — if in scope

1. Map **PI1.x** criteria: processing complete, accurate, timely, authorized.
2. Agent-specific: skill steps executed in order, deterministic audit workflows, hash verification.
3. Document QA for compliance skill outputs (validate=True in SkillsCapability).

### Step 6: Privacy (P) — if in scope

1. Map **P1.x–P8.x** to privacy notice, choice, collection, use, retention, disclosure, quality, monitoring.
2. Distinguish **Privacy** (personal information) from **Confidentiality** (broader confidential data).
3. Cross-reference HIPAA privacy rule if ePHI overlaps—document dual mapping.

### Step 7: Subservice organization mapping

1. List vendors (LLM, cloud, MCP hosts) as **subservice organizations**.
2. Choose SOC report method: **carve-out** (auditor relies on vendor SOC 2) vs **inclusive**.
3. Map CC9.2 vendor management to vendor inventory and review cadence.

### Step 8: Gap analysis and remediation plan

1. Consolidate FAIL/NOT IMPLEMENTED items by TSC ID.
2. Prioritize by auditor likelihood and risk (CC6/CC7 gaps are high priority).
3. Assign remediation owners and target dates.
4. Produce control matrix export: `tsc-control-matrix-{id}.csv`.

## Common Rationalizations

| Excuse the agent might generate | Required rebuttal |
| --- | --- |
| "We're a small team—CC1 control environment doesn't apply." | CC1 applies to **all** SOC 2 examinations regardless of size—scale controls appropriately. |
| "Security category is enough; skip Availability even with SLA." | If product commits to uptime SLAs, **A** criteria are in scope—omission is an audit gap. |
| "MCP tools are dev infrastructure, not in system boundary." | If MCP processes customer data in production audits, they are **in boundary** unless explicitly carved out with evidence. |
| "Privacy and Confidentiality are the same." | TSC treats them as **distinct categories** with different points of focus—map separately. |
| "We can mark NOT IMPLEMENTED as PASS with a note." | NOT IMPLEMENTED requires **remediation plan** or scope exclusion with auditor agreement—not PASS. |
| "Vendor SOC 2 covers our CC6 obligations entirely." | Vendor reports cover **subservice** controls—you remain responsible for oversight (CC9.2). |

## Red Flags

- SOC 2 scope excludes MCP servers that process customer data in production
- CC6 MFA gap on agent admin or deanonymization functions
- CC8 change management bypassed for skill/MCP hotfixes in production
- CC7 logging gaps for agent tool invocations
- Privacy category omitted while processing personal information
- Control matrix cites evidence that does not exist or lacks dates
- Carve-out claimed for critical LLM subservice without reviewed SOC 2 report

## Verification

- [ ] System description and trust boundaries documented
- [ ] TSC categories in scope explicitly selected (minimum Security)
- [ ] CC1.0–CC9.0 mapped with control owner and evidence source per point of focus
- [ ] Optional categories (A/C/PI/P) mapped if in scope—or exclusion documented
- [ ] Subservice organizations listed with carve-out/inclusive method
- [ ] Gap analysis completed with prioritized remediation plan
- [ ] Control matrix exported with PASS/FAIL/NOT IMPLEMENTED status
- [ ] Cross-references to HIPAA/PCI controls documented where dual compliance applies
- [ ] Auditor-ready narratives drafted for each FAIL gap remediation
- [ ] Evidence cross-reference IDs link to soc2-evidence-collection artifacts
