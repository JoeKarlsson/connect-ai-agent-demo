# Enterprise Data AI Agent

A demo built to show two distinct ways to connect enterprise data with Python — CData Connect AI's **Python SDK** (DB-API 2.0) and its **managed MCP server** — querying multiple live sources in a single session. Built as a first-session developer experience audit: I timed every step from zero to a working cross-source query, logged every friction point, and wrote up what I'd fix.

**Findings:** [docs/dx-audit.md](docs/dx-audit.md)  
**Interview presentation outline:** [docs/presentation-structure.md](docs/presentation-structure.md)

---

## What It Does

Two interfaces to the same platform:

**Python SDK (DB-API 2.0)** — `pip install cdata-connect-ai`. Standard cursor interface. Works with pandas, SQLAlchemy, and any existing Python data stack. No proprietary client to learn.

**MCP Agent** — CData Connect AI exposes a managed MCP server. Claude receives available tools, decides which sources to query, and synthesizes answers across them. Natural language in, structured analysis out.

**Connected sources in this demo:**
- `GoogleSheets1` — Google Sheets sales pipeline (20 opportunities, 4 reps, multi-region)
- `GitHub1` — GitHub repos, commits, issues, pull requests
- `SampleConnection1` — PostgreSQL (Customers, Orders, StockItems)
- `SampleConnection2` — MySQL (same schema, different connection)

---

## Quick Start

```bash
make setup    # creates venv, installs deps, scaffolds .env
```

Then open `.env` and fill in your credentials (see [Credentials](#credentials) below), then:

```bash
make check    # verify all credentials are set
make demo     # scripted two-act demo
make run      # interactive mode
```

---

## All Make Commands

| Command | What it does |
|---|---|
| `make setup` | Create venv, install dependencies, scaffold `.env` from `.env.example` |
| `make check` | Verify all required credentials are present in `.env` |
| `make run` | Launch interactive agent (type questions, `quit` to exit) |
| `make demo` | Scripted demo — press Enter to advance between acts |
| `make demo-auto` | Auto-advances without keypresses (good for screen recordings) |
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

`demo.py` runs a two-act walkthrough — one act per interface:

- **Act 1 — Python SDK (DB-API):** Connects via `cdata_connect_ai`, runs a SQL query against the Google Sheets pipeline, returns a pandas DataFrame. Shows the code, then executes it live.
- **Act 2 — MCP Agent (multi-source):** Connects to the MCP server, takes a natural language question spanning Google Sheets + PostgreSQL, lets Claude issue the tool calls, and synthesizes a cross-source answer.

```bash
make demo        # press Enter between acts — good for live presentations
make demo-auto   # auto-advances — good for screen recordings
```

---

## How It Works

```
Interactive mode:
  You → main.py → agent.py (Anthropic SDK tool use) → mcp_client.py → CData MCP Server → data source

SDK mode:
  demo.py → cdata_connect_ai (DB-API cursor) → CData Connect AI API → data source
```

**`mcp_client.py`** — HTTP client for the CData MCP server at `https://mcp.cloud.cdata.com/mcp/`. JSON-RPC 2.0 over SSE. Basic auth with base64(`email:PAT`).

**`agent.py`** — agent loop using the Anthropic Python SDK. Claude receives the MCP tool list, decides which to call, and iterates until it has a complete answer. Uses `claude-sonnet-4-6`.

**`main.py`** — CLI entry point: spinner, dim tool progress lines, markdown rendering via `rich`.

**`demo.py`** — two-act scripted demo. Act 1 shows the Python SDK (DB-API) with live code execution. Act 2 shows the MCP agent doing a cross-source natural language query.

---

## Project Structure

```
.
├── main.py                          # interactive + single-query CLI
├── demo.py                          # scripted two-act demo (SDK + MCP)
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
