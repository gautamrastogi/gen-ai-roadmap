"""Tests for token economics helpers."""

from pydantic import SecretStr

from src import token_usage
from src.settings import Settings


def test_token_estimate_empty_text_is_zero() -> None:
    assert token_usage.estimate_tokens("   ") == 0


def test_message_estimate_includes_overhead() -> None:
    messages = [{"role": "user", "content": "a" * 20}]

    assert token_usage.estimate_messages_tokens(messages) == 9


def test_cost_estimate_uses_configured_prices() -> None:
    settings = Settings(
        openai_api_key=SecretStr("local-model"),
        input_token_price_per_1m=1.0,
        output_token_price_per_1m=2.0,
    )

    assert token_usage.estimate_cost_usd(1_000_000, 500_000, settings) == 2.0


def test_budget_warnings_near_limit() -> None:
    assert token_usage.budget_warnings(90, 100) == [
        "Input is using at least 90% of the configured token budget."
    ]
