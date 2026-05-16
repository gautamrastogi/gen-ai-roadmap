"""Tests for CLI entrypoint helpers."""

import argparse
from collections.abc import Iterator

import pytest

from src import main


@pytest.fixture
def empty_provider_env(monkeypatch: pytest.MonkeyPatch) -> Iterator[None]:
    """Remove provider env vars so tests prove CLI flags are enough."""

    for key in (
        "OPENAI_BASE_URL",
        "OPENAI_API_KEY",
        "HF_TOKEN",
        "GITHUB_TOKEN",
        "MODEL",
        "OPENAI_MODEL",
    ):
        monkeypatch.delenv(key, raising=False)
    yield


def test_load_settings_accepts_cli_base_url_without_env(empty_provider_env: None) -> None:
    args = argparse.Namespace(
        model="local-model",
        temperature=None,
        max_tokens=None,
        base_url="http://127.0.0.1:1234/v1",
    )

    settings = main._load_settings(args)

    assert settings.openai_model == "local-model"
    assert settings.openai_base_url == "http://127.0.0.1:1234/v1"
