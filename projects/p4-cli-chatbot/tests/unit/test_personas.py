"""Tests for persona registry."""

import pytest

from src import personas


def test_default_persona_exists() -> None:
    persona = personas.get_persona("default")

    assert persona.name == "default"
    assert "practical" in persona.system_prompt


def test_get_persona_is_case_insensitive() -> None:
    persona = personas.get_persona("Senior-Engineer")

    assert persona.name == "senior-engineer"


def test_unknown_persona_raises_key_error() -> None:
    with pytest.raises(KeyError):
        personas.get_persona("space-wizard")


def test_list_personas_includes_expected_names() -> None:
    names = {persona.name for persona in personas.list_personas()}

    assert {"default", "senior-engineer", "socratic", "concise"} <= names
