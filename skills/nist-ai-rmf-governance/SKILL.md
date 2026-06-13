---
name: nist-ai-rmf-governance
description: Implements NIST AI Risk Management Framework (AI RMF 1.0, NIST AI 100-1)—GOVERN, MAP, MEASURE, and MANAGE functions—for trustworthy AI systems including LLM agents, MCP toolchains, and automated compliance workflows. Trigger when assessing AI governance, model risk, agent trustworthiness, GenAI deployment controls, or harmonizing AI RMF with NIST CSF 2.0 and ISO 42001 concepts. Do not use for general cybersecurity without AI scope (use nist-csf-2-assessment), HIPAA PHI controls alone (use hipaa-technical-safeguards), or EU AI Act (out of scope—use gdpr-us-multinational for privacy overlap only).
---

# NIST AI RMF Governance

## Overview

The **NIST AI Risk Management Framework (AI RMF 1.0)** (NIST AI 100-1, January 2023) provides voluntary guidance for **trustworthy AI** across four core functions:

| Function | Purpose | Agent/LLM relevance |
| --- | --- | --- |
| **GOVERN** | Culture, policies, accountability, workforce | AI governance board, agent approval process |
| **MAP** | Context, categorization, impacts, benefits/risks | Agent use-case inventory, stakeholder harm analysis |
| **MEASURE** | Metrics, evaluation, TEVV, documentation | Redaction FN/FP rates, prompt injection tests, bias evals |
| **MANAGE** | Prioritize, respond, recover, communicate | Kill switches, MCP allowlists, incident playbooks |

**Trustworthy AI characteristics** (NIST): valid & reliable, safe, secure & resilient, accountable & transparent, explainable & interpretable, privacy-enhanced, fair with harmful bias managed.

