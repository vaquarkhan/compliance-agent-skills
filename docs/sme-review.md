# SME review cadence and reference provenance

Regulatory checklists in `references/` are **operational aids**, not legal opinions. Skills cite them at runtime to reduce hallucination, but **accuracy and timeliness require human subject-matter expert (SME) review**.

## Review cadence

| Asset type | Minimum review | Trigger for out-of-cycle review |
|------------|----------------|----------------------------------|
| PCI-DSS, HIPAA, SOC 2 checklists | **Quarterly** | PCI SSC bulletin, OCR guidance, AICPA TSC update |
| State privacy (CCPA, etc.) | **Semi-annual** | New state law effective date |
| FedRAMP, CMMC, NIST | **Semi-annual** | NIST SP revision, CMMC rule change |
| FERPA, COPPA, EdTech | **Annual** | FTC policy statement, ED guidance |
| NIST AI RMF | **Semi-annual** | NIST AI RMF profile or playbook update |

## Provenance footer (required on each reference)

Every file under `references/` should end with:

```markdown
---

## Provenance

| Field | Value |
|-------|-------|
| **Source document** | e.g. PCI SSC PCI-DSS v4.0.1 |
| **Version / effective** | e.g. v4.0.1 (March 2024) |
| **Last reviewed** | YYYY-MM-DD |
| **Reviewer** | Name or role (e.g. QSA, CISO) |
| **Next review due** | YYYY-MM-DD |
| **Notes** | Optional scope limits |
```

## Review workflow

1. SME compares checklist items to authoritative source (official PDF, eCFR, NIST CSRC).
2. Update checklist and bump **Last reviewed** date.
3. Run `make validate` and open PR with `sme-review` label.
4. Link PR to change ticket or compliance calendar entry.

## Disclaimer

This repository does not replace Qualified Security Assessors, HIPAA Privacy Officers, licensed CPAs, or legal counsel. Provenance footers document **internal review effort**, not third-party attestation.
