# US State Comprehensive Privacy Laws Matrix

Quick reference for multi-state programs. Verify current statutes—laws amend frequently.

| State | Law | Key citation | Threshold (summary) | Sensitive data consent | Profiling/DPA | Universal opt-out |
| --- | --- | --- | --- | --- | --- | --- |
| California | CPRA/CCPA | Cal. Civ. Code §1798 | See `ccpa-cpra-checklist.md` | Yes (SPI) | CPPA regs | GPC |
| Virginia | VCDPA | Va. Code §59.1-575 | 100k or 25k + 50% sale revenue | Yes | Required (targeted ads, sale, profiling, sensitive) | Yes |
| Colorado | CPA | C.R.S. §6-1-1301 | 100k or 25k + sale revenue | Yes | Required (high-risk) | GPC |
| Connecticut | CTDPA | CGS §42-515 | 100k or 25k + 25% sale revenue | Yes | Required | GPC |
| Utah | UCPA | Utah Code §13-61 | 100k or 25k + 50% sale revenue | Opt-in sensitive only | No general DPA | No |
| Texas | TDPSA | Bus. & Com. Code Ch. 509 | Broad (SBO rules) | Yes | Required (high-risk) | Yes |
| Oregon | OCPA | ORS §646A.570 | 100k or 25k + 25% sale revenue | Yes | Required | GPC |
| Montana | MCDPA | MCA §30-14-2801 | 50k consumers | Yes | Required | GPC |
| Iowa | ICDPA | Iowa Code §715D | 100k consumers | Opt-in sensitive | Limited | No |
| Delaware | DPDPA | Del. Code tit. 6 §1200 | 35k or 10k + 20% sale | Yes | Required | GPC |
| New Jersey | NJDPA | N.J.S.A. 56:8-166 | 100k or 25k + sale revenue | Yes | Required | GPC |

## Harmonized consumer rights

Most comprehensive states provide:

- **Right to know/access** — categories and specific pieces
- **Right to delete** — with statutory exceptions
- **Right to correct** — accuracy (all except Utah historically)
- **Right to portability** — where applicable
- **Opt-out of sale** — and **share** (CPRA/VCDPA/CPA terminology varies)
- **Opt-out of targeted advertising**
- **Opt-out of profiling** in furtherance of significant decisions (CO, CT, VA, etc.)
- **Non-discrimination** for exercising rights

## Common exemptions (verify per state)

- HIPAA-covered PHI (entity level)
- GLBA-covered data (entity level)
- FERPA student data
- Employee data (B2B HR—varies; TX treats employee differently)
- De-identified data per state definition
- Publicly available information (limited)

## Agent / LLM considerations

| Risk | Mitigation skill |
| --- | --- |
| Prompts contain PI | `hipaa-phi-redaction-pipeline`, DSAR via Postgres MCP |
| Cross-state DSAR | `templates/dsar-request-log.yaml` + state residency field |
| Profiling via agent | DPIA per state; `gdpr-us-multinational` if EU also |
| LLM subprocessors | `vendor-third-party-risk`, processor contracts |
| Opt-out signals | Honor GPC; disable ad SDKs in agent telemetry |

## Breach notification overlap

State breach laws may apply **in addition to** HIPAA HITECH—use `hitech-breach-notification` and `breach-incident-response` together. Timelines may be **shorter than 60 days** (e.g., 30 days in some states).
