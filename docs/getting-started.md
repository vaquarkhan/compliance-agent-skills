# Getting Started

Your first compliance engagement with **compliance-agent-skills**.

## 1. Install

```bash
./bootstrap.sh          # macOS/Linux
# or
.\bootstrap.ps1         # Windows
```

This installs Python dependencies, detects your IDE, and validates the asset registry.

## 2. Choose a starter pack

| Industry | Starter pack |
| --- | --- |
| Healthcare | `starter-packs/hipaa-healthcare-starter.yaml` |
| E-commerce / payments | `starter-packs/pci-dss-ecommerce-starter.yaml` |
| SaaS | `starter-packs/soc2-saas-starter.yaml` |
| AI agents (multi-framework) | `starter-packs/regulated-ai-agents-starter.yaml` |
| Enterprise regulated (FedRAMP, SOX, CMMC, GLBA) | `starter-packs/enterprise-regulated-starter.yaml` |
| Multinational privacy (HITECH, state, GDPR) | `starter-packs/multinational-privacy-starter.yaml` |
| EdTech & youth (FERPA, COPPA, AI RMF) | `starter-packs/edtech-youth-privacy-starter.yaml` |

Apply the matching **preset** from `presets/*/PRESET.md`.

## 3. Run lifecycle commands

In Cursor or Claude Code:

1. **`/scope`** — define systems, data classes, frameworks
2. **`/audit`** — load framework skill and test controls
3. **`/evidence`** — collect artifacts with SHA-256 hashes
4. **`/remediate`** — assign owners to gaps
5. **`/report`** — executive + technical summary

## 4. Run the Python agent

```bash
pip install -r requirements.txt
export OPENAI_API_KEY=sk-...
python agent.py "Scope HIPAA controls for our LLM intake pipeline"
```

PHI is redacted via Presidio before the model sees your prompt.

## 5. Try an example

```bash
cd examples/hipaa-phi-redaction
python run_redaction.py
```

## 6. Validate

```bash
python scripts/validate-skills.py
python scripts/validate-assets.py
```

## Next steps

- [cursor-setup.md](cursor-setup.md) — Cursor IDE configuration
- [skill-anatomy.md](skill-anatomy.md) — authoring new skills
- [skills-index.md](../skills-index.md) — full skill catalog
