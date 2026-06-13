# Security Policy

## Supported versions

| Version | Supported          |
| ------- | ------------------ |
| 1.5.x   | :white_check_mark: |
| 1.4.x   | :white_check_mark: |
| 1.3.x   | :white_check_mark: |
| 1.2.x   | :white_check_mark: |
| < 1.2   | :x:                |

## Reporting a vulnerability

**Do not open public GitHub issues for security vulnerabilities.**

Submit reports via [GitHub Security Advisories](https://github.com/vaquarkhan/compliance-agent-skills/security/advisories/new) (private disclosure).

Include:

- Description of the vulnerability
- Steps to reproduce
- Impact assessment (especially PHI/CHD exposure paths)
- Suggested remediation, if any

We aim to acknowledge reports within **2 business days** and provide a remediation timeline within **10 business days**.

## Scope

In scope:

- `agent.py` / `redaction.py` bypass or deanonymization leaks
- MCP template misconfigurations that expose credentials or excessive tool scope
- Hook scripts that fail to enforce PHI redaction or audit mode
- Plugin installers that write outside intended directories

Out of scope:

- Third-party MCP server vulnerabilities (report to upstream maintainers)
- Customer misconfiguration of cloud IAM unrelated to this repository's templates

## PHI handling

This repository is designed so **raw ePHI never reaches the LLM**. Model output is returned **with redacted tokens by default**; restoring original values requires explicit opt-in (`deanonymize_output=True` or `COMPLIANCE_AGENT_DEANONYMIZE=1`). If you discover a path where Presidio redaction can be skipped or PHI is auto-restored without authorization, treat it as **critical** severity.
