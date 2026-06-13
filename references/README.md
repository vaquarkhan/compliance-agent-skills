# References

Selector guide for compliance reference documents in this repository.

## Regulatory checklists (15)

Each checklist includes **Authoritative sources** and **Provenance** (review dates, reviewer role, next review due). CI validates via `make validate-sme`.

| Framework | Document | Review cadence |
| --- | --- | --- |
| HIPAA Security Rule | [hipaa-security-rule-checklist.md](hipaa-security-rule-checklist.md) | Quarterly |
| HITECH breach | [hitech-breach-checklist.md](hitech-breach-checklist.md) | Quarterly |
| PCI-DSS v4.0 | [pci-dss-v4-checklist.md](pci-dss-v4-checklist.md) | Quarterly |
| SOC 2 TSC | [soc2-trust-services-checklist.md](soc2-trust-services-checklist.md) | Quarterly |
| ISO 27001 Annex A | [iso27001-annex-a-checklist.md](iso27001-annex-a-checklist.md) | Semi-annual |
| NIST CSF 2.0 | [nist-csf-2-checklist.md](nist-csf-2-checklist.md) | Semi-annual |
| NIST AI RMF 1.0 | [nist-ai-rmf-checklist.md](nist-ai-rmf-checklist.md) | Semi-annual |
| CCPA/CPRA | [ccpa-cpra-checklist.md](ccpa-cpra-checklist.md) | Semi-annual |
| GDPR | [gdpr-article-checklist.md](gdpr-article-checklist.md) | Semi-annual |
| FedRAMP Moderate | [fedramp-moderate-checklist.md](fedramp-moderate-checklist.md) | Semi-annual |
| CMMC / 800-171 | [cmmc-nist-800-171-checklist.md](cmmc-nist-800-171-checklist.md) | Semi-annual |
| SOX ITGC | [sox-itgc-checklist.md](sox-itgc-checklist.md) | Semi-annual |
| GLBA/FFIEC | [glba-ffiec-checklist.md](glba-ffiec-checklist.md) | Semi-annual |
| FERPA | [ferpa-checklist.md](ferpa-checklist.md) | Annual |
| COPPA | [coppa-checklist.md](coppa-checklist.md) | Annual |

### Attestation note

Provenance footers are **CI-enforced** and review records live under [reviews/](../reviews/). External SME sign-off (QSA, Privacy Officer, CPA) is **documented as pending** in Q2 2026 maintainer records — see [docs/project-status.md](../docs/project-status.md).

## Other references

| Topic | Document | Use when |
| --- | --- | --- |
| US state privacy | [us-state-privacy-matrix.md](us-state-privacy-matrix.md) | Multi-state applicability |
| MCP hardening | [mcp-compliance-patterns.md](mcp-compliance-patterns.md) | Deploying or auditing MCP servers |
| PHI redaction | [phi-redaction-patterns.md](phi-redaction-patterns.md) | Tuning Presidio / `redaction.py` |
| Policy-as-code | [compliance-as-code-patterns.md](compliance-as-code-patterns.md) | OPA, Terraform, CI gates |

## Related skills

Each reference pairs with one or more skills — see [skills-index.md](../skills-index.md).

## Validation

```bash
python scripts/validate-assets.py
python scripts/validate-sme-provenance.py
make validate-sme
```

See [docs/sme-review.md](../docs/sme-review.md) for review workflow and [reviews/TEMPLATE.md](../reviews/TEMPLATE.md) for sign-off records.
