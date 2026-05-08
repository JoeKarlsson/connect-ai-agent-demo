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

The framing: PMM's job isn't to run a developer program — it's to build the positioning, content, and commercial infrastructure that turns developer adoption into enterprise pipeline. DevRel earns trust. PMM turns that trust into revenue. These are different jobs and they fail when blurred.

---

### Competitive Context (set this up before the 90-day plan)

Before talking about what I'd do, here's what we're actually up against.

**Composio** is the most important competitor to understand — not Fivetran, not Airbyte.

| | CData Connect AI | Composio |
|---|---|---|
| **Integrations** | 350+ (ERP, databases, SaaS, financial systems) | 500+ (SaaS-heavy: Slack, Jira, GitHub, HubSpot) |
| **Interface** | SQL-queryable live data | Action-based tool calls |
| **Data engineering path** | JDBC/ODBC, pandas, SQLAlchemy, BI tools | No |
| **Enterprise depth** | SAP, NetSuite, Workday, Oracle, financial systems | Weak |
| **Pricing** | [fill in] | $29/mo for 200K tool calls — unpredictable at scale |
| **Developer awareness** | Low — absent from LLM responses | High — 150K developers, shows up everywhere |
| **SOC2/ISO** | Yes | Yes |

**The gap:** Composio wins on awareness. CData wins on depth, SQL compatibility, and enterprise data coverage — but engineers don't know it. That's a messaging and discoverability problem, not a product problem.

**CData's defensible position Composio can't replicate:**
- SQL interface means pandas, SQLAlchemy, BI tools work natively — Composio's action model doesn't support this
- 25+ years of enterprise connector expertise — OAuth edge cases, schema drift, rate limit handling are already solved
- Fivetran/Airbyte comparison: they replicate data to a warehouse. CData queries the source live. That's what AI agents need.

> "The category question every engineer is asking is: do I build this myself, use Composio, or use CData? Right now CData isn't in that conversation because we're not showing up where the question is being asked. That's fixable. And it's the first thing I'd fix."

---

### Days 1–30: Audit before you build

I've already started. Point to the repo and dx-audit.md.

**Three audits running in parallel:**

**1. Positioning audit** — What does the website say vs. what engineers actually need to hear?
- Does the website make the Composio comparison legible? (It should.)
- Is the SQL-queryable / live connectivity / enterprise depth story clear above the fold?
- What does Sales say to engineering leads, and does it hold up?

**2. DX audit** — I built with Connect AI this week. 6 documented friction points, all fixable. The one that matters most: time-to-first-API-call was ~15 minutes. That's good — but it took debugging two auth errors that shouldn't exist. (Show the audit doc.)

**3. LLM discoverability audit** — I ran the baseline before this interview:

| Query | Claude | What appeared instead |
|---|---|---|
| "Best MCP server for enterprise SaaS data?" | ❌ No CData | Composio, Zapier MCP, Pipedream |
| "How do I connect Claude to Salesforce?" | ❌ No CData | Custom build, community npm packages |
| "Best MCP server for multiple enterprise data endpoints?" | ❌ No CData | Composio ("best overall"), Airbyte MCP |

CData is absent from every response. Composio is named "best overall." That's not a content gap — it's a training data gap. Composio has 150K developers writing READMEs, Stack Overflow answers, and GitHub repos that train LLMs. CData doesn't have that yet. Fixable. Measurable quarterly.

**Day 30 deliverable:** Positioning + DX + discoverability brief to product and leadership. Share findings early — don't wait for perfect data.

---

### Days 31–60: Messaging architecture and launch foundations

**1. Build the competitive differentiation framework**

The core positioning question: when an engineer is choosing between building themselves, using Composio, or using CData — what's the decision criteria and where does CData win?

- DIY: Full control, 6 months, maintenance burden forever
- Composio: Fast setup, action-based, great for SaaS workflows, breaks down on SQL/BI/enterprise ERP use cases
- CData: SQL-native, enterprise depth, live data — the right answer for agents that need to query, analyze, and join across enterprise sources

Turn this into a one-pager Sales can actually use.

**2. Website messaging**

Own the developer-facing pages. What needs to change:
- Lead with the SQL-queryable angle — that's the differentiator Composio can't match
- Make the "live data vs. batch ELT" distinction explicit — engineers conflate CData with Fivetran constantly
- MCP product page: speak to agent builders specifically, not generic "enterprise AI"

**3. Product launch plan for three products**

- **Connect AI Developer Edition + Python SDK**: launch together, same week. Complementary paths to the same layer — MCP for agent builders, DB-API for data engineers.
- **CLI**: launch as beta with clear GA criteria stated publicly. Don't overclaim. Honest beta positioning builds more trust than vague "coming soon."
- Coordinate with DevRel on community seeding; PMM owns the launch assets, website copy, and Sales brief.

**4. Sales/CS enablement brief**

Sales is having conversations with engineering leads who've evaluated Composio. They need:
- The Composio comparison in plain language
- When to lead with MCP, when to lead with SQL/SDK
- How to respond to "we can just build this ourselves"
- One working code example they can share in a follow-up

---

### Days 61–90: Execute, measure, iterate

**Ship 2–3 high-impact content pieces** (written by me, not handed to a technical writer):
- "CData vs. Composio: when SQL connectivity beats action-based tools" — honest, specific, benchmark-backed
- MCP quickstart: Claude agent → Connect AI → enterprise source, under 20 minutes
- "Building vs. buying data connectivity for AI agents" — the ROI case with reproducible numbers

**Measurement infrastructure from day one:**
- UTM + first-touch attribution on all developer content (community-influenced deals need to show up in pipeline reporting)
- LLM mention benchmark re-run (quarterly — need movement data by Q3)
- Developer activation funnel: first API call → trial → production use → expansion

**Present at day 90:** what we shipped, what moved, what we'd do differently. Evidence-first.

---

### Goals framework

| Metric | Target | What it proves |
|---|---|---|
| LLM discoverability rank | CData in top 3 for 3–5 key queries by Q3 | Training data gap is closing |
| Developer activation rate | Define funnel baseline, 20% improvement by Q3 | Evaluation journey is working |
| Sales-influenced deals with developer touchpoints | Establish baseline + attribution | PMM is contributing to pipeline, not just awareness |
| Time-to-first-API-call | Under 15 min vs. Composio benchmark | DX is competitive |
| Competitive win rate vs. Composio | Track in CRM | Messaging is landing in engineering conversations |

---

## Closing (1 min)

Show the GitHub repo briefly — the demo, the audit doc, the LLM baseline screenshots.

> "I built this before the interview because I wanted to understand what engineers actually experience. The demo works. The audit has 6 specific bugs with root causes and fixes. The LLM baseline shows exactly where the discoverability gap is. That's the document I'd share with product and leadership on day 30 — not a strategy deck, but data. The 90-day plan I just walked through is what comes after that audit. The goal isn't developer awareness. It's qualified pipeline that Sales can close."

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
