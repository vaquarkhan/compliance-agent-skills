# Skills Index

Machine-readable registry: [registry/assets.json](registry/assets.json).  
Validation: `python scripts/validate-skills.py`

---

## Meta / orchestration

| Skill | Path | Summary |
| --- | --- | --- |
| **using-compliance-agent-skills** | [skills/using-compliance-agent-skills/](skills/using-compliance-agent-skills/) | Routes tasks to framework skills; configures presets, MCP, and audit lifecycle (`/scope` … `/report`). |

---

## HIPAA

| Skill | Path | Summary |
| --- | --- | --- |
| **hipaa-technical-safeguards** | [skills/hipaa-technical-safeguards/](skills/hipaa-technical-safeguards/) | §164.312 access, audit, integrity, authentication, transmission for agents/MCP. |
| **hipaa-phi-redaction-pipeline** | [skills/hipaa-phi-redaction-pipeline/](skills/hipaa-phi-redaction-pipeline/) | Presidio pipeline, entity tuning, redaction.py integration. |
| **hipaa-baa-vendor-assessment** | [skills/hipaa-baa-vendor-assessment/](skills/hipaa-baa-vendor-assessment/) | BAA and subprocessor review for LLM/cloud/MCP vendors. |
| **hipaa-privacy-minimum-necessary** | [skills/hipaa-privacy-minimum-necessary/](skills/hipaa-privacy-minimum-necessary/) | Privacy Rule §164.502(b) minimum necessary, de-id, patient rights. |

**Related:** preset `healthcare-hipaa`, starter `hipaa-healthcare-starter.yaml`, template `hipaa-phi-flow-diagram.yaml`

---

## PCI-DSS v4.0

| Skill | Path | Summary |
| --- | --- | --- |
| **pci-dss-script-audit** | [skills/pci-dss-script-audit/](skills/pci-dss-script-audit/) | Req 6.4.3 script inventory/integrity; Req 11.6.1 tamper detection. |
| **pci-dss-network-segmentation** | [skills/pci-dss-network-segmentation/](skills/pci-dss-network-segmentation/) | Req 1.x–2.x CDE isolation, scope reduction. |
| **pci-dss-encryption-key-management** | [skills/pci-dss-encryption-key-management/](skills/pci-dss-encryption-key-management/) | Req 3/4 PAN protection, encryption, key lifecycle, TLS. |

**Related:** preset `fintech-pci-dss`, starter `pci-dss-ecommerce-starter.yaml`, template `pci-script-baseline.yaml`

---

## SOC 2

| Skill | Path | Summary |
| --- | --- | --- |
| **soc2-trust-services-criteria** | [skills/soc2-trust-services-criteria/](skills/soc2-trust-services-criteria/) | TSC mapping, gap assessment, control design. |
| **soc2-evidence-collection** | [skills/soc2-evidence-collection/](skills/soc2-evidence-collection/) | Audit binders, hashes, Vanta/Drata-style packages. |
| **soc2-ccm-continuous-monitoring** | [skills/soc2-ccm-continuous-monitoring/](skills/soc2-ccm-continuous-monitoring/) | CCM, drift detection, alerting between audits. |

**Related:** preset `saas-soc2-type2`, starter `soc2-saas-starter.yaml`, template `soc2-control-evidence.yaml`

---

## ISO 27001

| Skill | Path | Summary |
| --- | --- | --- |
| **iso27001-annex-a-controls** | [skills/iso27001-annex-a-controls/](skills/iso27001-annex-a-controls/) | ISO/IEC 27001:2022 Annex A, SoA, risk treatment, control evidence. |

**Related:** references `iso27001-annex-a-checklist.md`, template `iso27001-statement-of-applicability.yaml`

---

## NIST CSF 2.0

| Skill | Path | Summary |
| --- | --- | --- |
| **nist-csf-2-assessment** | [skills/nist-csf-2-assessment/](skills/nist-csf-2-assessment/) | Govern/Identify/Protect/Detect/Respond/Recover gap assessment. |

**Related:** references `nist-csf-2-checklist.md`, template `nist-csf-profile.yaml`

---

## CCPA / CPRA (California)

