"""Unit tests for src.tools.llm.complete."""

import typing
from unittest.mock import AsyncMock, MagicMock, patch

import openai
import pytest

from src.models import schemas
from src.utils import errors
from tests import mocks


def _make_mock_client(response_text: str = "Hello!", model: str = "gpt-4o-mini") -> MagicMock:
    """Build a mock openai.AsyncOpenAI client that returns a fake completion.

    :param response_text: Text the mock LLM will return.
    :param model: Model name the mock will report.
    :return: Configured mock client.
    """
    mock_usage = MagicMock()
    mock_usage.prompt_tokens = 20
    mock_usage.completion_tokens = 10
    mock_usage.total_tokens = 30

    mock_message = MagicMock()
    mock_message.content = response_text

    mock_choice = MagicMock()
    mock_choice.message = mock_message

    mock_response = MagicMock()
    mock_response.choices = [mock_choice]
    mock_response.model = model
    mock_response.usage = mock_usage

    mock_client = MagicMock()
    mock_client.chat = MagicMock()
    mock_client.chat.completions = MagicMock()
    mock_client.chat.completions.create = AsyncMock(return_value=mock_response)
    return mock_client


@pytest.mark.asyncio
async def test_complete_returns_expected_shape() -> None:
    """complete() should return a dict matching CompletionResponse on success."""
    from src.tools.llm import complete

    mock_client = _make_mock_client(
        response_text=mocks.COMPLETION_RESPONSE_EXPECTED["text"],
        model=mocks.COMPLETION_RESPONSE_EXPECTED["model"],
    )
    request = schemas.CompletionRequest(**mocks.COMPLETION_REQUEST)

    result = await complete(client=mock_client, model="gpt-4o-mini", request=request)

    assert result == mocks.COMPLETION_RESPONSE_EXPECTED


@pytest.mark.asyncio
async def test_complete_raises_llm_error_on_auth_failure() -> None:
    """complete() should raise LLMError when OpenAI returns 401."""
    from src.tools.llm import complete

    mock_client = MagicMock()
    mock_client.chat.completions.create = AsyncMock(
        side_effect=openai.AuthenticationError(
            message="Invalid API key",
            response=MagicMock(status_code=401),
            body={"error": {"message": "Invalid API key"}},
        )
    )
    request = schemas.CompletionRequest(**mocks.COMPLETION_REQUEST)

    with pytest.raises(errors.LLMError, match="Invalid OpenAI API key"):
        await complete(client=mock_client, model="gpt-4o-mini", request=request)


@pytest.mark.asyncio
async def test_complete_raises_llm_error_on_rate_limit() -> None:
    """complete() should raise LLMError when OpenAI returns 429."""
    from src.tools.llm import complete

    mock_client = MagicMock()
    mock_client.chat.completions.create = AsyncMock(
        side_effect=openai.RateLimitError(
            message="Rate limit exceeded",
            response=MagicMock(status_code=429),
            body={"error": {"message": "Rate limit exceeded"}},
        )
    )
    request = schemas.CompletionRequest(**mocks.COMPLETION_REQUEST)

    with pytest.raises(errors.LLMError, match="rate limit"):
        await complete(client=mock_client, model="gpt-4o-mini", request=request)
