"""Shared test fixtures for P5."""

from src import schemas

TEXT = "FastAPI helps teams build typed Python APIs quickly."


def usage() -> schemas.TokenUsage:
    """Return a small token usage fixture."""

    return schemas.TokenUsage(
        input_tokens_estimated=20,
        output_tokens_estimated=8,
        total_tokens_estimated=28,
        input_tokens_actual=18,
        output_tokens_actual=7,
        total_tokens_actual=25,
    )


def metadata(operation: schemas.OperationName) -> schemas.ResponseMetadata:
    """Return response metadata fixture."""

    return schemas.ResponseMetadata(
        operation=operation,
        model="mock-model",
        adapter="chat",
        provider="mock",
        max_input_tokens=6000,
        budget_ok=True,
    )
