# SME review records

Maintainer and external SME sign-off records for regulatory checklists in `references/`.

## Structure

```
reviews/
  YYYY-Qn/           # e.g. 2026-Q2
    README.md        # Index of reviews in this period
    hipaa.md           # Maintainer review record
    pci-dss.md
    ...
```

Each review file documents:

- Checklist path and git commit or version reviewed
- Authoritative source document version checked
- Changes made (if any)
- Review tier: **maintainer** or **external_sme**
- Sign-off (name/role and date)

## Cadence

See [docs/sme-review.md](../docs/sme-review.md) for framework-specific schedules.

| Tier | Who | Attestation |
|------|-----|-------------|
| Maintainer | Repository contributors | Structure, links, agent-relevant subset |
| External SME | QSA, Privacy Officer, CPA (optional) | Mapping to authoritative source |

## CI enforcement

`scripts/validate-sme-provenance.py` runs in CI and requires every `references/*checklist*.md` to include **Authoritative sources** and **Provenance** sections with required fields.

```bash
make validate-sme
python scripts/validate-sme-provenance.py --strict-dates  # fail on overdue reviews
```

## Opening a review

Use the GitHub issue template **SME checklist review** or copy `reviews/TEMPLATE.md`.
