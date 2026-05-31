"""Prompt Playground — four prompt strategy builders.

Each function accepts a task string and returns a list of OpenAI chat
messages ready to pass to ``chat.completions.create()``.

Strategies
----------
- ``zero_shot``   — bare task, no examples, no guidance.
- ``few_shot``    — two worked examples before the real task.
- ``system_role`` — tight system message defining persona + format.
- ``chain_of_thought`` — explicit "think step by step" instruction.
"""

import typing

# OpenAI message type alias
Message = dict[str, str]


def zero_shot(task: str) -> list[Message]:
    """Build a zero-shot prompt — no examples, no instructions.

    :param task: The task text to send to the model.
    :return: List of chat messages.
    """
    return [
        {"role": "user", "content": task},
    ]


def few_shot(task: str) -> list[Message]:
    """Build a few-shot prompt with two worked examples.

    :param task: The task text to send to the model.
    :return: List of chat messages.
    """
    return [
        {
            "role": "user",
            "content": "Explain what a neural network is.",
        },
        {
            "role": "assistant",
            "content": (
                "A neural network is a system of interconnected nodes inspired by the brain. "
                "It learns patterns from data by adjusting the strength of connections between nodes."
            ),
        },
        {
            "role": "user",
            "content": "Explain what gradient descent is.",
        },
        {
            "role": "assistant",
            "content": (
                "Gradient descent is an optimisation algorithm that iteratively adjusts model "
                "parameters in the direction that reduces error, like rolling a ball downhill "
                "to find the lowest point."
            ),
        },
        {"role": "user", "content": task},
    ]


def system_role(task: str) -> list[Message]:
    """Build a system-role prompt with a constrained expert persona.

    :param task: The task text to send to the model.
    :return: List of chat messages.
    """
    return [
        {
            "role": "system",
            "content": (
                "You are a concise technical educator. "
                "Always respond in exactly 3 sentences. "
                "Use plain language — no jargon unless you define it first."
            ),
        },
        {"role": "user", "content": task},
    ]


def chain_of_thought(task: str) -> list[Message]:
    """Build a chain-of-thought prompt asking for explicit reasoning.

    :param task: The task text to send to the model.
    :return: List of chat messages.
    """
    return [
        {
            "role": "system",
            "content": "Think step by step before giving your final answer.",
        },
        {
            "role": "user",
            "content": (
                f"{task}\n\n"
                "Walk through your reasoning step by step, then give a clear final answer."
            ),
        },
    ]


# Registry — keeps runner.py free of if/else chains
STRATEGIES: dict[str, typing.Callable[[str], list[Message]]] = {
    "zero_shot": zero_shot,
    "few_shot": few_shot,
    "system_role": system_role,
    "chain_of_thought": chain_of_thought,
}
