---
name: hitech-breach-notification
description: Implements HITECH Act breach notification depth beyond baseline HIPAA—42 U.S.C. §17921–17923, ARRA Title XIII Subtitle D, OCR breach reporting portal workflows, 500+ individual media/HHS rules, business associate direct liability, encryption/unsecured PHI safe harbor analysis, and accounting of disclosures for breaches involving agent/LLM/MCP systems. Trigger when conducting HITECH-specific breach determinations, preparing OCR portal submissions, analyzing BA liability for LLM vendors, or auditing breach accounting and penalty exposure. Do not use for general incident containment (use breach-incident-response first), routine HIPAA Security Rule controls (use hipaa-technical-safeguards), or California CPRA consumer rights (use ccpa-cpra-privacy-rights).
---

# HITECH Breach Notification

## Overview

The **Health Information Technology for Economic and Clinical Health (HITECH) Act** (2009), codified at **42 U.S.C. §17921–17923** and implemented through HIPAA Omnibus Rule amendments, strengthened breach notification, extended **direct liability to business associates (BAs)**, and increased civil monetary penalties.

| HITECH element | Requirement | Primary reference |
| --- | --- | --- |
| Breach notification | Individual, HHS, media (if >500 in state) | 45 CFR **§164.400–414**; 42 U.S.C. **§17921** |
| Unsecured PHI | Breach applies to PHI not rendered unusable/unreadable/indecipherable | 45 CFR **§164.402**; HHS encryption guidance |
| BA liability | BAs directly liable for Security, Privacy, Breach Notification | 45 CFR **§160.402(c)** |
| OCR reporting | HHS breach portal; immediate if ≥500 individuals | [HHS Breach Portal](https://ocrportal.hhs.gov/ocr/breach/wizard_breach.jsf) |
| Penalty tiers | Four tiers under HITECH (willful neglect, correction) | 42 U.S.C. **§1320d-5** |
| Accounting of disclosures | Expanded accounting; breach may trigger disclosure log review | 45 CFR **§164.528** |

**Relationship to `breach-incident-response`:** Use that skill for **containment, scope, and cross-framework incident orchestration**. This skill adds **HITECH-specific legal depth**: unsecured PHI analysis, OCR portal mechanics, BA direct notification obligations, media triggers, and penalty-tier documentation.

AI/agent scenarios: LLM vendor without BAA receives ePHI prompts; MCP Postgres leak of session logs; failed redaction gate (`agent.py`) leading to model log retention; BA LLM subprocessors.

## When to Use

Use this skill when:

- **HITECH breach determination** after initial incident classification (`breach-incident-response` Step 4 complete)
- Preparing **HHS OCR breach portal** submission (≥500 immediate; <500 annual aggregation)
- Analyzing whether PHI was **secured** (encryption per NIST SP 800-111 or equivalent) for safe harbor
- **Business associate** (LLM cloud, MCP host) must notify covered entity within **60 days** of discovery (§164.410)
- **Media notification** required (>500 residents of a state or jurisdiction)
- **Penalty exposure** assessment and corrective action planning (willful neglect tiers)
- **Accounting of disclosures** update for breach-related unauthorized access
- Auditing **HITECH compliance** of agent pipelines post-incident

Do **not** use this skill when:

- Active containment still in progress (use `breach-incident-response` Steps 1–2 first)
- No PHI involved—pure PCI or SOC 2 incident without ePHI
- Preventive encryption design (use `hipaa-technical-safeguards`, `pci-dss-encryption-key-management`)
- State-only breach without HIPAA PHI (use `us-state-privacy-laws`)

## Core Process

Execute after containment. Steps **in order**.

### Step 1: Unsecured PHI determination

1. List PHI elements involved: identifiers, clinical data, dates, device IDs in agent logs.
2. Apply **secured PHI** test per HHS guidance:
   - Valid encryption per **NIST SP 800-111** (or documented equivalent)?
   - Destruction of paper/electronic media per policy?
3. If PHI was **encrypted at rest/in transit per guidance** and key not compromised → may not be "unsecured" → breach may not apply.
4. Document analysis in `templates/hitech-breach-workbook.yaml` — do not assume encryption safe harbor without key compromise review.

### Step 2: Four-factor risk assessment (§164.402(2))

If unsecured PHI involved, breach is **presumed** unless low probability documented:

| Factor | Assessment questions |
| --- | --- |
| Nature and extent of PHI | Diagnosis, financial, SSN, full clinical notes in LLM prompt? |
| Unauthorized person | External attacker, rogue employee, non-BAA LLM vendor employee? |
| Was PHI acquired or viewed? | Log evidence, model training retention, MCP export? |
| Extent of mitigation | Revocation, deletion certificates, re-encryption? |

Privacy officer signs determination: **breach** vs **security incident (no breach)**.

### Step 3: Individual notification (§164.404)

1. **Without unreasonable delay**, no later than **60 calendar days** from discovery.
2. Content per §164.404(c):
   - Brief description of incident and dates
   - Types of PHI involved
   - Steps individuals should take
   - CE investigation and mitigation steps
   - Contact procedures (toll-free, email, website)
3. **Substitute notice** if insufficient contact data (>10 individuals): website 90 days, media, or email if consented.
4. For agent breaches: explain if LLM/MCP systems were involved **without naming unnecessary clinical detail**.

### Step 4: HHS OCR notification (§164.408)

| Affected count | Action | Timeline |
| --- | --- | --- |
| **≥500** in a state/jurisdiction | Submit via OCR Breach Portal | **Without unreasonable delay**, max 60 days; OCR expects prompt submission |
| **<500** | Log for **annual** submission | Within 60 days of calendar year end |

1. Gather: CE/BA identity, incident dates, individuals affected, types of PHI, safeguards in place, brief description, mitigation.
2. Retain portal confirmation and submission ID in evidence manifest.
3. Cross-reference `breach-incident-response` timeline for discovery date (starts clock).

### Step 5: Media notification (§164.406)

If **>500 residents of a state or jurisdiction** affected:

1. Notify **prominent media outlets** in affected areas without unreasonable delay (max 60 days).
2. Coordinate with legal/comms—message consistent with individual notice.
3. Document media list and publication dates.

### Step 6: Business associate obligations (§164.410)

If CE uses BA (LLM vendor, MCP host, cloud agent platform):

1. BA must notify CE **without unreasonable delay**, no later than **60 days** from discovery.
2. BA provides: identities of affected individuals if known, other information CE needs for notification.
3. If **BA is agent skill operator's subprocessors chain**, map contractual notice SLAs—contract must meet or beat 60 days.
4. CE remains responsible for individual/HHS/media notification unless delegated in BAA (uncommon).

### Step 7: Penalty tier and corrective action (42 U.S.C. §1320d-5)

Document tier for management/legal (not legal advice):

| Tier | Conduct | Planning use |
| --- | --- | --- |
| 1 | Unknowing | Training gaps, undetected misconfig |
| 2 | Reasonable cause, not willful neglect | Process failure, delayed BA notification |
| 3 | Willful neglect, corrected | Known redaction bypass, uncorrected for period |
| 4 | Willful neglect, not corrected | Ignored OCR corrective action plan |

1. Draft corrective action plan: fix `redaction.py` gate, MCP allowlists, BAA gaps.
2. Link to `hipaa-baa-vendor-assessment` for vendor remediation.

### Step 8: Accounting of disclosures (§164.528)

1. Review whether breach constitutes **disclosure** requiring accounting update.
2. Update disclosure logs for affected individuals requesting accounting (6-year lookback).
3. Agent/MCP logs may be source of disclosure evidence—use hashed, access-controlled exports.

### Step 9: Evidence and retention

1. Package: risk assessment, notification letters, portal submission, media proof, BA notices.
2. SHA-256 manifest per `templates/audit-evidence-manifest.yaml`.
3. Retain **6 years** minimum (HIPAA documentation; state laws may differ).

## Common Rationalizations

| Excuse | Rebuttal |
| --- | --- |
| "Encrypted in transit to LLM—no breach." | Key compromise or vendor log retention of decrypted prompts voids safe harbor—document analysis. |
| "BA will handle all notifications." | CE retains **primary** notification duty unless explicit BAA delegation; verify contract language. |
| "<500 individuals—skip OCR until year-end." | **Individual notice still required within 60 days**; annual OCR log is separate obligation. |
| "We deleted LLM logs—no evidence of view." | Absence of logs does not negate breach presumption if unauthorized access was confirmed. |
| "HITECH is same as HIPAA breach skill." | HITECH adds **BA direct liability**, penalty tiers, and OCR portal mechanics requiring dedicated workbook. |

## Red Flags

- Discovery date undocumented (clock ambiguity)
- LLM vendor confirmed prompt retention without BAA
- ≥500 affected but no media notification plan
- BA notification received on day 59 with incomplete individual list
- Encryption claimed without NIST-aligned key management review
- OCR portal submission missing mitigation narrative

## Verification

- [ ] Unsecured PHI analysis completed with encryption/key compromise review
- [ ] Four-factor risk assessment signed by privacy officer
- [ ] Individual notice drafted and 60-day deadline tracked
- [ ] HHS OCR portal path determined (immediate vs annual log)
- [ ] Media notification plan if >500 in state/jurisdiction
- [ ] BA notification chain documented with contractual SLAs
- [ ] Penalty tier and corrective action plan drafted for management
- [ ] Accounting of disclosures reviewed and updated if applicable
- [ ] Evidence manifest with SHA-256 hashes archived
