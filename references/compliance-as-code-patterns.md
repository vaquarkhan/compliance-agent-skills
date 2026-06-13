# Compliance-as-Code Patterns

Automating HIPAA, PCI-DSS, and SOC 2 controls via policy-as-code and IaC scanning.

## Tooling matrix

| Tool | Use case | Frameworks |
| --- | --- | --- |
| **OPA / Rego** | Runtime and CI policy decisions | SOC 2 CC5, HIPAA access |
| **Checkov / tfsec** | Terraform static analysis | PCI 2.x, SOC 2 CC7 |
| **Sentinel** | Terraform Cloud policy sets | Enterprise SOC 2 |
| **AWS Config / Azure Policy / Org Policy** | Cloud drift detection | All |
| **Conftest** | Kubernetes manifest tests | Agent/MCP deployments |

## CI gate pattern

```yaml
# .github/workflows/compliance-gate.yml (conceptual)
jobs:
  iac-scan:
    steps:
      - run: checkov -d terraform/ --framework terraform
      - run: conftest test k8s/ --policy policies/
  policy-test:
    steps:
      - run: opa test policies/ -v
```

Block merge on **HIGH** findings in CDE/agent production paths.

## OPA example: deny public MCP ingress

```rego
package mcp.network

deny[msg] {
  input.resource_type == "kubernetes_ingress"
  input.metadata.labels.app == "mcp-server"
  not input.spec.tls
  msg := "MCP ingress must use TLS"
}
```

## Drift remediation workflow

1. **Detect** — Terraform MCP or cloud Config rules
2. **Ticket** — auto-create Jira with control ID (CC7.2)
3. **Remediate** — IaC PR with `/remediate` owner assignment
4. **Evidence** — attach plan/apply logs to evidence manifest

## Agent-specific policies

- Deny agent deployments without `presidio-sidecar` label (HIPAA)
- Deny MCP `tools` list exceeding approved manifest
- Require signed container images (Cosign)

## Skill mapping

Primary: `compliance-as-code-governance`

MCP: `mcp/terraform.mcp.json`

Preset: `presets/aws-compliance/PRESET.md`, `azure-compliance`, `gcp-compliance`
