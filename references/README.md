# References

Selector guide for compliance reference documents in this repository.

## By framework

| Framework | Document | Use when |
| --- | --- | --- |
| HIPAA | [hipaa-security-rule-checklist.md](hipaa-security-rule-checklist.md) | Security Rule §164.312 technical control reviews |
| PCI-DSS v4.0 | [pci-dss-v4-checklist.md](pci-dss-v4-checklist.md) | Merchant SAQ or ROC preparation |
| SOC 2 | [soc2-trust-services-checklist.md](soc2-trust-services-checklist.md) | TSC mapping and Type II readiness |

## By topic

| Topic | Document | Use when |
| --- | --- | --- |
| MCP hardening | [mcp-compliance-patterns.md](mcp-compliance-patterns.md) | Deploying or auditing MCP servers |
| PHI redaction | [phi-redaction-patterns.md](phi-redaction-patterns.md) | Tuning Presidio / `redaction.py` |
| Policy-as-code | [compliance-as-code-patterns.md](compliance-as-code-patterns.md) | OPA, Terraform, CI gates |

## Related skills

Each reference pairs with one or more skills — see [skills-index.md](../skills-index.md).

## Validation

References are indexed in [registry/assets.json](../registry/assets.json). Run:

```bash
python scripts/validate-assets.py
```