| Skill | Path | Summary |
| --- | --- | --- |
| **ccpa-cpra-privacy-rights** | [skills/ccpa-cpra-privacy-rights/](skills/ccpa-cpra-privacy-rights/) | Consumer rights, DSAR, opt-out, service provider contracts. |

**Related:** references `ccpa-cpra-checklist.md`, template `dsar-request-log.yaml`

---

## FedRAMP

| Skill | Path | Summary |
| --- | --- | --- |
| **fedramp-moderate-baseline** | [skills/fedramp-moderate-baseline/](skills/fedramp-moderate-baseline/) | FedRAMP Moderate, NIST 800-53 Rev 5, SSP, POA&M, ConMon. |

**Related:** references `fedramp-moderate-checklist.md`, template `fedramp-ssp-outline.yaml`, starter `enterprise-regulated-starter.yaml`

---

## SOX

| Skill | Path | Summary |
| --- | --- | --- |
| **sox-itgc-audit** | [skills/sox-itgc-audit/](skills/sox-itgc-audit/) | SOX 404 ITGC — access, change, development, operations. |

**Related:** references `sox-itgc-checklist.md`, template `sox-itgc-control-matrix.yaml`

---

## CMMC / Defense

| Skill | Path | Summary |
| --- | --- | --- |
| **cmmc-nist-800-171** | [skills/cmmc-nist-800-171/](skills/cmmc-nist-800-171/) | CMMC 2.0 Level 2, CUI, NIST 800-171, SPRS. |

**Related:** references `cmmc-nist-800-171-checklist.md`, template `cmmc-poam.yaml`

---

## GLBA / Financial

| Skill | Path | Summary |
| --- | --- | --- |
| **glba-ffiec-financial-privacy** | [skills/glba-ffiec-financial-privacy/](skills/glba-ffiec-financial-privacy/) | GLBA Safeguards/Privacy, FFIEC IT handbook alignment. |

**Related:** references `glba-ffiec-checklist.md`, preset `financial-services-glba`, starter `enterprise-regulated-starter.yaml`

---

## Cross-cutting

| Skill | Path | Summary |
| --- | --- | --- |
| **access-control-identity-audit** | [skills/access-control-identity-audit/](skills/access-control-identity-audit/) | IAM, MFA, RBAC, JML — CC6, §164.312(a), PCI 7/8. |
| **audit-logging-integrity** | [skills/audit-logging-integrity/](skills/audit-logging-integrity/) | Tamper-evident logs, SIEM, retention — §164.312(b), CC7.2, PCI 10. |
| **breach-incident-response** | [skills/breach-incident-response/](skills/breach-incident-response/) | HIPAA breach notification, SOC 2 CC7.4/7.5, state laws. |
| **vendor-third-party-risk** | [skills/vendor-third-party-risk/](skills/vendor-third-party-risk/) | Vendor questionnaires, SOC report review, subprocessor risk. |
| **compliance-as-code-governance** | [skills/compliance-as-code-governance/](skills/compliance-as-code-governance/) | OPA/Rego, Terraform scanning, CI policy gates. |
| **mcp-compliance-integration** | [skills/mcp-compliance-integration/](skills/mcp-compliance-integration/) | MCP OAuth, scoped tools, transport security for audits. |

**Related:** starter `regulated-ai-agents-starter.yaml`, references `mcp-compliance-patterns.md`, `compliance-as-code-patterns.md`

---

## Routing quick reference

```
User intent unclear          → using-compliance-agent-skills
PHI / redaction              → hipaa-phi-redaction-pipeline
Payment page JavaScript      → pci-dss-script-audit
SOC 2 audit binder           → soc2-evidence-collection
MCP server deployment        → mcp-compliance-integration
PCI encryption / PAN           → pci-dss-encryption-key-management
ISO 27001 Annex A              → iso27001-annex-a-controls
NIST CSF 2.0                   → nist-csf-2-assessment
CCPA / CPRA / DSAR             → ccpa-cpra-privacy-rights
HIPAA minimum necessary        → hipaa-privacy-minimum-necessary
FedRAMP / cloud ATO            → fedramp-moderate-baseline
SOX ITGC / financial controls  → sox-itgc-audit
CMMC / CUI / defense           → cmmc-nist-800-171
GLBA / bank or fintech         → glba-ffiec-financial-privacy
```
