#!/usr/bin/env python3
"""
CData Final Round Interview — Principal Developer Marketing Manager
====================================================================
30-minute presentation + Q&A

Run:
    cd presentations/cdata-interview
    /path/to/.venv/bin/python3 build_slides.py
    open -b "com.apple.Keynote" cdata-interview.pptx

Slide order:
    1.  Title
    2.  LIVE DEMO (switch to terminal)
    3.  Demo result stat — "15 minutes. Zero SQL."
    4.  How it works — architecture flow
    5.  Two paths to the data layer (MCP vs SDK)
    6.  The N-Integration Debt problem
    7.  The positioning statement
    8.  What earns vs. destroys developer trust
    9.  Prior results — CloudQuery impact numbers
   10.  Section divider — 90-Day GTM Plan
   11.  Competitive context — CData vs. Composio
   12.  The discoverability gap (Search · AI · Community)
   13.  Days 1–30: Audit already live, real findings, concurrent fix + workshops
   14.  Content strategy — three audiences, three content strategies
   15.  Days 31–60: Messaging + foundations
   16.  Days 61–90: Ship, measure, iterate
   17.  Goals framework
   18.  Closing — artifacts + QR code
   19.  Q & A
   20.  Thank you
"""

import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from pptx_utils import *
from pptx.util import Emu
from pptx.enum.text import PP_ALIGN

# ── CData brand overrides ──────────────────────────────────────────────────────
# These shadow the pptx_utils (env0) color constants with CData's palette.
# CData primary: #FFE500 yellow  |  Near-black: #1A1A1A  |  Off-white bg: #F5F5F0

CDATA_YELLOW = RGBColor(0xFF, 0xE5, 0x00)
CDATA_DARK   = RGBColor(0x1A, 0x1A, 0x1A)
CDATA_MID    = RGBColor(0x4A, 0x4A, 0x4A)  # body text on light bg
CDATA_GRAY   = RGBColor(0x80, 0x80, 0x80)  # secondary / captions
CDATA_CARD   = RGBColor(0xEC, 0xED, 0xE8)  # card bg (kept neutral)
CDATA_BG     = RGBColor(0xF5, 0xF5, 0xF0)  # slide bg (warm off-white)
CDATA_DIVIDER= RGBColor(0xD0, 0xD0, 0xC8)  # dividers

# Shadow pptx_utils globals used by layout helpers
GREEN    = CDATA_YELLOW   # hero right-panel fill, highlight bar, bullet dots
BG_LIME  = CDATA_YELLOW   # yellow-background slides
BG       = CDATA_BG
DARK     = CDATA_DARK
LGRAY    = CDATA_MID
GRAY     = CDATA_GRAY
CARD     = CDATA_CARD
DIVIDER  = CDATA_DIVIDER
# TEAL was env0's accent for overlines / card titles — map to near-black for CData
TEAL     = CDATA_DARK


# ── CData logo helpers ─────────────────────────────────────────────────────────

def _generate_cdata_logos():
    """Generate tight-cropped CData logo PNGs using Pillow."""
    from PIL import Image, ImageDraw, ImageFont as _IFont
    _FONT = '/System/Library/Fonts/HelveticaNeue.ttc'

    def _make(variant):
        img = Image.new('RGBA', (600, 100), (0, 0, 0, 0))
        d   = ImageDraw.Draw(img)
        if variant == 'light':
            mark_c, text_c = (0xFF, 0xE5, 0x00, 255), (0xFF, 0xFF, 0xFF, 255)
        elif variant == 'yellow':
            mark_c, text_c = (0x1A, 0x1A, 0x1A, 255), (0x1A, 0x1A, 0x1A, 255)
        else:
            mark_c, text_c = (0xFF, 0xE5, 0x00, 255), (0x1A, 0x1A, 0x1A, 255)
        try:
            font = _IFont.truetype(_FONT, 52, index=1)
        except Exception:
            font = _IFont.load_default()
        # C-shaped brand mark
        d.rectangle([4, 18, 48, 74], fill=mark_c)
        d.rectangle([22, 30, 48, 62], fill=(0, 0, 0, 0))
        d.text((62, 16), 'CData', font=font, fill=text_c)
        bbox = img.getbbox()
        return img.crop(bbox) if bbox else img

    for v in ('dark', 'light', 'yellow'):
        _make(v).save(os.path.join(HERE, f'cdata-logo-{v}.png'))

_generate_cdata_logos()

LOGO_DARK  = os.path.join(HERE, 'cdata-logo-dark.png')
LOGO_LIGHT = os.path.join(HERE, 'cdata-logo-light.png')
LOGO_YEL   = os.path.join(HERE, 'cdata-logo-yellow.png')

# Compute display dimensions from actual PNG pixel dimensions
def _logo_emu_dims(path, target_h=380000):
    from PIL import Image as _I
    pw, ph = _I.open(path).size
    h = Emu(target_h)
    w = int(h * pw / ph)
    return w, h

_CDATA_LOGO_W, _CDATA_LOGO_H = _logo_emu_dims(LOGO_DARK)
_CDATA_LOGO_L = W - ML - _CDATA_LOGO_W
# Vertically center logo with overline text (overline center ≈ y=450000)
_CDATA_LOGO_T = Emu(450000) - _CDATA_LOGO_H // 2


def add_cdata_logo(slide, variant='dark'):
    """Add CData logo to upper-right corner. Call LAST so it renders on top."""
    path = {'dark': LOGO_DARK, 'light': LOGO_LIGHT, 'yellow': LOGO_YEL}.get(variant, LOGO_DARK)
    slide.shapes.add_picture(path, _CDATA_LOGO_L, _CDATA_LOGO_T, _CDATA_LOGO_W, _CDATA_LOGO_H)


def _generate_qr_code(url):
    """Generate a QR code PNG for the given URL and return the local path."""
    import qrcode as _qr
    from PIL import Image as _I
    qr = _qr.QRCode(version=2, box_size=12, border=2,
                     error_correction=_qr.constants.ERROR_CORRECT_M)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color='black', back_color='white').convert('RGBA')
    path = os.path.join(HERE, 'repo-qr.png')
    img.save(path)
    return path

_REPO_QR = _generate_qr_code('https://github.com/JoeKarlsson/connect-ai-agent-demo')


# ── Talk config ────────────────────────────────────────────────────────────────

TALK = {
    'title':    'Developer Trust at Enterprise Scale',
    'subtitle': 'Content strategy, competitive positioning,\nand a 90-day GTM plan for CData Connect AI.',
    'speaker':  'Joe Karlsson',
    'company':  'joekarlsson.com',
    'event':    'CData Final Round',
    'date':     'MAY 2026',
    'linkedin': 'https://www.linkedin.com/in/joekarlsson',
}

PAD = Emu(185000)

# ── CData-branded overrides for pptx_utils layout helpers ─────────────────────
# pptx_utils functions use their own module's color constants (TEAL, GHBG, etc).
# These local definitions shadow those functions to use CData palette instead.

def overline(slide, text, left=None):
    """Category label in CData near-black (overrides pptx_utils teal)."""
    box(slide, text.upper(), left or ML, Emu(340000), TXT_W, Emu(220000),
        size=11, bold=False, color=CDATA_DARK, font='DM Sans')


