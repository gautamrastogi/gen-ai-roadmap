"""Unit tests for src.utils.errors."""

import pytest

from src.utils import errors


def test_app_error_str_with_details() -> None:
    """AppError.__str__ should include details when provided."""
    exc = errors.AppError("Something went wrong", details="extra info")
    assert str(exc) == "Something went wrong: extra info"


def test_app_error_str_without_details() -> None:
    """AppError.__str__ should return only the message when details is empty."""
    exc = errors.AppError("Something went wrong")
    assert str(exc) == "Something went wrong"


def test_llm_error_is_app_error() -> None:
    """LLMError should be a subclass of AppError."""
    exc = errors.LLMError("LLM failed")
    assert isinstance(exc, errors.AppError)


def test_validation_error_is_app_error() -> None:
    """ValidationError should be a subclass of AppError."""
    exc = errors.ValidationError("Bad input")
    assert isinstance(exc, errors.AppError)
