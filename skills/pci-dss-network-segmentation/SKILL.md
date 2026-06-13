---
name: pci-dss-network-segmentation
description: Validates PCI-DSS v4.0 network segmentation and scope reduction—Requirement 1.x (firewalls, network security controls) and 2.x (secure configurations)—for Cardholder Data Environment (CDE) isolation. Trigger when scoping PCI environments, reviewing firewall rules, VLAN segmentation, agent/MCP access to CDE, or reducing assessment scope. Do not use for payment-page script audits (use pci-dss-script-audit) or general IAM reviews without CDE focus (use access-control-identity-audit).
---

# PCI-DSS Network Segmentation

## Overview

This skill implements **PCI-DSS v4.0 Requirements 1 and 2** for **network segmentation** and **CDE scope reduction**. Proper segmentation limits PCI assessment scope to systems that store, process, or transmit **CHD/SAD** (cardholder data/sensitive authentication data) and systems connected to them.

Key requirements:

- **Req 1.2.x**: Network security control (NSC) configuration standards, inbound/outbound rules, CDE segmentation
- **Req 1.3.x**: Prohibit direct public access to CDE; restrict connections between untrusted networks and CDE
- **Req 1.4.x**: Personal firewall on mobile/remote devices accessing CDE
- **Req 2.x**: Secure configurations—change defaults, harden NSCs and system components

AI agents and MCP servers must **not** bridge untrusted networks into the CDE without explicit NSC rules and business justification.

## When to Use

Use this skill when:

- **Scoping PCI assessment**—identifying in-scope vs out-of-scope systems
- Reviewing **firewall rules, security groups, ACLs, WAF** between CDE and other zones
- Validating **segmentation test** (penetration test or connectivity probe) results
- Assessing whether **agent/MCP infrastructure** introduces CDE connectivity
- **Scope reduction** initiatives (moving payment to hosted iframe, P2PE)
- Hardening **NSC default configurations** (Req 2.1)

Do **not** use this skill when:

- Auditing checkout JavaScript (use `pci-dss-script-audit`)
- General SOC 2 logical access without CDE (use `access-control-identity-audit`)
- Encrypting data at rest (Req 3.x—note gap but use appropriate skill)

## Core Process

Execute steps **in order**.

### Step 1: CDE and connected-to identification

