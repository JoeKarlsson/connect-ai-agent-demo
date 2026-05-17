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

### Proof point: this is what the strategy looks like when it ships

Before getting into what I'd do at CData — here's what it looks like when I've done it.

> [Show Ahrefs screenshot]

> "This is organic traffic, impressions, and referring domains for [company] over the last few years. The spike you're seeing on the right is recent — that's the result of a content and discoverability strategy I ran. Organic traffic and impressions essentially flat for two years, then a sharp inflection. That didn't happen by accident. It happened because we shipped specific, runnable content in the places developers actually look — GitHub READMEs, Stack Overflow, technical blog posts with reproducible examples. The same playbook applies here. The difference is CData has a discoverability gap that's measurable and fixable, and I've already started."

This lands the 90-day plan as execution, not theory.

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

### Days 1–30: Instrument, baseline, and fix concurrently

The framing here matters: this isn't "audit, then act." Fixes ship the moment we find them. Data collected on day 5 becomes a remediated redirect on day 8. The goal is a working baseline — not a perfect one.

**Three parallel workstreams from day one, all feeding the same data model:**

**1. Developer pipeline funnel instrumentation**
- Map the full funnel: Discover → Evaluate → First API call → Build → Scale
- Verify analytics coverage at each stage — site, docs, product activation
- Pull existing product usage data: which ConnectAI connectors are getting trial activity? Where are enterprise users and AI agent builders dropping off?
- First funnel health report by week 2 — this is the input that drives prioritization for days 31–90

**2. Keyword cluster + site health**
- Technical SEO audit: redirect chains, Core Web Vitals, crawl health, internal linking
- Keyword cluster mapping: which queries does CData rank for? Which high-value clusters are gaps?
  - Priority clusters for ConnectAI: "enterprise MCP server," "AI agent data access," "SQL connectivity for LLMs," "live data for AI agents"
- Don't wait for the full audit to finish — remediate obvious issues immediately (broken redirects, missing metadata, slow pages)
- Set ranking baselines per cluster so we have a before/after for leadership

**3. LLM discoverability + DX baseline**
- LLM baseline: already run (CData absent from all 5 key queries, Composio named "best overall") — show the table
- DX timing: time-to-first-API-call documented with stopwatch — 6 friction points logged in dx-audit.md
- CData already has `llms.txt` on both `cdata.com` and `docs.cloud.cdata.com` — the foundation exists. Week 1 fix is rewriting the marketing file to be a curated Connect AI guide (SQL vs. action-based, quickstart URL, enterprise source list) rather than a product index. The docs file is a 300-page sitemap; that becomes `llms-full.txt`. One week of work, not a campaign.
- Start shipping into training-data-relevant surfaces in parallel: README improvements, Stack Overflow answers, GitHub repos with working ConnectAI examples — this doesn't wait for the llms.txt rewrite

**The Quick Start is the highest-leverage single page in the developer funnel — and it's broken.**

> [Show slide: "The Quick Start Problem"]

The current Quick Start walks you through signing in, connecting a source, and then waves at a menu of options: Power BI, Excel, Tableau, REST API, OData. It never shows you what success looks like. No expected output. No complete end-to-end flow. No moment where a developer can say "that worked."

That's not a quick start — it's a product tour that stops before the finish line.

**What a developer quick start actually needs to do:**
- Start with `pip install` — not "Step 1: Sign In"
- Show exactly 10–15 lines of code
- Show the exact output that means it worked
- End with the developer having queried real data and knowing what to build next

**The slide:**

| Current Quick Start | What it should be |
|---|---|
| "Connect a source, explore it, use it from AI or BI tools" | "Query your first data source in under 15 minutes" |
| Branches into Power BI / Excel / Tableau / REST / OData | One path: `pip install cdata-connect-ai` → credentials → working query |
| No expected output shown | Shows exact terminal output so you know it worked |
| Ends at "here are your options" | Ends with a working agent making a real query |

