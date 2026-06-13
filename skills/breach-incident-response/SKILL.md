---
name: breach-incident-response
description: Executes USA breach and security incident response—HIPAA Breach Notification Rule (45 CFR §164.400–414), HITECH 60-day notification, state breach laws, and SOC 2 CC7.4/CC7.5 incident management—for agent, MCP, and LLM-related events. Trigger when investigating suspected PHI/PII exposure, unauthorized MCP access, LLM data leakage, or preparing breach notifications. Do not use for preventive logging design (use audit-logging-integrity) or routine vulnerability scanning.
---

# Breach Incident Response

## Overview

This skill orchestrates **security incident and breach response** for USA regulatory obligations:

- **HIPAA Breach Notification Rule**: 45 CFR **§164.400–§164.414** (individual, HHS, media notification timelines)
- **HITECH**: 60-day notification to individuals; HHS OCR reporting
- **State breach laws**: variable timelines (many 30–90 days)—California, New York, etc.
- **SOC 2 CC7.4/CC7.5**: Incident identification, response, recovery, communication

AI-specific incidents include: unredacted ePHI sent to non-BAA LLM, MCP tool exfiltration, deanonymization abuse, compromised agent API keys, and prompt injection leading to data disclosure.

## When to Use

Use this skill when:

- **Suspected or confirmed** unauthorized access/disclosure of ePHI, CHD, or confidential data
- **LLM data leakage** (raw PHI in model logs, training pipeline, vendor breach notification)
- **MCP compromise** (rogue tool registration, stolen OAuth tokens)
- **Agent credential theft** or skill tampering detected
- Preparing **breach notification** letters, HHS OCR reporting, state AG notifications
- **Tabletop exercises** for agent/MCP incident scenarios
- Post-incident **root cause analysis** for SOC 2 and HIPAA documentation

Do **not** use this skill when:

- Designing preventive audit logs (use `audit-logging-integrity`)
- General vendor risk questionnaires (use `vendor-third-party-risk`)
- Non-security operational outages without data impact (use availability runbooks)

## Core Process

Execute steps **in order**. **Contain first**—do not delay containment for documentation.

### Step 1: Detection and classification

1. Triage alert source: SIEM, CCM, user report, vendor notification, red team.
2. Classify incident type:
   - **Security incident** (attempted access, no confirmed disclosure)
   - **Breach** (acquisition/access/disclosure of unsecured PHI per §164.402 definitions)
   - **PCI incident** (CHD/SAD suspected compromise)
3. Assign severity and incident commander.
4. Start **immutable incident timeline** (UTC timestamps, actor actions).

### Step 2: Immediate containment

1. **Isolate** affected systems without destroying forensic evidence:
   - Revoke compromised MCP OAuth tokens and API keys
   - Disable affected agent deployments; block LLM API keys
   - Snapshot logs and MCP server state before changes
2. Preserve evidence with SHA-256 hashes; chain of custody log.
3. Do **not** deanonymize logs for investigation unless authorized forensic path.

### Step 3: Scope and impact assessment

1. Determine **what data** was involved:
   - ePHI elements, volume, individuals affected
   - CHD/SAD if payment systems involved
2. Determine **unsecured PHI** analysis per §164.402:
   - Was data encrypted per HIPAA guidance such that disclosure is impracticable?
   - Risk assessment per **four-factor test** (§164.402(2)): nature of PHI, unauthorized person, acquisition/view, mitigation
3. Use audit logs (`audit-logging-integrity` artifacts) for timeline reconstruction.
4. Document **minimum necessary** findings—avoid spreading PHI in incident tickets.

### Step 4: HIPAA breach determination

1. If unsecured PHI involved, apply **breach presumption** (§164.402)—breach unless low probability of compromise documented.
2. Privacy officer/legal confirms breach vs security incident.
3. If breach: start **notification clock** (60 days to individuals per §164.404; HHS per §164.408).

