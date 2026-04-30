"""Rewriter — API runner.

Sends the input text through one or all rewrite tones.

Auth priority: HF_TOKEN → OPENAI_API_KEY.
HuggingFace routes via ``router.huggingface.co`` — reachable on Danske network.
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
    tone: str,
    settings: Settings,
) -> tuple[str, typing.Optional[dict[str, int]]]:
    """Make a single API call for one rewrite tone.

    :param client: Configured OpenAI-compatible client.
    :param text: The input text to rewrite.
    :param tone: Key in :data:`prompts.TONES`.
    :param settings: Validated application settings.
    :return: Tuple of (rewritten text, quota dict or None).
    """
    messages = prompts.TONES[tone](text)
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
                "requests_remaining": int(h.get("x-ratelimit-remaining", 0)),
                "requests_limit": int(h.get("x-ratelimit-limit", 0)),
                "tokens_remaining": int(h.get("x-ratelimit-remaining-tokens", 0)),
                "tokens_limit": int(h.get("x-ratelimit-limit-tokens", 0)),
                "reset_seconds": int(
                    float(h.get("x-ratelimit-reset-requests", "0").rstrip("s"))
                ),
            }
    except (ValueError, KeyError):
        pass

    return result, quota


def run_one(
    text: str,
    tone: str,
    settings: typing.Optional[Settings] = None,
) -> tuple[dict[str, str], typing.Optional[dict[str, int]]]:
    """Rewrite text in a single tone.

    :param text: Input text.
    :param tone: Tone key from :data:`prompts.TONES`.
    :param settings: Optional pre-built settings (loaded from .env if omitted).
    :return: Tuple of ({tone: rewritten_text}, quota or None).
    """
    cfg = settings or Settings()
    client = _make_client(cfg)
    result, quota = _call(client, text, tone, cfg)
    return {tone: result}, quota


def run_all(
    text: str,
    settings: typing.Optional[Settings] = None,
) -> tuple[dict[str, str], typing.Optional[dict[str, int]]]:
    """Rewrite text in all four tones with rate-limit pacing.

    :param text: Input text.
    :param settings: Optional pre-built settings (loaded from .env if omitted).
    :return: Tuple of ({tone: rewritten_text, ...}, last quota or None).
    """
    cfg = settings or Settings()
    client = _make_client(cfg)
    results: dict[str, str] = {}
    last_quota: typing.Optional[dict[str, int]] = None

    tones = list(prompts.TONES.keys())
    for i, tone in enumerate(tones):
        result, quota = _call(client, text, tone, cfg)
        results[tone] = result
        if quota:
            last_quota = quota
        if i < len(tones) - 1:
            time.sleep(_INTER_CALL_DELAY)

    return results, last_quota
