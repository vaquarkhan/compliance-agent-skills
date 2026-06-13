#!/usr/bin/env bash
# install.sh — install compliance-agent-skills toolkit with auto tool detection
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

PYTHON=""
for candidate in python3 python; do
  if command -v "$candidate" >/dev/null 2>&1; then
    PYTHON="$candidate"
    break
  fi
done

if [[ -z "$PYTHON" ]]; then
  echo "ERROR: Python 3.11+ required but not found in PATH" >&2
  exit 1
fi

echo "==> Using Python: $($PYTHON --version)"
echo "==> Running install_toolkit.py"

exec "$PYTHON" "$ROOT/scripts/install_toolkit.py" "$@"
