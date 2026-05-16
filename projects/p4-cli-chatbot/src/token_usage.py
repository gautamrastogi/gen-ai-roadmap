"""Small token accounting helpers.

This project intentionally avoids a tokenizer dependency. The estimates are
good enough for a CLI usage meter, and API-reported usage can replace them in a
future production version.
"""

from collections.abc import Iterable


def estimate_tokens(text: str) -> int:
    """Estimate token count for text with a conservative chars-per-token rule."""

    stripped = text.strip()
    if not stripped:
        return 0
    return max(1, (len(stripped) + 3) // 4)


def estimate_messages_tokens(messages: Iterable[dict[str, str]]) -> int:
    """Estimate tokens for chat messages, including small per-message overhead."""

    total = 0
    for message in messages:
        total += 4
        total += estimate_tokens(message.get("content", ""))
    return total
