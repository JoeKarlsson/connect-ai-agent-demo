#!/usr/bin/env python3
"""
CData Connect AI — Live Demo

Two interfaces, two data sources, one demo:
  1. Python SDK (DB-API 2.0) — direct SQL via cursor, pandas-ready
  2. MCP Agent — natural language across multiple sources via Claude

Usage:
    python demo.py           # press Enter to advance
    python demo.py --auto    # auto-advance (screen recordings)
"""
import sys
import os
import time
from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.syntax import Syntax
from rich.rule import Rule
import pandas as pd

load_dotenv()

console = Console()
AUTO = "--auto" in sys.argv


def wait(seconds: float = 1.5) -> None:
    if AUTO:
        time.sleep(seconds)
    else:
        try:
            input()
        except (EOFError, KeyboardInterrupt):
            sys.exit(0)


def pause(seconds: float = 1.2) -> None:
    time.sleep(seconds)


# ── Act 1: Python SDK ─────────────────────────────────────────────────────────

SDK_CODE = '''\
import cdata_connect_ai

conn = cdata_connect_ai.connect(
    username=EMAIL,
    password=ACCESS_TOKEN,
)

cur = conn.cursor()
cur.execute("""
    SELECT stage, account_owner,
           SUM(arr_value) AS total_arr,
           COUNT(*)       AS deals
    FROM [GoogleSheets1].[GoogleSheets].[Connect AI Demo — Sales Pipeline_pipeline]
    WHERE stage != 'Closed Lost'
    GROUP BY stage, account_owner
    ORDER BY stage, total_arr DESC
""")
df = pd.DataFrame(cur.fetchall(), columns=[d[0] for d in cur.description])
conn.close()
'''


def run_sdk_demo(email: str, token: str) -> pd.DataFrame:
    import cdata_connect_ai

    conn = cdata_connect_ai.connect(username=email, password=token)
    cur = conn.cursor()
    cur.execute("""
        SELECT stage, account_owner,
               SUM(arr_value) AS total_arr,
               COUNT(*)       AS deals
        FROM [GoogleSheets1].[GoogleSheets].[Connect AI Demo — Sales Pipeline_pipeline]
        WHERE stage != 'Closed Lost'
        GROUP BY stage, account_owner
        ORDER BY stage, total_arr DESC
    """)
    df = pd.DataFrame(cur.fetchall(), columns=[d[0] for d in cur.description])
    conn.close()
    return df


# ── Act 2: MCP Agent ──────────────────────────────────────────────────────────

AGENT_QUERY = (
    "We're deciding where to focus sales effort next quarter. "
    "Show our open pipeline ARR by industry from the sales pipeline. "
    "Then from the PostgreSQL customer database, pull total revenue by sector. "
    "Tell me: does our pipeline targeting match where our best customers actually come from — "
    "and where's the biggest gap?"
)


