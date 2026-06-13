"""HIPAA-oriented PHI/PII redaction using Microsoft Presidio.

Incoming text is scanned before it reaches the Pydantic AI reasoning engine.
Detected entities are replaced with reversible masked tokens (e.g. ``<PERSON_1>``).
Authorized downstream consumers can restore original values via :meth:`PHIRedactor.deanonymize`.

Entity profiles
---------------
``balanced`` (default)
    Core identifiers (names, SSN, email, phone, cards, licenses). Omits DATE_TIME,
    URL, LOCATION, and NRP to reduce over-redaction in audit text (e.g. checkout URLs
    for PCI script audits).

``aggressive``
    All types in :data:`AGGRESSIVE_ENTITY_TYPES`, including DATE_TIME and URL.
    Use when clinical notes or free-text PHI dominates and false negatives are
    unacceptable.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any, Literal

from presidio_analyzer import AnalyzerEngine, Pattern, PatternRecognizer
from presidio_analyzer.nlp_engine import NlpEngineProvider
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig

# Presidio invokes custom operator lambdas twice: once with this sentinel for
# validation, then with the real matched text. Never store a token for the probe.
PII_VALIDATION_PROBE = "PII"

EntityProfile = Literal["balanced", "aggressive"]

# Core PHI/PII — suitable for most compliance audit prompts.
BALANCED_ENTITY_TYPES: list[str] = [
    "PERSON",
    "PHONE_NUMBER",
    "EMAIL_ADDRESS",
    "US_SSN",
    "US_DRIVER_LICENSE",
    "US_PASSPORT",
    "US_BANK_NUMBER",
    "CREDIT_CARD",
    "MEDICAL_LICENSE",
    "IP_ADDRESS",
]

# Includes DATE_TIME, LOCATION, NRP, URL — higher recall, more false positives.
AGGRESSIVE_ENTITY_TYPES: list[str] = BALANCED_ENTITY_TYPES + [
    "DATE_TIME",
    "LOCATION",
    "NRP",
    "URL",
]

ENTITY_PROFILES: dict[EntityProfile, list[str]] = {
    "balanced": BALANCED_ENTITY_TYPES,
    "aggressive": AGGRESSIVE_ENTITY_TYPES,
}

# Backward-compatible alias for documentation and skills referencing DEFAULT_ENTITY_TYPES.
DEFAULT_ENTITY_TYPES: list[str] = AGGRESSIVE_ENTITY_TYPES


@dataclass
class RedactionResult:
    """Output of a single redaction pass."""

    original_text: str
    redacted_text: str
    entity_count: int
    entities_detected: list[str] = field(default_factory=list)


class PHIRedactor:
    """Detect and mask PHI/PII with reversible token placeholders."""

    def __init__(
        self,
        *,
        entity_types: list[str] | None = None,
        entity_profile: EntityProfile = "balanced",
        spacy_model: str = "en_core_web_sm",
        language: str = "en",
    ) -> None:
        if entity_types is not None:
            self.entity_types = entity_types
        else:
            self.entity_types = ENTITY_PROFILES[entity_profile]
        self.entity_profile = entity_profile
        self.language = language
        self._token_counters: dict[str, int] = defaultdict(int)
        self._token_to_value: dict[str, str] = {}

        nlp_configuration = {
            "nlp_engine_name": "spacy",
            "models": [{"lang_code": language, "model_name": spacy_model}],
        }
        provider = NlpEngineProvider(nlp_configuration=nlp_configuration)
        nlp_engine = provider.create_engine()

        self._analyzer = AnalyzerEngine(nlp_engine=nlp_engine, supported_languages=[language])
        self._anonymizer = AnonymizerEngine()
        self._register_custom_recognizers()

    def _register_custom_recognizers(self) -> None:
        """Register pattern recognizers for formats Presidio's defaults often miss."""
        ssn_recognizer = PatternRecognizer(
            supported_entity="US_SSN",
            patterns=[
                Pattern(name="ssn_dashed", regex=r"\b\d{3}-\d{2}-\d{4}\b", score=0.9),
                Pattern(name="ssn_spaced", regex=r"\b\d{3}\s+\d{2}\s+\d{4}\b", score=0.85),
            ],
        )
        self._analyzer.registry.add_recognizer(ssn_recognizer)

    def reset_session(self) -> None:
        """Clear token counters and mappings for a new agent session."""
        self._token_counters.clear()
        self._token_to_value.clear()

    def _next_token(self, entity_type: str, original_value: str) -> str:
        self._token_counters[entity_type] += 1
        token = f"<{entity_type}_{self._token_counters[entity_type]}>"
        self._token_to_value[token] = original_value
        return token

    def _preassign_tokens(
        self, text: str, analyzer_results: list[Any]
    ) -> dict[str, dict[str, str]]:
        """Assign one stable token per unique (entity_type, matched span text).

        Presidio's custom operators must not mint tokens inside the lambda — the
        engine calls it with ``PII_VALIDATION_PROBE`` before the real value.
        """
        lookups: dict[str, dict[str, str]] = defaultdict(dict)
        for result in analyzer_results:
            matched = text[result.start : result.end]
            entity_type = result.entity_type
            if matched in lookups[entity_type]:
                continue
            token = self._next_token(entity_type, matched)
            lookups[entity_type][matched] = token
        return lookups

    def _build_operators(
        self, token_lookups: dict[str, dict[str, str]]
    ) -> dict[str, OperatorConfig]:
        """Create per-entity operators that look up pre-assigned tokens."""

        def make_token_lambda(entity_type: str, lookup: dict[str, str]):
            def token_lambda(value: str) -> str:
                if value == PII_VALIDATION_PROBE:
                    return PII_VALIDATION_PROBE
                return lookup[value]

            return token_lambda

        operators: dict[str, OperatorConfig] = {}
        for entity_type, lookup in token_lookups.items():
            operators[entity_type] = OperatorConfig(
                "custom",
                {"lambda": make_token_lambda(entity_type, lookup)},
            )
        return operators

    def redact(self, text: str, *, score_threshold: float = 0.35) -> RedactionResult:
        """Scan *text* and return a tokenized copy safe for LLM ingestion."""
        if not text.strip():
            return RedactionResult(original_text=text, redacted_text=text, entity_count=0)

        analyzer_results = self._analyzer.analyze(
            text=text,
            language=self.language,
            entities=self.entity_types,
            score_threshold=score_threshold,
        )

        if not analyzer_results:
            return RedactionResult(original_text=text, redacted_text=text, entity_count=0)

        token_lookups = self._preassign_tokens(text, analyzer_results)
        operators = self._build_operators(token_lookups)

        anonymized = self._anonymizer.anonymize(
            text=text,
            analyzer_results=analyzer_results,  # type: ignore[arg-type]
            operators=operators or {"DEFAULT": OperatorConfig("redact", {})},
        )

        entities_detected = sorted({result.entity_type for result in analyzer_results})
        return RedactionResult(
            original_text=text,
            redacted_text=anonymized.text,
            entity_count=len(analyzer_results),
            entities_detected=entities_detected,
        )

    def deanonymize(self, text: str) -> str:
        """Restore masked tokens in *text* using the current session mapping."""
        restored = text
        for token in sorted(self._token_to_value, key=len, reverse=True):
            restored = restored.replace(token, self._token_to_value[token])
        return restored

    @property
    def active_token_count(self) -> int:
        return len(self._token_to_value)


def redact_text(text: str, *, redactor: PHIRedactor | None = None) -> tuple[str, PHIRedactor]:
    """Convenience helper: redact *text* and return ``(redacted_text, redactor)``."""
    engine = redactor or PHIRedactor()
    result = engine.redact(text)
    return result.redacted_text, engine
