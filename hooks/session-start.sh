#!/usr/bin/env bash
# session-start.sh — initialize compliance agent session context
set -euo pipefail

export COMPLIANCE_AGENT_ROOT="${COMPLIANCE_AGENT_ROOT:-$(cd "$(dirname "$0")/.." && pwd)}"
export COMPLIANCE_PHI_REDACTION="${COMPLIANCE_PHI_REDACTION:-required}"
export COMPLIANCE_AUDIT_MODE="${COMPLIANCE_AUDIT_MODE:-false}"

if [[ -z "${COMPLIANCE_ENGAGEMENT_ID:-}" ]]; then
  export COMPLIANCE_ENGAGEMENT_ID="ENG-$(date -u +%Y%m%d)-local"
fi

echo "[compliance-agent] Session started"
echo "  root:          $COMPLIANCE_AGENT_ROOT"
echo "  engagement:    $COMPLIANCE_ENGAGEMENT_ID"
echo "  phi_redaction: $COMPLIANCE_PHI_REDACTION"
echo "  audit_mode:    $COMPLIANCE_AUDIT_MODE"

if [[ "$COMPLIANCE_PHI_REDACTION" == "required" ]]; then
  if ! python3 -c "import presidio_analyzer" 2>/dev/null; then
    echo "WARN: Presidio not installed — run pip install -r requirements.txt" >&2
  fi
fi

exit 0