def three_cards(slide, items, top=None, card_h=None, animate=True):
    _top    = top    or CONT_S
    _card_h = card_h or Emu(3080000)
    gap = Emu(185000)
    cw  = (CW - 2 * gap) / 3
    pad = Emu(185000)
    groups = []
    for i, item in enumerate(items):
        l = ML + i * (cw + gap)
        bg  = shape(slide, l, _top, cw, _card_h, fill=CDATA_CARD)
        ttl = box(slide, item['title'], l + pad, _top + pad, cw - 2 * pad, Emu(430000),
                  size=17, bold=True, color=CDATA_DARK, wrap=True)
        bt  = _top + pad + Emu(460000)
        bdy = box(slide, item['body'], l + pad, bt, cw - 2 * pad,
                  _card_h - (bt - _top) - pad,
                  size=15, color=CDATA_MID, wrap=True)
        groups.append([bg.shape_id, ttl.shape_id, bdy.shape_id])
    if animate:
        add_appear_animations(slide, groups)


def two_cards(slide, items, top=None, card_h=None, animate=True):
    _top    = top    or CONTENT_T
    _card_h = card_h or Emu(3080000)
    gap = Emu(220000)
    cw  = (CW - gap) / 2
    pad = Emu(185000)
    groups = []
    for i, item in enumerate(items):
        l = ML + i * (cw + gap)
        bg  = shape(slide, l, _top, cw, _card_h, fill=CDATA_CARD)
        ttl = box(slide, item['title'], l + pad, _top + pad, cw - 2 * pad, Emu(430000),
                  size=17, bold=True, color=CDATA_DARK, wrap=True)
        bt  = _top + pad + Emu(460000)
        bdy = box(slide, item['body'], l + pad, bt, cw - 2 * pad,
                  _card_h - (bt - _top) - pad,
                  size=15, color=CDATA_MID, wrap=True)
        groups.append([bg.shape_id, ttl.shape_id, bdy.shape_id])
    if animate:
        add_appear_animations(slide, groups)


def highlight_box(slide, text, top, width=None, height=None):
    """CData callout box: card-color bg + yellow left accent bar."""
    import textwrap as _tw
    l = ML
    w = width or CW
    if height is None:
        cpl     = max(20, int((w - Emu(260000)) / 12700 / 7))
        n_lines = max(1, len(_tw.wrap(text, cpl)))
        height  = int(n_lines * int(13 * 12700 * 1.5) + Emu(220000))
    bg   = shape(slide, l, top, w, height, fill=CDATA_CARD, rounded=False)
    bar  = shape(slide, l, top, Emu(60000), height, fill=CDATA_YELLOW, rounded=False)
    body = box(slide, text, l + Emu(170000), top + Emu(100000),
               w - Emu(260000), height - Emu(170000),
               size=13, color=CDATA_DARK, wrap=True)
    return [bg.shape_id, bar.shape_id, body.shape_id]


# ── Speaker scripts ────────────────────────────────────────────────────────────

