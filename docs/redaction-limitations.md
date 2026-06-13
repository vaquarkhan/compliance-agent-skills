# Redaction limitations

The Presidio-based redaction gate (`redaction.py`) is designed for **US English** operational text. Understand these limits before relying on it for production PHI handling.

## Language and locale

| Supported | Not supported |
|-----------|---------------|
| US English clinical, financial, and identity patterns | Non-English PHI (Spanish, Chinese, Arabic, etc.) |
| US-formatted SSN, phone, dates | International ID formats without custom recognizers |
| Presidio default + custom dashed/spaced SSN | Handwritten or OCR-degraded scans (quality-dependent) |

Presidio's `en_core_web_sm` spaCy model underpins NER. Non-English names, addresses, and clinical terms may **not** be detected.

## Entity coverage

Default profile (`balanced`) detects common HIPAA-relevant entities: names, locations, dates, phone numbers, emails, SSN, credit cards, and related Presidio types.

The `aggressive` profile expands detection at the cost of more false positives. Neither profile guarantees exhaustive coverage of all 18 HIPAA identifiers.

## Determinism

Redaction output depends on:

- Locked library versions (`requirements-lock.txt`)
- spaCy model version (`en_core_web_sm-3.8.0`, URL-pinned)
- Presidio recognizer scores and thresholds

Upgrade any of these only after re-running the test suite and validating sample corpora.

## Recommendations for non-English PHI

1. Add language-specific spaCy models and Presidio recognizers
2. Extend `PHIRedactor` with locale-specific profiles
3. Run human review on a representative corpus before production use
4. Document locale coverage in your own risk assessment

## Related

- [Architecture](architecture.md) — where redaction sits in the pipeline
- [examples/hipaa-phi-redaction](../examples/hipaa-phi-redaction/) — runnable demo
