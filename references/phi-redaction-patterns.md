# PHI Redaction Patterns

Patterns for Microsoft Presidio integration via `redaction.py` and the compliance agent PHI gate.

## Architecture

```
User input → Presidio Analyzer → Token replacement → LLM reasoning → Optional deanonymize
```

The agent **never** sees raw ePHI when the gate is active. Tokens like `<PERSON_1>` are intentional.

## Default entity types

From `redaction.py` `DEFAULT_ENTITY_TYPES`:

`PERSON`, `PHONE_NUMBER`, `EMAIL_ADDRESS`, `US_SSN`, `US_DRIVER_LICENSE`, `US_PASSPORT`, `US_BANK_NUMBER`, `CREDIT_CARD`, `DATE_TIME`, `MEDICAL_LICENSE`, `IP_ADDRESS`, `LOCATION`, `NRP`, `URL`

## Tuning guidelines

| Scenario | Action |
| --- | --- |
| High false positives on dates | Raise `score_threshold` to 0.45–0.55 |
| Missing MRNs | Add custom recognizer (not in default list) |
| Clinical free text | Keep `PERSON`, `DATE_TIME`, `LOCATION` enabled |
| PCI checkout audits | Enable `CREDIT_CARD`; never log matches |

## Reversible tokenization

- Tokens stored in session-scoped `_token_to_value` map
- `deanonymize_response` tool restores values for authorized delivery only
- Call `reset_session()` between unrelated engagements

## Testing pattern

```python
from redaction import PHIRedactor

redactor = PHIRedactor()
result = redactor.redact("Patient John Doe, MRN 12345, DOB 01/15/1980")
assert "<PERSON_" in result.redacted_text
assert "John Doe" not in result.redacted_text
```

See `examples/hipaa-phi-redaction/run_redaction.py`.

## Anti-patterns

- Disabling redaction for "better model answers"
- Logging `original_text` from `RedactionResult` to SIEM
- Sharing deanonymized output in Slack without channel classification

## Hook integration

`hooks/phi-redaction-guard.sh` sets `COMPLIANCE_PHI_REDACTION=required` for IDE sessions.

## Skill mapping

Primary: `hipaa-phi-redaction-pipeline`

Reference: `references/hipaa-security-rule-checklist.md` (transmission security)
