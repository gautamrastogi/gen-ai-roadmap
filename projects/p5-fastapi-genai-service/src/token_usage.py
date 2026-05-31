"""Token estimation and lightweight cost helpers."""

from collections.abc import Iterable

from src.settings import Settings

Message = dict[str, str]


def estimate_tokens(text: str) -> int:
    """Estimate token count with a conservative chars-per-token rule."""

    stripped = text.strip()
    if not stripped:
        return 0
    return max(1, (len(stripped) + 3) // 4)


def estimate_messages_tokens(messages: Iterable[Message]) -> int:
    """Estimate tokens for chat messages, including small per-message overhead."""

    total = 0
    for message in messages:
        total += 4
        total += estimate_tokens(message.get("content", ""))
    return total


def estimate_cost_usd(
    input_tokens: int,
    output_tokens: int,
    settings: Settings,
) -> float | None:
    """Estimate request cost when token price settings are configured."""

    if settings.input_token_price_per_1m is None or settings.output_token_price_per_1m is None:
        return None
    cost = (input_tokens / 1_000_000) * settings.input_token_price_per_1m + (
        output_tokens / 1_000_000
    ) * settings.output_token_price_per_1m
    return round(cost, 8)


def budget_warnings(input_tokens: int, max_input_tokens: int) -> list[str]:
    """Return warnings when the prompt is close to the input budget."""

    if max_input_tokens <= 0:
        return []
    ratio = input_tokens / max_input_tokens
    if ratio >= 0.9:
        return ["Input is using at least 90% of the configured token budget."]
    if ratio >= 0.8:
        return ["Input is using at least 80% of the configured token budget."]
    return []
