"""Summarizer — API runner.

Sends the input text through one or all summarization formats.

Auth priority: HF_TOKEN → OPENAI_API_KEY.
HuggingFace routes via ``router.huggingface.co`` — reachable on corporate networks.
"""

import ssl
import time
import typing

import httpx
import openai
import truststore

from src import prompts
from src.settings import Settings

_HF_BASE_URL = "https://router.huggingface.co/v1"
# 1.5 s pause between calls respects HF burst limit (2 req / 2 s window)
_INTER_CALL_DELAY: float = 1.5


def _ssl_context() -> ssl.SSLContext:
    """Return an SSL context backed by the OS (Windows) certificate store.

    :return: :class:`ssl.SSLContext` backed by ``truststore``.
    """
    return truststore.SSLContext(ssl.PROTOCOL_TLS_CLIENT)


def _make_client(settings: Settings) -> openai.OpenAI:
    """Build an OpenAI-compatible client for whichever auth path is configured.

    :param settings: Validated application settings.
    :return: Configured :class:`openai.OpenAI` client.
    """
    http_client = httpx.Client(verify=_ssl_context())
    if settings.use_hf:
        return openai.OpenAI(
            api_key=settings.hf_token.get_secret_value(),
            base_url=_HF_BASE_URL,
            http_client=http_client,
        )
    return openai.OpenAI(
        api_key=settings.openai_api_key.get_secret_value(),
        http_client=http_client,
    )


def _call(
    client: openai.OpenAI,
    text: str,
    fmt: str,
    settings: Settings,
) -> tuple[str, typing.Optional[dict[str, int]]]:
    """Make a single API call for one output format.

    :param client: Configured OpenAI-compatible client.
    :param text: The input text to summarise.
    :param fmt: Key in :data:`prompts.FORMATS`.
    :param settings: Validated application settings.
    :return: Tuple of (response text, quota dict or None).
    """
    messages = prompts.FORMATS[fmt](text)
    raw = client.with_raw_response.chat.completions.create(
        model=settings.openai_model,
        messages=messages,  # type: ignore[arg-type]
        max_tokens=settings.max_tokens,
        temperature=settings.temperature,
    )
    response = raw.parse()
    result = (response.choices[0].message.content or "").strip()

    quota: typing.Optional[dict[str, int]] = None
    try:
        h = dict(raw.headers)
        if "x-ratelimit-remaining" in h:
            quota = {
                "remaining": int(h.get("x-ratelimit-remaining", -1)),
                "limit": int(h.get("x-ratelimit-limit", -1)),
                "remaining_tokens": int(h.get("x-ratelimit-remaining-tokens", -1)),
                "limit_tokens": int(h.get("x-ratelimit-limit-tokens", -1)),
                "reset_in_s": int(h.get("x-ratelimit-reset", -1)),
            }
    except (ValueError, TypeError):
        pass

    return result, quota


def run_one(
    text: str, fmt: str, settings: Settings
) -> tuple[dict[str, str], typing.Optional[dict[str, int]]]:
    """Run a single output format.

    :param text: Input text to summarise.
    :param fmt: Format name — one of the keys in :data:`prompts.FORMATS`.
    :param settings: Validated application settings.
    :raises KeyError: If ``fmt`` is not a valid format name.
    :return: Tuple of (results dict, quota info).
    """
    if fmt not in prompts.FORMATS:
        raise KeyError(f"Unknown format {fmt!r}. Valid: {list(prompts.FORMATS)}.")
    client = _make_client(settings)
    result, quota = _call(client, text, fmt, settings)
    return {fmt: result}, quota


def run_all(
    text: str, settings: Settings
) -> tuple[dict[str, str], typing.Optional[dict[str, int]]]:
    """Run all three output formats with pacing between calls.

    :param text: Input text to summarise.
    :param settings: Validated application settings.
    :return: Tuple of (results dict, quota info from last call).
    """
    client = _make_client(settings)
    results: dict[str, str] = {}
    quota: typing.Optional[dict[str, int]] = None
    names = list(prompts.FORMATS)
    for i, fmt in enumerate(names):
        result, quota = _call(client, text, fmt, settings)
        results[fmt] = result
        if i < len(names) - 1:
            time.sleep(_INTER_CALL_DELAY)
    return results, quota
