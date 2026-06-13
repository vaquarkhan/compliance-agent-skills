# HIPAA PHI Redaction Example

Demonstrates the **Presidio-based PHI redaction pipeline** (`redaction.py`) on synthetic clinical text.

## Prerequisites

```bash
pip install -r ../../requirements.txt
```

## Files

| File | Purpose |
| --- | --- |
| `sample_phi.txt` | Synthetic ePHI (not real patient data) |
| `run_redaction.py` | Runs PHIRedactor and prints redacted output |

## Run

```bash
cd examples/hipaa-phi-redaction
python run_redaction.py
```

## Expected output

- Entity types detected (PERSON, DATE_TIME, PHONE_NUMBER, etc.)
- Redacted text with tokens like `<PERSON_1>`
- Deanonymized round-trip demonstration

## Skill

Load `hipaa-phi-redaction-pipeline` for production tuning.

## Safety

`sample_phi.txt` contains **fabricated** data for testing only. Do not replace with real clinical records in this repository.

## Integration

The same redaction engine runs upstream of `agent.py` before LLM ingestion.
