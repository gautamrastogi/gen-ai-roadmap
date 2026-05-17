"""CLI entrypoint for P7 resume-vs-JD analysis."""

import argparse
import asyncio
import json
import sys
from pathlib import Path
from typing import cast

from src import errors, schemas
from src.service import ResumeJdAnalyzer
from src.settings import Settings


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse CLI arguments."""

    parser = argparse.ArgumentParser(
        prog="resume-jd-analyzer",
        description="Analyze fit between a resume and a job description.",
    )
    parser.add_argument("--resume", type=Path, help="Resume text file.")
    parser.add_argument("--jd", type=Path, help="Job description text file.")
    parser.add_argument("--resume-text", help="Resume text.")
    parser.add_argument("--jd-text", help="Job description text.")
    parser.add_argument(
        "--mode",
        choices=["prompt", "chat_schema", "responses_schema"],
        help="Override ANALYSIS_MODE.",
    )
    parser.add_argument("--compact", action="store_true", help="Print compact JSON.")
    return parser.parse_args(argv)


def _read_pair(args: argparse.Namespace) -> tuple[str, str]:
    """Read resume and JD text from file or CLI args."""

    resume = _read_text(args.resume_text, args.resume, "resume")
    jd = _read_text(args.jd_text, args.jd, "job description")
    return resume, jd


def _read_text(value: str | None, path: Path | None, label: str) -> str:
    """Read one input document."""

    if value:
        return value
    if path:
        return path.read_text(encoding="utf-8")
    raise ValueError(f"Provide --{label.replace(' ', '-')} or --{label.replace(' ', '-')}-text.")


def main(argv: list[str] | None = None) -> None:
    """Run the CLI."""

    args = _parse_args(argv)
    try:
        settings = Settings()
        resume_text, jd_text = _read_pair(args)
        analyzer = ResumeJdAnalyzer(settings)
        result = asyncio.run(analyzer.analyze(resume_text, jd_text, _cast_mode(args.mode)))
    except errors.BudgetExceededError as exc:
        sys.stderr.write(
            "[resume-jd-analyzer] "
            f"{exc.message} estimated={exc.estimated_input_tokens} max={exc.max_input_tokens}\n"
        )
        sys.exit(1)
    except (errors.AppError, ValueError) as exc:
        details = (
            f" Details: {exc.details}" if isinstance(exc, errors.AppError) and exc.details else ""
        )
        sys.stderr.write(f"[resume-jd-analyzer] {exc}{details}\n")
        sys.exit(1)

    indent = None if args.compact else 2
    print(json.dumps(result.model_dump(mode="json"), indent=indent, sort_keys=not args.compact))


def _cast_mode(value: str | None) -> schemas.AnalysisMode | None:
    """Cast argparse mode to the schema literal type."""

    if value is None:
        return None
    if value in {"prompt", "chat_schema", "responses_schema"}:
        return cast(schemas.AnalysisMode, value)
    raise ValueError(f"Unsupported analysis mode: {value}")


if __name__ == "__main__":
    main()
