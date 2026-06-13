---
name: pci-dss-encryption-key-management
description: Audits PCI-DSS v4.0 Requirement 3 (protect stored account data) and Requirement 4 (protect cardholder data with strong cryptography during transmission)—covering key management lifecycle, HSM usage, PAN masking, tokenization, and TLS 1.2+ enforcement with Terraform/Vault MCP patterns for evidence collection. Trigger when assessing encryption of CHD/SAD at rest or in transit, reviewing key rotation and split knowledge, validating tokenization scope reduction, or scanning IaC for crypto misconfigurations. Do not use for network segmentation (use pci-dss-network-segmentation), payment-page script inventory (use pci-dss-script-audit), or general IAM without crypto focus (use access-control-identity-audit).
---

# PCI-DSS Encryption and Key Management

## Overview

This skill implements **PCI-DSS v4.0 Requirements 3 and 4** for **protecting account data** at rest and in transit. These requirements apply to all systems that **store, process, or transmit** cardholder data (CHD) or sensitive authentication data (SAD).

**Requirement 3 — Protect stored account data:**

| Sub-requirement | Focus |
| --- | --- |
| **3.1** | Processes and mechanisms for protecting stored account data |
| **3.2** | **SAD storage prohibited** after authorization (full track, CVV, PIN)—never store post-auth |
| **3.3** | **PAN masking** when displayed (show first six/last four max per PCI guidance) |
| **3.4** | PAN rendered unreadable anywhere stored (encryption, hashing, tokenization, truncation) |
| **3.5** | Key management procedures documented and implemented |
| **3.6** | **Cryptographic keys** protected against disclosure and misuse |
| **3.7** | Key management documented for keys used to protect stored account data |

**Requirement 4 — Protect CHD during transmission:**

| Sub-requirement | Focus |
| --- | --- |
| **4.1** | Processes for strong cryptography during transmission over open, public networks |
| **4.2** | **PAN** protected with strong cryptography during transmission |
| **4.2.1** | Inventory of trusted keys and certificates |
| **4.2.2** | Wireless networks transmitting PAN use strong cryptography |

**Key management lifecycle** (Req 3.6–3.7): generation, distribution, storage, rotation, retirement, destruction. **HSMs** (Hardware Security Modules) or cloud KMS (AWS KMS, Azure Key Vault, GCP Cloud KMS) are standard for production PAN encryption.

This skill integrates **Terraform MCP** (`mcp/terraform.mcp.json`) and **HashiCorp Vault** patterns per `references/compliance-as-code-patterns.md` and `compliance-as-code-governance`.

## When to Use

Use this skill when:

- **Scoping encryption** for databases, logs, backups, and agent evidence stores touching CHD
- Auditing **key rotation**, dual control, and split knowledge (Req 3.6)
- Validating **tokenization** architecture for scope reduction
- Reviewing **TLS configuration** on payment endpoints, APIs, and MCP transport (Req 4.2)
- Scanning **Terraform/IaC** for unencrypted RDS, S3, or cleartext PAN fields
- Assessing whether **compliance agent/MCP** logs or Postgres evidence DB contain PAN

Do **not** use this skill when:

- Firewall/CDE segmentation (use `pci-dss-network-segmentation`)
- Checkout JavaScript and Req 6.4.3 (use `pci-dss-script-audit`)
- HIPAA ePHI encryption without CHD (use `hipaa-technical-safeguards`)
- California consumer privacy rights (use `ccpa-cpra-privacy-rights`)

## Core Process

Execute steps **in order**.

### Step 1: Account data inventory (Req 3.1)

1. Locate all CHD and SAD: databases, flat files, logs, backups, crash dumps, agent session stores, MCP query results.
2. Classify storage:

| Location | PAN present? | Protection method | In CDE? |
| --- | --- | --- | --- |
| Payment DB | Yes | AES-256 + KMS | Yes |
| Agent evidence Postgres | Must be No | Token only | Assess scope |
| Application logs | Must be No | Masking/redaction | Varies |

3. **CRITICAL**: Any PAN in agent/MCP logs expands PCI scope—scan with synthetic test PAN patterns.
4. Artifact: `account-data-inventory-{id}.csv`.

### Step 2: SAD and display controls (Req 3.2, 3.3)

1. Verify **no SAD stored** after authorization—query schemas for track data, CVV, PIN fields.
2. Review UI and admin consoles for **PAN masking** (max first six and last four for issuer identification).
3. Verify agent tools and `deanonymize_response` cannot expose full PAN without business justification and logging.
4. FAIL if full PAN appears in Slack MCP notifications or evidence exports.

### Step 3: PAN unreadable at rest (Req 3.4)

1. For each PAN storage location, verify one of:
   - **Strong cryptography** (AES-256 with per-record or envelope encryption)
   - **One-way hash** (with salt, for non-reversible use cases only)
   - **Tokenization** (irreversible token with secure token vault)
   - **Truncation** (if no storage of full PAN required)
2. Prohibit reversible encoding (Base64 alone) as "encryption."
3. Verify encryption keys are **not stored alongside** encrypted PAN (same DB table, same S3 object metadata unprotected).

### Step 4: Key management procedures (Req 3.5–3.7)

Document and test:

1. **Key generation** — cryptographically secure RNG; HSM/KMS where feasible.
2. **Key distribution** — secure channels; no keys in git, Slack, or agent prompts.
3. **Key storage** — HSM, KMS, or Vault with access logging.
4. **Key rotation** — periodic rotation per crypto period (typically annual or on compromise); document calendar.
5. **Key retirement** — secure destruction/archival when keys expire.
6. **Split knowledge / dual control** — minimum two people for critical key operations (Req 3.6.1.2).
7. Artifact: `key-management-procedures-{id}.pdf` with version and approver.

