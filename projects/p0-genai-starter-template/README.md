# GenAI Python Starter Template

> **Project 0 — GenAI Roadmap Phase 0: Software Baseline**  
> A reusable, production-ready FastAPI service skeleton for LLM-powered applications.  
> Clone this as the base for every project in your GenAI roadmap.

---

## What this is

A minimal but production-style Python service that gives you:

- **FastAPI** app with a health check and an LLM completion endpoint
- **Pydantic v2** request/response schemas with full validation
- **OpenAI async client** wired up cleanly via a factory function
- **Structured JSON logging** to stderr (stdout stays clean for the web server)
- **Settings** via `pydantic-settings` — one place, validated at startup, service exits cleanly if env vars are missing
- **Custom error hierarchy** (`AppError`, `LLMError`, `ValidationError`)
- **pytest unit tests** with mocked OpenAI — no real API key needed to run tests
- **ruff** for linting/formatting + **mypy** strict type checking
- **Makefile** as single developer interface (`make run`, `make test`, `make ci`)
- **Multi-stage Dockerfile** — slim runtime image, non-root user

---

## Project structure

```
p0-genai-starter-template/
├── src/
│   ├── main.py                  # FastAPI app + routes
│   ├── settings.py              # Pydantic-Settings: OPENAI_API_KEY, model, log level
│   ├── integrations/
│   │   └── openai_client.py     # init() → openai.AsyncOpenAI
│   ├── models/
│   │   └── schemas.py           # Request/response Pydantic models
│   ├── tools/
│   │   └── llm.py               # Business logic: complete()
│   └── utils/
│       ├── constants.py         # Shared constants
│       ├── errors.py            # AppError, LLMError, ValidationError
│       └── logging_context.py   # JSON logger factory
├── tests/
│   ├── mocks.py                 # Central fixture constants
│   ├── conftest.py              # Shared pytest fixtures
│   └── unit/
│       ├── tools/test_llm.py    # LLM tool tests (mocked OpenAI)
│       ├── tools/test_endpoints.py
│       └── utils/test_errors.py
│       └── utils/test_settings.py
├── docker/
│   └── Dockerfile               # Multi-stage build
├── .env.example                 # Copy to .env and fill in your key
├── pyproject.toml
├── Makefile
└── README.md
```

---

## Quick start

### 1. Clone / copy this template

```bash
cp -r projects/p0-genai-starter-template my-new-project
cd my-new-project
```

### 2. Set up your environment

```bash
cp .env.example .env
# Edit .env — add your OPENAI_API_KEY
```

### 3. Install dependencies

```bash
make install
```

### 4. Run the dev server

```bash
make run
# → http://localhost:8000
# → http://localhost:8000/docs  (Swagger UI)
# → http://localhost:8000/health
```

### 5. Test it

```bash
# Health check
curl http://localhost:8000/health

# LLM completion
curl -X POST http://localhost:8000/complete \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Summarise FastAPI in one sentence."}'
```

---

## Development commands

| Command | What it does |
|---------|-------------|
| `make install` | Install all dependencies |
| `make run` | Start dev server with hot reload |
| `make test` | Run unit tests (no API key needed) |
| `make fmt` | Auto-format with ruff |
| `make lint` | Lint with ruff |
| `make type` | Mypy strict type check |
| `make ci` | Full local CI: fmt-check + lint + type + test |

---

## API endpoints

### `GET /health`
Returns service health status. Use as a liveness probe.

```json
{
  "status": "ok",
  "app": "genai-starter",
  "version": "0.1.0",
  "model": "gpt-4o-mini"
}
```

### `POST /complete`
Send a prompt to the LLM and receive generated text.

**Request:**
```json
{
  "prompt": "Summarise FastAPI in one sentence.",
  "system": "You are a helpful assistant.",
  "max_tokens": 200,
  "temperature": 0.7
}
```

**Response:**
```json
{
  "text": "FastAPI is a modern, high-performance Python web framework...",
  "model": "gpt-4o-mini",
  "usage": {
    "prompt_tokens": 18,
    "completion_tokens": 14,
    "total_tokens": 32
  }
}
```

---

## Environment variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OPENAI_API_KEY` | Yes | — | Your OpenAI API key |
| `OPENAI_MODEL` | No | `gpt-4o-mini` | Model to use for completions |
| `LOG_LEVEL` | No | `INFO` | Logging level |
| `APP_NAME` | No | `genai-starter` | Service name in logs and /health |

---

## Extending this template

This is your **Phase 0 base**. To build the next projects on top of it:

1. Copy this folder
2. Add new Pydantic schemas in `src/models/`
3. Add new business-logic functions in `src/tools/`
4. Add new FastAPI routes in `src/main.py`
5. Add corresponding tests in `tests/unit/`

---

## Coding conventions

This project follows the same conventions as the cloud2_mcp project constitution:

- `import pydantic` module-level, never `from pydantic import ...`
- `import typing` module-level, never `from typing import ...`
- No `from __future__ import annotations`
- No nested functions — use `functools.partial` to bind args
- Module-level `logger` (never `_log`)
- Sphinx-style docstrings on every function
- Full type hints everywhere
- ruff for linting/formatting, mypy strict mode
- Tests mirror source structure
- Central `tests/mocks.py` for all fixture constants

---

*Phase 0 complete → proceed to Phase 1: Foundations*
