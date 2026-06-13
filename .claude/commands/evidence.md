# /evidence — Evidence Collection

Collect, hash, and package audit artifacts for assessors.

## Prerequisites

- Completed `/audit` with documented findings
- Skill: `soc2-evidence-collection` (cross-framework evidence mechanics)

## Instructions

1. **Inventory required evidence** per control/finding from audit worksheet.
2. **Collect artifacts** — exports, screenshots, log samples, config snapshots.
3. **Compute SHA-256** for each file.
4. **Populate manifest** — `templates/audit-evidence-manifest.yaml`.
5. **Chain of custody** — record collector, timestamp, source system.
6. **Store bundle** in `evidence-bundle/{engagement-id}/` (gitignored locally).

## Integrity

```bash
sha256sum evidence/* > evidence-bundle/sha256sums.txt
```

Update `bundle_hash` in manifest after all artifacts listed.

## Rules

- No raw PHI/PAN in evidence filenames or unencrypted shares
- Redact screenshots before external transfer
- Prefer read-only MCP queries for database evidence

## Output

Completed `audit-evidence-manifest.yaml` ready for auditor handoff.

## Next command

Proceed to `/remediate` for open findings, or `/report` if clean.
