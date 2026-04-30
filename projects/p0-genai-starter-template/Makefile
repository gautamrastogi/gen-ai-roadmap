.PHONY: install fmt fmt-check lint type test run clean help

# Required on OneDrive paths where hardlinks are blocked
export UV_LINK_MODE := copy

UV        := uv
SRC       := src
TESTS     := tests

COLOR_START := \033[0;32m
COLOR_DONE  := \033[0;34m
COLOR_ERROR := \033[0;31m
COLOR_RESET := \033[0m

## help: Show all available targets
help:
	@grep -E '^## ' Makefile | sed 's/## /  /'

## install: Install all dependencies (runtime + dev)
install:
	@printf "$(COLOR_START)▶ Installing dependencies...$(COLOR_RESET)\n"
	$(UV) sync --group dev
	@printf "$(COLOR_DONE)✔ Done.$(COLOR_RESET)\n"

## fmt: Auto-format code with ruff
fmt:
	@printf "$(COLOR_START)▶ Formatting...$(COLOR_RESET)\n"
	$(UV) run ruff format $(SRC) $(TESTS)
	$(UV) run ruff check --fix $(SRC) $(TESTS)
	@printf "$(COLOR_DONE)✔ Done.$(COLOR_RESET)\n"

## fmt-check: Check formatting without modifying files (CI gate)
fmt-check:
	@printf "$(COLOR_START)▶ Checking format...$(COLOR_RESET)\n"
	$(UV) run ruff format --check $(SRC) $(TESTS)
	$(UV) run ruff check $(SRC) $(TESTS)
	@printf "$(COLOR_DONE)✔ Done.$(COLOR_RESET)\n"

## lint: Run ruff linter
lint:
	@printf "$(COLOR_START)▶ Linting...$(COLOR_RESET)\n"
	$(UV) run ruff check $(SRC) $(TESTS)
	@printf "$(COLOR_DONE)✔ Done.$(COLOR_RESET)\n"

## type: Run mypy strict type checking
type:
	@printf "$(COLOR_START)▶ Type checking...$(COLOR_RESET)\n"
	$(UV) run mypy $(SRC)
	@printf "$(COLOR_DONE)✔ Done.$(COLOR_RESET)\n"

## test: Run unit tests with coverage
test:
	@printf "$(COLOR_START)▶ Running tests...$(COLOR_RESET)\n"
	$(UV) run pytest $(TESTS)/unit
	@printf "$(COLOR_DONE)✔ Done.$(COLOR_RESET)\n"

## ci: Full local CI pipeline (fmt-check → lint → type → test)
ci: fmt-check lint type test
	@printf "$(COLOR_DONE)✔ CI passed.$(COLOR_RESET)\n"

## run: Start the FastAPI dev server with hot reload
run:
	@printf "$(COLOR_START)▶ Starting dev server at http://localhost:8000$(COLOR_RESET)\n"
	$(UV) run uvicorn src.main:app --reload --port 8000

## clean: Remove build artifacts and caches
clean:
	@printf "$(COLOR_START)▶ Cleaning...$(COLOR_RESET)\n"
	Remove-Item -Recurse -Force .venv, __pycache__, .pytest_cache, htmlcov, .mypy_cache, .ruff_cache 2>$$null; true
	@printf "$(COLOR_DONE)✔ Done.$(COLOR_RESET)\n"
