---
name: ferpa-education-records
description: Implements FERPA (20 U.S.C. §1232g; 34 CFR Part 99) protections for student education records in EdTech, LMS integrations, and AI tutoring agents—school official exceptions, legitimate educational interest, directory information, parent/eligible student rights, and vendor DPAs. Trigger when K-12 or higher-ed systems process student records, deploying AI agents in classrooms, auditing EdTech subprocessors, or assessing LLM use with FERPA-regulated data. Do not use for HIPAA PHI in clinical settings (use hipaa-technical-safeguards), COPPA under-13 consumer apps without school context (use coppa-children-privacy), or general PII without education record nexus (use us-state-privacy-laws).
---

# FERPA Education Records

## Overview

The **Family Educational Rights and Privacy Act (FERPA)** protects **education records**—records directly related to a student maintained by an educational agency or institution (or party acting on its behalf).

| Concept | Regulation | Agent/EdTech relevance |
| --- | --- | --- |
| **Education record** | 34 CFR §99.3 | Grades, discipline, IDs, biometrics, AI chat logs tied to student |
| **Personally identifiable information (PII)** | §99.3 | Name + student ID in agent prompts = FERPA PII |
| **School official** | §99.31(a)(1) | LLM vendor may be school official with DPA + LEA |
| **Legitimate educational interest** | §99.31(a)(1)(i) | Agent must have LEA-defined purpose |
| **Directory information** | §99.37 | Opt-out affects what agents may disclose |
| **Parent/eligible student rights** | §99.10–99.12 | Access, amend, consent to disclose |
| **Recordation** | §99.32 | Audit log of disclosures from agent systems |

**HIPAA interaction:** Most K-12 health records in education records are **FERPA**, not HIPAA (except school nurse as covered entity in narrow cases—legal review).

**AI agents:** Tutoring bots, grading assistants, and analytics pipelines that store **prompts with student identity** are high-risk FERPA systems.

## When to Use

Use this skill when:

- **EdTech SaaS** or **district** deploys AI agents accessing student data
- Drafting **Data Processing Agreements** with LLM/MCP vendors as school officials
- **Legitimate educational interest** analysis for new agent features
- **Parent consent** or notification for directory information / disclosures
- **Audit** of agent logs, MCP Postgres, or Slack for improper redisclosure
- **State student privacy laws** overlay (SOPIPA, PPRA, state §)—FERPA is floor

Do **not** use this skill when:

- De-identified research datasets with no student IDs (may be outside FERPA—confirm)
- Pure COPPA consumer app not acting as school agent (use `coppa-children-privacy`)
- Employee (faculty) HR records (not education records)
- PCI payment for tuition without student academic data

## Core Process

Execute steps **in order**.

### Step 1: Education record inventory

1. Map systems: LMS, SIS, agent gateway, MCP evidence DB, LLM vendor logs.
2. Classify data elements per student:
   - **Education record** vs directory information vs de-identified
   - **Biometric** (voice/face in agent)—treat as sensitive PII
3. Document **who maintains** each record (LEA vs vendor).
4. Artifact: `templates/ferpa-school-official.yaml` inventory section.

### Step 2: School official and subcontractor chain

1. Vendor qualifies as **school official** only if (34 CFR §99.31(a)(1)):
   - Performs institutional service/function
   - Under **direct control** regarding use/maintenance of records
   - **DPA** meets §99.31(a)(1) requirements (use template)
2. Map **LLM provider** role: subprocessors require LEA approval and flow-down terms.
3. **MCP servers** holding student data = extensions of vendor/LEA—same control requirements.
4. Prohibit **training** vendor models on identifiable education records without consent.

### Step 3: Legitimate educational interest (LEI)

1. For each agent capability, document:
   - **Educational purpose** (tutoring, feedback, compliance audit of IT—not marketing)
   - **Scope** of records accessed (minimum necessary)
   - **Role** of user (teacher, admin, student)
2. Deny agent access where LEI cannot be articulated (e.g., unrelated LLM experimentation).
3. Align with `hipaa-privacy-minimum-necessary` conceptually—FERPA uses LEI instead.

### Step 4: Consent and directory information

1. **Directory information** (name, email, grade level)—annual notice + opt-out per §99.37.
2. Agent must **not** combine directory info with non-directory records for unauthorized parties.
3. **Redisclosure** rules §99.33: agent outputs to unauthorized third parties = violation.
4. **Parent/eligible student** consent required for non-excepted disclosures (§99.30).

### Step 5: Technical safeguards for agents

1. **Authentication**: student vs teacher RBAC (`access-control-identity-audit`).
2. **Redaction**: use `hipaa-phi-redaction-pipeline` patterns for student names/IDs in logs sent to LLM—prefer **pseudonymous session IDs** in prompts.
3. **Audit trail** §99.32: log each disclosure from agent (who, what record, recipient, purpose).
4. **Deanonymization** in `agent.py` — disable for student-facing production paths unless authorized.

### Step 6: Parent and eligible student rights

1. **Inspection** §99.10: provide access to education records including agent interaction logs tied to student.
2. **Amendment** §99.20: process to correct inaccurate records (including wrong AI-generated summaries in record).
3. **Hearing** procedures if amendment denied.
4. DSAR-style workflows — use structured export, not raw LLM summarization of other students' data.

### Step 7: Breach and improper disclosure

1. FERPA has **no federal breach notification statute** like HIPAA. However:
   - Contract and **state laws** may require notification
   - **FTC** and state AG for EdTech deceptive practices
2. Route confirmed leaks to `breach-incident-response` + legal.
3. Document in disclosure log §99.32.

### Step 8: Evidence and audit

1. DPA signed with all school officials (LLM, MCP host, analytics).
2. LEI matrix approved by LEA privacy officer.
3. Annual FERPA training for staff operating agents.
4. SHA-256 evidence manifest for audit binders.

## Common Rationalizations

| Excuse | Rebuttal |
| --- | --- |
| "We're a vendor—not subject to FERPA." | Vendors handling records **on behalf of LEA** are bound by contract and §99.31(a)(1) school official terms. |
| "Chat logs aren't education records." | Logs **directly related to a student** and maintained by institution/vendor are records under §99.3. |
| "LLM is ephemeral—no FERPA." | Vendor **retention**, caching, and training policies determine compliance—not user assumption. |
| "De-identified prompts are fine." | Re-identification via session context may still link to student—use pseudonymization policy. |
| "Teachers can paste any student data into the agent." | **LEI and minimum access** must govern—even teacher misuse is institutional control failure. |

## Red Flags

- LLM vendor DPA missing school official / FERPA clauses
- Agent prompts contain student names + grades with no LEI documentation
- MCP Postgres shared across schools without tenant isolation
- No §99.32 disclosure logging for agent exports
- Directory information used in agent training data
- Parent access request answered by unredacted LLM dump of all chats

## Verification

- [ ] Education record inventory and maintainer roles documented
- [ ] School official DPAs executed for LLM/MCP/analytics vendors
- [ ] LEI matrix approved for each agent capability
- [ ] Directory information notice and opt-out process current
- [ ] Technical RBAC, redaction/pseudonymization, and audit logging implemented
- [ ] Parent/eligible student access and amendment procedures defined
- [ ] Improper disclosure playbook linked to incident response
- [ ] Evidence package with privacy officer sign-off
