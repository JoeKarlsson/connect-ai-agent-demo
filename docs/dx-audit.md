# Connect AI Developer Experience Audit
**Auditor:** Joe Karlsson  
**Date:** [fill in]  
**Account type:** Developer Edition (free tier)  
**Data sources connected:** [fill in]

---

## Time-to-First-API-Call

**Start time:** When I first landed on the developer docs  
**End time:** When I got a meaningful query result from the MCP server  
**Total: ~15 minutes** ✅ (under the 20-minute target)

### Step-by-step timeline

| Step | Time taken | Notes |
|------|-----------|-------|
| Account signup | ~2 min | Straightforward |
| Email verification | ~1 min | Fast |
| Connect first data source (Google Sheets) | ~3 min | OAuth flow was smooth and fast — positive surprise |
| Generate PAT / API token | ~2 min | Settings → Access Tokens, clear enough |
| First MCP server call | ~5 min | Auth debugging (wrong email, wrong Accept header — see Issues below) |
| First meaningful query result | ~2 min | Once connected, queries worked immediately |

---

## What Worked Without Friction

- MCP server endpoint (`https://mcp.cloud.cdata.com/mcp/`) is documented and accessible
- Basic auth pattern (email + PAT) works once credentials are correct
- Tool discovery (`tools/list`) returns rich, well-structured tool definitions
- Agent queries work end-to-end — multi-step reasoning works automatically with no SQL written
- Demo data sources (PostgreSQL, MySQL) are pre-connected, so there's something to query immediately
- **Google Sheets OAuth flow was genuinely smooth** — click, authorize, done. No token copying, no config files. This is a real strength worth highlighting in content.

---

## Where I Got Stuck

### Issue 1: Wrong `Accept` header breaks every copy-pasted implementation
**What happened:** Every example in CData's own GitHub repos and MCP docs sets `Accept: text/event-stream`. This returns a 406 with a message saying you must accept *both* `application/json` and `text/event-stream`. The correct header is `Accept: application/json, text/event-stream`.  
**How I resolved it:** Trial and error — tried the Bearer format first, then read the 406 error message carefully.  
**How long it took:** ~15 minutes  
**What the docs should say:** The quickstart and any code sample showing the `Accept` header needs to be corrected to `application/json, text/event-stream`. Every developer who copies the existing examples will hit this 406 immediately.

### Issue 3: Setup Guide shows navigation steps you already completed
**Screenshot:** `docs/screenshots/github-setup-guide-redundant-steps.png`  
**What happened:** On the connection setup page, the right-side "Setup Guide" panel opens with steps 1–3 highlighted: "Open the Sources page," "Click + Add Connection," "Type GitHub into the search field." These are the steps to *navigate to* the page you're already on. By the time you see this guide, you've already done all three steps. The panel should instead show what to do *next* — how to complete the authentication fields on the left.  
**Impact:** Confusing for a developer who's trying to figure out the OAuth flow. They scroll down to find the actual auth instructions, but the initial impression is that the help content is out of sync with where they are in the flow.  
**How long it took:** Minor friction — ~1 min of "wait, is this guide for me?" before scrolling past it.  
**What the fix should be:** The setup guide should detect that the user is already on the connection page and jump to step 4 ("On the Basic Settings tab…"). This is a contextual rendering problem — the guide doesn't know what step the user is on.

### Issue 2: 401 error doesn't tell you the *username* is wrong
**What happened:** Got `"Failed to authenticate token"` when using the wrong email address. The error says "token" which implies the PAT is wrong — not that the username is the problem.  
**How I resolved it:** Realized the account was registered under a personal Gmail, not the work email I had tried first.  
**How long it took:** ~10 minutes  
**What the docs should say:** Explicitly call out that the Basic auth username is the email address used to register the Connect AI account — not necessarily a work email or any other identity.

---

## Auth Setup Notes

<!-- OAuth flows, token formats, what credentials are required vs. optional -->

- Authentication method used: Basic auth (email + PAT)
- Where to generate the PAT: [fill in the exact Settings path]
- Token format/quirks: [fill in]
- Any session/expiry behavior: [fill in]

---

## Error Messages Encountered

| Error message | Root cause | Was it clear? |
|---------------|------------|--------------|
| `{"error":"UNAUTHORIZED","message":"Failed to authenticate token"}` | Wrong email — PAT is scoped to the account email used at `cloud.cdata.com` signup, not necessarily your work email | No — error doesn't hint that the username matters, only says "token" failed |
| `{"code":-32000,"message":"Not Acceptable: Client must accept both application/json and text/event-stream"}` | `Accept` header must be `application/json, text/event-stream` — `text/event-stream` alone returns 406 | No — the MCP docs and CData's own example repos only show `text/event-stream`. This will break every developer who copies the documented pattern. |

