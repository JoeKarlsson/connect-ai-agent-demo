# Enterprise Data AI Agent

A natural-language interface to enterprise data sources via [CData Connect AI's](https://connect.cdata.com) managed MCP server.

Built as a first-session developer experience audit — I timed how long it took to get from zero to a working query, logged every friction point, and wrote up what I'd fix. Findings in [docs/dx-audit.md](docs/dx-audit.md).

## What It Does

Ask questions about your connected data in plain English. The agent routes your query through CData Connect AI's MCP server, which exposes 350+ data sources (Salesforce, QuickBooks, Google Sheets, etc.) through a consistent SQL-queryable interface.

```
You: What are my top 5 open opportunities by revenue?

Agent: Here are your top 5 open opportunities:
1. Acme Corp — $240,000 (Close date: 2026-06-15)
2. ...
```

The same agent works against any source you've connected in your CData account — no code changes required.

## Setup

**Prerequisites:**
- Python 3.11+
- [CData Connect AI](https://connect.cdata.com) account (free Developer Edition)
- At least one data source connected in your CData account
- [Anthropic API key](https://console.anthropic.com)

**1. Install dependencies**

```bash
pip install -r requirements.txt
```

**2. Configure credentials**

```bash
cp .env.example .env
```

Edit `.env`:
- `CDATA_EMAIL` — your CData account email
- `CDATA_ACCESS_TOKEN` — generate a Personal Access Token from Settings → API Access Tokens in the CData dashboard
- `ANTHROPIC_API_KEY` — your Anthropic API key

**3. Run it**

Interactive mode:
```bash
python main.py
```

Single query:
```bash
python main.py "show me all accounts created this month"
```

## How It Works

```
You → main.py → agent.py (Anthropic SDK) → mcp_client.py → CData MCP Server → your data source
```

The MCP client connects to `https://mcp.cloud.cdata.com/mcp/` using Basic auth (email + PAT). It discovers the available tools from your connected sources, then passes them to Claude as tool definitions. Claude decides which tools to call based on your query, the MCP client executes them, and the results come back as a natural-language answer.

No custom connector code. No per-source auth logic. One agent that works against any of your connected sources.

## Implementation Notes

`mcp_client.py` — direct HTTP client for the CData MCP server. Uses JSON-RPC 2.0 with SSE responses. No CData SDK required — just `requests`.

`agent.py` — agent loop using the standard Anthropic Python SDK. Tool use is handled manually (no agent framework) so the control flow is easy to follow and extend.

`main.py` — CLI entry point. Interactive and single-query modes.

## What I Learned Building This

See [docs/dx-audit.md](docs/dx-audit.md) for the full first-session experience audit, including time-to-first-API-call, every friction point I hit, and 5 specific DX improvements I'd prioritize.

The short version: the MCP path is genuinely fast to get running once you know where to find your PAT. The part that took longer than it should have was [fill in after your actual experience].
