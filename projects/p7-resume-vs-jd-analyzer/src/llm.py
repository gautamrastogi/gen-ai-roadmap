"""LLM adapters for resume/JD analysis."""

from __future__ import annotations

import dataclasses
import ssl
from typing import Any, cast

import httpx
import openai
import pydantic
import truststore

from src import errors, schemas
from src.settings import Settings

Message = dict[str, str]

_HF_BASE_URL = "https://router.huggingface.co/v1"
_GITHUB_MODELS_BASE_URL = "https://models.inference.ai.azure.com"


@dataclasses.dataclass(frozen=True)
class ActualUsage:
    """Provider-reported token usage."""

    input_tokens: int | None = None
    output_tokens: int | None = None
    total_tokens: int | None = None


@dataclasses.dataclass(frozen=True)
class LLMResult:
    """Model text output plus provider metadata."""

    text: str
    model: str
    usage: ActualUsage | None = None


def _ssl_context() -> ssl.SSLContext:
    """Return an SSL context backed by the OS certificate store."""

    return truststore.SSLContext(ssl.PROTOCOL_TLS_CLIENT)


def _api_key(settings: Settings) -> str:
    """Return API key for the selected provider."""

    if settings.analysis_mode == "responses_schema":
        return settings.openai_api_key.get_secret_value()
    if settings.use_local_or_custom_base_url:
        explicit_key = settings.openai_api_key.get_secret_value().strip()
        return explicit_key or "local-model"
    if settings.use_hf:
        return settings.hf_token.get_secret_value()
    if settings.use_github_models:
        return settings.github_token.get_secret_value()
    return settings.openai_api_key.get_secret_value()


def _base_url(settings: Settings) -> str | None:
    """Return OpenAI-compatible base URL, if any."""

    if settings.analysis_mode == "responses_schema":
        return None
    if settings.use_local_or_custom_base_url:
        return settings.openai_base_url.strip().rstrip("/")
    if settings.use_hf:
        return _HF_BASE_URL
    if settings.use_github_models:
        return _GITHUB_MODELS_BASE_URL
    return None


def make_client(settings: Settings) -> openai.AsyncOpenAI:
    """Create an async OpenAI SDK client."""

    http_client = httpx.AsyncClient(
        verify=_ssl_context(),
        timeout=settings.request_timeout_seconds,
    )
    base_url = _base_url(settings)
    if base_url:
        return openai.AsyncOpenAI(
            api_key=_api_key(settings),
            base_url=base_url,
            http_client=http_client,
            timeout=settings.request_timeout_seconds,
        )
    return openai.AsyncOpenAI(
        api_key=_api_key(settings),
        http_client=http_client,
        timeout=settings.request_timeout_seconds,
    )


async def generate_analysis(
    messages: list[Message],
    mode: schemas.AnalysisMode,
    settings: Settings,
    client: openai.AsyncOpenAI | None = None,
) -> LLMResult:
    """Generate structured analysis text."""

    active_client = client or make_client(settings)
    try:
        if mode == "responses_schema":
            return await _generate_responses_schema(active_client, messages, settings)
        return await _generate_chat(active_client, messages, mode, settings)
    except openai.AuthenticationError as exc:
        raise errors.LLMProviderError("Invalid provider credentials.", str(exc)) from exc
    except openai.RateLimitError as exc:
        raise errors.LLMProviderError("Provider rate limit exceeded.", str(exc)) from exc
    except (openai.APITimeoutError, TimeoutError) as exc:
        raise errors.LLMTimeoutError("Provider request timed out.", str(exc)) from exc
    except openai.APIError as exc:
        raise errors.LLMProviderError("Provider API error.", str(exc)) from exc


async def _generate_chat(
    client: openai.AsyncOpenAI,
    messages: list[Message],
    mode: schemas.AnalysisMode,
    settings: Settings,
) -> LLMResult:
    """Generate through Chat Completions."""

    kwargs: dict[str, Any] = {}
    if mode == "chat_schema":
        kwargs["response_format"] = {
            "type": "json_schema",
            "json_schema": _json_schema_format(schemas.ResumeJdModelOutput, "resume_jd_analysis"),
        }

    response = await client.chat.completions.create(
        model=settings.openai_model,
        messages=messages,  # type: ignore[arg-type]
        max_tokens=settings.max_tokens,
        temperature=settings.temperature,
        **kwargs,
    )
    text = (response.choices[0].message.content or "").strip()
    return LLMResult(text=text, model=response.model, usage=_chat_usage(response))


async def _generate_responses_schema(
    client: openai.AsyncOpenAI,
    messages: list[Message],
    settings: Settings,
) -> LLMResult:
    """Generate through Responses API structured outputs."""

    response = await client.responses.create(
        model=settings.openai_model,
        input=cast(Any, messages),
        max_output_tokens=settings.max_tokens,
        temperature=settings.temperature,
        text=cast(
            Any,
            {
                "format": {
                    "type": "json_schema",
                    **_json_schema_format(schemas.ResumeJdModelOutput, "resume_jd_analysis"),
                }
            },
        ),
    )
    text = str(getattr(response, "output_text", "") or "").strip()
    return LLMResult(
        text=text,
        model=str(getattr(response, "model", settings.openai_model)),
        usage=_responses_usage(response),
    )


def _json_schema_format(
    schema_model: type[pydantic.BaseModel],
    schema_name: str,
) -> dict[str, Any]:
    """Return OpenAI-compatible JSON Schema response format."""

    return {
        "name": schema_name,
        "description": "Evidence-backed resume versus job-description fit analysis.",
        "schema": schema_model.model_json_schema(),
        "strict": True,
    }


def _chat_usage(response: Any) -> ActualUsage | None:
    """Extract usage from Chat Completions response."""

    usage = getattr(response, "usage", None)
    if usage is None:
        return None
    return ActualUsage(
        input_tokens=getattr(usage, "prompt_tokens", None),
        output_tokens=getattr(usage, "completion_tokens", None),
        total_tokens=getattr(usage, "total_tokens", None),
    )


def _responses_usage(response: Any) -> ActualUsage | None:
    """Extract usage from Responses response."""

    usage = getattr(response, "usage", None)
    if usage is None:
        return None
    return ActualUsage(
        input_tokens=getattr(usage, "input_tokens", None),
        output_tokens=getattr(usage, "output_tokens", None),
        total_tokens=getattr(usage, "total_tokens", None),
    )
