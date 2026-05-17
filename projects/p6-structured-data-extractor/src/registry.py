"""Registry of supported extraction schemas."""

import dataclasses

import pydantic

from src import schemas


@dataclasses.dataclass(frozen=True)
class SchemaDefinition:
    """Metadata for one supported schema."""

    name: schemas.SchemaName
    title: str
    description: str
    model: type[pydantic.BaseModel]


SCHEMAS: dict[str, SchemaDefinition] = {
    "invoice": SchemaDefinition(
        name="invoice",
        title="Invoice",
        description="Vendor invoice with line items, totals, tax, payment terms, and dates.",
        model=schemas.Invoice,
    ),
    "support_ticket": SchemaDefinition(
        name="support_ticket",
        title="Support Ticket",
        description="Support or workflow ticket with priority, category, impacted services, and action.",
        model=schemas.SupportTicket,
    ),
    "log_incident": SchemaDefinition(
        name="log_incident",
        title="Log Incident",
        description="Operational log or alert text with severity, symptoms, hosts, and next steps.",
        model=schemas.LogIncident,
    ),
}


def list_schemas() -> list[SchemaDefinition]:
    """Return supported schemas in stable order."""

    return [SCHEMAS[name] for name in sorted(SCHEMAS)]


def get_schema(name: str) -> SchemaDefinition:
    """Return schema metadata by name."""

    try:
        return SCHEMAS[name]
    except KeyError as exc:
        supported = ", ".join(sorted(SCHEMAS))
        raise ValueError(f"Unknown schema {name!r}. Supported schemas: {supported}.") from exc
