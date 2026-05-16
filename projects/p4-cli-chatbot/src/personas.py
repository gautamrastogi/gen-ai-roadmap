"""Persona prompts for the CLI chatbot."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Persona:
    """A named system prompt."""

    name: str
    description: str
    system_prompt: str


PERSONAS: dict[str, Persona] = {
    "default": Persona(
        name="default",
        description="Balanced, practical assistant.",
        system_prompt=(
            "You are a practical AI assistant. Be clear, helpful, and concise. "
            "Ask a question only when the next step is genuinely ambiguous."
        ),
    ),
    "senior-engineer": Persona(
        name="senior-engineer",
        description="Direct senior engineer for implementation and tradeoffs.",
        system_prompt=(
            "You are a senior software engineer. Give pragmatic engineering advice, "
            "call out tradeoffs, prefer simple designs, and include concrete next steps."
        ),
    ),
    "socratic": Persona(
        name="socratic",
        description="Coaching style that teaches by asking focused questions.",
        system_prompt=(
            "You are a Socratic technical coach. Help the user reason through the problem. "
            "Ask one focused question at a time, then synthesize the lesson."
        ),
    ),
    "concise": Persona(
        name="concise",
        description="Short answers with minimal ceremony.",
        system_prompt=(
            "You are a concise assistant. Answer in the fewest words that still solve the "
            "problem. Prefer compact bullets for multi-step answers."
        ),
    ),
}


def get_persona(name: str) -> Persona:
    """Return a persona by name.

    :raises KeyError: If the persona does not exist.
    """

    key = name.strip().lower()
    if key not in PERSONAS:
        raise KeyError(f"Unknown persona {name!r}. Available: {', '.join(PERSONAS)}")
    return PERSONAS[key]


def list_personas() -> list[Persona]:
    """Return personas in display order."""

    return list(PERSONAS.values())
