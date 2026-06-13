#!/usr/bin/env bash
# phi-redaction-guard.sh — enforce PHI redaction before agent prompts
set -euo pipefail

if [[ "${COMPLIANCE_PHI_REDACTION:-required}" != "required" ]]; then
  exit 0
fi

# Cursor hook: read prompt from stdin if piped
PROMPT=""
if [[ ! -t 0 ]]; then
  PROMPT="$(cat)"
fi

ROOT="${COMPLIANCE_AGENT_ROOT:-$(cd "$(dirname "$0")/.." && pwd)}"

if ! python3 -c "import presidio_analyzer" 2>/dev/null; then
  echo "BLOCK: PHI redaction required but Presidio not installed." >&2
  echo "Run: pip install -r $ROOT/requirements.txt" >&2
  exit 1
fi

# Optional: warn on high-risk patterns even before Presidio pass
if echo "$PROMPT" | grep -qE '\b([0-9]{3}-[0-9]{2}-[0-9]{4}|[0-9]{16})\b'; then
  echo "WARN: Prompt may contain SSN or PAN-like data — ensure Presidio redaction active." >&2
fi

exit 0
