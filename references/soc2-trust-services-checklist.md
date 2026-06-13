# SOC 2 Trust Services Criteria Checklist

Based on AICPA **Trust Services Criteria** (2017, with 2022 revisions). Common Criteria (CC) apply to all examinations.

## CC1 — Control environment

- [ ] Board/management demonstrates commitment to integrity and ethics
- [ ] Organizational structure defines security/compliance roles
- [ ] Agent/MCP governance documented in system description

## CC2 — Communication and information

- [ ] Internal security policies communicated to personnel
- [ ] External commitments (SLAs, privacy notices) documented

## CC3 — Risk assessment

- [ ] Risk assessment identifies agent/LLM/MCP threats
- [ ] Fraud risk considered for automated tool chains

## CC4 — Monitoring activities

- [ ] Ongoing evaluations of control effectiveness
- [ ] CCM dashboards for agent infrastructure (`soc2-ccm-continuous-monitoring`)

## CC5 — Control activities

- [ ] Policies implemented via technology (policy-as-code)
- [ ] Agent deployments require CI/CD approval

## CC6 — Logical and physical access

| ID | Control | Agent relevance |
| --- | --- | --- |
| CC6.1 | Logical access restrictions | MCP OAuth scopes, IAM |
| CC6.2 | User registration/de-registration | JML for agent operators |
| CC6.3 | Role-based access | Tool allowlists per role |
| CC6.6 | System boundaries | VPC/perimeter around MCP |
| CC6.7 | Encryption in transit | TLS for all agent APIs |
| CC6.8 | Prevention of unauthorized software | Signed MCP containers |

## CC7 — System operations

| ID | Control | Agent relevance |
| --- | --- | --- |
| CC7.1 | Vulnerability management | MCP image scanning |
| CC7.2 | Security monitoring | SIEM for agent events |
| CC7.3 | Evaluation of anomalies | Alert triage runbooks |
| CC7.4 | Incident response | `breach-incident-response` |
| CC7.5 | Recovery | Agent failover tested |

## CC8 — Change management

- [ ] Changes authorized, tested, approved before production
- [ ] GitHub MCP evidence for agent config changes

## CC9 — Risk mitigation (vendor management)

- [ ] Vendor risk assessments for LLM/MCP providers
- [ ] Subservice organization controls documented (Carve-out/inclusive method)

## Optional categories

### Availability (A)

- [ ] Uptime monitoring for agent gateway
- [ ] DR tested for MCP backends

### Confidentiality (C)

- [ ] Confidential data classified and protected
- [ ] PHI redaction where applicable

### Processing Integrity (PI)

- [ ] Agent outputs validated for downstream systems

### Privacy (P)

- [ ] Privacy notice covers automated processing

## Skill mapping

Primary: `soc2-trust-services-criteria`, `soc2-evidence-collection`, `soc2-ccm-continuous-monitoring`

Template: `templates/soc2-control-evidence.yaml`

Example: `examples/soc2-evidence-bundle/`

---

## Authoritative sources

- AICPA Trust Services Criteria (2017): [SOC 2 overview](https://www.aicpa.org/resources/landing/system-and-organization-controls-soc-2)
- AICPA Description Criteria: [2018 Description Criteria](https://www.aicpa.org/resources/download/trust-services-criteria)

## Provenance

| Field | Value |
|-------|-------|
| **Source document** | AICPA Trust Services Criteria (2017) |
| **Version / effective** | 2017 TSC (current AICPA publication) |
| **Last reviewed** | 2026-06-13 |
| **Reviewer** | Repository maintainer |
| **Next review due** | 2026-09-13 |
| **Notes** | Agent-relevant CC subset; not a SOC 2 Type II report |
| **Review record** | [reviews/2026-Q2/soc2.md](../../reviews/2026-Q2/soc2.md) |
