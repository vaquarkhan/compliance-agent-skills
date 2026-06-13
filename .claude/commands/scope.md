# /scope — Engagement Scoping

Define the audit boundary before any control testing.

## Instructions

1. **Identify frameworks** — HIPAA, PCI-DSS v4.0, SOC 2 (list all that apply).
2. **List in-scope systems** — URLs, apps, databases, MCP servers, identity providers, cloud accounts.
3. **Classify data** — ePHI, CHD/SAD, confidential, public.
4. **Document exclusions** with rationale.
5. **Record authorization** — written approval to scan/test production (if applicable).
6. **Assign engagement ID** — `ENG-{YYYYMMDD}-{slug}`.

## Output artifact

Create `scope-{engagement-id}.json`:

```json
{
  "engagement_id": "ENG-2026-001",
  "created_at": "2026-06-13T00:00:00Z",
  "frameworks": ["HIPAA-Security-Rule"],
  "in_scope": [],
  "out_of_scope": [],
  "data_classes": [],
  "approver": "",
  "authorization_date": null
}
```

## Apply preset

If industry/cloud named, read matching `presets/*/PRESET.md`.

## Skill

Load `using-compliance-agent-skills` Step 2 (Scope definition).

## Next command

Proceed to `/audit` when scope is approved.