**Companion resources:** [NIST AI RMF Playbook](https://airc.nist.gov/AI_RMF), Generative AI profile (NIST AI 600-1), cross-walk to **NIST CSF 2.0** (`nist-csf-2-assessment`).

This skill is the **primary AI-specific governance** path for compliance-agent-skills deployments.

## When to Use

Use this skill when:

- **Deploying or auditing** LLM agents, MCP servers, or GenAI in regulated workflows
- Building **AI governance policies** (acceptable use, human oversight, model selection)
- **Mapping AI risks** for compliance agents processing PHI, PCI, or PII
- **TEVV** (test, evaluation, verification, validation) for agent outputs and tool calls
- **Executive/board** AI risk reporting using NIST taxonomy
- Harmonizing with **SOC 2** (CC8 change, CC7 monitoring) and **ISO 27001** for AI systems
- Customer **AI due diligence** questionnaires (NIST AI RMF, SOC 2 + AI addendum)

Do **not** use this skill when:

- Pure infrastructure security with no AI/ML (use `nist-csf-2-assessment`)
- PHI redaction tuning only (use `hipaa-phi-redaction-pipeline`)
- Children's data FTC rules (use `coppa-children-privacy`)
- Student education records (use `ferpa-education-records`)

## Core Process

Execute steps **in order**.

### Step 1: GOVERN — AI accountability structure

1. Document **AI system inventory**: agents, models, MCP tools, embeddings, fine-tunes.
2. Assign roles: executive sponsor, AI risk owner, legal/privacy, security, domain experts.
3. Policies required:
   - Acceptable use for LLM prompts (no raw PHI/PAN without redaction)
   - Human-in-the-loop for high-impact decisions
   - Model/vendor change management (CC8.1 alignment)
4. Artifact: AI governance charter + RACI matrix.

### Step 2: MAP — Context and risk framing

1. For each agent use case document:
   - **Intended purpose** and **context of use**
   - **Actors**: users, subjects, operators, third parties (LLM vendor)
   - **Data types**: ePHI, PI, CHD, CUI, public
   - **Benefits** and **potential harms** (individual, group, societal)
2. Categorize **risk tier** (low / moderate / high) based on autonomy, data sensitivity, reversibility.
3. Map dependencies: `agent.py` redaction gate, `mcp-compliance-integration`, vendor BAAs/DPAs.
4. Populate `templates/nist-ai-rmf-profile.yaml` MAP section.

### Step 3: MAP — Impacts and likelihood

1. Identify **failure modes**:
   - Hallucinated regulatory citations (`using-compliance-agent-skills` anti-patterns)
   - Prompt injection via MCP tools
   - Deanonymization without authorization (`agent.py` opt-in)
   - Tool over-permission (Postgres MCP write access)
2. Document **trustworthiness gaps** per NIST characteristics.
3. Cross-reference loaded skills — agent must not invent controls.

### Step 4: MEASURE — Metrics and TEVV

1. Define **measurable metrics**:
   | Metric | Example target |
   | --- | --- |
   | Redaction false negative rate | 0% on SSN in test corpus |
   | Skill routing accuracy | 100% framework match on test prompts |
   | Unauthorized tool call rate | 0 in audit mode |
   | Human override rate | Tracked for high-tier use cases |
2. **TEVV plan**:
   - Pre-deployment: `compliance_tests/` corpus, adversarial prompts
   - Production: CCM alerts on deanonymize flag, MCP anomaly detection
3. Document evaluation datasets — **synthetic only** in CI; no production PHI.
4. Populate MEASURE section in AI RMF profile template.

### Step 5: MEASURE — Documentation and transparency

1. **Model cards / system cards** for agent stack: base model, skills loaded, redaction profile, MCP tools.
2. User-facing disclosure when interacting with AI agent (FTC/state AI transparency trends).
3. Log retention for audit — align `audit-logging-integrity`.

### Step 6: MANAGE — Risk treatment

1. Prioritize risks by tier and exploitability.
2. Controls (map to repo capabilities):
   - **Technical**: Presidio balanced profile, MCP OAuth, audit mode hooks
   - **Process**: `/scope` before `/audit`, one primary skill per thread
   - **Human**: Privacy officer sign-off on breach-tier agent outputs
3. **Residual risk** acceptance with executive sign-off for high-tier deployments.

### Step 7: MANAGE — Continuous monitoring and incidents

1. Integrate with `soc2-ccm-continuous-monitoring` for drift detection.
2. AI-specific incidents: model behavior change, vendor breach, jailbreak — route to `breach-incident-response`.
3. **Change management** when adding skills, MCP servers, or model versions — re-run MAP/MEASURE delta.

### Step 8: Profile completion and roadmap

1. Complete Current vs Target profile in `templates/nist-ai-rmf-profile.yaml`.
2. 12-month improvement plan with owners.
3. Cross-walk high-priority controls to NIST CSF 2.0 subcategories for unified reporting.

## Common Rationalizations

| Excuse | Rebuttal |
| --- | --- |
| "We're just wrapping GPT—no AI risk." | **Agent orchestration** with tools and regulated data is in scope for AI RMF GOVERN/MAP. |
| "CSF 2.0 covers everything." | CSF addresses cyber; **AI RMF adds TEVV, bias, transparency, GenAI failures** not in CSF alone. |
| "Vendor's AI ethics statement is enough." | **Accountability stays with deployer**—document MAP and MEASURE for your agent configuration. |
| "Redaction solves AI privacy." | Redaction supports privacy-enhanced AI but does not address **validity, safety, or explainability**. |
| "No metrics—we'll eyeball outputs." | AI RMF MEASURE requires **documented TEVV**—use test corpus and routing validation. |

## Red Flags

- Production agent without AI use-case inventory or risk tier
- MCP tools with write access and no human oversight on high-tier flows
- No TEVV before adding new framework skills to production
- Deanonymization enabled globally in EU or HIPAA paths
- Model version changes without change-management record
- Customer-facing agent with no disclosure of automated assistance

## Verification

- [ ] GOVERN: AI inventory, RACI, and acceptable-use policy documented
- [ ] MAP: Use cases with harms, data types, and risk tiers completed
- [ ] MEASURE: Metrics and TEVV plan with synthetic test corpus referenced
- [ ] MEASURE: System/model card for agent stack published internally
- [ ] MANAGE: Risk treatment and residual risk sign-off for high-tier cases
- [ ] MANAGE: CCM and incident hooks integrated for AI-specific events
- [ ] AI RMF profile template completed with Current/Target states
- [ ] Cross-walk to NIST CSF 2.0 documented where required
