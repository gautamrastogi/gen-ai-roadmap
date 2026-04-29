#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_DIR="$ROOT_DIR/local-agent/.venv"
PYTHON_BIN="$VENV_DIR/bin/python"
REQ_FILE="$ROOT_DIR/local-agent/requirements.txt"
SERVER_FILE="$ROOT_DIR/local-agent/mcp_server.py"

export WORKSPACE_ROOT="${WORKSPACE_ROOT:-$ROOT_DIR}"
export LM_STUDIO_BASE_URL="${LM_STUDIO_BASE_URL:-http://127.0.0.1:1234}"

if [[ ! -x "$PYTHON_BIN" ]]; then
  echo "Creating virtual environment..."
  python3 -m venv "$VENV_DIR"
fi

echo "Installing/updating local-agent dependencies..."
"$PYTHON_BIN" -m pip install --upgrade pip >/dev/null
"$PYTHON_BIN" -m pip install -r "$REQ_FILE" >/dev/null

echo "Starting MCP server..."
echo "WORKSPACE_ROOT=$WORKSPACE_ROOT"
echo "LM_STUDIO_BASE_URL=$LM_STUDIO_BASE_URL"
exec "$PYTHON_BIN" "$SERVER_FILE"
