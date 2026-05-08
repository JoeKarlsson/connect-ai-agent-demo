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

load_dotenv()

console = Console()
AUTO  = "--auto"  in sys.argv
FAST  = "--fast"  in sys.argv
TYPE_SPEED = 0.018 if FAST else 0.042   # seconds per character

DEMO_STEPS = [
    {
        "comment": "what does the pipeline look like right now?",
        "command": "python main.py \"What's my pipeline value by stage and who are the top reps?\"",
        "query":   "What's my pipeline value by stage and who are the top reps?",
    },
    {
        "comment": "now pull in GitHub too — same command, both sources",
        "command": "python main.py \"Who is my top sales rep, what are their biggest open deals, and do I have any GitHub repos relevant to those deals?\"",
        "query":   "Who is my top sales rep, what are their biggest open deals, and do I have any GitHub repos relevant to those deals?",
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

    with console.status("[dim]connecting...[/dim]", spinner="dots"):
        mcp = ConnectAIMCPClient(email, token)
        mcp.list_tools()

    newline()

    for i, step in enumerate(DEMO_STEPS):
        print_comment(step["comment"])
        print_command(step["command"])
        pause(0.6)
        run_step(step["query"], mcp)

        if i < len(DEMO_STEPS) - 1:
            newline()
            if not AUTO:
                console.print("[dim]Press Enter to continue...[/dim]", end="")
            wait_for_enter()

    newline()


if __name__ == "__main__":
    main()