SCRIPTS = {
    1: """· Don't explain the demo upfront — just say "before strategy, I want to show you something I built this week"
· The repo is public: github.com/JoeKarlsson/connect-ai-agent-demo — they can pull it up right now
· You built this in ~4 hours using Developer Edition; credibility signal, not a code showcase""",

    2: """· The agent makes 3–4 tool calls to answer one question — watch the ↳ indicators appear
· Without CData, this is custom OAuth, custom pagination, custom field mapping per source — weeks of work
· Claude doesn't know anything about the data schema; it's routing blind through CData's SQL interface
· Don't narrate — let the output land, then advance""",

    3: """· The three bullet points are content implications, not bug complaints — frame them that way verbally
· "The quickstart is the product's first content touchpoint" — this is PMM thinking. The first thing a developer reads IS the content strategy in action.
· Anthropic is a named customer in the JD — say explicitly: "the same connectivity layer they're using." That's the social proof the content needs to reflect.
· The point of building with the product: you can't write credible content about something you haven't used. This is the research method, not the deliverable.""",

    4: """· MCP is Anthropic's open protocol — CData being MCP-native means any Claude agent works with it without modification
· Key architectural distinction vs. Composio: Composio is action-based (do something), CData is query-based (get data) — those are fundamentally different models
· SQL interface = pandas, SQLAlchemy, BI tools work natively — this is a capability Composio's model structurally cannot support
· "Add a source in the dashboard → immediately queryable" is the compounding leverage argument: platform gets more valuable as sources grow, with zero additional engineering""",

    5: """· Sales commonly pitches MCP to data engineering teams — wrong audience. DB-API and pandas are the entry points for that persona.
· MCP is newer (2024) and moving fast — VS Code, Cursor, Windsurf all added support within months of the protocol launching
· The SDK path is the "trusted path" — any Python data engineer recognizes DB-API cursor patterns immediately, no learning curve
· Content strategy mirrors this split: separate quickstarts, separate use cases, same underlying platform story. Don't conflate them in one page.""",

    6: """· This framing works because it's from the engineer's perspective, not the product manager's
· Composio solves connector 1 well (Slack, Jira, GitHub). It does not solve connectors 3–12 at enterprise depth (SAP, NetSuite, Workday, financial systems) — that's the gap
· "Each breaks independently, on its own schedule" — this is the hidden cost nobody puts in the build vs. buy spreadsheet
· Worth saying out loud: "I've maintained integrations like this. This is the pain I'm describing." Personal credibility.""",

    7: """· "Would have built" acknowledges engineering competence — never say "you can't build this." They can. The question is whether they should.
· The 3 Cs come directly from the JD — Connectivity, Context, Control — use their language back at them
· 25 years of enterprise connectors = OAuth edge cases, schema drift, rate limit handling solved across hundreds of API versions. Nobody replicates this quickly.
· If they push on "what stops Composio from building more enterprise connectors?" — the answer is accumulated institutional knowledge of API quirks, not just connector count""",

    8: """· Documentation, quickstarts, and error messages are content — PMM should own the quality bar for all of them, not just blog posts
· The quickstart is the most important marketing asset CData has. It runs before any sales conversation happens.
· "Docs that don't show what happens when auth fails" — CData's 401 error message is a live example right now. That's a content fix, not just a product fix.
· Engineers forward docs to their team. If the docs are wrong once, trust in everything else drops. One bad experience spreads.""",

    9: """· These are real numbers from CloudQuery — same methodology, 8 weeks in
· Don't over-explain the context; let the numbers speak and move on quickly
· Docs quickstart completions 0→23/wk is the exact metric you're proposing for CData — you've already moved it at another company
· The $10K SQO with content first-touch is why UTM attribution from day one isn't optional — if you don't track it, you can't prove it
· "Same methodology" is the bridge sentence: Part 1 was the framework, this slide is the proof, Part 2 is the plan""",

    10: """· Say the DevRel/PMM split line out loud: "DevRel earns developer trust. PMM turns it into pipeline. These are different jobs." Then pause.
· This matters for the panel because they're hiring alongside a Director of DevRel. They're thinking about overlap. Address it proactively — don't leave it to Q&A.
· The split in practice: DevRel writes from community experience and authenticity; PMM writes for evaluation cycles and purchase framing. DevRel owns Discord, events, and community code. PMM owns the website, product launches, Sales enablement, and the commercial bridge from developer adoption to pipeline.
· "Different jobs" means you're not going to duplicate DevRel's work or step on their territory — and you're not going to hand them PMM work either.""",

    11: """· Composio has 150K developers — that's why it dominates LLM responses and search results. Content volume, not product quality.
· Key question Composio structurally can't answer: "Can I query this with pandas?" No. CData: Yes.
· Composio's $29/mo is unpredictable at enterprise scale (200K tool calls) — procurement hates consumption pricing without caps
· Fivetran/Airbyte aren't in this category: they replicate to a warehouse on a schedule. CData queries live. Different infrastructure decision, different buyer.
· "Messaging problem, not a product problem" — the most important sentence on this slide. Say it slowly.""",

    12: """· These are actual queries run 2026-05-08 — not hypothetical. Show the screenshot if questioned.
· SEO gap: "Python DB-API Salesforce" should return CData immediately. It doesn't. That's a fixable content problem, not a domain authority problem.
· Community gap: Composio's 150K devs are writing Stack Overflow answers and READMEs that train LLMs. Even 1,000 CData developers writing specific technical content would shift this.
· AEO and SEO have the same fix: specific, runnable, factual content. READMEs train LLMs. Tutorials rank in search. Both build community signal.
· Quarterly re-audit shows leadership a trend line, not just a snapshot — you need the baseline now to show movement in Q3""",

    13: """· The headline is literally the JD: "testing integration flows yourself and logging what breaks before prospects find it" — this slide shows I already did that.
· Card 2 is the proof: real findings, real timings, real root causes. The Accept header bug is in CData's own GitHub repos. Every developer who copies the documented pattern hits it. One-line fix.
· "Filed. Goes to Product as roadmap input" — this is the JD's "translate developer feedback into roadmap input" made concrete. Not a memo. Not a slide. A ticket.
· Card 3: high-severity findings don't wait for a report. Two workstreams: audit continues, fixes ship immediately. That's what "improve" means in the JD — not just log it, fix it.
· Workshop framing: Product + Eng respond to shared observation, not written briefs. Start the quickstart cold with them watching. When it breaks, you all see it at the same time.
· Sales + CS: this is where the enterprise leader content track comes from. They know every objection that doesn't have a sharp answer — that's a messaging gap list handed to you for free.
· Point to the repo and dx-audit.md here: "This is the document I would share with Product leadership on day 30. Not a strategy deck — data." """,

    14: """· The key insight: developers don't close enterprise deals — but enterprise deals don't close without developer trust. Content has to serve both buying motions.
· Card 1 (developer eval): the JD says "developers decide in the first 20 minutes." If the quickstart is broken, nothing else matters. This content earns the technical trust.
· Card 2 (the bridge) is the most important card for this panel: benchmark pieces and architecture docs are technically credible AND business-outcome legible. That's the format that gets a developer's evaluation turned into a signed contract. One comparison post can travel from engineer → technical lead → VP with no rewriting.
· Card 3 (enterprise buying): PMM owns the battlecard — Sales shouldn't be building this themselves. The customer reference (Anthropic, Databricks, Palantir) is the enterprise trust signal that procurement needs to see.
· CData's customer base is explicitly enterprise — Anthropic, Databricks, Microsoft, Google. That means the enterprise buying track isn't optional. Every piece of developer content needs a path to the enterprise evaluation.
· "PMM owns this — Sales shouldn't have to build it" — say this out loud. It signals you understand the scope of the role.""",

    15: """· Three things, three distinct PMM artifacts: messaging brief, launch plan, website copy + battlecard. Name the artifact for each.
· The messaging architecture is the foundation — everything else (website copy, launch assets, Sales brief) is downstream of getting this right first.
· Developer Edition + Python SDK launch together: this is a strategic call, not a scheduling convenience. Launching them separately fragments the platform story.
· "PMM writes this copy; it doesn't get briefed out" — say this explicitly. The JD says "not hand off to a technical writer." The panel needs to hear you understand that.
· Product launch GTM: emphasize the cross-functional coordination — you're aligning Product on messaging, Engineering on technical accuracy, Sales on how to position it, Marketing on campaign support. That's the scope of "principal."
· CLI beta positioning: "explicit GA criteria stated publicly" is the trust signal. Developers remember when you overclaim and when you under-deliver.""",

    16: """· Lead with the content program infrastructure card — the panel wants to know you're building a machine, not doing a sprint.
· The editorial calendar is the key artifact: who writes what, how often, on what channel. PMM owns competitive and positioning content; DevRel owns community and tutorial content. That split is the collaboration model made operational.
· "Each piece is a template" — the quickstart video isn't just a video, it's the format spec for every quickstart video after it. The competitive comparison isn't just one article, it's the tone and evidence standard for all competitive content.
· "CData vs. Composio" needs to be honest: if Composio beats CData at something, say so. Engineers trust content that acknowledges tradeoffs.
· Day 90 is a program review: editorial calendar running, ownership clear, attribution model live, early evidence of what's working. "Three one-off pieces" is not success — a running content machine is.""",

    17: """· Lead with the top row: developer → pipeline attribution. UTM + first-touch attribution from day 1. Miss the first 30 days and you've lost attribution data you can never recover — it's not retro-fittable.
· This is the metric that justifies the PMM function to finance: "here are the deals with a developer touchpoint, here's the first-touch content, here's the pipeline value." Without this, you're reporting impressions to a CFO.
· Discoverability rank is quarterly — LLM training data updates on 3–6 month cycles, so weekly tracking is noise. You need the baseline now to show Q3 movement.
· Activation rate bridges DevRel and PMM: DevRel drives top-of-funnel developer trust, PMM measures whether that trust is converting into trial starts and pipeline.
· Win rate vs. Composio in CRM: this is the metric that tells you whether messaging is landing in real engineering conversations, not just marketing dashboards.""",

    18: """· "I built this before the interview because I needed to understand what engineers actually experience — not to impress, but to have real data"
· DX audit = what you'd hand to engineering on day 1
· Discoverability baseline = what you'd present to leadership on day 30
· Point to the QR code — repo is live, invite them to try it themselves""",

    19: """LIKELY QUESTIONS:

· Fivetran/Airbyte? Batch ELT moves data to a warehouse on a schedule. Connect AI queries live. AI agents need current data — a 4-hour-old snapshot breaks real-time workflows. Different infrastructure decision entirely.
· MCP vs. SDK? Two developers, same platform. Pitching MCP to a data engineer signals you don't understand the audience. Sales needs to know which door to open first.
· Only 30 days? Fix the Accept header bug and the error message. Those two alone shave 10+ minutes off the critical path for every new developer. Everything else is downstream.
· Dev adoption → pipeline? UTM from day one, or you can never prove the investment. "Three engineers from Acme asked about auth config this week" is actionable signal. A Discord user list is not.
· Build vs. buy objection? Make it a reproducible formula: 10 connectors × 2 weeks = 20 weeks of engineering time. Then add: what happens when Salesforce updates their API? Make the math real.
· DevRel/PMM line? DevRel owns community authenticity — the moment DevRel content looks like it's optimized for conversion, developers stop trusting it. PMM owns the commercial bridge. Both functions fail when blurred.
· Day-to-day with the DevRel Director? Weekly editorial sync: who owns each piece in the queue, clear handoffs. Shared content calendar with ownership columns — no co-authorship ambiguity. I write for evaluation cycles and purchase framing; they write from community experience and authenticity. Joint metric is developer activation rate: DevRel drives top-of-funnel trust, PMM measures whether that trust converts to pipeline. That shared metric is what keeps both functions pointing at the same goal.""",

    20: """· Leave on screen — people will scan for contact info
· joekarlsson.com has additional context on developer marketing strategy""",
}


# ── Slide builders ─────────────────────────────────────────────────────────────

