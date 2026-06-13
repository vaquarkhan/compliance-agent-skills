# NIST AI RMF 1.0 Checklist

Based on NIST AI 100-1 (GOVERN, MAP, MEASURE, MANAGE). Not legal advice.

## GOVERN

- [ ] AI system inventory (agents, models, MCP tools)
- [ ] Executive sponsor and AI risk owner assigned
- [ ] Acceptable use policy for LLM prompts and tools
- [ ] Human oversight defined for high-risk use cases
- [ ] Change management for model/skill/MCP updates

## MAP

- [ ] Use case documented: purpose, context, actors
- [ ] Data types classified (ePHI, PI, CHD, CUI, public)
- [ ] Benefits and potential harms identified
- [ ] Risk tier assigned (low / moderate / high)
- [ ] Trustworthiness gaps mapped (validity, safety, privacy, bias, transparency)
- [ ] Failure modes: hallucination, prompt injection, tool abuse, deanonymize leak

## MEASURE

- [ ] Metrics defined with targets (redaction FN, routing accuracy, tool violations)
- [ ] TEVV plan: pre-deploy tests + production monitoring
- [ ] Synthetic/adversarial test corpus (no production PHI in CI)
- [ ] System/model card for agent stack
- [ ] User disclosure of AI assistance where appropriate

## MANAGE

- [ ] Risk treatment plan with technical/process/human controls
- [ ] Residual risk acceptance sign-off for high-tier deployments
- [ ] CCM integration for drift and anomalies
- [ ] AI incident playbook linked to breach-incident-response
- [ ] Current vs Target profile and 12-month roadmap

## Repo integration

- [ ] `redaction.py` balanced profile active; deanonymize opt-in only
- [ ] `agent.py` skills routing enforced (no invented regulations)
- [ ] MCP OAuth and audit mode hooks configured
- [ ] `compliance_tests/` corpus run in CI

---

## Authoritative sources

- NIST AI RMF 1.0: [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework)
- NIST AI 100-1 publication: [NIST CSRC AI 100-1](https://csrc.nist.gov/pubs/ai/100/1/final)

## Provenance

| Field | Value |
|-------|-------|
| **Source document** | NIST AI RMF 1.0 (NIST AI 100-1) |
| **Version / effective** | July 2024 |
| **Last reviewed** | 2026-06-13 |
| **Reviewer** | Repository maintainer (pending AI risk officer sign-off) |
| **Next review due** | 2026-12-13 |
| **Notes** | Agent/MCP mapping; not a NIST conformity assessment |
