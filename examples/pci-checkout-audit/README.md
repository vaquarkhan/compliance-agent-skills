# PCI Checkout Script Audit Example

Demonstrates **PCI-DSS v4.0 Requirement 6.4.3** payment-page script inventory and baseline comparison using the compliance agent toolkit.

## Prerequisites

- Python 3.11+
- Optional: Playwright MCP for live DOM capture
- **Authorization** to audit target checkout URL

## Structure

```
pci-checkout-audit/
├── README.md
├── Makefile
└── config/
    └── baseline.yaml
```

## Quick start

```bash
cd examples/pci-checkout-audit
make validate          # Validate baseline YAML structure
make audit URL=https://example.com/checkout   # Placeholder audit target
```

## Workflow

1. **Scope** — confirm checkout URL is in-scope CDE-connected page
2. **Baseline** — edit `config/baseline.yaml` with authorized scripts
3. **Audit** — compare live page scripts vs baseline (Playwright MCP or manual export)
4. **Evidence** — hash screenshots and script lists into evidence manifest
5. **Report** — document gaps (missing authorization, missing SRI)

## Skill

Load `pci-dss-script-audit` for full procedure.

## Safety

- **Never** enter real PAN/CVV in automated browsers
- Use test merchant environments when possible
- Read-only audit mode: `source ../../hooks/audit-mode.sh`

## Template

Based on `templates/pci-script-baseline.yaml`.
