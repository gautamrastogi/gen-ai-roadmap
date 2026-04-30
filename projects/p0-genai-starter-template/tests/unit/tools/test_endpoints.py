"""Unit tests for the /health and /complete FastAPI endpoints."""

import typing
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi.testclient import TestClient
from pydantic import SecretStr

from tests import mocks


@pytest.fixture()
def client() -> typing.Generator[TestClient, None, None]:
    """Return a FastAPI test client with a patched OpenAI client.

    Patches ``openai_client.init`` so no real API key is needed.
    """
    with patch("src.main._settings") as mock_settings, \
         patch("src.main._client") as mock_client:
        mock_settings.app_name = "genai-starter-test"
        mock_settings.openai_model = "gpt-4o-mini"
        mock_settings.openai_api_key = SecretStr("sk-fake")

        # Import app after patching settings
        from src.main import app
        yield TestClient(app)


def test_health_returns_ok(client: TestClient) -> None:
    """GET /health should return HTTP 200 with status 'ok'.

    :param client: Injected FastAPI test client fixture.
    """
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "version" in data
    assert "model" in data
