"""Shared pytest fixtures."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

FIXTURES = Path(__file__).resolve().parent / "fixtures"
CORPUS_PATH = FIXTURES / "synthetic_phi_corpus.yaml"


@pytest.fixture(scope="session")
def phi_corpus() -> list[dict]:
    data = yaml.safe_load(CORPUS_PATH.read_text(encoding="utf-8"))
    return data["cases"]
