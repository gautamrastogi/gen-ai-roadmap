"""Summarizer — prompt builders.

Each function takes the input text and returns a list of OpenAI chat messages.

Formats
-------
- ``summary``      — concise paragraph (3-5 sentences).
- ``bullets``      — 5 key bullet points.
- ``action_items`` — numbered action items extracted from the text.
"""

import typing

Message = dict[str, str]


def summary(text: str) -> list[Message]:
    """Build a prompt that produces a concise paragraph summary.

    :param text: The text to summarise.
    :return: List of chat messages.
    """
    return [
        {
            "role": "system",
            "content": (
                "You are a precise summarizer. "
                "Respond with a single paragraph of 3-5 sentences that captures the key points. "
                "No bullet points. No headings. Plain prose only."
            ),
        },
        {"role": "user", "content": f"Summarise the following text:\n\n{text}"},
    ]


def bullets(text: str) -> list[Message]:
    """Build a prompt that extracts exactly 5 key bullet points.

    :param text: The text to summarise.
    :return: List of chat messages.
    """
    return [
        {
            "role": "system",
            "content": (
                "You are a precise summarizer. "
                "Respond with exactly 5 bullet points (each starting with '• '). "
                "Each bullet must be one concise sentence. No intro, no outro."
            ),
        },
        {
            "role": "user",
            "content": f"Extract the 5 key points from the following text:\n\n{text}",
        },
    ]


def action_items(text: str) -> list[Message]:
    """Build a prompt that extracts numbered action items.

    :param text: The text to analyse.
    :return: List of chat messages.
    """
    return [
        {
            "role": "system",
            "content": (
                "You are an assistant that extracts actionable tasks. "
                "Respond with a numbered list of concrete action items implied by the text. "
                "If there are no action items, respond with '1. No action items identified.' "
                "No intro, no outro."
            ),
        },
        {
            "role": "user",
            "content": f"Extract action items from the following text:\n\n{text}",
        },
    ]


# Registry — maps format name → prompt builder
FORMATS: dict[str, typing.Callable[[str], list[Message]]] = {
    "summary": summary,
    "bullets": bullets,
    "action_items": action_items,
}
