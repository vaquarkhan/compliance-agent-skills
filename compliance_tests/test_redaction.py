"""Presidio integration tests using the synthetic PHI corpus."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from redaction import PHIRedactor
from compliance_tests.support import presidio

CORPUS_PATH = Path(__file__).resolve().parent / "fixtures" / "synthetic_phi_corpus.yaml"
PHI_CORPUS: list[dict] = yaml.safe_load(CORPUS_PATH.read_text(encoding="utf-8"))["cases"]


@presidio
@pytest.mark.parametrize("case", PHI_CORPUS, ids=lambda case: case["id"])
def test_corpus_detection(case: dict) -> None:
    xfail_reason = case.get("xfail_reason")
    if xfail_reason:
        pytest.xfail(xfail_reason)

    profile = case.get("profile", "balanced")
    threshold = case.get("score_threshold", 0.35)
    redactor = PHIRedactor(entity_profile=profile)
    result = redactor.redact(case["text"], score_threshold=threshold)

    for entity_type in case.get("must_detect", []):
        assert entity_type in result.entities_detected, (
            f"{case['id']}: expected {entity_type} in {result.entities_detected}"
        )

    for substring in case.get("must_redact_substrings", []):
        assert substring not in result.redacted_text, (
            f"{case['id']}: expected {substring!r} to be redacted"
        )

    for substring in case.get("must_not_redact_substrings", []):
        assert substring in result.redacted_text, (
            f"{case['id']}: balanced profile should preserve {substring!r}"
        )

    for substring in case.get("must_redact_substrings_profile", []):
        assert substring not in result.redacted_text, (
            f"{case['id']}: aggressive profile should redact {substring!r}"
        )


@presidio
def test_redact_deanonymize_round_trip() -> None:
    redactor = PHIRedactor(entity_profile="balanced")
    original = "Member Jane Doe, SSN 987-65-4321, email jane@example.org."
    result = redactor.redact(original, score_threshold=0.25)
    assert result.entity_count >= 2
    assert "Jane Doe" not in result.redacted_text
    restored = redactor.deanonymize(result.redacted_text)
    assert "Jane Doe" in restored
    assert "987-65-4321" in restored


@presidio
def test_session_isolation_between_redactors() -> None:
    first = PHIRedactor(entity_profile="balanced")
    second = PHIRedactor(entity_profile="balanced")
    first.redact("Patient Alice Smith SSN 111-22-3333.", score_threshold=0.25)
    second.redact("Patient Bob Jones SSN 444-55-6666.", score_threshold=0.25)
    assert first.active_token_count >= 1
    assert second.active_token_count >= 1
    assert first._token_to_value != second._token_to_value