def slide_01_title(prs):
    """Hero title — white bg, yellow right panel."""
    s = blank(prs)
    set_bg(s, RGBColor(0xFF, 0xFF, 0xFF))
    shape(s, LP_L, LP_T, LP_W, LP_H, fill=CDATA_YELLOW, rounded=False)
    add_cdata_logo(s, 'dark')
    box(s, f"{TALK['event'].upper()}  ·  {TALK['date']}", ML, Emu(1280000), TXT_W, Emu(300000),
        size=12, bold=True, color=CDATA_DARK, font='DM Sans')
    box(s, TALK['title'], ML, Emu(1680000), TXT_W, Emu(1600000),
        size=46, bold=True, color=CDATA_DARK, wrap=True)
    box(s, TALK['subtitle'], ML, Emu(3450000), TXT_W, Emu(1000000),
        size=17, color=CDATA_GRAY, wrap=True)
    box(s, TALK['speaker'], ML, Emu(4700000), TXT_W, Emu(370000),
        size=16, bold=True, color=CDATA_DARK)
    box(s, TALK['company'], ML, Emu(5100000), TXT_W, Emu(330000),
        size=13, color=CDATA_GRAY, url='https://joekarlsson.com')
    set_notes(s, SCRIPTS[1])


def slide_02_live_demo(prs):
    """Full-screen LIVE DEMO card — presenter switches to terminal here."""
    s = blank(prs)
    set_bg(s, CDATA_DARK)
    add_cdata_logo(s, 'light')

    mid_y = H // 2 - Emu(900000)
    box(s, '▶', 0, mid_y, W, Emu(700000),
        size=44, bold=True, color=CDATA_YELLOW, align=PP_ALIGN.CENTER)
    box(s, 'LIVE DEMO', 0, mid_y + Emu(750000), W, Emu(400000),
        size=14, bold=True, color=CDATA_YELLOW, align=PP_ALIGN.CENTER, font='DM Sans')
    box(s, 'Enterprise Data AI Agent', 0, mid_y + Emu(1210000), W, Emu(500000),
        size=28, bold=True, color=RGBColor(0xF0, 0xF0, 0xF0), align=PP_ALIGN.CENTER)

    cmd_y = mid_y + Emu(1850000)
    cmd_h = Emu(480000)
    shape(s, ML + Emu(800000), cmd_y, CW - Emu(1600000), cmd_h,
          fill=RGBColor(0x2A, 0x2A, 0x2A), rounded=True)
    box(s, 'python main.py "Who is my top rep and what are their biggest open deals?"',
        ML + Emu(1000000), cmd_y + Emu(120000), CW - Emu(2000000), Emu(270000),
        size=13, color=CDATA_YELLOW, font='Courier New', wrap=False)
    set_notes(s, SCRIPTS[2])


def slide_03_demo_result(prs):
    """Yellow stat — the demo result."""
    s = blank(prs)
    set_bg(s, CDATA_YELLOW)
    add_cdata_logo(s, 'yellow')

    box(s, 'THE RESULT', 0, Emu(620000), W, Emu(270000),
        size=11, bold=True, color=CDATA_DARK, align=PP_ALIGN.CENTER, font='DM Sans')
    box(s, '15 minutes.', 0, Emu(1050000), W, Emu(1550000),
        size=88, bold=True, color=CDATA_DARK, align=PP_ALIGN.CENTER)
    box(s, 'Zero SQL. Natural language to cross-source enterprise data.',
        0, Emu(2700000), W, Emu(500000),
        size=22, color=CDATA_DARK, align=PP_ALIGN.CENTER, wrap=True)

    shape(s, ML + Emu(3500000), Emu(3380000), CW - Emu(7000000), Emu(34000),
          fill=CDATA_DARK, rounded=False)

    implications = [
        "The quickstart is the product's first content touchpoint — it has to work.",
        "Auth errors without root causes = a troubleshooting guide that doesn't exist yet.",
        "Missing terminal-first path = a whole developer persona the content doesn't reach.",
    ]
    dy = Emu(3560000)
    for d in implications:
        box(s, d, ML, dy, CW, Emu(300000),
            size=13, color=CDATA_DARK, wrap=True)
        dy += Emu(330000)

    box(s, 'Anthropic, Databricks, and Palantir use this connectivity layer. The content has to be worthy of that reference.',
        0, Emu(4800000), W, Emu(400000),
        size=14, bold=True, color=CDATA_DARK, align=PP_ALIGN.CENTER, wrap=True)

    source_label(s,
        'Full first-session audit: docs/dx-audit.md  ·  github.com/JoeKarlsson/connect-ai-agent-demo',
        top=Emu(6300000))
    set_notes(s, SCRIPTS[3])


def slide_04_architecture(prs):
    """Architecture flow — how the agent actually works."""
    s = blank(prs)
    set_bg(s, CDATA_BG)
    add_cdata_logo(s, 'dark')
    overline(s, 'HOW IT WORKS')
    h1(s, 'Natural language to enterprise data in one hop.', size=34)

    nodes = [
        ('Natural\nLanguage',  CDATA_CARD,   'Plain English\nquestion',         CDATA_DARK),
        ('Claude\nSonnet 4.6', CDATA_YELLOW, 'Decides which\ntools to call',    CDATA_DARK),
        ('CData\nMCP Server',  CDATA_DARK,   '350+ sources\none SQL interface', RGBColor(0xFF,0xFF,0xFF)),
        ('Data\nSources',      CDATA_CARD,   'Sheets · GitHub\nSAP · Postgres', CDATA_DARK),
    ]

    n      = len(nodes)
    nw     = Emu(1900000)
    aw     = Emu(380000)
    total  = n * nw + (n - 1) * aw
    sx     = ML + (CW - total) // 2
    nh     = Emu(1450000)
    ny     = Emu(2350000)
    lh     = Emu(600000)

    groups = []
    for i, (title, fill, sub_txt, txt_c) in enumerate(nodes):
        nx  = sx + i * (nw + aw)
        bg  = shape(s, nx, ny, nw, nh, fill=fill, rounded=True)
        ttl = box(s, title, nx, ny + Emu(300000), nw, Emu(600000),
                  size=18, bold=True, color=txt_c, align=PP_ALIGN.CENTER, wrap=True)
        lbl = box(s, sub_txt, nx, ny + nh + Emu(130000), nw, lh,
                  size=11, color=CDATA_GRAY, align=PP_ALIGN.CENTER, wrap=True)
        if i < n - 1:
            ax  = nx + nw
            ay  = ny + nh // 2 - Emu(100000)
            arr = box(s, '→', ax, ay, aw, Emu(300000),
                      size=22, bold=True, color=CDATA_DIVIDER, align=PP_ALIGN.CENTER)
            groups.append([bg.shape_id, ttl.shape_id, lbl.shape_id, arr.shape_id])
        else:
            groups.append([bg.shape_id, ttl.shape_id, lbl.shape_id])

    add_appear_animations(s, groups)
    highlight_box(s,
        'Add a source in the CData dashboard → immediately queryable. No code changes. No new connector to write.',
        top=Emu(4650000))
    set_notes(s, SCRIPTS[4])


def slide_05_two_paths(prs):
    """Two cards — MCP path vs Python SDK path."""
    s = blank(prs)
    set_bg(s, CDATA_BG)
    add_cdata_logo(s, 'dark')
    overline(s, 'TWO PATHS, ONE DATA LAYER')
    h1(s, 'Two developers. Same platform. Different interfaces.', size=26)
    sub(s, 'Same data layer underneath. Right interface for each developer.')

    two_cards(s, [
        {
            'title': 'MCP — for AI agent builders',
            'body':  'Standardized tool-calling interface (Model Context Protocol).\n'
                     'One tool namespace exposes 350+ sources.\n'
                     'Connect Claude, GPT-4o, or any MCP-compatible agent.\n'
                     'No per-source connector code.',
        },
        {
            'title': 'Python SDK — for data engineers',
            'body':  'DB-API 2.0 cursor interface — familiar to any Python data engineer.\n'
                     'Works natively with pandas, SQLAlchemy, ETL pipelines.\n'
                     'Same underlying data layer as MCP.\n'
                     'Different evaluation criteria, different content.',
        },
    ], top=CONT_S, animate=True)
    set_notes(s, SCRIPTS[5])


