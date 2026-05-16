"""Rich terminal display helpers."""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from src import personas
from src.session_store import ChatSession


def print_help(console: Console) -> None:
    """Render available slash commands."""

    table = Table(title="Commands", show_header=True, header_style="bold cyan")
    table.add_column("Command")
    table.add_column("Action")
    rows = [
        ("/help", "Show commands"),
        ("/personas", "List available personas"),
        ("/persona NAME", "Switch persona for future turns"),
        ("/stats", "Show token/session stats"),
        ("/undo", "Remove the last user/assistant turn"),
        ("/clear", "Clear this session"),
        ("/save [PATH]", "Save session JSON"),
        ("/export [PATH]", "Export transcript JSON"),
        ("/exit", "Quit"),
    ]
    for command, action in rows:
        table.add_row(command, action)
    console.print(table)


def print_personas(console: Console) -> None:
    """Render available personas."""

    table = Table(title="Personas", show_header=True, header_style="bold magenta")
    table.add_column("Name")
    table.add_column("Description")
    for persona in personas.list_personas():
        table.add_row(persona.name, persona.description)
    console.print(table)


def print_stats(console: Console, session: ChatSession) -> None:
    """Render session stats."""

    table = Table(title="Session Stats", show_header=False)
    table.add_column("Metric", style="cyan")
    table.add_column("Value")
    table.add_row("Session ID", session.session_id)
    table.add_row("Persona", session.persona)
    table.add_row("Messages", str(len(session.messages)))
    table.add_row("Turns", str(len(session.turns)))
    table.add_row("Prompt tokens", str(session.total_prompt_tokens))
    table.add_row("Completion tokens", str(session.total_completion_tokens))
    table.add_row("Total tokens", str(session.total_tokens))
    console.print(table)


def print_welcome(console: Console, session: ChatSession, model: str, session_path: str) -> None:
    """Render startup info."""

    console.print(
        Panel(
            (
                f"[bold]P4 CLI Chatbot[/bold]\n"
                f"Model: [cyan]{model}[/cyan]\n"
                f"Persona: [magenta]{session.persona}[/magenta]\n"
                f"Session: [green]{session_path}[/green]\n"
                "Type [cyan]/help[/cyan] for commands."
            ),
            title="GenAI Roadmap",
            border_style="cyan",
        )
    )
