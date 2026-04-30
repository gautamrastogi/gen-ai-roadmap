# Copilot Instructions — GenAI Starter Template (and all roadmap projects)

This file governs how GitHub Copilot should behave in this project and all
projects under the GenAI roadmap tracker. These conventions are derived from
the cloud2_mcp project constitution.

---

## Project context

This is a learning project for transitioning from Python Software Engineer to
GenAI / LLM Engineer. Each project under `projects/` corresponds to a phase
in `genai-roadmap.md`. The goal is to build production-quality Python AI
services — not demos.

---

## Non-negotiable coding rules

### Imports
- **NEVER** `from __future__ import annotations` — Python 3.11+ natively supports all union syntax
- **ALWAYS** `import typing` at module level — use `typing.Any`, `typing.Optional`, etc.
- **ALWAYS** `import pydantic` at module level — use `pydantic.Field(description=...)`, `pydantic.BaseModel`
- **NEVER** `from pydantic import Field, BaseModel` etc.
- **NEVER** `from typing import Any, List, Optional` scatter-imports

### Functions
- **NEVER** nested functions (closures) inside other functions
- Use `functools.partial` at the call site instead of nested helpers
- Every function, method, and class attribute **must** have full type hints
- Return type annotations are **required**
- `typing.Any` is allowed but only with a comment explaining why

### Logging
- Module-level logger **always** named `logger`, never `_log`, `log`, or `LOG`
- Pattern: `logger = logging_context.get_logger("genai_starter.<module_path>")`
- **NEVER** `print()` — always use the logger
- All logs go to **stderr** only

### Pydantic models
- Every model field **must** have `pydantic.Field(description=...)`
- Every model **must** have `model_config = pydantic.ConfigDict(extra="ignore")`
- Use `pydantic.SecretStr` for any credential or API key field

### Error handling
- Tools/route handlers **catch** `AppError` subclasses and return structured error dicts
- **Never** let unhandled exceptions propagate to the framework as raw exceptions
- Error response shape: `{"error": "short message", "details": "extended info"}`

### Type annotations
- `typing.TypeVar` is **forbidden** — use `typing.Any` or explicit union types
- Bare `dict` and `list` are **forbidden** — always use `dict[str, typing.Any]`, `list[str]`, etc.

---

## Docstrings

Sphinx-style exclusively. Format:

```python
def my_function(param: str, limit: int = 10) -> list[str]:
    """One-line summary on the same line as the opening quotes.

    :param param: Description of param.
    :param limit: Description of limit.
    :return: Description of what is returned.
    :raises AppError: When something specific goes wrong.
    """
```

Rules:
- Summary on the same line as opening `"""`
- `:param name:` for every parameter
- `:return:` always present
- `:raises ExcType:` for every raised exception
- Module-level docstrings describe the module's responsibility in one sentence

---

## Project structure pattern

Every project follows this layout:

```
project-name/
├── src/
│   ├── main.py              # FastAPI app entry point
│   ├── settings.py          # pydantic-settings: all env vars
│   ├── integrations/        # External service clients (one file per service)
│   │   └── <service>_client.py   # init() → client
│   ├── models/              # Pydantic schemas (request/response shapes)
│   │   └── schemas.py
│   ├── tools/               # Business logic (pure async functions)
│   │   └── <feature>.py
│   └── utils/
│       ├── constants.py
│       ├── errors.py
│       └── logging_context.py
├── tests/
│   ├── mocks.py             # All fixture constants here — never inline in tests
│   ├── conftest.py          # Shared pytest fixtures
│   └── unit/                # Unit tests mirror src/ structure
├── docker/Dockerfile
├── .env.example
├── pyproject.toml
├── Makefile
└── README.md
```

---

## Tests

- **pytest exclusively** — no `unittest`, no `TestCase` classes
- **pytest-asyncio** for async tests — `asyncio_mode = "auto"` in pyproject.toml
- Test files mirror source: `tests/unit/tools/test_llm.py` tests `src/tools/llm.py`
- All shared fixture data lives in `tests/mocks.py` as module-level constants
- `conftest.py` contains pytest fixtures that reference `mocks.py`
- Test assertions: single comprehensive `assert result == expected` — never assert individual dict keys one by one
- Every error path (auth failure, rate limit, unexpected error) **must** have a test

---

## Makefile interface

The Makefile is the single developer interface:

| Target | Purpose |
|--------|---------|
| `make install` | Install all dependencies via uv |
| `make run` | Start dev server |
| `make test` | Run unit tests |
| `make fmt` | Auto-format with ruff |
| `make lint` | Lint with ruff |
| `make type` | mypy strict type check |
| `make ci` | Full local CI gate |

**Always use `uv run <cmd>`** — never invoke Python directly.

---

## Security rules

- API keys **only** from environment variables — never hardcoded
- Credentials **never** appear in log output at any level
- `.env` files are git-ignored; `.env.example` (with placeholders) is committed
- Multi-stage Dockerfile — no build tools in the runtime image
- Non-root user in Docker runtime

---

## AI agent behaviour

When working in this project:

1. **Read before editing** — understand existing code before modifying it
2. **Never invent** file paths, function names, or API shapes — search first
3. **Run tests after changes** — `make test` is the signal that things work
4. **Keep diffs small** — prefer incremental focused changes over large rewrites
5. **No backward-looking comments** — never add comments like "previously this was..."
6. **No placeholder TODOs** — implement it or leave it out

---

## Roadmap tracking

- Progress is tracked in `../../genai-roadmap.md` and `../../dashboard.html`
- When a project is complete, say "mark Project N done" and the roadmap will be updated
- Each project folder name follows the pattern `p<N>-<short-name>`
