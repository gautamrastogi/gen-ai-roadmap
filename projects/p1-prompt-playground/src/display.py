"""Prompt Playground — terminal display.

Renders the strategy comparison as labelled panels to stdout.
No external dependencies — pure Python only.
"""

# Column width for the output panels
_WIDTH = 80

_LABELS: dict[str, str] = {
    "zero_shot": "ZERO-SHOT",
    "few_shot": "FEW-SHOT",
    "system_role": "SYSTEM ROLE",
    "chain_of_thought": "CHAIN-OF-THOUGHT",
}

_DESCRIPTIONS: dict[str, str] = {
    "zero_shot": "Raw task — no examples, no guidance",
    "few_shot": "Two worked examples in the prompt",
    "system_role": "Expert persona + strict format constraint",
    "chain_of_thought": "Explicit step-by-step reasoning instruction",
}


def print_results(task: str, results: dict[str, str]) -> None:
    """Print a side-by-side comparison panel for all strategy results.

    :param task: The original task string (printed as header).
    :param results: Mapping of strategy name to response text.
    """
    border = "═" * _WIDTH
    print(f"\n{'═' * _WIDTH}")
    print(f"  TASK: {task}")
    print(f"{'═' * _WIDTH}\n")

    for name, response in results.items():
        label = _LABELS.get(name, name.upper())
        desc = _DESCRIPTIONS.get(name, "")

        print(f"┌─ {label} {'─' * (_WIDTH - len(label) - 4)}┐")
        print(f"│  {desc}")
        print(f"├{'─' * (_WIDTH - 2)}┤")

        # Word-wrap the response to fit inside the panel
        words = response.split()
        line: list[str] = []
        for word in words:
            if sum(len(w) for w in line) + len(line) + len(word) > _WIDTH - 4:
                print(f"│  {'  '.join(line)}")
                line = [word]
            else:
                line.append(word)
        if line:
            print(f"│  {' '.join(line)}")

        print(f"└{'─' * (_WIDTH - 2)}┘\n")
