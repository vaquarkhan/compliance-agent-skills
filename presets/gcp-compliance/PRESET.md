---
preset_id: gcp-compliance
name: GCP Compliance
version: "1.0.0"
cloud_provider: gcp
frameworks:
  - HIPAA-Security-Rule
  - PCI-DSS-v4.0
  - SOC2-TSC-2017
---

# GCP Compliance Preset

Control mappings for **Google Cloud Platform** workloads with Vertex AI / Gemini and agent tooling.

## Key GCP services

- **Cloud IAM** — least privilege, workforce identity (CC6, PCI 7)
- **Cloud Logging / Security Command Center** — audit and SIEM feeds
- **Cloud KMS** — encryption key management
- **VPC Service Controls** — data exfiltration boundaries
- **Vertex AI** — managed ML/LLM (assess BAA/status for ePHI)

## Segmentation

Use **VPC Service Controls** perimeters around projects containing agent backends and MCP servers. PCI CDE projects should be in separate perimeter from corporate.

## Skills to combine

- `pci-dss-network-segmentation` — VPC firewall rules, Shared VPC
- `compliance-as-code-governance` — Forseti/Policy Controller, Terraform
- `audit-logging-integrity` — log bucket retention and locks

## MCP deployment

Run MCP servers on **Cloud Run** with:

- Invoker IAM restricted to agent service account
- No `--allow-unauthenticated`
- Secret Manager for OAuth client credentials

## Evidence exports

- IAM Recommender reports
- SCC findings export
- Org Policy constraint compliance

## Note on Gemini

Verify Google's **BAA coverage** and data processing terms before routing even redacted clinical workflows through Vertex AI.
