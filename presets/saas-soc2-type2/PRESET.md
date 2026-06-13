---
preset_id: saas-soc2-type2
name: SaaS SOC 2 Type II
version: "1.0.0"
frameworks:
  - SOC2-TSC-2017
industry: saas
audit_type: Type2
---

# SaaS SOC 2 Type II Preset

Apply for **B2B SaaS** organizations undergoing SOC 2 Type II examinations with agent/MCP infrastructure in the system description.

## Default TSC categories

- **Security** (required)
- **Availability** (common for SaaS)
- **Confidentiality** (customer data processing)

Optional: Processing Integrity, Privacy — add only if in scope letter confirms.

## Default skills

1. `soc2-trust-services-criteria` — control mapping
2. `soc2-evidence-collection` — binder automation
3. `soc2-ccm-continuous-monitoring` — drift between audits
4. `access-control-identity-audit` — CC6.x
5. `vendor-third-party-risk` — CC9.2 subservice organizations

## Evidence period

Type II requires **continuous** evidence across the examination period (typically 6–12 months). Use `templates/audit-evidence-manifest.yaml` with quarterly snapshots.

## MCP configuration

- **GitHub MCP** — CC8.1 change tickets
- **Postgres MCP** — read-only evidence queries
- **Terraform MCP** — CC7.x infrastructure monitoring

## Agent platform controls

Map agent/MCP components to:

| Component | Typical TSC |
| --- | --- |
| Agent gateway | CC6.1, CC6.6 |
| MCP OAuth | CC6.1, CC6.7 |
| Prompt logging (redacted) | CC7.2 |
| Vendor LLM API | CC9.2 |

## Starter pack

`starter-packs/soc2-saas-starter.yaml`