Time-to-first-successful-query is the metric. The current Quick Start doesn't optimize for it. This is the first concrete DX fix — rewrite it with a stopwatch in hand and don't ship until a developer with no CData context can hit a working query in under 15 minutes.

**Audiences being instrumented across all three workstreams:** enterprise users (IT leads, data teams), developers (AI agent builders, Python data engineers), and AI agents (Claude Code, Cursor, Copilot). Each discovers CData through a different channel, and each channel breaks differently. ConnectAI is the primary focus.

**Day 30 deliverable:** Funnel baseline + keyword cluster map + LLM/DX findings. Data with clear implications — not a strategy deck.

---

### Days 31–60: Let data drive prioritization

By now the baseline exists. The question is: which part of the developer funnel is actually failing?

**Read the data, then allocate effort:**
- If discovery is the bottleneck → SEO remediation + LLM presence content + community seeding
- If evaluation-to-activation is leaking → fix the quickstart, add honest comparison content (ConnectAI vs. Composio, ConnectAI vs. DIY)
- If activation-to-production is breaking → DX improvements, better error messages, searchable error context
- If product usage data shows specific connectors driving early enterprise traction → build content around those exact sources first

The funnel tells you where to push. You don't decide up front — you respond to signal.

**What ships in parallel, regardless of where the bottleneck is:**
- Highest-ROI SEO remediations already identified in days 1–30 (these are queued, not blocked)
- 1–2 content pieces targeting keyword clusters with clear volume and no strong incumbent
- Messaging framework for all three ConnectAI audiences: enterprise buyers, developer builders, and AI agent integrations each need different landing language
- One concrete DX fix — whatever timing data shows is most directly blocking the 20-minute time-to-value window

**Product usage check-in with product team:**
- Which enterprise connectors are generating the most trial activity?
- Which parts of ConnectAI are generating support tickets? (That's a DX failure signal, not a support problem.)
- What does usage tell us about actual ICP — data engineers, AI agent builders, or enterprise IT?

Messaging architecture gets built around these answers, not before them.

---

### Days 61–90: Iterate on what the data showed — not on the original plan

This is not "execute the plan." It's respond to what moved and what didn't.

**Re-measure at day 60 against day 30 baseline:**
- Did the funnel improve at the stage we targeted? If not, what changed?
- Are keyword cluster rankings moving? Which remediations are showing ROI?
- LLM benchmark re-run — is ConnectAI appearing in any new query responses?
- Product usage: any shift in activation patterns, connector adoption, or enterprise signal volume?

**Ship the next round based on signal:**
- Extend content in keyword clusters showing ranking movement
- Double down on distribution surfaces that drove actual activation (signups, first API calls — not impressions)
- Fix the next-highest-priority DX friction surfaced by product data or funnel analysis

**Content that ships in this window (driven by data, not pre-planned):**
- The comparison piece addressing the evaluation question we saw most in the funnel data
- MCP quickstart updated from dx-audit findings — tested with stopwatch, not assumed
- One piece specifically written for AI agent builders if product usage confirms that's the leading ICP

**Day 90 deliverable:** What moved in the funnel, rankings, and LLM presence — and why. Not an activity report. Evidence-first, with a draft 6-month roadmap built from what we learned.

---

### Goals framework

| Metric | Day 30 baseline | Day 90 target | What it proves |
|---|---|---|---|
| Developer funnel drop-off rate (by stage) | Established from audit | 20%+ improvement at highest-loss stage | We found and fixed the right bottleneck |
| Keyword cluster rankings (5 priority clusters) | Mapped at day 30 | Movement on 3–5 clusters | SEO remediation is working |
| LLM discoverability for ConnectAI | 0/5 key queries (current baseline) | CData in 2–3 responses | Training data gap closing |
| Time-to-first-API-call | ~15 min with friction | Under 15 min, clean | DX is competitive |
| Product trial activation rate | TBD from usage data | Directional improvement + established baseline | Funnel is converting |
| Community-influenced pipeline | Not attributed | Attribution established + first tagged deal | PMM contributing to revenue, not just awareness |

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
