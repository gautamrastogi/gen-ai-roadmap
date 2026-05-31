"""Pydantic schemas for the starter template API."""

import typing

import pydantic


class HealthResponse(pydantic.BaseModel):
    """Response body returned by ``GET /health``."""

    status: str = pydantic.Field(description="Service status.")
    app: str = pydantic.Field(description="Application name.")
    version: str = pydantic.Field(description="Application version.")
    model: str = pydantic.Field(description="Configured LLM model.")


class CompletionRequest(pydantic.BaseModel):
    """Request body accepted by ``POST /complete``."""

    prompt: str = pydantic.Field(
        min_length=1,
        description="User prompt to send to the LLM.",
    )
    system: str = pydantic.Field(
        default="You are a helpful assistant.",
        min_length=1,
        description="System instruction used for the completion.",
    )
    max_tokens: int = pydantic.Field(
        default=200,
        ge=1,
        le=4096,
        description="Maximum number of completion tokens to request.",
    )
    temperature: float = pydantic.Field(
        default=0.7,
        ge=0.0,
        le=2.0,
        description="Sampling temperature for the completion.",
    )


class CompletionResponse(pydantic.BaseModel):
    """Successful response body returned by ``POST /complete``."""

    text: str = pydantic.Field(description="Generated completion text.")
    model: str = pydantic.Field(description="Model that generated the completion.")
    usage: dict[str, typing.Any] = pydantic.Field(
        default_factory=dict,
        description="Provider token usage metadata when available.",
    )


class ErrorResponse(pydantic.BaseModel):
    """Error response envelope used by documented FastAPI responses."""

    error: str = pydantic.Field(description="Stable error summary.")
    details: str | None = pydantic.Field(
        default=None,
        description="Additional provider or validation details when available.",
    )
