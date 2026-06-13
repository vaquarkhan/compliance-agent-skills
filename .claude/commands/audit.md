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
| HIPAA | `hipaa-technical-safeguards`, `hipaa-phi-redaction-pipeline`, `hipaa-privacy-minimum-necessary` |
| PCI-DSS | `pci-dss-script-audit`, `pci-dss-network-segmentation`, `pci-dss-encryption-key-management` |
| SOC 2 | `soc2-trust-services-criteria`, `soc2-evidence-collection`, `soc2-ccm-continuous-monitoring` |
| ISO 27001 | `iso27001-annex-a-controls` |
| NIST CSF 2.0 | `nist-csf-2-assessment` |
| CCPA / CPRA | `ccpa-cpra-privacy-rights` |
| FedRAMP | `fedramp-moderate-baseline` |
| SOX | `sox-itgc-audit` |
| CMMC | `cmmc-nist-800-171` |
| GLBA / FFIEC | `glba-ffiec-financial-privacy` |

## Next command

Proceed to `/evidence` to collect proof artifacts.
