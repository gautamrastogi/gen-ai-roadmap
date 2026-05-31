"""Tests for FastAPI endpoints with mocked service calls."""

from fastapi.testclient import TestClient

from src import schemas
from src.main import app
from tests import mocks


class FakeService:
    """Async fake service for endpoint tests."""

    async def summarize(self, _: schemas.SummarizeRequest) -> schemas.TextOperationResponse:
        return schemas.TextOperationResponse(
            result="summary",
            usage=mocks.usage(),
            metadata=mocks.metadata("summarize"),
        )

    async def rewrite(self, _: schemas.RewriteRequest) -> schemas.TextOperationResponse:
        return schemas.TextOperationResponse(
            result="rewritten",
            usage=mocks.usage(),
            metadata=mocks.metadata("rewrite"),
        )

    async def classify(self, _: schemas.ClassifyRequest) -> schemas.ClassifyResponse:
        return schemas.ClassifyResponse(
            label="incident",
            confidence=0.9,
            reason="It describes an outage.",
            usage=mocks.usage(),
            metadata=mocks.metadata("classify"),
        )

    async def extract(self, _: schemas.ExtractRequest) -> schemas.ExtractResponse:
        return schemas.ExtractResponse(
            fields={
                "server": schemas.ExtractedField(
                    value="app01",
                    confidence=0.9,
                    evidence="server app01",
                )
            },
            usage=mocks.usage(),
            metadata=mocks.metadata("extract"),
        )


def test_health_returns_configuration() -> None:
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_summarize_endpoint(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    monkeypatch.setattr("src.main._service", FakeService())
    client = TestClient(app)

    response = client.post("/summarize", json={"text": mocks.TEXT, "format": "paragraph"})

    assert response.status_code == 200
    assert response.json()["result"] == "summary"


def test_rewrite_endpoint(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    monkeypatch.setattr("src.main._service", FakeService())
    client = TestClient(app)

    response = client.post("/rewrite", json={"text": mocks.TEXT, "tone": "friendly"})

    assert response.status_code == 200
    assert response.json()["metadata"]["operation"] == "rewrite"


def test_classify_endpoint(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    monkeypatch.setattr("src.main._service", FakeService())
    client = TestClient(app)

    response = client.post(
        "/classify",
        json={"text": mocks.TEXT, "labels": ["incident", "request"]},
    )

    assert response.status_code == 200
    assert response.json()["label"] == "incident"


def test_extract_endpoint(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    monkeypatch.setattr("src.main._service", FakeService())
    client = TestClient(app)

    response = client.post(
        "/extract",
        json={"text": "server app01 failed", "fields": [{"name": "server"}]},
    )

    assert response.status_code == 200
    assert response.json()["fields"]["server"]["value"] == "app01"


def test_invalid_classify_labels_returns_422() -> None:
    client = TestClient(app)

    response = client.post("/classify", json={"text": "hello", "labels": ["only-one"]})

    assert response.status_code == 422
    assert response.json()["error"] == "validation_error"
