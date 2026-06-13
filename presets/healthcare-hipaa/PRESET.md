---
preset_id: healthcare-hipaa
name: Healthcare HIPAA
version: "1.0.0"
frameworks:
  - HIPAA-Security-Rule
  - HIPAA-Breach-Notification
industry: healthcare
---

# Healthcare HIPAA Preset

Apply this preset when auditing **covered entities** or **business associates** handling ePHI with AI agents, LLM gateways, or MCP tool integrations.

## Default skills

1. `using-compliance-agent-skills` — engagement routing
2. `hipaa-phi-redaction-pipeline` — mandatory before any LLM ingestion
3. `hipaa-technical-safeguards` — §164.312 control testing
4. `hipaa-baa-vendor-assessment` — LLM/cloud vendor BAAs

## Scope defaults

| In scope | Out of scope (unless requested) |
| --- | --- |
| ePHI flows to/from agent gateway | De-identified research datasets (verify de-id method) |
| Presidio redaction pipeline (`redaction.py`) | Non-US jurisdictions |
| MCP servers touching clinical data | Marketing websites without PHI |
| Audit logs for agent tool calls | Employee HR records without PHI |

## Required artifacts

- `templates/hipaa-phi-flow-diagram.yaml`
- `templates/breach-notification-plan.yaml`
- BAA registry with subprocessor list

## MCP configuration

Enable **Presidio MCP** and **Postgres MCP** (read-only, row-level security). Disable broad Playwright unless testing patient portals with authorization.

## Redaction entities

Use default `DEFAULT_ENTITY_TYPES` in `redaction.py` plus `MEDICAL_LICENSE` and `US_SSN`. Never disable redaction for "debugging" in production engagements.

## Lifecycle emphasis

`/scope` must document **minimum necessary** data flows before `/audit`.

## Starter pack

`starter-packs/hipaa-healthcare-starter.yaml`
