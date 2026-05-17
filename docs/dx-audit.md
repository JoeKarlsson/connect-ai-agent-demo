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
**What the docs should say:** The quickstart and any code sample showing the `Accept` header needs to be corrected to `application/json, text/event-stream`. Every developer who copies the existing examples will hit this 406 immediately. This is not a CData-specific quirk — the MCP Streamable HTTP spec (2025-03-26) mandates the combined header, and the same 406 has been independently filed against the Anthropic Claude SDK ([#202](https://github.com/anthropics/claude-agent-sdk-typescript/issues/202)), Composio ([#2152](https://github.com/ComposioHQ/composio/issues/2152)), and the model-context-protocol Python SDK ([#1641](https://github.com/modelcontextprotocol/python-sdk/issues/1641)). CData's documentation makes no mention of the `Accept` header requirement anywhere — the docs that do exist show only `text/event-stream`.

**Remediation:**
- *Content (PMM/DevRel):* Update every code sample in docs.cloud.cdata.com, both GitHub READMEs (`connectcloud-mcp-server`, `cdata-jdbc-mcp-server`), and any blog posts or tutorials that show the `Accept` header. Add a "known issue" callout on the MCP docs page while the fix propagates. File as P0 bug with Engineering so it is tracked alongside the content fix.
- *Engineering:* Accept `text/event-stream` alone as a valid header (return the SSE stream without requiring `application/json`), or return a 400 with the correct header value stated explicitly in the response body so the error is self-documenting.

### Issue 3: Setup Guide shows navigation steps you already completed
**Screenshot:** `docs/screenshots/github-setup-guide-redundant-steps.png`  
**What happened:** On the connection setup page, the right-side "Setup Guide" panel opens with steps 1–3 highlighted: "Open the Sources page," "Click + Add Connection," "Type GitHub into the search field." These are the steps to *navigate to* the page you're already on. By the time you see this guide, you've already done all three steps. The panel should instead show what to do *next* — how to complete the authentication fields on the left.  
**Impact:** Confusing for a developer who's trying to figure out the OAuth flow. They scroll down to find the actual auth instructions, but the initial impression is that the help content is out of sync with where they are in the flow.  
**How long it took:** Minor friction — ~1 min of "wait, is this guide for me?" before scrolling past it.  
**What the fix should be:** The setup guide should detect that the user is already on the connection page and jump to step 4 ("On the Basic Settings tab…"). This is a contextual rendering problem — the guide doesn't know what step the user is on.

**Remediation:**
- *Content (PMM/DevRel):* Rewrite the setup guide panel text for the connection page so it starts at step 4 ("On the Basic Settings tab…") — the actual next action for a developer who has already navigated to the page.
- *Engineering:* Detect the user's current page context and render the corresponding guide step rather than always starting at step 1. This is a contextual rendering fix in the guide panel component.

### Issue 2: 401 error doesn't tell you the *username* is wrong
**What happened:** Got `"Failed to authenticate token"` when using the wrong email address. The error says "token" which implies the PAT is wrong — not that the username is the problem.  
**How I resolved it:** Realized the account was registered under a personal Gmail, not the work email I had tried first.  
**How long it took:** ~10 minutes  
**What the docs should say:** Explicitly call out that the Basic auth username is the email address used to register the Connect AI account — not necessarily a work email or any other identity.

**Remediation:**
- *Content (PMM/DevRel):* Add an explicit callout to the auth docs and every quickstart: "Your username is the email address used to register at cloud.cdata.com — not necessarily a work email."
- *Engineering:* Update the 401 error message to distinguish username failure from token failure, e.g.: `"Authentication failed: verify that your username matches the email address used to register at cloud.cdata.com"`.

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

**Remediation:**
- *Content (PMM/DevRel):* Write a "setting up CData with AI coding assistants" guide that walks through the current browser-based flow step by step, acknowledges the context-switching limitation, and positions the upcoming CLI as the long-term fix. Coordinate with Engineering on launch content for CLI GA.
- *Engineering (roadmap):* Ship `cdata auth login`, `cdata sources add`, and `cdata token create` CLI commands following the pattern established by Vercel CLI, GitHub CLI, and Stripe CLI. This is the single highest-impact product investment for the AI-assisted developer audience.

### Issue 5: Tool responses embed verbose schema metadata on every call
**What happened:** Every `queryData` or `getTables` response includes a full `schema` array per row — column names, data types, catalog/schema/table names, ordinals, labels. This is useful once but gets sent back to the LLM on every tool call, bloating the context significantly and making agentic queries slow (or appear to hang).  
**Impact:** With `claude-opus-4-7`, a simple query appeared to hang indefinitely. Switching to Sonnet and stripping the `schema` key from responses made the same query return in ~3 seconds.  
**Recommended fix:** Either make schema metadata opt-in via a query parameter (`?includeSchema=false`), or only return it on the first call per session. Developers building agents shouldn't have to work around this manually.

**Remediation:**
- *Content (PMM/DevRel):* Publish an "optimizing agent performance with CData Connect AI" guide showing the schema-stripping pattern and explaining the context window impact of verbose tool responses. Link from the MCP docs page as recommended reading for developers building production agents.
- *Engineering:* Add a `?includeSchema=false` query parameter to `queryData` (or make schema opt-in per session via a handshake parameter). This is the architectural fix; the content guide bridges the gap until it ships.

### Issue 4: No virtual environment guidance in quickstart
**What happened:** Running `python main.py` after following setup instructions returns `ModuleNotFoundError: No module named 'dotenv'` because the system Python doesn't have the dependencies — the venv does. The quickstart doesn't mention activating the venv.  
**How I resolved it:** `source .venv/bin/activate` then re-run.  
**What the docs should say:** Any Python quickstart needs to include `source .venv/bin/activate` as an explicit step, and note that it's required each new terminal session. This is a classic first-session stumble that affects every new developer. The Python Client documentation ([docs.cloud.cdata.com/Python-Client.html](https://docs.cloud.cdata.com/Python-Client.html)) lists prerequisites (Python ≥3.10, `requests`, `ijson`) and proceeds directly to `pip install cdata-connect-ai` with no mention of creating or activating a virtual environment.

**Remediation:**
- *Content (PMM/DevRel):* Add `source .venv/bin/activate` (macOS/Linux) and `.venv\Scripts\activate` (Windows) as explicit numbered steps in every Python quickstart. Add a callout: "You'll need to activate the virtual environment in each new terminal session."
- *Engineering:* None — docs-only fix.

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

---

## Agentic Documentation Gap

Documentation is one of the most important marketing investments for a developer tool in 2025 — not because humans read it, but because AI agents do. When a developer asks Claude Code, Cursor, or Perplexity "how do I connect my agent to Salesforce," the model retrieves from its training data and from indexed, structured documentation. Products that structure their documentation for AI retrieval get recommended. Products that don't, don't.

CData has started this work — but only partially. The gaps are specific and fixable.

### llms.txt — exists but coverage is poor

CData publishes [cdata.com/llms.txt](https://www.cdata.com/llms.txt) on the marketing domain. This is good — the file exists and signals intent. The problem is coverage: the file does not surface Connect AI specifically, does not explain how CData differs from Composio (SQL vs. action-based, enterprise depth, data engineering path), and does not point agents to the quickstart, MCP docs, or connector list in a token-efficient way. The docs domain publishes [docs.cloud.cdata.com/llms.txt](https://docs.cloud.cdata.com/llms.txt) as a documentation index — the MCP docs even instruct agents to fetch it. But a 300-page sitemap is not the same as a curated LLM guide. A developer asking an AI assistant what CData does gets noise from a sitemap; they get a clear answer from Composio's concise [composio.dev/llms.txt](https://composio.dev/llms.txt).

The fix is not to add a file — it's to rewrite the existing one. The marketing llms.txt needs a concise product description, the SQL vs. action-based differentiation, the quickstart URL, the MCP docs URL, and the enterprise source list. `llms-full.txt` should serialize the complete Connect AI doc set. One week of work; immediate impact on every AI assistant recommendation.

### Agent-readiness audit — nine missing signals

Beyond llms.txt, [isitagentready.com](https://isitagentready.com/www.cdata.com) audits cdata.com against the emerging standards for AI agent discoverability. As of the date of this audit, cdata.com fails on nine distinct checks:

**1. Link response headers for agent discovery (RFC 8288)**  
Link headers are present but contain no agent-useful relation types. Fix: add `Link: </.well-known/api-catalog>; rel="api-catalog"` to advertise the API catalog, and `Link: </docs/api>; rel="service-doc"` for API documentation. Spec: [RFC 8288](https://www.rfc-editor.org/rfc/rfc8288), [RFC 9727 §3](https://www.rfc-editor.org/rfc/rfc9727#section-3).

**2. Markdown negotiation for agents**  
Requests with `Accept: text/markdown` return HTTP 403. AI agents that request markdown representations of HTML pages (for more efficient parsing) get blocked entirely. Fix: enable Cloudflare's Markdown for Agents or equivalent so `Accept: text/markdown` returns a markdown version while HTML stays the default for browsers. Docs: [Cloudflare Markdown for Agents](https://developers.cloudflare.com/fundamentals/reference/markdown-for-agents/).

**3. Content Signals in robots.txt**  
No `Content-Signal` directives in robots.txt. These declare AI content usage preferences — whether the site allows AI training, search indexing, and AI input. Fix: add `Content-Signal: ai-train=no, search=yes, ai-input=no` (or the appropriate preferences). Without this, CData has no declared position on AI usage of its content. Spec: [contentsignals.org](https://contentsignals.org/).

**4. API catalog (RFC 9727)**  
No `/.well-known/api-catalog` endpoint. This is how agents programmatically discover APIs — what endpoints exist, where the OpenAPI spec lives, where the docs live, and where the health endpoint is. Fix: create `/.well-known/api-catalog` returning `application/linkset+json` with entries for the Connect AI REST API, MCP endpoint, and Python SDK. Spec: [RFC 9727](https://www.rfc-editor.org/rfc/rfc9727).

**5. OAuth/OIDC discovery metadata**  
No `/.well-known/openid-configuration` or `/.well-known/oauth-authorization-server`. Agents that need to authenticate with CData's APIs cannot programmatically discover how to do so — they have to read documentation and hardcode endpoints. Fix: publish the standard discovery document with `issuer`, `authorization_endpoint`, `token_endpoint`, `jwks_uri`, and `grant_types_supported`. Spec: [RFC 8414](https://www.rfc-editor.org/rfc/rfc8414).

**6. OAuth Protected Resource Metadata**  
No `/.well-known/oauth-protected-resource`. This tells agents which OAuth servers can issue tokens for CData's APIs and what scopes are supported. Without it, agents cannot discover how to obtain access tokens without reading docs. Spec: [RFC 9728](https://www.rfc-editor.org/rfc/rfc9728).

**7. MCP Server Card**  
No `/.well-known/mcp/server-card.json`. This is the emerging standard (SEP-1649) for advertising an MCP server's existence, transport endpoint, and capabilities at a well-known URL. AI agents and MCP clients that support discovery will automatically find and configure CData's MCP server if this file exists. Fix: publish the server card with `serverInfo`, transport endpoint, and capabilities. Spec: [MCP Server Card PR #2127](https://github.com/modelcontextprotocol/modelcontextprotocol/pull/2127).

**8. Agent skills discovery index**  
No `/.well-known/agent-skills/index.json`. This index declares what programmatic capabilities the site exposes to agents — what they can do, not just what they can read. Fix: publish the skills index per the Agent Skills Discovery RFC v0.2.0 with a `$schema` field and a `skills` array. Spec: [agentskills.io](https://agentskills.io/).

**9. WebMCP**  
No `navigator.modelContext.provideContext()` calls detected. WebMCP allows a website to expose tool definitions directly to AI agents running in the browser — every page load can tell an agent what actions are available. Fix: implement WebMCP with tool definitions for Connect AI's key actions (query data, add a source, generate a token). Docs: [Chrome WebMCP](https://developer.chrome.com/blog/webmcp-epp).

### What this means in practice

Each of these nine gaps is a place where an AI agent — Claude Code, Cursor, a browser-based assistant — tries to understand what CData is and how to work with it, and fails silently. Composio has engineered its discoverability across most of these vectors. CData has started with llms.txt but has not yet addressed the protocol-level signals that agents use for discovery.

The LLM discoverability baseline (five queries, zero CData appearances) is partly a training data problem and partly this: agents that could discover CData automatically, via well-known endpoints and Link headers, cannot. Fixing this layer costs days of engineering work and has immediate, compounding impact on every AI assistant recommendation — faster than any content program.

**Priority order:** llms.txt rewrite (content, one week) → API catalog + OAuth discovery (engineering, one sprint) → MCP Server Card (engineering, one day once the spec finalizes) → Link headers + Content Signals + Markdown negotiation (engineering, hours each).

---

## Production Readiness Findings

The following issues were identified through documentation review, GitHub repository inspection, and community thread research (2026-05-14). These are distinct from the first-session DX issues above — they are architectural or policy gaps that block production deployment, not evaluation friction.

---

### Issue 7: Rate limit is a shared per-user ceiling, not per-connection — and is absent from MCP documentation

**What the developer hits:** The rate limit is 100 requests/user/minute for query operations and 500/user/minute for metadata operations. This ceiling is shared across all connected data sources simultaneously. An agent querying Salesforce, NetSuite, and SAP in parallel can silently starve one connection while the others consume the budget. There is no in-protocol signal that rate limiting is the cause of missing results — the agent simply stops receiving data.  
**Source:** [docs.cloud.cdata.com/FAQs.html](https://docs.cloud.cdata.com/FAQs.html) — *"100 requests per user per minute for regular queries and 500 requests per user per minute for metadata queries. These limits apply across all data sources collectively. If a user consumes 70 requests to one connection within a minute, only 30 requests remain available for other connections that same minute."* Also appears in the Microsoft Learn connector reference as "100 API calls per connection per 60 seconds." The MCP documentation page (`docs.cloud.cdata.com/en/API/MCP`) contains no mention of rate limits.  
**Priority:** High. Multi-source analysis is the core advertised use case. Silent failure with no diagnostic signal is a production trust-breaker.

**Remediation:**
- *Content (PMM/DevRel):* Add a "Rate Limits" section to the MCP documentation page with the per-minute ceilings and a clear note that the limit is shared across all sources simultaneously. Publish a "multi-source query patterns" guide recommending sequential over parallel source queries when the budget is tight.
- *Engineering:* Return rate limit headers on MCP responses (`X-RateLimit-Remaining`, `Retry-After`) so agents can detect and respond to rate limiting rather than receiving silent empty results. Add a real-time rate limit counter to the dashboard.

---

### Issue 8: Cross-source JOINs are client-side federation — full result sets pulled before filtering

**What the developer hits:** The SQL Reference confirms cross-source JOINs execute as separate per-source queries with results aggregated client-side before the JOIN is applied. Joining a 500K-row Salesforce table to a 200K-row NetSuite table means 700K rows transferred before any filter runs. Marketing copy implies seamless federation with no caveats; the SQL Reference footnotes the constraint.  
**Source:** [docs.cloud.cdata.com/SQL-Reference.html](https://docs.cloud.cdata.com/SQL-Reference.html) — *"Large federated queries can take longer to execute than single-source queries because Connect AI must receive the data from each source individually."* and *"Federated queries act as individual queries to each data source."* Marketing copy implies seamless federation with no caveats; this constraint appears only in the SQL Reference footnotes.  
**Priority:** High. This is the pattern most likely to trigger both the rate limit (Issue 7) and the 30-second timeout (Issue 9) simultaneously, with no advance warning to the developer.

**Remediation:**
- *Content (PMM/DevRel):* Add a prominent callout in the SQL Reference: "Cross-source JOINs transfer full result sets from each source before filtering. Always filter within each source query first." Publish a "federated query performance guide" with before/after SQL patterns showing predicate push-down.
- *Engineering:* Investigate server-side predicate push-down for cross-source JOINs. At minimum, surface the constraint in the `queryData` tool description so agents have the guidance without reading the SQL Reference.

---

### Issue 9: Default query timeout is 30 seconds with GUI-only override — no API or MCP tool parameter

**What the developer hits:** The default per-query timeout is 30 seconds, configurable only through the Advanced Settings tab in the dashboard UI, per-connection, manually. The `queryData` MCP tool has no timeout parameter. A community thread documents the exact error: `[ERROR] Execution of the SELECT query failed. Error: Timeout when wait response.`  
**Source:** [community.cdata.com/cdata-connect-ai-98/timeout-error-in-connect-ai-174](https://community.cdata.com/cdata-connect-ai-98/timeout-error-in-connect-ai-174) — *"The default value for the timeout in the Advanced Settings Tab is 30 seconds."* The REST API `/query` endpoint does expose a `timeout` parameter (1–300 second range, documented at [docs.cloud.cdata.com/Query-Operation.html](https://docs.cloud.cdata.com/Query-Operation.html)), but the MCP `queryData` tool exposes no equivalent — whether the MCP layer passes the REST timeout through is not documented anywhere.  
**Priority:** High. Enterprise queries against SAP, Workday, and Oracle regularly exceed 30 seconds. The only documented fix requires a manual dashboard action with no API or IaC equivalent.

**Remediation:**
- *Content (PMM/DevRel):* Document the 30-second default timeout and the dashboard override path in both the MCP docs and the Query Operation reference. Add a troubleshooting entry: "Query timed out? Increase the per-connection timeout under Advanced Settings in the dashboard."
- *Engineering:* Add a `timeout` parameter to the `queryData` MCP tool (capped at 300 seconds, matching the REST API). Expose timeout configuration via the API so it can be set programmatically without dashboard access.

---

### Issue 10: PATs have no scoping — one token grants full read/write to all connected sources

**What the developer hits:** Personal Access Tokens cannot be scoped to read-only operations or to specific connections. One PAT = full read/write access to all 350+ connected sources on the account. There is no mechanism to issue a least-privilege credential to an LLM agent querying production financial data. The auth documentation ([docs.cloud.cdata.com/Authentication.html](https://docs.cloud.cdata.com/Authentication.html)) describes only Basic Auth with no mention of scoping. The pricing page ([cdata.com/ai/pricing/](https://cdata.com/ai/pricing/)) confirms that "Source-Level Permissions" and "Per-User Authentication" are Business-tier-only features — meaning Standard and Growth tier PATs have no fine-grained scoping by design. The SQL Reference documents that `queryData` supports SELECT, INSERT, UPDATE, DELETE, and EXEC, confirming write access is available to any valid token.  
**Priority:** High. Enterprise security reviews require least-privilege credential issuance. This is not a paperwork problem — it is an architectural gap that will block production approvals.

**Remediation:**
- *Content (PMM/DevRel):* Document the current PAT limitation clearly in the auth docs. Reference the JWT embed API (Business tier) as the scoping mechanism for enterprise deployments. Publish a "production security guide" covering recommended mitigations: dedicated accounts per agent, minimal source connections per account.
- *Engineering (roadmap):* Add read-only and connection-level scoping to standard PATs. This is an architectural security gap that will block enterprise production approvals from security reviewers.

---

### Issue 11: Log retention is 7 days with dashboard-only access — no log streaming API or export

**What the developer hits:** Query logs are auto-deleted after 7 days. Log access is exclusively through the dashboard UI — there is no API endpoint for programmatic retrieval, no webhook, no SIEM integration path. Verbosity is configurable (levels 1–5) per-connection, but log files are only downloadable per-query via a dashboard button.  
**Source:** [docs.cloud.cdata.com/Logs.html](https://docs.cloud.cdata.com/Logs.html) — *"Connect AI saves log files for seven days only. Log files older than seven days are deleted automatically."* Log access is described as dashboard-only (Query Log and Audit Log tabs in the UI). No log streaming API, export endpoint, or webhook appears anywhere in public documentation.  
**Priority:** Medium. Production deployments running CI, automated pipelines, or multi-agent orchestration cannot ingest logs into observability stacks. A production issue that occurred 8 days ago has no data. No alerting on failed queries is documented.

**Remediation:**
- *Content (PMM/DevRel):* Document the 7-day retention policy and dashboard-only access clearly in the observability docs. Publish a "building observability for CData agents" guide showing client-side logging patterns as a workaround — log tool call inputs/outputs on the agent side before they reach CData.
- *Engineering:* Add a log export API endpoint and webhook support for failed queries. Extend log retention to 30 days minimum for paid tiers.

---

### Issue 12: "Build your own MCP tools" is gated to Business tier (custom pricing)

**What the developer hits:** The pricing page lists "Build your own MCP tools" as a Business-tier-only feature. Standard ($99/mo) and Growth ($199/mo) tiers cannot extend the MCP tool schema with custom tools. This restriction is not mentioned anywhere in the MCP documentation, the quickstart, or any developer tutorial. Source: [cdata.com/ai/pricing/](https://cdata.com/ai/pricing/).  
**Priority:** Medium. Any developer who builds a working prototype and attempts to extend the tool schema for domain-specific use hits a sales call gate. The gap between Developer Edition "get started free" messaging and the production extensibility wall is undisclosed.

**Remediation:**
- *Content (PMM/DevRel):* Add a tier callout in the MCP documentation and quickstart: "Custom MCP tool creation requires Business tier." Create a tier feature comparison guide so developers know the extensibility ceiling before they build a prototype that hits a sales gate.
- *Product:* Consider moving basic custom tool creation to the Growth tier or offering a time-limited trial. The gap between "free developer prototype" and "custom tool in production" currently requires a sales conversation with no self-serve path.

---

### Issue 13: SSO and RBAC are Business-tier-only — no permission controls below enterprise pricing

**What the developer hits:** Standard and Growth tiers have no SSO integration and no role-based access controls. Additional users on these tiers share the same permission level — it is not possible to grant a read-only role to one user and write access to another without enterprise pricing. The pricing page lists "SSO and permission controls," "Single Sign-On (SSO)," "Source-Level Permissions," and "Per-User Authentication" exclusively under the Business tier. Source: [cdata.com/ai/pricing/](https://cdata.com/ai/pricing/).  
**Priority:** Medium. Enterprise teams doing a team proof-of-concept on Growth tier will discover this gap late, when attempting to onboard their security or compliance team.

**Remediation:**
- *Content (PMM/DevRel):* Add a clear callout in the team setup and auth docs showing which access controls are available at each tier. Create a "team setup guide" that surfaces Growth tier limitations upfront so teams do not discover them during security review.
- *Product:* Consider adding basic role separation (admin/read-only) to the Growth tier. Teams doing proof-of-concepts at $199/mo will hit this limitation when onboarding security reviewers.

---

### Issue 14: Local MCP server (open-source) is stdio-only — cannot be used in remote or cloud deployments

**What the developer hits:** The `cdata-jdbc-mcp-server` GitHub repo states explicitly: *"The server uses stdio so can only be used with clients that run on the same machine as the server."* Cloud-hosted agents (AWS Lambda, Cloud Run, any remote infrastructure) cannot use this server. The `connectcloud-mcp-server` repo acknowledges this and points to the paid hosted product as the solution. Sources: [github.com/CDataSoftware/cdata-jdbc-mcp-server](https://github.com/CDataSoftware/cdata-jdbc-mcp-server), [github.com/CDataSoftware/connectcloud-mcp-server](https://github.com/CDataSoftware/connectcloud-mcp-server).  
**Priority:** Medium. Developers evaluating via the free open-source server hit a hard architectural wall when moving to cloud deployment. The marketing page at cdata.com/solutions/mcp/ shows a simple download-and-configure path with no cloud deployment caveats.

**Remediation:**
- *Content (PMM/DevRel):* Update the cdata.com/solutions/mcp/ marketing page to state the stdio constraint for the open-source server explicitly. Publish a "local vs. cloud MCP deployment" comparison guide so developers understand the architectural choice before committing to either path.
- *Engineering:* The `connectcloud-mcp-server` already supports `TRANSPORT_TYPE=http` — document this as the recommended cloud deployment path and add a Docker Compose example. Consider making HTTP mode the README default.

---

### Issue 15: Error response schema uses numeric codes 0–79 with no published reference table

**What the developer hits:** The REST API documentation confirms errors return an `ErrorCode` integer enum with values 0 through 79 alongside a `message` string. No table mapping those values to error names, categories, or retry guidance is published anywhere in the doc set. An agent receiving `code: 42` cannot determine whether to retry, re-authenticate, or rewrite the query without pattern-matching against the message string — a brittle approach that breaks when CData changes message wording. Source: [docs.cloud.cdata.com/en/API/REST-API](https://docs.cloud.cdata.com/en/API/REST-API) (defines the enum range; provides no legend).  
**Priority:** Medium. Structured, documented error codes are required for robust agent error handling. Without them, agents cannot distinguish upstream API rate-limit errors from CData rate-limit errors from query syntax errors.

**Remediation:**
- *Content (PMM/DevRel):* Publish an error code reference page mapping all codes 0–79 to: name, category, description, and retry guidance (retry / re-authenticate / rewrite query / contact support). Link from the Query Operation docs and any error-handling tutorial.
- *Engineering:* Add a `codeName` string field alongside the numeric `code` in error responses (e.g., `"codeName": "RATE_LIMIT_EXCEEDED"`) so agents can branch on error type without a lookup table.

---

### Issue 16: No sandbox environment — every query hits production credentials

**What the developer hits:** No staging environment, mock MCP endpoint, or sandbox data set is documented anywhere. The only hint is an undocumented `CDATA_URL` environment variable in the `connectcloud-mcp-server` README (`CDATA_URL=https://your-test-environment-url`) — no test URL is provided by CData and no documentation points to it. Source: [github.com/CDataSoftware/connectcloud-mcp-server](https://github.com/CDataSoftware/connectcloud-mcp-server) README (the only place `CDATA_URL` appears in any public CData resource).  
**Priority:** Medium. Enterprise developers cannot build or test agent behavior without real production credentials. Every development query counts against the 100M-record monthly fair-use limit. Sales engineers running demos must use live production systems.

**Remediation:**
- *Content (PMM/DevRel):* Publish a "safe testing guide" positioning the pre-connected PostgreSQL and MySQL demo sources (SampleConnection1, SampleConnection2) as the recommended development environment. Document their full schemas so developers can build and test agent queries without touching production data or consuming their record cap.
- *Engineering/Product:* Create an official sandbox MCP endpoint with curated demo data and no record cap. Add a usage counter to the dashboard showing current month consumption vs. the 100M limit.

---

### Issue 17: 100M record/month "fair use" limit is undefined — metadata calls may count toward the cap

**What the developer hits:** The pricing page states "100M records outlined in our fair use policy" as the monthly limit. The fair-use page ([cdata.com/ai/fair-use/](https://cdata.com/ai/fair-use/)) uses "rows" and "records" interchangeably, mentions additional metrics (rows processed before aggregation, total data transferred), and does not define any of these terms precisely. It is unclear whether metadata calls (`getCatalogs`, `getTables`, `getColumns`) count toward the cap. The MCP server makes multiple metadata round-trips before every query session. No dashboard counter shows current month usage versus the 100M cap. Source: [cdata.com/ai/pricing/](https://cdata.com/ai/pricing/), [cdata.com/ai/fair-use/](https://cdata.com/ai/fair-use/).  
**Priority:** Medium. An agent doing source discovery on a large enterprise deployment (50+ tables, multiple schemas) may consume metadata records at a rate the developer cannot estimate or monitor.

**Remediation:**
- *Content (PMM/DevRel):* Add a definition of "record" to the pricing page and FAQ. Clarify explicitly whether metadata calls (`getCatalogs`, `getTables`, `getColumns`) count toward the cap. Publish guidance on estimating usage per query type.
- *Engineering:* Add a usage counter to the dashboard showing current month record consumption vs. the 100M cap, with an alert at 80% consumed.

---

### Issue 18: Per-framework docs exist but are siloed — no unified compatibility matrix or discovery path

**What the developer hits:** CData has standalone documentation pages for [LangChain](https://docs.cloud.cdata.com/LangChain-Client.html), [LlamaIndex](https://docs.cloud.cdata.com/LlamaIndex-Client.html), and [CrewAI](https://docs.cloud.cdata.com/CrewAI-Client.html) — but no AutoGen, no OpenAI Assistants coverage, and no unified compatibility matrix. No single page shows all supported frameworks with version requirements, known limitations, or recommended patterns. Each guide is a standalone page with only a "Python ≥3.10" prerequisite and no version pinning for the framework itself. A developer evaluating Connect AI from LangChain or CrewAI would need to find the right page by navigation — none of these are surfaced in the MCP quickstart or the main developer landing page.  
**Priority:** Low. The framework docs exist — this is a discoverability and completeness gap, not a coverage gap from scratch.

**Remediation:**
- *Content (PMM/DevRel):* Create a single "Framework Compatibility" index page listing all supported frameworks with version requirements, links to guides, and a clear note on which are MCP-based vs. SDK-based. Add AutoGen and OpenAI Assistants coverage — these represent a significant portion of production deployments and are high-traffic search queries.
- *Engineering:* Formally test and version-pin framework compatibility. Publish the matrix as a maintained reference page (not a blog post) so it stays current as frameworks evolve.

---

## Agent Runtime Findings

The following issues are experienced at runtime by the AI agent itself — not during developer setup. They affect query reliability, token cost, and error recovery in production agentic workflows.

---

### Issue 19: `getInstructions` tool routes agents into an expensive metadata discovery loop

**What the agent hits:** `getInstructions` is positioned as the entry point for agent sessions. Following its output sends the agent through a sequential discovery chain: `getCatalogs` → `getSchemas` → `getTables` → `getColumns` — 4–8 tool calls per connected source before a single query runs. With 4 sources, this can consume 10+ tool rounds. The efficient pattern — hardcode the schema in the system prompt and skip `getInstructions` — is not documented. Developers discover it by profiling tool call counts.  
**Source:** Observed in live agentic sessions; workaround implemented in `agent.py:15-41`.  
**Priority:** Medium. Every production agent session that follows the documented path pays this cost on every call. Schema prefetching is a standard optimization for agentic SQL tools and should be the documented default.

**Remediation:**
- *Content (PMM/DevRel):* Publish a "production agent optimization guide" showing the system prompt schema prefetch pattern — provide table names and columns upfront, skip `getInstructions`. Include a benchmark: prefetch path ≈ 3 tool calls vs. discovery path ≈ 10+. Link from the MCP docs page and from the `getInstructions` tool description.
- *Engineering:* Update the `getInstructions` response to offer schema prefetch as the recommended fast path. Consider adding a `tools/schema` endpoint that returns all connected source schemas in a single call, eliminating the discovery loop entirely.

---

### Issue 20: Fully-qualified three-part table names required but not surfaced until query failure

**What the agent hits:** All SQL queries must use `[Catalog].[Schema].[Table]` syntax (e.g., `[GoogleSheets1].[GoogleSheets].[Connect AI Demo — Sales Pipeline_pipeline]`). Queries written without the fully-qualified form fail with an error that does not explain the required format. The `queryData` tool description does not mention the requirement. Agents learn the format by failure, costing at least one additional tool round per session. The SQL Reference ([docs.cloud.cdata.com/SQL-Reference.html](https://docs.cloud.cdata.com/SQL-Reference.html)) documents the three-part naming requirement and bracket quoting for non-standard characters — but this is not surfaced in the MCP tool description where an agent would encounter it. System prompt workaround implemented in `agent.py:38`.  
**Priority:** Medium. Adding a one-line note on the required name format to the `queryData` tool description is a zero-cost doc fix that eliminates a common failure mode for new agents and developers.

**Remediation:**
- *Content (PMM/DevRel):* Add the `[Catalog].[Schema].[Table]` format requirement to the MCP docs quickstart with a live example from a connected source (e.g., `[GoogleSheets1].[GoogleSheets].[My Sheet Name]`).
- *Engineering:* Update the `queryData` tool description to include the naming format. Update the query failure error message to show the correct format with a concrete example rather than a generic "table not found."

---

### Issue 21: Tool naming convention breaks for multi-word or underscore-containing source names

**What the developer hits:** CData tool names follow an inferred pattern such as `query_salesforce_contacts`, where the source name is `parts[1]` when split on `_`. This fails silently for any source name that contains an underscore (e.g., a source named `my_salesforce_prod` yields `my` as the parsed source). No formal tool naming spec is published — the convention must be inferred from observed examples. Client code that groups or displays tools by source will silently misclassify them for non-trivially-named sources.  
**Source:** Observed in `mcp_client.py:80-88`; tool naming convention confirmed absent from MCP documentation.  
**Priority:** Low. A published tool naming schema — or a dedicated `source` field in the tool definition — would eliminate fragile string parsing.

**Remediation:**
- *Content (PMM/DevRel):* Document the tool naming convention in the MCP reference so developers know the pattern and its edge cases before writing parsing code.
- *Engineering:* Add a `source` metadata field to each tool definition in the `tools/list` response. This eliminates string parsing entirely and is a non-breaking addition to the existing schema.

---

### Issue 22: No result streaming or pagination through the MCP tool interface

**What the agent hits:** The `queryData` MCP tool returns the full result set as a single payload. There is no cursor, page token, or `LIMIT`/`OFFSET` guidance in the tool description. A query returning a large table either succeeds (returning the full set at once, bloating context) or times out at 30 seconds (Issue 9). The agent has no proactive signal to add `LIMIT` unless the system prompt instructs it. The REST Query API (`docs.cloud.cdata.com/Query-Operation.html`) has no `limit`, `offset`, `maxRows`, or cursor fields in its `QueryRequest` schema either — all rows return in a single `rows` array. Streaming and pagination are absent from both the MCP and REST layers.  
**Priority:** Medium. The `queryData` tool description should recommend `LIMIT` for large tables and note the 30-second timeout. An optional `maxRows` parameter in the tool itself would be a stronger fix.

**Remediation:**
- *Content (PMM/DevRel):* Add a "working with large datasets" section to the MCP docs recommending `LIMIT` clauses and noting the 30-second query ceiling. Include an example: `SELECT * FROM [Catalog].[Schema].[Table] LIMIT 1000`.
- *Engineering:* Add a `maxRows` parameter to the `queryData` MCP tool. Implement cursor-based pagination for result sets exceeding a configurable threshold. Both bring the MCP tool interface to parity with what the REST Query API already supports.

---

### Issue 23: DataType enum mapping table exists in REST API docs but is not linked from MCP or Query Operation pages

**What the developer hits:** Every tool response that includes schema metadata uses an integer `dataType` field (values 1–18) to represent column SQL types. The mapping table *does* exist at `docs.cloud.cdata.com/en/API/REST-API#data-types` — but it is buried in the REST API reference and is not linked from the MCP documentation, the Query Operation page, or any quickstart. Developers parsing schema responses from the MCP tool will find the integer field and have no indication that a legend exists elsewhere in the docs.  
**Source:** `docs.cloud.cdata.com/en/API/REST-API#data-types` (full 18-row table: 1=BINARY, 2=VARBINARY … 17=TIMESTAMP, 18=UUID). The table is correct and complete; it is simply not discoverable from the MCP toolchain docs.  
**Priority:** Low. The fix is a link addition, not new documentation. Add a cross-reference from the MCP docs and the Query Operation page to the REST API data-types anchor.

**Remediation:**
- *Content (PMM/DevRel):* Add a "Data Types" note to the MCP tool response documentation linking to `docs.cloud.cdata.com/en/API/REST-API#data-types`. One sentence and a link — the table already exists.
- *Engineering:* Return `dataTypeName` as a string alongside `dataType` as an integer in all schema responses so developers do not need to look up the table at all. The field appears in some responses already — make it consistent.

---

### Issue 24: MCP server config examples store credentials without secrets management guidance

**What the developer hits:** The `connectcloud-mcp-server` README shows credentials stored as plaintext in `claude_desktop_config.json`: `"CDATA_USERNAME": "<your-cdata-username>", "CDATA_PAT": "<your-cdata-personal-access-token>"`. No `.gitignore` guidance, no reference to secrets managers (1Password, Vault, AWS Secrets Manager), and no warning that a leaked PAT grants full read/write access to all connected enterprise sources (Issue 10). The JDBC server README shows the same pattern with JDBC connection strings in `.prp` config files. Sources: [github.com/CDataSoftware/connectcloud-mcp-server](https://github.com/CDataSoftware/connectcloud-mcp-server), [github.com/CDataSoftware/cdata-jdbc-mcp-server](https://github.com/CDataSoftware/cdata-jdbc-mcp-server).  
**Priority:** Medium. Given that PATs carry full account access with no scoping (Issue 10), the setup guides need at minimum a `.gitignore` callout and a note on environment variable injection rather than hardcoded config files.

**Remediation:**
- *Content (PMM/DevRel):* Update both MCP server READMEs with a "Secrets Management" section: add a `.gitignore` callout for `.env` files, recommend environment variable injection over hardcoded config values, and reference common secrets managers (1Password CLI, AWS Secrets Manager, HashiCorp Vault) for production deployments.
- *Engineering:* Make `.env` file support the primary credential method in all config examples. Replace the `claude_desktop_config.json` snippet that shows plaintext credential values with a template that reads from environment variables.

---

### Issue 26: Documentation fragmented across subdomains — domain authority split hurts search and brand

**What the developer hits:** CData's documentation lives across at least four different hostnames:
- `docs.cloud.cdata.com` — Connect AI documentation
- `docs.cdata.com` — driver and ODBC/JDBC documentation
- `cdn.cdata.com/help/ASN/sync/` — CData Sync help (the page that Connect AI "Help" links resolve to — see Issue 25)
- `www.cdata.com` — marketing, pricing, and blog

Every subdomain is treated by search engines as a separate site for domain authority purposes. Inbound links to `docs.cloud.cdata.com` do not strengthen the ranking of `www.cdata.com`, and vice versa. The marketing site gets the backlinks; the docs site doesn't benefit. The docs site gets the developer traffic; the marketing site doesn't benefit. Neither builds a coherent authority signal.

**The discoverability consequence:** A developer searching "CData Connect AI MCP server documentation" on Google is not guaranteed to find `docs.cloud.cdata.com` on the first page — they may find a blog post on `www.cdata.com` that links there, or they may find nothing useful at all. During this audit, locating the correct documentation required hours of navigation and lateral searching. No single Google query returned `docs.cloud.cdata.com` directly. The Connect AI documentation is effectively invisible to organic search traffic.

**The agent-readiness consequence:** When a developer asks Claude Code, Cursor, or Perplexity "how do I set up CData Connect AI," the AI retrieves from indexed, structured content. A fragmented subdomain structure produces fragmented training signal — each subdomain tells a partial story. A developer asking their AI assistant for help gets either the marketing pitch (from `www.cdata.com`) or the driver docs (from `docs.cdata.com`) but not the Connect AI MCP reference, because the subdomain that hosts it has insufficient authority to surface in retrieval.

**The brand consequence:** Every subdomain is a separate namespace that developers encounter without context. A developer who bookmarks `docs.cloud.cdata.com` and tells a colleague "the CData docs are at..." has to give a URL that does not obviously belong to `cdata.com`. Sub-brand trust is harder to build than domain-level trust.

**What other developer tools do:** Vercel docs live at `vercel.com/docs`. Stripe docs live at `docs.stripe.com` — a subdomain, but one that is the canonical documentation home, consistently branded, with all products under one roof. CData has the opposite: multiple sub-homes, none of which a new developer can confidently say is the right place to look.

**Priority:** High. This is a structural issue that compounds every other documentation gap. Fixing individual pages matters less if developers cannot find them in the first place.

**Remediation:**
- *Content/Engineering:* Evaluate consolidating all documentation under `cdata.com/docs/` (preferred for domain authority) or under a single dedicated subdomain (`docs.cdata.com`) with Connect AI as a product section. At minimum, ensure that `docs.cloud.cdata.com` is canonical, indexed, and cross-linked from the marketing site's header and footer so search engines can establish the authority relationship.
- *Content (PMM/DevRel):* Add canonical `<link rel="canonical">` tags and proper cross-domain sitemaps so search engines understand the relationship between the documentation domain and the marketing domain.

---

### Issue 27: Documentation absent from primary navigation — developer section has no docs link

**What the developer hits:** The primary navigation on `cdata.com/ai/` and `www.cdata.com` has a "Developers" section in the header. That section contains no link to documentation. The only documentation link on the marketing site is buried in the footer under "Support & Services → Product Documentation" — a section a developer will never look at before scrolling to the bottom of the page after already being lost.

For a developer arriving at `cdata.com/ai/` to evaluate Connect AI:
1. They look in the header under "Developers" — no docs link
2. They scan the hero section — no docs link
3. They click "Get Started" — goes to sign-up, not docs
4. They eventually scroll to the footer — find "Product Documentation," click it, land on a page that does not distinguish Connect AI from CData Sync

This is not a hypothetical flow. This is the exact flow this audit reproduced. Locating the correct documentation for Connect AI required hours, not minutes.

**The developer expectation:** Every developer tool — Stripe, Vercel, Twilio, GitHub, Anthropic — puts documentation in the header navigation, either in a "Docs" tab or within the "Developers" dropdown. Documentation is the first thing a developer looks for after deciding a tool might be worth evaluating. It is not a footer item. It is not a support item. It is the primary developer-facing content.

**The specific gaps:**
- The "Developers" header item does not link to `docs.cloud.cdata.com`
- The "Developers" header item does not link to the quickstart
- The "Developers" header item does not link to the MCP reference
- The `cdata.com/ai/` product page has no documentation link above the fold or in the header
- The `cdata.com/ai/` product page has no documentation link in the body content

**Priority:** High. A developer who cannot find the docs in the first two minutes of evaluation leaves. The developer header section is the canonical location where developers expect documentation. Its absence there signals that the product is not developer-first.

**Remediation:**
- *Content/Engineering:* Add a "Docs" link to the primary header navigation that routes to `docs.cloud.cdata.com`. At minimum, add documentation to the "Developers" dropdown. Add a "View the docs →" CTA above the fold on `cdata.com/ai/` alongside "Get Started" — both are the first actions a developer takes. Add documentation to the footer of `cdata.com/ai/` explicitly for Connect AI (not the generic "Product Documentation" link that goes to a product-selector page).
- *Content (PMM/DevRel):* Make "documentation first" the rule for all future Connect AI landing pages. If the page is developer-facing, documentation is in the header. No exceptions.

---

### Issue 28: No model or version disclosure — developers cannot calibrate expectations

**What the developer hits:** Nowhere in the Connect AI documentation, marketing pages, MCP reference, or API docs is there any disclosure of which AI model powers the platform's intelligent features. Developers ask Claude Code, Cursor, or Perplexity to recommend tools for enterprise data access — but they also have opinions about the underlying models those tools use. GPT-4o, Claude Sonnet, Gemini Flash, and a fine-tuned distilled model have meaningfully different accuracy profiles, latency characteristics, context window sizes, and known failure modes. Telling developers which model you use is not giving away trade secrets. It is giving them the information they need to calibrate their expectations before they invest time in an integration.

**What is missing:**
- Which foundation model (or models) powers Connect AI's AI-assisted features?
- What version of that model? (GPT-4o-mini vs. GPT-4o vs. GPT-4o-2024-11-20 are meaningfully different)
- Does the model change? Under what circumstances?
- Will developers be notified when the underlying model changes?
- Is there a model changelog or version history?

**Why this matters for trust:** A developer who builds a workflow on top of an AI feature assumes some stability in the underlying model's behavior. If CData silently upgrades from one model to another — even to a better model — and the developer's prompts, output parsing, or behavior tests break, that developer loses trust immediately. The solution is not to freeze the model forever; it is to disclose what the model is, commit to a deprecation notice window, and publish a changelog when it changes. This is table stakes for any production AI feature.

**Examples of how other products handle this:** OpenAI publishes every model version with a dated slug (`gpt-4o-2024-11-20`), a deprecation timeline, and a migration guide. Anthropic publishes model IDs with dated slugs and a deprecation policy. Even smaller AI API providers disclose the underlying model. CData discloses nothing.

**Priority:** High. Model transparency is a baseline developer expectation for any AI-powered API. Absence of this disclosure signals immaturity in the product's AI governance.

**Remediation:**
- *Content (PMM/DevRel):* Add a "Model" section to the MCP documentation and the AI features overview page disclosing the current model, version, and update policy. Publish a model changelog. Commit to a minimum 30-day advance notice before any model change that affects behavior.
- *Product/Engineering:* Return a `model` field in MCP tool responses or session metadata so developers can log and monitor what model processed each request. Add a `X-CData-Model-Version` response header to all AI-assisted API endpoints.

---

### Issue 29: No latency specifications — developers cannot evaluate fitness for their use case

**What the developer hits:** An AI feature that returns results in 200 milliseconds is a code-completion candidate. An AI feature that returns results in 8 seconds is a batch analytics tool. These are not the same product, and developers need to know which one they are evaluating before they integrate it into their workflow. CData's documentation, marketing pages, and MCP reference contain no latency information of any kind: no P50, no P95, no SLA, no "typical query time," no comparison between connection types.

**What happens without this:** Developers discover latency on their first real query. If it is worse than they expected for their use case, they turn the feature off and never come back. If it is better than expected, they are pleasantly surprised but had no basis for making the integration decision. Either way, the absence of latency documentation means developers are making integration decisions without a key input.

**What is missing:**
- Typical end-to-end query latency for a simple SELECT against a SaaS source (Salesforce, Google Sheets)
- How latency scales with result set size
- How latency differs between the hosted MCP endpoint and the local stdio server
- Whether latency varies by source type (database vs. SaaS API vs. cloud warehouse)
- Any SLA or uptime commitment for the hosted MCP endpoint

**During this audit:** A simple query against Google Sheets via the MCP server returned results in approximately 3 seconds after schema stripping was implemented (Issue 5). Without schema stripping, the same query appeared to hang indefinitely with the largest model. These are meaningful data points that developers need before integrating. They are not in the docs.

**Priority:** High. Latency is as important as any functional specification for developers evaluating an AI API. Omitting it means developers can't evaluate the tool for their use case without investing in a prototype first.

**Remediation:**
- *Content (PMM/DevRel):* Publish a "Performance" section in the MCP and API docs with representative latency numbers for common query patterns (simple SELECT, JOIN across two sources, large result set). Be honest — if 8 seconds is typical for cross-source JOINs, say so, and explain why (client-side federation, Issue 8). Honest latency data with explanation builds more trust than no data.
- *Engineering:* Return `X-CData-Query-Duration-Ms` response headers on all query endpoints so developers can measure and log actual latency in their own applications.

---

### Issue 30: No accuracy or limitation disclosures — "AI is highly accurate" means nothing

**What the developer hits:** The Connect AI documentation and marketing pages make no accuracy claims of any kind — which is actually the problem. The MCP tool descriptions do not note where the AI-assisted features perform well or poorly. There is no published benchmark, no error rate, no known failure mode documentation, and no statement of what input types produce worse results. Developers will test CData against edge cases within the first ten minutes of using it. They want to know ahead of time where the boundaries are.

**Specific gaps:**
- No documentation on what SQL patterns the AI struggles to generate correctly (complex subqueries, window functions, non-standard syntax for specific sources)
- No documentation on which sources have better or worse schema understanding (does the AI know Salesforce's object model? NetSuite's custom fields?)
- No known limitations section in the MCP reference
- No confidence signal in query results — the developer cannot tell whether the AI-generated SQL was a high-confidence translation or a best guess
- No documentation on how the AI behaves with ambiguous natural language queries (does it ask for clarification? does it guess? does it return an error?)

**What this looks like in practice:** During this audit, the agent correctly handled multi-step analytical queries against structured data (pipeline totals, rep breakdowns). It was not tested against highly ambiguous queries, custom-field-heavy sources, or deeply nested schema structures. That test was not run because the docs gave no guidance on where to push the boundaries.

**Priority:** Medium. Accuracy disclosure is standard practice for any production AI feature. The absence of it is not a safety issue — it is a trust and expectation management issue that surfaces as developer churn when reality differs from assumption.

**Remediation:**
- *Content (PMM/DevRel):* Add a "Known Limitations" section to the MCP documentation. Be specific: "Natural language queries that reference custom fields by user-defined name may not resolve correctly without schema context." Specific limitations build more trust than vague disclaimers. Publish a prompt library (the CData Prompt Library already exists — link to it from this section) as a curated set of queries known to work well.
- *Product:* Consider surfacing a confidence signal in `queryData` responses — even a simple `"queryConfidence": "high" | "low"` field lets developers branch on uncertainty rather than blindly consuming results.

---

### Issue 31: No developer override or control mechanism documented — black-box AI is a dealbreaker

**What the developer hits:** The MCP documentation's only guidance for influencing AI behavior is: "use specific, detailed prompts" and a reference to the CData Prompt Library. There is no documented way to:
- See the SQL the AI generated before it executes
- Edit the AI-generated SQL before execution
- Reject an AI result and fall back to a manual SQL query
- Inspect why the AI interpreted the query a particular way
- Set guardrails on what tables or schemas the AI can access in a query

This is the question that separates developer-friendly AI from consumer AI. Consumers want a black box that just works. Developers need to be able to see what was produced, understand why, edit it, and reject it. The moment developer control is removed from an AI feature, the developer cannot ship it to production — because they cannot reason about its failure modes or audit its outputs.

**Specific missing mechanisms:**
- No `dryRun` or `explainQuery` mode that returns the generated SQL without executing it
- No way to pass a pre-written SQL query directly to `queryData` and bypass the NL→SQL translation
- No documented fallback pattern for when the agent gets the query wrong
- No documented undo mechanism for write operations (INSERT, UPDATE, DELETE)
- No query preview before execution in any documented workflow

**Note on write access:** The SQL Reference documents that `queryData` supports SELECT, INSERT, UPDATE, DELETE, and EXEC. A developer who issues a natural language query like "update the pipeline status for all Q2 deals" has no preview step before data is modified. This is not a hypothetical concern — it is a production risk for any AI agent with write access.

**Priority:** High. Developer control is not a nice-to-have for enterprise tooling — it is a prerequisite for production approval. An AI agent that can modify data without a confirmation step will not pass security review at any enterprise customer.

**Remediation:**
- *Content (PMM/DevRel):* Document the recommended pattern for developers who want to review AI-generated SQL before execution: extract the `queryData` tool, call `getColumns` first to get schema context, have the agent generate SQL as text, display it to the developer, then execute via `queryData` with the explicit SQL. This pattern exists — it is just not documented.
- *Engineering:* Add a `dryRun: true` parameter to `queryData` that returns the generated SQL without executing it. This is the single most important developer control mechanism for production deployments. Also add a `rawSql` parameter that bypasses NL→SQL translation entirely, for developers who want to write SQL directly through the MCP interface.

---

### Issue 32: No cost or token implications disclosed for AI features — surprise bills block production adoption

**What the developer hits:** AI inference is not free. If CData is passing prompts to a foundation model, there is a per-token cost somewhere. The pricing page lists flat monthly tiers ($99/mo Standard, $199/mo Growth) and a 100M record/month fair-use limit. It does not disclose:
- Whether AI inference costs are included in the flat tier pricing
- Whether there is a per-token metering layer below the record cap
- What happens when the 100M record fair-use limit is hit — hard stop or overage billing?
- Whether CI/CD pipelines, automated agents, or batch jobs that trigger thousands of AI-assisted queries incur additional charges
- Whether metadata calls (schema discovery, `getCatalogs`, `getTables`) count toward the record cap or toward a separate AI inference budget

**Why this blocks production adoption:** A developer whose CI pipeline triggers an automated agent that runs nightly against 5 connected sources has no way to estimate their monthly bill. A company that discovers mid-month that an automated workflow consumed their entire 100M record budget has no advance warning and no documented recourse. Enterprise buyers require a cost model they can reason about before signing a purchase order. "Flat monthly fee" is not a cost model for AI-assisted tools with per-query compute costs.

**Priority:** High. Cost opacity is a production adoption blocker, not a documentation preference. Enterprise procurement requires a cost formula. Individual developers require confidence that their CI pipeline won't generate a surprise bill.

**Remediation:**
- *Content (PMM/DevRel):* Add a "Cost Model" section to the pricing page and the MCP documentation explicitly answering: (1) Is AI inference included in the flat tier price? (2) Are metadata calls counted against the record cap? (3) What happens at 100M records — hard cap or overage? (4) Is there a usage calculator or cost estimator?
- *Engineering:* Add real-time usage counters to the dashboard showing current-month record consumption vs. cap, broken down by source and query type. Add a configurable spending alert at a developer-defined threshold. These are standard features in any metered API product (AWS, Twilio, Stripe) and their absence is conspicuous at the pricing tier CData operates at.

---

### Issue 33: docs.cloud.cdata.com fails agent-readiness checks independently of www.cdata.com

**What the developer hits:** The existing audit (Agentic Documentation Gap section, Issues 1–9) covers agent-readiness gaps for `www.cdata.com`. The documentation subdomain at `docs.cloud.cdata.com` has its own set of agent-readiness gaps that compound the problem. Because the documentation is where agents go to learn how to use a product, agent-readiness failures on the docs domain are higher-impact than failures on the marketing domain.

Fetching `docs.cloud.cdata.com` as an AI agent reveals:
- No `Link` response headers with agent-useful relation types (`api-catalog`, `service-doc`)
- No `/.well-known/api-catalog` on the docs subdomain — agents cannot discover the Connect AI REST API or MCP endpoint programmatically from the docs domain
- No `/.well-known/mcp/server-card.json` on the docs subdomain
- The `llms.txt` file at `docs.cloud.cdata.com/llms.txt` exists and is comprehensive (100+ pages indexed across API, auth, integrations, MCP, SQL reference, and data sources) — this is genuine progress. But it is a documentation index, not a curated product brief. A developer asking an AI assistant what CData Connect AI does and how it differs from Composio will not get a useful answer from a 300-page sitemap. The file needs a short product description at the top, the SQL-vs-action-based differentiation, the quickstart URL, the MCP endpoint, and the enterprise source list — all before the page index begins.
- The `Accept: text/markdown` response for the docs domain was not tested in this audit, but given that the marketing domain returns 403 for markdown negotiation (Issue 2 in the Agentic Documentation Gap section), it is likely the same.

**The core gap:** `docs.cloud.cdata.com/llms.txt` is a good start but solves the wrong problem. It tells an agent "here is a list of our documentation pages." What agents need is "here is what CData Connect AI does, why it is different, and where to start." Composio's `llms.txt` answers all three in the first paragraph. CData's answers none of them before the page index.

**Priority:** High. The docs subdomain is the highest-value surface for agent discovery — it is where an AI assistant retrieves when a developer asks "how do I use CData." Fixing the `llms.txt` on the docs domain is the same one-week content investment as fixing the marketing `llms.txt`, and it has higher retrieval impact.

**Remediation:**
- *Content (PMM/DevRel):* Rewrite the preamble of `docs.cloud.cdata.com/llms.txt` to lead with: (1) a one-paragraph product description of Connect AI and how it differs from Composio/Zapier, (2) the quickstart URL, (3) the MCP endpoint URL and auth pattern, (4) the list of top 10 supported enterprise sources, (5) then the full page index. Publish a companion `llms-full.txt` that serializes the complete Connect AI doc set in a single token-efficient file.
- *Engineering:* Add `Link` headers to the docs subdomain pointing to the api-catalog and MCP server card. Run `isitagentready.com/docs.cloud.cdata.com` as a recurring audit check and track it alongside the `www.cdata.com` results.

---

### Issue 25: In-product "Help" links resolve to CData Sync docs — not Connect AI

**What the developer hits:** Following "Help" or documentation links from the Connect AI product surface returns CData Sync documentation — a separate product with a different architecture, different configuration model, and different use cases. Fetching [cdn.cdata.com/help/ASN/sync/](https://cdn.cdata.com/help/ASN/sync/) returns a page titled *"CData Sync - Getting Started | 26.2.9629"* describing CData Sync as *"a robust, easy-to-use data integration platform."* There is no equivalent hosted help URL for Connect AI. Developers who click through for help land on docs for a product they are not using and have to navigate back to find anything relevant.

**Why this matters:** Documentation is the foundation on which every other content investment rests. A developer who cannot find accurate docs for the product they just signed up for has no baseline for trust — and no path forward except trial and error. This is not a documentation gap in the sense of missing a page or a section; it is the absence of a documentation home for the product. The quickstart, the MCP reference, the auth docs, and the error code reference all exist as scattered pages — but there is no unified, product-specific help URL developers can bookmark or share.

**Priority:** High. This is distinct from all other documentation issues above because it is foundational — it makes every other doc gap harder to find and harder to fix. A developer who lands on CData Sync docs once will distrust every "Help" link going forward.

**Remediation:**
- *Content (PMM/DevRel):* Establish `docs.cloud.cdata.com/connect-ai/` (or equivalent) as the canonical documentation root for Connect AI. All dashboard "Help" links, quickstart "Learn more" links, and in-product tooltips must resolve there — not to the Sync help URL. This is a redirect and navigation audit, not a content creation task.
- *Engineering:* Update all in-product help links to route to the correct Connect AI documentation. Ensure `cdn.cdata.com/help/` has either a product selector or product-aware routing so developers cannot land on CData Sync docs from a Connect AI context.

---

---

## Documentation Usability Audit

The following issues were identified by auditing five key pages a new developer encounters in sequence: the docs home (`/en/docs`), the Quick Start Guide, the Authentication docs, the Python Client docs, and the FAQ. These are not missing features — they are failures in the learning path itself. A working product with a broken learning path loses developers before they reach the first successful query.

---

### Issue 34: Quick Start Guide has no prerequisites section — developers arrive unprepared

**What the developer hits:** The Quick Start Guide begins with "Step 1: Sign in" but never lists what the developer needs to have ready before starting. By Step 2, they are asked to connect Salesforce and "Provide Client ID and Client Secret" with a one-line parenthetical pointing to where those live inside Salesforce. A developer who does not already have a Salesforce Connected App configured has to stop, leave the docs, set one up, and come back. There is no estimate of how long setup takes, no checklist of credentials to gather first, and no guidance on what to do if they don't have access to the required system.

**What a good prerequisites section looks like:**
```
Before you begin, you'll need:
- A CData Connect AI account (free — sign up at cloud.cdata.com)
- Admin access to at least one data source (Salesforce, Google Sheets, PostgreSQL, etc.)
- For OAuth sources: a Connected App or OAuth client already configured in the source system
- Your CData account email address and a Personal Access Token (Settings → Access Tokens)
Estimated time to complete: 15–20 minutes
```
That is four bullet points and one sentence. It would eliminate the most common source of mid-guide abandonment.

**Priority:** High. Missing prerequisites is the most predictable quickstart failure mode. Every developer who stalls at credential setup abandons the guide and forms a negative first impression.

**Remediation:**
- *Content (PMM/DevRel):* Add a "Before you begin" section as the first element of the Quick Start Guide. List required credentials, required system access, and a time estimate. For OAuth sources, link directly to the source-specific OAuth setup guide — not a generic mention that it exists.

---

### Issue 35: Zero screenshots in the Quick Start Guide — developers navigate UI blind

**What the developer hits:** The Quick Start Guide has seven steps covering signup, source connection, data exploration, view creation, tool integration, workspace organization, and permissions management. None of these steps contain a screenshot, annotated UI callout, or screen recording. Developers are told to find "Sources > Add Connection" in a dashboard they have never seen before, with no visual reference for what that looks like or where it lives.

**Why this matters beyond aesthetics:** Screenshots are not decoration — they are orientation cues. A developer who cannot find "Sources" in the sidebar in the first 30 seconds of using a new dashboard loses confidence. When the UI inevitably changes (column moves, label rename, feature flag rollout), text-only docs keep working; screenshot-heavy docs need updating. But zero screenshots is not a maintenance optimization — it is an absence of basic usability support.

**The highest-value screenshots for this guide:**
1. The dashboard with "Sources" highlighted
2. The "Add Connection" modal with OAuth source selected
3. The connection success state with the green indicator
4. The Data Explorer showing a connected table

Four images. They would cut first-session confusion significantly.

**Priority:** Medium. The impact is real but the guide is still followable by an experienced developer. A new developer — someone who has never set up a data connector before — will stall without visual cues.

**Remediation:**
- *Content (PMM/DevRel):* Add annotated screenshots at minimum to Steps 1–3 (sign in, connect source, explore data). Steps 4–7 are less critical. If screenshots are considered too expensive to maintain, use screen-recorded GIFs for the OAuth flow specifically — this is the highest-confusion step and motion removes ambiguity about what to click.

---

### Issue 36: Code samples are missing imports — not copy-pasteable without trial and error

**What the developer hits:** The Python Client documentation includes code examples for queries, batch inserts, stored procedures, and Pandas integration. Most of them do not include `import` statements. A developer who copies the batch operations example gets a `NameError` on the first run because the import is not in the sample. The parameterized query example has the same problem. Across the Python docs, developers must infer which imports are needed from context — a form of undocumented prerequisite that adds friction to every code sample.

This is endemic across the doc set, not isolated to one page. The MCP quickstart examples similarly omit boilerplate that a developer needs to actually run the code.

**The fix is trivial.** Every code sample should be self-contained and runnable as copied. If it requires an import, the import is in the sample. If it requires a connection string, there is a clearly marked placeholder. If it requires a table name, the sample uses the same three-part format documented in the SQL Reference (`[Catalog].[Schema].[Table]`) rather than a hardcoded example that breaks for every reader's actual schema.

**Priority:** Medium. This is low effort to fix and high frustration to encounter — the definition of a quick win.

**Remediation:**
- *Content (PMM/DevRel):* Audit every code sample across the Python Client, Node.js, JDBC, and MCP quickstart docs. Add imports to any sample that omits them. Add a connection setup block to any sample that assumes an active connection without showing how it was created. One review pass; one-time effort.

---

### Issue 37: No error handling in any code sample — production patterns are absent

**What the developer hits:** Every code sample in the Python Client docs assumes success. There is no try/except, no connection error handling, no SQL error handling, no timeout handling, and no example of what to do when `queryData` returns an error. A developer who copies these samples into a production environment gets unhandled exceptions the first time anything goes wrong — and for an enterprise data integration tool, things going wrong (network timeout, expired token, rate limit, malformed query) is routine, not exceptional.

This is not just a documentation aesthetic issue. Code samples teach patterns. A developer who learns to write data integration code from CData's samples learns to write it without error handling. That pattern propagates into production codebases.

**What a minimal error-handling example looks like:**
```python
import cdata_connect_ai as cdata

try:
    conn = cdata.connect(
        user="joekarlsson1@gmail.com",
        password="your_pat_here"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM [GoogleSheets1].[GoogleSheets].[Pipeline] LIMIT 10")
    results = cursor.fetchall()
except cdata.OperationalError as e:
    print(f"Connection failed: {e}")
except cdata.DatabaseError as e:
    print(f"Query failed: {e}")
finally:
    conn.close()
```

That is eight additional lines. They set the expectation that production code handles failures.

**Priority:** Medium. Not a blocker, but a signal of maturity. Enterprise developers evaluating a data integration tool will notice that the samples don't model real usage.

**Remediation:**
- *Content (PMM/DevRel):* Add a "production-ready" version of the basic query example to the Python Client docs that includes connection error handling, query error handling, and explicit connection cleanup. This becomes the canonical sample; the "minimal" example can remain for brevity but should link to the production version.

---

### Issue 38: FAQ has 6 questions and almost no cross-links — nearly useless as a recovery resource

**What the developer hits:** The FAQ page contains exactly six questions. They cover rate limits, static IP whitelisting, email address changes, missing data in integration tools, service outages, and technical support contact. There are no questions about authentication, error codes, pricing, SDK availability, framework compatibility, or any of the common first-session stumbles documented in this audit. Most answers contain no links to deeper documentation — they are self-contained paragraphs that dead-end.

A developer who gets stuck mid-integration and navigates to the FAQ looking for help will find: how to whitelist a static IP address, and how to change their email. They will close the tab.

**The FAQ's actual function:** For developer tools, the FAQ is a recovery surface — it is where developers go when they are stuck and don't know where else to look. A six-question FAQ with no cross-links is not a recovery surface; it is a placeholder. The questions that belong in a Connect AI FAQ but are absent:

- "I'm getting a 406 error. What does that mean?" → links to Issue 1 fix
- "Authentication keeps failing even though my PAT is correct." → links to Issue 2 fix
- "My query is timing out." → links to Issue 9
- "How do I see what tables are available in my connected source?" → links to Data Explorer
- "Why is my agent running slowly?" → links to schema prefetch guide
- "Is there a limit on how many records I can query per month?" → links to pricing/fair use

**Priority:** Medium. The FAQ is a low-cost, high-leverage recovery surface. Populating it with the actual questions developers ask — sourced from support tickets, community threads, and the issues documented in this audit — would meaningfully reduce support volume.

**Remediation:**
- *Content (PMM/DevRel):* Expand the FAQ to a minimum of 20–25 questions organized by category (Getting Started, Authentication, Querying Data, Performance, Pricing, Troubleshooting). Source questions from: support ticket categories, community forum posts, and this audit's issue list. Every answer must link to the relevant documentation page — the FAQ is an index and triage layer, not a destination.

---

### Issue 39: Docs home page has no beginner/advanced split — all navigation is flat

**What the developer hits:** The docs home at `docs.cloud.cdata.com/en/docs` presents six navigation categories (Dashboard, Sources, Integrations, API, Virtual Databases, SQL Reference) as a flat list with no guidance on which path a new developer should take versus an experienced one. The Quick Start Guide is mentioned as a recommendation but is positioned after the feature description — it is not the first thing a new developer sees or clicks. There is no "New to Connect AI? Start here" banner, no estimated-time callout, no "if you're coming from LangChain / Composio / REST APIs" entry point.

**What new developers actually need from the docs home:**
1. A single, prominent "Start here" path for first-timers (Quick Start → MCP quickstart → first query)
2. A "I'm familiar with MCP, just need the reference" path for experienced developers
3. A "I use [LangChain / Python / LlamaIndex]" entry point that routes to the right framework docs
4. Clear separation between conceptual docs (what Connect AI is, how it works) and reference docs (API specs, SQL syntax, error codes)

None of these exist. The current structure works for a developer who already knows where they're going. It does not work for a developer who just signed up and is trying to figure out where to start.

**Priority:** Medium. The Quick Start Guide exists and is reachable — this is a discoverability and orientation gap, not a content gap. But orientation is the first thing a new developer experiences, and a flat navigation with no path guidance produces a worse first impression than the content warrants.

**Remediation:**
- *Content (PMM/DevRel):* Redesign the docs home to have three explicit entry points above the fold: "New to Connect AI," "Building with MCP," and "Using a specific framework." Each routes to a tailored starting page. Add a "Start here" callout block linking to the Quick Start Guide as the first element on the page, with an estimated time to complete.

---

---

## SEO Audit

The following issues were identified by auditing the marketing site (`www.cdata.com/ai/`), the docs site (`docs.cloud.cdata.com`), the blog (`www.cdata.com/blog/`), and the sitemap and robots.txt files for both domains. Note: the WebFetch tool renders HTML to markdown, so `<head>` tags are not always directly visible — some findings below are confirmed absences and some are unconfirmed. Where an element could not be confirmed present, that is noted. Anything that could not be confirmed present should be verified by opening the browser DevTools network panel on the live page.

---

### Issue 40: No JSON-LD structured data detected on any audited page

**What was found:** No JSON-LD `<script type="application/ld+json">` blocks were detected on the marketing homepage (`cdata.com/ai/`), the docs home (`docs.cloud.cdata.com/en/docs`), the MCP reference page, or the blog index. Structured data is how search engines understand what type of content a page represents — without it, Google has to guess.

**What is missing and what it costs:**

| Page | Schema type needed | What it unlocks in search |
|---|---|---|
| `cdata.com` homepage | `Organization` | Knowledge panel, sitelinks |
| `cdata.com/ai/` | `SoftwareApplication` | App rich results, rating display |
| Every blog post | `BlogPosting` / `Article` | Article rich results, date display, author display |
| Every docs page | `TechArticle` | Article rich results, breadcrumb display |
| FAQ page | `FAQPage` | Accordion FAQ directly in search results |
| Any docs page with steps | `HowTo` | Step-by-step rich results for "how to connect X to Y" queries |
| Navigation / docs | `BreadcrumbList` | Breadcrumb path displayed under the result URL |

The `FAQPage` schema is the fastest win: the FAQ page has six questions that could be marked up today and would earn accordion rich results in Google — a visual format that increases click-through rate significantly and gives CData more vertical space on the search result page for queries like "CData Connect AI rate limit" or "CData MCP timeout."

The `HowTo` schema on quickstart and tutorial pages is the highest-value unlock for developer queries: "how to connect Claude to Salesforce," "how to set up an MCP server for enterprise data" — these are answer-box and rich-result eligible with `HowTo` markup on a page that already has sequential steps.

**Priority:** High. Structured data is not optional for a product competing on developer search traffic. Composio and Airbyte both implement structured data. CData's absence means every competitor earns richer search presentation for the same queries.

**Remediation:**
- *Engineering:* Implement `Organization` JSON-LD on the homepage, `SoftwareApplication` on the product page, `BlogPosting` on every blog post (auto-generated from CMS metadata), and `TechArticle` on every docs page. Add `FAQPage` to the FAQ page immediately — this is a one-day implementation with measurable search result impact within weeks.
- *Content (PMM/DevRel):* Structure quickstart and tutorial content as numbered steps in the HTML so `HowTo` schema can be auto-generated from the page structure. Don't add steps just for schema — structure the content correctly and the schema follows.

---

### Issue 41: Open Graph and Twitter Card tags unconfirmed — social sharing uses browser fallback

**What was found:** No Open Graph tags (`og:title`, `og:description`, `og:image`, `og:url`) or Twitter Card tags were confirmed present on the marketing site or docs site during this audit. If these tags are absent, every link shared to LinkedIn, Slack, Twitter/X, or Discord renders with a browser-generated title and no image — the worst possible first impression for a developer tool that lives and dies by word-of-mouth sharing.

**Why this matters specifically for developer tools:** Developers share documentation links constantly — in Slack threads, GitHub issues, Discord servers, Stack Overflow comments. When a link to a CData docs page unfurls in Slack with no image, no description, and a raw URL as the title, it looks unmaintained. When a Composio tutorial unfurls with a clean card and a one-line description of what it does, it looks professional. The decision of whether to click is made in one second.

**What every page should have:**
```html
<meta property="og:title" content="Connect to Salesforce via MCP — CData Connect AI" />
<meta property="og:description" content="Query Salesforce data from any AI agent using CData's MCP server. Five-minute setup, no SQL required." />
<meta property="og:image" content="https://www.cdata.com/og/connect-ai-mcp.png" />
<meta property="og:url" content="https://docs.cloud.cdata.com/en/API/MCP" />
<meta property="og:type" content="article" />
<meta name="twitter:card" content="summary_large_image" />
```

**Priority:** High. This is a one-time infrastructure implementation (meta tags in the page template) with permanent compounding impact on every link share. The docs site appears to be Next.js — Open Graph tags can be set per-page with one line in the page component.

**Remediation:**
- *Engineering:* Add Open Graph and Twitter Card tags to both the marketing site and docs site page templates. Make `og:title`, `og:description`, and `og:image` dynamic per page — pull from the page title and meta description. Generate a default OG image template for docs pages (page title on CData brand background). This is a one-sprint implementation that covers every existing and future page.

---

### Issue 42: Docs home page has no H1 — page starts with H2

**What was found:** The docs home at `docs.cloud.cdata.com/en/docs` has no H1 tag. The page begins with H2 ("Documentation Index," "Getting Started," "Key Features"). The MCP reference page has an H1 of "MCP" — a single word with no context.

**Why this matters:** The H1 is the single strongest on-page signal Google uses to understand what a page is about. A page with no H1 forces Google to infer the topic from the title tag and body text. A page with an H1 of "MCP" tells Google the page is about the acronym "MCP" — not about "CData Connect AI MCP server," "Model Context Protocol for enterprise data," or any of the keyword-rich phrases a developer would actually search.

**What the H1s should be:**

| Page | Current H1 | Recommended H1 |
|---|---|---|
| `docs.cloud.cdata.com/en/docs` | *(none)* | "CData Connect AI Documentation" |
| `docs.cloud.cdata.com/en/API/MCP` | "MCP" | "MCP Server Integration — Connect AI Model Context Protocol Reference" |
| `docs.cloud.cdata.com/Quick-Start-Guide` | *(unknown)* | "CData Connect AI Quick Start Guide" |
| `docs.cloud.cdata.com/Authentication` | *(unknown)* | "Authentication — CData Connect AI API" |

These are not keyword-stuffed — they are descriptive, specific, and directly match what a developer would type into a search engine to find each page.

**Priority:** High. H1 is foundational on-page SEO. Every docs page without a proper H1 is ranking below its potential for the queries it should own.

**Remediation:**
- *Engineering:* Audit every docs page for H1 presence and correctness. Enforce H1 in the docs page template — every page must have exactly one H1, auto-populated from the page title if no explicit H1 is set. Fix the MCP page H1 from "MCP" to a full, descriptive title.

---

### Issue 43: No last-updated dates on docs pages — content looks stale to Google and to developers

**What was found:** No reader-visible "last updated" timestamp was found on any audited docs page. The sitemap includes `<lastmod>` dates for all 1,600+ docs URLs — values range from February 2026 through May 2026, confirming the content is recent. But those dates are invisible to the developer reading the page and are only partially useful to Google.

**The two-audience problem:** Freshness signals matter to two audiences simultaneously:

1. **Google:** Google uses page freshness as a ranking signal for queries where recency matters. Developer documentation for a product that launched in 2024–2025 is absolutely recency-sensitive. A docs page with no visible date and no `dateModified` in its structured data looks identical to a page that hasn't been touched in three years.

2. **Developers:** A developer reading an MCP integration guide who cannot see when it was written has no way to know if it reflects the current API or a version from eighteen months ago. "Was this written before or after the MCP Streamable HTTP spec changed?" is a real question that a visible date answers immediately.

**What the sitemap `lastmod` dates tell us:** The sitemap has `lastmod` values, but `lastmod` in sitemaps is widely considered an unreliable signal by Google because most CMSs update it on any rebuild regardless of whether content changed. It is not a substitute for `datePublished` / `dateModified` in JSON-LD structured data or a visible timestamp on the page.

**Priority:** Medium. Freshness signals compound over time — pages with visible dates and structured `dateModified` build a freshness track record. Pages without them do not.

**Remediation:**
- *Engineering:* Add a "Last updated: [date]" timestamp to the bottom of every docs page, auto-populated from the CMS last-modified date. Add `datePublished` and `dateModified` fields to the `TechArticle` JSON-LD schema on all docs pages. Add `datePublished` and `dateModified` to `BlogPosting` schema on all blog posts (publish dates are visible on blog cards but may not be in structured data).

---

### Issue 44: Blog posts lack BlogPosting schema — author and date signals not machine-readable

**What was found:** The blog index shows publish dates and author bylines on every post card — the visible content is well-structured. But no `BlogPosting` or `Article` JSON-LD structured data was detected. This means the author, publish date, category, and article body that Google can see in structured data are absent — Google is inferring all of these from the HTML rather than reading them from a declared schema.

**What `BlogPosting` schema unlocks:**
- **Author rich results** — author name and image displayed alongside search results
- **Date display** — publish date shown in search results (helps recency signal)
- **Article rich results** — eligible for top stories carousel for news-adjacent content
- **Knowledge graph association** — byline authors become associated with the topic in Google's entity graph over time

The blog already has the data — author names, dates, categories. The schema just makes it machine-readable. This is likely a one-day CMS template change that applies to every post automatically.

**Priority:** Medium. The content investment is already made — schema markup extracts more search value from it. Without it, the blog competes on content quality alone; with it, it also competes on presentation.

**Remediation:**
- *Engineering:* Add `BlogPosting` JSON-LD to the blog post template, auto-populated from CMS fields: `headline` (post title), `datePublished`, `dateModified`, `author.name`, `author.url` (author profile page), `image` (featured image), `description` (meta description), `url` (canonical URL). One template change; applies to all posts.

---

### Issue 45: Sitemap generated by Screaming Frog — not CMS-native, risks going stale

**What was found:** The `www.cdata.com` sitemap index references two sitemaps (`sitemap.xml` and `sitemap1.xml`), both with a last-modified date of April 1, 2026. The sitemapindex.xml file was generated by Screaming Frog SEO Spider version 23.3 — a desktop crawling tool used for manual site audits, not typically used for production sitemap generation.

**Why this is a process risk:** Screaming Frog sitemaps are generated by crawling the live site at a point in time. They are not automatically updated when new pages are published, existing pages are deleted, or URLs change. If the last Screaming Frog crawl was April 1, 2026, then any page published after that date is not in the sitemap — and Google's discovery of new content depends on crawl budget, internal links, and external links rather than the sitemap. If a page was deleted after April 1, the sitemap still points to a 404.

**The docs sitemap is different:** `docs.cloud.cdata.com/sitemap.xml` appears to be CMS-generated (Next.js), includes 1,600+ URLs with `lastmod` dates ranging through May 2026, and is referenced in the docs `robots.txt`. This is fine. The problem is the marketing site.

**Priority:** Medium. The marketing site's sitemap freshness directly affects how quickly new blog posts, product pages, and landing pages are discovered and indexed by Google. A stale Screaming Frog sitemap is a process failure, not a one-time mistake — it will recur every time someone forgets to re-run the crawl.

**Remediation:**
- *Engineering:* Replace the Screaming Frog-generated sitemap with a CMS-native or server-generated sitemap that updates automatically when content changes. Most modern CMS platforms (WordPress, Contentful, Webflow) have native sitemap plugins. If the marketing site is custom-built, implement a sitemap endpoint that generates URLs from the content database. Submit the new sitemap to Google Search Console and monitor for errors.

---

### Issue 46: hreflang tags absent despite Japanese documentation existing

**What was found:** The docs sitemap includes both `/en/` and `/ja/` URL paths, confirming Japanese documentation exists. However, no `hreflang` tags were detected on audited pages. Without `hreflang`, Google cannot reliably serve the correct language version to users — a Japanese developer may be served the English page, or worse, Google may treat the English and Japanese versions as duplicate content and apply a duplicate content penalty to one of them.

**The hreflang requirement:** Every page that has a language alternate must include `hreflang` tags pointing to each version:
```html
<link rel="alternate" hreflang="en" href="https://docs.cloud.cdata.com/en/API/MCP" />
<link rel="alternate" hreflang="ja" href="https://docs.cloud.cdata.com/ja/API/MCP" />
<link rel="alternate" hreflang="x-default" href="https://docs.cloud.cdata.com/en/API/MCP" />
```
These must appear on both the English and Japanese versions of each page. Missing them is one of the most common technical SEO errors for multilingual sites.

**Priority:** Medium. If Japanese docs exist and are indexed, hreflang must be present to prevent duplicate content issues and ensure correct language serving. This is a template fix — one implementation covers all pages.

**Remediation:**
- *Engineering:* Add `hreflang` link tags to the docs site page template, auto-populated from the available language alternates for each page. Add `x-default` pointing to the English version. Include hreflang in the sitemap `<xhtml:link>` elements as well — Google accepts hreflang from either the page HTML or the sitemap, but both is preferred.

---

### Issue 47: Image alt text uses filenames — keyword opportunity missed and accessibility failed

**What was found:** Images on `cdata.com/ai/` use descriptive filenames as alt text (e.g., `connect-ai-diagram-r2.webp`). Filename-as-alt-text is not descriptive to screen readers and does not contribute keyword signal to Google Images or the page's topic relevance.

**Alt text serves two purposes:**
1. **Accessibility** — screen readers read alt text aloud to visually impaired users. "connect-ai-diagram-r2.webp" communicates nothing. "Diagram showing CData Connect AI connecting AI agents to Salesforce, NetSuite, and Google Sheets via MCP" communicates the content.
2. **SEO** — Google uses alt text as a signal for what an image depicts, contributing to the page's topical relevance and making images eligible for Google Images search results.

The marketing site's hero diagrams and product screenshots are the highest-value images to fix — they appear above the fold, are likely large and visually prominent, and currently carry no keyword signal.

**Priority:** Low. The impact is real but diffuse — alt text contributes to rankings at the margin, not dramatically. Accessibility is a stronger argument for fixing this than SEO alone.

**Remediation:**
- *Content (PMM/DevRel):* Audit all images on `cdata.com/ai/` and the docs site. Replace filename-based alt text with descriptive alt text that explains what the image shows and includes relevant keywords naturally. Establish an alt text standard for the content team: "describe the image as you would to someone who cannot see it, in one sentence."

---

---

## Competitor DX Benchmark

Audited against the same criteria used throughout this document. Competitors evaluated: **Composio** (the tool recommended by every LLM query in the baseline), **Airbyte** (enterprise data movement, overlapping buyer), **Zapier MCP** (no-code MCP competitor). Each was assessed on documentation home, quickstart, MCP reference, navigation, SEO signals, and llms.txt / agent readiness.

---

### Scoring Matrix

| Criteria | CData Connect AI | Composio | Airbyte | Zapier MCP |
|---|---|---|---|---|
| Docs linked in header nav | ❌ Footer only | ✅ Prominent | ✅ It is the site | ⚠️ Resources section |
| Quickstart time estimate | ❌ None | ✅ "5 minutes" | ❌ None | ❌ None |
| Prerequisites listed upfront | ❌ None | ⚠️ Implied | ❌ None | ⚠️ Implied |
| Code samples include imports | ❌ Inconsistent | ✅ Most samples | N/A | N/A |
| Error handling in samples | ❌ None | ❌ None | N/A | N/A |
| Screenshots in docs | ❌ None | ❌ None | ❌ None | ✅ Workflow mockups |
| Model / version disclosure | ❌ None | ✅ GPT-5, Claude Sonnet 4.6 named | ❌ None | ❌ None |
| Latency specifications | ❌ None | ❌ None | ❌ None | ❌ None |
| Cost / token disclosure | ❌ Unclear | ⚠️ Tiered pricing exists | ⚠️ Free trial noted | ⚠️ "Uses your task quota" |
| Developer override / control | ❌ None | ✅ Server management API | N/A | N/A |
| Beginner / advanced split | ❌ Flat | ⚠️ Tutorial vs. reference | ✅ Explicit dual-path | ❌ Marketing only |
| llms.txt quality | ⚠️ Exists, page index only | ✅ Product description first | N/A | N/A |
| Last-updated dates on pages | ❌ None | ❌ None | ❌ None | ❌ None |
| JSON-LD structured data | ❌ None | ❌ None detected | ❌ None detected | ❌ None |
| Open Graph tags | ❌ Unconfirmed | ⚠️ Unconfirmed | ⚠️ Unconfirmed | ⚠️ Unconfirmed |
| H1 tag quality | ❌ Missing or 1 word | ✅ Clear, descriptive | ✅ "Airbyte documentation" | ⚠️ Marketing copy |
| FAQ with cross-links | ❌ 6 questions, no links | ✅ Multiple questions | ✅ Categorized | ❌ Vague |
| Multi-language support | ✅ English + Japanese | ❌ English only | ❌ English only | ❌ English only |
| Agent-specific entry points | ❌ None | ✅ Claude, Codex, Cursor, Hermes | ✅ Agent connectors section | ❌ None |

**Legend:** ✅ Addressed well · ⚠️ Partial or vague · ❌ Absent

---

### Where CData Leads

**Multi-language documentation.** CData publishes English and Japanese docs with 1,600+ URLs in both languages. No audited competitor does this. For enterprise sales into Japanese-headquartered companies (Toyota, Sony, Fujitsu, Hitachi — all potential CData buyers), Japanese documentation is a genuine competitive advantage that is currently invisible because hreflang is missing (Issue 46) and the Japanese docs are not promoted anywhere on the marketing site.

**Enterprise source depth.** CData's 350+ connectors with real SQL semantics, full CRUD, and enterprise-grade authentication (SSO, RBAC, JWT) is a structurally deeper capability than Composio's action-based integrations. This is not reflected in the documentation or onboarding — the quickstart uses Google Sheets as the demo source, which positions CData identically to any lightweight integration tool. The documentation undersells the enterprise depth.

**Structured MCP endpoint.** CData's MCP server returns well-defined tool schemas with rich metadata. The `tools/list` response is more structured than Composio's equivalent. This is a real developer-facing quality signal that is never mentioned in any documentation.

---

### Where Composio Leads

**Model and version disclosure.** Composio's MCP reference explicitly names GPT-5 and Claude Sonnet 4.6 as supported models in code examples. This is a small implementation choice — showing the actual model ID in a code sample — but it tells developers two things at once: which models are tested and supported, and that Composio tracks model versions carefully. CData's MCP docs reference no model anywhere.

**llms.txt quality.** Composio's llms.txt opens with a 40-word product description and positioning statement before any page index. CData's opens with a page list. When an AI assistant fetches these files to answer "what does this product do," Composio gives a clear answer in the first paragraph; CData does not. This is the single fastest content fix that directly improves LLM recommendation rates.

**Agent-specific entry points.** Composio's navigation has dedicated paths for Claude, Codex, Cursor, and Hermes — the actual agents developers are building with. A developer building a Claude Code integration clicks "Claude" and gets a Claude-specific quickstart. CData has no equivalent. Every developer starts from the same generic MCP page regardless of what they're building.

**Quickstart time estimate.** "Run your first tool call in 5 minutes." This one sentence sets an expectation and creates a commitment device — a developer who reads "5 minutes" is more likely to start. CData's quickstart has no time estimate. The actual CData quickstart time (this audit measured ~15 minutes from landing page to first query result) is competitive — it just isn't communicated.

**Docs in header navigation.** Composio has a "Docs" link in the primary header. Airbyte's docs site is their primary developer surface. CData's docs are in the footer under "Support & Services." This is the most visible signal that a product considers documentation a first-class product artifact. It is also the easiest single fix on this list.

**Server management API.** Composio's MCP reference documents list, get, update, and delete operations for MCP servers — production lifecycle management. CData documents the initial connection; Composio documents the entire operational surface. This is a product gap, but it is also a documentation gap: CData has the equivalent capability (PAT management, connection management) that is not surfaced in the MCP reference.

---

### Where the Entire Category Has Gaps

Several issues identified in this audit are not CData-specific competitive disadvantages — they are industry-wide documentation failures. CData should not deprioritize them, but should not treat them as competitive catches either:

- **No error handling in code samples** — none of the audited competitors include try/except or equivalent in their example code. This is a category-wide failure that CData can lead on.
- **No latency specifications** — all four products omit latency data entirely. The first product to publish honest P50/P95 numbers earns immediate credibility with developers who have been burned by slow AI features.
- **No last-updated dates on docs pages** — none. The first docs site to consistently show "Last updated: May 2026" on every page earns implicit trust that competitors do not.
- **No JSON-LD structured data** — none detected across any audited competitor. This is a category-wide gap that CData can move first on. `FAQPage` and `TechArticle` schema are low-effort implementations with direct search result impact.
- **Cost / token transparency** — all competitors are vague or silent on AI inference cost implications. CData is not uniquely opaque here, but the gap remains a blocker for enterprise procurement.

These are not "we're behind" findings — they are "we can lead" opportunities. The developer integration category has set a low bar on documentation quality. CData has more complete enterprise functionality than Composio and more AI-native positioning than Airbyte. The documentation does not reflect either advantage.

---

### Priority Recommendations from the Benchmark

In order of competitive impact:

1. **Add "Docs" to the header nav** — Composio has it, Airbyte is it. CData's most visible signal of developer-seriousness costs one engineering hour.

2. **Rewrite llms.txt preamble** — Composio leads with a product description. CData leads with a page index. One paragraph fix, immediate LLM recommendation improvement.

3. **Add agent-specific entry points** — "Building with Claude? Start here." "Using LangChain? Start here." Composio routes by agent; CData routes by product section. This is a navigation and content structure change, not new content creation.

4. **Add quickstart time estimate** — "First query in 15 minutes." Sets expectation, creates commitment, is honest. One sentence.

5. **Name the model in MCP code examples** — Composio names GPT-5 and Claude Sonnet 4.6 in code. CData names nothing. One line per code sample.

6. **Lead on error handling in samples** — No competitor does this. The first developer tool docs that model production-ready error handling patterns earns lasting credibility with the engineers who will actually deploy it.

7. **Lead on latency disclosure** — No competitor does this. Publishing honest latency numbers (with context: simple SELECT ≈ 3s, cross-source JOIN ≈ 8–12s, why) builds more trust than competitors' silence.

8. **Lead on JSON-LD** — No competitor has structured data. `FAQPage` on the FAQ, `TechArticle` on every docs page, `BlogPosting` on every post. First to implement earns rich results the others don't get.

---

---

## Positioning for the AI Developer Audience

CData is a 20-year-old driver company trying to attract an audience that has never installed an ODBC driver and never will. That is not a problem — it is a positioning opportunity. But only if the website, the messaging, and the product surface are restructured for the audience that is actually arriving, not the audience that arrived ten years ago.

This section is about that structural shift: what AI developers see when they land on CData today, why it does not convert them, and what needs to change.

---

### The identity problem: "driver company" is not a category AI developers shop in

When an AI developer searches for "MCP server enterprise data" and finds CData, they arrive at a website whose primary navigation reads: Platform, Solutions, Developers, Embed, Resources, CData for AI. The hero copy is: *"The connectivity, context, and control needed to turn AI into ROI."*

This copy is written for a VP of Data Engineering justifying a purchase to a CFO. It is not written for the engineer who is building an AI agent at 11pm and needs to know if CData will work with their stack before they commit to integrating it.

The words "connectivity," "context," and "control" mean completely different things to these two audiences:

| Term | What the enterprise buyer hears | What the AI developer hears |
|---|---|---|
| Connectivity | Data pipeline, ETL, BI tool integration | "Does it have a Python SDK? Does it work with LangChain?" |
| Context | Business context, compliance, governance | Context window, token budget, RAG pipeline |
| Control | Admin controls, RBAC, audit logging | Can I override what the AI does? Can I see the SQL it generated? |

The website is speaking one language. The arriving audience speaks another. The product supports both conversations — the documentation proves it. But a developer who bounces from the homepage in 30 seconds never reaches the documentation.

---

### The language gap: enterprise speak vs. AI developer speak

AI developers in 2025 have a specific vocabulary. They think in agents, tools, tool use, MCP servers, function calling, context windows, system prompts, token budgets, and streaming. They do not think in ODBC, JDBC, data connectors, ETL pipelines, or data integration platforms — even when they need exactly the functionality those terms describe.

CData has the product. It speaks the wrong language in the places where the decision is made.

**Current language → AI developer translation needed:**

| CData says | AI developer needs to hear |
|---|---|
| "SQL-queryable data connectivity" | "Your agent can query Salesforce, NetSuite, and Google Sheets in natural language — no SQL required" |
| "350+ pre-built connectors" | "350+ enterprise sources available as MCP tools — Salesforce, SAP, NetSuite, Workday, QuickBooks, and more" |
| "Real-time data access" | "Live data — not synced copies. Your agent reads what's in the system right now." |
| "Enterprise-grade security" | "PAT-based auth, SSO, RBAC — production-ready credentials your security team will approve" |
| "Data integration platform" | "The connection layer between your AI agent and every enterprise data source it needs" |
| "Virtual databases" | "Query across Salesforce and NetSuite in a single SQL statement — CData federates the join" |

None of these require changing what the product does. They require describing what the product does in the vocabulary of the developer who is evaluating it.

---

### The heritage story: 20 years of connectors is an asset, not a liability

CData's driver heritage is the most underleveraged asset in its AI developer positioning. The company has spent two decades writing connectors for enterprise data sources — debugging OAuth flows, handling schema drift, managing API version changes, absorbing pagination edge cases, maintaining compatibility across hundreds of source systems. That work exists in production at thousands of enterprise customers.

Composio is a 2023 startup. Their connectors are good. CData's connectors are battle-tested against edge cases that Composio has not encountered yet.

An AI developer integrating with production Salesforce data will hit rate limits, API version deprecations, custom field naming collisions, and schema changes. CData has absorbed and handled all of these at scale. Composio has not. That is a real differentiation — and the website says nothing about it.

**The story to tell:**

> "We've been writing enterprise connectors since 2004. Our MCP server isn't a weekend project — it's 20 years of production connector expertise exposed through the protocol AI agents actually use. When your agent hits a Salesforce API change at 2am, our connector handles it. When NetSuite updates their schema, we update the mapping. You write the agent; we keep the data flowing."

This is the story that makes Composio's "1000+ toolkits" look thin by comparison. Quantity of integrations is not the same as depth of integration. CData wins on depth. The website does not say this.

---

### What the homepage needs to do for AI developers

The current homepage hero answers: "What is CData?" (a connectivity platform). A developer who already knows what CData is does not need this answer. A developer who does not know what CData is will not understand "connectivity, context, and control" without more context.

The homepage needs to answer three questions in under ten seconds for the AI developer arriving from a Google search or LLM recommendation:

1. **What is it?** — One sentence. "CData gives AI agents live read/write access to 350+ enterprise data sources via MCP."
2. **Will it work with what I'm already using?** — Framework badges. Claude Code. Cursor. LangChain. CrewAI. Python. If their tool is in the list, they keep reading.
3. **How hard is it to set up?** — A time estimate and a code sample. "First query in 15 minutes." One code block showing a working MCP connection.

None of the current above-the-fold content answers any of these three questions for an AI developer. All three can be answered without removing a single word of the existing enterprise-facing content — they belong above it, in a tabbed or segmented hero that routes by audience.

**Recommended hero structure:**

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│   Give your AI agent access to any enterprise data.     │
│                                                         │
│   350+ sources. Live data. MCP-native. 15-minute setup. │
│                                                         │
│   [I'm building an AI agent]   [I'm a data engineer]    │
│                                                         │
│   Works with:                                           │
│   [Claude] [Cursor] [LangChain] [CrewAI] [Python] [→]  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

The two CTA buttons segment the audience immediately — developers click the left button and get the MCP quickstart, data engineers click the right button and get the existing Connect AI / Sync / Drivers story. Both audiences are served. Neither has to decode a homepage that was not written for them.

---

### The product naming problem: one surface, not four

A developer arriving at `cdata.com` encounters: CData Connect AI, CData Sync, CData Drivers, and CData Embed. These are four products with overlapping names, overlapping capabilities in the developer's mind, and no clear signal about which one applies to them.

An AI developer building with MCP needs CData Connect AI. But "Connect AI" sounds like an AI chat product. "CData Drivers" is what shows up in many Google results for CData. "CData Sync" sounds closest to what they need (connecting things). None of the product names map to "MCP server for enterprise data" — which is what the developer searched for.

**The recommendation is not to rename the products** — that is a large organizational decision with implications across sales, partnerships, and existing customers. The recommendation is to add a layer of audience-routing that sits above the product names:

```
Building AI agents?          → CData Connect AI (MCP server, REST API, Python SDK)
Moving data?                 → CData Sync (ETL/ELT, pipelines, scheduled jobs)
Building software products?  → CData Embed (embed connectivity in your app)
Need a database driver?      → CData Drivers (ODBC, JDBC, ADO.NET)
```

This map does not require renaming anything. It adds a translation layer between what the developer is trying to do and what CData calls the product that does it.

---

### Social proof that works for AI developers

The current website uses enterprise logos and case study pull-quotes about BI tool connectivity and ETL pipeline performance. These are the right proof points for data engineers and enterprise buyers. They are the wrong proof points for AI developers.

AI developers read different signals:

| What converts enterprise buyers | What converts AI developers |
|---|---|
| Customer logos (Fortune 500) | GitHub stars and recent commits |
| Case studies with ROI metrics | Code samples that actually work |
| Gartner Magic Quadrant mentions | Framework compatibility badges (LangChain ✓, CrewAI ✓) |
| "Used by 10,000 companies" | "Used by [recognizable dev tool / startup]" |
| White papers | Working demo repositories |
| Analyst quotes | Developer testimonials from Twitter/X or Discord |
| Compliance certifications | "Production-ready" with specific SLA or uptime number |

CData needs both. The enterprise buyer signals already exist. The developer signals do not exist on the website and barely exist anywhere — the GitHub repos have low star counts, there are no developer testimonials, and there is no working demo repository that a developer can clone and run in five minutes.

A public `cdata-connect-ai-demo` repository — the kind of repo this audit built as an interview artifact — should be a first-class marketing asset linked from the developer hub, the MCP docs page, and the GitHub organization readme. It should have a one-command setup (`make demo`) and produce visible results that a developer can screenshot and share.

---

### Community: where AI developers actually are

CData's developer community is a support forum at `community.cdata.com`. The threads are technical and helpful — but it is a support forum, not a developer community. AI developers in 2025 live in:

- **Discord** — real-time discussion, immediate help, developer-to-developer conversation
- **GitHub Discussions** — async technical discussion attached to the code
- **Twitter/X** — product launches, demos, developer announcements
- **Hacker News** — Show HN posts, "Ask HN: what do you use for X"
- **Reddit** — r/MachineLearning, r/LangChain, r/ClaudeAI

CData has no confirmed presence on any of these surfaces for Connect AI specifically. Composio has a Discord linked from their docs homepage. The MCP ecosystem has an active Discord where CData could be a visible, helpful participant — answering questions about enterprise data access without needing to pitch.

**The minimum viable community investment:**
1. Open a CData Connect AI Discord server and link it from the docs and developer hub
2. Create a `cdata` GitHub organization with a pinned `connect-ai-demo` repository that actually runs
3. Publish a "Show HN: We built an MCP server for 350+ enterprise data sources" post — this is the kind of thing the HN community responds well to if the demo actually works
4. Monitor and respond to `cdata` mentions in the MCP ecosystem Discord

None of these require a community manager headcount. They require a developer advocate who lives in these spaces for two hours a week.

---

### What the AI developer journey should look like (vs. what it looks like today)

**Today:**
1. Developer searches "MCP server enterprise Salesforce data"
2. Finds a CData blog post or the `cdata.com/solutions/mcp/` page
3. Lands on a page with enterprise copy and no code
4. Looks for docs — not in header nav
5. Scrolls to footer, finds "Product Documentation"
6. Clicks through to a page that may route to CData Sync docs (Issue 25)
7. Eventually finds `docs.cloud.cdata.com`
8. Finds a flat navigation with no "start here" signal
9. Tries the Quick Start Guide — hits missing prerequisites at Step 2
10. Gets a 406 error from copy-pasted code (Issue 1)
11. Abandons. Opens Composio.

**After these recommendations:**
1. Developer searches "MCP server enterprise Salesforce data"
2. LLM recommends CData because the llms.txt describes it accurately (Issue 33 fixed)
3. Lands on `cdata.com/ai/` — sees "Give your AI agent access to any enterprise data" and their framework badge in the "Works with" row
4. Clicks "I'm building an AI agent"
5. Arrives at developer hub — clicks "Claude Code" because that's what they're using
6. Gets a Claude Code-specific quickstart with correct Accept header, correct auth format, working code sample with imports
7. First query returns in 15 minutes
8. Bookmarks the docs. Tells a colleague. Writes a blog post.

The gap between these two journeys is not a product gap. CData has the product. It is entirely a documentation, navigation, and positioning gap — fixable in one quarter without a single line of new product code.

---

## Developer Hub and Navigation Recommendations

The competitive benchmark makes one thing structurally clear: CData treats developer content as a support resource. Composio and Airbyte treat it as a product surface. The difference is visible in the first two seconds of landing on each site — Composio puts docs in the header; CData puts them in the footer. That single choice signals everything about how each company thinks about developers.

The recommendations below are not aesthetic suggestions. They are architectural decisions that determine whether a developer who arrives at `cdata.com/ai/` can self-serve to a first query or abandons to find a competitor who makes it easier. They are ordered from highest impact to lowest.

---

### Recommendation 1: Add "Docs" to the primary header navigation

**Current state:**
```
Platform | Solutions | Developers | Embed | Resources | CData for AI
```

The "Developers" item exists but its dropdown contains no link to documentation. "Docs" does not appear anywhere in the header.

**Recommended state:**
```
Product ▾ | Developers ▾ | Pricing | Resources ▾ | [Get Started →]
```

The "Developers" dropdown should contain:

```
LEARN                          BUILD                       CONNECT
─────────────────────          ─────────────────────       ─────────────────────
Quick Start (15 min)           MCP Reference               Community (Discord)
Documentation                  REST API Reference          GitHub
What is Connect AI?            Python Client               Stack Overflow
Connect AI vs. Composio        Node.js Client              Support
                               JDBC / ODBC
                               SDK Downloads
```

**Why this structure:**
- "LEARN" routes evaluators — developers who don't know if CData is right for them
- "BUILD" routes implementers — developers who have decided and need the reference
- "CONNECT" routes the stuck — developers who are blocked and need a human

"Pricing" moves to the top level because enterprise buyers look for it there and developers need to know the cost model before they integrate (Issue 32). "Resources" consolidates blog, case studies, and webinars. The `[Get Started →]` button is the only CTA in the header and routes to the quickstart, not the signup page — the quickstart earns the signup, not the other way around.

**The `cdata.com/ai/` product page specifically** should add a persistent "Docs →" link alongside the hero CTA — same pattern as Anthropic's product pages, which show "Read the docs" next to "Get started" above the fold.

---

### Recommendation 2: Build a dedicated developer hub at `cdata.com/developers/`

CData has a "Developers" nav item but no developer hub — a page that is the canonical home for everything a developer needs. Stripe has `stripe.com/docs`. Vercel has `vercel.com/docs`. Anthropic has `docs.anthropic.com`. These are not documentation indexes — they are developer portals that route every developer to the right starting point based on what they're trying to do.

**Recommended page structure for `cdata.com/developers/` (or `developers.cdata.com/`):**

```
─────────────────────────────────────────────────────────────────
CDATA FOR DEVELOPERS

Connect any AI agent to any enterprise data source.
SQL-queryable. Live data. 350+ connectors. MCP-native.

[Quick Start — 15 min]    [Read the Docs →]    [Browse Connectors →]
─────────────────────────────────────────────────────────────────

START WITH YOUR TOOL
────────────────────────────────────────────────
[ Claude Code ]  [ Cursor ]  [ LangChain ]  [ CrewAI ]
[ LlamaIndex ]   [ Python ]  [ Node.js ]    [ More → ]

Each routes to a pre-configured quickstart for that tool.
────────────────────────────────────────────────

POPULAR GUIDES                          REFERENCE
──────────────────────────────          ──────────────────────────────
→ Connect Salesforce to Claude          → MCP Server Reference
→ Query Google Sheets via MCP           → REST API Reference
→ Build a multi-source agent            → SQL Reference
→ Set up enterprise SSO                 → Error Code Reference
→ Optimize agent query performance      → Rate Limits & Fair Use

WHAT'S NEW
──────────────────────────────
[Changelog]  [Status]  [GitHub]  [Community Discord]
─────────────────────────────────────────────────────────────────
```

**The "start with your tool" section is the most important element.** It solves Issue 39 (flat navigation) and the benchmark gap (Composio has agent-specific entry points; CData does not). A developer building with Claude Code clicks "Claude Code" and arrives at a Claude-specific quickstart with Claude-specific code samples and Claude-specific troubleshooting. They do not wade through a generic MCP reference trying to figure out which parts apply to them.

This is not new content — it is routing to existing content organized by the developer's actual entry point. The quickstart, MCP reference, and Python docs already exist. The developer hub is the map that connects them.

---

### Recommendation 3: Restructure the docs site home for three distinct entry points

**Current docs home (`docs.cloud.cdata.com/en/docs`):**
A flat list of six navigation categories with the Quick Start Guide mentioned after the feature description. No path differentiation. No time estimate. No agent-specific routing.

**Recommended docs home structure:**

```
─────────────────────────────────────────────────────────────────
CONNECT AI DOCUMENTATION

[ New to Connect AI?  ]  [ Building with MCP?  ]  [ Using a Framework?     ]
[ Start here — 15 min ]  [ MCP reference →     ]  [ LangChain / CrewAI /   ]
[                     ]  [                     ]  [ LlamaIndex / Python →  ]
─────────────────────────────────────────────────────────────────

QUICK LINKS
──────────────────────────────────────────────
API Reference   |   SQL Reference   |   Error Codes
Authentication  |   Rate Limits     |   Changelog
─────────────────────────────────────────────────────────────────

FULL REFERENCE
─────────────────────────────────────────────────────────────────
Dashboard  |  Sources  |  Integrations  |  API  |  Virtual DBs  |  SQL
```

The three entry-point cards are the critical addition. They replace the implicit "figure it out yourself" with explicit routing:

- **New to Connect AI?** → Quick Start Guide (with time estimate)
- **Building with MCP?** → MCP reference with authentication, tool definitions, code samples
- **Using a Framework?** → Framework-specific docs (LangChain, CrewAI, LlamaIndex, Python, Node.js)

Every developer who arrives at the docs home fits one of these three buckets. Routing them immediately to the right content is the single highest-impact change to the docs site that requires no new content.

---

### Recommendation 4: Create agent-specific quickstart paths

The current MCP quickstart is a single page. Every developer — whether they are building with Claude Code, Cursor, a custom Python agent, or a no-code tool — reads the same page and extracts what applies to them.

**Recommended structure:**

```
MCP Getting Started
│
├── Claude Code (claude.ai/code, Claude Desktop)
│     → Config file path, exact JSON format, test command
│
├── Cursor / Windsurf / Cline
│     → MCP server config in IDE settings, connection verification
│
├── Python (custom agent, LangChain, CrewAI, LlamaIndex)
│     → pip install, connection string, first query, schema prefetch pattern
│
├── Node.js / TypeScript
│     → npm install, connection setup, MCP client configuration
│
└── REST API (no SDK)
      → cURL quickstart, Accept header, auth format, first query
```

Each path is a self-contained page: install, authenticate, run first query, next steps. No developer has to read a section that does not apply to them. Each page links to the shared MCP reference for the full tool definitions, SQL reference for query syntax, and the production optimization guide for scaling.

**This is the same structure Composio uses** — dedicated nav items for Claude, Codex, Cursor, Hermes — and it is the single most visible documentation quality signal for AI-native developer tools in 2025.

---

### Recommendation 5: Surface the Japanese documentation

CData is the only audited product with Japanese documentation — 1,600+ pages across the full doc set. This is a genuine competitive advantage for enterprise sales into Japanese-headquartered multinationals (Toyota, Sony, Hitachi, Fujitsu, NTT) that is currently invisible.

**What needs to happen:**
- Add a language switcher (EN / 日本語) to the docs site header — one component, visible on every page
- Add `hreflang` tags to all 1,600+ pages (Issue 46 — one template change)
- Add a line to the marketing site: "Documentation available in English and Japanese" — specifically on the enterprise and compliance pages where Japanese buyers are evaluating

This costs nothing to create — the content exists. It costs one sprint to surface.

---

### Recommended header (final state)

```
┌─────────────────────────────────────────────────────────────────────┐
│  CData    Product ▾    Developers ▾    Pricing    Resources ▾    EN/日  │
│                                                        [Get Started →] │
└─────────────────────────────────────────────────────────────────────┘
```

**Developers ▾ dropdown:**
```
LEARN                       BUILD                    CONNECT
Quick Start (15 min)        MCP Reference            Community
Documentation               REST API Reference       GitHub
What is Connect AI?         Python / Node.js SDKs    Stack Overflow
Connect AI vs. Composio     JDBC / ODBC              Support

START WITH YOUR TOOL:
[Claude Code] [Cursor] [LangChain] [CrewAI] [Python] [All →]
```

**What this achieves:**
- Documentation is discoverable in the first second (Issue 27)
- Developers are routed by tool, not by product section (benchmark gap)
- Japanese documentation is surfaced to the right buyers
- Pricing is one click from anywhere — no more "how much does this cost" mystery (Issue 32)
- The CTA routes to quickstart, not signup — earns the conversion instead of demanding it

---

## Summary: Issue Priority Matrix

| # | Issue | Category | Priority |
|---|-------|----------|----------|
| 1 | Wrong `Accept` header breaks every copy-pasted example | First-session DX | High |
| 2 | 401 error blames token when username is wrong | First-session DX | High |
| 3 | Setup guide shows steps already completed | First-session DX | Low |
| 4 | No venv guidance in Python quickstart | First-session DX | Medium |
| 5 | Schema metadata bloats LLM context on every tool call | Architecture | High |
| 6 | No terminal-first CLI path — dashboard required | Product roadmap | High |
| 7 | Rate limit shared across all sources — silent failure | Architecture | High |
| 8 | Cross-source JOINs are client-side — full result sets pulled | Architecture | High |
| 9 | 30-second timeout, GUI-only override, no MCP parameter | Product | High |
| 10 | PATs have no scoping — full read/write, no least-privilege | Security | High |
| 11 | Log retention 7 days, dashboard-only, no streaming API | Observability | Medium |
| 12 | Custom MCP tools gated to Business tier | Pricing/docs | Medium |
| 13 | RBAC/SSO gated to Business tier | Pricing/docs | Medium |
| 14 | Local MCP server is stdio-only — no cloud deployment | Architecture | Medium |
| 15 | Error codes 0–79 with no published reference table | Documentation | Medium |
| 16 | No sandbox environment — every query hits production | Product | Medium |
| 17 | 100M record cap undefined — metadata call counting unclear | Pricing/docs | Medium |
| 18 | Framework docs exist (LangChain, LlamaIndex, CrewAI) but no unified matrix or MCP quickstart links | Documentation | Low |
| 19 | `getInstructions` routes agents into expensive discovery loop | Agent runtime | Medium |
| 20 | Three-part table name syntax required but not surfaced until failure | Agent runtime | Medium |
| 21 | Tool naming convention breaks for underscore-containing source names | Agent runtime | Low |
| 22 | No result streaming or pagination through MCP tool interface | Agent runtime | Medium |
| 23 | DataType mapping table exists in REST API docs but not linked from MCP or Query Operation pages | Documentation | Low |
| 24 | MCP server config examples show credentials without secrets guidance | Security | Medium |
| 25 | In-product "Help" links resolve to CData Sync docs — not Connect AI | Documentation | High |
| 26 | Documentation fragmented across subdomains — domain authority split | SEO/Discoverability | High |
| 27 | Docs absent from primary navigation — not in header or developer section | Navigation | High |
| 28 | No model or version disclosure — developers cannot calibrate expectations | Documentation | High |
| 29 | No latency specifications — developers cannot evaluate fitness for use case | Documentation | High |
| 30 | No accuracy or limitation disclosures — "results may vary" is not documentation | Documentation | Medium |
| 31 | No developer override or control mechanism — black-box AI blocks production | Product | High |
| 32 | No cost or token implications disclosed — surprise bills block enterprise adoption | Pricing/docs | High |
| 33 | docs.cloud.cdata.com fails agent-readiness checks independently of www.cdata.com | Agent readiness | High |
| 34 | Quick Start Guide has no prerequisites section — developers arrive unprepared | Documentation | High |
| 35 | Zero screenshots in Quick Start Guide — developers navigate UI blind | Documentation | Medium |
| 36 | Code samples missing imports — not copy-pasteable without trial and error | Documentation | Medium |
| 37 | No error handling in any code sample — production patterns absent | Documentation | Medium |
| 38 | FAQ has 6 questions and no cross-links — useless as a recovery resource | Documentation | Medium |
| 39 | Docs home has no beginner/advanced split — all navigation is flat | Documentation | Medium |
| 40 | No JSON-LD structured data on any page — rich results blocked entirely | SEO | High |
| 41 | Open Graph / Twitter Card tags unconfirmed — social shares render with no image or description | SEO | High |
| 42 | Docs pages have weak or missing H1 tags — MCP page H1 is just "MCP" | SEO | High |
| 43 | No last-updated dates on docs pages — freshness signal absent for Google and developers | SEO | Medium |
| 44 | Blog posts lack BlogPosting schema — author and date not machine-readable | SEO | Medium |
| 45 | Marketing sitemap generated by Screaming Frog — not CMS-native, risks going stale | SEO | Medium |
| 46 | hreflang tags absent despite Japanese docs existing — duplicate content risk | SEO | Medium |
| 47 | Image alt text uses filenames — accessibility failure and missed keyword signal | SEO | Low |
