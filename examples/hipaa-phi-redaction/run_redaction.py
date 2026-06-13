#!/usr/bin/env python3
"""Run Presidio PHI redaction on sample_phi.txt — hipaa-phi-redaction example."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

from redaction import PHIRedactor  # noqa: E402

SAMPLE = Path(__file__).resolve().parent / "sample_phi.txt"


def main() -> int:
    text = SAMPLE.read_text(encoding="utf-8")
    redactor = PHIRedactor()
    result = redactor.redact(text)

    print("=== HIPAA PHI Redaction Example ===")
    print(f"Source: {SAMPLE.name}")
    print(f"Entities detected ({result.entity_count}): {', '.join(result.entities_detected) or 'none'}")
    print()
    print("--- Redacted (safe for LLM) ---")
    print(result.redacted_text)
    print()
    print("--- Deanonymized round-trip ---")
    print(redactor.deanonymize(result.redacted_text))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
