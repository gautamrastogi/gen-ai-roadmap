"""Shared pytest fixtures for the GenAI Starter Template test suite."""

import pytest
from pydantic import SecretStr

from src.settings import Settings


@pytest.fixture()
def settings() -> Settings:
    """Return a :class:`~src.settings.Settings` instance with dummy test credentials.

    :return: Settings with a fake API key and debug log level.
    """
    return Settings(
        openai_api_key=SecretStr("sk-test-fake-key-for-testing"),
        openai_model="gpt-4o-mini",
        log_level="DEBUG",
        app_name="genai-starter-test",
    )
