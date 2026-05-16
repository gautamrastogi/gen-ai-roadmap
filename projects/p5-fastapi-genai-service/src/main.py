"""FastAPI application for Project 5."""

import sys

import fastapi
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from src import errors, schemas
from src.service import GenAIService
from src.settings import Settings


def _load_settings() -> Settings:
    """Load settings and exit with a clear message if configuration is invalid."""

    try:
        return Settings()
    except Exception as exc:  # noqa: BLE001
        sys.stderr.write(f"[p5-fastapi-genai-service] FATAL: {exc}\n")
        sys.exit(1)


_settings = _load_settings()
_service = GenAIService(_settings)

app = fastapi.FastAPI(
    title="P5 FastAPI GenAI Service",
    version="0.1.0",
    description="Production-style GenAI API with token usage metadata.",
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    _: fastapi.Request,
    exc: RequestValidationError,
) -> JSONResponse:
    """Return validation errors in the service error envelope."""

    return JSONResponse(
        status_code=422,
        content=jsonable_encoder(
            schemas.ErrorResponse(error="validation_error", details=exc.errors())
        ),
    )


@app.exception_handler(errors.BudgetExceededError)
async def budget_exception_handler(
    _: fastapi.Request,
    exc: errors.BudgetExceededError,
) -> JSONResponse:
    """Return token budget failures as HTTP 422."""

    return JSONResponse(
        status_code=422,
        content=schemas.ErrorResponse(
            error=exc.message,
            details=exc.details,
            estimated_input_tokens=exc.estimated_input_tokens,
            max_input_tokens=exc.max_input_tokens,
            suggestion="Shorten text or pass a larger max_input_tokens value.",
        ).model_dump(),
    )


@app.exception_handler(errors.LLMTimeoutError)
async def timeout_exception_handler(
    _: fastapi.Request,
    exc: errors.LLMTimeoutError,
) -> JSONResponse:
    """Return provider timeouts as HTTP 504."""

    return JSONResponse(
        status_code=504,
        content=schemas.ErrorResponse(error=exc.message, details=exc.details).model_dump(),
    )


@app.exception_handler(errors.LLMProviderError)
async def provider_exception_handler(
    _: fastapi.Request,
    exc: errors.LLMProviderError,
) -> JSONResponse:
    """Return provider failures as HTTP 502."""

    return JSONResponse(
        status_code=502,
        content=schemas.ErrorResponse(error=exc.message, details=exc.details).model_dump(),
    )


@app.exception_handler(errors.LLMOutputError)
async def output_exception_handler(
    _: fastapi.Request,
    exc: errors.LLMOutputError,
) -> JSONResponse:
    """Return malformed model output as HTTP 502."""

    return JSONResponse(
        status_code=502,
        content=schemas.ErrorResponse(error=exc.message, details=exc.details).model_dump(),
    )


@app.get("/health", response_model=schemas.HealthResponse, tags=["meta"])
async def health() -> schemas.HealthResponse:
    """Return service health and model configuration."""

    return schemas.HealthResponse(
        status="ok",
        app=_settings.app_name,
        model=_settings.openai_model,
        adapter=_settings.llm_adapter,
        provider=_settings.provider,
    )


@app.post(
    "/summarize",
    response_model=schemas.TextOperationResponse,
    responses={422: {"model": schemas.ErrorResponse}, 502: {"model": schemas.ErrorResponse}},
    tags=["genai"],
)
async def summarize(request: schemas.SummarizeRequest) -> schemas.TextOperationResponse:
    """Summarize input text."""

    return await _service.summarize(request)


@app.post(
    "/rewrite",
    response_model=schemas.TextOperationResponse,
    responses={422: {"model": schemas.ErrorResponse}, 502: {"model": schemas.ErrorResponse}},
    tags=["genai"],
)
async def rewrite(request: schemas.RewriteRequest) -> schemas.TextOperationResponse:
    """Rewrite input text."""

    return await _service.rewrite(request)


@app.post(
    "/classify",
    response_model=schemas.ClassifyResponse,
    responses={422: {"model": schemas.ErrorResponse}, 502: {"model": schemas.ErrorResponse}},
    tags=["genai"],
)
async def classify(request: schemas.ClassifyRequest) -> schemas.ClassifyResponse:
    """Classify input text into one user-provided label."""

    return await _service.classify(request)


@app.post(
    "/extract",
    response_model=schemas.ExtractResponse,
    responses={422: {"model": schemas.ErrorResponse}, 502: {"model": schemas.ErrorResponse}},
    tags=["genai"],
)
async def extract(request: schemas.ExtractRequest) -> schemas.ExtractResponse:
    """Extract requested fields from input text."""

    return await _service.extract(request)
