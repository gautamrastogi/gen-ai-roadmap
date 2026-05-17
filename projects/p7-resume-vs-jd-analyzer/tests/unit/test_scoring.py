"""Tests for deterministic scoring."""

from src import schemas, scoring


def test_deterministic_score_matches_resume_keywords_to_jd() -> None:
    resume = "Python FastAPI Kafka Redis Postgres Docker OpenShift observability"
    jd = "Need Python FastAPI Kafka Redis PostgreSQL Docker Kubernetes observability and AWS"

    score = scoring.deterministic_score(resume, jd)

    assert score.deterministic_fit_score >= 70
    assert "python" in score.matched_keywords
    assert "aws" in score.missing_keywords


def test_blend_scores_prefers_model_but_keeps_deterministic_signal() -> None:
    output = schemas.ResumeJdModelOutput.model_validate(
        {
            "fit_score": 90,
            "recommendation": "strong_match",
            "matching_skills": ["Python"],
            "partial_matches": [],
            "missing_skills": [],
            "strengths": ["Backend"],
            "risks": [],
            "suggestions": [],
            "evidence": [
                {
                    "area": "Python",
                    "resume_evidence": "Python",
                    "jd_evidence": "Python",
                    "judgment": "strong_match",
                }
            ],
        }
    )
    deterministic = schemas.ScoreBreakdown(
        llm_fit_score=0,
        deterministic_fit_score=50,
        final_fit_score=50,
        matched_keywords=["python"],
        missing_keywords=["aws"],
    )

    blended = scoring.blend_scores(output, deterministic)

    assert blended.llm_fit_score == 90
    assert blended.final_fit_score == 78
