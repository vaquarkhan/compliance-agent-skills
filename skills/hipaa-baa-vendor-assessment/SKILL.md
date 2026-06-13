---
name: hipaa-baa-vendor-assessment
description: Reviews Business Associate Agreements and subprocessors for LLM vendors, cloud providers, and MCP server operators under HIPAA (45 CFR §164.502(e), §164.504(e)). Trigger when onboarding OpenAI/Anthropic/Azure OpenAI, cloud hosts, observability tools, or MCP integrations that may access ePHI. Do not use for technical encryption testing (use hipaa-technical-safeguards) or general vendor SOC reports without BAA focus (use vendor-third-party-risk).
---

# HIPAA BAA Vendor Assessment

## Overview

This skill performs structured **Business Associate Agreement (BAA)** review for vendors that create, receive, maintain, or transmit **ePHI** on behalf of a covered entity or business associate. Key regulations:

- **45 CFR §164.502(e)**: BA may use/disclose ePHI only per BAA or law
- **45 CFR §164.504(e)**: Required BAA provisions
- **45 CFR §164.308(b)(1)**: Business associate contracts and other arrangements

LLM and MCP ecosystems introduce non-obvious subprocessors: model hosts, vector DBs, prompt logging, crash reporters, and MCP registry operators. This skill produces a **vendor-by-vendor compliance matrix** with pass/fail on mandatory BAA clauses—not a substitute for legal counsel.

## When to Use

Use this skill when:

- Onboarding an **LLM provider** (OpenAI, Anthropic, Azure OpenAI, AWS Bedrock) for ePHI-adjacent workloads
- Evaluating **cloud infrastructure** (AWS, GCP, Azure) for HIPAA workloads
- Assessing **MCP server** operators or self-hosted MCP with third-party dependencies
- Reviewing **observability, logging, or support tools** that may capture prompts/responses
- Annual **BAA renewal** or subprocessor change notification review
- Determining whether a vendor is a **Business Associate** vs **conduit** exception

Do **not** use this skill when:

- Vendor handles only de-identified data with expert determination (confirm de-identification first)
- Pure PCI card processing without ePHI (use PCI skills)
- Technical control testing of encryption (use `hipaa-technical-safeguards`)

## Core Process

Execute steps **in order**.

### Step 1: Vendor inventory and BA determination

1. List all vendors in the ePHI processing chain:
   - LLM API provider, cloud host, MCP server host, CDN, email, ticketing, SIEM
2. For each vendor, determine status:
   - **Business Associate**: accesses ePHI on behalf of CE/BA → BAA **required**
   - **Conduit**: transient access only (e.g., TLS VPN pipe)—document narrow exception analysis
   - **Not in scope**: no ePHI access—document exclusion rationale
3. Record: `vendor-inventory-{id}.csv` with data types, access mode, BAA status.

### Step 2: BAA availability verification

1. Confirm vendor offers a **HIPAA BAA** (signed or click-through for cloud).
2. Verify BAA covers the **specific services** in use (e.g., Azure OpenAI vs general Azure—not all SKUs are covered).
3. For LLM vendors, confirm:
   - **Zero data retention** / no training on customer data (contractual, not marketing)
   - Geographic processing restrictions if required
   - Subprocessor list and notification process
4. **BLOCK** production ePHI flows to vendors without executed BAA.

### Step 3: Mandatory BAA clause checklist (§164.504(e))

Review executed or draft BAA for each required element:

| §164.504(e) element | Pass criteria |
| --- | --- |
| Permitted uses/disclosures | Limited to BAA, CE instruction, or law |
| Safeguards | Appropriate safeguards per Security Rule |
| Subcontractors | BA requires same restrictions via subcontractor agreement |
| Report breaches | BA reports breaches to CE per §164.410 |
| Access/amendment/accounting | BA supports individual rights where applicable |
| HHS access | BA makes internal practices available to HHS |
| Termination | CE may terminate if BA violates material terms |
| Return/destruction | ePHI returned or destroyed at termination |

