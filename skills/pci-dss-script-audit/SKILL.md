---
name: pci-dss-script-audit
description: Automates PCI-DSS v4.0 Requirements 6.4.3 (payment-page script authorization, inventory, integrity hashes, and business justification) and 11.6.1 (weekly change/tamper detection for HTTP security headers and DOM scripts). Trigger when auditing ecommerce checkout or payment pages, validating third-party JavaScript governance, detecting unauthorized script or CSP changes, or producing PCI script inventory evidence. Do not use for backend server patching, network firewall rules, cardholder data storage encryption, or non-payment marketing pages.
---

# PCI-DSS Script Audit

## Overview

This skill drives a deterministic audit workflow for **PCI-DSS v4.0 Requirement 6.4.3** (script management on payment pages) and **Requirement 11.6.1** (change and tamper detection). The agent must treat the skill steps as mandatory sequence—not suggestions—and produce verifiable artifacts (DOM snapshots, script inventory, SHA-256 hashes, header baselines, and diff reports).

Payment-page script attacks (Magecart, formjacking, skimming) bypass traditional WAF controls because malicious code executes in the browser DOM. This skill closes that gap by combining headless browser extraction via the **official Playwright MCP server** with cryptographic integrity verification and continuous baseline comparison.

## When to Use

Use this skill when:

- Auditing a **checkout, cart, or payment page** for PCI-DSS v4.0 compliance
- Building or refreshing a **script inventory** with authorization status and business justification
- Verifying **SHA-256 integrity hashes** of inline and external JavaScript against an authorized baseline
- Running **Requirement 11.6.1** monitoring (headers + DOM) on a schedule (at least every 7 days)
- Investigating alerts for **unauthorized script additions, modifications, or deletions**
- Reviewing **Content-Security-Policy (CSP)** and other security headers on payment pages

Do **not** use this skill when:

- The target is a non-payment page (blog, marketing landing page, internal admin console)
- The task is purely backend infrastructure (database encryption, OS hardening, vault key rotation)
- You lack authorization to scan the target URL or connect MCP tools to production systems
- You need HIPAA PHI redaction only (use a HIPAA-focused skill instead)

## Core Process

Execute the following steps **in order**. Do not skip or reorder steps.

### Phase A — Requirement 6.4.3: Script Authorization, Inventory, and Integrity

#### Step 1: Initialize audit context

1. Record the audit metadata:
   - Target payment page URL(s)
   - Audit timestamp (UTC)
   - Auditor identity / agent run ID
   - PCI scope identifier (e.g., CDE checkout flow name)
2. Confirm you have MCP access to the **Playwright MCP server** (official `@playwright/mcp` or equivalent documented Playwright MCP implementation).
3. If Playwright MCP is unavailable, **stop** and report a blocking error—do not substitute manual curl or static HTML fetches for dynamic checkout pages.

#### Step 2: Headless DOM extraction (Playwright MCP)

1. Invoke the Playwright MCP server to launch a headless browser.
2. Navigate to each target payment page URL.
3. Wait until the page reaches a **network-idle** or documented stable state (all dynamic scripts loaded).
4. Capture:
   - Full rendered HTML / DOM snapshot
   - Final response HTTP status
   - Response and request headers for the document
5. Save the DOM snapshot as evidence artifact `dom-snapshot-{timestamp}.html`.

#### Step 3: Script enumeration

1. Parse the captured DOM and extract **every** script source:
   - External scripts: all `<script src="...">` URLs (resolve relative URLs to absolute)
   - Inline scripts: all `<script>` blocks without `src` (include type/module variants)
   - Dynamically injected scripts visible in the final DOM (via attributes, `data-*`, or inline handlers if present)
2. Produce a machine-readable inventory table with columns:
   - `script_id` (stable hash of location + src or inline prefix)
   - `type` (`external` | `inline`)
   - `location` (URL or `inline:{line-range}`)
   - `src_url` (if external)
   - `first_seen_dom_path` (optional CSS path or line reference)

#### Step 4: Integrity verification (SHA-256)

For each enumerated script:

1. Obtain raw script content:
   - **External**: download via HTTP(S) using the resolved absolute URL
   - **Inline**: use the exact inline body from the DOM snapshot
2. Compute `SHA-256` hash of the raw bytes (document as `sha256:{hex}`).
3. Compare against the organization's **authorized baseline** (Postgres MCP, compliance DB, or provided hash manifest):
   - If `H(current) == H(authorized)` → mark `integrity_status: PASS`
   - If hash missing from baseline → mark `integrity_status: UNKNOWN — requires authorization`
   - If hash mismatch → mark `integrity_status: FAIL — tamper suspected`
4. Record comparison timestamp and baseline version ID in the audit log.

#### Step 5: Authorization and business justification

For each script where `integrity_status` is not `PASS`:

