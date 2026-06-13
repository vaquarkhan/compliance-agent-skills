#!/usr/bin/env python3
"""Example: extend PHIRedactor with a custom MRN pattern recognizer.

Copy patterns into redaction.py ``_register_custom_recognizers`` or subclass
PHIRedactor for organization-specific identifiers.
"""

from __future__ import annotations

from presidio_analyzer import Pattern, PatternRecognizer

from redaction import PHIRedactor


def mrn_recognizer() -> PatternRecognizer:
    return PatternRecognizer(
        supported_entity="MEDICAL_RECORD_NUMBER",
        patterns=[
            Pattern(name="mrn_label", regex=r"\bMRN[:\s#-]*(\d{6,10})\b", score=0.85),
            Pattern(name="mrn_wristband", regex=r"\b(?:wristband|chart)\s+#(\d{6,10})\b", score=0.8),
        ],
    )


class ExtendedPHIRedactor(PHIRedactor):
    def _register_custom_recognizers(self) -> None:
        super()._register_custom_recognizers()
        self._analyzer.registry.add_recognizer(mrn_recognizer())
        if "MEDICAL_RECORD_NUMBER" not in self.entity_types:
            self.entity_types = [*self.entity_types, "MEDICAL_RECORD_NUMBER"]


if __name__ == "__main__":
    sample = "Chief complaint: cough. MRN: 8844221 for Maria Garcia."
    engine = ExtendedPHIRedactor()
    result = engine.redact(sample)
    print(result.redacted_text)
    print("entities:", result.entities_detected)
