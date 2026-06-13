---
name: financial-services-glba
description: Preset for banks, credit unions, and fintech organizations subject to GLBA Safeguards Rule, Privacy Rule, and FFIEC IT examination guidance. Apply when auditing customer financial information protection, vendor oversight, or AI systems in consumer banking workflows.
---

# Financial Services GLBA Preset

## Overview

Aligns compliance-agent-skills workflows with **Gramm-Leach-Bliley Act** (Safeguards Rule 16 CFR Part 314, Privacy Rule Part 313) and **FFIEC** IT examination handbook expectations for institutions supervised by OCC, FDIC, Federal Reserve, or NCUA.

## Use When

- Organization is a **financial institution** or **service provider** to one
- Customer **nonpublic personal information (NPI)** is processed by agents or MCP tools
- Preparing for **FFIEC IT** or **state banking** examinations
- Evaluating **fintech** partnerships and data sharing

## Preferred Skills

1. `glba-ffiec-financial-privacy` (primary)
2. `vendor-third-party-risk`
3. `access-control-identity-audit`
4. `audit-logging-integrity`
5. `ccpa-cpra-privacy-rights` (California customers)

## Design Rules

- Treat all customer NPI as in-scope unless formally de-identified per GLBA
- No customer account data in LLM prompts without encryption and vendor GLBA compliance
- Maintain **Qualified Individual** accountability for information security program
- Annual **risk assessment** and program evaluation are mandatory artifacts

## Verification

- [ ] Primary skill `glba-ffiec-financial-privacy` loaded
- [ ] Privacy and Safeguards Rule obligations mapped
- [ ] Service provider contracts reviewed for GLBA compliance
- [ ] FFIEC-aligned control evidence indexed
