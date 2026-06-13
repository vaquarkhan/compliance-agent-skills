---
name: ccpa-cpra-privacy-rights
description: Implements California Consumer Privacy Act (CCPA) as amended by the California Privacy Rights Act (CPRA)—Cal. Civ. Code §1798.100 et seq.—covering consumer rights to know, delete, correct, opt-out of sale/share, and limit use of sensitive personal information, plus DSAR workflows, privacy notices, and service provider contracts for AI/agent data handling. Trigger when processing California residents' personal information, operating DSAR programs, reviewing agent/LLM data flows for CPRA compliance, or auditing privacy notices and vendor agreements. Do not use for HIPAA-covered PHI workflows (use hipaa-privacy-minimum-necessary), PCI cardholder encryption (use pci-dss-encryption-key-management), or general vendor SOC reports without CPRA scope (use vendor-third-party-risk).
---

# CCPA / CPRA Privacy Rights

## Overview

This skill operationalizes **California privacy law** under **CCPA as amended by CPRA** (operationalized by the **California Privacy Protection Agency**, CPPA). Key statutes:

| Topic | Primary citations |
| --- | --- |
| Consumer rights | Cal. Civ. Code **§1798.100–§1798.135** |
| Sensitive PI limitations | **§1798.121** (limit use/disclosure) |
| Opt-out of sale/share | **§1798.120**, **§1798.135** (Do Not Sell or Share) |
| Right to correct | **§1798.106** (CPRA addition) |
| Right to delete | **§1798.105**, **§1798.110(c)(7)** |
| Right to know | **§1798.110**, **§1798.115** |
| Service providers / contractors | **§1798.140(ag)**, **§1798.140(j)**, **§1798.140(v)** |
| Automated decision-making | **§1798.185(a)(16)** (regulations) |
| Privacy policy requirements | **§1798.130(a)(5)**, **§1798.135(b)** |

**Personal information (PI)** includes identifiers, commercial information, biometric data, geolocation, and inferences—**prompts and agent logs may contain PI** even when not HIPAA PHI.

**Sensitive personal information (SPI)** includes SSN, precise geolocation, racial/ethnic origin, mail/email/password in combination with credentials, and contents of mail/email (with exceptions).

AI/agent systems must address: **what PI enters LLM prompts**, **retention by LLM vendors**, **subprocessor chains**, and **DSAR fulfillment** across agent databases and logs.

## When to Use

Use this skill when:

- **Processing California residents' PI** in products, analytics, or agent workflows
- Building or auditing **Data Subject Access Request (DSAR)** / consumer rights request programs
- Reviewing **privacy policies**, **notice at collection**, and **CPRA addendum** disclosures
- Assessing **sale/share** of PI (including cross-context behavioral advertising) and **opt-out** mechanisms
- Drafting or reviewing **service provider agreements** for LLM, MCP, or analytics vendors
- Evaluating **agent prompt/logging** practices for PI minimization and deletion capability
- Responding to **CPPA enforcement trends** or customer CPRA questionnaires

Do **not** use this skill when:

- HIPAA Security Rule technical controls only (use `hipaa-technical-safeguards`)
- PCI PAN encryption and key management (use `pci-dss-encryption-key-management`)
- SOC 2 TSC-only audits without California PI (use `soc2-trust-services-criteria`)
- Breach notification under HIPAA/state breach laws without CPRA rights scope (use `breach-incident-response`)

## Core Process

Execute steps **in order**.

### Step 1: Scope and role determination

1. Determine if organization is **business**, **service provider**, **contractor**, or **third party** per §1798.140 definitions.
2. Map **data flows** for California consumers:
   - Web/app collection → agent prompts → LLM API → logs → MCP Postgres evidence store
3. Identify **business purposes** vs **commercial purposes** (sale/share) per §1798.140.
4. Document **sensitive PI** categories collected—triggers §1798.121 **Limit the Use** rights.
5. Artifact: `cpra-data-map-{id}.json`.

### Step 2: Consumer rights inventory

For each right, document statutory basis, process owner, SLA, and systems affected:

| Right | Citation | SLA (recommended) | Agent/LLM considerations |
| --- | --- | --- | --- |
| Know (access) | §1798.110, §1798.115 | 45 days + extension | Export prompts/logs with redaction of other consumers' PI |
| Delete | §1798.105 | 45 days | Delete from agent DB, vector stores, LLM vendor if contractually required |
| Correct | §1798.106 | 45 days | Update source systems; re-index embeddings if used |
| Opt-out of sale/share | §1798.120 | 15 business days for opt-out processing | Stop sharing ad identifiers; review analytics SDKs |
| Limit SPI use | §1798.121 | As soon as feasible | Restrict SPI in agent prompts to minimum necessary |
| Non-discrimination | §1798.125 | Immediate | No denial of service for exercising rights |

### Step 3: DSAR intake and verification

1. Provide **two or more designated methods** for submission (§1798.130(a)(1))—web form, toll-free, email.
2. **Verify consumer identity** to reasonable degree (§1798.140)—do not over-collect verification PI.
3. For agent-related requests:
   - Query internal stores: session logs, `redaction.py` token maps (may contain PI—handle as SPI)
   - Issue **vendor requests** to LLM provider if they hold PI on your behalf (requires contract terms)
4. Log DSAR in tracker: request ID, type, receipt date, verification status, due date, outcome.
5. **Do not** send raw consumer PI to LLM for DSAR processing—use redaction or structured DB queries via **Postgres MCP** (read-only, audited).

