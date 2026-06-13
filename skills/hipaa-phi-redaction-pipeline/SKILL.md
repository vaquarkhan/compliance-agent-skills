---
name: hipaa-phi-redaction-pipeline
description: Configures and validates the Presidio-based PHI redaction pipeline—DLP entity detection, reversible tokenization before LLM ingestion, and authorized deanonymization—integrated with redaction.py and the compliance agent. Trigger when ePHI may appear in prompts, implementing minimum-necessary LLM access, tuning entity types, or auditing redaction effectiveness. Do not use for HIPAA access control design (use hipaa-technical-safeguards) or legal BAA review (use hipaa-baa-vendor-assessment).
---

# HIPAA PHI Redaction Pipeline

## Overview

This skill governs the **PHI redaction gate** that prevents raw ePHI from reaching the LLM reasoning engine. The repository implements this in `redaction.py` using **Microsoft Presidio** (`presidio_analyzer`, `presidio_anonymizer`) with **reversible masked tokens** (e.g., `<PERSON_1>`, `<US_SSN_1>`).

**Pipeline flow:**

```
User input → Presidio analyze → Tokenize → Redacted text → LLM/agent → Output → Deanonymize (authorized only)
```

The compliance agent (`agent.py`) runs redaction **upstream** of `compliance_agent.run()`. The agent receives only redacted text; restoration uses `deanonymize_response` tool or `PHIRedactor.deanonymize()` for authorized downstream delivery.

**Default entity profile** (`entity_profile="balanced"` in `PHIRedactor`): PERSON, PHONE_NUMBER, EMAIL_ADDRESS, US_SSN, US_DRIVER_LICENSE, US_PASSPORT, US_BANK_NUMBER, CREDIT_CARD, MEDICAL_LICENSE, IP_ADDRESS.

**Aggressive profile** (`entity_profile="aggressive"`): balanced types plus DATE_TIME, LOCATION, NRP, URL — higher recall but over-redacts audit URLs and dates. Use for clinical free-text; use balanced for PCI/SOC 2 technical audits.

Legacy alias `DEFAULT_ENTITY_TYPES` maps to the aggressive list.

**Built-in custom recognizers** in `redaction.py` add dashed and spaced US SSN patterns. For MRN/ICD/CPT, see `examples/custom-ssn-recognizer.py`.

## When to Use

Use this skill when:

- **Tuning** Presidio entity types or score thresholds for your data
- **Validating** redaction effectiveness before production agent deployment
- **Auditing** whether prompts/responses leak ePHI past the gate
- **Integrating** Presidio MCP or custom DLP with the agent pipeline
- **Configuring** session-scoped token maps and deanonymization authorization
- **Testing** edge cases: clinical notes, structured HL7/FHIR snippets, mixed PHI/PCI

Do **not** use this skill when:

- Designing IAM or encryption controls (use `hipaa-technical-safeguards`)
- Replacing a full data-loss-prevention program for non-LLM channels
- PCI cardholder data tokenization in payment systems (use PCI skills)

## Core Process

Execute steps **in order**.

### Step 1: Baseline configuration audit

1. Read current `PHIRedactor` configuration:
   - `entity_types` list vs organizational PHI taxonomy
   - `spacy_model` (default `en_core_web_sm`)—verify model installed
   - `score_threshold` (default `0.35`)—document rationale
2. Verify `agent.py` calls `redactor.redact(user_prompt)` **before** `compliance_agent.run()`.
3. Confirm `reset_session()` runs per engagement to prevent cross-session token leakage.
4. Record config snapshot: `redaction-config-{id}.json`.

### Step 2: Entity coverage matrix

1. For each ePHI category in organizational policy, map to Presidio entity type or custom recognizer:

| ePHI category | Presidio entity | Custom recognizer needed? |
| --- | --- | --- |
| Patient names | PERSON | Maybe (provider names vs patients) |
| MRNs / account numbers | Custom | Often yes—add pattern recognizer |
| Dates of service | DATE_TIME | Tune to avoid over-redaction |
| Diagnosis/procedure codes | Custom | ICD/CPT patterns |
| Email/phone | EMAIL_ADDRESS, PHONE_NUMBER | Usually sufficient |
| SSN | US_SSN | Required for USA deployments |

2. Identify gaps; document plan for custom `Recognizer` classes in Presidio analyzer.
3. Do **not** remove entity types without risk analysis—under-redaction exposes ePHI to LLM.

### Step 3: Redaction effectiveness testing

