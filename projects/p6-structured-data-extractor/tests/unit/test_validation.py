"""Tests for business validation reports."""

from src import schemas, validation


def test_invoice_validation_flags_total_mismatch() -> None:
    invoice = schemas.Invoice.model_validate(
        {
            "invoice_number": "INV-1",
            "vendor_name": "Acme",
            "customer_name": "Contoso",
            "invoice_date": "2026-05-01",
            "due_date": "2026-05-31",
            "currency": "EUR",
            "line_items": [
                {
                    "description": "Support",
                    "quantity": 1,
                    "unit_price": 100,
                    "line_total": 100,
                }
            ],
            "subtotal": 100,
            "tax": 20,
            "total": 999,
            "payment_terms": "Net 30",
        }
    )

    report = validation.build_validation_report(invoice)

    assert report.issue_count == 1
    assert report.issues[0].path == "total"


def test_support_ticket_validation_warns_when_high_priority_has_no_services() -> None:
    ticket = schemas.SupportTicket.model_validate(
        {
            "ticket_id": "INC-1",
            "title": "Checkout down",
            "requester": "ops",
            "priority": "critical",
            "category": "incident",
            "affected_services": [],
            "summary": "Checkout is failing.",
            "requested_action": "Investigate.",
            "evidence": ["5xx errors"],
        }
    )

    report = validation.build_validation_report(ticket)

    assert report.issue_count == 1
    assert report.issues[0].path == "affected_services"
