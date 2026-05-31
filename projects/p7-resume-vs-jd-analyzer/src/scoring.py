"""Deterministic fit scoring helpers."""

import re

from src import schemas

_CANONICAL_SKILLS: dict[str, tuple[str, ...]] = {
    "python": ("python",),
    "django": ("django",),
    "fastapi": ("fastapi", "fast api"),
    "rest api": ("rest", "api", "apis"),
    "microservices": ("microservice", "microservices"),
    "event-driven systems": ("event driven", "event-driven", "events"),
    "kafka": ("kafka",),
    "redis": ("redis",),
    "postgres": ("postgres", "postgresql"),
    "docker": ("docker", "container"),
    "kubernetes/openshift": ("kubernetes", "openshift", "k8s"),
    "ci/cd": ("ci/cd", "cicd", "pipeline", "github actions", "azure devops"),
    "aws": ("aws", "amazon web services"),
    "terraform": ("terraform",),
    "linux": ("linux",),
    "observability": ("observability", "monitoring", "logging", "tracing", "elk"),
    "llm/genai": ("llm", "genai", "generative ai", "openai", "rag", "agent"),
}

_ROLE_TERMS = {
    "backend": ("backend", "api", "service"),
    "platform": ("platform", "infrastructure", "devops"),
    "ai": ("ai", "genai", "llm", "rag", "agent"),
}


def deterministic_score(resume_text: str, jd_text: str) -> schemas.ScoreBreakdown:
    """Compute a lightweight deterministic fit score from keyword overlap."""

    resume = _normalize(resume_text)
    jd = _normalize(jd_text)
    jd_keywords = _keywords_in_text(jd)
    resume_keywords = _keywords_in_text(resume)

    required = sorted(jd_keywords)
    matched = sorted(jd_keywords & resume_keywords)
    missing = sorted(jd_keywords - resume_keywords)

    keyword_score = round((len(matched) / len(required)) * 100) if required else 50

    role_bonus = _role_alignment_bonus(resume, jd)
    deterministic = max(0, min(100, keyword_score + role_bonus))
    return schemas.ScoreBreakdown(
        llm_fit_score=0,
        deterministic_fit_score=deterministic,
        final_fit_score=deterministic,
        matched_keywords=matched,
        missing_keywords=missing,
    )


def blend_scores(
    llm_output: schemas.ResumeJdModelOutput,
    deterministic: schemas.ScoreBreakdown,
) -> schemas.ScoreBreakdown:
    """Blend model judgment with deterministic keyword overlap."""

    final = round((llm_output.fit_score * 0.7) + (deterministic.deterministic_fit_score * 0.3))
    return schemas.ScoreBreakdown(
        llm_fit_score=llm_output.fit_score,
        deterministic_fit_score=deterministic.deterministic_fit_score,
        final_fit_score=max(0, min(100, final)),
        matched_keywords=deterministic.matched_keywords,
        missing_keywords=deterministic.missing_keywords,
    )


def _keywords_in_text(text: str) -> set[str]:
    """Return canonical skills mentioned in text."""

    found = set()
    for canonical, aliases in _CANONICAL_SKILLS.items():
        if any(_contains_alias(text, alias) for alias in aliases):
            found.add(canonical)
    return found


def _contains_alias(text: str, alias: str) -> bool:
    """Return whether normalized text contains a skill alias."""

    if " " in alias or "/" in alias:
        return alias in text
    return bool(re.search(rf"\b{re.escape(alias)}\b", text))


def _role_alignment_bonus(resume: str, jd: str) -> int:
    """Add a small bonus when resume and JD share role-family terms."""

    bonus = 0
    for aliases in _ROLE_TERMS.values():
        if any(alias in jd for alias in aliases) and any(alias in resume for alias in aliases):
            bonus += 3
    return min(bonus, 9)


def _normalize(text: str) -> str:
    """Normalize text for simple matching."""

    return re.sub(r"\s+", " ", text.lower())
