---
title: EdTech & Youth Privacy Preset
version: "1.0.0"
frameworks:
  - NIST-AI-RMF
  - FERPA
  - COPPA
skills:
  - using-compliance-agent-skills
  - nist-ai-rmf-governance
  - ferpa-education-records
  - coppa-children-privacy
  - hipaa-phi-redaction-pipeline
  - us-state-privacy-laws
  - mcp-compliance-integration
templates:
  - templates/nist-ai-rmf-profile.yaml
  - templates/ferpa-school-official.yaml
  - templates/coppa-parental-consent.yaml
references:
  - references/nist-ai-rmf-checklist.md
  - references/ferpa-checklist.md
  - references/coppa-checklist.md
mcp:
  - mcp/postgres.mcp.json
  - mcp/presidio.mcp.json
hooks:
  - hooks/phi-redaction-guard.sh
rules:
  - .cursor/rules/20-phi-redaction-first.mdc
  - .cursor/rules/30-framework-routing.mdc
---

# EdTech & Youth Privacy Preset

For **K-12, higher-ed EdTech, and child-directed AI agents** — NIST AI RMF governance plus FERPA and COPPA.

## When to apply

- District or EdTech vendor deploying **AI tutoring, grading, or support agents**
- **Consumer apps** with users under 13 or child-directed UX
- **AI governance** reviews for youth-facing LLM features

## Mandatory controls

1. **NIST AI RMF** MAP/MEASURE before production agent features
2. **FERPA** school official DPA + LEI for institutional deployments
3. **COPPA** VPC and service provider agreements for under-13 consumer paths
4. **Redaction + no auto-deanonymize** on youth production paths

## Routing

| Context | Primary skill |
| --- | --- |
| School/LMS integration | `ferpa-education-records` |
| Child-directed consumer app | `coppa-children-privacy` |
| AI governance / TEVV | `nist-ai-rmf-governance` |

## Disclaimers

Not legal advice. LEA privacy officers and FTC COPPA counsel should review binding obligations.