### Step 5: Notification workflows

#### HIPAA (if breach confirmed)

| Audience | Requirement | Timeline |
| --- | --- | --- |
| Individuals | Written notice (mail or email if opted) | Without unreasonable delay, max **60 days** |
| HHS OCR | Portal submission | ≤60 days; <500 individuals = annual log |
| Media | If >500 residents of a state | Without unreasonable delay, max 60 days |

1. Draft notification content per §164.404(c): description, types of PHI, steps for individuals, CE contact, mitigation steps.
2. **Do not** include unnecessary PHI in notification letters.

#### State laws

1. Identify affected individuals' states; check **state breach statutes** (timeline may be shorter than HIPAA).
2. Notify state AG where required (e.g., CA, NY thresholds).

#### SOC 2 CC7.5

1. Document customer notification if incident affects service commitments or confidentiality.
2. Align with contractual incident notification SLAs.

### Step 6: PCI incident response (if CHD involved)

1. Engage PCI forensics (PFI) if required by acquirer/brands.
2. Do not store full PAN in incident docs—use tokenized references.
3. Cross-notify payment brands per merchant agreement.

### Step 7: Eradication and recovery

1. Remove attacker access: rotate all secrets, patch vulnerabilities, remove rogue MCP tools.
2. Restore from known-good baselines; re-run `compliance-as-code-governance` scans.
3. Verify redaction gate and MCP allowlists before re-enabling agent production traffic.

### Step 8: Post-incident review

1. Root cause analysis: technical, process, human factors.
2. Update skills, runbooks, CCM rules to prevent recurrence.
3. Document lessons learned for board/management (CC1.2, CC2.2).
4. Retain incident records per HIPAA documentation requirements (6 years common).

### Step 9: Regulatory reporting completion

1. Track notification deliveries and HHS submission confirmation.
2. Archive all artifacts in encrypted evidence store with access controls.

## Common Rationalizations

| Excuse the agent might generate | Required rebuttal |
| --- | --- |
| "It's probably not a breach—skip notification planning." | HIPAA applies **breach presumption** until documented four-factor risk assessment proves low probability. |
| "We contained it—notification can wait." | Notification clocks start upon **discovery**—delay beyond regulatory timelines is a secondary violation. |
| "Put full incident details in Slack for speed." | Incident channels must use **approved secure tools**—no cleartext PHI in Slack unless BAA-covered and scoped. |
| "LLM vendor deleted the data—no breach." | Vendor assurance does not replace **your breach determination** and notification obligations. |
| "Only 10 patients—no HHS report needed." | HHS reporting still required (**annual log** if <500)—individual notification still required. |
| "Forensics can wait until after we're back online." | Snapshot logs and MCP state **before** recovery actions destroy evidence. |

## Red Flags

- Raw ePHI confirmed in non-BAA LLM vendor logs
- Deanonymization tool used anomalously without ticket correlation
- Incident commander lacks privacy/legal engagement on PHI breach
- Notification letters drafted past 60-day HIPAA deadline
- Full patient list posted in unencrypted incident spreadsheet
- MCP rogue tool remained registered during containment phase
- No HHS OCR submission tracking for reportable breach

## Verification

- [ ] Incident classified (security incident vs breach) with privacy/legal sign-off
- [ ] Containment executed with forensic snapshots hashed before destructive changes
- [ ] Scope assessment completed with four-factor risk analysis documented
- [ ] HIPAA notification timeline tracked with individual/HHS/media requirements identified
- [ ] Applicable state breach notifications identified and scheduled
- [ ] SOC 2/customer contractual notifications sent per SLA
- [ ] PCI PFI engaged if CHD compromise suspected
- [ ] Eradication verified; agent/MCP production restored only after control revalidation
- [ ] Post-incident RCA completed with CCM/policy updates implemented
- [ ] All incident artifacts stored encrypted with access audit trail