def slide_06_problem(prs):
    """Three cards — the N-Integration Debt problem frame."""
    s = blank(prs)
    set_bg(s, CDATA_BG)
    add_cdata_logo(s, 'dark')
    overline(s, 'THE PROBLEM')
    h1(s, 'The N-Integration Debt Problem.', size=40)
    sub(s, "The pain every engineer who's maintained 3+ integrations has lived.")

    three_cards(s, [
        {
            'title': 'Connector 1 — weeks of work',
            'body':  'OAuth flow. Token refresh. Rate limits. Pagination. Field-level permissions. '
                     'You build it once and it works.',
        },
        {
            'title': 'Connectors 3–12 — the real problem',
            'body':  'Different OAuth. Different rate limits. Different field naming for conceptually '
                     'identical data. Each breaks independently, on its own schedule.',
        },
        {
            'title': 'Production failure at 2am',
            'body':  'Salesforce updates their API. QuickBooks deprecates an endpoint. '
                     'You find out when your agent fails in production — not from a changelog.',
        },
    ], top=CONT_S, card_h=Emu(2400000), animate=True)
    set_notes(s, SCRIPTS[6])


def slide_07_positioning(prs):
    """Yellow mandate — the positioning statement."""
    s = blank(prs)
    set_bg(s, CDATA_YELLOW)
    add_cdata_logo(s, 'yellow')

    box(s, 'THE POSITIONING', 0, Emu(580000), W, Emu(270000),
        size=11, bold=True, color=CDATA_DARK, align=PP_ALIGN.CENTER, font='DM Sans')

    stmt = box(s,
        '"Connect AI is the data access layer your team would have built\n'
        'if you had 6 months and dedicated maintenance bandwidth."',
        ML, Emu(1080000), CW, Emu(2500000),
        size=38, bold=True, color=CDATA_DARK, wrap=True)

    pillars = box(s, 'CONNECTIVITY  ·  CONTEXT  ·  CONTROL',
        0, Emu(3680000), W, Emu(270000),
        size=13, bold=True, color=CDATA_DARK, align=PP_ALIGN.CENTER, font='DM Sans')

    shape(s, ML + Emu(3600000), Emu(4050000), CW - Emu(7200000), Emu(34000),
          fill=CDATA_DARK, rounded=False)

    sub_text = box(s,
        "The question isn't whether you can build it. It's whether that's what you want to be working on.",
        ML, Emu(4230000), CW, Emu(560000),
        size=18, color=RGBColor(0x33, 0x33, 0x33), align=PP_ALIGN.CENTER, wrap=True)

    add_appear_animations(s, [[stmt.shape_id], [pillars.shape_id, sub_text.shape_id]])
    set_notes(s, SCRIPTS[7])


def slide_08_trust(prs):
    """Two cards — what earns vs. destroys developer trust."""
    s = blank(prs)
    set_bg(s, CDATA_BG)
    add_cdata_logo(s, 'dark')
    overline(s, 'DEVELOPER TRUST')
    h1(s, "The quickstart either runs in 20 minutes or it doesn't.", size=28)
    sub(s, "That's the real evaluation. Everything else is downstream.")

    two_cards(s, [
        {
            'title': 'What earns trust',
            'body':  'Specific numbers with context.\n'
                     'Code that actually runs.\n'
                     'Honest about limitations and failure modes.\n'
                     'Error messages that tell you what actually went wrong.',
        },
        {
            'title': 'What destroys trust',
            'body':  '"Powerful." "Seamless." "Enterprise-grade."\n'
                     'Code samples with no error handling.\n'
                     "Docs that describe what an API does\nbut not what happens when it fails.",
        },
    ], top=CONT_S, card_h=Emu(2400000), animate=True)
    set_notes(s, SCRIPTS[8])


def slide_09_prior_impact(prs):
    """Yellow stat slide — prior results from CloudQuery (bridges Part 1 to Part 2)."""
    s = blank(prs)
    set_bg(s, CDATA_YELLOW)
    add_cdata_logo(s, 'yellow')

    box(s, 'PRIOR RESULTS', 0, Emu(380000), W, Emu(270000),
        size=11, bold=True, color=CDATA_DARK, align=PP_ALIGN.CENTER, font='DM Sans')
    box(s, 'CloudQuery  ·  8 weeks  ·  same methodology',
        0, Emu(640000), W, Emu(270000),
        size=13, color=RGBColor(0x33, 0x33, 0x33), align=PP_ALIGN.CENTER)

    stats = [
        ('+440%',   'docs traffic'),
        ('0→23/wk', 'quickstart completions'),
        ('4.9×',    'search impressions ATH'),
        ('+5.2',    'avg position (4 wks)'),
    ]

    n     = len(stats)
    bw    = Emu(2500000)
    gap   = (CW - n * bw) // (n - 1)
    num_y = Emu(1020000)
    lbl_y = Emu(1620000)

    groups = []
    for i, (num, label) in enumerate(stats):
        x  = ML + i * (bw + gap)
        sn = box(s, num, x, num_y, bw, Emu(640000),
                 size=44, bold=True, color=CDATA_DARK, align=PP_ALIGN.CENTER, wrap=False)
        lb = box(s, label, x, lbl_y, bw, Emu(310000),
                 size=11, color=RGBColor(0x33, 0x33, 0x33), align=PP_ALIGN.CENTER, wrap=False)
        groups.append([sn.shape_id, lb.shape_id])

    shape(s, ML + Emu(3400000), Emu(2040000), CW - Emu(6800000), Emu(28000),
          fill=CDATA_DARK, rounded=False)

    pipe = box(s, '19 organic MQLs  ·  1 confirmed $10K SQO — content first-touch attribution',
               ML, Emu(2160000), CW, Emu(320000),
               size=14, bold=True, color=CDATA_DARK, align=PP_ALIGN.CENTER, wrap=True)

    # Ahrefs performance chart
    _img_path = os.path.join(HERE, 'ahrefs-performance.png')
    _iw, _ih = 1474, 998  # px
    chart_h = Emu(3300000)
    chart_w = int(chart_h * _iw / _ih)
    chart_x = ML + (CW - chart_w) // 2
    chart_y = Emu(2640000)
    chart_pic = s.shapes.add_picture(_img_path, chart_x, chart_y, chart_w, chart_h)

    source_label(s,
        'Ahrefs  ·  cloudquery.io  ·  Jan 2022 – May 2026  ·  red box = start of engagement',
        top=Emu(6060000))

    add_appear_animations(s, groups + [[pipe.shape_id], [chart_pic.shape_id]])
    set_notes(s, SCRIPTS[9])


def slide_10_divider(prs):
    """Yellow section divider — Part 2."""
    s = blank(prs)
    set_bg(s, CDATA_YELLOW)
    add_cdata_logo(s, 'yellow')
    box(s, 'PART TWO', 0, Emu(2200000), W, Emu(310000),
        size=12, bold=True, color=CDATA_DARK, align=PP_ALIGN.CENTER, font='DM Sans')
    box(s, '90-Day GTM Plan', 0, Emu(2620000), W, Emu(1350000),
        size=52, bold=True, color=CDATA_DARK, align=PP_ALIGN.CENTER, wrap=True)
    box(s, 'DevRel earns developer trust. PMM turns it into pipeline. These are different jobs.',
        0, Emu(4050000), W, Emu(500000),
        size=20, color=CDATA_DARK, align=PP_ALIGN.CENTER, wrap=True)
    set_notes(s, SCRIPTS[10])


