# compliance-agent-skills

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](requirements.txt)
[![HIPAA](https://img.shields.io/badge/HIPAA-Security%20Rule-green.svg)](#hipaa)
[![PCI-DSS](https://img.shields.io/badge/PCI--DSS-v4.0-red.svg)](#pci-dss)
[![SOC 2](https://img.shields.io/badge/SOC%202-TSC-purple.svg)](#soc-2)
[![Skills](https://img.shields.io/badge/skills-24-orange.svg)](skills-index.md)

**Deterministic USA compliance auditing for AI agents** — progressive-disclosure Agent Skills, a Presidio PHI redaction gate, MCP integrations, and IDE plugins for HIPAA, PCI-DSS v4.0, SOC 2, ISO 27001, NIST CSF 2.0, CCPA/CPRA, FedRAMP, SOX, CMMC, and GLBA/FFIEC workflows.

> **Disclaimer:** This repository provides operational audit patterns and automation templates. It is **not legal advice** and does not replace a Qualified Security Assessor (QSA), HIPAA Privacy Officer, or licensed CPA for SOC 2 attestation.

---

## Why this exists

LLM agents can accelerate compliance work, but they must not:

- Invent regulatory steps or cite non-existent requirements
- Send raw ePHI or cardholder data to model providers
- Produce unauditable "compliant" claims without evidence

compliance-agent-skills addresses this with:

1. **24 specialized skills** with explicit triggers, anti-patterns, and output artifacts
2. **Mandatory PHI redaction** (`redaction.py`) before any user text reaches the model
3. **Audit lifecycle commands** — `/scope`, `/audit`, `/evidence`, `/remediate`, `/report`
4. **MCP templates** for Playwright DOM audits, Postgres evidence queries, Presidio DLP, Slack notifications, GitHub change tracking, and Terraform drift
5. **IDE install surfaces** — VS Code extension and JetBrains plugin

---

## Quick start

### Prerequisites

- Python **3.11+**
- Node.js **18+** (for VS Code extension build; optional)
- JDK **17+** (for JetBrains plugin build; optional)
- `spacy` model `en_core_web_sm` (installed automatically via `requirements.txt`)

### Bootstrap (recommended)

**macOS / Linux:**

```bash
git clone https://github.com/vaquarkhan/compliance-agent-skills.git
# or: git clone git@github.com:vaquarkhan/compliance-agent-skills.git
cd compliance-agent-skills
chmod +x bootstrap.sh
./bootstrap.sh
```

**Windows (PowerShell):**

```powershell
git clone https://github.com/vaquarkhan/compliance-agent-skills.git
cd compliance-agent-skills
.\bootstrap.ps1
```

The installer detects your IDE (Cursor, VS Code, Claude Code, JetBrains) and copies skills, presets, rules, hooks, and MCP templates to the appropriate config directories.

### Run the agent locally

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt

export OPENAI_API_KEY=sk-...   # or ANTHROPIC_API_KEY
python agent.py "Scope a HIPAA PHI redaction review for our LLM intake pipeline"
```

Without API keys, the agent falls back to Pydantic AI `TestModel` for local development.

**Deanonymization is opt-in.** By default, agent output keeps redacted tokens (`<PERSON_1>`). To restore original PHI for an authorized downstream channel only:

```python
from agent import run_compliance_agent_sync

# Default — redacted output (safe)
run_compliance_agent_sync("Review Jane Doe SSN 123-45-6789")

# Authorized restore — explicit opt-in
run_compliance_agent_sync("Review Jane Doe SSN 123-45-6789", deanonymize_output=True)
# or: COMPLIANCE_AGENT_DEANONYMIZE=1 python agent.py "..."
```

Run the no-API-key demo: `python scripts/demo_agent.py` or `make demo`.

### Validate the repository

```bash
make validate   # or run scripts individually
make test       # requires: pip install -r requirements.txt -r requirements-dev.txt
```

---

## Plugin installation

### Cursor

Run `./bootstrap.sh --target cursor` or follow [docs/cursor-setup.md](docs/cursor-setup.md). Installs:

- `.cursor/rules/` — compliance core, deterministic audit, PHI redaction, framework routing
- Skills symlink/copy to project or global skills directory
- MCP templates from `mcp/`
- Hooks from `hooks/`

### VS Code / GitHub Copilot

```bash
./bootstrap.sh --target vscode
```

Or install the bundled extension:

```bash
cd vscode-extension && npm install && npx vsce package
code --install-extension compliance-agent-skills-*.vsix
```

See [docs/vscode-setup.md](docs/vscode-setup.md) and [.github/copilot-instructions.md](.github/copilot-instructions.md).

### Claude Code / Claude Desktop

```bash
./bootstrap.sh --target claude
```

Copies `.claude/commands/` lifecycle commands and `CLAUDE.md`. See [docs/claude-setup.md](docs/claude-setup.md).

### JetBrains (IntelliJ, PyCharm, etc.)

Build and install from `jetbrains-plugin/`:

```bash
cd jetbrains-plugin && ./gradlew buildPlugin
```

See [docs/jetbrains-setup.md](docs/jetbrains-setup.md).

---

## Audit lifecycle commands

| Command | Purpose | Skill / doc |
| --- | --- | --- |
| `/scope` | Define in-scope systems, data flows, frameworks, exclusions | `.claude/commands/scope.md`, `using-compliance-agent-skills` |
| `/audit` | Execute framework-specific control testing | Framework skills (HIPAA, PCI, SOC 2) |
| `/evidence` | Collect, hash, and package audit artifacts | `soc2-evidence-collection`, templates |
| `/remediate` | Draft remediation plans with owners and deadlines | Output of `/audit` |
| `/report` | Executive + technical findings summaries | `.claude/commands/report.md` |

Example engagement flow:

```
/scope  →  /audit (pci-dss-script-audit)  →  /evidence  →  /remediate  →  /report
```

---

## Skills catalog

24 skills organized by framework. Full catalog: [skills-index.md](skills-index.md).

| Group | Skills |
| --- | --- |
| **Meta** | `using-compliance-agent-skills` |
| **HIPAA** | `hipaa-technical-safeguards`, `hipaa-phi-redaction-pipeline`, `hipaa-baa-vendor-assessment`, `hipaa-privacy-minimum-necessary` |
| **PCI-DSS v4.0** | `pci-dss-script-audit`, `pci-dss-network-segmentation`, `pci-dss-encryption-key-management` |
| **SOC 2** | `soc2-trust-services-criteria`, `soc2-evidence-collection`, `soc2-ccm-continuous-monitoring` |
| **ISO 27001** | `iso27001-annex-a-controls` |
| **NIST CSF 2.0** | `nist-csf-2-assessment` |
| **CCPA / CPRA** | `ccpa-cpra-privacy-rights` |
| **FedRAMP** | `fedramp-moderate-baseline` |
| **SOX** | `sox-itgc-audit` |
| **CMMC** | `cmmc-nist-800-171` |
| **GLBA / FFIEC** | `glba-ffiec-financial-privacy` |
| **Cross-cutting** | `access-control-identity-audit`, `audit-logging-integrity`, `breach-incident-response`, `vendor-third-party-risk`, `compliance-as-code-governance`, `mcp-compliance-integration` |

Load skills progressively — only pull in what matches the task. See [AGENTS.md](AGENTS.md) for routing.

---

## Frameworks

### HIPAA

Security Rule (45 CFR §164.312), Breach Notification (§164.400–414), BAA review (§164.502(e)). Skills cover technical safeguards, Presidio redaction pipelines, and vendor BAAs.

**Preset:** [presets/healthcare-hipaa/PRESET.md](presets/healthcare-hipaa/PRESET.md)  
**Starter pack:** [starter-packs/hipaa-healthcare-starter.yaml](starter-packs/hipaa-healthcare-starter.yaml)

### PCI-DSS

v4.0 Requirements 1–2 (network), 6.4.3 / 11.6.1 (payment-page scripts), 7–8 (access), 10 (logging).

**Preset:** [presets/fintech-pci-dss/PRESET.md](presets/fintech-pci-dss/PRESET.md)  
**Starter pack:** [starter-packs/pci-dss-ecommerce-starter.yaml](starter-packs/pci-dss-ecommerce-starter.yaml)

### SOC 2

AICPA Trust Services Criteria (2017 + 2022 revisions): Security, Availability, Confidentiality, Processing Integrity, Privacy.

**Preset:** [presets/saas-soc2-type2/PRESET.md](presets/saas-soc2-type2/PRESET.md)  
**Starter pack:** [starter-packs/soc2-saas-starter.yaml](starter-packs/soc2-saas-starter.yaml)

### ISO 27001

ISO/IEC 27001:2022 Annex A controls, Statement of Applicability, risk treatment.

**Related skill:** `iso27001-annex-a-controls`  
**Template:** [templates/iso27001-statement-of-applicability.yaml](templates/iso27001-statement-of-applicability.yaml)

### NIST CSF 2.0

Govern, Identify, Protect, Detect, Respond, Recover gap assessments and organizational profiles.

**Related skill:** `nist-csf-2-assessment`  
**Template:** [templates/nist-csf-profile.yaml](templates/nist-csf-profile.yaml)

### CCPA / CPRA

California consumer privacy rights, DSAR workflows, service provider contracts.

**Related skill:** `ccpa-cpra-privacy-rights`  
**Template:** [templates/dsar-request-log.yaml](templates/dsar-request-log.yaml)

### FedRAMP

FedRAMP Moderate baseline, NIST SP 800-53 Rev 5, SSP/POA&M/ConMon authorization packages.

**Related skill:** `fedramp-moderate-baseline`  
**Template:** [templates/fedramp-ssp-outline.yaml](templates/fedramp-ssp-outline.yaml)

### SOX

Sarbanes-Oxley IT general controls (SOX 404) — access, change, development, operations.

**Related skill:** `sox-itgc-audit`  
**Template:** [templates/sox-itgc-control-matrix.yaml](templates/sox-itgc-control-matrix.yaml)

### CMMC

CMMC 2.0 Level 2, CUI, NIST SP 800-171, SPRS scoring for defense supply chain.

**Related skill:** `cmmc-nist-800-171`  
**Template:** [templates/cmmc-poam.yaml](templates/cmmc-poam.yaml)

### GLBA / FFIEC

GLBA Safeguards and Privacy Rules, FFIEC IT handbook alignment for financial institutions.

**Related skill:** `glba-ffiec-financial-privacy`  
**Preset:** [presets/financial-services-glba/PRESET.md](presets/financial-services-glba/PRESET.md)  
**Starter pack:** [starter-packs/enterprise-regulated-starter.yaml](starter-packs/enterprise-regulated-starter.yaml)

---

## Project structure

```
compliance-agent-skills/
├── agent.py                 # Pydantic AI entry + SkillsCapability
├── redaction.py             # Presidio PHI redaction gate
├── requirements.txt
├── skills/                  # 24 Agent Skills (SKILL.md each)
├── presets/                 # Framework + cloud presets
├── starter-packs/           # Curated skill + template bundles
├── templates/               # YAML/MD audit artifacts
├── references/              # Checklists and pattern guides
├── registry/assets.json     # Machine-readable asset index
├── mcp/                     # MCP server templates
├── hooks/                   # Session hooks (PHI guard, audit mode)
├── docs/                    # Setup and authoring guides
├── .cursor/rules/           # Cursor agent rules
├── .claude/commands/        # Lifecycle slash commands
├── agents/                  # Persona prompts (architect, QSA, etc.)
├── examples/                # Runnable audit examples
├── scripts/                 # install + validation
├── vscode-extension/
└── jetbrains-plugin/
```

---

## MCP integrations

Pre-configured templates in `mcp/` for compliance audit workflows:

| Server | Use case |
| --- | --- |
| Playwright | Payment-page script inventory, DOM tamper detection |
| Postgres | Evidence queries, access review exports |
| Presidio | Custom DLP / PHI detection MCP bridge |
| Slack | Incident and audit notifications |
| GitHub | Change management evidence (CC8.1) |
| Terraform | IaC drift and compliance-as-code scans |

See [mcp/README.md](mcp/README.md) and skill `mcp-compliance-integration`.

---

## Examples

| Example | Description |
| --- | --- |
| [examples/pci-checkout-audit/](examples/pci-checkout-audit/) | PCI Req 6.4.3 script baseline audit |
| [examples/hipaa-phi-redaction/](examples/hipaa-phi-redaction/) | Presidio redaction on sample PHI |
| [examples/soc2-evidence-bundle/](examples/soc2-evidence-bundle/) | Evidence manifest packaging |

---

## Documentation

| Doc | Topic |
| --- | --- |
| [docs/getting-started.md](docs/getting-started.md) | First engagement walkthrough |
| [docs/skill-anatomy.md](docs/skill-anatomy.md) | Authoring skills |
| [docs/plugin-publishing.md](docs/plugin-publishing.md) | VS Code / JetBrains releases |
| [AGENTS.md](AGENTS.md) | Agent entry + skill routing |
| [CLAUDE.md](CLAUDE.md) | Claude-specific entry |

---

## License

MIT — see [LICENSE](LICENSE).

---

## Acknowledgments

Built on [Pydantic AI](https://ai.pydantic.dev/), [Microsoft Presidio](https://microsoft.github.io/presidio/), and the Agent Skills progressive-disclosure pattern.