1. Check authorization registry (baseline metadata: owner, approval date, ticket ID).
2. If unauthorized, use semantic analysis of the script source (API calls, DOM hooks, network endpoints, library fingerprints) to draft a **written business justification** candidate, for example:
   - "Minified bundle matches Zendesk chat widget v4.x; loads `static.zdassets.com`; no payment field selectors observed."
3. Flag every unauthorized or unknown script for **human security review** with severity:
   - `CRITICAL` — touches payment fields, PAN patterns, or exfiltration endpoints
   - `HIGH` — unknown third-party with network beacon behavior
   - `MEDIUM` — known vendor, missing paperwork
   - `LOW` — static analytics with no payment DOM access
4. Do **not** mark the audit complete while any `CRITICAL` or `HIGH` items remain unreviewed.

### Phase B — Requirement 11.6.1: Change and Tamper Detection

#### Step 6: Establish or load baseline

1. Load the most recent authorized baseline containing:
   - Normalized DOM script inventory (IDs, hashes, URLs)
   - Security header set: at minimum `Content-Security-Policy`, `Strict-Transport-Security`, `X-Frame-Options`, `X-Content-Type-Options`, `Referrer-Policy`
2. If no baseline exists, promote the current Phase A output as `baseline-v1` after human approval.

#### Step 7: Scheduled comparison (≥ every 7 days)

1. Re-run Steps 2–4 to obtain `current_state`.
2. Diff `current_state` vs `baseline`:
   - **Scripts added** (new `script_id` or new `src_url`)
   - **Scripts removed**
   - **Scripts modified** (`sha256` changed)
   - **Header changes** (especially CSP `script-src`, `frame-src`, `connect-src` directives)
3. Classify each diff as `authorized change` or `indicator of compromise (IOC)`.
4. If any IOC is detected:
   - Generate a forensic diff report (unified diff for inline scripts; hash before/after for external)
   - Alert SOC via configured communication MCP (e.g., Slack MCP) with page URL, diff summary, and timestamps
   - Do **not** auto-approve IOC diffs

#### Step 8: Evidence packaging

1. Emit a compliance evidence bundle:
   - DOM snapshot(s)
   - Script inventory CSV/JSON
   - Hash verification log
   - Header baseline comparison
   - Unauthorized script queue with justification drafts
   - 11.6.1 diff report (or "no changes detected")
2. Store artifacts with immutable audit IDs suitable for QSA review.

## Common Rationalizations

| Excuse the agent might generate | Required rebuttal |
| --- | --- |
| "A static HTML fetch is enough; Playwright is overkill." | PCI 6.4.3 requires the **fully rendered** payment page DOM. Checkout flows load scripts dynamically; static fetches miss authorized and unauthorized scripts alike. |
| "I'll verify hashes later after the report is drafted." | Integrity verification is a **blocking gate**. Reports without hashes are incomplete evidence and violate the skill sequence. |
| "Unknown scripts are probably fine if the page loads." | Unknown scripts on payment pages are **presumed unauthorized** until matched to baseline metadata and human review. |
| "CSP headers are optional for this merchant." | CSP and related headers are explicit **11.6.1** monitoring targets. Skipping header diff leaves tamper detection incomplete. |
| "I'll batch SOC alerts into a weekly summary." | IOC diffs require **immediate** notification with forensic context; batching delays containment. |
| "Inline script hashes are too hard; I'll skip inline blocks." | Inline scripts are in scope for **both 6.4.3 and 11.6.1**. Skipping them is a direct compliance gap. |
| "Business justification can be a one-line placeholder." | PCI requires **written business justification** tied to observable behavior—not generic placeholders. |

## Red Flags

Stop and escalate immediately if any of the following occur:

- Script accessing `input` fields named like card/PAN/CVV without baseline authorization
- New third-party domain in CSP `script-src` not present in approved vendor list
- Hash mismatch on previously authorized script without change ticket reference
- Playwright MCP unreachable but audit marked complete
- Agent skips inline scripts or uses static HTML fetch instead of Playwright MCP
- IOC diff detected but no SOC alert generated

## Verification

Do not mark this skill complete until **all** exit criteria are explicitly confirmed with evidence links or artifact IDs:

- [ ] Playwright MCP was used to capture a post-render DOM snapshot for every in-scope payment URL
- [ ] Script inventory lists **100%** of external and inline scripts found in the DOM
- [ ] SHA-256 hash computed and recorded for **every** script entry
- [ ] Each script mapped to `PASS`, `UNKNOWN`, or `FAIL` against the authorized baseline
- [ ] Unauthorized/unknown scripts have drafted business justifications and human review severity
- [ ] Security headers captured and compared to baseline (CSP diff explicitly checked)
- [ ] 11.6.1 diff executed (or scheduled run documented with date of last successful comparison ≤ 7 days)
- [ ] IOC findings (if any) triggered SOC alert with diff artifacts—none silently dropped
- [ ] Evidence bundle stored with immutable audit ID and UTC timestamps
- [ ] No step skipped due to tool unavailability without a documented blocking finding
