"""Prompt Playground — API runner.

Sends a task through every registered strategy and returns results.
Supports three auth paths (checked in priority order):

* **HuggingFace** (``HF_TOKEN``) — calls ``router.huggingface.co``.
  Free tier, reachable on the Danske/Zscaler network.  Default.
* **GitHub Models** (``GITHUB_TOKEN``) — calls ``models.inference.ai.azure.com``.
  Requires a personal github.com PAT (not enterprise GHE).
* **OpenAI direct** (``OPENAI_API_KEY``) — standard ``api.openai.com`` path.
  Home/personal networks only.

All paths use the OpenAI SDK with an OpenAI-compatible endpoint.
"""

import ssl
import time
import typing

import httpx
import openai
import truststore

from src import strategies as strats
from src.settings import Settings

# Seconds to wait between sequential strategy calls.
# HF free tier burst limit: 2 requests per ~2 s window.
_INTER_CALL_DELAY: float = 1.5

_HF_BASE_URL_STR = "https://router.huggingface.co/v1"
_GITHUB_MODELS_BASE_URL = "https://models.inference.ai.azure.com"


def _ssl_context() -> ssl.SSLContext:
    """Return an SSL context that trusts the OS (Windows) certificate store.

    :return: :class:`ssl.SSLContext` backed by ``truststore``.
    """
    return truststore.SSLContext(ssl.PROTOCOL_TLS_CLIENT)


def _make_client(settings: Settings) -> openai.OpenAI:
    """Build an OpenAI-compatible client for whichever auth path is configured.

    Priority: HF_TOKEN → GITHUB_TOKEN → OPENAI_API_KEY.

    :param settings: Validated application settings.
    :return: Configured :class:`openai.OpenAI` client.
    """
    http_client = httpx.Client(verify=_ssl_context())

    if settings.use_hf:
        return openai.OpenAI(
            api_key=settings.hf_token.get_secret_value(),
            base_url=_HF_BASE_URL_STR,
            http_client=http_client,
        )

    if settings.use_copilot:
        return openai.OpenAI(
            api_key=settings.github_token.get_secret_value(),
            base_url=_GITHUB_MODELS_BASE_URL,
            http_client=http_client,
        )

    return openai.OpenAI(
        api_key=settings.openai_api_key.get_secret_value(),
        http_client=http_client,
    )


def _call(
    client: openai.OpenAI, task: str, strategy_name: str, settings: Settings
) -> tuple[str, typing.Optional[dict[str, int]]]:
    """Make a single API call for one strategy.

    Also captures HuggingFace rate-limit headers when available.

    :param client: Configured OpenAI-compatible client.
    :param task: The task string.
    :param strategy_name: Key in :data:`strats.STRATEGIES`.
    :param settings: Validated application settings.
    :return: Tuple of (response text, quota dict or None).
    """
    messages = strats.STRATEGIES[strategy_name](task)
    raw = client.with_raw_response.chat.completions.create(
        model=settings.openai_model,
        messages=messages,  # type: ignore[arg-type]
        max_tokens=settings.max_tokens,
        temperature=settings.temperature,
    )
    response = raw.parse()
    text = (response.choices[0].message.content or "").strip()

    # Extract quota from HF response headers
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

    return text, quota


def run_one(
    task: str, strategy: str, settings: Settings
) -> tuple[dict[str, str], typing.Optional[dict[str, int]]]:
    """Call the API for a single strategy only (saves rate-limit quota).

    :param task: The task string to send to the model.
    :param strategy: Strategy name — one of the keys in :data:`strats.STRATEGIES`.
    :param settings: Validated application settings.
    :raises KeyError: If ``strategy`` is not a valid strategy name.
    :return: Tuple of (results dict, quota info from last call).
    """
    if strategy not in strats.STRATEGIES:
        raise KeyError(
            f"Unknown strategy {strategy!r}. Valid: {list(strats.STRATEGIES)}."
        )
    client = _make_client(settings)
    text, quota = _call(client, task, strategy, settings)
    return {strategy: text}, quota


def run_all(
    task: str, settings: Settings
) -> tuple[dict[str, str], typing.Optional[dict[str, int]]]:
    """Call the API once per strategy and return all responses.

    A :data:`_INTER_CALL_DELAY` second pause is inserted between calls to
    respect the HuggingFace burst limit (2 requests / 2 s window).

    :param task: The task string to send to the model.
    :param settings: Validated application settings.
    :return: Tuple of (results dict, quota info from last call).
    """
    client = _make_client(settings)
    results: dict[str, str] = {}
    quota: typing.Optional[dict[str, int]] = None
    names = list(strats.STRATEGIES)
    for i, name in enumerate(names):
        text, quota = _call(client, task, name, settings)
        results[name] = text
        if i < len(names) - 1:
            time.sleep(_INTER_CALL_DELAY)
    return results, quota
