"""Tests for LLM adapter behavior."""

import asyncio
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

from pydantic import SecretStr

from src import llm, schemas
from src.settings import Settings


def test_prompt_mode_uses_chat_without_response_format() -> None:
    settings = Settings(
        extraction_mode="prompt",
        openai_base_url="http://127.0.0.1:11434/v1",
        openai_api_key=SecretStr("local-model"),
        openai_model="test-model",
    )
    client = _mock_chat_client('{"invoice_number": "INV-1"}')

    asyncio.run(
        llm.generate_json(
            [{"role": "user", "content": "hi"}],
            schemas.Invoice,
            "invoice",
            "prompt",
            settings,
            client,
        )
    )

    kwargs = client.chat.completions.create.call_args.kwargs
    assert "response_format" not in kwargs


def test_chat_schema_mode_sends_json_schema_response_format() -> None:
    settings = Settings(
        extraction_mode="chat_schema",
        openai_base_url="http://127.0.0.1:11434/v1",
        openai_api_key=SecretStr("local-model"),
        openai_model="test-model",
    )
    client = _mock_chat_client('{"invoice_number": "INV-1"}')

    asyncio.run(
        llm.generate_json(
            [{"role": "user", "content": "hi"}],
            schemas.Invoice,
            "invoice",
            "chat_schema",
            settings,
            client,
        )
    )

    response_format = client.chat.completions.create.call_args.kwargs["response_format"]
    assert response_format["type"] == "json_schema"
    assert response_format["json_schema"]["name"] == "invoice"
    assert response_format["json_schema"]["strict"] is True


def test_responses_schema_mode_sends_text_format() -> None:
    settings = Settings(
        extraction_mode="responses_schema",
        openai_base_url="",
        openai_api_key=SecretStr("sk-test"),
        openai_model="gpt-test",
    )
    response = SimpleNamespace(
        output_text='{"invoice_number": "INV-1"}',
        model="gpt-test",
        usage=SimpleNamespace(input_tokens=5, output_tokens=3, total_tokens=8),
    )
    client = MagicMock()
    client.responses.create = AsyncMock(return_value=response)

    result = asyncio.run(
        llm.generate_json(
            [{"role": "user", "content": "hi"}],
            schemas.Invoice,
            "invoice",
            "responses_schema",
            settings,
            client,
        )
    )

    text_format = client.responses.create.call_args.kwargs["text"]["format"]
    assert result.text == '{"invoice_number": "INV-1"}'
    assert text_format["type"] == "json_schema"
    assert text_format["name"] == "invoice"
    assert text_format["strict"] is True


def _mock_chat_client(content: str) -> MagicMock:
    response = SimpleNamespace(
        choices=[SimpleNamespace(message=SimpleNamespace(content=content))],
        model="test-model",
        usage=SimpleNamespace(prompt_tokens=5, completion_tokens=3, total_tokens=8),
    )
    client = MagicMock()
    client.chat.completions.create = AsyncMock(return_value=response)
    return client