def slide_11_competitive(prs):
    """CData vs. Composio comparison table — rows appear on click."""
    s = blank(prs)
    set_bg(s, CDATA_BG)
    add_cdata_logo(s, 'dark')
    overline(s, 'COMPETITIVE CONTEXT')
    h1(s, "The competitor that matters isn't Fivetran.", size=38)

    rows = [
        ('Connectivity',        '350+  —  ERP, databases, SaaS, financial',   '500+  —  SaaS-heavy: Slack, Jira, GitHub'),
        ('Context — interface', 'SQL-queryable live data',                     'Action-based tool calls  —  no SQL'),
        ('Context — coverage',  'JDBC/ODBC, pandas, SQLAlchemy, BI tools',     '✗  Not supported'),
        ('Control',             'SAP, NetSuite, Workday, Oracle  +  SOC2',     'Weak enterprise depth'),
        ('Developer awareness', 'Low  —  absent from AEO responses',           'High  —  named "best overall" by Claude'),
    ]

    table_y = Emu(1780000)
    hdr_h   = Emu(420000)
    row_h   = Emu(470000)
    p       = Emu(160000)
    label_w = Emu(2300000)
    gap     = Emu(60000)
    val_w   = (CW - label_w - gap) // 2 - Emu(30000)

    # Yellow header row with dark text
    shape(s, ML, table_y, CW, hdr_h, fill=CDATA_YELLOW, rounded=False)
    box(s, 'FEATURE',
        ML + p, table_y + Emu(110000), label_w - p, Emu(210000),
        size=10, bold=True, color=CDATA_DARK, font='DM Sans')
    box(s, 'CDATA CONNECT AI',
        ML + label_w + gap, table_y + Emu(110000), val_w, Emu(210000),
        size=10, bold=True, color=CDATA_DARK, font='DM Sans')
    box(s, 'COMPOSIO',
        ML + label_w + gap + val_w + gap, table_y + Emu(110000), val_w, Emu(210000),
        size=10, bold=True, color=CDATA_DARK, font='DM Sans')

    groups = []
    for i, (label, cdata_val, composio_val) in enumerate(rows):
        ry   = table_y + hdr_h + i * row_h
        fill = CDATA_CARD if i % 2 == 0 else CDATA_BG
        bg   = shape(s, ML, ry, CW, row_h, fill=fill, rounded=False)
        div  = shape(s, ML, ry, CW, Emu(18000), fill=CDATA_DIVIDER, rounded=False)
        b1   = box(s, label,
                   ML + p, ry + Emu(110000), label_w - p, Emu(280000),
                   size=12, bold=True, color=CDATA_DARK)
        b2   = box(s, cdata_val,
                   ML + label_w + gap, ry + Emu(100000), val_w - Emu(60000), Emu(300000),
                   size=11, color=CDATA_MID, wrap=True)
        b3   = box(s, composio_val,
                   ML + label_w + gap + val_w + gap, ry + Emu(100000),
                   val_w - Emu(60000), Emu(300000),
                   size=11, color=CDATA_GRAY, wrap=True)
        groups.append([bg.shape_id, div.shape_id, b1.shape_id, b2.shape_id, b3.shape_id])

    add_appear_animations(s, groups)
    set_notes(s, SCRIPTS[11])


def slide_12_discoverability(prs):
    """Three-surface discoverability gap — Search, AI/AEO, Community."""
    s = blank(prs)
    set_bg(s, CDATA_YELLOW)
    add_cdata_logo(s, 'yellow')

    box(s, 'THE DISCOVERABILITY GAP', 0, Emu(580000), W, Emu(270000),
        size=11, bold=True, color=CDATA_DARK, align=PP_ALIGN.CENTER, font='DM Sans')

    big = box(s, 'CData is absent.\nAcross every channel developers use.',
              ML, Emu(1080000), CW, Emu(2000000),
              size=40, bold=True, color=CDATA_DARK, align=PP_ALIGN.CENTER, wrap=True)

    shape(s, ML + Emu(3700000), Emu(3200000), CW - Emu(7400000), Emu(34000),
          fill=CDATA_DARK, rounded=False)

    surfaces = [
        ('Search (SEO)',   'Not ranking for "Python DB-API Salesforce," "MCP server enterprise data," or any high-intent query.'),
        ('AI responses (AEO)', 'Claude, Perplexity, GPT-4o return Composio, Zapier, MuleSoft — CData absent from every test query.'),
        ('Community',      '~150K developers write Composio READMEs, Stack Overflow answers, GitHub repos. CData has almost none of this.'),
    ]
    detail_ids = []
    sy = Emu(3400000)
    for label, desc in surfaces:
        lbl = box(s, label.upper(), ML + Emu(100000), sy, Emu(2200000), Emu(270000),
                  size=11, bold=True, color=CDATA_DARK, font='DM Sans')
        dsc = box(s, desc, ML + Emu(2400000), sy, CW - Emu(2500000), Emu(270000),
                  size=12, color=RGBColor(0x22, 0x22, 0x22), wrap=True)
        detail_ids += [lbl.shape_id, dsc.shape_id]
        sy += Emu(380000)

    note = box(s,
        'Same fix for all three: ship specific, runnable, factual content where engineers actually look.',
        ML, Emu(4900000), CW, Emu(320000),
        size=13, bold=True, color=CDATA_DARK, align=PP_ALIGN.CENTER, wrap=True)

    add_appear_animations(s, [[big.shape_id], detail_ids + [note.shape_id]])
    source_label(s, 'Baseline run 2026-05-08  ·  Claude Sonnet 4.6  ·  All three surfaces re-audited quarterly',
                 top=Emu(6300000))
    set_notes(s, SCRIPTS[12])


def slide_13_days_1_30(prs):
    """Three cards — Days 1–30: audit already started, real findings, concurrent fix + collaboration."""
    s = blank(prs)
    set_bg(s, CDATA_BG)
    add_cdata_logo(s, 'dark')
    overline(s, 'DAYS 1–30')
    h1(s, 'Test the integration flows. Log what breaks. Fix it before prospects find it.', size=30)
    sub(s, 'Already started. Live artifact: dx-audit.md.')

    three_cards(s, [
        {
            'title': '01  Audit in progress',
            'body':  'Built with the product. Time-to-first-API-call: ~15 min ✅\n\n'
                     '· Positioning — website vs. what engineers need\n'
                     '· Content gaps — friction points = unanswered questions\n'
                     '· Discoverability — Search, AI, Community (May 8)',
        },
        {
            'title': '02  First session findings',
            'body':  '· Accept header bug: every copy-pasted example returns 406\n'
                     '· Misleading 401: says "token" failed — username is wrong\n'
                     '· Setup guide shows steps you already completed\n\n'
                     'Filed as Product roadmap input — not a slide deck.',
        },
        {
            'title': '03  Audit + fix concurrently',
            'body':  'High-severity fixes ship immediately — don\'t wait for day 30.\n\n'
                     '· Product + Eng: walk the journey live, cold\n'
                     '· Sales + CS: recurring objections = content gaps\n'
                     '· Leadership: developer + enterprise tracks named separately',
        },
    ], top=CONT_S, animate=True)
    set_notes(s, SCRIPTS[13])