1. Prepare **synthetic test corpus** (no real patient data in logs):
   - Mixed PHI types, adversarial formats (spaced SSN, unicode homoglyphs)
   - Clinical note templates, referral letters, billing snippets
2. Run each sample through `PHIRedactor.redact()`:
   ```python
   from redaction import PHIRedactor
   r = PHIRedactor()
   result = r.redact(sample_text)
   assert result.entity_count >= expected_minimum
   ```
3. Verify **no raw PHI substrings** remain in `result.redacted_text` (automated scan).
4. Record detection rate, false positive rate, false negative rate per entity type.
5. False negatives are **CRITICAL** findings—block production until remediated.

### Step 4: Tokenization and session isolation

1. Verify tokens are **stable within session** (`<PERSON_1>` maps consistently).
2. Verify `reset_session()` clears `_token_to_value` between engagements.
3. Test `redaction_status` tool reports accurate `active_tokens` count.
4. Confirm tokens are **not reversible** by the LLM (model instructions prohibit reconstruction).

### Step 5: Deanonymization authorization

1. Document who may call `deanonymize_response`:
   - Role-based access; MFA for human operators
   - Automated downstream systems via service account with audit logging
2. Test deanonymization round-trip:
   - Redact → process → deanonymize restores exact original values
   - Partial token replacement does not corrupt adjacent text
3. Verify deanonymized output is **never** written to:
   - Unencrypted logs, Slack, or non-BAA LLM follow-up prompts

### Step 6: Presidio MCP integration (optional)

If using a Presidio MCP server for live DLP:

1. Configure MCP tool to mirror `redaction.py` entity types and thresholds.
2. Verify MCP and local redactor produce **consistent** token formats.
3. Log MCP invocations without storing raw input text in MCP server logs.
4. Fail closed if MCP unavailable—do not bypass redaction gate.

### Step 7: LLM boundary verification

1. Capture a test run's model input payload (redacted only).
2. Assert zero matches for SSN, MRN, and name patterns in payload.
3. Verify system prompt instructs model not to reconstruct tokens.
4. Store evidence: `redaction-boundary-test-{id}.json` with pass/fail per check.

### Step 8: Operational monitoring

1. Define metrics: entities redacted per session, false negative reports, deanonymization events.
2. Alert on `entity_count == 0` for prompts expected to contain PHI (possible detector failure).
3. Schedule quarterly retesting with updated Presidio/spaCy versions.

## Common Rationalizations

| Excuse the agent might generate | Required rebuttal |
| --- | --- |
| "Presidio catches enough; we don't need custom MRNs." | MRNs are common ePHI and often **missed** by default recognizers—custom patterns are typically required. |
| "Low score threshold causes too many false positives; we'll raise it to 0.9." | Raising threshold increases **false negatives** (ePHI leakage). Tune with measured FN/FP tradeoff, not convenience. |
| "Deanonymize in the model prompt for better answers." | Reconstruction in LLM context violates **minimum necessary** and defeats the redaction gate. |
| "Session tokens can persist for user convenience." | Cross-session token maps risk **wrong patient attribution**—reset per engagement. |
| "Redaction is optional for internal admin users." | Role does not remove HIPAA obligation—**all** paths to LLM require redaction unless BAA-covered zero-retention architecture is documented. |
| "We'll log redacted text only, so originals are safe." | Logs with tokens plus deanonymization maps can **reconstruct PHI**—protect token maps as ePHI. |

## Red Flags

- `compliance_agent.run()` invoked with unredacted user text
- False negative on SSN, MRN, or patient name in LLM input capture
- Deanonymization available without authentication or audit log
- Token-to-value map persisted unencrypted across sessions
- Presidio MCP bypassed when server is down
- Model instructed to "guess" or "fill in" redacted token values
- Redaction test corpus uses real production PHI in CI logs

## Verification

- [ ] `redaction.py` configuration documented and matches organizational PHI taxonomy
- [ ] Redaction runs upstream of every LLM/agent invocation
- [ ] Entity coverage matrix complete with custom recognizer plan for gaps
- [ ] Effectiveness test corpus executed with FN/FP rates recorded
- [ ] Zero false negatives on CRITICAL entity types (SSN, MRN if in scope)
- [ ] Session isolation verified via `reset_session()` tests
- [ ] Deanonymization authorization and audit logging documented and tested
- [ ] LLM boundary test confirms no raw PHI in model input payload
- [ ] Operational metrics and quarterly retest schedule defined
- [ ] Evidence artifacts stored with SHA-256 hashes and audit ID
