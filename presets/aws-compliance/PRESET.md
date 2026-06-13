---
preset_id: aws-compliance
name: AWS Compliance
version: "1.0.0"
cloud_provider: aws
frameworks:
  - HIPAA-Security-Rule
  - PCI-DSS-v4.0
  - SOC2-TSC-2017
---

# AWS Compliance Preset

Cloud-specific control mappings for workloads on **Amazon Web Services** with agent/MCP deployments.

## Shared responsibility focus

| Layer | AWS responsibility | Customer responsibility |
| --- | --- | --- |
| Physical | Data centers | — |
| Hypervisor | EC2, Lambda isolation | — |
| Network | VPC infrastructure | Security groups, NACLs, segmentation |
| Application | Managed services | Agent code, MCP configs, IAM policies |

## Key AWS services (typical)

- **IAM / SSO** — access control (CC6, PCI 7/8)
- **CloudTrail + CloudWatch** — audit logging (CC7.2, PCI 10)
- **KMS** — encryption at rest (§164.312(a)(2)(iv))
- **WAF / Shield** — edge protection (PCI 1.x)
- **AWS Config / Security Hub** — compliance-as-code drift

## Skills to combine

- `compliance-as-code-governance` — Checkov/tfsec on Terraform
- `audit-logging-integrity` — CloudTrail integrity validation
- `pci-dss-network-segmentation` — CDE VPC isolation

## MCP

Use **Terraform MCP** against read-only state backend for drift evidence. Never grant MCP write access to production IAM.

## HIPAA on AWS

Require **BAA with AWS** before ePHI in account. Document in `templates/hipaa-phi-flow-diagram.yaml` which services touch ePHI (S3, RDS, Bedrock, etc.).

## Evidence exports

- IAM Access Analyzer findings
- Config conformance pack reports
- CloudTrail Lake queries (agent API calls)
