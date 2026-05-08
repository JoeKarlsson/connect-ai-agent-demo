#!/usr/bin/env python3
"""
Enterprise Data AI Agent — CData Connect AI Demo

Usage:
    source .venv/bin/activate
    python main.py                  # interactive mode
    python main.py "your question"  # single query mode
"""
import os
import sys
from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text
from rich.rule import Rule
from rich import print as rprint

load_dotenv()

console = Console()


def _get_required_env(key: str) -> str:
    value = os.environ.get(key)
    if not value:
        console.print(f"[red]Error:[/red] {key} is not set.")
        console.print("Copy [bold].env.example[/bold] to [bold].env[/bold] and add your credentials.")
        sys.exit(1)
    return value


def run_with_spinner(query: str, mcp) -> str:
    from agent import run_query

    tool_log = []

    def on_tool_call(tool_names: list[str]):
        label = ", ".join(tool_names)
        tool_log.append(label)
        console.print(f"  [dim]↳ {label}[/dim]")

    with console.status("[bold cyan]Querying your data...[/bold cyan]", spinner="dots"):
        # status context keeps the spinner running; tool calls print beneath it
        pass

    # Run outside status so tool prints aren't swallowed
    return run_query(query, mcp, on_tool_call=on_tool_call)


def ask(query: str, mcp) -> None:
    from agent import run_query

    console.print()

    tool_calls_made = []

    def on_tool_call(tool_names: list[str]):
        label = ", ".join(tool_names)
        tool_calls_made.append(label)
        console.print(f"  [dim]↳ {label}[/dim]", highlight=False)

    with console.status("[bold cyan]Querying your data...[/bold cyan]", spinner="dots"):
        answer = run_query(query, mcp, on_tool_call=on_tool_call)

    console.print()
    console.print(Markdown(answer))
    console.print()


def main():
    email = _get_required_env("CDATA_EMAIL")
    token = _get_required_env("CDATA_ACCESS_TOKEN")

    from mcp_client import ConnectAIMCPClient

    with console.status("[dim]Connecting to CData Connect AI...[/dim]", spinner="dots"):
        try:
            mcp = ConnectAIMCPClient(email, token)
            tools = mcp.list_tools()
        except Exception as e:
            console.print(f"[red]Connection failed:[/red] {e}")
            console.print("Check your credentials and ensure you have at least one data source connected.")
            sys.exit(1)

    console.print(
        Panel(
            f"[bold green]Connected[/bold green] — [cyan]{len(tools)} tools[/cyan] available from CData Connect AI\n"
            "[dim]Sources: SalesPipeline (Google Sheets) · GitHub1 · SampleConnection1 (PostgreSQL) · SampleConnection2 (MySQL)[/dim]",
            expand=False,
        )
    )

    # Single query mode
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        ask(query, mcp)
        return

    # Interactive mode
    console.print("[dim]Ask anything about your connected data. Type [bold]quit[/bold] to exit.[/dim]\n")

    while True:
        try:
            query = console.input("[bold cyan]You:[/bold cyan] ").strip()
        except (EOFError, KeyboardInterrupt):
            console.print("\n[dim]Bye.[/dim]")
            break

        if query.lower() in ("quit", "exit", "q"):
            console.print("[dim]Bye.[/dim]")
            break

        if not query:
            continue

        try:
            ask(query, mcp)
        except Exception as e:
            console.print(f"[red]Error:[/red] {e}")


if __name__ == "__main__":
    main()
