---
preset_id: azure-compliance
name: Azure Compliance
version: "1.0.0"
cloud_provider: azure
frameworks:
  - HIPAA-Security-Rule
  - PCI-DSS-v4.0
  - SOC2-TSC-2017
---

# Azure Compliance Preset

Control mappings for **Microsoft Azure** deployments including Azure OpenAI with HIPAA BAA.

## Key Azure services

- **Microsoft Entra ID** — IAM, MFA, conditional access (CC6, PCI 8)
- **Azure Monitor / Log Analytics** — centralized logging (CC7.2, PCI 10)
- **Key Vault** — secrets and key management
- **Azure Policy** — compliance-as-code guardrails
- **Azure OpenAI** — LLM with Microsoft BAA (document in BAA registry)

## Agent architecture notes

Prefer **Azure OpenAI** over public endpoints when ePHI may be processed (after Presidio redaction). Document data residency region in scope artifact.

## Skills to combine

- `hipaa-baa-vendor-assessment` — Microsoft BAA + subprocessor list
- `compliance-as-code-governance` — Azure Policy + Terraform
- `access-control-identity-audit` — Entra ID role reviews

## MCP hardening

Host MCP servers on **Azure Container Apps** or **AKS** with:

- Managed identity (no long-lived secrets in env)
- Private endpoints for Postgres MCP backends
- Application Gateway WAF for external MCP ingress

## Evidence exports

- Entra ID access review reports
- Azure Policy compliance dashboard
- Diagnostic settings for agent hosting resources
