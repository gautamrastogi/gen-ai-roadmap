"""Rewriter — prompt builders.

Each function takes the input text and returns a list of OpenAI chat messages
instructing the model to rewrite the text in a specific tone.

Tones
-----
- ``professional`` — formal, authoritative business language.
- ``concise``      — maximum information density, no filler.
- ``technical``    — precise terminology, structured prose.
- ``friendly``     — warm, conversational, approachable.
"""

import typing

Message = dict[str, str]

_REWRITE_USER_TMPL = "Rewrite the following text:\n\n{text}"


def professional(text: str) -> list[Message]:
    """Build a prompt that rewrites the text in a professional business tone.

    :param text: The text to rewrite.
    :return: List of chat messages.
    """
    return [
        {
            "role": "system",
            "content": (
                "You are a professional business writer. "
                "Rewrite the provided text in a formal, authoritative tone suitable for "
                "executive communications or official documents. "
                "Use complete sentences, avoid contractions, and favour precise vocabulary. "
                "Output only the rewritten text — no commentary, no headings."
            ),
        },
        {"role": "user", "content": _REWRITE_USER_TMPL.format(text=text)},
    ]


def concise(text: str) -> list[Message]:
    """Build a prompt that rewrites the text as densely as possible.

    :param text: The text to rewrite.
    :return: List of chat messages.
    """
    return [
        {
            "role": "system",
            "content": (
                "You are an editor who specialises in concise writing. "
                "Rewrite the provided text by removing all filler words, redundancy, and padding "
                "while preserving every key fact. "
                "Aim for the shortest possible prose without losing meaning. "
                "Output only the rewritten text — no commentary, no headings."
            ),
        },
        {"role": "user", "content": _REWRITE_USER_TMPL.format(text=text)},
    ]


def technical(text: str) -> list[Message]:
    """Build a prompt that rewrites the text with technical precision.

    :param text: The text to rewrite.
    :return: List of chat messages.
    """
    return [
        {
            "role": "system",
            "content": (
                "You are a technical writer. "
                "Rewrite the provided text using domain-accurate terminology, active voice, "
                "and a structured, logical flow. "
                "Avoid jargon that is not standard in the field, but do not simplify concepts. "
                "Output only the rewritten text — no commentary, no headings."
            ),
        },
        {"role": "user", "content": _REWRITE_USER_TMPL.format(text=text)},
    ]


def friendly(text: str) -> list[Message]:
    """Build a prompt that rewrites the text in a warm, conversational tone.

    :param text: The text to rewrite.
    :return: List of chat messages.
    """
    return [
        {
            "role": "system",
            "content": (
                "You are a friendly communicator. "
                "Rewrite the provided text in a warm, conversational tone — as if explaining "
                "to a curious colleague over coffee. "
                "Use contractions where natural, keep sentences short, and be encouraging. "
                "Output only the rewritten text — no commentary, no headings."
            ),
        },
        {"role": "user", "content": _REWRITE_USER_TMPL.format(text=text)},
    ]


# Registry — maps tone name → prompt builder
TONES: dict[str, typing.Callable[[str], list[Message]]] = {
    "professional": professional,
    "concise": concise,
    "technical": technical,
    "friendly": friendly,
}
