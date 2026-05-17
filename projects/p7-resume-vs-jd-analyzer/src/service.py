"""Service flow for resume/JD analysis."""

import json

import openai
import pydantic

from src import errors, json_utils, llm, prompts, schemas, scoring, token_usage
from src.settings import Settings


class ResumeJdAnalyzer:
    """Owns prompt building, model calls, scoring, and final response assembly."""

    def __init__(self, settings: Settings, client: openai.AsyncOpenAI | None = None) -> None:
        self.settings = settings
        self.client = client

    async def analyze(
        self,
        resume_text: str,
        jd_text: str,
        mode: schemas.AnalysisMode | None = None,
    ) -> schemas.ResumeJdAnalysis:
        """Analyze resume fit against a job description."""

        active_mode = mode or self.settings.analysis_mode
        messages = (
            prompts.analysis_messages(resume_text, jd_text)
            if active_mode == "prompt"
            else prompts.schema_mode_messages(resume_text, jd_text)
        )

        input_tokens_estimated = token_usage.estimate_messages_tokens(messages)
        if input_tokens_estimated > self.settings.max_input_tokens:
            raise errors.BudgetExceededError(input_tokens_estimated, self.settings.max_input_tokens)

        model_result = await llm.generate_analysis(
            messages=messages,
            mode=active_mode,
            settings=self.settings,
            client=self.client,
        )
        parsed = _parse_model_output(model_result.text)
        deterministic = scoring.deterministic_score(resume_text, jd_text)
        score_breakdown = scoring.blend_scores(parsed, deterministic)
        output_tokens_estimated = token_usage.estimate_tokens(model_result.text)
        payload = parsed.model_dump(mode="json")
        payload["fit_score"] = score_breakdown.final_fit_score

        return schemas.ResumeJdAnalysis(
            **payload,
            score_breakdown=score_breakdown,
            usage=_usage(input_tokens_estimated, output_tokens_estimated, model_result.usage),
            metadata=schemas.AnalysisMetadata(
                model=model_result.model,
                provider=self.settings.provider,
                mode=active_mode,
                max_input_tokens=self.settings.max_input_tokens,
                warnings=token_usage.budget_warnings(
                    input_tokens_estimated,
                    self.settings.max_input_tokens,
                ),
            ),
        )


def _parse_model_output(text: str) -> schemas.ResumeJdModelOutput:
    """Parse and validate model JSON."""

    try:
        raw = json.loads(json_utils.extract_json_object(text))
    except json.JSONDecodeError as exc:
        raise errors.LLMOutputError("Model returned invalid JSON.", text[:500]) from exc
    try:
        return schemas.ResumeJdModelOutput.model_validate(raw)
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
