---
name: compliance-as-code-governance
description: Implements policy-as-code and infrastructure compliance scanning—OPA/Rego policies, Terraform static analysis, CI gates, and drift remediation—for SOC 2, HIPAA, and PCI control enforcement. Trigger when codifying security policies, integrating Checkov/tfsec/Sentinel, or automating guardrails for agent/MCP deployments. Do not use for one-time manual audits (use framework-specific skills) or vendor BAA review (use hipaa-baa-vendor-assessment).
---

# Compliance-as-Code Governance

## Overview

This skill codifies compliance controls as **executable policy** integrated into CI/CD and runtime admission. It bridges **SOC 2 CC8** (change management), **CC5** (control activities), **HIPAA §164.312** (technical safeguards), and **PCI Req 2** (secure configurations) through:

- **OPA/Rego** policies for Kubernetes, API gateways, and custom resources
- **Terraform/IaC scanning** (Checkov, tfsec, terraform-compliance)
- **Git-pre-merge gates** blocking non-compliant infrastructure
- **Policy versioning** aligned with TSC control matrix

Compliance-as-code is **not** a substitute for auditor evidence—it generates **continuous proof** consumed by `soc2-ccm-continuous-monitoring` and `soc2-evidence-collection`.

## When to Use

Use this skill when:

- **Codifying** security baselines (encryption, public access, MFA) as OPA/Rego or scan rules
- Adding **CI gates** for Terraform, Kubernetes manifests, or MCP server configs
- **Remediating drift** detected by CCM with policy updates
- Standardizing **agent deployment** guardrails (skills validation, redaction required)
- Mapping **policy rules to TSC/PCI/HIPAA** control IDs for traceability
- Building **exception workflows** for time-bound policy waivers with approval

Do **not** use this skill when:

- Legal BAA negotiation (use `hipaa-baa-vendor-assessment`)
- Initial TSC gap analysis without automation intent (use `soc2-trust-services-criteria`)
- Payment page script inventory (use `pci-dss-script-audit`)

## Core Process

Execute steps **in order**.

### Step 1: Policy scope and control mapping

1. Import control requirements from TSC matrix, PCI Req 1-2, HIPAA §164.312.
2. Select **automatable** controls (encryption flags, SG rules, IAM policies, public exposure).
3. Create traceability matrix:

| Policy ID | Rego/scan rule | Control ID | Severity |
| --- | --- | --- | --- |
| POL-S3-001 | deny public S3 ACL | CC6.1, PCI 1.3 | CRITICAL |
| POL-IAM-002 | require MFA for admin | CC6.1, PCI 8.4 | HIGH |
| POL-AGENT-003 | redaction gate in agent.py | HIPAA §164.312(e) | CRITICAL |

Artifact: `policy-control-matrix-{id}.csv`.

### Step 2: OPA/Rego policy development

1. Organize policies in `policy/` directory with package naming convention:
   ```
   package compliance.soc2.cc6
   ```
2. Write Rego rules with **deny** messages citing control ID:
   ```rego
   deny[msg] {
     input.resource.type == "aws_s3_bucket"
     input.resource.public_access == true
     msg := "CC6.1/PCI1.3: S3 bucket must not allow public access"
   }
   ```
3. Include **unit tests** (`*_test.rego`) with positive and negative cases.
4. Version policies in git; tag releases aligned with baseline promotions.

### Step 3: Terraform/IaC scanning

1. Configure Checkov or tfsec with custom checks mapped to policy IDs.
2. Scan targets: VPC, SG, IAM, RDS, EKS, MCP deployment modules.
3. Fail CI on CRITICAL/HIGH unless documented exception ID present in resource tag:
   `ComplianceException = EX-2025-042`
4. Export SARIF/JSON for evidence store.

### Step 4: CI/CD pipeline integration

1. Pipeline stages:
   - **Lint**: Rego compilation, policy tests
   - **Plan scan**: Terraform plan JSON → OPA evaluation
   - **Apply gate**: manual approval for production with policy summary
2. Agent-specific gates:
   - `SkillsCapability(validate=True)` must remain enabled in `agent.py`
   - `redactor.redact()` must precede `compliance_agent.run()` (static analysis or AST check)
   - New `skills/*/SKILL.md` must pass schema validation
3. Block merge on policy failure—no `--no-verify` bypass without security approval.

### Step 5: Runtime admission (optional)

1. Deploy OPA as admission controller (Kubernetes) or API gateway plugin.
2. Enforce policies on MCP server deployments: resource limits, network policies, secret mounts.
3. Log deny decisions to SIEM for CC7 evidence.

### Step 6: Exception management

1. Exception request requires: control ID, risk analysis, approver, expiry date (max 90 days default).
2. Tag affected resources; CCM monitors exception expiry.
3. Expired exceptions → auto-FAIL in CCM dashboard.

### Step 7: Drift remediation loop

1. When CCM detects drift, determine if:
   - Policy gap (update Rego)
   - Unauthorized change (incident)
   - Authorized change (update baseline)
2. Link remediation PR to control ID and evidence hash post-merge.

### Step 8: Evidence and reporting

1. Store CI scan outputs with SHA-256 in evidence bucket.
2. Monthly report: policy pass rate, top violations, mean time to remediate.
3. Feed `soc2-evidence-collection` for CC8 change and CC5 control activity samples.

## Common Rationalizations

| Excuse the agent might generate | Required rebuttal |
| --- | --- |
| "Policy-as-code replaces SOC 2 audits." | It **automates control testing**—auditors still require design/operating effectiveness assessment. |
| "We'll scan Terraform in prod only." | Policies must run at **plan/PR stage**—post-deploy scanning is too late for prevention. |
| "OPA is too complex; manual checklist is enough." | Manual checklists don't scale and fail **CC8** consistency—codify repeatable rules. |
| "Exception tags are technical debt we ignore." | Untracked exceptions are **audit findings**—require expiry and approval workflow. |
| "Agent redaction can't be policy-checked." | Static analysis can verify call order in `agent.py`—implement POL-AGENT-003. |
| "Critical findings can merge with a JIRA link later." | CRITICAL policy failures must **block merge** until fixed or formal exception recorded. |

## Red Flags

- Terraform apply without plan-time policy scan
- Public cloud resources deployed with `ComplianceException` tag and no ticket
- OPA policies without unit tests or version control
- Agent deployment bypasses redaction gate in CI
- Policy matrix missing mapping to control IDs (orphan rules)
- Exception expiry dates passed with no remediation
- Scan results stored only in ephemeral CI logs (no evidence retention)

## Verification

- [ ] Policy-control traceability matrix complete with severity levels
- [ ] OPA/Rego policies written with unit tests and git versioning
- [ ] Terraform/IaC scanning integrated in CI with CRITICAL/HIGH block rules
- [ ] Agent-specific gates verify skills validation and redaction call order
- [ ] Exception workflow documented with max expiry and approver roles
- [ ] Runtime admission deployed (if in scope) with deny logging to SIEM
- [ ] CCM integration feeds drift events into remediation loop
- [ ] Monthly policy compliance report generated with pass rates
- [ ] Scan artifacts retained with SHA-256 for SOC 2 evidence
- [ ] No CRITICAL violations in production without active approved exception