def slide_14_content_strategy(prs):
    """Three cards — developer eval → bridge → enterprise buying journey."""
    s = blank(prs)
    set_bg(s, CDATA_BG)
    add_cdata_logo(s, 'dark')
    overline(s, 'CONTENT STRATEGY')
    box(s, 'Developers evaluate. Enterprises buy. Content has to serve both.',
        ML, TXT_T, CW, H1_H, size=34, bold=True, color=CDATA_DARK, wrap=True)

    three_cards(s, [
        {
            'title': 'Developer evaluation track',
            'body':  '"Does this work in under 20 minutes?"\n\n'
                     '· Quickstart guides + sample repos to clone and run\n'
                     '· Integration tutorials: MCP, DB-API, pandas, SQLAlchemy\n'
                     '· Auth reference: OAuth, API keys, SSO patterns\n'
                     '· Demo videos for YouTube and developer channels',
        },
        {
            'title': 'The bridge: technical decision-maker',
            'body':  '"Can I justify this to my org?"\n\n'
                     '· CData vs. Composio vs. DIY — honest, reproducible benchmarks\n'
                     '· Architecture doc: live queries vs. batch ELT for AI\n'
                     '· ROI case: managed vs. building + maintaining connectors\n'
                     'Technical enough for leads. Legible enough for executives.',
        },
        {
            'title': 'Enterprise buying track',
            'body':  '"Can we trust this at scale? Who else uses it?"\n\n'
                     '· Security + compliance: SOC2, high-volume, auth at scale\n'
                     '· Customer references: Anthropic, Databricks, Palantir, Microsoft\n'
                     '· Sales battlecard + code example for follow-ups\n'
                     'PMM owns this — Sales shouldn\'t have to build it.',
        },
    ], top=Emu(2500000), animate=True)
    set_notes(s, SCRIPTS[14])


def slide_15_days_31_60(prs):
    """Three cards — Days 31–60: messaging architecture and launch foundations."""
    s = blank(prs)
    set_bg(s, CDATA_BG)
    add_cdata_logo(s, 'dark')
    overline(s, 'DAYS 31–60')
    h1(s, 'Fix before you publish.', size=44)
    sub(s, 'Messaging architecture. Product launches. Website copy. Sales enablement.')

    three_cards(s, [
        {
            'title': '01  Messaging architecture',
            'body':  'Positioning brief: three audience segments, key messages per segment, '
                     'how the 3 Cs (Connectivity, Context, Control) translate to each persona. '
                     'Competitive differentiation one-pager: DIY vs. Composio vs. CData — '
                     'grounded in technical accuracy, built for Sales conversations.',
        },
        {
            'title': '02  Product launch GTM',
            'body':  'Developer Edition + Python SDK: launch together, same week — '
                     'complementary paths to the same data layer. '
                     'CLI: launch as beta with explicit GA criteria stated publicly. '
                     'Coordinate across Product, Engineering, Sales, and Marketing. '
                     'PMM owns launch copy, assets, and the Sales brief.',
        },
        {
            'title': '03  Website + Sales enablement',
            'body':  'Write the developer-facing pages directly — product pages, use case pages, '
                     'technical landing pages. PMM writes this copy; it doesn\'t get briefed out. '
                     'Sales battlecard: Composio comparison, MCP vs. SDK decision guide, '
                     'one working code example reps can paste into follow-up emails.',
        },
    ], top=CONT_S, animate=True)
    set_notes(s, SCRIPTS[15])


def slide_16_days_61_90(prs):
    """Three cards — Days 61–90: ship, measure, iterate."""
    s = blank(prs)
    set_bg(s, CDATA_BG)
    add_cdata_logo(s, 'dark')
    overline(s, 'DAYS 61–90')
    h1(s, 'Set the standard. Build the machine that scales it.', size=28)
    sub(s, 'First output sets the quality bar. The program runs after day 90.')

    three_cards(s, [
        {
            'title': '01  Content program infrastructure',
            'body':  'PMM writes: positioning, competitive, launch content.\n'
                     'DevRel writes: community, tutorials, hands-on code.\n\n'
                     'Content types: quickstarts, architecture docs, auth references, comparison pages, demo videos.\n'
                     'Distribution: blog, docs, GitHub, YouTube, developer channels.',
        },
        {
            'title': '02  First output: benchmark pieces',
            'body':  '"CData vs. Composio: when SQL beats action-based tools" — sets the competitive content bar.\n'
                     'MCP quickstart video + written guide — sets the tutorial bar.\n'
                     '"Building vs. buying data connectivity for AI agents" — the ROI case with reproducible numbers.\n'
                     'Three pieces. One per content type. Each one a template for what follows.',
        },
        {
            'title': '03  Day 90 deliverable',
            'body':  'A content program, not a content list: editorial calendar, '
                     'content types, distribution channels, ownership map, and attribution model — all running.\n'
                     'Evidence-first review: what shipped, what moved, what we\'d do differently.',
        },
    ], top=CONT_S, animate=True)
    set_notes(s, SCRIPTS[16])


def slide_17_goals(prs):
    """Stacked metric rows — goals framework."""
    s = blank(prs)
    set_bg(s, CDATA_BG)
    add_cdata_logo(s, 'dark')
    overline(s, 'GOALS FRAMEWORK')
    box(s, 'Developer adoption converts to pipeline. Here\'s how we measure both.',
        ML, TXT_T, CW, H1_H, size=30, bold=True, color=CDATA_DARK, wrap=True)

    metrics = [
        ('Developer → pipeline attribution',
         'UTM + first-touch from day 1  ·  baseline by day 30',
         'Proves PMM contributes to revenue — miss the first 30 days, lose the attribution forever'),
        ('Developer discoverability rank',
         'Top 3 for 3–5 key queries by Q3 (SEO + AEO)',
         'Discoverability gap is closing across Search and AI channels'),
        ('Developer activation rate',
         'Funnel baseline → 20% improvement by Q3',
         'Evaluation journey is working'),
        ('Time-to-first-API-call',
         'Under 15 min vs. Composio benchmark',
         'DX is competitive'),
        ('Competitive win rate vs. Composio',
         'Track in CRM from day 60',
         'Messaging is landing in engineering conversations'),
    ]

    card_h = Emu(690000)
    card_y = Emu(1650000)
    gap    = Emu(55000)
    p      = Emu(160000)
    met_w  = Emu(2800000)
    tgt_w  = Emu(3400000)
    why_w  = CW - met_w - tgt_w

    groups = []
    for i, (metric, target, why) in enumerate(metrics):
        cy = card_y + i * (card_h + gap)
        bg = shape(s, ML, cy, CW, card_h, fill=CDATA_CARD)
        # Yellow left accent bar on each row
        bar = shape(s, ML, cy, Emu(45000), card_h, fill=CDATA_YELLOW, rounded=False)
        b1  = box(s, metric,
                  ML + p, cy + Emu(200000), met_w - 2 * p, Emu(300000),
                  size=12, bold=True, color=CDATA_DARK)
        b2  = box(s, target,
                  ML + met_w, cy + Emu(200000), tgt_w - Emu(80000), Emu(300000),
                  size=12, color=CDATA_DARK, wrap=True)
        b3  = box(s, why,
                  ML + met_w + tgt_w, cy + Emu(200000), why_w - Emu(80000), Emu(300000),
                  size=11, color=CDATA_GRAY, wrap=True)
        groups.append([bg.shape_id, bar.shape_id, b1.shape_id, b2.shape_id, b3.shape_id])

    add_appear_animations(s, groups)
    set_notes(s, SCRIPTS[17])