### Step 4: DSAR fulfillment workflow

1. **Access (Know)**:
   - Categories and specific pieces of PI collected (§1798.110)
   - Sources, business/commercial purposes, third parties disclosed to (§1798.115)
   - Deliver in portable format; exclude other consumers' data and trade secrets
2. **Delete**:
   - Direct service providers/contractors to delete (§1798.105(c))
   - Delete agent session data, cached prompts, analytics events
   - Document exceptions: legal retention, security incidents, complete transaction
3. **Correct**:
   - Correct inaccurate PI; instruct service providers per §1798.106
4. **Opt-out / Limit**:
   - Honor **Global Privacy Control (GPC)** as valid opt-out signal where required (CPPA regulations)
   - Implement **Limit SPI** link if collecting SPI for non-essential purposes (§1798.135(a)(2))

### Step 5: Privacy notices and disclosures

1. Review **privacy policy** for CPRA-required elements (§1798.130(a)(5)):
   - Categories of PI collected, purposes, retention, sale/share practices
   - Consumer rights and how to exercise them
   - SPI categories and Limit the Use link if applicable
   - **Automated decision-making** disclosure if applicable (§1798.185)
2. **Notice at collection** at each collection point—including agent chat interfaces.
3. **Annual privacy metrics** (if business meets volume thresholds)—requests received and median response times.
4. Artifact: `privacy-notice-gap-analysis-{id}.md`.

### Step 6: Service provider and LLM vendor contracts

1. Verify written contracts prohibit **selling/sharing** PI and restrict use to **business purposes** (§1798.140(ag)).
2. For LLM/agent vendors, contract must address:
   - **No training** on consumer PI unless disclosed and permitted
   - **Deletion** support for DSAR
   - **Subprocessor** notification
   - **Security** requirements comparable to CPRA §1798.100(e)
3. Cross-ref `vendor-third-party-risk` for assessment methodology and `hipaa-baa-vendor-assessment` only if PHI overlap exists.
4. Distinguish **service provider** vs **third party**—third party relationships require consumer notice and opt-out where applicable.

### Step 7: Agent and MCP data handling controls

1. **Minimization**: Do not pass consumer PI to LLM beyond task necessity—align with `hipaa-phi-redaction-pipeline` patterns for tokenization.
2. **Retention**: Define TTL for agent logs; automated deletion jobs.
3. **Sale/share analysis**: Review whether analytics, advertising integrations, or data licensing constitute **sale** or **sharing** under CPRA definitions.
4. **MCP logging**: Ensure Slack/Postgres MCP does not persist consumer PI in cleartext—see `mcp-compliance-integration`.
5. **GPC/opt-out**: Technical honor signal before agent enriches profile with shared data.

### Step 8: Findings and remediation

1. Emit findings with CPRA citations:

```yaml
id: FIND-CPRA-001
severity: HIGH
control_id: CCPA-1798.105
observation: "Agent session store lacks delete workflow for DSAR"
recommendation: "Implement deletion API covering Postgres evidence DB and 30-day LLM vendor purge SLA"
owner: ""
due_date: null
status: open
```

2. Package evidence: data map, notice copies, DSAR samples (redacted), contract clauses, policy versions with hashes.

## Common Rationalizations

| Excuse the agent might generate | Required rebuttal |
| --- | --- |
| "We're B2B only, so CCPA doesn't apply." | CPRA applies when you process **California consumers'** PI—B2B contacts may still be consumers; assess actual data not business model label. |
| "LLM vendor is a service provider, so no disclosure needed." | **Service provider status requires a qualifying contract** and limited use—default API terms often fail; verify §1798.140(ag). |
| "Agent logs aren't 'personal information'." | Logs with identifiers, inferences, or linked account data **are PI** under §1798.140(v). |
| "We don't sell data—we just share with ad partners." | CPRA **"share"** for cross-context behavioral advertising triggers **opt-out** rights—distinct from colloquial "sale." |
| "DSAR delete is impossible because LLM trained on it." | Training use should be **contractually prohibited**; if occurred, legal review required—do not claim impossibility without vendor confirmation. |
| "GPC doesn't apply to us yet." | CPPA regulations treat **GPC as opt-out signal** for applicable businesses—implement technical honor or document exemption basis with counsel. |

## Red Flags

- Consumer PI sent to LLM without service provider agreement restricting secondary use
- No mechanism to delete agent session history per verified DSAR
- Privacy policy missing SPI categories or Limit the Use link when SPI collected
- Analytics/ad SDKs active after consumer opt-out of sale/share
- Postgres MCP evidence database retains consumer PI indefinitely without retention policy
- DSAR responses include other consumers' PI (over-disclosure)
- Verification process collects more PI than necessary (SSN required for all requests)
- GPC signal ignored on website where regulations apply

## Verification

- [ ] Data map complete for California consumer PI including agent/LLM flows
- [ ] Business vs service provider vs third party roles documented per vendor
- [ ] All six consumer rights have documented processes, owners, and SLAs
- [ ] DSAR intake, verification, and fulfillment tested with sample request (synthetic data)
- [ ] Privacy policy and notice at collection reviewed against §1798.130/§1798.135
- [ ] LLM and MCP vendor contracts include CPRA service provider provisions
- [ ] Sale/share analysis complete with opt-out and GPC technical controls verified
- [ ] SPI Limit the Use mechanism implemented where required
- [ ] Agent log retention and deletion automation documented and tested
- [ ] Evidence package hashed with engagement ID and audit timestamp
