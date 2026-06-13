# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

[1.2.0]: https://github.com/vaquarkhan/compliance-agent-skills/releases/tag/v1.2.0
[1.1.0]: https://github.com/vaquarkhan/compliance-agent-skills/releases/tag/v1.1.0
[1.0.0]: https://github.com/vaquarkhan/compliance-agent-skills/releases/tag/v1.0.0
