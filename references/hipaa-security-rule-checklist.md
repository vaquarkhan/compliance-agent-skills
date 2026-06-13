# HIPAA Security Rule Checklist (Technical Safeguards)

Administrative and physical safeguards are out of scope for this technical checklist. Focus: **45 CFR §164.312** and agent/MCP architecture.

## §164.312(a) Access control

- [ ] **Unique user identification** — agent service accounts mapped to human owners
- [ ] **Emergency access procedure** — documented break-glass for clinical/agent outages
- [ ] **Automatic logoff** — session timeout on agent admin consoles
- [ ] **Encryption and decryption** — ePHI at rest encrypted (AES-256 or equivalent)

### Agent-specific

- [ ] MCP tools scoped to minimum necessary operations
- [ ] No shared API keys across environments
- [ ] RBAC enforced on agent configuration changes

## §164.312(b) Audit controls

- [ ] Hardware, software, and procedural mechanisms record ePHI access
- [ ] Agent prompt/tool invocations logged (redacted payloads)
- [ ] Logs protected against tampering (WORM, hash chains, SIEM)
- [ ] Retention meets organizational policy (typically ≥6 years for HIPAA entities)

## §164.312(c) Integrity

- [ ] Mechanisms authenticate ePHI not improperly altered/destroyed
- [ ] Code signing for agent deployments
- [ ] Integrity monitoring for MCP server images

## §164.312(d) Person or entity authentication

- [ ] Verify identity of persons/entities accessing ePHI
- [ ] MFA for admin access to agent gateway
- [ ] OAuth 2.1 + PKCE for MCP connections

## §164.312(e) Transmission security

- [ ] Integrity controls on ePHI in transit
- [ ] Encryption on all external ePHI transmissions (TLS 1.2+)
- [ ] No ePHI in LLM prompts without Presidio redaction (`redaction.py`)

## PHI redaction gate (repository standard)

- [ ] Presidio analyzes all user input before LLM reasoning
- [ ] Reversible tokens only deanonymized via authorized tool
- [ ] Redaction effectiveness tested quarterly

## Business associates

- [ ] BAA executed with LLM/cloud/MCP vendors touching ePHI flows
- [ ] Subprocessor list reviewed annually

## Skill mapping

Primary: `hipaa-technical-safeguards`, `hipaa-phi-redaction-pipeline`, `hipaa-baa-vendor-assessment`

Template: `templates/hipaa-phi-flow-diagram.yaml`
