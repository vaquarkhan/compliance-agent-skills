#!/usr/bin/env bash
# audit-mode.sh — enable read-only compliance audit mode
set -euo pipefail

export COMPLIANCE_AUDIT_MODE=true
export COMPLIANCE_PHI_REDACTION=required
export COMPLIANCE_EVIDENCE_DIR="${COMPLIANCE_EVIDENCE_DIR:-./evidence-bundle}"

mkdir -p "$COMPLIANCE_EVIDENCE_DIR"

echo "[compliance-agent] Audit mode ENABLED"
echo "  evidence_dir: $COMPLIANCE_EVIDENCE_DIR"
echo "  MCP write tools: DISABLED (policy)"
echo "  Use /evidence lifecycle command for artifact collection"

# Reminder for operators
cat <<'EOF'
Audit mode checklist:
  - Playwright: snapshot only, no form submit
  - Postgres: read-only role
  - GitHub: read token only
  - Terraform: plan/drift only, no apply
EOF

exit 0
