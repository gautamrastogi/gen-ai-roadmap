#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_PY="$ROOT_DIR/local-agent/.venv/bin/python"
TEST_SCRIPT="$ROOT_DIR/local-agent/test_mcp.py"

if [[ ! -x "$VENV_PY" ]]; then
  echo "Missing venv Python at: $VENV_PY"
  echo "Run: python3 -m venv local-agent/.venv && local-agent/.venv/bin/pip install -r local-agent/requirements.txt"
  exit 1
fi

echo "Running local-agent smoke checks..."
"$VENV_PY" "$TEST_SCRIPT"
echo "All checks completed."
