# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.6.0] - 2026-06-13

### Added

- **Engineering hardening** — CI lint (Ruff), mypy, security scans (pip-audit, Bandit, detect-secrets), CodeQL
- **Dependency locks** — `requirements.in` + `requirements-lock.txt` (pip-tools); bumped `pydantic-ai>=1.74` for skills compatibility
- **Coverage gate** — pytest-cov ≥80% on `agent.py` + `redaction.py`
- **Pre-commit** — Ruff, detect-secrets, validators (`.pre-commit-config.yaml`)
- **Dependabot** — pip, npm, gradle, GitHub Actions
- **Docs** — architecture diagram, redaction limitations, SME review cadence
- **Examples** — FERPA, COPPA, NIST AI RMF runnable validators
- **Repo hygiene** — CODEOWNERS, issue/PR templates, CITATION.cff
- PCI-DSS v4.0.1 timeliness note and provenance footers (PCI, SME standard in `docs/sme-review.md`)

## [1.5.0] - 2026-06-13

### Added

- **Phase 5 skills** — AI governance and youth privacy:
  - `nist-ai-rmf-governance` — NIST AI RMF 1.0 GOVERN/MAP/MEASURE/MANAGE for LLM agents
  - `ferpa-education-records` — FERPA school officials, LEI, EdTech agent controls
  - `coppa-children-privacy` — FTC COPPA VPC, direct notice, LLM service providers
- Checklists, templates, `edtech-youth-privacy` preset and starter pack
- Agent personas: NIST AI RMF assessor, FERPA officer, COPPA officer

## [1.4.0] - 2026-06-13

### Added

- **Phase 4 skills** — multinational privacy coverage:
  - `hitech-breach-notification` — HITECH Act depth, OCR portal, unsecured PHI, BA liability
  - `us-state-privacy-laws` — VCDPA, CPA, TDPSA, and multi-state harmonized programs
  - `gdpr-us-multinational` — GDPR for US multinationals (RoPA, SCCs/DPF, 72-hour breach, DPIA)
- Reference checklists and templates (HITECH workbook, state assessment, GDPR RoPA)
- Preset `multinational-privacy` and starter pack `multinational-privacy-starter.yaml`
- Agent personas: HITECH breach coordinator, state privacy analyst, GDPR DPO advisor

## [1.3.0] - 2026-06-13

### Fixed

- **Breaking (security):** `run_compliance_agent` no longer auto-deanonymizes output. Deanonymization is opt-in via `deanonymize_output=True` or `COMPLIANCE_AGENT_DEANONYMIZE=1`. The `deanonymize_response` tool now requires session authorization.
- Redaction default profile is **`balanced`** (preserves URLs/dates in audit text); use `entity_profile="aggressive"` for maximum PHI recall.
- `hash_evidence.py` writes the manifest once (removed placeholder double-write).

### Added

- Test suite: synthetic PHI corpus, unit/integration tests, pytest wired in CI
- `Makefile` targets: `validate`, `test`, `demo`, `sync-version`
- `VERSION` single source of truth + `scripts/sync-version.py`
- Custom SSN pattern recognizer (dashed and spaced formats) in `redaction.py`
- Example custom MRN recognizer: `examples/custom-ssn-recognizer.py`
- `scripts/smoke_syntax.py` — AST syntax check in CI validate job

## [1.2.0] - 2026-06-13

### Added

- **Phase 3 skills** — enterprise and regulated-industry coverage:
  - `fedramp-moderate-baseline` — FedRAMP Moderate, NIST SP 800-53 Rev 5, SSP/POA&M/ConMon
  - `sox-itgc-audit` — Sarbanes-Oxley IT general controls (COSO / SOX 404)
  - `cmmc-nist-800-171` — CMMC 2.0 Level 2, CUI, SPRS scoring
  - `glba-ffiec-financial-privacy` — GLBA Safeguards/Privacy, FFIEC alignment
- Reference checklists, templates (SSP outline, SOX ITGC matrix, CMMC POA&M)
- Preset `financial-services-glba` and starter pack `enterprise-regulated-starter.yaml`
- Phase 3 agent personas (FedRAMP 3PAO, SOX IT auditor, CMMC assessor, GLBA officer)
- Full documentation wiring: README, CLAUDE.md, Copilot instructions, cursor routing rules, lifecycle commands

## [1.1.0] - 2026-06-13

### Added

- **Phase 2 skills** (full workflows, not stubs):
  - `iso27001-annex-a-controls` — ISO/IEC 27001:2022 Annex A and Statement of Applicability
  - `nist-csf-2-assessment` — NIST Cybersecurity Framework 2.0 six Functions
  - `ccpa-cpra-privacy-rights` — California CCPA/CPRA consumer rights and DSAR
  - `pci-dss-encryption-key-management` — PCI-DSS v4.0 Req 3/4 encryption and key management
  - `hipaa-privacy-minimum-necessary` — HIPAA Privacy Rule minimum necessary and de-identification
- Reference checklists and templates for ISO 27001, NIST CSF 2.0, and CCPA/CPRA
- `scripts/validate-plugin-manifest.py` and `scripts/sync-install-manifest.py`

## [1.0.0] - 2026-06-13

### Added

- Initial release of **compliance-agent-skills** for USA regulatory frameworks:
  - **HIPAA** Security Rule and Breach Notification workflows
  - **PCI-DSS v4.0** script inventory, network segmentation, and Req 10 logging
  - **SOC 2** Trust Services Criteria mapping, evidence collection, and CCM
- Pydantic AI agent entry point (`agent.py`) with mandatory Presidio PHI redaction gate (`redaction.py`)
- 15 progressive-disclosure Agent Skills under `skills/`
- VS Code extension and JetBrains plugin install surfaces
- Templates, starter packs, presets, and reference checklists
- MCP server templates (Playwright, Postgres, Presidio, Slack, GitHub, Terraform)
- Cursor rules, Claude commands, and Copilot instructions for audit lifecycle
- Validation scripts for skills frontmatter and registry assets
- Example audit workflows: PCI checkout script audit, HIPAA PHI redaction, SOC 2 evidence bundle

### Security

- PHI redaction runs upstream of all LLM reasoning; reversible tokens require explicit deanonymization tool call

[1.5.0]: https://github.com/vaquarkhan/compliance-agent-skills/releases/tag/v1.5.0
[1.4.0]: https://github.com/vaquarkhan/compliance-agent-skills/releases/tag/v1.4.0
[1.3.0]: https://github.com/vaquarkhan/compliance-agent-skills/releases/tag/v1.3.0
[1.2.0]: https://github.com/vaquarkhan/compliance-agent-skills/releases/tag/v1.2.0
[1.1.0]: https://github.com/vaquarkhan/compliance-agent-skills/releases/tag/v1.1.0
[1.0.0]: https://github.com/vaquarkhan/compliance-agent-skills/releases/tag/v1.0.0
