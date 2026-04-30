"""Summarizer — terminal display."""

_WIDTH = 80

_LABELS: dict[str, str] = {
    "summary": "SUMMARY",
    "bullets": "KEY BULLETS",
    "action_items": "ACTION ITEMS",
}


def print_results(results: dict[str, str]) -> None:
    """Print each summarization format in a labelled panel.

    :param results: Mapping of format name to response text.
    """
    for fmt, text in results.items():
        label = _LABELS.get(fmt, fmt.upper())
        print(f"\n┌─ {label} {'─' * (_WIDTH - len(label) - 4)}┐")
        for line in text.splitlines():
            # Wrap long lines
            while len(line) > _WIDTH - 4:
                print(f"│  {line[:_WIDTH - 4]}")
                line = line[_WIDTH - 4 :]
            print(f"│  {line}")
        print(f"└{'─' * (_WIDTH - 2)}┘")