Mark each **PASS**, **FAIL**, or **NEEDS LEGAL REVIEW**.

### Step 4: LLM-specific addendum review

For each LLM vendor, verify contractual terms on:

1. **Input/output logging**: what is logged, retention period, who can access
2. **Model training**: explicit prohibition on training/fine-tuning on customer ePHI
3. **Human review**: opt-out of human review of prompts containing ePHI
4. **Region/data residency**: matches organizational policy
5. **API metadata**: request IDs in logs—confirm they cannot reconstruct ePHI alone
6. **Enterprise vs consumer tier**: consumer tiers often **lack BAA**—FAIL if used for ePHI

### Step 5: MCP server operator assessment

For each MCP server processing ePHI:

1. Identify **operator** (self-hosted, vendor-hosted, open-source with cloud telemetry).
2. Determine if operator accesses ePHI (tool inputs/outputs, server logs).
3. Require BAA or confirm operator is **within CE boundary** (employee/contractor under CE policies).
4. Review MCP dependency chain: npm packages with phone-home, crash analytics.
5. Document tool allowlist—MCP operator should not have broader access than BAA permits.

### Step 6: Subprocessor cascade

1. Obtain vendor **subprocessor list** (LLM → cloud → CDN → support SaaS).
2. Verify flow-down obligations in BAA.
3. Flag new subprocessors added since last review.
4. Map subprocessors to ePHI exposure (HIGH: prompt storage; LOW: physical datacenter with no logical access).

### Step 7: Gap remediation and risk acceptance

1. FAIL items: block ePHI until remediated or alternative vendor selected.
2. NEEDS LEGAL REVIEW: escalate with clause citation—do not auto-approve.
3. Document compensating controls only with legal and privacy officer approval.
4. Set BAA renewal calendar (annual minimum; 90-day subprocessor review).

### Step 8: Evidence packaging

1. Store executed BAAs (redacted signatures if needed), subprocessor lists, assessment matrix.
2. SHA-256 hash all documents; link to vendor inventory IDs.
3. Produce summary for privacy officer sign-off.

## Common Rationalizations

| Excuse the agent might generate | Required rebuttal |
| --- | --- |
| "We redact PHI, so no BAA is needed with the LLM vendor." | Residual ePHI or re-identification risk may remain; **vendor role** is determined by access capability, not intent. Legal must confirm conduit/de-identified exceptions. |
| "Enterprise API terms say HIPAA—good enough without signed BAA." | Marketing language ≠ **executed BAA** with §164.504(e) clauses. |
| "MCP is open source, so there's no vendor." | **Operator** of the running instance and its telemetry dependencies may still be a BA. |
| "Subprocessors are the vendor's problem." | CE/BA retains **oversight obligation**—subprocessor notification must be monitored. |
| "Consumer ChatGPT Plus works for clinical summaries." | Consumer products typically **lack BAA**—automatic FAIL for ePHI. |
| "BAA review can wait until after pilot." | Pilot with real ePHI **is production** under HIPAA—BAA must precede ePHI flow. |

## Red Flags

- Production ePHI sent to LLM without executed BAA
- Consumer-tier LLM account used for clinical workflows
- Vendor subprocessor added with ePHI access and no notification review
- BAA missing breach notification or termination for cause clauses
- MCP server logs full tool payloads to non-BAA analytics
- "Conduit" exception claimed for vendor that stores prompts
- Verbal vendor assurance substituted for contractual BAA language

## Verification

- [ ] Complete vendor inventory with BA/conduit/not-in-scope determination
- [ ] Executed BAA on file for every BA vendor before ePHI processing
- [ ] §164.504(e) checklist completed for each BAA
- [ ] LLM-specific addendum reviewed (training, logging, human review, tier)
- [ ] MCP operators assessed with dependency chain documented
- [ ] Subprocessor list current with change notification process verified
- [ ] FAIL items blocked or remediated—none silently waived
- [ ] Legal review queue documented for ambiguous clauses
- [ ] Evidence bundle hashed with privacy officer sign-off field
- [ ] BAA renewal and subprocessor review dates scheduled
