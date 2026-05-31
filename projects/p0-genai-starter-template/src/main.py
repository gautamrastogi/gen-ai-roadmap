"""GenAI Starter Template — FastAPI application entry point.

Creates the FastAPI app, wires up the OpenAI client and settings,
and registers all routes.

Run locally::

    uv run uvicorn src.main:app --reload

Or via Makefile::

    make run
"""

import sys
import typing

import fastapi
import fastapi.middleware.cors

from src.integrations import openai_client
from src.models import schemas
from src.settings import Settings
from src.tools import llm as llm_tools
from src.utils import constants, errors, logging_context

# ---------------------------------------------------------------------------
# Bootstrap settings — exit cleanly if required env vars are missing
# ---------------------------------------------------------------------------


def _load_settings() -> Settings:
    """Load and validate settings; exit with a clear message if invalid.

    :return: Validated :class:`~src.settings.Settings` instance.
    :raises SystemExit: If required environment variables are missing.
    """
    try:
        return Settings()
    except Exception as exc:  # noqa: BLE001
        sys.stderr.write(f"[genai-starter] FATAL: {exc}\n")
        sys.exit(1)


_settings = _load_settings()
_client = openai_client.init(_settings)
logger = logging_context.get_logger("genai_starter.main")

# ---------------------------------------------------------------------------
# FastAPI app
# ---------------------------------------------------------------------------

app = fastapi.FastAPI(
    title=_settings.app_name,
    version=constants.APP_VERSION,
    description="GenAI Python starter template — reusable base for LLM services.",
)

app.add_middleware(
    fastapi.middleware.cors.CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------


@app.get(
    "/health",
    response_model=schemas.HealthResponse,
    summary="Health check",
    tags=["meta"],
)
async def health() -> dict[str, typing.Any]:
    """Return service health status.

    Use this as a liveness probe. Always returns HTTP 200 when the service
    is running and settings are valid.

    :return: :class:`~src.models.schemas.HealthResponse` dict.
    """
    logger.info("Health check called")
    return schemas.HealthResponse(
        status="ok",
        app=_settings.app_name,
        version=constants.APP_VERSION,
        model=_settings.openai_model,
    ).model_dump()


@app.post(
    "/complete",
    response_model=schemas.CompletionResponse,
    responses={500: {"model": schemas.ErrorResponse}},
    summary="LLM completion",
    tags=["llm"],
)
async def complete(
    request: schemas.CompletionRequest,
) -> dict[str, typing.Any]:
    """Send a prompt to the LLM and return the generated text.

    Accepts a JSON body matching :class:`~src.models.schemas.CompletionRequest`.
    Returns generated text plus token usage on success, or an error envelope
    on failure.

    :param request: Validated completion request body.
    :return: :class:`~src.models.schemas.CompletionResponse` dict on success.
    :raises fastapi.HTTPException: HTTP 500 on LLM or unexpected errors.
    """
    logger.info("Complete endpoint called", extra={"model": _settings.openai_model})
    try:
        return await llm_tools.complete(
            client=_client,
            model=_settings.openai_model,
            request=request,
        )
    except errors.LLMError as exc:
        logger.error("LLM error in /complete", extra={"error": exc.message})
        raise fastapi.HTTPException(
            status_code=500,
            detail={"error": exc.message, "details": exc.details},
        ) from exc
    except Exception as exc:  # noqa: BLE001
        logger.exception("Unexpected error in /complete")
        raise fastapi.HTTPException(
            status_code=500,
            detail={"error": "Unexpected server error", "details": str(exc)},
        ) from exc
