"""Tests for token estimation helpers."""

from src import token_usage


def test_empty_text_has_zero_tokens() -> None:
    assert token_usage.estimate_tokens("") == 0
    assert token_usage.estimate_tokens("   ") == 0


def test_non_empty_text_has_at_least_one_token() -> None:
    assert token_usage.estimate_tokens("hi") == 1


def test_token_estimate_scales_with_length() -> None:
    assert token_usage.estimate_tokens("a" * 20) == 5


def test_message_token_estimate_includes_overhead() -> None:
    messages = [
        {"role": "system", "content": "hello"},
        {"role": "user", "content": "a" * 20},
    ]

    assert token_usage.estimate_messages_tokens(messages) == 15
