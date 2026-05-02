#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys

from roadmap_agent import core


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Local read-only coach for the GenAI roadmap.")
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--json", action="store_true", help="Print machine-readable JSON.")

    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("status", parents=[common], help="Show current roadmap status.")
    next_parser = subparsers.add_parser("next", parents=[common], help="Recommend one focused next task.")
    next_parser.add_argument(
        "--no-llm",
        action="store_true",
        help="Use deterministic roadmap logic without a local model call.",
    )

    phase_parser = subparsers.add_parser(
        "phase",
        parents=[common],
        help="Show compact details for a roadmap phase.",
    )
    phase_parser.add_argument("--id", type=int, required=True, help="Phase id, for example 2.")

    init_parser = subparsers.add_parser("init", parents=[common], help="Print progress-file template.")
    init_parser.add_argument("--print-template", action="store_true", help="Print example JSON.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    try:
        if args.command == "status":
            payload = core.get_status()
            output = payload if args.json else core.format_status(payload)
        elif args.command == "next":
            payload = core.next_task() if args.no_llm else core.coach_next_task()
            if args.json:
                output = payload
            elif args.no_llm:
                output = core.format_next_task(payload)
            else:
                output = core.format_coach_task(payload)
        elif args.command == "phase":
            payload = core.get_phase_details(args.id)
            output = payload if args.json else core.format_phase(payload)
        elif args.command == "init":
            payload = json.loads(core.EXAMPLE_PROGRESS_PATH.read_text(encoding="utf-8"))
            output = payload if args.json else json.dumps(payload, indent=2)
        else:
            raise ValueError(f"Unknown command: {args.command}")
    except Exception as exc:  # noqa: BLE001
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(output, ensure_ascii=True, indent=2))
    else:
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
