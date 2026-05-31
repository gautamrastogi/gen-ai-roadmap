"""Tests for slash command parsing."""

from src.commands import Command, parse_command


def test_parse_normal_chat_returns_none() -> None:
    assert parse_command("hello there") is None


def test_parse_simple_command() -> None:
    assert parse_command("/stats") == Command(name="stats", args=[])


def test_parse_command_with_quoted_args() -> None:
    assert parse_command('/save "sessions/demo chat.json"') == Command(
        name="save",
        args=["sessions/demo chat.json"],
    )


def test_parse_command_strips_whitespace() -> None:
    assert parse_command("  /persona senior-engineer  ") == Command(
        name="persona",
        args=["senior-engineer"],
    )
