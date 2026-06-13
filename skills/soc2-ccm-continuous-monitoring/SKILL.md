---
name: soc2-ccm-continuous-monitoring
description: Implements Continuous Control Monitoring (CCM) for SOC 2—automated control testing, configuration drift detection, predictive risk scoring, and alerting—for agent platforms, MCP servers, and cloud infrastructure. Trigger when building always-on compliance dashboards, detecting TSC control drift between audits, or operationalizing CC4/CC7 monitoring. Do not use for one-time evidence binders (use soc2-evidence-collection) or initial TSC mapping (use soc2-trust-services-criteria).
---

# SOC 2 CCM Continuous Monitoring

## Overview

**Continuous Control Monitoring (CCM)** satisfies SOC 2 **CC4.1** (monitoring activities) and **CC7.x** (system monitoring) by automating control tests on a schedule and alerting on drift. This skill operationalizes monitoring between annual audits—replacing point-in-time compliance with **always-on assurance**.

Components:

1. **Control test automation**: scheduled scripts/MCP jobs per TSC control
2. **Drift detection**: baseline vs current config comparison
3. **Predictive risk scores**: weighted FAIL trends, mean-time-to-remediate
4. **Alert routing**: Slack MCP, SIEM, ticketing integration

## When to Use

Use this skill when:

- Implementing **always-on SOC 2 monitoring** (Vanta/Drata-style continuous controls)
- Detecting **configuration drift** (IAM, firewall, MCP tool allowlists, agent skills)
- Building **executive risk dashboards** with control health scores
- Transitioning from **Type I point-in-time** to **Type II period-of-time** readiness
- Alerting on **regression** after remediation (control was PASS, now FAIL)
- Integrating compliance scans into CI/CD (Terraform, OPA policy checks)

Do **not** use this skill when:

- One-time audit evidence packaging (use `soc2-evidence-collection`)
- Initial control design gap analysis (use `soc2-trust-services-criteria`)
- PCI weekly script tamper detection (use `pci-dss-script-audit` 11.6.1 workflow)

## Core Process

Execute steps **in order**.

### Step 1: Control inventory for monitoring

1. Import TSC control matrix from `soc2-trust-services-criteria` output.
2. Filter controls suitable for **automated testing** (target ≥70% automation for CC6/CC7):
   - MFA enforcement, password policy, encryption at rest flags
   - Public S3 bucket detection, security group overly permissive rules
   - MCP OAuth scope drift, agent skill directory checksum changes
   - Failed login rate thresholds, backup success signals
3. Mark each control: **AUTOMATED**, **SEMI-AUTO**, **MANUAL**.
4. Artifact: `ccm-control-inventory-{id}.json`.

### Step 2: Baseline establishment

1. For each AUTOMATED control, capture **golden baseline**:
   - IAM policy JSON hash, SG rule set, MCP server config manifest
   - Authorized agent skills SHA-256 list from `skills/` directory
   - Presidio redaction config hash from `redaction.py` entity types
2. Store baselines in Postgres evidence schema with version IDs.
3. Require **human approval** before baseline promotion to production CCM.

### Step 3: Test schedule definition

| Control frequency | Examples | Minimum interval |
| --- | --- | --- |
| Real-time | Critical IAM changes, new MCP tool registration | Event-driven |
| Daily | Public exposure scans, cert expiry | 24h |
| Weekly | Script/header monitoring (PCI overlap), access anomaly | 7d |
| Monthly | Full IAM review sample, backup restore test | 30d |
| Quarterly | Access certification, policy review attestation | 90d |

Document schedule in `ccm-schedule-{id}.yaml` with cron expressions and owners.

### Step 4: Drift detection implementation

For each baselined asset:

1. **Collect current state** via same method as baseline (API, MCP, git).
2. **Diff** current vs baseline:
   - Added/removed/changed rules, policies, tools, skills