---

## Compared to Building This Yourself

**Time to connect one source via Connect AI:** [fill in]  
**Estimated time to build equivalent connector from scratch:** [fill in based on experience — be honest]  
**Main maintenance burden eliminated:** [fill in — OAuth handling? Schema drift? Rate limits?]

---

### Issue 6: No terminal-first setup path — dashboard required for OAuth and PAT generation
**What happened:** Setting up Connect AI with a coding agent (Claude Code, Cursor, etc.) requires multiple context switches to a browser:
1. Create account at cloud.cdata.com
2. Navigate dashboard UI to add a data source
3. Complete OAuth flow in browser
4. Navigate to Settings → Access Tokens to generate a PAT
5. Copy PAT back to terminal / .env file

Every one of these steps breaks the terminal-first workflow. For a developer using an AI coding assistant, each browser switch is a blocker — the agent loses context, the developer has to manually relay information back, and the setup process slows to a crawl.

**Why this matters for the CData CLI:** The CLI product is explicitly positioned as the "developer ergonomics layer for the AI-assisted coding era." A developer using Claude Code or Cursor to build a Connect AI integration should be able to do the entire setup without leaving the terminal:
```bash
cdata auth login                        # browser OAuth once, token stored locally
cdata sources add google-sheets         # launches OAuth flow, handles callback
cdata sources add github --token $PAT   # PAT-based sources via flag
cdata token create --name "my-agent"    # generate Connect AI PAT from CLI
cdata sources list                      # verify what's connected
```
This is the pattern developers expect from modern CLI tools (Vercel, Stripe, Heroku, GitHub CLI). Without it, Connect AI has a "last mile" problem for the exact audience the Developer Edition targets.

**Priority:** High. This is a product roadmap item for CLI GA, not a docs fix — but it's the single biggest friction point for developers building with AI coding assistants.

### Issue 5: Tool responses embed verbose schema metadata on every call
**What happened:** Every `queryData` or `getTables` response includes a full `schema` array per row — column names, data types, catalog/schema/table names, ordinals, labels. This is useful once but gets sent back to the LLM on every tool call, bloating the context significantly and making agentic queries slow (or appear to hang).  
**Impact:** With `claude-opus-4-7`, a simple query appeared to hang indefinitely. Switching to Sonnet and stripping the `schema` key from responses made the same query return in ~3 seconds.  
**Recommended fix:** Either make schema metadata opt-in via a query parameter (`?includeSchema=false`), or only return it on the first call per session. Developers building agents shouldn't have to work around this manually.

### Issue 4: No virtual environment guidance in quickstart
**What happened:** Running `python main.py` after following setup instructions returns `ModuleNotFoundError: No module named 'dotenv'` because the system Python doesn't have the dependencies — the venv does. The quickstart doesn't mention activating the venv.  
**How I resolved it:** `source .venv/bin/activate` then re-run.  
**What the docs should say:** Any Python quickstart needs to include `source .venv/bin/activate` as an explicit step, and note that it's required each new terminal session. This is a classic first-session stumble that affects every new developer.

---

## Top 5 DX Improvements I'd Prioritize

Ranked by impact on time-to-first-API-call:

1. **Fix the `Accept` header in all docs and example repos** — Every copy-pasted implementation from CData's own GitHub repos returns a 406 immediately because the documented header (`Accept: text/event-stream`) is wrong. The correct value is `Accept: application/json, text/event-stream`. This is a one-line fix that unblocks every developer who follows the documented path. Until this is fixed, the quickstart is broken by default.

2. **Rewrite the 401 error to say the username is wrong, not the token** — The current error (`"Failed to authenticate token"`) implies the PAT is invalid. The actual cause is usually a wrong email address — developers use a work email when the account was registered with a personal Gmail. The error response should say: `"Authentication failed: check that your username matches the email address used to register at cloud.cdata.com"`. This alone eliminates ~10 minutes of debugging from the average first session.

3. **Add `source .venv/bin/activate` as an explicit step in every Python quickstart** — Missing from current docs. Every developer hitting this for the first time on Python 3.12+ gets a `ModuleNotFoundError` because they're running system Python. This is the most common first-session stumble for Python tooling and takes one sentence to prevent.

4. **Fix the setup guide contextual rendering** — The right-panel "Setup Guide" on the connection setup page shows steps 1–3 ("Open the Sources page," "Click + Add Connection," "Type GitHub into the search field") to a developer who has already completed those steps to arrive at the page. The guide should detect the current page context and jump to step 4. Minor friction individually, but it signals the docs are out of sync with where the user actually is.

