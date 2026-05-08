#!/usr/bin/env python3
"""
Demo magic-style walkthrough for CData Connect AI.

Shows actual commands being typed out live — looks like a real terminal session.
Press Enter to advance, or run with --auto to self-advance.

Usage:
    python demo.py             # press Enter to advance
    python demo.py --auto      # auto-advance (screen recordings)
    python demo.py --fast      # faster typing speed
"""
import sys
import time
import random
import os
from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.rule import Rule
from rich.align import Align

load_dotenv()

console = Console()
AUTO  = "--auto"  in sys.argv
FAST  = "--fast"  in sys.argv
TYPE_SPEED = 0.018 if FAST else 0.042   # seconds per character

DEMO_STEPS = [
    {
        "act":      "Act 1 — Single Source",
        "subtitle": "Querying a Google Sheets sales pipeline in plain English",
        "comment":  "Connect to our sales pipeline — Google Sheets as the data source",
        "command":  "python main.py \"What's my pipeline value by stage and who are the top reps?\"",
        "query":    "What's my pipeline value by stage and who are the top reps?",
    },
    {
        "act":      "Act 2 — Second Source",
        "subtitle": "Same command. Completely different source type.",
        "comment":  "Now query GitHub — same interface, zero code changes",
        "command":  "python main.py \"Show me my GitHub repos updated in the last 60 days\"",
        "query":    "Show me my GitHub repos updated in the last 60 days",
    },
    {
        "act":      "Act 3 — Cross-Source Intelligence",
        "subtitle": "One question. Two sources. No joins written by hand.",
        "comment":  "Ask something that spans both sources at once",
        "command":  "python main.py \"Who is my top sales rep and do I have GitHub repos relevant to their biggest deals?\"",
        "query":    "Who is my top sales rep and do I have GitHub repos relevant to their biggest deals?",
    },
]


# ── low-level typing helpers ──────────────────────────────────────────────────

def _write(text: str) -> None:
    sys.stdout.write(text)
    sys.stdout.flush()


def type_out(text: str, speed: float = TYPE_SPEED) -> None:
    """Print text character by character with slight random jitter — demo-magic style."""
    for char in text:
        _write(char)
        time.sleep(speed + random.uniform(-speed * 0.3, speed * 0.5))


def newline() -> None:
    _write("\n")


def pause(seconds: float = 1.2) -> None:
    """Wait between command display and execution — mimics reading time."""
    time.sleep(seconds)


def wait_for_enter() -> None:
    if AUTO:
        time.sleep(1.8)
        return
    try:
        input()
    except (EOFError, KeyboardInterrupt):
        newline()
        sys.exit(0)


# ── demo building blocks ──────────────────────────────────────────────────────

def print_comment(text: str) -> None:
    """Dim comment line — narrates what's about to happen."""
    _write("\033[0;90m")          # grey
    type_out(f"# {text}", speed=TYPE_SPEED * 0.7)
    _write("\033[0m")             # reset
    newline()


def print_command(cmd: str) -> None:
    """Type out the command with a green prompt."""
    _write("\n\033[1;32m$ \033[0m")   # bold green prompt
    _write("\033[1m")                  # bold command text
    type_out(cmd)
    _write("\033[0m")
    newline()


def run_step(query: str, mcp) -> None:
    """Execute the query and render the result."""
    from agent import run_query

    def on_tool_call(tool_names):
        console.print(f"  [dim]↳ {', '.join(tool_names)}[/dim]", highlight=False)

    with console.status("[bold cyan]  Querying...[/bold cyan]", spinner="dots"):
        answer = run_query(query, mcp, on_tool_call=on_tool_call)

    console.print()
    console.print(Markdown(answer))


# ── main demo ─────────────────────────────────────────────────────────────────

def main():
    email = os.environ.get("CDATA_EMAIL")
    token = os.environ.get("CDATA_ACCESS_TOKEN")

    if not email or not token:
        console.print("[red]Missing CDATA_EMAIL or CDATA_ACCESS_TOKEN in .env[/red]")
        sys.exit(1)

    from mcp_client import ConnectAIMCPClient

    # Banner
    console.print()
    console.print(
        Panel(
            Align.center(
                "[bold white]Enterprise Data AI Agent[/bold white]\n"
                "[dim]CData Connect AI · MCP Server Demo[/dim]"
            ),
            border_style="cyan",
            padding=(1, 6),
        )
    )
    console.print()

    # Connect
    with console.status("[dim]Connecting...[/dim]", spinner="dots"):
        mcp = ConnectAIMCPClient(email, token)
        tools = mcp.list_tools()

    console.print(
        f"  [green]✓[/green] [bold]{len(tools)} tools[/bold] available — "
        "Google Sheets · GitHub · PostgreSQL · MySQL\n"
    )

    if not AUTO:
        console.print("  [dim]Press Enter to start the demo...[/dim]", end="")
    wait_for_enter()

    # Acts
    for i, step in enumerate(DEMO_STEPS):
        console.print()
        console.print(Rule(f"[bold cyan]{step['act']}[/bold cyan]", style="dim cyan"))
        console.print(f"  [dim]{step['subtitle']}[/dim]")
        console.print()

        print_comment(step["comment"])
        print_command(step["command"])
        pause(0.6)

        run_step(step["query"], mcp)

        if i < len(DEMO_STEPS) - 1:
            console.print()
            if not AUTO:
                console.print("  [dim]Press Enter for next act...[/dim]", end="")
            wait_for_enter()

    # Close
    console.print()
    console.print(Rule(style="dim cyan"))
    console.print(
        Align.center(
            "\n[bold green]✓ Demo complete[/bold green]\n"
            "[dim]One MCP server. 350+ sources. No custom connectors.[/dim]\n"
        )
    )


if __name__ == "__main__":
    main()