3. Classify drift:
   - **AUTHORIZED**: matching change ticket ID in ITSM
   - **UNAUTHORIZED**: no ticket → alert CRITICAL
   - **EXPECTED**: automated rotation with documented pattern
4. Store drift events with UTC timestamp and diff artifact.

#### Agent/MCP-specific drift checks

- `skills/` directory: new SKILL.md without CI validation → alert
- MCP tool manifest: tool added outside allowlist → alert
- `agent.py` redaction gate bypass (run without redact) → CRITICAL alert
- Playwright baseline DOM hash drift on monitored pages → cross-skill alert to PCI 11.6.1

### Step 5: Predictive risk scoring

1. Define score formula per control (example):
   ```
   risk_score = severity_weight × fail_count × (1 + days_open/30)
   ```
2. Aggregate to category level (CC6, CC7, CC8) and overall **control health %**.
3. Trend weekly; flag **negative trajectory** (health declining 2+ weeks).
4. Surface top 10 risks in executive dashboard—no raw ePHI in dashboard exports.

### Step 6: Alerting and escalation

1. Route alerts by severity:
   - CRITICAL: Slack MCP + PagerDuty analog, 15-minute response SLA
   - HIGH: Slack channel, 4-hour SLA
   - MEDIUM/LOW: daily digest ticket
2. Include: control ID, drift summary, baseline version, remediation runbook link.
3. **Suppress duplicate alerts** with correlation ID; do not alert-fatigue into ignored channels.

### Step 7: Evidence auto-capture for Type II

1. On each scheduled test PASS/FAIL, auto-append to evidence store:
   - Test output JSON, timestamp, hash
2. Enables `soc2-evidence-collection` to pull period samples without manual reruns.
3. Retain per organizational policy (typically examination period + 12 months).

### Step 8: CCM program review

1. Monthly: false positive rate, missed drift postmortems, control coverage %
2. Quarterly: recalibrate baselines, update automation for new TSC mappings
3. Annual: align with SOC 2 auditor on acceptable CCM evidence for Type II

## Common Rationalizations

| Excuse the agent might generate | Required rebuttal |
| --- | --- |
| "Annual audit is enough; CCM is redundant." | Type II requires **operating effectiveness over time**—CCM generates period-of-time proof. |
| "We'll monitor manually when someone remembers." | Manual monitoring fails **CC4.1** consistency requirements—automate or document systematic manual process with evidence. |
| "Drift without a ticket is probably fine." | Unauthorized drift is a **CC8** change management failure until proven otherwise. |
| "Risk scores are vanity metrics." | Scores must drive **prioritized remediation** with tracked MTTR—otherwise discard the metric. |
| "Alert on everything so we never miss anything." | Alert fatigue causes ignored CRITICAL items—tune severity and deduplication. |
| "CCM replaces soc2-evidence-collection entirely." | CCM **feeds** evidence collection—auditors may still request ad hoc samples. |

## Red Flags

- CCM baselines never updated after authorized changes (constant false positives)
- CRITICAL drift alerts disabled to reduce noise
- Agent redaction bypass undetected for >24 hours
- No event-driven monitoring on IAM/MCP tool registration
- CCM evidence retention shorter than SOC 2 examination period
- Risk scores published with customer ePHI in alert payloads
- 100% MANUAL control inventory claimed as CCM

## Verification

- [ ] CCM control inventory with AUTOMATED/SEMI-AUTO/MANUAL classification
- [ ] Baselines captured, versioned, and human-approved for production
- [ ] Test schedules documented with owners and cron/event triggers
- [ ] Drift detection running with AUTHORIZED/UNAUTHORIZED classification
- [ ] Agent/MCP-specific drift checks enabled (skills, tools, redaction gate)
- [ ] Risk scoring formula documented with weekly trend output
- [ ] Alert routing tested for CRITICAL and HIGH severities
- [ ] Auto-captured test results stored with hashes for Type II evidence
- [ ] Monthly/quarterly CCM review cadence scheduled
- [ ] False positive rate tracked with tuning backlog
