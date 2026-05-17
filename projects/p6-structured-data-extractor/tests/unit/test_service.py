"""Tests for extraction service flow."""

import asyncio
import json
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest
from pydantic import SecretStr

from src import errors
from src.service import StructuredExtractor
from src.settings import Settings


def test_extract_invoice_with_mocked_llm() -> None:
    settings = Settings(
        extraction_mode="prompt",
        openai_base_url="http://127.0.0.1:11434/v1",
        openai_api_key=SecretStr("local-model"),
        openai_model="test-model",
    )
    client = _mock_client(json.dumps(_invoice_payload()))
    extractor = StructuredExtractor(settings, client)

    result = asyncio.run(extractor.extract("invoice", "Invoice INV-1 from Acme total 121 EUR"))

    assert result.schema_name == "invoice"
    assert result.data["invoice_number"] == "INV-1"
    assert result.validation_report.valid is True
    assert result.usage.total_tokens_actual == 8


def test_extract_raises_on_over_budget_input() -> None:
    settings = Settings(
        extraction_mode="prompt",
        openai_base_url="http://127.0.0.1:11434/v1",
        openai_api_key=SecretStr("local-model"),
        openai_model="test-model",
        max_input_tokens=1,
    )
    extractor = StructuredExtractor(settings, _mock_client(json.dumps(_invoice_payload())))

    with pytest.raises(errors.BudgetExceededError):
        asyncio.run(extractor.extract("invoice", "Invoice INV-1 from Acme total 121 EUR"))


def test_extract_raises_on_invalid_model_json() -> None:
    settings = Settings(
        extraction_mode="prompt",
        openai_base_url="http://127.0.0.1:11434/v1",
        openai_api_key=SecretStr("local-model"),
        openai_model="test-model",
    )
    extractor = StructuredExtractor(settings, _mock_client("not json"))

    with pytest.raises(errors.LLMOutputError):
        asyncio.run(extractor.extract("invoice", "Invoice INV-1 from Acme total 121 EUR"))


def _mock_client(content: str) -> MagicMock:
    response = SimpleNamespace(
        choices=[SimpleNamespace(message=SimpleNamespace(content=content))],
        model="test-model",
        usage=SimpleNamespace(prompt_tokens=5, completion_tokens=3, total_tokens=8),
    )
    client = MagicMock()
    client.chat.completions.create = AsyncMock(return_value=response)
    return client


def _invoice_payload() -> dict[str, object]:
    return {
        "invoice_number": "INV-1",
        "vendor_name": "Acme",
        "customer_name": "Contoso",
        "invoice_date": "2026-05-01",
        "due_date": "2026-05-31",
        "currency": "EUR",
        "line_items": [
            {
                "description": "Support",
                "quantity": 2,
                "unit_price": 50,
                "line_total": 100,
            }
        ],
        "subtotal": 100,
        "tax": 21,
        "total": 121,
        "payment_terms": "Net 30",
    }
