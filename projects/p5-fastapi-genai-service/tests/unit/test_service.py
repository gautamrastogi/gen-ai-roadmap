"""Tests for service-level behavior."""

import asyncio
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest
from pydantic import SecretStr

from src import errors, schemas
from src.service import GenAIService, _parse_model_json
from src.settings import Settings


def _service_with_text(text: str = "done") -> GenAIService:
    settings = Settings(
        openai_base_url="http://127.0.0.1:11434/v1",
        openai_api_key=SecretStr("local-model"),
        openai_model="mock-model",
    )
    response = SimpleNamespace(
        choices=[SimpleNamespace(message=SimpleNamespace(content=text))],
        model="mock-model",
        usage=SimpleNamespace(prompt_tokens=10, completion_tokens=5, total_tokens=15),
    )
    client = MagicMock()
    client.chat.completions.create = AsyncMock(return_value=response)
    return GenAIService(settings, client)


def test_summarize_returns_usage_metadata() -> None:
    service = _service_with_text("Short summary.")

    result = asyncio.run(service.summarize(schemas.SummarizeRequest(text="Long text.")))

    assert result.result == "Short summary."
    assert result.metadata.operation == "summarize"
    assert result.usage.total_tokens_actual == 15


def test_budget_exceeded_prevents_llm_call() -> None:
    settings = Settings(
        openai_base_url="http://127.0.0.1:11434/v1",
        openai_api_key=SecretStr("local-model"),
        max_input_tokens=1,
    )
    client = MagicMock()
    service = GenAIService(settings, client)

    with pytest.raises(errors.BudgetExceededError):
        asyncio.run(service.summarize(schemas.SummarizeRequest(text="This is too long.")))

    assert not client.chat.completions.create.called


def test_parse_model_json_extracts_object_from_text() -> None:
    parsed = _parse_model_json(
        'Here: {"label": "incident", "confidence": 0.7, "reason": "alert text"}',
        schemas.ClassifyModelOutput,
    )

    assert isinstance(parsed, schemas.ClassifyModelOutput)
    assert parsed.label == "incident"


def test_parse_model_json_rejects_malformed_json() -> None:
    with pytest.raises(errors.LLMOutputError):
        _parse_model_json("not json", schemas.ClassifyModelOutput)
