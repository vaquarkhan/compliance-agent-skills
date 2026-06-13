# PCI-DSS v4.0 Checklist (Agent-Relevant Subset)

Full PCI-DSS has 12 requirements. This checklist emphasizes controls commonly tested when **AI agents or MCP tools** interact with payment environments.

## Requirement 1: Network security controls

- [ ] NSCs installed between CDE and untrusted networks
- [ ] Inbound/outbound traffic restricted to necessary ports/services
- [ ] Agent/MCP servers in CDE segment documented and justified
- [ ] Segmentation validated annually (`pci-dss-network-segmentation`)

## Requirement 2: Secure configurations

- [ ] System components configured securely (no default passwords)
- [ ] MCP server hardening baseline applied
- [ ] Configuration standards reviewed every 6 months

## Requirement 6: Develop and maintain secure systems

### 6.4.3 Payment-page scripts

- [ ] Inventory of all payment-page scripts maintained
- [ ] Each script has business justification and authorization record
- [ ] Integrity mechanism (SRI, CSP, or hash) for each script
- [ ] Method to detect unauthorized script changes

### 6.4.3 Agent note

Agents using Playwright MCP must **not** inject scripts into payment pages — read-only audit mode only.

## Requirement 7: Restrict access to CHD

- [ ] Access need-to-know enforced
- [ ] Agent service accounts denied CHD database access unless explicitly scoped

## Requirement 8: Identify users and authenticate access

- [ ] MFA for all CDE access
- [ ] Unique IDs for all users and service accounts

## Requirement 10: Log and monitor

- [ ] Audit trails for CHD access and privileged actions
- [ ] Logs protected, retained ≥12 months (3 months immediately available)
- [ ] Agent/MCP tool calls in CDE logged

## Requirement 11: Test security regularly

### 11.6.1 Tamper detection

- [ ] Weekly detection of unauthorized changes to payment pages
- [ ] Security header monitoring (CSP, HSTS)
- [ ] Alerts investigated within defined SLA

## Requirement 12: Support information security with policies

- [ ] Risk assessment includes agent/MCP integrations
- [ ] Personnel trained on AI tool usage in CDE

## Absolute prohibitions for agents

- **Never** process PAN, CVV, or PIN in LLM prompts
- **Never** store CHD in agent memory or logs

## Skill mapping

Primary: `pci-dss-script-audit`, `pci-dss-network-segmentation`, `audit-logging-integrity`

Template: `templates/pci-script-baseline.yaml`

Example: `examples/pci-checkout-audit/`
