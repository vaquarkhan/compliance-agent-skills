# SME review cadence and reference provenance

Regulatory checklists in `references/` are **operational aids**, not legal opinions. Skills cite them at runtime to reduce hallucination, but **accuracy and timeliness require human subject-matter expert (SME) review**.

## Review cadence

| Asset type | Minimum review | Trigger for out-of-cycle review |
|------------|----------------|----------------------------------|
| PCI-DSS, HIPAA, SOC 2, HITECH checklists | **Quarterly** | PCI SSC bulletin, OCR guidance, AICPA TSC update |
| State privacy (CCPA, etc.), GDPR | **Semi-annual** | New state law effective date |
| FedRAMP, CMMC, NIST CSF, SOX, ISO, GLBA | **Semi-annual** | NIST SP revision, CMMC rule change |
| FERPA, COPPA, EdTech | **Annual** | FTC policy statement, ED guidance |
| NIST AI RMF | **Semi-annual** | NIST AI RMF profile or playbook update |

## Required checklist sections

Every file matching `references/*checklist*.md` must include:

1. **`## Authoritative sources`** — at least one link to official guidance
2. **`## Provenance`** — table with required fields below

### Provenance footer (required)

```markdown
---

## Authoritative sources

- ...

## Provenance

| Field | Value |
|-------|-------|
| **Source document** | e.g. PCI SSC PCI-DSS v4.0.1 |
| **Version / effective** | e.g. v4.0.1 (March 2024) |
| **Last reviewed** | YYYY-MM-DD |
| **Reviewer** | Name or role (e.g. QSA, CISO) |
| **Next review due** | YYYY-MM-DD |
| **Notes** | Optional scope limits |
| **Review record** | Link to reviews/YYYY-Qn/framework.md (recommended) |
```

## Review tiers

| Tier | Who | Attestation |
|------|-----|-------------|
| **Maintainer** | Repository contributors | Structure, links, agent-relevant subset |
| **External SME** | QSA, Privacy Officer, CPA (optional) | Mapping to authoritative source |

Use `Repository maintainer` until a named SME completes review; update **Reviewer** when sign-off is recorded.

## Review workflow

1. SME compares checklist items to authoritative source (official PDF, eCFR, NIST CSRC).
2. Update checklist and bump **Last reviewed** / **Next review due** dates.
3. Add a record under `reviews/YYYY-Qn/` (copy from [reviews/TEMPLATE.md](../reviews/TEMPLATE.md)).
4. Run `make validate` (includes `validate-sme`) and open PR with `sme-review` label.
5. Link PR to change ticket or compliance calendar entry.

## CI enforcement

```bash
python scripts/validate-sme-provenance.py           # required in CI
python scripts/validate-sme-provenance.py --strict-dates  # fail on overdue reviews
make validate-sme
```

The validator fails if any checklist is missing sections, required provenance rows, or a valid `Next review due` date.

## Disclaimer

This repository does not replace Qualified Security Assessors, HIPAA Privacy Officers, licensed CPAs, or legal counsel.

See also [reviews/README.md](../reviews/README.md).
