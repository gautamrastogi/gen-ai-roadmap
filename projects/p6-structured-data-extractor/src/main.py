"""CLI entrypoint for P6 structured data extraction."""

import argparse
import asyncio
import json
import sys
from pathlib import Path
from typing import cast

from src import errors, registry, schemas
from src.service import StructuredExtractor
from src.settings import Settings


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse CLI arguments."""

    parser = argparse.ArgumentParser(
        prog="structured-extractor",
        description="Extract strict typed JSON from messy text using local or hosted LLMs.",
    )
    parser.add_argument("--schema", choices=sorted(registry.SCHEMAS), help="Target schema name.")
    parser.add_argument("--file", type=Path, help="Input text file.")
    parser.add_argument("--text", help="Input text.")
    parser.add_argument(
        "--mode",
        choices=["prompt", "chat_schema", "responses_schema"],
        help="Override EXTRACTION_MODE.",
    )
    parser.add_argument("--list-schemas", action="store_true", help="List supported schemas.")
    parser.add_argument("--compact", action="store_true", help="Print compact JSON.")
    return parser.parse_args(argv)


def _read_input(args: argparse.Namespace) -> str:
    """Read text from --text, --file, or stdin."""

    if args.text:
        return cast(str, args.text)
    if args.file:
        return cast(Path, args.file).read_text(encoding="utf-8")
    if not sys.stdin.isatty():
        return str(sys.stdin.read())
    raise ValueError("Provide --text, --file, or pipe text on stdin.")


def _print_schemas() -> None:
    """Print supported schema names."""

    for definition in registry.list_schemas():
        print(f"{definition.name}\t{definition.title}\t{definition.description}")


def main(argv: list[str] | None = None) -> None:
    """Run the structured extraction CLI."""

    args = _parse_args(argv)
    if args.list_schemas:
        _print_schemas()
        return
    if not args.schema:
        sys.stderr.write(
            "[structured-extractor] --schema is required unless --list-schemas is used.\n"
        )
        sys.exit(2)

    try:
        settings = Settings()
        text = _read_input(args)
        mode = args.mode
        extractor = StructuredExtractor(settings)
        result = asyncio.run(extractor.extract(args.schema, text, _cast_mode(mode)))
    except errors.BudgetExceededError as exc:
        sys.stderr.write(
            "[structured-extractor] "
            f"{exc.message} estimated={exc.estimated_input_tokens} max={exc.max_input_tokens}\n"
        )
        sys.exit(1)
    except (errors.AppError, ValueError) as exc:
        details = (
            f" Details: {exc.details}" if isinstance(exc, errors.AppError) and exc.details else ""
        )
        sys.stderr.write(f"[structured-extractor] {exc}{details}\n")
        sys.exit(1)

    indent = None if args.compact else 2
    print(json.dumps(result.model_dump(mode="json"), indent=indent, sort_keys=not args.compact))


def _cast_mode(value: str | None) -> schemas.ExtractionMode | None:
    """Cast argparse mode to the schema literal type."""

    if value is None:
        return None
    if value in {"prompt", "chat_schema", "responses_schema"}:
        return cast(schemas.ExtractionMode, value)
    raise ValueError(f"Unsupported extraction mode: {value}")


if __name__ == "__main__":
    main()
