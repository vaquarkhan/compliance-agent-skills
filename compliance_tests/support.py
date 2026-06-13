"""Test helpers (local imports only — avoid ``tests.conftest`` cross-project shadowing)."""

from __future__ import annotations

import pytest


def presidio_available() -> bool:
    try:
        import spacy  # noqa: F401
        from presidio_analyzer import AnalyzerEngine  # noqa: F401

        return True
    except ImportError:
        return False


presidio = pytest.mark.skipif(
    not presidio_available(),
    reason="Presidio/spaCy not installed (pip install -r requirements.txt)",
)
