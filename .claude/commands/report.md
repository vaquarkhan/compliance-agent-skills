# /report — Findings Report

Produce executive and technical compliance reports.

## Prerequisites

- Scope artifact (`/scope`)
- Audit findings (`/audit`)
- Evidence manifest (`/evidence`)
- Remediation plan (`/remediate`) if gaps exist

## Report structure

### 1. Executive summary (≤1 page)

- Engagement ID, period, frameworks
- Overall posture: **not assessed / gaps identified / controls operating effectively** (never "certified compliant")
- Top 3–5 risks by severity
- Remediation timeline summary

### 2. Scope recap

- In-scope / out-of-scope systems
- Data classifications
- Limitations and dependencies

### 3. Findings detail

| ID | Severity | Control | Observation | Recommendation | Status |
| --- | --- | --- | --- | --- | --- |

### 4. Evidence index

Reference `audit-evidence-manifest.yaml` artifact IDs — do not embed raw evidence in report body.

### 5. Remediation tracker

Summary table from `/remediate` output.

### 6. Appendices

- Control matrix excerpt
- Methodology (skills used, MCP tools, sampling approach)

## Rules

- No raw PHI/PAN in report text
- Cite control IDs (HIPAA §, PCI Req, TSC CC)
- Include disclaimer: not legal advice; not attestation

## Distribution

Classify as **Confidential**. Use secure channel for external auditors.
