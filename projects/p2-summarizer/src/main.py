"""Summarizer — CLI entrypoint.

Usage::

    uv run python -m src.main --text "Paste your text here"
    uv run python -m src.main --file path/to/file.txt
    uv run python -m src.main --file notes.txt --format bullets
"""

import argparse
import sys

from src import display, runner
from src.settings import Settings


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse CLI arguments.

    :param argv: Argument list (defaults to ``sys.argv``).
    :return: Parsed namespace.
    """
    parser = argparse.ArgumentParser(
        prog="summarizer",
        description="Condense any text into a summary, bullet points, and action items.",
    )
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--text", help="Text to summarise (pass as a quoted string).")
    source.add_argument("--file", help="Path to a .txt file to summarise.")
    parser.add_argument(
        "--format",
        default=None,
        choices=["summary", "bullets", "action_items"],
        help="Run only one format instead of all three (saves API quota).",
    )
    parser.add_argument("--model", default=None, help="Override the model from .env.")
    parser.add_argument(
        "--temperature",
        type=float,
        default=None,
        help="Override temperature (0.0–1.0).",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    """Run the summarizer.

    :param argv: Optional argument list for testing; defaults to ``sys.argv``.
    """
    args = _parse_args(argv)

    # Read input text
    if args.file:
        try:
            text = open(args.file, encoding="utf-8").read().strip()
        except OSError as exc:
            sys.stderr.write(f"[summarizer] Cannot read file: {exc}\n")
            sys.exit(1)
    else:
        text = args.text.strip()

    if not text:
        sys.stderr.write("[summarizer] Input text is empty.\n")
        sys.exit(1)

    try:
        settings = Settings()
    except Exception as exc:  # noqa: BLE001
        sys.stderr.write(f"[summarizer] Config error: {exc}\n")
        sys.exit(1)

    if args.model:
        settings = settings.model_copy(update={"openai_model": args.model})
    if args.temperature is not None:
        settings = settings.model_copy(update={"temperature": args.temperature})

    print(f"\nModel: {settings.openai_model}  |  Temperature: {settings.temperature}")
    print(f"Input: {len(text.split())} words\n")

    if args.format:
        print(f"Running format: {args.format}")
        results, quota = runner.run_one(text, args.format, settings)
    else:
        print("Running all 3 formats... (1.5 s pause between calls)")
        results, quota = runner.run_all(text, settings)

    display.print_results(results)

    if quota and quota.get("remaining", -1) >= 0:
        print(
            f"\n  Quota: {quota['remaining']}/{quota['limit']} requests remaining"
            f"  |  {quota['remaining_tokens']}/{quota['limit_tokens']} tokens remaining"
            f"  |  resets in {quota['reset_in_s']}s"
        )


if __name__ == "__main__":
    main()
