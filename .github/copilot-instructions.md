# GitHub Copilot Instructions — compliance-agent-skills

You assist with **USA compliance auditing** in this repository: HIPAA, PCI-DSS v4.0, SOC 2, ISO 27001, NIST CSF 2.0, CCPA/CPRA, FedRAMP, SOX, CMMC, and GLBA/FFIEC.

## Read first

- [AGENTS.md](../AGENTS.md) — skill routing
- [skills-index.md](../skills-index.md) — 24 skills catalog

## Core rules

1. Follow loaded Agent Skills exactly — **never invent regulatory requirements**.
2. Treat PHI redaction tokens (`<PERSON_1>`) as intentional — do not reconstruct masked values.
3. **Never** put PAN, CVV, or raw ePHI in code, comments, or suggested prompts.
4. Prefer audit lifecycle: `/scope` → `/audit` → `/evidence` → `/remediate` → `/report`.

## Skill routing (quick)

- Payment scripts → `pci-dss-script-audit`
- PHI redaction → `hipaa-phi-redaction-pipeline`
- SOC 2 mapping → `soc2-trust-services-criteria`
- ISO 27001 SoA → `iso27001-annex-a-controls`
- NIST CSF profile → `nist-csf-2-assessment`
- California DSAR → `ccpa-cpra-privacy-rights`
- FedRAMP SSP → `fedramp-moderate-baseline`
- SOX ITGC → `sox-itgc-audit`
- CMMC / CUI → `cmmc-nist-800-171`
- GLBA / banking → `glba-ffiec-financial-privacy`
- MCP hardening → `mcp-compliance-integration`
- Incidents → `breach-incident-response`

## Code changes

- Run `python scripts/validate-skills.py` when editing `skills/*/SKILL.md`
- Run `python scripts/validate-assets.py` when editing `registry/assets.json`
- Match existing patterns in `agent.py` and `redaction.py`

## Templates

Use scaffolds in `templates/` for control matrices, evidence manifests, and runbooks.

## Disclaimers

Operational guidance only — not legal advice. Recommend QSA, CPA, 3PAO, C3PAO, or Privacy Officer for formal attestation.
