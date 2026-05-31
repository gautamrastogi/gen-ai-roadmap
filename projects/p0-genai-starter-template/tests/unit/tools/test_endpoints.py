"""Unit tests for the /health and /complete FastAPI endpoints."""

import typing

import pytest
from fastapi.testclient import TestClient


@pytest.fixture()
def client(monkeypatch: pytest.MonkeyPatch) -> typing.Generator[TestClient, None, None]:
    """Return a FastAPI test client with a fake API key.

    Only the health route is exercised here, so the client is initialized but
    no real OpenAI API call is made.
    """
    monkeypatch.setenv("OPENAI_API_KEY", "sk-fake")

    # Import app after setting the fake key because settings load at module import time.
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
