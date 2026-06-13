---
preset_id: fintech-pci-dss
name: Fintech PCI-DSS
version: "1.0.0"
frameworks:
  - PCI-DSS-v4.0
industry: fintech
---

# Fintech PCI-DSS Preset

Apply for **merchants and service providers** processing cardholder data, especially e-commerce checkout and payment-page script governance (Req 6.4.3, 11.6.1).

## Default skills

1. `pci-dss-script-audit` — payment-page JavaScript inventory
2. `pci-dss-network-segmentation` — CDE isolation
3. `access-control-identity-audit` — Req 7/8
4. `audit-logging-integrity` — Req 10

## Scope defaults

| In scope | Out of scope |
| --- | --- |
| Checkout / payment pages | Corporate marketing site (no CHD) |
| CDE-connected agent integrations | Cardholder data in LLM prompts (must be zero) |
| Third-party payment scripts | Issuer processing environments |

## Critical rule

**Never send PAN, CVV, or magnetic stripe data to an LLM.** Agents may audit script URLs and metadata only.

## MCP configuration

Enable **Playwright MCP** for DOM/script capture. Use **GitHub MCP** for change-management evidence (Req 6.4.3 authorization records).

## Templates

- `templates/pci-script-baseline.yaml`
- `examples/pci-checkout-audit/config/baseline.yaml`

## Weekly monitoring

Req 11.6.1 requires weekly script/header tamper checks — configure `hooks/audit-mode.sh` for scheduled runs.

## Starter pack

`starter-packs/pci-dss-ecommerce-starter.yaml`
