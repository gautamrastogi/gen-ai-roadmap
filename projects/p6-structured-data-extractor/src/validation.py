"""Business validation rules for extracted data."""

import math

import pydantic

from src import schemas


def build_validation_report(data: pydantic.BaseModel) -> schemas.ValidationReport:
    """Run business validation for a parsed extraction object."""

    issues: list[schemas.ValidationIssue] = []
    if isinstance(data, schemas.Invoice):
        issues.extend(_invoice_issues(data))
    elif isinstance(data, schemas.SupportTicket):
        issues.extend(_support_ticket_issues(data))
    elif isinstance(data, schemas.LogIncident):
        issues.extend(_log_incident_issues(data))

    return schemas.ValidationReport(
        valid=not any(issue.severity == "error" for issue in issues),
        issue_count=len(issues),
        issues=issues,
    )


def _invoice_issues(invoice: schemas.Invoice) -> list[schemas.ValidationIssue]:
    """Return invoice-specific validation issues."""

    issues: list[schemas.ValidationIssue] = []
    if len(invoice.currency.strip()) != 3:
        issues.append(_issue("error", "currency", "Currency should be a three-letter code."))

    line_total = round(sum(item.line_total for item in invoice.line_items), 2)
    if invoice.subtotal is not None and not _close(line_total, invoice.subtotal):
        issues.append(
            _issue(
                "warning",
                "subtotal",
                f"Line totals sum to {line_total}, but subtotal is {invoice.subtotal}.",
            )
        )

    expected_total = None
    if invoice.subtotal is not None and invoice.tax is not None:
        expected_total = round(invoice.subtotal + invoice.tax, 2)
    elif invoice.subtotal is not None:
        expected_total = round(invoice.subtotal, 2)

    if expected_total is not None and not _close(expected_total, invoice.total):
        issues.append(
            _issue(
                "warning",
                "total",
                f"Expected total is {expected_total}, but extracted total is {invoice.total}.",
            )
        )
    if not invoice.line_items:
        issues.append(_issue("warning", "line_items", "Invoice has no line items."))
    return issues


def _support_ticket_issues(ticket: schemas.SupportTicket) -> list[schemas.ValidationIssue]:
    """Return support-ticket-specific validation issues."""

    issues: list[schemas.ValidationIssue] = []
    if ticket.priority in {"high", "critical"} and not ticket.affected_services:
        issues.append(
            _issue(
                "warning",
                "affected_services",
                "High-priority tickets should identify affected services.",
            )
        )
    if not ticket.evidence:
        issues.append(_issue("warning", "evidence", "No supporting evidence was extracted."))
    return issues


def _log_incident_issues(incident: schemas.LogIncident) -> list[schemas.ValidationIssue]:
    """Return log-incident-specific validation issues."""

    issues: list[schemas.ValidationIssue] = []
    if incident.severity in {"high", "critical"} and not incident.recommended_next_steps:
        issues.append(
            _issue(
                "warning",
                "recommended_next_steps",
                "High-severity incidents should include next diagnostic steps.",
            )
        )
    if incident.environment == "prod" and incident.severity == "low":
        issues.append(
            _issue(
                "warning",
                "severity",
                "Production incidents marked low severity should be double-checked.",
            )
        )
    return issues


def _issue(severity: schemas.Severity, path: str, message: str) -> schemas.ValidationIssue:
    """Create a validation issue."""

    return schemas.ValidationIssue(severity=severity, path=path, message=message)


def _close(left: float, right: float) -> bool:
    """Return whether two money-like values are close enough."""

    return math.isclose(left, right, abs_tol=0.02)
