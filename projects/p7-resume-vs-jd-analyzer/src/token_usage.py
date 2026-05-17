"""Token estimation helpers."""

from collections.abc import Iterable

Message = dict[str, str]


def estimate_tokens(text: str) -> int:
    """Estimate token count with a simple chars-per-token rule."""

    stripped = text.strip()
    if not stripped:
        return 0
    return max(1, (len(stripped) + 3) // 4)


def estimate_messages_tokens(messages: Iterable[Message]) -> int:
    """Estimate chat message tokens with a small per-message overhead."""

    total = 0
    for message in messages:
        total += 4
        total += estimate_tokens(message.get("content", ""))
    return total


def budget_warnings(input_tokens: int, max_input_tokens: int) -> list[str]:
    """Return warnings for prompts close to the input budget."""

    if max_input_tokens <= 0:
        return []
    ratio = input_tokens / max_input_tokens
    if ratio >= 0.9:
        return ["Input is using at least 90% of the configured token budget."]
    if ratio >= 0.8:
        return ["Input is using at least 80% of the configured token budget."]
    return []
