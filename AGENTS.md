# AGENTS.md — Compliance Agent Entry Point

This file is the **primary routing document** for AI coding agents working in this repository. Read it before loading any skill.

## Mission

Execute **deterministic USA compliance audits** across HIPAA, HITECH, PCI-DSS v4.0, SOC 2, ISO 27001, NIST CSF 2.0, NIST AI RMF, FERPA, COPPA, CCPA/CPRA, US state privacy laws, GDPR, FedRAMP, SOX, CMMC, and GLBA/FFIEC without inventing regulatory requirements. All user-provided text passes through **PHI redaction** (`redaction.py`) before LLM reasoning.

## Mandatory rules

1. **Load skills progressively** — use `using-compliance-agent-skills` for routing; then load exactly one primary framework skill per audit thread.
2. **Never reconstruct redacted tokens** (`<PERSON_1>`, `<US_SSN_1>`) unless using the authorized `deanonymize_response` tool in `agent.py`.
3. **Cite authoritative sources** — CFR, PCI-DSS v4.0, AICPA TSC. Do not fabricate requirement numbers.
4. **Emit auditable artifacts** — scope JSON, evidence manifests with SHA-256 hashes, remediation trackers.
5. **Respect lifecycle order** when possible: `/scope` → `/audit` → `/evidence` → `/remediate` → `/report`.

## Skill routing

| Signal in user request | Primary skill |
| --- | --- |
| Broad / unclear framework | `using-compliance-agent-skills` |
| PHI, ePHI, BAA, Security Rule | `hipaa-technical-safeguards`, `hipaa-phi-redaction-pipeline`, or `hipaa-baa-vendor-assessment` |
| Payment scripts, checkout, Req 6.4.3 | `pci-dss-script-audit` |
| CDE, firewall, segmentation | `pci-dss-network-segmentation` |
| TSC mapping, SOC 2 scope | `soc2-trust-services-criteria` |
| Audit binder, screenshots | `soc2-evidence-collection` |
| Continuous monitoring | `soc2-ccm-continuous-monitoring` |
| IAM, MFA, RBAC | `access-control-identity-audit` |
| Logs, SIEM, Req 10 | `audit-logging-integrity` |
| Breach, incident notification | `breach-incident-response` |
| HITECH breach / OCR portal | `hitech-breach-notification` |
| US state privacy (VCDPA, CPA, TDPSA) | `us-state-privacy-laws` |
| GDPR / EU transfers (US multinational) | `gdpr-us-multinational` |
| Vendor SOC reports | `vendor-third-party-risk` |
| OPA, Terraform, policy-as-code | `compliance-as-code-governance` |
| MCP server hardening | `mcp-compliance-integration` |
| ISO 27001 Annex A / SoA | `iso27001-annex-a-controls` |
| NIST CSF 2.0 gap assessment | `nist-csf-2-assessment` |
| CCPA/CPRA, DSAR, California privacy | `ccpa-cpra-privacy-rights` |
| PCI encryption, PAN, key management | `pci-dss-encryption-key-management` |
| HIPAA minimum necessary / de-id | `hipaa-privacy-minimum-necessary` |
| FedRAMP Moderate / NIST 800-53 | `fedramp-moderate-baseline` |
| SOX ITGC / SOX 404 | `sox-itgc-audit` |
| CMMC / CUI / NIST 800-171 | `cmmc-nist-800-171` |
| GLBA / FFIEC financial privacy | `glba-ffiec-financial-privacy` |
| NIST AI RMF / trustworthy AI | `nist-ai-rmf-governance` |
| FERPA / education records / EdTech | `ferpa-education-records` |
| COPPA / under-13 / child-directed app | `coppa-children-privacy` |

Full catalog: [skills-index.md](skills-index.md).

## Presets

Apply a preset when the user names an industry or cloud:

| Preset | Path |
| --- | --- |
| Healthcare HIPAA | `presets/healthcare-hipaa/PRESET.md` |
| Fintech PCI-DSS | `presets/fintech-pci-dss/PRESET.md` |
| SaaS SOC 2 Type II | `presets/saas-soc2-type2/PRESET.md` |
| Financial GLBA/FFIEC | `presets/financial-services-glba/PRESET.md` |
| Multinational privacy | `presets/multinational-privacy/PRESET.md` |
| EdTech & youth privacy | `presets/edtech-youth-privacy/PRESET.md` |
| AWS | `presets/aws-compliance/PRESET.md` |
| Azure | `presets/azure-compliance/PRESET.md` |
| GCP | `presets/gcp-compliance/PRESET.md` |

## Persona agents

For role-play or multi-agent workflows, see `agents/`:

- `compliance-architect.md` — cross-framework design
- `hipaa-privacy-officer.md` — HIPAA Privacy/Security Rule focus
- `pci-qsa-reviewer.md` — PCI-DSS v4.0 QSA-style review
- `soc2-auditor.md` — TSC evidence and testing
- `fedramp-3pao-advisor.md` — FedRAMP Moderate authorization packages
- `sox-it-auditor.md` — SOX 404 IT general controls
- `cmmc-assessor.md` — CMMC Level 2 / CUI assessments
- `glba-compliance-officer.md` — GLBA Safeguards and Privacy
- `gdpr-dpo-advisor.md` — GDPR RoPA, transfers, DPIA for US multinationals
- `hitech-breach-coordinator.md` — HITECH OCR breach workflows
- `state-privacy-analyst.md` — Multi-state US privacy (VCDPA, CPA, TDPSA)
- `nist-ai-rmf-assessor.md` — NIST AI RMF trustworthy AI governance
- `ferpa-compliance-officer.md` — FERPA education records and school officials
- `coppa-privacy-officer.md` — FTC COPPA parental consent and child-directed apps

## MCP servers

Configure from `mcp/` before technical audits requiring browser, database, or IaC access. See `mcp/README.md`.

## Key files

| File | Role |
| --- | --- |
| `agent.py` | Pydantic AI agent + skills capability |
| `redaction.py` | Presidio PHI gate |
| `registry/assets.json` | Templates, packs, examples index |
| `templates/` | YAML/MD artifact scaffolds |
| `hooks/hooks.json` | Session PHI guard, audit mode |

## Validation

Before committing skill or asset changes:

```bash
python scripts/validate-skills.py
python scripts/validate-assets.py
python scripts/validate-plugin-manifest.py
```
