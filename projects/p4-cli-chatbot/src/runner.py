"""OpenAI-compatible streaming runner."""

import ssl
from collections.abc import Iterator
from typing import cast

import httpx
import openai
import truststore
from openai.types.chat import ChatCompletionChunk

from src.settings import Settings

_HF_BASE_URL = "https://router.huggingface.co/v1"
_GITHUB_MODELS_BASE_URL = "https://models.inference.ai.azure.com"


def _ssl_context() -> ssl.SSLContext:
    """Return an SSL context backed by the OS certificate store."""

    return truststore.SSLContext(ssl.PROTOCOL_TLS_CLIENT)


def _api_key(settings: Settings) -> str:
    """Return the API key for the selected provider."""

    if settings.use_local_or_custom_base_url:
        explicit_key = settings.openai_api_key.get_secret_value().strip()
        return explicit_key or "local-model"
    if settings.use_hf:
        return settings.hf_token.get_secret_value()
    if settings.use_github_models:
        return settings.github_token.get_secret_value()
    return settings.openai_api_key.get_secret_value()


def _base_url(settings: Settings) -> str | None:
    """Return the selected provider base URL, if custom."""

    if settings.use_local_or_custom_base_url:
        return settings.openai_base_url.strip().rstrip("/")
    if settings.use_hf:
        return _HF_BASE_URL
    if settings.use_github_models:
        return _GITHUB_MODELS_BASE_URL
    return None


def make_client(settings: Settings) -> openai.OpenAI:
    """Build an OpenAI-compatible client for the selected provider."""

    http_client = httpx.Client(verify=_ssl_context())
    base_url = _base_url(settings)
    if base_url:
        return openai.OpenAI(
            api_key=_api_key(settings),
            base_url=base_url,
            http_client=http_client,
        )
    return openai.OpenAI(api_key=_api_key(settings), http_client=http_client)


def stream_chat(
    messages: list[dict[str, str]],
    settings: Settings,
    client: openai.OpenAI | None = None,
) -> Iterator[str]:
    """Stream assistant text chunks from an OpenAI-compatible chat endpoint."""

    active_client = client or make_client(settings)
    stream = cast(
        Iterator[ChatCompletionChunk],
        active_client.chat.completions.create(
            model=settings.openai_model,
            messages=messages,  # type: ignore[arg-type]
            max_tokens=settings.max_tokens,
            temperature=settings.temperature,
            stream=True,
        ),
    )
    for event in stream:
        if not event.choices:
            continue
        chunk = event.choices[0].delta.content
        if chunk:
            yield chunk
