"""Rewriter — terminal display."""

_WIDTH = 80

_LABELS: dict[str, str] = {
    "professional": "PROFESSIONAL",
    "concise": "CONCISE",
    "technical": "TECHNICAL",
    "friendly": "FRIENDLY",
}


def print_results(results: dict[str, str]) -> None:
    """Print each rewrite tone in a labelled panel.

    :param results: Mapping of tone name to rewritten text.
    """
    for tone, text in results.items():
        label = _LABELS.get(tone, tone.upper())
        print(f"\n┌─ {label} {'─' * (_WIDTH - len(label) - 4)}┐")
        for line in text.splitlines():
            while len(line) > _WIDTH - 4:
                print(f"│  {line[:_WIDTH - 4]}")
                line = line[_WIDTH - 4 :]
            print(f"│  {line}")
        print(f"└{'─' * (_WIDTH - 2)}┘")
