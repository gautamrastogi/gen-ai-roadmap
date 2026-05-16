"""Tests for LLM adapters."""

import asyncio
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

from pydantic import SecretStr

from src import llm
from src.settings import Settings


def test_chat_adapter_returns_text_and_usage() -> None:
    settings = Settings(
        openai_base_url="http://127.0.0.1:11434/v1",
        openai_api_key=SecretStr("local-model"),
        openai_model="test-model",
    )
    response = SimpleNamespace(
        choices=[SimpleNamespace(message=SimpleNamespace(content="hello"))],
        model="test-model",
        usage=SimpleNamespace(prompt_tokens=5, completion_tokens=3, total_tokens=8),
    )
    client = MagicMock()
    client.chat.completions.create = AsyncMock(return_value=response)

    result = asyncio.run(llm.generate([{"role": "user", "content": "hi"}], settings, client))

    assert result.text == "hello"
    assert result.model == "test-model"
    assert result.usage is not None
    assert result.usage.total_tokens == 8


def test_responses_adapter_returns_output_text() -> None:
    settings = Settings(
        llm_adapter="responses",
        openai_base_url="",
        openai_api_key=SecretStr("sk-test"),
        openai_model="gpt-test",
    )
    response = SimpleNamespace(
        output_text="responses text",
        model="gpt-test",
        usage=SimpleNamespace(input_tokens=6, output_tokens=4, total_tokens=10),
    )
    client = MagicMock()
    client.responses.create = AsyncMock(return_value=response)

    result = asyncio.run(llm.generate([{"role": "user", "content": "hi"}], settings, client))

    assert result.text == "responses text"
    assert result.usage is not None
    assert result.usage.input_tokens == 6
