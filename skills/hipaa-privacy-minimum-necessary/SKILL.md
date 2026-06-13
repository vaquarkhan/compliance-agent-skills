---
name: hipaa-privacy-minimum-necessary
description: Implements HIPAA Privacy Rule minimum necessary standard—45 CFR §164.502(b)—plus §164.514 de-identification, Limited Data Sets, and patient rights to access and amend records, with agent prompt minimization, role-based PHI exposure, and integration with the Presidio redaction pipeline. Trigger when designing LLM/agent PHI access policies, auditing disclosure practices, implementing patient rights workflows, or validating that agent prompts contain only minimum necessary ePHI. Do not use for Presidio entity tuning alone (use hipaa-phi-redaction-pipeline), Security Rule technical controls (use hipaa-technical-safeguards), or BAA legal review (use hipaa-baa-vendor-assessment).
---

# HIPAA Privacy Minimum Necessary

## Overview

This skill operationalizes the **HIPAA Privacy Rule** standards for **minimum necessary** use and disclosure of protected health information (PHI), **de-identification**, **Limited Data Sets**, and **individual rights**. Primary citations:

| Topic | Citation |
| --- | --- |
| Minimum necessary | **45 CFR §164.502(b)** — covered entities and BAAs |
| Minimum necessary policies | **45 CFR §164.514(d)** — implementation specifications |
| De-identification (Safe Harbor / Expert Determination) | **45 CFR §164.514(a)–(b)** |
| Limited Data Set | **45 CFR §164.514(e)** — data use agreement required |
| Patient access to PHI | **45 CFR §164.524** |
| Amendment of PHI | **45 CFR §164.526** |
| Accounting of disclosures | **45 CFR §164.528** (where applicable) |

**Minimum necessary** requires covered entities and business associates to **limit PHI** to the minimum needed to accomplish the intended purpose. For **AI agents**, this means:

- Prompts to LLMs contain **only fields required** for the compliance task—not full charts
- **Role-based** exposure: auditor role ≠ billing role ≠ clinical role
- **Redaction upstream** via `redaction.py` before LLM reasoning—complements `hipaa-phi-redaction-pipeline`
- **No reconstruction** of redacted tokens in model context unless authorized downstream delivery

The **Security Rule** (§164.312) technical controls are addressed in `hipaa-technical-safeguards`; this skill focuses on **Privacy Rule** use/disclosure limits.

## When to Use

Use this skill when:

- **Designing agent workflows** that may process ePHI (compliance audits, chart review assistants)
- Auditing whether current LLM prompts/logs exceed **minimum necessary**
- Implementing **role-based PHI access** for agent operators and MCP tools
- Planning **de-identified** or **Limited Data Set** datasets for analytics/training
- Building **patient access** or **amendment** workflows touching agent-held data
- **Policy review** for §164.514(d) minimum necessary procedures
- Complementing redaction pipeline deployment with **organizational** privacy controls

Do **not** use this skill when:

- Tuning Presidio entity types and thresholds (use `hipaa-phi-redaction-pipeline`)
- Encryption, access control, audit logs under Security Rule (use `hipaa-technical-safeguards`)
- Vendor BAA clause negotiation (use `hipaa-baa-vendor-assessment`)
- California consumer privacy rights (use `ccpa-cpra-privacy-rights`)

## Core Process

Execute steps **in order**.

### Step 1: PHI flow and purpose mapping (§164.502(b))

1. Document each **agent use case** and its ** intended purpose** (treatment, payment, healthcare operations, or other with authorization).
2. Map PHI elements accessed per use case:

| Use case | PHI elements | Purpose | Minimum necessary? |
| --- | --- | --- | --- |
| HIPAA gap audit | Policies, configs (no clinical) | Operations | Yes |
| Clinical coding assist | Diagnosis, procedures | Treatment | Partial—review scope |
| Full chart summarization | Entire note | Unclear | Likely **excessive** |

3. Identify **routine disclosures** vs **non-routine** (§164.514(d)(3)—non-routine requires case-by-case minimum necessary review).
4. Artifact: `phi-purpose-map-{id}.json`.

### Step 2: Minimum necessary policies (§164.514(d))

1. Verify organizational policies define:
   - **Roles and classes of persons** who need access to PHI
   - **Categories of PHI** accessible per role
   - **Conditions** appropriate for access (§164.514(d)(2))
2. For **non-routine requests**, document case-by-case review process.
3. **Standard disclosures** (e.g., to HHS)—document limited data sets permitted.
4. Map agent service accounts to **human role equivalents**—MCP Postgres roles must mirror policy.

### Step 3: Agent prompt minimization

1. Audit sample agent prompts (redacted captures only) against purpose map:
   - Remove **demographics not needed** for task (e.g., full address for policy audit)
   - Remove **dates** not needed (over-redaction preferred over under-collection)
   - Use **structured fields** instead of full narrative notes where possible
2. Implement **prompt templates** per skill/task with explicit PHI field allowlists.
3. Verify `agent.py` pipeline:
   - Redaction runs **before** `compliance_agent.run()`
   - System instructions prohibit requesting additional PHI from user
4. **FAIL** if prompts include entire EMR exports for narrow compliance questions.

### Step 4: Role-based PHI exposure

1. Define RBAC matrix for agent operators and tools:

| Role | Agent skills allowed | MCP tools | PHI categories |
| --- | --- | --- | --- |
| Compliance auditor | hipaa-*, soc2-* | Read-only Postgres (config) | No clinical PHI |
| Privacy officer | + hipaa-privacy-* | Presidio, evidence DB | De-identified + LDS |
| Break-glass clinical | Restricted | Full read with logging | Full PHI—time-bound |

