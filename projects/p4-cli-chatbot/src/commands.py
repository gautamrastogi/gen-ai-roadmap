"""Slash command parsing for the chatbot CLI."""

import dataclasses
import shlex


@dataclasses.dataclass(frozen=True)
class Command:
    """Parsed slash command."""

    name: str
    args: list[str]


def parse_command(text: str) -> Command | None:
    """Parse a slash command, returning None for normal chat text."""

    stripped = text.strip()
    if not stripped.startswith("/"):
        return None
    parts = shlex.split(stripped)
    if not parts:
        return None
    return Command(name=parts[0][1:].lower(), args=parts[1:])
