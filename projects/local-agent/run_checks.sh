#!/usr/bin/env bash
set -euo pipefail

# Get script directory and project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Configurable base directory for MCP server
MCP_BASE_DIR="${MCP_BASE_DIR:-$SCRIPT_DIR}"

VENV_PY="$MCP_BASE_DIR/.venv/bin/python"
TEST_SCRIPT="$MCP_BASE_DIR/test_mcp.py"

if [[ ! -x "$VENV_PY" ]]; then
  echo "Missing venv Python at: $VENV_PY"
  echo "Run: python3 -m venv $MCP_BASE_DIR/.venv && $MCP_BASE_DIR/.venv/bin/pip install -r $MCP_BASE_DIR/requirements.txt"
  exit 1
fi

echo "Running local-agent smoke checks..."
"$VENV_PY" "$TEST_SCRIPT"
"$VENV_PY" -m unittest "$MCP_BASE_DIR/test_roadmap_agent.py"
echo "All checks completed."
