"""Tests for schema validation."""

import pydantic
import pytest

from src import schemas


def test_model_output_rejects_invalid_score() -> None:
    payload = _model_output_payload()
    payload["fit_score"] = 101

    with pytest.raises(pydantic.ValidationError):
        schemas.ResumeJdModelOutput.model_validate(payload)


def test_model_output_rejects_extra_fields() -> None:
    payload = _model_output_payload()
    payload["extra"] = "nope"

    with pytest.raises(pydantic.ValidationError):
        schemas.ResumeJdModelOutput.model_validate(payload)


def _model_output_payload() -> dict[str, object]:
    return {
        "fit_score": 82,
        "recommendation": "strong_match",
        "matching_skills": ["Python", "FastAPI"],
        "partial_matches": ["AWS"],
        "missing_skills": ["LangGraph"],
        "strengths": ["Backend"],
        "risks": ["Limited GenAI production evidence"],
        "suggestions": ["Add RAG project"],
        "evidence": [
            {
                "area": "Backend",
                "resume_evidence": "Built FastAPI services",
                "jd_evidence": "Requires FastAPI",
                "judgment": "strong_match",
            }
        ],
    }
