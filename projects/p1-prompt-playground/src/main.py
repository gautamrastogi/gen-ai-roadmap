"""Prompt Playground — CLI entrypoint.

Usage::

    uv run python -m src.main --task "Explain what a transformer model is"
    uv run python -m src.main --task "What is RAG?" --model gpt-4o --temperature 0.3

Or via Makefile::

    make run
"""

import argparse
import sys

from src import runner, display
from src.settings import Settings


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse CLI arguments.

    :param argv: Argument list (defaults to ``sys.argv``).
    :return: Parsed namespace.
    """
    parser = argparse.ArgumentParser(
        prog="prompt-playground",
        description="Compare zero-shot, few-shot, system-role, and chain-of-thought on any task.",
    )
    parser.add_argument(
        "--task",
        required=True,
        help='The task to send to the model, e.g. "Explain what a transformer model is".',
    )
    parser.add_argument(
        "--model",
        default=None,
        help="Override the model from .env (e.g. gpt-4o).",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=None,
        help="Override sampling temperature (0.0 – 1.0).",
    )
    parser.add_argument(
        "--strategy",
        default=None,
        choices=["zero_shot", "few_shot", "system_role", "chain_of_thought"],
        help="Run only one strategy instead of all four (saves API calls).",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    """Run the prompt playground.

    :param argv: Optional argument list for testing; defaults to ``sys.argv``.
    """
    args = _parse_args(argv)

    try:
        settings = Settings()
    except Exception as exc:  # noqa: BLE001
        sys.stderr.write(f"[prompt-playground] Config error: {exc}\n")
        sys.exit(1)

    # Allow CLI flags to override .env values
    if args.model:
        settings = settings.model_copy(update={"openai_model": args.model})
    if args.temperature is not None:
        settings = settings.model_copy(update={"temperature": args.temperature})

    if args.strategy:
        print(
            f"\nModel: {settings.openai_model}  |  Temperature: {settings.temperature}"
        )
        print(f"Running strategy: {args.strategy}\n")
        results, quota = runner.run_one(args.task, args.strategy, settings)
    else:
        print(
            f"\nModel: {settings.openai_model}  |  Temperature: {settings.temperature}"
        )
        print("Running 4 strategies... (1.5 s pause between calls)\n")
        results, quota = runner.run_all(args.task, settings)
    display.print_results(args.task, results)
    if quota and quota.get("remaining", -1) >= 0:
        pct = (
            int(quota["remaining"] / quota["limit"] * 100) if quota["limit"] > 0 else 0
        )
        tok_rem = quota["remaining_tokens"]
        tok_lim = quota["limit_tokens"]
        print(
            f"\n  Quota: {quota['remaining']}/{quota['limit']} requests remaining"
            f"  |  {tok_rem}/{tok_lim} tokens remaining"
            f"  |  resets in {quota['reset_in_s']}s  [{pct}%]"
        )


if __name__ == "__main__":
    main()
