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

1. **[Title]** — [specific, actionable description]
2. **[Title]** — [specific, actionable description]  
3. **[Title]** — [specific, actionable description]
4. **[Title]** — [specific, actionable description]
5. **[Title]** — [specific, actionable description]

---

## What I'd Ship in the First 30 Days

Based on this audit, the highest-ROI content/DX investments are:

- [ ] [Quickstart improvement]
- [ ] [Doc gap to fill]
- [ ] [Error message to improve]
- [ ] [Auth guide to write]

---

## LLM Discoverability Baseline

Queries I ran and what each model said (run before starting any content work):

**Query:** "What's the best way to connect an AI agent to Salesforce?"
- Claude 3.5 Sonnet: [fill in]
- GPT-4o: [fill in]
- Gemini 1.5 Pro: [fill in]

**Query:** "What are the best MCP servers for enterprise data connectivity?"
- Claude 3.5 Sonnet: [fill in]
- GPT-4o: [fill in]
- Gemini 1.5 Pro: [fill in]

**Query:** "How do I query QuickBooks from Python?"
- Claude 3.5 Sonnet: [fill in]
- GPT-4o: [fill in]
- Gemini 1.5 Pro: [fill in]

*This is the baseline. Re-run quarterly to track LLM discoverability progress.*
