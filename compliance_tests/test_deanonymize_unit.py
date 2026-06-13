"""Unit tests for deanonymization and session behavior (no Presidio required)."""

from __future__ import annotations

from collections import defaultdict

from redaction import PHIRedactor


def _bare_redactor() -> PHIRedactor:
    """PHIRedactor instance without loading spaCy (deanonymize-only tests)."""
    engine = object.__new__(PHIRedactor)
    engine._token_counters = defaultdict(int)
    engine._token_to_value = {}
    engine.entity_types = []
    engine.entity_profile = "balanced"
    engine.language = "en"
    return engine


def test_deanonymize_replaces_longer_tokens_first() -> None:
    redactor = _bare_redactor()
    redactor._token_to_value = {
        "<PERSON_1>": "Alice",
        "<PERSON_10>": "Bob",
    }
    text = "Seen <PERSON_10> and <PERSON_1> today."
    assert redactor.deanonymize(text) == "Seen Bob and Alice today."


def test_deanonymize_round_trip_preserves_unrelated_text() -> None:
    redactor = _bare_redactor()
    redactor._token_to_value = {"<US_SSN_1>": "123-45-6789"}
    assert redactor.deanonymize("SSN token: <US_SSN_1> end.") == "SSN token: 123-45-6789 end."


def test_reset_session_clears_token_map() -> None:
    redactor = _bare_redactor()
    redactor._token_to_value["<EMAIL_ADDRESS_1>"] = "a@b.com"
    redactor._token_counters["EMAIL_ADDRESS"] = 1
    redactor.reset_session()
    assert redactor.active_token_count == 0
    assert redactor.deanonymize("<EMAIL_ADDRESS_1>") == "<EMAIL_ADDRESS_1>"
