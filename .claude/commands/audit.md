# /audit — Control Testing

Execute framework-specific control tests against scoped systems.

## Prerequisites

- Completed `/scope` artifact with approver sign-off
- Primary skill selected from routing table (see `AGENTS.md`)

## Instructions

1. **Confirm scope** — restate in-scope systems and frameworks.
2. **Load primary skill** — follow its Core Process exactly.
3. **Execute tests** — use MCP tools only if authorized in scope.
4. **Record findings** — severity, control ID, observation, evidence refs.
5. **Do not claim compliance** — report pass/fail/not-tested per control.

## MCP audit mode

Run `hooks/audit-mode.sh` or set `COMPLIANCE_AUDIT_MODE=true` for read-only tool enforcement.

## Output

- Findings list (YAML or JSON)
- Updated control matrix (`templates/compliance-control-matrix.yaml`)
- Test notes with UTC timestamps and tester identity

## Framework skills

| Framework | Skills |
| --- | --- |
| HIPAA | `hipaa-technical-safeguards`, `hipaa-phi-redaction-pipeline` |
| PCI | `pci-dss-script-audit`, `pci-dss-network-segmentation` |
| SOC 2 | `soc2-trust-services-criteria` |

## Next command

Proceed to `/evidence` to collect proof artifacts.
