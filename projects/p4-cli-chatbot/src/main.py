"""CLI Chatbot entrypoint."""

import argparse
import sys
from pathlib import Path
from typing import Any

from rich.console import Console
from rich.prompt import Prompt

from src import commands, display, personas, runner, session_store, token_usage
from src.settings import Settings


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse CLI arguments."""

    parser = argparse.ArgumentParser(
        prog="chatbot",
        description="Stateful terminal chatbot with personas, streaming, and transcripts.",
    )
    parser.add_argument("--session", type=Path, default=None, help="Session JSON path.")
    parser.add_argument("--persona", default=None, help="Initial persona name.")
    parser.add_argument("--model", default=None, help="Override model from .env.")
    parser.add_argument("--temperature", type=float, default=None, help="Override temperature.")
    parser.add_argument(
        "--max-tokens", type=int, default=None, help="Override max response tokens."
    )
    parser.add_argument("--base-url", default=None, help="Override OpenAI-compatible base URL.")
    return parser.parse_args(argv)


def _load_or_create_session(path: Path, persona_name: str) -> session_store.ChatSession:
    """Load session from disk or create a new one."""

    if path.exists():
        session = session_store.load_session(path)
        if persona_name:
            personas.get_persona(persona_name)
            session.persona = persona_name
        return session
    personas.get_persona(persona_name)
    return session_store.new_session(persona=persona_name)


def _handle_command(
    command: commands.Command,
    session: session_store.ChatSession,
    session_path: Path,
    console: Console,
) -> bool:
    """Handle a slash command.

    :return: True when the main loop should continue.
    """

    if command.name in {"exit", "quit", "q"}:
        session_store.save_session(session, session_path)
        console.print("[green]Saved. Bye.[/green]")
        return False

    if command.name == "help":
        display.print_help(console)
    elif command.name == "personas":
        display.print_personas(console)
    elif command.name == "persona":
        if not command.args:
            console.print("[red]Usage: /persona NAME[/red]")
        else:
            persona = personas.get_persona(command.args[0])
            session.persona = persona.name
            session_store.save_session(session, session_path)
            console.print(f"[green]Persona switched to {persona.name}.[/green]")
    elif command.name == "stats":
        display.print_stats(console, session)
    elif command.name == "undo":
        removed = session_store.undo_last_turn(session)
        session_store.save_session(session, session_path)
        console.print(
            "[green]Last turn removed.[/green]" if removed else "[yellow]Nothing to undo.[/yellow]"
        )
    elif command.name == "clear":
        session_store.clear_session(session)
        session_store.save_session(session, session_path)
        console.print("[green]Session cleared.[/green]")
    elif command.name in {"save", "export"}:
        target = Path(command.args[0]) if command.args else session_path
        session_store.save_session(session, target)
        console.print(f"[green]Saved to {target}.[/green]")
    else:
        console.print(f"[red]Unknown command: /{command.name}. Try /help.[/red]")

    return True


def _load_settings(args: argparse.Namespace) -> Settings:
    """Load settings with CLI overrides applied before validation."""

    updates: dict[str, Any] = {}
    if args.model:
        updates["openai_model"] = args.model
    if args.temperature is not None:
        updates["temperature"] = args.temperature
    if args.max_tokens is not None:
        updates["max_tokens"] = args.max_tokens
    if args.base_url:
        updates["openai_base_url"] = args.base_url
    return Settings(**updates)


def main(argv: list[str] | None = None) -> None:
    """Run the interactive chatbot."""

    console = Console()
    args = _parse_args(argv)

    try:
        settings = _load_settings(args)
        persona_name = args.persona or "default"
        session_path = args.session or settings.session_path
        session = _load_or_create_session(session_path, persona_name)
    except Exception as exc:  # noqa: BLE001
        sys.stderr.write(f"[chatbot] Config/session error: {exc}\n")
        sys.exit(1)

    display.print_welcome(console, session, settings.openai_model, str(session_path))

    while True:
        user_text = Prompt.ask("[bold cyan]you[/]").strip()
        if not user_text:
            continue

        command = commands.parse_command(user_text)
        if command:
            if not _handle_command(command, session, session_path, console):
                break
            continue

        persona = personas.get_persona(session.persona)
        api_messages = session_store.build_api_messages(session, persona.system_prompt)
        api_messages.append({"role": "user", "content": user_text})
        prompt_tokens = token_usage.estimate_messages_tokens(api_messages)

        console.print("[bold magenta]assistant[/bold magenta]")
        chunks: list[str] = []
        try:
            for chunk in runner.stream_chat(api_messages, settings):
                chunks.append(chunk)
                console.print(chunk, end="")
            console.print()
        except Exception as exc:  # noqa: BLE001
            console.print(f"\n[red]Model call failed: {exc}[/red]")
            continue

        assistant_text = "".join(chunks).strip()
        stats = session_store.TurnStats(
            prompt_tokens=prompt_tokens,
            completion_tokens=token_usage.estimate_tokens(assistant_text),
        )
        session_store.add_turn(session, user_text, assistant_text, stats)
        session_store.save_session(session, session_path)


if __name__ == "__main__":
    main()
