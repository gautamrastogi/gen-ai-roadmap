# syntax=docker/dockerfile:1

FROM python:3.11-slim AS builder

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY pyproject.toml .
COPY src/ src/

ENV UV_LINK_MODE=copy
RUN uv sync --no-dev

FROM python:3.11-slim AS runtime

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/src /app/src

ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

RUN useradd --no-create-home --no-log-init appuser
USER appuser

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
