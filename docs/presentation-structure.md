# CData Interview Presentation Structure
## Principal Developer Marketing Manager — Final Round

**Format:** 20 min presentation + 10 min Q&A  
**Panel:** Product marketing, sales, and product leadership  
**Artifact:** This GitHub repo + docs/dx-audit.md

---

## Opening (1 min)

Don't start with a slide. Start with a live demo.

> "Before I get into positioning and strategy, I want to show you something I built this week."

Open terminal. Run:
```bash
python main.py "show me the top 5 customers by total order value"
```

Let it run. Watch the agent hit multiple tables and return a formatted answer. Then say:

> "That agent just queried a connected database through CData's MCP server. I wrote no SQL. No custom connector. That's the problem this solves — and it took me about [X minutes] to get here from zero. I tracked every step in a developer experience audit that I'll show you at the end."

---

## Part 1: Developer Positioning (7–8 min)

### The problem frame

**The N-Integration Debt Problem** — name it this way, use this framing:

> "A senior engineer building an AI agent knows this pain. You implement connector 1: OAuth flow, token refresh, rate limits, pagination, field permissions. Weeks of work. Connector 2: different OAuth, different rate limits, different field naming for conceptually identical data. Connector 3: completely different auth model.
>
> The real problem isn't connector 1. It's connectors 3 through 12 — and what happens when each breaks independently, on its own schedule. Salesforce updates their API. QuickBooks deprecates an endpoint. You find out when your agent fails in production."

This framing lands because every engineer who's maintained 3+ integrations has lived it. It's not a marketing claim — it's a diagnosis.

### Mapping value props to developer trade-offs

Walk through this table when you say each claim out loud:

| What CData says | What the engineer is actually thinking |
|---|---|
| "350+ sources" | "Do you cover *my* sources? And are they v0.1 skeletons or actually maintained?" |
| "Feature-complete coverage" | "Will it handle OAuth edge cases, rate limit retry, schema drift? Or do I debug those myself?" |
| "Consistent SQL interface" | "I don't want to learn 350 APIs. I want one query pattern." |
| "MCP-native" | "I don't want to write a custom MCP implementation per source. One tool namespace." |

### The positioning statement (own this phrase)

> "Connect AI is the data access layer your team would have built if you had 6 months and dedicated maintenance bandwidth. The question isn't whether you *can* build it — it's whether that's what you want to be working on."

### What earns vs. destroys developer trust

**Earns:** Specific numbers with context. Code that actually runs. Honest about limitations and failure modes.  
**Destroys:** "Powerful." "Seamless." "Enterprise-grade." — without specifics. Code samples with no error handling.

Tie back to the demo: the quickstart either runs in under 20 minutes or it doesn't. That's the real evaluation.

---

## Part 2: 90-Day GTM Execution (12–13 min)

Frame using the three distribution surfaces: human developers, search crawlers, LLMs.  
*"Most developer programs master one while the others stay broken."*

### Days 1–30: Build it and break it

**I've already started this.** Point to the repo and dx-audit.md.

- Benchmarked time-to-first-API-call: **~15 minutes** (under the 20-min target)
- Logged 6 friction points — all documented with root causes and specific fixes
- Ran the LLM discoverability baseline before this interview. Results:

| Query | Claude | What appeared instead |
|---|---|---|
| "Best MCP server for enterprise SaaS data?" | ❌ No CData | Composio, Zapier MCP, Pipedream |
| "How do I connect Claude to Salesforce?" | ❌ No CData | Custom build, community npm packages |
| "Best tools for AI agents + Salesforce/QuickBooks/NetSuite?" | ❌ No CData | MuleSoft, Workato, Boomi, Zapier |
| "Best MCP server for aggregating multiple enterprise data endpoints?" | ❌ No CData | Composio ("best overall"), Airbyte MCP, dbt MCP, mcp-proxy |

