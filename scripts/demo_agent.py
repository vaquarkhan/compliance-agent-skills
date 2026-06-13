#!/usr/bin/env python3
"""End-to-end demo using TestModel (no API key). Shows redaction + agent run."""

from __future__ import annotations

import asyncio
import os
import sys
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agent import run_compliance_agent
from redaction import PHIRedactor


async def main() -> int:
    prompt = (
        sys.argv[1]
        if len(sys.argv) > 1
        else "Scope a HIPAA review for patient Jane Doe (SSN 123-45-6789) in our LLM pipeline."
    )
    print("=== Input (raw) ===")
    print(prompt)
    print()

    redaction = PHIRedactor().redact(prompt, score_threshold=0.25)
    print("=== After Presidio redaction (sent to model) ===")
    print(redaction.redacted_text)
    print(f"Entities masked: {redaction.entities_detected} ({redaction.entity_count} spans)")
    print()

    has_api_key = bool(os.environ.get("OPENAI_API_KEY") or os.environ.get("ANTHROPIC_API_KEY"))
    if has_api_key:
        output = await run_compliance_agent(prompt, deanonymize_output=False)
    else:
        print("=== Agent (TestModel mock — no API key) ===")
        mock_result = MagicMock()
        mock_result.output = (
            "Scoped HIPAA LLM pipeline review. Redacted subject tokens preserved in output."
        )
        with patch("agent.compliance_agent.run", new_callable=AsyncMock, return_value=mock_result):
            output = await run_compliance_agent(prompt, deanonymize_output=False)

    print(output)
    print()
    print("Deanonymization is opt-in: deanonymize_output=True or COMPLIANCE_AGENT_DEANONYMIZE=1")
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
