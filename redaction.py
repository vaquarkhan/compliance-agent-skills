"""HIPAA-oriented PHI/PII redaction using Microsoft Presidio.

Incoming text is scanned before it reaches the Pydantic AI reasoning engine.
Detected entities are replaced with reversible masked tokens (e.g. ``<PERSON_1>``).
Authorized downstream consumers can restore original values via :meth:`PHIRedactor.deanonymize`.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field

from presidio_analyzer import AnalyzerEngine
from presidio_analyzer.nlp_engine import NlpEngineProvider
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig, RecognizerResult

# Entity types commonly associated with HIPAA ePHI and general PII.
DEFAULT_ENTITY_TYPES: list[str] = [
    "PERSON",
    "PHONE_NUMBER",
    "EMAIL_ADDRESS",
    "US_SSN",
    "US_DRIVER_LICENSE",
    "US_PASSPORT",
    "US_BANK_NUMBER",
    "CREDIT_CARD",
    "DATE_TIME",
    "MEDICAL_LICENSE",
    "IP_ADDRESS",
    "LOCATION",
    "NRP",
    "URL",
]


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
        spacy_model: str = "en_core_web_sm",
        language: str = "en",
    ) -> None:
        self.entity_types = entity_types or DEFAULT_ENTITY_TYPES
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

    def reset_session(self) -> None:
        """Clear token counters and mappings for a new agent session."""
        self._token_counters.clear()
        self._token_to_value.clear()

    def _next_token(self, entity_type: str, original_value: str) -> str:
        self._token_counters[entity_type] += 1
        token = f"<{entity_type}_{self._token_counters[entity_type]}>"
        self._token_to_value[token] = original_value
        return token

    def _build_operators(self, analyzer_results: list[RecognizerResult]) -> dict[str, OperatorConfig]:
        """Create per-entity custom operators that emit stable masked tokens."""

        def make_token_lambda(entity_type: str):
            def token_lambda(value: str) -> str:
                return self._next_token(entity_type, value)

            return token_lambda

        operators: dict[str, OperatorConfig] = {}
        for entity_type in {result.entity_type for result in analyzer_results}:
            operators[entity_type] = OperatorConfig(
                "custom",
                {"lambda": make_token_lambda(entity_type)},
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

        operators = self._build_operators(analyzer_results)

        anonymized = self._anonymizer.anonymize(
            text=text,
            analyzer_results=analyzer_results,
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
        # Replace longer tokens first to avoid partial overlap issues.
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
