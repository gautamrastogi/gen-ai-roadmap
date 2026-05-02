#!/usr/bin/env bash
set -euo pipefail

PROVIDER="${1:-${LOCAL_MODEL_PROVIDER:-lmstudio}}"

case "$PROVIDER" in
  lmstudio)
    exec "$(dirname "$0")/ensure_lm_studio.sh"
    ;;
  ollama)
    MODEL="${LOCAL_MODEL_NAME:-qwen3}"
    BASE_URL="${LOCAL_MODEL_BASE_URL:-http://127.0.0.1:11434/v1}"
    if ! command -v ollama >/dev/null 2>&1; then
      echo "Missing Ollama CLI: ollama"
      echo "Install Ollama or use: ./scripts/ensure_local_model.sh lmstudio"
      exit 1
    fi
    if ! curl -fsS --max-time 2 "$BASE_URL/models" >/dev/null 2>&1; then
      echo "Starting Ollama..."
      ollama serve >/tmp/ollama-serve.log 2>&1 &
      for _ in $(seq 1 30); do
        if curl -fsS --max-time 2 "$BASE_URL/models" >/dev/null 2>&1; then
          break
        fi
        sleep 1
      done
    fi
    if ! curl -fsS --max-time 2 "$BASE_URL/models" >/dev/null 2>&1; then
      echo "Ollama did not become ready."
      tail -n 40 /tmp/ollama-serve.log 2>/dev/null || true
      exit 1
    fi
    if ! ollama list | awk -v model="$MODEL" 'NR > 1 && ($1 == model || $1 == model ":latest") { found = 1 } END { exit !found }'; then
      echo "Pulling Ollama model: $MODEL"
      ollama pull "$MODEL"
    fi
    echo "Ollama is ready."
    echo "Base URL: $BASE_URL"
    echo "Model: $MODEL"
    ;;
  *)
    echo "Unknown provider: $PROVIDER"
    echo "Use one of: lmstudio, ollama"
    exit 1
    ;;
esac
