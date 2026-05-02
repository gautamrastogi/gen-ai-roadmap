#!/usr/bin/env bash
set -euo pipefail

LM_STUDIO_BASE_URL="${LM_STUDIO_BASE_URL:-http://127.0.0.1:1234}"
LOCAL_MODEL_BASE_URL="${LOCAL_MODEL_BASE_URL:-$LM_STUDIO_BASE_URL}"
LM_STUDIO_MODEL="${LM_STUDIO_MODEL:-qwen/qwen3.5-9b}"
LOCAL_MODEL_NAME="${LOCAL_MODEL_NAME:-$LM_STUDIO_MODEL}"
LM_STUDIO_CONTEXT_LENGTH="${LM_STUDIO_CONTEXT_LENGTH:-4096}"
LM_STUDIO_START_TIMEOUT_SECONDS="${LM_STUDIO_START_TIMEOUT_SECONDS:-45}"

PORT="${LOCAL_MODEL_BASE_URL##*:}"
PORT="${PORT%%/*}"

if ! command -v lms >/dev/null 2>&1; then
  echo "Missing LM Studio CLI: lms"
  echo "Open LM Studio once and install/enable the CLI from the app."
  exit 1
fi

has_models_endpoint() {
  curl -fsS --max-time 2 "$LOCAL_MODEL_BASE_URL/v1/models" >/dev/null 2>&1
}

echo "Checking LM Studio daemon..."
if ! lms daemon status >/dev/null 2>&1; then
  echo "Starting LM Studio daemon..."
  lms daemon up >/dev/null 2>&1 || true
fi

if ! has_models_endpoint; then
  echo "Starting LM Studio server on $LOCAL_MODEL_BASE_URL..."
  lms server start -p "$PORT" >/tmp/lms-server-start.log 2>&1 &
  server_pid=$!

  for _ in $(seq 1 "$LM_STUDIO_START_TIMEOUT_SECONDS"); do
    if has_models_endpoint; then
      break
    fi
    sleep 1
  done

  if ! has_models_endpoint; then
    kill "$server_pid" >/dev/null 2>&1 || true
    echo "LM Studio server did not become ready."
    echo "Last lms output:"
    tail -n 40 /tmp/lms-server-start.log 2>/dev/null || true
    echo
    echo "Manual fallback: open LM Studio, start the local server on port $PORT, then rerun this script."
    exit 1
  fi
fi

if ! lms ls 2>/dev/null | grep -F "$LOCAL_MODEL_NAME" | grep -F "LOADED" >/dev/null 2>&1; then
  echo "Loading model: $LOCAL_MODEL_NAME"
  lms load "$LOCAL_MODEL_NAME" --context-length "$LM_STUDIO_CONTEXT_LENGTH" --yes
fi

echo "Verifying local model API..."
curl -fsS --max-time 5 "$LOCAL_MODEL_BASE_URL/v1/models" >/dev/null

echo "LM Studio is ready."
echo "Base URL: $LOCAL_MODEL_BASE_URL"
echo "Model: $LOCAL_MODEL_NAME"
