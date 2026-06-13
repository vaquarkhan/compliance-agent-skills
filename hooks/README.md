# Compliance Agent Hooks

Cursor/IDE hooks for session safety, PHI redaction enforcement, and audit mode.

## Files

| Hook | Trigger | Purpose |
| --- | --- | --- |
| `session-start.sh` / `.ps1` | Session start | Load engagement context, validate env |
| `phi-redaction-guard.sh` / `.ps1` | Before agent prompt | Enforce redaction flag |
| `audit-mode.sh` | Manual / scheduled | Enable read-only MCP and evidence paths |
| `release-guard.sh` | Pre-release | Block releases with open HIGH findings |

Configuration: [hooks.json](hooks.json)

## Installation

```bash
./bootstrap.sh --target cursor
```

Merge `hooks.json` into your project's `.cursor/hooks.json` or global hooks config.

## Environment variables

| Variable | Values | Effect |
| --- | --- | --- |
| `COMPLIANCE_PHI_REDACTION` | `required` | Block session if redaction unavailable |
| `COMPLIANCE_AUDIT_MODE` | `true` | Read-only tools, evidence dir enforced |
| `COMPLIANCE_ENGAGEMENT_ID` | `ENG-*` | Tag all artifacts |

## Windows support

PowerShell equivalents provided for `session-start` and `phi-redaction-guard`.
