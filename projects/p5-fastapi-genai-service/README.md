# P5 - FastAPI GenAI Service

Production-style GenAI backend with four JSON endpoints:

- `POST /summarize`
- `POST /rewrite`
- `POST /classify`
- `POST /extract`

Every GenAI response includes lightweight token economics metadata: estimated tokens, actual provider tokens when available, budget status, warnings, and optional estimated cost.

## Quickstart

```bash
make install

# Local Ollama path
ollama pull qwen2.5:1.5b
make run-ollama
```

Open:

- `http://localhost:8000/docs`
- `http://localhost:8000/health`

For LM Studio, OpenAI, HuggingFace Router, or GitHub Models:

```bash
cp .env.example .env
# Edit .env for your provider
make run
```

## Example Requests

### Summarize

```bash
curl -X POST http://localhost:8000/summarize \
  -H "Content-Type: application/json" \
  -d '{"text":"FastAPI helps teams build typed Python APIs quickly.","format":"paragraph"}'
```

### Rewrite

```bash
curl -X POST http://localhost:8000/rewrite \
  -H "Content-Type: application/json" \
  -d '{"text":"fix this asap because users are blocked","tone":"professional"}'
```

### Classify

```bash
curl -X POST http://localhost:8000/classify \
  -H "Content-Type: application/json" \
  -d '{"text":"Database latency is causing checkout failures.","labels":["incident","request","question"]}'
```

### Extract

```bash
curl -X POST http://localhost:8000/extract \
  -H "Content-Type: application/json" \
  -d '{
    "text":"Server app01 failed at 14:05 UTC with disk full errors.",
    "fields":[
      {"name":"server","description":"Affected host name"},
      {"name":"error","description":"Main failure reason"}
    ]
  }'
```

## Response Shape

```json
{
  "result": "FastAPI is a Python framework for quickly building typed APIs.",
  "usage": {
    "input_tokens_estimated": 42,
    "output_tokens_estimated": 14,
    "total_tokens_estimated": 56,
    "input_tokens_actual": null,
    "output_tokens_actual": null,
    "total_tokens_actual": null,
    "estimated_cost_usd": null
  },
  "metadata": {
    "operation": "summarize",
    "model": "qwen2.5:1.5b",
    "adapter": "chat",
    "provider": "ollama",
    "max_input_tokens": 6000,
    "budget_ok": true,
    "warnings": []
  }
}
```

## Token Budgeting

The service estimates input tokens before calling the model. If a request exceeds `MAX_INPUT_TOKENS` or request-level `max_input_tokens`, the API returns HTTP 422 instead of silently truncating text.

```json
{
  "error": "Input exceeds token budget.",
  "details": "Reduce the input text or increase max_input_tokens.",
  "estimated_input_tokens": 9000,
  "max_input_tokens": 6000,
  "suggestion": "Shorten text or pass a larger max_input_tokens value."
}
```

Optional cost estimate:

```env
INPUT_TOKEN_PRICE_PER_1M=0.15
OUTPUT_TOKEN_PRICE_PER_1M=0.60
```

## Configuration

| Variable | Default | Description |
|---|---:|---|
| `LLM_ADAPTER` | `chat` | `chat` or `responses` |
| `OPENAI_BASE_URL` | `http://127.0.0.1:11434/v1` | OpenAI-compatible base URL |
| `OPENAI_API_KEY` | empty | OpenAI key, or dummy key for local providers |
| `HF_TOKEN` | empty | HuggingFace Router token |
| `GITHUB_TOKEN` | empty | GitHub Models token |
| `MODEL` | `qwen2.5:1.5b` | Model name |
| `TEMPERATURE` | `0.2` | Sampling temperature |
| `MAX_TOKENS` | `700` | Max output tokens |
| `MAX_INPUT_TOKENS` | `6000` | Input token budget |
| `REQUEST_TIMEOUT_SECONDS` | `60` | Provider request timeout |

## Developer Commands

```bash
make install
make fmt
make ci
make run
make run-ollama
make docker-build
```

## Docker

```bash
make docker-build
docker run --rm -p 8000:8000 \
  -e OPENAI_BASE_URL=http://host.docker.internal:11434/v1 \
  -e OPENAI_API_KEY=local-model \
  -e MODEL=qwen2.5:1.5b \
  p5-fastapi-genai-service
```
