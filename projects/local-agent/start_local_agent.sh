#!/usr/bin/env bash
set -euo pipefail

# Get script directory and project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Configurable base directory for MCP server
MCP_BASE_DIR="${MCP_BASE_DIR:-$SCRIPT_DIR}"

VENV_DIR="$MCP_BASE_DIR/.venv"
PYTHON_BIN="$VENV_DIR/bin/python"
REQ_FILE="$MCP_BASE_DIR/requirements.txt"
SERVER_FILE="$MCP_BASE_DIR/mcp_server.py"

export WORKSPACE_ROOT="${WORKSPACE_ROOT:-$PROJECT_ROOT}"
export MCP_BASE_DIR="${MCP_BASE_DIR:-$SCRIPT_DIR}"
export LOCAL_MODEL_BASE_URL="${LOCAL_MODEL_BASE_URL:-${LM_STUDIO_BASE_URL:-http://127.0.0.1:1234}}"

if [[ ! -x "$PYTHON_BIN" ]]; then
  echo "Creating virtual environment..."
  python3 -m venv "$VENV_DIR"
fi

echo "Installing/updating local-agent dependencies..."
"$PYTHON_BIN" -m pip install --upgrade pip >/dev/null
"$PYTHON_BIN" -m pip install -r "$REQ_FILE" >/dev/null

echo "Starting MCP server..."
echo "WORKSPACE_ROOT=$WORKSPACE_ROOT"
echo "LOCAL_MODEL_BASE_URL=$LOCAL_MODEL_BASE_URL"
if [[ -n "${LOCAL_MODEL_NAME:-}" ]]; then
  echo "LOCAL_MODEL_NAME=$LOCAL_MODEL_NAME"
fi
exec "$PYTHON_BIN" "$SERVER_FILE"
