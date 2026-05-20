.PHONY: install fmt lint type test run run-ollama ci docker-build help

export UV_LINK_MODE := copy

UV    := uv
SRC   := src
TESTS := tests

## help: Show available targets
help:
	@grep -E '^## ' Makefile | sed 's/## /  /'

## install: Install all dependencies
install:
	$(UV) sync --group dev

## fmt: Format + auto-fix
fmt:
	$(UV) run ruff format $(SRC) $(TESTS)
	$(UV) run ruff check --fix $(SRC) $(TESTS)

## lint: Lint only
lint:
	$(UV) run ruff check $(SRC) $(TESTS)

## type: Type-check
type:
	$(UV) run mypy $(SRC)

## test: Run unit tests
test:
	$(UV) run pytest $(TESTS)/unit -v

## ci: Full local CI (lint -> type -> test)
ci: lint type test

## run: Start FastAPI dev server
run:
	$(UV) run uvicorn src.main:app --reload --port 8000

## run-ollama: Start service configured for local Ollama
run-ollama:
	OPENAI_BASE_URL=http://127.0.0.1:11434/v1 MODEL=$${MODEL:-gemma4:latest} $(UV) run uvicorn src.main:app --reload --port 8000

## docker-build: Build production image
docker-build:
	docker build -f docker/Dockerfile -t p5-fastapi-genai-service .
