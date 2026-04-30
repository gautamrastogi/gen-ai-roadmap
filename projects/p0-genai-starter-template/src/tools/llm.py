"""GenAI Starter Template — LLM tool functions.

All business logic for calling the LLM lives here.
FastAPI route handlers import from this module.

Tool functions accept an ``openai.AsyncOpenAI`` client directly — they never
create their own clients and never access settings directly.
"""

import typing

import openai

from src.models import schemas
from src.utils import constants, errors, logging_context

logger = logging_context.get_logger("genai_starter.tools.llm")


async def complete(
    client: openai.AsyncOpenAI,
    model: str,
    request: schemas.CompletionRequest,
) -> dict[str, typing.Any]:
    """Send a prompt to the LLM and return the generated text.

    :param client: Authenticated :class:`openai.AsyncOpenAI` client.
    :param model: OpenAI model name (e.g. ``"gpt-4o-mini"``).
    :param request: Validated :class:`~src.models.schemas.CompletionRequest`.
    :return: Dict matching :class:`~src.models.schemas.CompletionResponse` on
        success, or ``{"error": ..., "details": ...}`` on failure.
    """
    logger.debug("LLM complete called", extra={"model": model, "max_tokens": request.max_tokens})

    try:
        response = await client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": request.system},
                {"role": "user", "content": request.prompt},
            ],
            max_tokens=request.max_tokens,
            temperature=request.temperature,
        )

        text = response.choices[0].message.content or ""
        usage: dict[str, typing.Any] = {}
        if response.usage:
            usage = {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens,
            }

        result = schemas.CompletionResponse(text=text, model=response.model, usage=usage)
        logger.debug("LLM complete success", extra={"total_tokens": usage.get("total_tokens")})
        return result.model_dump()

    except openai.AuthenticationError as exc:
        logger.error("OpenAI authentication failed", exc_info=True)
        raise errors.LLMError("Invalid OpenAI API key", details=str(exc)) from exc
    except openai.RateLimitError as exc:
        logger.error("OpenAI rate limit hit", exc_info=True)
        raise errors.LLMError("OpenAI rate limit exceeded", details=str(exc)) from exc
    except openai.APIError as exc:
        logger.error("OpenAI API error", exc_info=True)
        raise errors.LLMError("OpenAI API error", details=str(exc)) from exc
