"""Prompt builders for the P5 service operations."""

from src import schemas

Message = dict[str, str]


def summarize_messages(text: str, output_format: schemas.SummaryFormat) -> list[Message]:
    """Build messages for summarization."""

    format_instructions = {
        "paragraph": "Return one concise paragraph of 3-5 sentences. No heading.",
        "bullets": "Return exactly five bullet points. No intro or outro.",
        "action_items": (
            "Return a numbered list of concrete action items. If none exist, return "
            "'1. No action items identified.'"
        ),
    }
    return [
        {
            "role": "system",
            "content": (
                "You are a precise summarization assistant. Preserve key facts, names, "
                "numbers, risks, and decisions. Do not invent missing context."
            ),
        },
        {
            "role": "user",
            "content": f"{format_instructions[output_format]}\n\nText:\n{text}",
        },
    ]


def rewrite_messages(text: str, tone: schemas.RewriteTone) -> list[Message]:
    """Build messages for text rewriting."""

    tone_instructions = {
        "professional": "formal, clear, and suitable for business communication",
        "concise": "as short as possible while preserving every key fact",
        "technical": "technically precise, structured, and active-voice",
        "friendly": "warm, conversational, and easy to read",
    }
    return [
        {
            "role": "system",
            "content": (
                "You rewrite text without changing the meaning. Output only the rewritten text, "
                "with no commentary, headings, or markdown fences."
            ),
        },
        {
            "role": "user",
            "content": f"Rewrite this text in a {tone_instructions[tone]} tone:\n\n{text}",
        },
    ]


def classify_messages(
    text: str,
    labels: list[str],
    instructions: str | None = None,
) -> list[Message]:
    """Build messages for label classification."""

    label_text = ", ".join(labels)
    extra = f"\nAdditional instructions: {instructions}" if instructions else ""
    return [
        {
            "role": "system",
            "content": (
                "You classify text into exactly one user-provided label. "
                "Return valid JSON only with keys: label, confidence, reason. "
                "The label must be one of the provided labels. Confidence is 0.0 to 1.0."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Labels: {label_text}{extra}\n\n"
                f"Text:\n{text}\n\n"
                'Return JSON like {"label":"...", "confidence":0.82, "reason":"..."}'
            ),
        },
    ]


def extract_messages(
    text: str,
    fields: list[schemas.FieldDefinition],
    instructions: str | None = None,
) -> list[Message]:
    """Build messages for field extraction."""

    field_lines = []
    for field in fields:
        description = f": {field.description}" if field.description else ""
        field_lines.append(f"- {field.name}{description}")
    extra = f"\nAdditional instructions: {instructions}" if instructions else ""
    return [
        {
            "role": "system",
            "content": (
                "You extract requested fields from text. Return valid JSON only with a top-level "
                "'fields' object. Each requested field must be present. Use null when missing. "
                "Each field value must include value, confidence, and evidence."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Requested fields:\n{chr(10).join(field_lines)}{extra}\n\n"
                f"Text:\n{text}\n\n"
                'Return JSON like {"fields":{"field_name":{"value":"...",'
                '"confidence":0.8,"evidence":"..."}}}'
            ),
        },
    ]
