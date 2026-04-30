"""Rewriter — CLI entrypoint.

Usage::

    uv run python -m src.main --text "Paste your text here"
    uv run python -m src.main --file path/to/file.txt
    uv run python -m src.main --file draft.txt --tone professional
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
        prog="rewriter",
        description="Rewrite any text in professional, concise, technical, or friendly tone.",
    )
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--text", help="Text to rewrite (pass as a quoted string).")
    source.add_argument("--file", help="Path to a .txt file to rewrite.")
    parser.add_argument(
        "--tone",
        default=None,
        choices=["professional", "concise", "technical", "friendly"],
        help="Run only one tone instead of all four (saves API quota).",
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
    """Run the rewriter.

    :param argv: Optional argument list for testing; defaults to ``sys.argv``.
    """
    args = _parse_args(argv)

    # Read input text
    if args.file:
        try:
            text = open(args.file, encoding="utf-8").read().strip()
        except OSError as exc:
            sys.stderr.write(f"[rewriter] Cannot read file: {exc}\n")
            sys.exit(1)
    else:
        text = args.text.strip()

    if not text:
        sys.stderr.write("[rewriter] Input text is empty.\n")
        sys.exit(1)

    try:
        settings = Settings()
    except Exception as exc:  # noqa: BLE001
        sys.stderr.write(f"[rewriter] Config error: {exc}\n")
        sys.exit(1)

    # Apply overrides
    if args.model:
        settings = settings.model_copy(update={"openai_model": args.model})
    if args.temperature is not None:
        settings = settings.model_copy(update={"temperature": args.temperature})

    word_count = len(text.split())
    print(f"\nModel: {settings.openai_model}  |  Temperature: {settings.temperature}")
    print(f"Input: {word_count} words\n")

    if args.tone:
        print(f"Running tone: {args.tone}...")
        results, quota = runner.run_one(text, args.tone, settings)
    else:
        print("Running all 4 tones... (1.5 s pause between calls)\n")
        results, quota = runner.run_all(text, settings)

    display.print_results(results)

    if quota:
        print(
            f"\n  Quota: {quota['requests_remaining']}/{quota['requests_limit']} requests remaining"
            f"  |  {quota['tokens_remaining']}/{quota['tokens_limit']} tokens remaining"
            f"  |  resets in {quota['reset_seconds']}s"
        )


if __name__ == "__main__":
    main()
