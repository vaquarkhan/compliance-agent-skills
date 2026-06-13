"""Compliance agent entry point.

Orchestrates Pydantic AI with Agent Skills (progressive disclosure) and a Presidio
PHI redaction gate so raw ePHI never reaches the model reasoning engine.
"""

from __future__ import annotations

import asyncio
import os
from dataclasses import dataclass, field
from pathlib import Path

from pydantic_ai import Agent, RunContext
from pydantic_ai_skills import SkillsCapability

from redaction import PHIRedactor, RedactionResult

SKILLS_DIR = Path(__file__).resolve().parent / "skills"
DEFAULT_MODEL = os.environ.get("COMPLIANCE_AGENT_MODEL", "openai:gpt-4o")


def _resolve_model() -> str | object:
    """Use TestModel locally when no provider API key is configured."""
    if os.environ.get("OPENAI_API_KEY") or os.environ.get("ANTHROPIC_API_KEY"):
        return DEFAULT_MODEL
    from pydantic_ai.models.test import TestModel

    return TestModel()


@dataclass
class ComplianceDeps:
    """Type-safe dependencies injected into tools via :class:`RunContext`."""

    redactor: PHIRedactor = field(default_factory=PHIRedactor)
    last_redaction: RedactionResult | None = None


compliance_agent = Agent(
    model=_resolve_model(),
    deps_type=ComplianceDeps,
    instructions=(
        "You are a deterministic USA compliance auditing assistant. "
        "Follow loaded Agent Skills exactly—never invent regulatory steps. "
        "Use progressive disclosure: call load_skill only when a skill matches the task. "
        "All user-provided text you receive has already passed through PHI redaction; "
        "do not attempt to reconstruct redacted token values."
    ),
    capabilities=[
        SkillsCapability(
            directories=[str(SKILLS_DIR)],
            validate=True,
        ),
    ],
)


@compliance_agent.system_prompt
async def redaction_context(ctx: RunContext[ComplianceDeps]) -> str:
    """Surface redaction state to the model without exposing raw PHI."""
    if ctx.deps.last_redaction and ctx.deps.last_redaction.entity_count:
        entities = ", ".join(ctx.deps.last_redaction.entities_detected)
        return (
            f"PHI redaction active: {ctx.deps.last_redaction.entity_count} "
            f"entity(ies) masked ({entities}). Tokens like <PERSON_1> are intentional."
        )
    return "PHI redaction active: no sensitive entities detected in the user prompt."


@compliance_agent.tool
def deanonymize_response(ctx: RunContext[ComplianceDeps], text: str) -> str:
    """Restore masked PHI tokens in agent output for authorized downstream delivery."""
    return ctx.deps.redactor.deanonymize(text)


@compliance_agent.tool
def redaction_status(ctx: RunContext[ComplianceDeps]) -> dict[str, int | list[str]]:
    """Report how many reversible PHI tokens exist in the current session."""
    last = ctx.deps.last_redaction
    return {
        "active_tokens": ctx.deps.redactor.active_token_count,
        "last_pass_entities": last.entities_detected if last else [],
        "last_pass_entity_count": last.entity_count if last else 0,
    }


async def run_compliance_agent(user_prompt: str, *, deps: ComplianceDeps | None = None) -> str:
    """Execute the compliance agent with mandatory PHI redaction upstream."""
    run_deps = deps or ComplianceDeps()
    run_deps.redactor.reset_session()
    redaction = run_deps.redactor.redact(user_prompt)
    run_deps.last_redaction = redaction

    result = await compliance_agent.run(redaction.redacted_text, deps=run_deps)
    return run_deps.redactor.deanonymize(result.output)


def run_compliance_agent_sync(user_prompt: str, *, deps: ComplianceDeps | None = None) -> str:
    """Synchronous wrapper around :func:`run_compliance_agent`."""
    return asyncio.run(run_compliance_agent(user_prompt, deps=deps))


if __name__ == "__main__":
    import sys

    prompt = " ".join(sys.argv[1:]) or (
        "Audit checkout scripts on https://example.com/checkout for PCI-DSS 6.4.3."
    )
    print(run_compliance_agent_sync(prompt))
