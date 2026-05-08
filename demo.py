#!/usr/bin/env python3
"""
Scripted demo walkthrough for CData Connect AI.

Tells a story in three acts:
  1. Query a single source (Google Sheets sales pipeline)
  2. Query a second source (GitHub repos)
  3. Cross-source query — the "aha" moment

Run: python demo.py
     python demo.py --auto    # auto-advance without keypresses (for recordings)
"""
import sys
import time
import os
from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.rule import Rule
from rich.text import Text
from rich.align import Align

load_dotenv()

console = Console()
AUTO = "--auto" in sys.argv

DEMO_STEPS = [
    {
        "act": "Act 1 — Single Source",
        "subtitle": "Querying a Google Sheets sales pipeline in plain English",
        "query": "What's my total pipeline value by stage, and who are the top 3 reps by open ARR?",
    },
    {
        "act": "Act 2 — Second Source",
        "subtitle": "Same interface, completely different source type",
        "query": "Show me my GitHub repositories updated in the last 30 days with their descriptions.",
    },
    {
        "act": "Act 3 — Cross-Source Intelligence",
        "subtitle": "One question. Two sources. No joins written by hand.",
        "query": "Who is my top sales rep by open pipeline, and do I have any GitHub repos relevant to their biggest deals?",
    },
]


def typewrite(text: str, style: str = "", delay: float = 0.03) -> None:
    """Print text character by character."""
    for char in text:
        console.print(char, style=style, end="", highlight=False)
        time.sleep(delay)
    console.print()


def press_to_continue() -> None:
    if AUTO:
        time.sleep(2)
        return
    console.print("\n[dim]  Press Enter to continue...[/dim]", end="")
    try:
        input()
    except (EOFError, KeyboardInterrupt):
        console.print()
        sys.exit(0)


def run_demo_query(query: str, mcp) -> None:
    from agent import run_query

    # Type out the query
    console.print("[dim]  You:[/dim] ", end="")
    typewrite(query, style="bold white", delay=0.025)
    console.print()

    def on_tool_call(tool_names):
        console.print(f"  [dim]↳ {', '.join(tool_names)}[/dim]", highlight=False)

    with console.status("[bold cyan]  Querying...[/bold cyan]", spinner="dots"):
        answer = run_query(query, mcp, on_tool_call=on_tool_call)

    console.print()
    console.print(Markdown(answer))


def main():
    email = os.environ.get("CDATA_EMAIL")
    token = os.environ.get("CDATA_ACCESS_TOKEN")

    if not email or not token:
        console.print("[red]Error:[/red] Missing CDATA_EMAIL or CDATA_ACCESS_TOKEN in .env")
        sys.exit(1)

    from mcp_client import ConnectAIMCPClient

    # Banner
    console.print()
    console.print(
        Panel(
            Align.center(
                "[bold white]Enterprise Data AI Agent[/bold white]\n"
                "[dim]Powered by CData Connect AI MCP Server[/dim]"
            ),
            border_style="cyan",
            padding=(1, 4),
        )
    )
    console.print()

    with console.status("[dim]Connecting to CData Connect AI...[/dim]", spinner="dots"):
        mcp = ConnectAIMCPClient(email, token)
        tools = mcp.list_tools()

    console.print(
        f"[green]✓[/green] Connected — [cyan]{len(tools)} tools[/cyan] across "
        "[bold]Google Sheets · GitHub · PostgreSQL · MySQL[/bold]\n"
    )

    press_to_continue()

    for i, step in enumerate(DEMO_STEPS):
        console.print(Rule(f"[bold cyan]{step['act']}[/bold cyan]", style="cyan"))
        console.print(f"  [dim]{step['subtitle']}[/dim]\n")

        run_demo_query(step["query"], mcp)

        if i < len(DEMO_STEPS) - 1:
            press_to_continue()

    console.print()
    console.print(Rule(style="cyan"))
    console.print(
        Align.center(
            "\n[bold green]Demo complete.[/bold green]\n"
            "[dim]One MCP server. 350+ sources. No custom connectors.[/dim]\n"
        )
    )


if __name__ == "__main__":
    main()
