# Project status — compliance-agent-skills v1.6.2+

Current capabilities, engineering posture, and **honest limits** of what this repository can claim.

> **Not legal advice.** Operational patterns and automation only.

---

## Release summary (v1.0 → v1.6.2)

| Version | Theme |
|---------|--------|
| **1.0–1.2** | Core skills (HIPAA, PCI, SOC 2, ISO, NIST CSF, CCPA, FedRAMP, SOX, CMMC, GLBA); VS Code / JetBrains plugins |
| **1.3** | Security: opt-in deanonymize; test suite; custom SSN recognizer; balanced redaction profile |
| **1.4** | HITECH breach, US state privacy, GDPR multinational |
| **1.5** | NIST AI RMF, FERPA, COPPA (EdTech / youth privacy) |
| **1.6.0** | CI hardening (Ruff, mypy, pip-audit, Bandit, detect-secrets, CodeQL); locked deps; coverage gate; Dependabot; pre-commit; architecture docs |
| **1.6.1** | **Redaction fix:** Presidio PII probe phantom tokens; regression tests |
| **1.6.2** | Regulatory report generator; SME provenance on all 15 checklists; CI `validate-sme-provenance`; review records scaffold |

**Current version:** see [VERSION](../VERSION) (latest tag on [GitHub Releases](https://github.com/vaquarkhan/compliance-agent-skills/releases)).

---

## What ships today

### Agent core

| Component | Purpose |
|-----------|---------|
| `agent.py` | Pydantic AI + SkillsCapability; mandatory redaction upstream |
| `redaction.py` | Presidio PHI gate; reversible tokens; opt-in deanonymize |
| 30 skills | Progressive-disclosure regulatory workflows |
| Audit lifecycle | `/scope` → `/audit` → `/evidence` → `/remediate` → `/report` |

### Framework coverage (30 skills)

Healthcare (HIPAA, HITECH), payments (PCI-DSS v4), audit (SOC 2, ISO 27001), security frameworks (NIST CSF 2.0, NIST AI RMF), privacy (CCPA/CPRA, US state, GDPR), federal/defense (FedRAMP, CMMC), financial (GLBA/FFIEC, SOX ITGC), EdTech (FERPA, COPPA), and cross-cutting (IAM, logging, breach IR, vendor risk, MCP, policy-as-code).

Full catalog: [skills-index.md](../skills-index.md). Gaps: [coverage-roadmap.md](coverage-roadmap.md).

### Templates and references

- **20+ YAML/MD templates** — evidence manifests, control matrices, framework scaffolds
- **15 regulatory checklists** — each with **Authoritative sources** + **Provenance** footer
- **Regulatory reports** — [regulatory-reports.md](regulatory-reports.md); five synthetic examples

### Examples (runnable)

| Example | Framework |
|---------|-----------|
| `examples/hipaa-phi-redaction/` | HIPAA / Presidio |
| `examples/pci-checkout-audit/` | PCI-DSS 6.4.3 |
| `examples/soc2-evidence-bundle/` | SOC 2 evidence |
| `examples/ferpa-education-records/` | FERPA |
| `examples/coppa-parental-consent/` | COPPA |
| `examples/nist-ai-rmf-profile/` | NIST AI RMF |
| `examples/regulatory-reports/*/` | Generated findings reports |

### IDE and distribution

- VS Code extension (`.vsix` on GitHub Releases)
- JetBrains plugin (Gradle wrapper; ZIP on releases)
- Bootstrap for Cursor, Claude Code, VS Code, JetBrains
- [plugin-publishing.md](plugin-publishing.md) for Marketplace manual publish

### Engineering and CI

| Gate | Tool / script |
|------|----------------|
| Validate | `validate-skills`, `validate-assets`, `validate-plugin-manifest`, `validate-evidence-manifest`, `validate-sme-provenance` |
| Lint | Ruff check + format |
| Types | mypy on `agent.py`, `redaction.py`, `scripts/` |
| Security | pip-audit, Bandit, detect-secrets baseline, CodeQL |
| Tests | pytest + ≥80% coverage on `agent.py` + `redaction.py` |
| Dependencies | `requirements-lock.txt` (pip-tools); Dependabot |
| Pre-commit | Ruff, detect-secrets, validators |

```bash
make validate    # includes validate-sme
make test
make lint
make security
make report INPUT=... OUTPUT=...
```

### Documentation map

| Doc | Topic |
|-----|--------|
| [architecture.md](architecture.md) | Redaction gate, threat model, deanonymize auth |
| [redaction-limitations.md](redaction-limitations.md) | US/English-only; entity coverage limits |
| [sme-review.md](sme-review.md) | Provenance cadence; CI enforcement |
| [regulatory-reports.md](regulatory-reports.md) | Structured `/report` outputs |
| [coverage-roadmap.md](coverage-roadmap.md) | USA gaps; Phase 6 candidates |
| [plugin-publishing.md](plugin-publishing.md) | VSIX / JetBrains Marketplace |
| [getting-started.md](getting-started.md) | First engagement |

---

## SME review program

Reference checklists include **provenance footers**, **authoritative source links**, and a documented **review cadence**. CI enforces completeness via `validate-sme-provenance`.

1. **Provenance footers** on all 15 reference checklists (source doc, version, last reviewed, next review due, reviewer)
2. **Authoritative source links** (eCFR, PCI SSC, NIST CSRC, AICPA, FTC, etc.)
3. **Review cadence** per framework (quarterly / semi-annual / annual) — [sme-review.md](sme-review.md)
4. **CI enforcement** — `scripts/validate-sme-provenance.py`
5. **Review records** under `reviews/YYYY-Qn/` — [reviews/TEMPLATE.md](../reviews/TEMPLATE.md)
6. **Issue template** — `.github/ISSUE_TEMPLATE/sme_review.yml`
7. **Skills** cite references at runtime to reduce hallucination

### Completing a review

1. Compare checklist items to the authoritative source (per `reviews/TEMPLATE.md`)
2. Update provenance **Last reviewed** and **Next review due**
3. Record sign-off in `reviews/YYYY-Qn/<framework>.md`
4. Run `make validate-sme` and open a PR with the `sme-review` label

---

## Known limits (unchanged by v1.6.x)

| Limit | Detail |
|-------|--------|
| Redaction | US English–oriented Presidio; see [redaction-limitations.md](redaction-limitations.md) |
| Skills | Agent-relevant subsets; not full ROC / HIPAA risk analysis / SOC 2 Type II report |
| Test collection | `test_agent.py` skips when `pydantic_ai` not installed (graceful degradation) |
| SME content | Provenance + review cadence enforced in CI; see [sme-review.md](sme-review.md) |

---

## Phase 6 candidates (not shipped)

NY DFS 23 NYCRR 500, FISMA/RMF, expanded state breach playbooks — see [coverage-roadmap.md](coverage-roadmap.md).

---

## Citation

If referencing this project academically, see [CITATION.cff](../CITATION.cff).
