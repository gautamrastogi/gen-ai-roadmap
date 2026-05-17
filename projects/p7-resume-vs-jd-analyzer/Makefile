.PHONY: install fmt lint type test run run-ollama ci help

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

## run: Analyze the sample resume and JD
run:
	$(UV) run python -m src.main --resume examples/resume.txt --jd examples/job-description.txt

## run-ollama: Run against local Ollama using prompt-and-validate mode
run-ollama:
	OPENAI_BASE_URL=http://127.0.0.1:11434/v1 OPENAI_API_KEY=local-model MODEL=$${MODEL:-qwen2.5:1.5b} ANALYSIS_MODE=prompt $(UV) run python -m src.main --resume examples/resume.txt --jd examples/job-description.txt
