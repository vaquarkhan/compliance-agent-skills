# Regulatory reports

Structured **findings reports** for the `/report` audit lifecycle step. Inputs are YAML (no raw PHI/PAN); outputs are Markdown suitable for executive and auditor distribution.

## Quick start

```bash
# Scaffold from template
cp templates/reports/regulatory-findings-report.yaml my-engagement/findings-input.yaml

# Edit findings-input.yaml from /scope, /audit, /evidence, /remediate outputs

# Generate Markdown
python scripts/generate-regulatory-report.py my-engagement/findings-input.yaml \
  -o my-engagement/findings-report.md
```

Or use `make report INPUT=... OUTPUT=...` (see Makefile).

## Sample reports (synthetic)

| Framework | Input | Generated report |
|-----------|--------|------------------|
| HIPAA Security Rule | [findings-input.yaml](../examples/regulatory-reports/hipaa-llm-intake/findings-input.yaml) | [findings-report.md](../examples/regulatory-reports/hipaa-llm-intake/findings-report.md) |
| PCI-DSS v4.0 (Req 6.4.3) | [findings-input.yaml](../examples/regulatory-reports/pci-checkout-scripts/findings-input.yaml) | [findings-report.md](../examples/regulatory-reports/pci-checkout-scripts/findings-report.md) |
| SOC 2 TSC | [findings-input.yaml](../examples/regulatory-reports/soc2-access-review/findings-input.yaml) | [findings-report.md](../examples/regulatory-reports/soc2-access-review/findings-report.md) |
| NIST AI RMF 1.0 | [findings-input.yaml](../examples/regulatory-reports/nist-ai-rmf-agent/findings-input.yaml) | [findings-report.md](../examples/regulatory-reports/nist-ai-rmf-agent/findings-report.md) |
| FERPA + COPPA (EdTech) | [findings-input.yaml](../examples/regulatory-reports/edtech-ferpa-coppa/findings-input.yaml) | [findings-report.md](../examples/regulatory-reports/edtech-ferpa-coppa/findings-report.md) |

## Report sections

1. Executive summary (posture, top risks, limitations)
2. Scope recap
3. Findings table (control ID, severity, evidence refs)
4. Evidence index (manifest artifact IDs — not embedded content)
5. Remediation tracker
6. Methodology (skills, MCP, redaction profile)
7. Sign-off block

## Posture values

| Value | Meaning |
|-------|---------|
| `not_assessed` | Scope only; no testing completed |
| `gaps_identified` | Fail/open findings require remediation |
| `controls_operating_effectively` | Point-in-time pass (not certification) |

## Rules

- **Never** embed raw PHI, PAN, or child PI in YAML or Markdown
- Reference evidence by **artifact ID** from `templates/audit-evidence-manifest.yaml`
- Include disclaimer: not legal advice, not attestation
- SME-reviewed regulatory mappings: see [sme-review.md](sme-review.md) (human cadence required)

## Related

- Command workflow: [`.claude/commands/report.md`](../.claude/commands/report.md)
- Evidence packaging: `templates/audit-evidence-manifest.yaml`
- Control matrix: `templates/compliance-control-matrix.yaml`
