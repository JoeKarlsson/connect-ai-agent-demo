# Enterprise Data AI Agent — Project Context

## What This Is

A demo project built to support a final-round interview for the Principal Developer Marketing Manager role at CData. It serves two purposes:

1. **Interview artifact** — a working AI agent that queries enterprise data via CData Connect AI's MCP server, used to demonstrate hands-on technical credibility
2. **DX audit** — a documented first-session developer experience audit of CData Connect AI, with specific bugs, friction points, and improvement recommendations

The GitHub repo is public: https://github.com/JoeKarlsson/connect-ai-agent-demo

---

## Running the Project

```bash
make setup    # first time only
make check    # verify credentials
make demo     # scripted 3-act presentation demo
make run      # interactive agent
```

Credentials are in `.env` (not committed). All three are required:
- `CDATA_EMAIL` — joekarlsson1@gmail.com (the Gmail used for the CData account)
- `CDATA_ACCESS_TOKEN` — CData personal access token
- `ANTHROPIC_API_KEY` — Anthropic API key

## Key Files

| File | Purpose |
|---|---|
| `main.py` | CLI entry point — rich terminal UI, interactive + single-query modes |
| `demo.py` | Scripted 3-act demo with typewriter effect and press-to-advance |
| `agent.py` | Anthropic SDK agent loop with tool use. Uses `claude-sonnet-4-6`. |
| `mcp_client.py` | HTTP client for CData MCP server (`https://mcp.cloud.cdata.com/mcp/`) |
| `docs/dx-audit.md` | First-session DX audit — real findings, timings, recommended fixes |
| `docs/presentation-structure.md` | Full interview presentation outline with talking points and Q&A prep |

## Connected Data Sources

- **SalesPipeline** (Google Sheets) — 20 demo opportunities, 4 reps, multi-region pipeline
- **GitHub1** (GitHub) — Joe's personal GitHub account
- **SampleConnection1** (PostgreSQL) — CData demo data (Customers, Orders, StockItems)
- **SampleConnection2** (MySQL) — same schema, different connection

## Technical Notes

- MCP server auth: Basic auth with `base64(email:PAT)`. Accept header must be `application/json, text/event-stream` (not just SSE — this is a bug in CData's own docs).
- Tool responses include verbose schema metadata — `mcp_client.py` strips the `schema` key to keep context small.
- `agent.py` has a system prompt telling Claude the available sources and table names so it skips the discovery phase (reduces tool call rounds from ~10 to ~3).
- Python 3.14 requires a venv — cannot install into system Python.

## Interview Context

- **Role:** Principal Developer Marketing Manager at CData Software
- **Interview format:** 20-min presentation + 10-min Q&A with product marketing, sales, and product leadership
- **Part 1:** Developer positioning — frame the "N-integration debt" problem, map CData's value props to real engineer trade-offs
- **Part 2:** 90-day GTM plan — three distribution surfaces (human devs, search, LLMs), DX audit → fix before publish, DevRel/PMM split

The dx-audit.md and this working demo are the primary artifacts for the presentation. The positioning and 90-day plan are in `docs/presentation-structure.md`.
