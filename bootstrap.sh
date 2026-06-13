#!/usr/bin/env bash
# bootstrap.sh — one-command setup for compliance-agent-skills
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

echo "==> compliance-agent-skills bootstrap"
echo "    Root: $ROOT"

if [[ -f "$ROOT/scripts/install.sh" ]]; then
  exec bash "$ROOT/scripts/install.sh" "$@"
else
  echo "ERROR: scripts/install.sh not found" >&2
  exit 1
fi
