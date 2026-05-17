"""Tests for extraction schemas."""

import pydantic
import pytest

from src import registry, schemas


def test_registry_lists_supported_schemas() -> None:
    names = [definition.name for definition in registry.list_schemas()]

    assert names == ["invoice", "log_incident", "support_ticket"]


def test_invoice_rejects_extra_fields() -> None:
    payload = _invoice_payload()
    payload["unexpected"] = "nope"

    with pytest.raises(pydantic.ValidationError):
        schemas.Invoice.model_validate(payload)


def test_support_ticket_requires_known_priority() -> None:
    with pytest.raises(pydantic.ValidationError):
        schemas.SupportTicket.model_validate(
            {
                "ticket_id": "INC-1",
                "title": "Broken checkout",
                "requester": "ops",
                "priority": "urgent",
                "category": "incident",
                "affected_services": ["checkout"],
                "summary": "Checkout is failing.",
                "requested_action": "Investigate.",
                "evidence": ["5xx errors"],
            }
        )


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