5. **Make schema metadata opt-in in tool responses** — Every `queryData` response includes a full `schema` array per row (column names, data types, ordinals, catalog/schema/table names). This metadata is useful once but inflates every subsequent tool call, bloating LLM context and causing apparent hangs with larger models. Adding a `?includeSchema=false` query parameter (or only returning schema on the first call per session) would make agent-based queries significantly faster without changing the default behavior for existing integrations.

---

## What I'd Ship in the First 30 Days

The DX fixes above are quick wins — file them as bugs, ship them inside week one. The 30-day plan is bigger: audit everything before publishing anything new.

### Week 1–2: Quick wins + audit kickoff

**DX fixes (ship immediately — don't wait):**
- [x] Fix `Accept` header across all docs and example repos
- [ ] Rewrite 401 error message to surface username mismatch
- [ ] Add `source .venv/bin/activate` to Python quickstart

**Audit kickoff (running in parallel):**
- [ ] **Marketing website audit** — walk every developer-facing page cold. Does the above-the-fold copy make the SQL-queryable / live connectivity / enterprise depth story legible? Is the Composio comparison addressable? What's the time-to-understanding for a developer who lands from a Google search vs. an LLM referral?
- [ ] **Channel audit** — inventory every active channel: newsletter cadence + open rates, social (LinkedIn, Twitter/X, YouTube), developer community (Discord, Slack, Stack Overflow presence). What's publishing? What's performing? What went dark?
- [ ] **Documentation coverage audit** — which connectors have full tutorials vs. stubs? Which auth patterns (OAuth, API key, SSO, service accounts) are documented with working examples vs. described in one sentence? Where are developers dropping off in the docs funnel?

### Week 3–4: Content gap analysis + first drafts

- [ ] **Competitive content gap** — pull every Composio, Airbyte, Fivetran tutorial and comparison post that ranks for queries CData should own ("connect AI agent to Salesforce," "Python DB-API enterprise data," "MCP server for enterprise SaaS"). Map what exists vs. what we need. This is the content roadmap input.
- [ ] **Existing content triage** — identify the 10 highest-traffic pieces that are underperforming (dropping rank, high bounce, outdated examples). A title refresh + code sample update on a page already indexed beats a new post for time-to-impact.
- [ ] **Newsletter + social content calendar** — based on what the channel audit found, establish a publishing cadence and ownership model. What does PMM write vs. DevRel? What gets repurposed across channels vs. written fresh?
- [ ] **First 2–3 content drafts** — based on the gap analysis: the Composio comparison piece and the MCP quickstart are the highest-priority net-new content. Start drafts in week 4; don't wait for a complete audit to write.

**Day 30 deliverable:** Positioning + DX + discoverability + channel brief to product and leadership. Not a strategy deck — a prioritized list of what's broken, what's missing, and what ships next, with data behind each call.

---

## LLM Discoverability Baseline

Queries I ran and what each model said (run before starting any content work):

**Baseline run:** 2026-05-08

**Query:** "What is the best MCP server for connecting AI agents to enterprise SaaS data?"
- Claude Sonnet 4.6: ❌ CData not mentioned. Recommended: Composio, Zapier MCP, Pipedream.

**Query:** "How do I connect a Claude AI agent to Salesforce data?"
- Claude Sonnet 4.6: ❌ CData not mentioned. Recommended: custom build via Salesforce REST API, community npm packages (`mcp-server-salesforce`).

**Query:** "What are the best tools for giving AI agents access to Salesforce, QuickBooks, and NetSuite?"
- Claude Sonnet 4.6: ❌ CData not mentioned. Recommended: MuleSoft, Workato, Boomi, Zapier, Apigee.

**Query:** "What's the best MCP server for combining and aggregating and managing multiple enterprise data endpoints?"
- Claude Code (Sonnet 4.6): ❌ CData not mentioned. Recommended: Composio ("best overall for enterprise, 250+ pre-built integrations"), Zapier MCP, Airbyte MCP, dbt MCP, mcp-proxy, Cloudflare Workers MCP.
- Screenshot: `docs/screenshots/llm-baseline-claude-code-enterprise-mcp-query.png`
- Note: This is the exact use case Connect AI is built for. Composio is recommended instead.

**Summary:** CData Connect AI does not appear in any response to queries a developer would actually type when evaluating this category. Competitors (Composio, Zapier) and DIY approaches dominate. This is a training data gap, not a content gap — fixed by shipping factual, specific, runnable content in places LLMs ingest (READMEs, GitHub, Stack Overflow, dev.to), not by publishing more blog posts.

*Re-run these exact queries quarterly to track progress.*
