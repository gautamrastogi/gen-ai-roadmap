"""Tests for request/response schemas."""

import pydantic
import pytest

from src import schemas


def test_classify_request_rejects_duplicate_labels() -> None:
    with pytest.raises(pydantic.ValidationError):
        schemas.ClassifyRequest(text="hello", labels=["incident", "Incident"])


def test_classify_request_requires_two_labels() -> None:
    with pytest.raises(pydantic.ValidationError):
        schemas.ClassifyRequest(text="hello", labels=["incident"])


def test_extract_request_rejects_duplicate_fields() -> None:
    with pytest.raises(pydantic.ValidationError):
        schemas.ExtractRequest(
            text="Server abc failed.",
            fields=[
                schemas.FieldDefinition(name="server"),
                schemas.FieldDefinition(name="Server"),
            ],
        )


def test_error_response_accepts_budget_details() -> None:
    response = schemas.ErrorResponse(
        error="Input exceeds token budget.",
        estimated_input_tokens=100,
        max_input_tokens=50,
        suggestion="Shorten text.",
    )

    assert response.estimated_input_tokens == 100
    assert response.max_input_tokens == 50
