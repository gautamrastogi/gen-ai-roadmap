"""Unit tests for src/prompts.py — no API calls."""

from src import prompts
from tests import mocks


class TestProfessionalPrompt:
    def test_returns_two_messages(self) -> None:
        msgs = prompts.professional(mocks.SAMPLE_TEXT)
        assert len(msgs) == 2

    def test_system_message_first(self) -> None:
        msgs = prompts.professional(mocks.SAMPLE_TEXT)
        assert msgs[0]["role"] == "system"
        assert mocks.PROFESSIONAL_SYSTEM in msgs[0]["content"]

    def test_user_message_contains_text(self) -> None:
        msgs = prompts.professional(mocks.SAMPLE_TEXT)
        assert msgs[1]["role"] == "user"
        assert mocks.SAMPLE_TEXT in msgs[1]["content"]

    def test_all_messages_have_role_and_content(self) -> None:
        msgs = prompts.professional(mocks.SAMPLE_TEXT)
        assert all("role" in m and "content" in m for m in msgs)


class TestConcisePrompt:
    def test_returns_two_messages(self) -> None:
        msgs = prompts.concise(mocks.SAMPLE_TEXT)
        assert len(msgs) == 2

    def test_system_message_first(self) -> None:
        msgs = prompts.concise(mocks.SAMPLE_TEXT)
        assert msgs[0]["role"] == "system"
        assert mocks.CONCISE_SYSTEM in msgs[0]["content"]

    def test_user_message_contains_text(self) -> None:
        msgs = prompts.concise(mocks.SAMPLE_TEXT)
        assert mocks.SAMPLE_TEXT in msgs[1]["content"]


class TestTechnicalPrompt:
    def test_returns_two_messages(self) -> None:
        msgs = prompts.technical(mocks.SAMPLE_TEXT)
        assert len(msgs) == 2

    def test_system_message_first(self) -> None:
        msgs = prompts.technical(mocks.SAMPLE_TEXT)
        assert msgs[0]["role"] == "system"
        assert mocks.TECHNICAL_SYSTEM in msgs[0]["content"]

    def test_user_message_contains_text(self) -> None:
        msgs = prompts.technical(mocks.SAMPLE_TEXT)
        assert mocks.SAMPLE_TEXT in msgs[1]["content"]


class TestFriendlyPrompt:
    def test_returns_two_messages(self) -> None:
        msgs = prompts.friendly(mocks.SAMPLE_TEXT)
        assert len(msgs) == 2

    def test_system_message_first(self) -> None:
        msgs = prompts.friendly(mocks.SAMPLE_TEXT)
        assert msgs[0]["role"] == "system"
        assert mocks.FRIENDLY_SYSTEM in msgs[0]["content"]

    def test_user_message_contains_text(self) -> None:
        msgs = prompts.friendly(mocks.SAMPLE_TEXT)
        assert mocks.SAMPLE_TEXT in msgs[1]["content"]


class TestTonesRegistry:
    def test_all_four_tones_registered(self) -> None:
        assert set(prompts.TONES.keys()) == {
            "professional",
            "concise",
            "technical",
            "friendly",
        }

    def test_each_tone_is_callable(self) -> None:
        for name, fn in prompts.TONES.items():
            result = fn(mocks.SAMPLE_TEXT)
            assert isinstance(result, list), f"{name} should return a list"
            assert len(result) == 2

    def test_tones_embed_input_text(self) -> None:
        for name, fn in prompts.TONES.items():
            msgs = fn(mocks.SAMPLE_TEXT)
            combined = " ".join(m["content"] for m in msgs)
            assert mocks.SAMPLE_TEXT in combined, f"{name}: input text not in messages"

    def test_all_tones_produce_system_and_user(self) -> None:
        for name, fn in prompts.TONES.items():
            msgs = fn(mocks.SAMPLE_TEXT)
            roles = [m["role"] for m in msgs]
            assert roles == [
                "system",
                "user",
            ], f"{name}: expected [system, user], got {roles}"
