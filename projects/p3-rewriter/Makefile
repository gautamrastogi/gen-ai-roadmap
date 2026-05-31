.PHONY: install fmt lint type test run ci help

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

## ci: Full local CI (lint → type → test)
ci: lint type test

## run: Rewrite sample.txt in all four tones
run:
	$(UV) run python -m src.main --file sample.txt