> **CData didn't appear in a single response.** That's not a content gap — it's a training data gap. The fix is factual, specific, runnable content in places LLMs actually ingest: READMEs, Stack Overflow answers, GitHub examples, dev.to posts. Not blog posts. This is fixable in 30 days and measurable quarterly.

**Deliverable:** State of Developer Experience brief shared with product + leadership by day 30. Share early findings immediately — don't wait for perfect data.

### Days 31–60: Fix before you publish

> "The biggest ranking jumps I've seen didn't come from new content. They came from fixing what was already broken."

Priority order:
1. **Quickstart first** — if time-to-first-API-call is >20 min, that's job one. Nothing else matters.
2. **README as LLM marketing surface** — READMEs are in training corpora. Factual, specific, runnable content gets cited. Marketing copy doesn't.
3. **Ship 2–3 high-impact pieces:**
   - Benchmark post: "Building vs. buying data connectivity for AI agents" — with reproducible numbers, honest about when DIY makes sense
   - MCP quickstart: Claude agent → Connect AI → [source] in under 20 minutes
   - Python SDK tutorial: DB-API → pandas → SQLAlchemy

Set up measurement infrastructure:
- LLM mention benchmark baseline (quarterly cadence — need baseline *now*)
- AI referral traffic in Plausible/GA4
- UTM + first-touch attribution on all developer content from day one

### Days 61–90: Execute and show evidence

**Launch sequencing for the three products:**
- Connect AI Developer Edition + Python SDK launch together — complementary paths to the same layer
- CLI launches as beta, JDBC-only — positioned as "developer tooling for the driver model," not interchangeable with Connect AI

**DevRel / PMM coordination:**
- DevRel owns: community, code, events, "Dev Zero" (showing up before features ship)
- PMM owns: positioning, website, launches, Sales/CS enablement, commercial bridge

> "DevRel earns developer trust. PMM turns that trust into pipeline. We fail when we blur that line."

**Deliver:** 6-month roadmap with measurement layer established. Even "we tried X, it didn't move Y, here's what we'd change" is more credible than a dashboard full of impressions.

### Goals framework

| Metric | Target | Why it matters |
|---|---|---|
| Time-to-first-API-call | Under 20 min vs. baseline | Gating metric — nothing downstream works without this |
| LLM discoverability | Top 3 responses for 3–5 key queries by Q3 | Emerging channel; baseline needed now |
| AI referral traffic | +30% QoQ from baseline | "The top of the funnel has moved" |
| Community-influenced pipeline | Attribution on deals with developer touchpoints | UTM from day one; this is how you justify budget |

---

## Closing (1 min)

Show `docs/dx-audit.md` briefly.

> "This is the document I'd share with product leadership on day 30. It's not a strategy deck — it's data. Two bugs, exact error messages, how long each one took, what the docs should say. That's what I'd do first. Everything else is downstream of this."

---

## Q&A Prep

**"How do you differentiate Connect AI from Fivetran or Airbyte?"**  
Fivetran/Airbyte are batch ELT — they move data to a warehouse. Connect AI is live connectivity — you query the source directly, which is what AI agents need. Different problem.

**"MCP angle vs. Python SDK angle?"**  
Two developers, same platform. MCP is for AI agent builders (standardized tool-calling, one interface). SDK is for Python data engineers (DB-API familiarity, pandas/SQLAlchemy). Same data layer, different interface choice.

**"What if you only had 30 days?"**  
One thing: measure time-to-first-API-call and fix whatever is blocking it from being under 20 minutes. Everything else is downstream.

**"How do you bridge developer adoption to enterprise pipeline?"**  
UTM and attribution from day one. Surface enterprise signals from community to sales with context — not just names. "Three engineers from Acme Corp asked about auth configuration this week" is an actionable signal. A Discord user list is not.

**"What metrics for year 1?"**  
LLM discoverability rank (quarterly), developer activation rate (funnel from first API call to production), community-influenced pipeline with attribution, time-to-first-value vs. competitors.
