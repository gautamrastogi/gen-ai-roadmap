"""Pydantic schemas for resume-vs-JD analysis."""

from typing import Literal

import pydantic

AnalysisMode = Literal["prompt", "chat_schema", "responses_schema"]
Recommendation = Literal["strong_match", "possible_match", "weak_match", "not_recommended"]
Judgment = Literal["strong_match", "possible_match", "weak_match", "partial_match", "gap"]


class StrictModel(pydantic.BaseModel):
    """Base model for strict structured model outputs."""

    model_config = pydantic.ConfigDict(extra="forbid")


class EvidenceItem(StrictModel):
    """One evidence-backed fit judgment."""

    area: str = pydantic.Field(description="Skill, responsibility, domain, or requirement area.")
    resume_evidence: str = pydantic.Field(description="Relevant evidence from the resume.")
    jd_evidence: str = pydantic.Field(description="Relevant evidence from the job description.")
    judgment: Judgment = pydantic.Field(description="How well the resume matches this area.")


class ResumeJdModelOutput(StrictModel):
    """Structured output expected from the LLM."""

    fit_score: int = pydantic.Field(ge=0, le=100, description="Overall model-estimated fit score.")
    recommendation: Recommendation
    matching_skills: list[str] = pydantic.Field(
        description="Skills or requirements that match well."
    )
    partial_matches: list[str] = pydantic.Field(
        description="Skills or requirements with partial evidence."
    )
    missing_skills: list[str] = pydantic.Field(
        description="Important JD requirements missing from resume."
    )
    strengths: list[str] = pydantic.Field(description="Candidate strengths for this role.")
    risks: list[str] = pydantic.Field(description="Hiring or screening risks.")
    suggestions: list[str] = pydantic.Field(description="Concrete resume or learning suggestions.")
    evidence: list[EvidenceItem] = pydantic.Field(description="Evidence-backed comparison details.")


class ScoreBreakdown(pydantic.BaseModel):
    """Model score plus deterministic scoring metadata."""

    llm_fit_score: int = pydantic.Field(ge=0, le=100)
    deterministic_fit_score: int = pydantic.Field(ge=0, le=100)
    final_fit_score: int = pydantic.Field(ge=0, le=100)
    matched_keywords: list[str]
    missing_keywords: list[str]


class TokenUsage(pydantic.BaseModel):
    """Token usage metadata."""

    input_tokens_estimated: int
    output_tokens_estimated: int
    total_tokens_estimated: int
    input_tokens_actual: int | None = None
    output_tokens_actual: int | None = None
    total_tokens_actual: int | None = None


class AnalysisMetadata(pydantic.BaseModel):
    """Non-content metadata for one analysis."""

    model: str
    provider: str
    mode: AnalysisMode
    max_input_tokens: int
    warnings: list[str] = pydantic.Field(default_factory=list)


class ResumeJdAnalysis(ResumeJdModelOutput):
    """Final analysis returned by the CLI."""

    score_breakdown: ScoreBreakdown
    usage: TokenUsage
    metadata: AnalysisMetadata
