"""Structured extraction service flow."""

import json

import openai
import pydantic

from src import errors, json_utils, llm, prompts, registry, schemas, token_usage, validation
from src.settings import Settings


class StructuredExtractor:
    """Owns schema selection, prompt building, model calls, and validation."""

    def __init__(self, settings: Settings, client: openai.AsyncOpenAI | None = None) -> None:
        self.settings = settings
        self.client = client

    async def extract(
        self,
        schema_name: str,
        text: str,
        mode: schemas.ExtractionMode | None = None,
    ) -> schemas.ExtractionResult:
        """Extract typed data from raw text."""

        definition = registry.get_schema(schema_name)
        active_mode = mode or self.settings.extraction_mode
        messages = (
            prompts.extraction_messages(definition, text)
            if active_mode == "prompt"
            else prompts.schema_mode_messages(definition, text)
        )

        input_tokens_estimated = token_usage.estimate_messages_tokens(messages)
        if input_tokens_estimated > self.settings.max_input_tokens:
            raise errors.BudgetExceededError(input_tokens_estimated, self.settings.max_input_tokens)

        model_result = await llm.generate_json(
            messages=messages,
            schema_model=definition.model,
            schema_name=definition.name,
            mode=active_mode,
            settings=self.settings,
            client=self.client,
        )
        parsed = _parse_model_output(model_result.text, definition.model)
        report = validation.build_validation_report(parsed)
        output_tokens_estimated = token_usage.estimate_tokens(model_result.text)

        return schemas.ExtractionResult(
            schema_name=definition.name,
            mode=active_mode,
            data=parsed.model_dump(mode="json"),
            validation_report=report,
            usage=_usage(input_tokens_estimated, output_tokens_estimated, model_result.usage),
            metadata=schemas.ExtractionMetadata(
                model=model_result.model,
                provider=self.settings.provider,
                schema_name=definition.name,
                mode=active_mode,
                max_input_tokens=self.settings.max_input_tokens,
                warnings=token_usage.budget_warnings(
                    input_tokens_estimated,
                    self.settings.max_input_tokens,
                ),
            ),
        )


def _parse_model_output(
    text: str,
    schema_model: type[pydantic.BaseModel],
) -> pydantic.BaseModel:
    """Parse and validate model JSON."""

    try:
        raw = json.loads(json_utils.extract_json_object(text))
    except json.JSONDecodeError as exc:
        raise errors.LLMOutputError("Model returned invalid JSON.", text[:500]) from exc
    try:
        return schema_model.model_validate(raw)
    except pydantic.ValidationError as exc:
        raise errors.LLMOutputError(
            "Model JSON did not match the target schema.",
            str(exc),
        ) from exc


def _usage(
    input_tokens_estimated: int,
    output_tokens_estimated: int,
    actual: llm.ActualUsage | None,
) -> schemas.TokenUsage:
    """Build usage response metadata."""

    return schemas.TokenUsage(
        input_tokens_estimated=input_tokens_estimated,
        output_tokens_estimated=output_tokens_estimated,
        total_tokens_estimated=input_tokens_estimated + output_tokens_estimated,
        input_tokens_actual=actual.input_tokens if actual else None,
        output_tokens_actual=actual.output_tokens if actual else None,
        total_tokens_actual=actual.total_tokens if actual else None,
    )