2. Enforce via IAM, MCP OAuth scopes, and Postgres row/column policies—cross-ref `access-control-identity-audit`.
3. Deanonymization (`deanonymize_response`) restricted to roles with documented need.

### Step 5: De-identification (§164.514(a)–(b))

1. For datasets used in **analytics, ML, or broad agent testing**, apply:

**Safe Harbor method (§164.514(b)(2))** — remove 18 identifiers:
- Names, geographic subdivisions smaller than state, dates (except year), telephone, fax, email, SSN, MRN, health plan numbers, account numbers, certificate/license numbers, vehicle identifiers, device identifiers, URLs, IP addresses, biometric identifiers, full-face photos, other unique identifying numbers/characteristics/code

**Expert Determination (§164.514(b)(1))** — qualified expert documents re-identification risk is very small.

2. **Agent test corpora** must use synthetic or de-identified data—never production PHI in CI logs.
3. Document method in `de-identification-record-{id}.yaml`.

### Step 6: Limited Data Sets (§164.514(e))

1. If using LDS (may include city, state, ZIP, dates of service, age, dates of birth/death):
   - Execute **Data Use Agreement (DUA)** with recipient
   - Limit use to research, public health, or healthcare operations purposes stated in agreement
2. Agent accessing LDS must not **combine** with other data to re-identify.
3. LDS in LLM prompts still requires BAA and minimum necessary review—LDS ≠ unlimited disclosure.

### Step 7: Patient rights — access and amendment (§164.524, §164.526)

1. **Right of access**:
   - Provide access to PHI in designated record set within 30 days (§164.524(b))
   - If agent stores derived summaries, determine if part of designated record set—legal review if unclear
   - Access requests fulfilled without sending **other patients'** PHI to LLM
2. **Right to amend**:
   - Process amendment requests; if denied, document reason (§164.526)
   - If agent outputs incorrect PHI-derived conclusions, trigger amendment workflow—not silent correction in model only
3. Use **Postgres MCP read-only** for structured retrieval—never paste full database exports into LLM.

### Step 8: Integration with redaction pipeline

1. Confirm `hipaa-phi-redaction-pipeline` controls:
   - Entity coverage matches minimum necessary policy (don't redact then deanonymize unnecessarily)
   - Session `reset_session()` between patients/engagements
   - False negative testing for elements **intentionally excluded** from prompts
2. **Redaction ≠ minimum necessary alone**—redaction supports it but policy defines **which fields enter the pipeline at all**.
3. Presidio MCP (if used) must mirror local `redaction.py` thresholds per `mcp-compliance-integration`.

### Step 9: Findings and evidence

1. Emit findings:

```yaml
id: FIND-HIPAA-PRIV-001
severity: HIGH
control_id: 45CFR-164.502(b)
observation: "Agent prompt template includes full clinical note for billing audit task"
recommendation: "Restrict template to claim ID, procedure codes, and payer policy fields only"
owner: ""
due_date: null
status: open
```

2. Package: purpose map, RBAC matrix, policy excerpts, prompt audit samples (redacted), de-id records, hashes.

## Common Rationalizations

| Excuse the agent might generate | Required rebuttal |
| --- | --- |
| "Redaction handles minimum necessary—we send full charts." | Redaction **masks** PHI still sent to LLM—minimum necessary requires **not collecting** excess fields upstream. |
| "LLM needs context; more PHI means better answers." | Privacy Rule **limits** disclosure regardless of model performance—narrow the task or use de-identified data. |
| "De-identified Safe Harbor is too hard; we'll use production." | Production PHI in dev/test violates **minimum necessary** and Security Rule—use synthetic or de-identified corpora. |
| "All staff can use the agent—it's internal." | Internal access still requires **role-based** limits per §164.514(d)—standing access to all PHI fails. |
| "Limited Data Set means we can put it in any prompt." | LDS requires **DUA** and purpose limits—LLM vendor must be covered BAA with permitted uses. |
| "Patient access requests can go through the LLM for speed." | Access fulfillment must be **accurate and complete**—LLM summarization risks omission; use authoritative records. |

## Red Flags

- Full EMR notes or CCDA documents in agent prompts for narrow operational tasks
- MCP Postgres tool returns `SELECT *` from clinical tables without column restrictions
- Deanonymization available to all agent users without role check
- Production PHI in agent test logs or Slack MCP notifications
- No documented minimum necessary policy for agent use cases (§164.514(d))
- LDS used without executed Data Use Agreement
- Agent-derived patient summaries treated as source of truth for access requests
- Cross-patient PHI in single session without `reset_session()`

## Verification

- [ ] PHI purpose map complete for all agent use cases with minimum necessary assessment
- [ ] §164.514(d) minimum necessary policies documented and mapped to agent roles
- [ ] Prompt templates use field allowlists; sample audit shows no excess clinical PHI
- [ ] RBAC matrix enforced for operators, MCP tools, and deanonymization
- [ ] De-identification method documented for analytics/test data (Safe Harbor or Expert Determination)
- [ ] Limited Data Set agreements verified where LDS is used
- [ ] Patient access and amendment workflows defined for agent-held derived data
- [ ] Redaction pipeline integrated per hipaa-phi-redaction-pipeline with session isolation
- [ ] Findings logged with 45 CFR citations and remediation owners
- [ ] Evidence artifacts hashed with engagement ID and UTC timestamp