def run_agent_demo(mcp) -> str:
    from agent import run_query

    tool_rounds = []

    def on_tool_call(tool_names):
        label = ", ".join(tool_names)
        tool_rounds.append(label)
        console.print(f"  [dim]↳ {label}[/dim]", highlight=False)

    with console.status("[bold cyan]  Agent running...[/bold cyan]", spinner="dots"):
        answer = run_query(AGENT_QUERY, mcp, on_tool_call=on_tool_call)

    return answer


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    email = os.environ.get("CDATA_EMAIL")
    token = os.environ.get("CDATA_ACCESS_TOKEN")

    if not email or not token:
        console.print("[red]Missing CDATA_EMAIL or CDATA_ACCESS_TOKEN in .env[/red]")
        sys.exit(1)

    # ── Intro ─────────────────────────────────────────────────────────────────
    console.print()
    console.print(Panel.fit(
        "[bold]CData Connect AI — Live Demo[/bold]\n"
        "[dim]Two interfaces · Multiple sources · Real data[/dim]",
        border_style="cyan",
    ))
    console.print()
    console.print("[dim]Press Enter to advance →[/dim]" if not AUTO else "")
    wait(1.0)

    # ══════════════════════════════════════════════════════════════════════════
    # ACT 1: Python SDK
    # ══════════════════════════════════════════════════════════════════════════
    console.print()
    console.print(Rule("[bold]Interface 1 — Python SDK  (DB-API 2.0)[/bold]", style="green"))
    console.print()
    console.print(
        "[green]pip install cdata-connect-ai[/green]\n\n"
        "Standard DB-API interface — cursors, fetchall, pandas. "
        "No proprietary client to learn. Drops into any existing Python data stack.\n"
        "[dim]Source: Google Sheets / Sales Pipeline[/dim]"
    )
    console.print()
    console.print("[dim]Press Enter to run →[/dim]" if not AUTO else "")
    wait(0.8)

    # Show the code
    console.print(Syntax(SDK_CODE, "python", theme="monokai", line_numbers=False))
    console.print()
    console.print("[dim]Press Enter to execute →[/dim]" if not AUTO else "")
    wait(0.8)

    # Execute it live
    with console.status("[bold green]  Querying via Python SDK...[/bold green]", spinner="dots"):
        df = run_sdk_demo(email, token)

    console.print()
    console.print("[bold green]Result:[/bold green]")
    console.print()

    # Pretty-print the dataframe
    from rich.table import Table
    table = Table(show_header=True, header_style="bold cyan", border_style="dim")
    for col in df.columns:
        table.add_column(col)
    for _, row in df.iterrows():
        table.add_row(*[str(v) for v in row])
    console.print(table)

    console.print()
    console.print("[dim]Standard Python. Works with SQLAlchemy, pandas, any DB-API tool.[/dim]")
    console.print()
    console.print("[dim]Press Enter for Act 2 →[/dim]" if not AUTO else "")
    wait(1.5)

    # ══════════════════════════════════════════════════════════════════════════
    # ACT 2: MCP Agent
    # ══════════════════════════════════════════════════════════════════════════
    console.print()
    console.print(Rule("[bold]Interface 2 — MCP Agent  (Multi-Source)[/bold]", style="cyan"))
    console.print()
    console.print(
        "[cyan]CData Connect AI exposes a managed MCP server.[/cyan]\n\n"
        "The same 350+ source coverage — but now an AI agent can discover "
        "and call the right tools itself. No query authoring required.\n"
        "[dim]Sources: Google Sheets (pipeline) + PostgreSQL (customers)[/dim]"
    )
    console.print()

    # Connect MCP
    with console.status("[dim]Connecting to MCP server...[/dim]", spinner="dots"):
        from mcp_client import ConnectAIMCPClient
        mcp = ConnectAIMCPClient(email, token)
        tools = mcp.list_tools()

    console.print(f"[dim]MCP server: {len(tools)} tools available[/dim]")
    console.print()

    # Show the question
    console.print(Panel(
        f"[italic]\"{AGENT_QUERY}\"[/italic]",
        title="[bold]Natural Language Query[/bold]",
        border_style="cyan",
        expand=False,
    ))
    console.print()
    console.print("[dim]Press Enter to run →[/dim]" if not AUTO else "")
    wait(0.8)

    # Run the agent
    answer = run_agent_demo(mcp)

    console.print()
    console.print(Markdown(answer))
    console.print()
    console.print(
        "[dim]Same data, different interface. "
        "The agent picked the tools, issued the queries, and synthesized across sources.[/dim]"
    )
    console.print()

    # ── Close ─────────────────────────────────────────────────────────────────
    console.print(Rule(style="dim"))
    console.print()
    console.print(Panel.fit(
        "[bold]Two interfaces. One platform. 350+ sources.[/bold]\n"
        "[dim]Python SDK (DB-API) · MCP Agent · Same auth, same data[/dim]",
        border_style="dim",
    ))
    console.print()


if __name__ == "__main__":
    main()
