"""Business logic for the P5 FastAPI GenAI endpoints."""

import json
from typing import TypeVar

import openai
import pydantic

from src import errors, llm, prompts, schemas, token_usage
from src.settings import Settings

Message = dict[str, str]
ModelT = TypeVar("ModelT", bound=pydantic.BaseModel)


class GenAIService:
    """Operation service that owns prompt building, budget checks, and LLM calls."""

    def __init__(self, settings: Settings, client: openai.AsyncOpenAI | None = None) -> None:
        self.settings = settings
        self.client = client

    async def summarize(self, request: schemas.SummarizeRequest) -> schemas.TextOperationResponse:
        """Summarize text."""

        messages = prompts.summarize_messages(request.text, request.format)
        result = await self._generate("summarize", messages, request.max_input_tokens)
        return schemas.TextOperationResponse(
            result=result.text,
            usage=result.usage,
            metadata=result.metadata,
        )

    async def rewrite(self, request: schemas.RewriteRequest) -> schemas.TextOperationResponse:
        """Rewrite text in the requested tone."""

        messages = prompts.rewrite_messages(request.text, request.tone)
        result = await self._generate("rewrite", messages, request.max_input_tokens)
        return schemas.TextOperationResponse(
            result=result.text,
            usage=result.usage,
            metadata=result.metadata,
        )

    async def classify(self, request: schemas.ClassifyRequest) -> schemas.ClassifyResponse:
        """Classify text into one user-provided label."""

        messages = prompts.classify_messages(request.text, request.labels, request.instructions)
        result = await self._generate("classify", messages, request.max_input_tokens)
        parsed = _parse_model_json(result.text, schemas.ClassifyModelOutput)
        if parsed.label not in request.labels:
            raise errors.LLMOutputError(
                "Model returned a label outside the requested label set.",
                f"label={parsed.label!r}",
            )
        return schemas.ClassifyResponse(
            label=parsed.label,
            confidence=parsed.confidence,
            reason=parsed.reason,
            usage=result.usage,
            metadata=result.metadata,
        )

    async def extract(self, request: schemas.ExtractRequest) -> schemas.ExtractResponse:
        """Extract user-requested fields from text."""

        messages = prompts.extract_messages(request.text, request.fields, request.instructions)
        result = await self._generate("extract", messages, request.max_input_tokens)
        parsed = _parse_model_json(result.text, schemas.ExtractModelOutput)
        expected = {field.name for field in request.fields}
        missing = expected - set(parsed.fields)
        if missing:
            raise errors.LLMOutputError(
                "Model omitted requested fields.",
                f"missing={sorted(missing)}",
            )
        return schemas.ExtractResponse(
            fields=parsed.fields,
            usage=result.usage,
            metadata=result.metadata,
        )

    async def _generate(
        self,
        operation: schemas.OperationName,
        messages: list[Message],
        request_max_input_tokens: int | None,
    ) -> "_OperationResult":
        max_input_tokens = request_max_input_tokens or self.settings.max_input_tokens
        input_tokens_estimated = token_usage.estimate_messages_tokens(messages)
        if input_tokens_estimated > max_input_tokens:
            raise errors.BudgetExceededError(input_tokens_estimated, max_input_tokens)

        llm_result = await llm.generate(messages, self.settings, self.client)
        output_tokens_estimated = token_usage.estimate_tokens(llm_result.text)
        usage = self._usage(
            input_tokens_estimated=input_tokens_estimated,
            output_tokens_estimated=output_tokens_estimated,
            actual=llm_result.usage,
        )
        metadata = schemas.ResponseMetadata(
            operation=operation,
            model=llm_result.model,
            adapter=self.settings.llm_adapter,
            provider=self.settings.provider,
            max_input_tokens=max_input_tokens,
            budget_ok=True,
            warnings=token_usage.budget_warnings(input_tokens_estimated, max_input_tokens),
        )
        return _OperationResult(text=llm_result.text, usage=usage, metadata=metadata)

    def _usage(
        self,
        input_tokens_estimated: int,
        output_tokens_estimated: int,
        actual: llm.ActualUsage | None,
    ) -> schemas.TokenUsage:
        actual_input = actual.input_tokens if actual else None
        actual_output = actual.output_tokens if actual else None
        actual_total = actual.total_tokens if actual else None
        cost_input = actual_input if actual_input is not None else input_tokens_estimated
        cost_output = actual_output if actual_output is not None else output_tokens_estimated
        return schemas.TokenUsage(
            input_tokens_estimated=input_tokens_estimated,
            output_tokens_estimated=output_tokens_estimated,
            total_tokens_estimated=input_tokens_estimated + output_tokens_estimated,
            input_tokens_actual=actual_input,
            output_tokens_actual=actual_output,
            total_tokens_actual=actual_total,
            estimated_cost_usd=token_usage.estimate_cost_usd(
                cost_input,
                cost_output,
                self.settings,
            ),
        )


class _OperationResult(pydantic.BaseModel):
    """Internal operation result."""

    text: str
    usage: schemas.TokenUsage
    metadata: schemas.ResponseMetadata


def _parse_model_json(text: str, model: type[ModelT]) -> ModelT:
    """Parse JSON returned by the model into the requested Pydantic model."""

    try:
        raw = json.loads(_extract_json_object(text))
    except json.JSONDecodeError as exc:
        raise errors.LLMOutputError("Model returned invalid JSON.", text[:500]) from exc
    try:
        return model.model_validate(raw)
    except pydantic.ValidationError as exc:
        raise errors.LLMOutputError(
            "Model JSON did not match the expected schema.", str(exc)
        ) from exc


def _extract_json_object(text: str) -> str:
    """Extract the first JSON object from model text."""

    stripped = text.strip()
    if stripped.startswith("{") and stripped.endswith("}"):
        return stripped

    start = stripped.find("{")
    if start < 0:
        raise json.JSONDecodeError("No JSON object found", stripped, 0)

    depth = 0
    in_string = False
    escaped = False
    for index, char in enumerate(stripped[start:], start=start):
        if escaped:
            escaped = False
            continue
        if char == "\\":
            escaped = True
            continue
        if char == '"':
            in_string = not in_string
            continue
        if in_string:
            continue
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return stripped[start : index + 1]

    raise json.JSONDecodeError("Unclosed JSON object", stripped, start)