def slide_18_close(prs):
    """Closing — three artifacts + QR code for the repo."""
    s = blank(prs)
    set_bg(s, RGBColor(0xFF, 0xFF, 0xFF))
    shape(s, LP_L, LP_T, LP_W, LP_H, fill=CDATA_YELLOW, rounded=False)
    add_cdata_logo(s, 'dark')

    box(s, 'THE ARTIFACTS', ML, Emu(580000), TXT_W, Emu(270000),
        size=11, bold=True, color=CDATA_DARK, font='DM Sans')
    box(s, 'Built this week. Ready to use on day one.', ML, Emu(900000), TXT_W, Emu(1100000),
        size=36, bold=True, color=CDATA_DARK, wrap=True)

    artifacts = [
        '✓  Working demo — Claude agent querying enterprise data through CData MCP',
        '✓  DX audit — 6 friction points, root causes, and recommended fixes',
        '✓  Discoverability baseline — Search, AI, and Community channels documented',
    ]
    ay = Emu(2150000)
    for a in artifacts:
        box(s, a, ML, ay, TXT_W, Emu(310000), size=14, color=CDATA_DARK, wrap=False)
        ay += Emu(360000)

    shape(s, ML, Emu(3300000), Emu(4800000), Emu(34000), fill=CDATA_DIVIDER, rounded=False)

    box(s, "That's what I'd share on day 30 — not a strategy deck. Data.\nThe goal is qualified pipeline Sales can close.",
        ML, Emu(3460000), TXT_W, Emu(650000),
        size=16, color=CDATA_DARK, wrap=True)

    # GitHub URL + QR code
    qr_size = Emu(1250000)
    qr_x    = ML + Emu(2800000)
    qr_y    = Emu(4350000)
    s.shapes.add_picture(_REPO_QR, qr_x, qr_y, qr_size, qr_size)
    box(s, 'Scan for repo', qr_x, qr_y + qr_size + Emu(60000), qr_size, Emu(220000),
        size=10, color=CDATA_GRAY, align=PP_ALIGN.CENTER)

    box(s, 'github.com/JoeKarlsson/connect-ai-agent-demo',
        ML, Emu(4400000), Emu(2650000), Emu(330000),
        size=12, color=CDATA_DARK,
        url='https://github.com/JoeKarlsson/connect-ai-agent-demo')

    mbox(s, [{'runs': [
        {'text': TALK['linkedin'].replace('https://www.', '').replace('https://', ''),
         'size': 12, 'color': CDATA_DARK, 'url': TALK['linkedin']},
    ]}], ML, Emu(4820000), Emu(2650000), Emu(330000))

    box(s, TALK['company'], ML, Emu(5240000), Emu(2650000), Emu(330000),
        size=12, color=CDATA_DARK, url='https://joekarlsson.com')

    set_notes(s, SCRIPTS[18])


def slide_19_qa(prs):
    """Q&A holding slide — stays on screen during questions."""
    s = blank(prs)
    set_bg(s, CDATA_YELLOW)
    add_cdata_logo(s, 'yellow')
    box(s, 'Q & A', 0, Emu(2300000), W, Emu(1400000),
        size=80, bold=True, color=CDATA_DARK, align=PP_ALIGN.CENTER)
    box(s, 'github.com/JoeKarlsson/connect-ai-agent-demo',
        0, Emu(4000000), W, Emu(380000),
        size=16, color=CDATA_DARK, align=PP_ALIGN.CENTER,
        url='https://github.com/JoeKarlsson/connect-ai-agent-demo')
    set_notes(s, SCRIPTS[19])


def slide_20_thankyou(prs):
    """Thank you — final slide."""
    s = blank(prs)
    set_bg(s, RGBColor(0xFF, 0xFF, 0xFF))
    shape(s, LP_L, LP_T, LP_W, LP_H, fill=CDATA_YELLOW, rounded=False)
    add_cdata_logo(s, 'dark')
    box(s, 'Thank you.', ML, Emu(2100000), TXT_W, Emu(1000000),
        size=64, bold=True, color=CDATA_DARK)
    box(s, TALK['speaker'], ML, Emu(3350000), TXT_W, Emu(370000),
        size=18, bold=True, color=CDATA_DARK)
    mbox(s, [{'runs': [
        {'text': TALK['linkedin'].replace('https://www.', '').replace('https://', ''),
         'size': 14, 'color': CDATA_DARK, 'url': TALK['linkedin']},
    ]}], ML, Emu(3820000), TXT_W, Emu(350000))
    box(s, TALK['company'], ML, Emu(4220000), TXT_W, Emu(350000),
        size=14, color=CDATA_DARK, url='https://joekarlsson.com')
    box(s, 'github.com/JoeKarlsson/connect-ai-agent-demo',
        ML, Emu(4620000), TXT_W, Emu(350000),
        size=14, color=CDATA_DARK,
        url='https://github.com/JoeKarlsson/connect-ai-agent-demo')
    set_notes(s, SCRIPTS[20])


# ── Keynote notes injection ────────────────────────────────────────────────────

def inject_keynote_notes(doc_name_fragment='cdata-interview'):
    """Inject SCRIPTS into the open Keynote document via AppleScript.

    postprocess_pptx() strips all notesSlide XML (required to prevent Keynote
    Code=2 errors on slides with hyperlinks). This re-injects the SCRIPTS dict
    directly into the live Keynote document after the PPTX has been imported.

    Usage:
        1. Open cdata-interview.pptx in Keynote
        2. python build_slides.py --inject-notes
    """
    import subprocess
    lines = ['tell application "Keynote"']
    lines.append('    set targetDoc to missing value')
    lines.append('    repeat with d in documents')
    lines.append(f'        if name of d contains "{doc_name_fragment}" then')
    lines.append('            set targetDoc to d')
    lines.append('            exit repeat')
    lines.append('        end if')
    lines.append('    end repeat')
    lines.append('    if targetDoc is missing value then')
    lines.append(f'        error "Could not find Keynote document containing \\"{doc_name_fragment}\\""')
    lines.append('    end if')
    for slide_num, script_text in SCRIPTS.items():
        escaped = script_text.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
        lines.append(f'    set presenter notes of slide {slide_num} of targetDoc to "{escaped}"')
    lines.append('end tell')
    result = subprocess.run(['osascript', '-e', '\n'.join(lines)], capture_output=True, text=True)
    if result.returncode != 0:
        print(f'  [notes] AppleScript error: {result.stderr.strip()}')
        print('  [notes] Make sure cdata-interview.pptx is already open in Keynote before running --inject-notes')
    else:
        print(f'  [notes] Injected notes for {len(SCRIPTS)} slides into Keynote.')


# ── Build ──────────────────────────────────────────────────────────────────────

def build(inject_notes=False):
    check_fonts()
    prs = new_prs()

    slide_01_title(prs)
    slide_02_live_demo(prs)
    slide_03_demo_result(prs)
    slide_04_architecture(prs)
    slide_05_two_paths(prs)
    slide_06_problem(prs)
    slide_07_positioning(prs)
    slide_08_trust(prs)
    slide_09_prior_impact(prs)
    slide_10_divider(prs)
    slide_11_competitive(prs)
    slide_12_discoverability(prs)
    slide_13_days_1_30(prs)
    slide_14_content_strategy(prs)
    slide_15_days_31_60(prs)
    slide_16_days_61_90(prs)
    slide_17_goals(prs)
    slide_18_close(prs)
    slide_19_qa(prs)
    slide_20_thankyou(prs)

    out = os.path.join(HERE, 'cdata-interview.pptx')
    prs.save(out)
    postprocess_pptx(out)
    print(f'Saved {len(prs.slides)} slides → {out}')

    if inject_notes:
        inject_keynote_notes()

    return out


if __name__ == '__main__':
    inject = '--inject-notes' in sys.argv
    build(inject_notes=inject)
