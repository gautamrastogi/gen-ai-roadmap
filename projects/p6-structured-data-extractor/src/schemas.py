"""Typed extraction schemas and response models."""

from typing import Any, Literal

import pydantic

ExtractionMode = Literal["prompt", "chat_schema", "responses_schema"]
SchemaName = Literal["invoice", "support_ticket", "log_incident"]
Severity = Literal["info", "warning", "error"]


class StrictModel(pydantic.BaseModel):
    """Base model for extraction targets."""

    model_config = pydantic.ConfigDict(extra="forbid")


class InvoiceItem(StrictModel):
    """One invoice line item."""

    description: str = pydantic.Field(description="Item or service description.")
    quantity: float = pydantic.Field(ge=0, description="Purchased quantity.")
    unit_price: float = pydantic.Field(ge=0, description="Unit price before tax.")
    line_total: float = pydantic.Field(ge=0, description="Quantity multiplied by unit price.")


class Invoice(StrictModel):
    """Structured invoice data extracted from raw text."""

    invoice_number: str | None = pydantic.Field(
        description="Invoice identifier, or null if missing."
    )
    vendor_name: str = pydantic.Field(description="Company or person issuing the invoice.")
    customer_name: str | None = pydantic.Field(description="Bill-to customer, or null if missing.")
    invoice_date: str | None = pydantic.Field(
        description="Invoice date as written or ISO-like text."
    )
    due_date: str | None = pydantic.Field(
        description="Payment due date as written or ISO-like text."
    )
    currency: str = pydantic.Field(description="Three-letter currency code such as EUR or USD.")
    line_items: list[InvoiceItem] = pydantic.Field(description="Invoice line items.")
    subtotal: float | None = pydantic.Field(
        ge=0, description="Subtotal before tax, or null if missing."
    )
    tax: float | None = pydantic.Field(ge=0, description="Tax amount, or null if missing.")
    total: float = pydantic.Field(ge=0, description="Final invoice total.")
    payment_terms: str | None = pydantic.Field(
        description="Payment terms or bank details if present."
    )


class SupportTicket(StrictModel):
    """Structured support ticket data extracted from raw text."""

    ticket_id: str | None = pydantic.Field(description="Ticket or request identifier.")
    title: str = pydantic.Field(description="Short ticket title.")
    requester: str | None = pydantic.Field(description="Requester name, team, or email.")
    priority: Literal["low", "medium", "high", "critical"] = pydantic.Field(
        description="Business priority."
    )
    category: Literal["incident", "service_request", "question", "change"] = pydantic.Field(
        description="Ticket category."
    )
    affected_services: list[str] = pydantic.Field(
        description="Services, apps, or systems affected."
    )
    summary: str = pydantic.Field(description="Concise problem/request summary.")
    requested_action: str | None = pydantic.Field(description="Requested next action, or null.")
    evidence: list[str] = pydantic.Field(
        description="Facts from the text supporting the extraction."
    )


class LogIncident(StrictModel):
    """Structured operational incident data extracted from logs or alerts."""

    service: str | None = pydantic.Field(description="Affected service or application.")
    environment: Literal["dev", "test", "stage", "prod", "unknown"] = pydantic.Field(
        description="Environment inferred from text."
    )
    severity: Literal["low", "medium", "high", "critical"] = pydantic.Field(
        description="Operational severity."
    )
    affected_hosts: list[str] = pydantic.Field(description="Hostnames, pods, or nodes affected.")
    symptoms: list[str] = pydantic.Field(description="Observed symptoms or alerts.")
    suspected_cause: str | None = pydantic.Field(description="Likely cause, or null if unclear.")
    recommended_next_steps: list[str] = pydantic.Field(
        description="Concrete next diagnostic steps."
    )


class ValidationIssue(pydantic.BaseModel):
    """One business validation issue."""

    severity: Severity
    path: str
    message: str


class ValidationReport(pydantic.BaseModel):
    """Business-level validation report for extracted data."""

    valid: bool
    issue_count: int
    issues: list[ValidationIssue]


class TokenUsage(pydantic.BaseModel):
    """Token usage metadata."""

    input_tokens_estimated: int
    output_tokens_estimated: int
    total_tokens_estimated: int
    input_tokens_actual: int | None = None
    output_tokens_actual: int | None = None
    total_tokens_actual: int | None = None


class ExtractionMetadata(pydantic.BaseModel):
    """Non-content metadata for an extraction run."""

    model: str
    provider: str
    schema_name: SchemaName
    mode: ExtractionMode
    max_input_tokens: int
    warnings: list[str] = pydantic.Field(default_factory=list)


class ExtractionResult(pydantic.BaseModel):
    """CLI/API-friendly extraction result."""

    schema_name: SchemaName
    mode: ExtractionMode
    data: dict[str, Any]
    validation_report: ValidationReport
    usage: TokenUsage
    metadata: ExtractionMetadata
