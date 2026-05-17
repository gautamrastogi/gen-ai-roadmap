"""Prompt builders for resume/JD comparison."""

import json

from src import schemas

Message = dict[str, str]


def analysis_messages(resume_text: str, jd_text: str) -> list[Message]:
    """Build local-friendly prompt messages that include the target schema."""

    schema_json = json.dumps(
        schemas.ResumeJdModelOutput.model_json_schema(), indent=2, sort_keys=True
    )
    return [
        {
            "role": "system",
            "content": (
                "You are a precise technical hiring analyst. Compare a candidate resume against "
                "a job description. Return valid JSON only. Do not include markdown fences, "
                "commentary, or extra keys. Use evidence from both documents. Be fair: do not "
                "invent experience, and do not penalize missing wording when equivalent evidence exists."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Target JSON Schema:\n{schema_json}\n\n"
                f"Resume:\n{resume_text}\n\n"
                f"Job Description:\n{jd_text}\n\n"
                "Return one JSON object matching the schema. The fit_score must be 0-100. "
                "Recommendation must be one of: strong_match, possible_match, weak_match, not_recommended."
            ),
        },
    ]


def schema_mode_messages(resume_text: str, jd_text: str) -> list[Message]:
    """Build shorter messages for provider-level schema enforcement."""

    return [
        {
            "role": "system",
            "content": (
                "You are a precise technical hiring analyst. Compare a candidate resume against "
                "a job description using evidence from both documents. Follow the response schema exactly."
            ),
        },
        {
            "role": "user",
            "content": f"Resume:\n{resume_text}\n\nJob Description:\n{jd_text}",
        },
    ]
