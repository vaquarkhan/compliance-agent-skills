# SOC 2 Evidence Bundle Example

Demonstrates packaging audit artifacts with **SHA-256 integrity hashes** for SOC 2 Type II evidence handoff.

## Structure

```
soc2-evidence-bundle/
├── README.md
└── evidence-manifest.yaml
```

## Usage

1. Copy `evidence-manifest.yaml` as starting point
2. Place artifacts in `evidence/` subdirectory (local, gitignored)
3. Compute hashes:

```bash
sha256sum evidence/* 
```

4. Update manifest `artifacts[].sha256` and `bundle_hash`
5. Hand off to auditor via secure portal

## Skill

Load `soc2-evidence-collection` for full automation patterns.

## Template source

Based on `templates/audit-evidence-manifest.yaml` with SOC 2 TSC control IDs.

## Period

Type II example covers Q2 2026 — adjust dates for your examination window.

## Classification

Mark bundle **Confidential** — do not commit real evidence files to git.
