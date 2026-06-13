# Coverage & Roadmap

What **compliance-agent-skills** covers today (30 skills) and notable **USA gaps** planned for future phases.

> Operational patterns only — not legal advice.

---

## Covered today (by domain)

| Domain | Skills / assets | Depth |
| --- | --- | --- |
| **Healthcare** | HIPAA Security/Privacy, BAA, redaction, minimum necessary, HITECH breach | Strong for agent/MCP technical + breach |
| **Payments** | PCI-DSS v4 scripts, segmentation, encryption/keys | Focused on Req 1–2, 3–4, 6.4.3, 10 — not full QSA 12-req program |
| **SaaS / audit** | SOC 2 TSC, evidence, CCM | Type I/II readiness |
| **Security frameworks** | ISO 27001 Annex A, NIST CSF 2.0 | Gap assessment + templates |
| **Privacy — California** | CCPA/CPRA | DSAR, opt-out, service providers |
| **Privacy — US states** | `us-state-privacy-laws` | VCDPA, CPA, TDPSA, CT, OR, MT, IA, DE, NJ + matrix |
| **Privacy — EU (US cos.)** | `gdpr-us-multinational` | RoPA, SCCs/DPF, 72h breach |
| **Federal cloud** | FedRAMP Moderate | SSP, POA&M, ConMon |
| **Financial** | GLBA/FFIEC, SOX ITGC | Safeguards + ITGC |
| **Defense** | CMMC L2 / 800-171 | CUI, SPRS |
| **Cross-cutting** | IAM, logging, breach IR, vendor risk, policy-as-code, MCP | Shared controls |

---

## USA compliance gaps (not yet dedicated skills)

| EdTech & youth (FERPA, COPPA, AI RMF) | `nist-ai-rmf-governance`, `ferpa-education-records`, `coppa-children-privacy` | Strong |

---

## USA compliance gaps (not yet dedicated skills)

### High priority (Phase 6 candidates)

| Framework | Why it matters for AI agents |
| --- | --- |
| **NY DFS 23 NYCRR 500** | NY financial services cybersecurity — common for fintech |
| **FISMA / RMF** | Federal agency systems (distinct from FedRAMP CSP path) |
| **State breach notification playbooks** | Per-state timelines (partially in `breach-incident-response`) |

### Medium priority

| Framework | Notes |
| --- | --- |
| **FDA 21 CFR Part 11** | Electronic records/signatures in pharma/med device AI |
| **NERC CIP** | Energy sector critical infrastructure |
| **CJIS Security Policy** | Law enforcement / criminal justice data |
| **IRS Pub. 1075 / FTI** | Tax return information handling |
| **BSA/AML / FinCEN** | Fintech KYC/transaction monitoring (often overlaps GLBA) |
| **PCI-DSS full program** | All 12 requirements + ROC readiness (expand existing PCI skills) |
| **HITECH Information Blocking** | 21st Century Cures / ONC interoperability rules |
| **Section 508 / WCAG** | Federal/state accessibility for agent UIs |

### Completed in Phase 5 ✓

- ~~NIST AI RMF~~ → `nist-ai-rmf-governance`
- ~~FERPA~~ → `ferpa-education-records`
- ~~COPPA~~ → `coppa-children-privacy`

### Medium priority

| Framework | Notes |
| --- | --- |
| **FDA 21 CFR Part 11** | Electronic records/signatures in pharma/med device AI |
| **NERC CIP** | Energy sector critical infrastructure |
| **CJIS Security Policy** | Law enforcement / criminal justice data |
| **IRS Pub. 1075 / FTI** | Tax return information handling |
| **BSA/AML / FinCEN** | Fintech KYC/transaction monitoring (often overlaps GLBA) |
| **PCI-DSS full program** | All 12 requirements + ROC readiness (expand existing PCI skills) |
| **HITECH Information Blocking** | 21st Century Cures / ONC interoperability rules |
| **Section 508 / WCAG** | Federal/state accessibility for agent UIs |

### Lower priority / niche

| Framework | Notes |
| --- | --- |
| **FCRA / FACTA** | Credit reporting — fair lending AI |
| **ECOA / Reg B** | Fair lending model governance |
| **CAN-SPAM / TCPA** | Marketing agents, SMS/voice |
| **ITAR / EAR** | Export-controlled technical data (defense overlap with CMMC) |
| **OSHA** | Workplace safety — rarely agent-audit scope |
| **State insurance (NAIC)** | InsurTech — overlaps GLBA/state privacy |

### Explicitly out of scope

- **EU-only** frameworks without US nexus (covered partially via `gdpr-us-multinational`)
- **Industry QSA sign-off** or licensed attestation (skills are readiness, not certification)
- **Non-US national laws** (LGPD, PIPEDA, etc.) unless added in a future international phase

---

## Partial coverage (use existing skills)

| Need | Use today |
| --- | --- |
| General breach + state mentions | `breach-incident-response` → `hitech-breach-notification` for PHI depth |
| California + other states | `ccpa-cpra-privacy-rights` + `us-state-privacy-laws` |
| HIPAA admin/physical safeguards | `hipaa-technical-safeguards` (technical focus); admin/physical policies are customer-owned |
| FFIEC deep examination | `glba-ffiec-financial-privacy` (program-level, not full IT handbook) |
| NIST 800-53 controls | `fedramp-moderate-baseline` (FedRAMP baseline) or `cmmc-nist-800-171` (800-171) |

---

## Suggest Phase 6?

If you want the next build, recommended order:

1. **NY DFS 500** — fintech gap alongside GLBA  
2. **FISMA / RMF** — federal agency path  
3. **State breach playbook skill** — deepens `breach-incident-response`  

Open an issue or PR with `phase-6` label to prioritize.
