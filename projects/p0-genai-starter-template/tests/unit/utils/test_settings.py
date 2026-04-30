"""Unit tests for src.settings.Settings."""

import pytest
from pydantic import SecretStr

from src.settings import Settings


def test_settings_valid() -> None:
    """Settings should load successfully when OPENAI_API_KEY is provided."""
    s = Settings(openai_api_key=SecretStr("sk-test-abc123"))
    assert s.openai_api_key.get_secret_value() == "sk-test-abc123"
    assert s.openai_model == "gpt-4o-mini"
    assert s.log_level == "INFO"


def test_settings_missing_api_key_raises() -> None:
    """Settings should raise ValueError when OPENAI_API_KEY is empty."""
    with pytest.raises(ValueError, match="OPENAI_API_KEY"):
        Settings(openai_api_key=SecretStr(""))


def test_settings_custom_model() -> None:
    """Settings should accept a custom model name."""
    s = Settings(openai_api_key=SecretStr("sk-test"), openai_model="gpt-4o")
    assert s.openai_model == "gpt-4o"
