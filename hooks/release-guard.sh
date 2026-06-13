#!/usr/bin/env bash
# release-guard.sh — block releases when HIGH compliance findings are open
set -euo pipefail

FINDINGS_FILE="${COMPLIANCE_FINDINGS_FILE:-./findings/open-high.json}"

if [[ ! -f "$FINDINGS_FILE" ]]; then
  echo "[release-guard] No findings file — pass"
  exit 0
fi

COUNT=$(python3 -c "
import json, sys
from pathlib import Path
data = json.loads(Path('$FINDINGS_FILE').read_text())
high = [f for f in data.get('findings', []) if f.get('severity') == 'HIGH' and f.get('status') != 'closed']
print(len(high))
")

if [[ "$COUNT" -gt 0 ]]; then
  echo "BLOCK: $COUNT open HIGH compliance finding(s). Resolve before release." >&2
  exit 1
fi

echo "[release-guard] Pass — no open HIGH findings"
exit 0
