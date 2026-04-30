"""Unit tests for src/strategies.py.

Tests verify message shapes only — no API calls made.
"""

from src import strategies
from tests import mocks


def _all_messages_have_role_and_content(messages: list[dict[str, str]]) -> bool:
    """Check every message has non-empty 'role' and 'content' keys."""
    return all(
        isinstance(m.get("role"), str) and isinstance(m.get("content"), str)
        for m in messages
    )


class TestZeroShot:
    def test_returns_single_user_message(self) -> None:
        msgs = strategies.zero_shot(mocks.SAMPLE_TASK)
        assert msgs == mocks.ZERO_SHOT_MESSAGES

    def test_message_shape(self) -> None:
        msgs = strategies.zero_shot(mocks.SAMPLE_TASK)
        assert _all_messages_have_role_and_content(msgs)

    def test_task_is_preserved(self) -> None:
        msgs = strategies.zero_shot(mocks.SAMPLE_TASK)
        assert msgs[-1]["content"] == mocks.SAMPLE_TASK


class TestFewShot:
    def test_correct_message_count(self) -> None:
        msgs = strategies.few_shot(mocks.SAMPLE_TASK)
        assert len(msgs) == mocks.FEW_SHOT_MESSAGE_COUNT

    def test_last_message_is_task(self) -> None:
        msgs = strategies.few_shot(mocks.SAMPLE_TASK)
        assert msgs[-1]["role"] == "user"
        assert msgs[-1]["content"] == mocks.SAMPLE_TASK

    def test_message_shape(self) -> None:
        msgs = strategies.few_shot(mocks.SAMPLE_TASK)
        assert _all_messages_have_role_and_content(msgs)

    def test_examples_alternate_roles(self) -> None:
        msgs = strategies.few_shot(mocks.SAMPLE_TASK)
        # First 4 messages should alternate user/assistant
        roles = [m["role"] for m in msgs[:4]]
        assert roles == ["user", "assistant", "user", "assistant"]


class TestSystemRole:
    def test_correct_message_count(self) -> None:
        msgs = strategies.system_role(mocks.SAMPLE_TASK)
        assert len(msgs) == mocks.SYSTEM_ROLE_MESSAGE_COUNT

    def test_first_message_is_system(self) -> None:
        msgs = strategies.system_role(mocks.SAMPLE_TASK)
        assert msgs[0]["role"] == "system"

    def test_last_message_is_task(self) -> None:
        msgs = strategies.system_role(mocks.SAMPLE_TASK)
        assert msgs[-1]["content"] == mocks.SAMPLE_TASK

    def test_message_shape(self) -> None:
        msgs = strategies.system_role(mocks.SAMPLE_TASK)
        assert _all_messages_have_role_and_content(msgs)


class TestChainOfThought:
    def test_correct_message_count(self) -> None:
        msgs = strategies.chain_of_thought(mocks.SAMPLE_TASK)
        assert len(msgs) == mocks.CHAIN_OF_THOUGHT_MESSAGE_COUNT

    def test_first_message_is_system(self) -> None:
        msgs = strategies.chain_of_thought(mocks.SAMPLE_TASK)
        assert msgs[0]["role"] == "system"

    def test_user_message_contains_task(self) -> None:
        msgs = strategies.chain_of_thought(mocks.SAMPLE_TASK)
        assert mocks.SAMPLE_TASK in msgs[-1]["content"]

    def test_user_message_contains_cot_instruction(self) -> None:
        msgs = strategies.chain_of_thought(mocks.SAMPLE_TASK)
        assert "step by step" in msgs[-1]["content"].lower()

    def test_message_shape(self) -> None:
        msgs = strategies.chain_of_thought(mocks.SAMPLE_TASK)
        assert _all_messages_have_role_and_content(msgs)


class TestStrategyRegistry:
    def test_all_four_strategies_registered(self) -> None:
        assert set(strategies.STRATEGIES.keys()) == {
            "zero_shot",
            "few_shot",
            "system_role",
            "chain_of_thought",
        }

    def test_all_strategies_callable(self) -> None:
        for fn in strategies.STRATEGIES.values():
            assert callable(fn)
