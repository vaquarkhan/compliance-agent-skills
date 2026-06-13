# Regulatory report examples

Synthetic findings reports generated from structured YAML. **Not real audit opinions.**

## Generate all samples

```bash
python scripts/generate-regulatory-report.py examples/regulatory-reports/hipaa-llm-intake/findings-input.yaml \
  -o examples/regulatory-reports/hipaa-llm-intake/findings-report.md
```

See [docs/regulatory-reports.md](../../docs/regulatory-reports.md) for the full catalog.

## Layout

Each subdirectory contains:

- `findings-input.yaml` — structured input (fill from `/scope` … `/remediate`)
- `findings-report.md` — generated Markdown (regenerate after editing input)
