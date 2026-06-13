---
title: Multinational Privacy Preset
version: "1.0.0"
frameworks:
  - HITECH
  - US-State-Privacy
  - GDPR
  - CCPA-CPRA
skills:
  - using-compliance-agent-skills
  - hitech-breach-notification
  - us-state-privacy-laws
  - gdpr-us-multinational
  - ccpa-cpra-privacy-rights
  - breach-incident-response
  - hipaa-phi-redaction-pipeline
  - vendor-third-party-risk
templates:
  - templates/hitech-breach-workbook.yaml
  - templates/state-privacy-assessment.yaml
  - templates/gdpr-ropa-template.yaml
  - templates/dsar-request-log.yaml
references:
  - references/hitech-breach-checklist.md
  - references/us-state-privacy-matrix.md
  - references/gdpr-article-checklist.md
  - references/ccpa-cpra-checklist.md
mcp:
  - mcp/postgres.mcp.json
  - mcp/presidio.mcp.json
hooks:
  - hooks/phi-redaction-guard.sh
rules:
  - .cursor/rules/20-phi-redaction-first.mdc
  - .cursor/rules/30-framework-routing.mdc
---

# Multinational Privacy Preset

Use for **US companies with national and international privacy obligations**: HITECH breach depth, multi-state US laws (VCDPA, CPA, TDPSA, etc.), California CPRA, and GDPR for EU/EEA data subjects.

## When to apply

- SaaS with US nationwide users **and** EU customers
- Healthcare-adjacent products needing **HITECH** breach workflows beyond general incident response
- Agent/LLM platforms processing prompts with PI across jurisdictions
- Privacy team building **unified DSAR + breach + transfer** program

## Mandatory controls

1. **PHI/PI redaction** before any LLM call (`redaction.py`, balanced profile default)
2. **Deanonymization opt-in only** for authorized exports (`agent.py`)
3. **RoPA + state matrix** maintained quarterly
4. **72-hour GDPR** and **60-day HITECH** breach clocks in separate runbooks

## Lifecycle

```
/scope → us-state-privacy-laws OR gdpr-us-multinational
/audit → framework skill Core Process
/evidence → templates + SHA-256 manifest
/breach → breach-incident-response → hitech-breach-notification (if PHI)
```

## Disclaimers

Operational templates only—not legal advice. Engage privacy counsel for binding interpretations and regulatory filings.
