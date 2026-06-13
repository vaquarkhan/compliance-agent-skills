# GDPR Article Checklist (US Multinational)

Operational checklist for EU/EEA/UK GDPR programs. Not legal advice. UK GDPR parallels noted where aligned.

## Scope (Art. 3)

- [ ] EU/EEA data subjects identified in product/agent flows
- [ ] Controller / processor / joint controller roles documented
- [ ] Lead supervisory authority identified (Art. 56) or EU representative (Art. 27) if required

## Principles (Art. 5)

- [ ] Lawfulness, fairness, transparency
- [ ] Purpose limitation for agent features
- [ ] Data minimization (`redaction.py` before LLM transfer)
- [ ] Accuracy and storage limitation (retention schedule for prompts/logs)
- [ ] Integrity and confidentiality (Art. 32)
- [ ] Accountability documentation

## Lawful basis (Art. 6 / Art. 9)

- [ ] Art. 6 basis per processing activity (contract, consent, LIA, legal obligation)
- [ ] Art. 9 explicit consent or exception if special category in prompts
- [ ] Legitimate interest assessment (LIA) documented where used

## Records of processing (Art. 30)

- [ ] RoPA maintained (`templates/gdpr-ropa-template.yaml`)
- [ ] LLM/MCP subprocessors listed with transfer safeguards
- [ ] Retention and security measures referenced

## International transfers (Chapter V)

- [ ] Transfer inventory to US (LLM APIs, MCP hosts)
- [ ] DPF certification verified OR 2021 SCCs executed
- [ ] UK IDTA/Addendum if UK data
- [ ] Transfer impact assessment (Schrems II supplementary measures)

## Data subject rights (Arts. 15-22)

- [ ] Access, erasure, portability workflows (one-month SLA)
- [ ] Object/restrict processing for profiling agents
- [ ] LLM vendor deletion SLAs in DPA

## Security (Art. 32)

- [ ] Pseudonymization/redaction gate active
- [ ] MCP OAuth least privilege
- [ ] Deanonymization opt-in only (`agent.py`)

## DPIA (Art. 35)

- [ ] High-risk agent processing identified (profiling, special categories)
- [ ] DPIA completed; DPO consulted
- [ ] Supervisory authority consultation if residual high risk (Art. 36)

## Breach (Arts. 33-34)

- [ ] 72-hour supervisory authority notification playbook
- [ ] Data subject notification criteria (high risk)
- [ ] Processor (LLM) breach notification clause in DPA

## Processor DPA (Art. 28)

- [ ] Written instructions, subprocessor list, audit rights
- [ ] Deletion/return at termination
- [ ] Assistance with DSAR and DPIA

## DPO (Arts. 37-39)

- [ ] DPO appointed if required (large-scale Art. 9 or systematic monitoring)
- [ ] DPO contact published; consulted on DPIA

---

## Authoritative sources

- GDPR (Regulation EU 2016/679): [EUR-Lex GDPR text](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679)
- EDPB guidelines: [European Data Protection Board](https://www.edpb.europa.eu/)

## Provenance

| Field | Value |
|-------|-------|
| **Source document** | GDPR (EU) 2016/679 |
| **Version / effective** | GDPR in force; EDPB guidance as of 2026-06-13 |
| **Last reviewed** | 2026-06-13 |
| **Reviewer** | Repository maintainer (pending DPO sign-off) |
| **Next review due** | 2026-12-13 |
| **Notes** | US multinational subset; not EU representative opinion |