### Step 5: HSM and KMS validation

1. Inventory all key stores:

| System | Key type | FIPS 140-2/3 validated? | Access control |
| --- | --- | --- | --- |
| AWS KMS | DEK/CMK | Level 2+ (KMS) | IAM roles |
| HashiCorp Vault | Transit keys | Depends on backend | Vault policies |
| On-prem HSM | Master keys | Level 3 typical | M of N admin |

2. Verify KMS/Vault policies enforce **least privilege**—cross-ref `access-control-identity-audit`.
3. Verify **audit logs** for key use—cross-ref `audit-logging-integrity` (PCI Req 10 overlap).
4. Test: unauthorized identity cannot `decrypt` or `export` key material.

### Step 6: Tokenization assessment

1. Document tokenization flow: PAN → token vault → token returned to application/agent.
2. Verify agent and MCP see **tokens only**, not PAN—supports scope reduction with `pci-dss-network-segmentation`.
3. Validate token vault meets Req 3.4–3.7 (same rigor as PAN encryption).
4. Verify detokenization is restricted, logged, and not available via MCP without approval.

### Step 7: Transmission security (Req 4.1, 4.2)

1. Inventory all channels transmitting PAN: HTTPS checkout, API, internal service mesh, MCP transport.
2. Verify **TLS 1.2 or higher**; disable SSLv3, TLS 1.0/1.1 (Req 4.2, industry standard).
3. Review cipher suites—prefer forward secrecy (ECDHE); disable weak ciphers.
4. Maintain **certificate inventory** (Req 4.2.1): expiry monitoring, trusted CA chain, no self-signed in production payment paths.
5. Test with SSL Labs or `openssl s_client` from authorized probe; store results.
6. **MCP compliance**: TLS 1.2+ for all MCP server connections per `mcp-compliance-integration`.

### Step 8: Terraform/Vault MCP evidence collection

1. Configure **Terraform MCP** read-only against state backend:
   ```json
   // mcp/terraform.mcp.json — read-only plan/state
   ```
2. Scan for violations:
   - RDS/SQL without `storage_encrypted = true`
   - S3 buckets with CHD tags lacking encryption
   - ALB/listeners allowing TLS 1.0
   - Secrets in plaintext Terraform variables
3. **Vault MCP** (if deployed): export policy list showing who can read transit keys—never export key material via MCP.
4. Integrate **Checkov/tfsec** rules from `compliance-as-code-governance`—map to PCI 3.4, 4.2.
5. Hash scan outputs for evidence manifest.

### Step 9: Findings and remediation

1. Severity guide:
   - **CRITICAL**: Cleartext PAN in logs/agent store; SAD stored post-auth; TLS 1.0 on payment path
   - **HIGH**: Missing key rotation; keys in source control; no dual control on HSM
   - **MEDIUM**: Certificate expiry monitoring gap; incomplete key inventory
2. Emit standard finding YAML with `control_id: PCI-3.4` or `PCI-4.2`.

## Common Rationalizations

| Excuse the agent might generate | Required rebuttal |
| --- | --- |
| "We tokenize at the gateway, so Req 3 doesn't apply to our app." | If **any** system stores/processes PAN, Req 3 applies—tokenization must cover **all** PAN locations including logs. |
| "TLS terminates at the load balancer; backend HTTP is internal." | Internal networks are not exempt if PAN traverses them—encrypt or segment per Req 4 and Req 1. |
| "KMS manages keys, so we don't need documented procedures." | Req 3.5–3.7 require **documented procedures** for human processes around KMS—managed service ≠ procedural compliance. |
| "Agent only sees tokens occasionally—we don't audit that path." | **Any** PAN exposure path is in scope—MCP Postgres queries must be proven token-only. |
| "Vault dev mode is fine for staging." | Staging with real PAN patterns requires **production-equivalent** crypto—dev mode Vault is a CRITICAL finding if CHD present. |
| "Base64 encoding protects PAN in the database." | Encoding is **not encryption**—Req 3.4 requires strong cryptography or approved alternative. |

## Red Flags

- Full PAN or CVV in application, agent, or MCP logs
- Encryption keys in git repository or agent skill files
- TLS 1.0/1.1 enabled on payment or PAN API endpoints
- RDS/database storage encryption disabled in Terraform state
- Tokenization bypass API returns PAN to agent tools without audit
- No key rotation evidence for >12 months
- Single person can generate, distribute, and activate production keys (no dual control)
- Vault or KMS decrypt permission granted to broad `*` IAM role
- SAD retained in database after authorization completes

## Verification

- [ ] Account data inventory complete including agent/MCP/log locations
- [ ] SAD storage verified absent post-authorization (Req 3.2)
- [ ] PAN masking validated on all display and notification paths (Req 3.3)
- [ ] All PAN at rest rendered unreadable per Req 3.4 with method documented
- [ ] Key management procedures documented covering full lifecycle (Req 3.5–3.7)
- [ ] HSM/KMS/Vault access controls and audit logging verified
- [ ] Tokenization flow documented; agent/MCP confirmed token-only
- [ ] TLS 1.2+ verified on all PAN transmission paths (Req 4.2)
- [ ] Certificate inventory and expiry monitoring operational (Req 4.2.1)
- [ ] Terraform MCP / Checkov scan completed with findings remediated or tracked
- [ ] Evidence manifest with SHA-256 hashes and PCI control ID mapping
