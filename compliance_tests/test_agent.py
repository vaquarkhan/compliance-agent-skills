"""Agent entry-point tests (TestModel — no API key required)."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from agent import (
    ComplianceDeps,
    _env_deanonymize_enabled,
    deanonymize_response,
    run_compliance_agent,
)
from compliance_tests.support import presidio


def test_deanonymize_authorized_defaults_false() -> None:
    assert ComplianceDeps().deanonymize_authorized is False


def test_env_deanonymize_enabled(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("COMPLIANCE_AGENT_DEANONYMIZE", raising=False)
    assert _env_deanonymize_enabled() is False
    monkeypatch.setenv("COMPLIANCE_AGENT_DEANONYMIZE", "1")
    assert _env_deanonymize_enabled() is True


@presidio
@pytest.mark.asyncio
async def test_default_output_not_deanonymized() -> None:
    deps = ComplianceDeps()
    calls: list[str] = []
    original = deps.redactor.deanonymize

    def tracked_deanonymize(text: str) -> str:
        calls.append(text)
        return original(text)

    deps.redactor.deanonymize = tracked_deanonymize  # type: ignore[method-assign]

    mock_result = MagicMock()
    mock_result.output = "Findings for <PERSON_1> regarding <US_SSN_1>."

    with patch("agent.compliance_agent.run", new_callable=AsyncMock, return_value=mock_result):
        output = await run_compliance_agent(
            "Audit PHI handling for patient Jane Doe SSN 123-45-6789.",
            deps=deps,
            deanonymize_output=False,
        )

    assert calls == []
    assert "<PERSON_" in output or "<US_SSN_" in output


@presidio
@pytest.mark.asyncio
async def test_opt_in_deanonymize_restores_tokens() -> None:
    deps = ComplianceDeps()
    redaction = deps.redactor.redact(
        "Review record for Jane Doe, email jane@example.org.",
        score_threshold=0.25,
    )
    deps.last_redaction = redaction
    deps.redactor.reset_session()
    redaction = deps.redactor.redact(
        "Review record for Jane Doe, email jane@example.org.",
        score_threshold=0.25,
    )
    deps.last_redaction = redaction

    mock_result = MagicMock()
    mock_result.output = redaction.redacted_text

    with patch("agent.compliance_agent.run", new_callable=AsyncMock, return_value=mock_result):
        output = await run_compliance_agent(
            "Review record for Jane Doe, email jane@example.org.",
            deps=deps,
            deanonymize_output=True,
        )

    assert "Jane Doe" in output or "jane@example.org" in output


@presidio
def test_deanonymize_tool_requires_authorization() -> None:
    ctx = MagicMock()
    ctx.deps = ComplianceDeps(deanonymize_authorized=False)
    with pytest.raises(PermissionError, match="not authorized"):
        deanonymize_response(ctx, "token <PERSON_1>")


@presidio
def test_deanonymize_tool_allowed_when_authorized() -> None:
    deps = ComplianceDeps(deanonymize_authorized=True)
    deps.redactor._token_to_value["<PERSON_1>"] = "Jane Doe"  # noqa: SLF001
    ctx = MagicMock()
    ctx.deps = deps
    assert deanonymize_response(ctx, "Patient <PERSON_1>") == "Patient Jane Doe"
