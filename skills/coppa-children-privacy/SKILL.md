---
name: coppa-children-privacy
description: Implements FTC COPPA (15 U.S.C. §6501–6506; 16 CFR Part 312) for operators of websites, apps, and AI agents directed to children under 13 or with actual knowledge of child users—verifiable parental consent, data minimization, retention, security, and third-party LLM/MCP subprocessors. Trigger when building consumer apps, chatbots, or agents used by children, auditing EdTech with under-13 users outside school official context, or reviewing parental consent flows and vendor DPAs. Do not use for FERPA school official deployments (use ferpa-education-records), HIPAA pediatric clinical data (use hipaa-technical-safeguards), or general teen users 13+ (use us-state-privacy-laws / ccpa-cpra-privacy-rights).
---

# COPPA Children's Privacy

## Overview

The **Children's Online Privacy Protection Act (COPPA)**, enforced by the **FTC**, regulates operators collecting **personal information** from children **under 13**.

| Requirement | Rule cite | Agent/AI relevance |
| --- | --- | --- |
| **Operator** | §312.2 | SaaS running child-directed agent = operator |
| **Personal information** | §312.2 | Name, email, voice, photos, persistent IDs, prompts with child PII |
| **Direct notice to parents** | §312.4 | Before collection—what LLM/MCP receives |
| **Verifiable parental consent (VPC)** | §312.5 | Before most collection—limited exceptions |
| **Data minimization** | §312.2 (2025 Rule updates) | Collect only reasonably necessary |
| **Retention / deletion** | §312.10 | Delete when no longer needed |
| **Security** | §312.8 | Reasonable procedures—redaction, access control |
| **Service providers** | §312.2 | LLM vendor as service provider with written agreement |

**2025 COPPA Rule amendments** (phased): strengthen VPC, limit push notifications, restrict disclosure for targeted advertising, data retention limits—verify effective dates for your compliance calendar.

**School exception:** COPPA does **not** apply when collecting from child **at direction of school** under FERPA school official arrangement—use `ferpa-education-records` for that path.

## When to Use

Use this skill when:

- **Child-directed** app, game, or chatbot (including AI agent UI)
- **Mixed audience** with **actual knowledge** user is under 13
- Designing **parental consent** and **direct notice** flows before agent chat
- **LLM/MCP vendors** process children's voice, prompts, or persistent IDs
- **FTC compliance review** or Safe Harbor program alignment
- **Advertising/analytics** in child contexts (strict limits)

Do **not** use this skill when:

- School acts as agent under FERPA DPA only (use `ferpa-education-records`)
- Users confirmed 13+ with age gate (state teen laws may apply separately)
- Anonymous play with no PI collection (confirm no persistent IDs)

## Core Process

Execute steps **in order**.

### Step 1: Operator determination and audience

1. Is service **child-directed** (§312.2)—subject matter, visual content, music, use of animated characters, child celebrities?
2. **Mixed audience**: age screen + **actual knowledge** triggers if under-13 user identified.
3. Document **operator** entity responsible for agent (not disclaimable to LLM vendor alone).
4. Artifact: COPPA applicability memo.

### Step 2: Personal information inventory

1. List all PI collected from children via agent:
   - Registration, prompts, voice, photos, geolocation, device IDs, cookies
   - **Inference** from prompts (school name + grade = PI)
2. Map flows to **LLM API**, **MCP Postgres**, analytics, crash logs.
3. **Minimize**: do not collect PI in prompts unless essential—use `redaction.py` and session tokens.

### Step 3: Direct notice to parents (§312.4)

Before collection, provide parents:

1. **Types** of PI collected and how used (including AI training—must disclose)
2. **Disclosure** practices to third parties (LLM subprocessors by name/category)
3. Parent **rights**: review, delete, refuse further collection
4. Link to online notice; separate direct notice for **school+parent** contexts if hybrid.

Populate `templates/coppa-parental-consent.yaml` notice section.

### Step 4: Verifiable parental consent (§312.5)

1. Obtain **VPC** before collecting, using, or disclosing PI (except limited exceptions):
   - **Internal operations** support (strictly defined)
   - **One-time contact** / respond to child request (no retention)
   - **Safety** emergencies
2. Approved VPC methods (Rule): print-and-fax, toll-free, video, government ID check, credit card micro-charge, approved Safe Harbor, etc.
3. **Email plus** additional step for higher-risk uses.
4. **Agent chat for under-13** without VPC = violation unless within exception.

### Step 5: Service provider agreements (LLM/MCP)

1. Written agreement per §312.2:
   - Process PI **only** for operator's service provision
   - **No** independent use, advertising profile, or model training on child PI
   - **Security** and **deletion** on operator request
2. Map OpenAI/Anthropic/other **API data usage** policies to COPPA commitments.
3. Subprocessor list in privacy policy.

### Step 6: Data retention and deletion (§312.10)

1. Retain PI **only as long as reasonably necessary** for purpose collected.
2. Agent session logs: define TTL; automated purge job on MCP Postgres.
3. Parent **deletion requests**—cascade to LLM vendor per contract.
4. Document exceptions (legal hold, safety).

### Step 7: Security (§312.8)

1. Reasonable security appropriate to sensitivity:
   - Encryption in transit, access controls, MFA for admin
   - **Presidio redaction** before sending child PI to LLM where possible
   - **Deanonymize opt-in off** in child agent paths
2. Integrate `access-control-identity-audit` and `mcp-compliance-integration`.

### Step 8: Prohibited practices and advertising

1. **No conditioning** participation on disclosing more PI than necessary.
2. **Targeted advertising** to children heavily restricted under amended Rule—audit SDKs.
3. **Push notifications** and **precise geolocation**—enhanced consent under amendments.
4. Agent **must not** encourage children to share excess PI in prompts—system prompts and UX review.

### Step 9: Safe Harbor and FTC readiness

1. Optional FTC-approved **Safe Harbor** programs for compliance defense.
2. Maintain **consent logs**, deletion records, vendor audits.
3. Prepare for **Civil Investigative Demand** documentation package.

## Common Rationalizations

| Excuse | Rebuttal |
| --- | --- |
| "We're general audience—COPPA doesn't apply." | **Actual knowledge** of under-13 user triggers COPPA regardless of intent. |
| "Parents agreed in T&C." | COPPA requires **verifiable** parental consent—not browsewrap alone. |
| "LLM vendor handles privacy." | **Operator** remains liable—must contractually bind service providers. |
| "We don't store chats." | Vendor-side retention/training still counts if PI was **disclosed** to them. |
| "School uses our app—COPPA exempt." | School direction may invoke **FERPA path**—must meet school official requirements, not ignore COPPA blindly. |

## Red Flags

- Under-13 registration or age gate bypass
- Child voice/audio sent to LLM without VPC and disclosure
- Analytics/ad SDKs in child-directed agent app
- No written LLM service provider agreement limiting training on child PI
- Indefinite retention of child chat logs in MCP Postgres
- Agent system prompt encouraging personal details from children

## Verification

- [ ] COPPA applicability (child-directed / actual knowledge) documented
- [ ] PI inventory mapped through agent, LLM, and MCP chain
- [ ] Direct notice to parents complete and current
- [ ] VPC obtained before collection (or valid exception documented)
- [ ] Service provider agreements with LLM/MCP vendors executed
- [ ] Retention/deletion policy implemented with automation
- [ ] Security controls aligned to §312.8
- [ ] Advertising/push/geolocation restrictions reviewed under amended Rule
- [ ] Consent and deletion audit logs maintained