1. Inventory systems that **store, process, or transmit** CHD/SAD.
2. Identify systems **connected to** CDE (even if they don't touch CHD)—they enter scope unless adequately segmented.
3. Document data flows: payment forms, tokenization, API gateways, MCP Postgres access.
4. Artifact: `pci-scope-diagram-{id}.json` with trust zones (CDE, DMZ, Corporate, Cloud).

### Step 2: Network zone model

Define zones:

| Zone | Description | Default trust |
| --- | --- | --- |
| CDE | CHD/SAD processing | Highest restriction |
| DMZ | Public-facing, no CHD storage | Restricted |
| Corporate | Internal business systems | Untrusted relative to CDE |
| Agent/MCP | Compliance agent runtime | **Assess connectivity to CDE** |

Map all inter-zone connections with protocol, port, source, destination, business purpose.

### Step 3: Requirement 1.2 — NSC rule review

For each NSC (firewall, cloud SG, NACL, WAF):

1. Export rule set (JSON/text) via cloud API or config backup.
2. Verify **deny-all default** with explicit allow rules only.
3. Check **bidirectional justification** for each CDE rule:
   - Source IP/CIDR, destination, port, service owner, change ticket
4. Flag violations:
   - `ANY/ANY` rules touching CDE
   - Corporate zone → CDE without jump host or PAM
   - Agent/MCP subnet → CDE database port (CRITICAL unless scoped tokenization proxy)
5. Verify **rule review at least every 6 months** (Req 1.2.7)—collect review evidence.

### Step 4: Requirement 1.3 — CDE boundary protection

1. Confirm **no direct Internet → CDE** paths (except documented encrypted payment entry in DMZ).
2. Verify **DMZ → CDE** limited to minimum ports (e.g., app tier only).
3. Test from untrusted network (authorized pentest or automated probe):
   - Attempt connectivity to CDE IPs on common DB/app ports
   - Expected: **connection refused/timeout** unless explicitly allowed
4. Document segmentation test methodology and results.

### Step 5: Requirement 1.4 — Remote access

1. Inventory remote access paths to CDE (VPN, ZTNA, admin consoles).
2. Verify personal firewall on endpoints where applicable.
3. Ensure multi-factor authentication on all remote CDE access (cross-ref CC6/Req 8).

### Step 6: Requirement 2 — Secure NSC configuration

1. Verify default passwords changed on all NSCs (Req 2.1).
2. Remove unnecessary services, protocols, accounts (Req 2.2).
3. Document configuration standards with version ID.
4. Compare running config vs standard—drift = FAIL until remediated or authorized.

### Step 7: Agent/MCP segmentation assessment

1. Map compliance agent and MCP server network placement:
   - Playwright MCP: runs from which subnet? Can it reach CDE checkout URLs only (expected) or CDE backend?
   - Postgres MCP: which databases reachable? CDE DB = **in scope** for agent infrastructure
2. If agent bridges zones, require:
   - Dedicated jump architecture, read-only replicas outside CDE, or tokenized data only
   - NSC rules documented with PCI QSA review
3. **Never** store CHD in agent evidence DB without encryption and scope approval.

### Step 8: Scope reduction validation

1. Evaluate scope reduction strategies:
   - **SAQ A/A-EP**: outsourced payment, iframe isolation
   - **Tokenization**: agent sees tokens only, not PAN
   - **Network segmentation**: documented isolation per Appendix D guidance
2. If claiming reduced scope, provide **segmentation test evidence** proving out-of-scope systems cannot reach CDE.

### Step 9: Findings and evidence

1. Classify: CRITICAL (CDE exposed to Internet), HIGH (overly broad rule), MEDIUM (missing review documentation).
2. Package: rule exports, segmentation test results, scope diagram, remediation plan.

## Common Rationalizations

| Excuse the agent might generate | Required rebuttal |
| --- | --- |
| "We use tokenization, so network segmentation doesn't matter." | Tokenization reduces data scope but **connected systems** may still be in scope—segmentation still required. |
| "Cloud SG allows 0.0.0.0/0 on app port but WAF protects us." | NSC rules must be **least privilege**—reliance on WAF alone does not replace deny-by-default SG design. |
| "Compliance agent needs CDE DB access for audits." | Agent access **expands PCI scope**—use read replicas, sanitized data, or out-of-band QSA processes. |
| "Segmentation test passed last year." | Req 1.2.7 requires **ongoing** reviews and tests when topology changes—stale tests are insufficient. |
| "MCP runs in same VPC—that's internal, so safe." | Same VPC without zone segmentation often means **flat network**—explicit CDE isolation required. |
| "Temporary firewall rule for debugging is fine." | Undocumented temporary rules are **audit failures**—require ticket and expiry. |

## Red Flags

- CDE database security group allows corporate LAN or 0.0.0.0/0
- Agent/MCP Postgres tool can query tables containing PAN or SAD
- Segmentation test not performed after major cloud migration
- NSC rule review overdue (>6 months) with no compensating evidence
- Default vendor credentials on firewall/cloud NSC console
- Flat VPC with CDE and general workloads sharing unrestricted east-west traffic
- CHD found in agent evidence store or MCP logs

## Verification

- [ ] CDE and connected-to systems inventory complete with data flow diagram
- [ ] All NSC rule sets exported and reviewed for deny-default and least privilege
- [ ] No unauthorized ANY/ANY or Internet→CDE paths (or documented exception with QSA review)
- [ ] Segmentation connectivity test executed with results archived
- [ ] Req 1.4 remote access and MFA cross-checked
- [ ] Req 2 secure configuration standards applied with drift check
- [ ] Agent/MCP network placement assessed with CDE connectivity documented
- [ ] Scope reduction claims supported by segmentation test evidence
- [ ] Six-month NSC rule review evidence collected or scheduled gap flagged
- [ ] Findings prioritized with remediation owners and evidence bundle hashed
