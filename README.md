# Enterprise Data AI Agent

A natural-language CLI agent for querying enterprise data via [CData Connect AI's](https://cloud.cdata.com) managed MCP server. Built as a first-session developer experience audit — I timed every step from zero to a working cross-source query, logged every friction point, and wrote up what I'd fix.

**Findings:** [docs/dx-audit.md](docs/dx-audit.md)  
**Interview presentation outline:** [docs/presentation-structure.md](docs/presentation-structure.md)

---

## What It Does

Ask questions in plain English. The agent routes queries through CData Connect AI's MCP server, which exposes 350+ data sources through a consistent SQL-queryable interface. No custom connectors. No per-source auth logic. Add a new source in the CData dashboard and it's immediately queryable — no code changes.

**Connected sources in this demo:**
- `SalesPipeline` — Google Sheets sales pipeline (20 opportunities, 4 reps, multi-region)
- `GitHub1` — GitHub repos, commit activity, issues
- `SampleConnection1` — PostgreSQL (Customers, Orders, StockItems)
- `SampleConnection2` — MySQL (same schema, different connection)

**Example queries:**
```
What's my total pipeline value by stage?
Who are my top 3 reps by open ARR?
Show me my most recently updated GitHub repos.
Cross-reference my top rep's deals with my public GitHub repos.
```

---

## Quick Start

```bash
make setup    # creates venv, installs deps, scaffolds .env
```

Then open `.env` and fill in your credentials (see [Credentials](#credentials) below), then:

```bash
make check    # verify all credentials are set
make demo     # run the scripted 3-act demo
make run      # interactive mode
```

---

## All Make Commands

| Command | What it does |
|---|---|
| `make setup` | Create venv, install dependencies, scaffold `.env` from `.env.example` |
| `make check` | Verify all required credentials are present in `.env` |
| `make run` | Launch interactive agent (type questions, `quit` to exit) |
| `make demo` | Scripted 3-act demo — press Enter to advance between acts |
| `make demo-auto` | Auto-advances without keypresses (good for screen recordings) |
| `make demo-fast` | Faster typing speed (good for rehearsal) |
| `make clean` | Remove `.venv` and caches |

---

## Manual Setup (without Make)

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# edit .env with your credentials
python main.py
```

> **Note:** `source .venv/bin/activate` is required each new terminal session. After activation, your prompt shows `(.venv)`.

---

## Credentials

Three environment variables required in `.env`:

| Variable | Where to get it |
|---|---|
| `CDATA_EMAIL` | The email address you used to sign up at [cloud.cdata.com](https://cloud.cdata.com) |
| `CDATA_ACCESS_TOKEN` | CData dashboard → Settings (gear icon) → Access Tokens → Create PAT |
| `ANTHROPIC_API_KEY` | [console.anthropic.com](https://console.anthropic.com) → API Keys |

> **Auth gotcha:** The `CDATA_EMAIL` must match your CData account email exactly — not a work email alias. The MCP server returns `"Failed to authenticate token"` if the username is wrong, which doesn't hint that the email is the issue. See [docs/dx-audit.md](docs/dx-audit.md).

---

## Scripted Demo

`demo.py` runs a three-act walkthrough:

- **Act 1** — Single source: Google Sheets pipeline query (total ARR by stage, top reps)
- **Act 2** — Second source: GitHub repos (different source type, same interface)
- **Act 3** — Cross-source: connects both sources in one query (the "aha" moment)

Queries are typed out character-by-character. Tool calls appear as dim progress lines. Results render as native terminal UI via `rich`.

```bash
make demo        # press Enter between acts — good for live presentations
make demo-auto   # auto-advances — good for screen recordings
```

---

## How It Works

```
You → main.py → agent.py (Anthropic SDK tool use) → mcp_client.py → CData MCP Server → data source
```

**`mcp_client.py`** — direct HTTP client for the CData MCP server at `https://mcp.cloud.cdata.com/mcp/`. Uses JSON-RPC 2.0 with SSE responses. Basic auth with base64(`email:PAT`). No CData SDK — just `requests`.

**`agent.py`** — agent loop using the standard Anthropic Python SDK. Claude receives available tools from the MCP server, decides which to call, and iterates until it has a complete answer. Uses `claude-sonnet-4-6`.

**`main.py`** — CLI entry point with `rich` terminal UI: spinner, dim tool progress lines, native markdown rendering.

**`demo.py`** — scripted walkthrough with typewriter effect and press-to-advance pacing.

---

## Project Structure

```
.
├── main.py                          # interactive + single-query CLI
├── demo.py                          # scripted 3-act demo
├── agent.py                         # Anthropic SDK agent loop
├── mcp_client.py                    # CData MCP HTTP client
├── requirements.txt
├── Makefile
├── .env.example
├── demo-data/
│   └── pipeline.csv                 # sample sales pipeline data (load into Google Sheets)
└── docs/
    ├── dx-audit.md                  # first-session developer experience audit
    ├── presentation-structure.md    # interview presentation outline
    └── screenshots/
        └── github-setup-guide-redundant-steps.png
```

---

## DX Audit Summary

Built and audited during a single session. Key findings:

1. **Wrong `Accept` header in all existing docs** — must be `application/json, text/event-stream`, not just `text/event-stream` (returns 406 otherwise)
2. **Setup guide shows steps you already completed** — contextual help panel on the connection page shows navigation steps, not auth steps
3. **Verbose schema metadata on every tool response** — bloats context, causes agents to appear hung on slower models
4. **No terminal-first setup path** — OAuth and PAT generation require browser dashboard; breaks AI coding assistant workflows
5. **Venv not mentioned in quickstart** — `ModuleNotFoundError` is the first thing new developers hit

Full details and recommended fixes: [docs/dx-audit.md](docs/dx-audit.md)
