"""Unit tests for src/prompts.py — no API calls."""

from src import prompts
from tests import mocks


class TestSummaryPrompt:
    def test_returns_two_messages(self) -> None:
        msgs = prompts.summary(mocks.SAMPLE_TEXT)
        assert len(msgs) == 2

    def test_system_message_first(self) -> None:
        msgs = prompts.summary(mocks.SAMPLE_TEXT)
        assert msgs[0]["role"] == "system"
        assert mocks.SUMMARY_PROMPT_SYSTEM in msgs[0]["content"]

    def test_user_message_contains_text(self) -> None:
        msgs = prompts.summary(mocks.SAMPLE_TEXT)
        assert msgs[1]["role"] == "user"
        assert mocks.SAMPLE_TEXT in msgs[1]["content"]

    def test_all_messages_have_role_and_content(self) -> None:
        msgs = prompts.summary(mocks.SAMPLE_TEXT)
        assert all("role" in m and "content" in m for m in msgs)


class TestBulletsPrompt:
    def test_returns_two_messages(self) -> None:
        msgs = prompts.bullets(mocks.SAMPLE_TEXT)
        assert len(msgs) == 2

    def test_system_message_first(self) -> None:
        msgs = prompts.bullets(mocks.SAMPLE_TEXT)
        assert msgs[0]["role"] == "system"
        assert mocks.BULLETS_PROMPT_SYSTEM in msgs[0]["content"]

    def test_user_message_contains_text(self) -> None:
        msgs = prompts.bullets(mocks.SAMPLE_TEXT)
        assert mocks.SAMPLE_TEXT in msgs[1]["content"]

    def test_system_mentions_five_bullets(self) -> None:
        msgs = prompts.bullets(mocks.SAMPLE_TEXT)
        assert "5" in msgs[0]["content"]


class TestActionItemsPrompt:
    def test_returns_two_messages(self) -> None:
        msgs = prompts.action_items(mocks.SAMPLE_TEXT)
        assert len(msgs) == 2

    def test_system_message_first(self) -> None:
        msgs = prompts.action_items(mocks.SAMPLE_TEXT)
        assert msgs[0]["role"] == "system"
        assert mocks.ACTION_ITEMS_PROMPT_SYSTEM in msgs[0]["content"]

    def test_user_message_contains_text(self) -> None:
        msgs = prompts.action_items(mocks.SAMPLE_TEXT)
        assert mocks.SAMPLE_TEXT in msgs[1]["content"]


class TestFormatsRegistry:
    def test_all_three_formats_registered(self) -> None:
        assert set(prompts.FORMATS.keys()) == {"summary", "bullets", "action_items"}

    def test_each_format_is_callable(self) -> None:
        for name, fn in prompts.FORMATS.items():
            result = fn(mocks.SAMPLE_TEXT)
            assert isinstance(result, list), f"{name} should return a list"
            assert len(result) >= 1

    def test_formats_embed_input_text(self) -> None:
        for name, fn in prompts.FORMATS.items():
            msgs = fn(mocks.SAMPLE_TEXT)
            combined = " ".join(m["content"] for m in msgs)
            assert mocks.SAMPLE_TEXT in combined, f"{name}: input text not in messages"
