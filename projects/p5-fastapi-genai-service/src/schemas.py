"""Pydantic request and response schemas for the P5 API."""

from typing import Literal

import pydantic

SummaryFormat = Literal["paragraph", "bullets", "action_items"]
RewriteTone = Literal["professional", "concise", "technical", "friendly"]
OperationName = Literal["summarize", "rewrite", "classify", "extract"]


class ErrorResponse(pydantic.BaseModel):
    """Consistent API error envelope."""

    error: str
    details: object | None = None
    estimated_input_tokens: int | None = None
    max_input_tokens: int | None = None
    suggestion: str | None = None


class TokenUsage(pydantic.BaseModel):
    """Token usage metadata for one request."""

    input_tokens_estimated: int
    output_tokens_estimated: int
    total_tokens_estimated: int
    input_tokens_actual: int | None = None
    output_tokens_actual: int | None = None
    total_tokens_actual: int | None = None
    estimated_cost_usd: float | None = None


class ResponseMetadata(pydantic.BaseModel):
    """Shared non-content metadata returned by GenAI endpoints."""

    operation: OperationName
    model: str
    adapter: str
    provider: str
    max_input_tokens: int
    budget_ok: bool
    warnings: list[str] = pydantic.Field(default_factory=list)


class HealthResponse(pydantic.BaseModel):
    """Service health response."""

    status: Literal["ok"]
    app: str
    model: str
    adapter: str
    provider: str


class TextRequest(pydantic.BaseModel):
    """Common text input fields."""

    text: str = pydantic.Field(min_length=1, max_length=200_000)
    max_input_tokens: int | None = pydantic.Field(default=None, ge=1, le=200_000)


class SummarizeRequest(TextRequest):
    """Request body for ``POST /summarize``."""

    format: SummaryFormat = "paragraph"


class RewriteRequest(TextRequest):
    """Request body for ``POST /rewrite``."""

    tone: RewriteTone = "professional"


class ClassifyRequest(TextRequest):
    """Request body for ``POST /classify``."""

    labels: list[str] = pydantic.Field(min_length=2, max_length=30)
    instructions: str | None = pydantic.Field(default=None, max_length=2000)

    @pydantic.field_validator("labels")
    @classmethod
    def normalize_labels(cls, labels: list[str]) -> list[str]:
        """Trim labels and reject duplicates."""

        normalized = [label.strip() for label in labels if label.strip()]
        if len(normalized) < 2:
            raise ValueError("At least two non-empty labels are required.")
        lowered = [label.lower() for label in normalized]
        if len(lowered) != len(set(lowered)):
            raise ValueError("Labels must be unique.")
        return normalized


class FieldDefinition(pydantic.BaseModel):
    """Field requested by ``POST /extract``."""

    name: str = pydantic.Field(min_length=1, max_length=64, pattern=r"^[A-Za-z_][A-Za-z0-9_ -]*$")
    description: str | None = pydantic.Field(default=None, max_length=500)


class ExtractRequest(TextRequest):
    """Request body for ``POST /extract``."""

    fields: list[FieldDefinition] = pydantic.Field(min_length=1, max_length=25)
    instructions: str | None = pydantic.Field(default=None, max_length=2000)

    @pydantic.field_validator("fields")
    @classmethod
    def reject_duplicate_fields(cls, fields: list[FieldDefinition]) -> list[FieldDefinition]:
        """Reject duplicated field names case-insensitively."""

        lowered = [field.name.lower() for field in fields]
        if len(lowered) != len(set(lowered)):
            raise ValueError("Field names must be unique.")
        return fields


class TextOperationResponse(pydantic.BaseModel):
    """Response body for summarize/rewrite."""

    result: str
    usage: TokenUsage
    metadata: ResponseMetadata


class ClassifyModelOutput(pydantic.BaseModel):
    """Validated JSON output from the model for classification."""

    label: str
    confidence: float | None = pydantic.Field(default=None, ge=0.0, le=1.0)
    reason: str | None = None


class ClassifyResponse(ClassifyModelOutput):
    """API response body for classification."""

    usage: TokenUsage
    metadata: ResponseMetadata


class ExtractedField(pydantic.BaseModel):
    """A single extracted field value."""

    value: str | int | float | bool | None
    confidence: float | None = pydantic.Field(default=None, ge=0.0, le=1.0)
    evidence: str | None = None


class ExtractModelOutput(pydantic.BaseModel):
    """Validated JSON output from the model for extraction."""

    fields: dict[str, ExtractedField]


class ExtractResponse(ExtractModelOutput):
    """API response body for extraction."""

    usage: TokenUsage
    metadata: ResponseMetadata
