---
name: soc2-evidence-collection
description: Automates SOC 2 evidence gathering—screenshots, configuration exports, access reviews, log samples, and audit-trail packaging with integrity hashes—for AICPA TSC examinations. Trigger when preparing audit binders, populating Vanta/Drata-style evidence requests, or packaging agent/MCP compliance artifacts. Do not use for control mapping (use soc2-trust-services-criteria) or continuous drift monitoring (use soc2-ccm-continuous-monitoring).
---

# SOC 2 Evidence Collection

## Overview

This skill implements **automated and semi-automated evidence collection** for SOC 2 Type I/II examinations. Evidence must be **complete, dated, tamper-evident, and mapped to TSC control IDs**. The agent uses MCP tools where available:

- **Playwright MCP**: screenshots, DOM/state captures for web admin consoles
- **Postgres MCP**: query exports for access lists, change tickets, control status
- **Slack MCP**: export approval messages (redacted) for change management evidence
- **Shell/API exports**: IAM policies, Terraform state metadata, cloud config snapshots

Every artifact receives a **SHA-256 hash** and entry in an evidence manifest suitable for auditor import.

## When to Use

Use this skill when:

- Building an **audit evidence binder** for SOC 2 Type I or Type II
- Responding to **auditor evidence requests** (ERDs, sample periods)
- Populating **GRC platform** evidence slots (Vanta, Drata, Secureframe alternatives)
- Packaging **quarterly control testing** results
- Collecting **point-in-time** and **period-of-time** samples (Type II requires continuous samples)
- Documenting agent/MCP compliance after running other skills (PCI, HIPAA)

Do **not** use this skill when:

- Defining which TSC controls apply (use `soc2-trust-services-criteria`)
- Real-time drift detection (use `soc2-ccm-continuous-monitoring`)
- Replacing auditor judgment on sample adequacy

## Core Process

Execute steps **in order**.

### Step 1: Evidence request intake

1. Obtain auditor evidence request list or map from TSC control matrix.
2. For each request, record:
   - Control ID (e.g., CC6.1, CC7.2)
   - Evidence type (screenshot, config export, log sample, policy PDF)
   - Sample period (for Type II: e.g., Q1–Q4 2025)
   - Population and sample size (auditor may specify)
3. Artifact: `evidence-request-register-{id}.csv`.

### Step 2: Collection plan and tool mapping

| Evidence type | Primary collection method | MCP/tool |
| --- | --- | --- |
| IAM user list + MFA status | Cloud API or IdP export | Shell, Postgres |
| Admin console screenshot | Authenticated browser capture | Playwright MCP |
| Firewall/security group rules | Cloud API JSON export | Shell |
| Change tickets | ITSM export | Postgres, API |
| Log sample (auth failures) | SIEM query export | Postgres, API |
| Policy documents | Document store hash | File read |
| Agent skill validation | Git commit + CI run | Shell |
| MCP access logs | Log aggregator export | Postgres |

Identify blocking gaps (missing MCP credentials, read-only access)—document before collection.

### Step 3: Automated collection execution

For each evidence item:

1. **Collect** using prescribed tool—do not manually recreate data that can be exported programmatically.
2. **Redact** ePHI/PII/secrets from evidence unless auditor specifically requires raw sample under NDA.
3. **Timestamp** collection in UTC; record collector identity (human or agent run ID).
4. **Hash** raw artifact: `sha256sum` equivalent; store in manifest.
5. **Name** files predictably: `{control-id}_{evidence-type}_{date}.{ext}`.

#### Playwright MCP screenshot protocol

1. Authenticate to target console via approved test account (not production admin unless authorized).
2. Navigate to exact page showing control (e.g., MFA enforcement policy).
3. Capture full-page screenshot including URL bar and timestamp overlay if available.
4. Save as PNG with manifest entry.

#### Postgres MCP export protocol

1. Run read-only queries against compliance/evidence schema only.
2. Export CSV/JSON; limit rows to sample size.
3. Verify query logged in audit trail.

### Step 4: Period-of-time sampling (Type II)

1. For each recurring control (access reviews, vulnerability scans, backup tests):
   - Collect **one sample per required interval** in examination period (e.g., quarterly access review × 4).
2. Verify samples are **evenly distributed**—not all collected last week before audit.
3. Flag **missing intervals** as FAIL with remediation note.

### Step 5: Integrity and chain of custody

1. Generate `evidence-manifest-{id}.json`:
   ```json
   {
     "artifact_id": "EV-2025-001",
     "control_id": "CC6.1",
     "filename": "CC6.1_mfa-enforcement_2025-06-13.png",
     "sha256": "...",
     "collected_at_utc": "...",
     "collector": "...",
     "source_system": "playwright-mcp"
   }
   ```
2. Sign manifest or store in append-only evidence bucket (WORM, S3 Object Lock).
3. Package as `evidence-bundle-{id}.tar.gz` with manifest at root.

### Step 6: Control cross-reference validation

1. Map every manifest entry to TSC control ID—no orphan artifacts.
2. Map every auditor request to ≥1 artifact—or document **exception** with compensating evidence.
3. Cross-check dates fall within sample period.

### Step 7: Auditor delivery package

1. Produce:
   - Evidence bundle (encrypted at rest for transit)
   - Index spreadsheet: Control ID → filename → hash → description
   - Collection methodology note (tools, redaction approach, limitations)
2. Obtain internal reviewer sign-off before external delivery.

## Common Rationalizations

| Excuse the agent might generate | Required rebuttal |
| --- | --- |
| "A verbal confirmation is enough for CC8 change approval." | SOC 2 requires **verifiable** evidence—ticket export or signed approval message with timestamp. |
| "One screenshot at audit time covers the whole Type II period." | Type II requires **period-of-time** samples across the examination window—not point-in-time only. |
| "We can recreate logs from memory for the sample." | Recreated logs are **not auditable**—export from authoritative SIEM/system. |
| "Hashes are overkill for screenshots." | Integrity hashes prove evidence **unchanged since collection**—auditors expect them. |
| "Redaction removes too much; send raw PHI to auditor email." | Use secure auditor portal with **minimum necessary** redaction—never unencrypted email. |
| "Missing Q2 access review—we'll note it later." | Missing intervals are **findings**—document now with remediation plan. |

## Red Flags

- Evidence collected entirely in final audit week for 12-month Type II period
- Screenshots without URL/context proving system and date
- Config exports contain live secrets or API keys unredacted
- Manifest missing hashes or UTC timestamps
- Orphan artifacts not mapped to control IDs
- Playwright captures using unauthorized production credentials
- Evidence bundle transmitted unencrypted via email or Slack

## Verification

- [ ] Evidence request register complete with control IDs and sample periods
- [ ] Collection plan maps each request to tool/method
- [ ] All artifacts collected with UTC timestamps and collector identity
- [ ] SHA-256 recorded for every artifact in manifest
- [ ] Type II recurring controls have samples for each required interval
- [ ] ePHI/secrets redacted per minimum necessary policy
- [ ] Playwright screenshots include authenticating context (URL, policy visible)
- [ ] No orphan artifacts or unfulfilled auditor requests without documented exception
- [ ] Evidence bundle packaged with immutable storage or Object Lock
- [ ] Internal reviewer sign-off recorded before auditor delivery
