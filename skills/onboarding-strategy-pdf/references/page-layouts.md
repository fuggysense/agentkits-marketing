# Page Layouts — Onboarding Strategy Report PDF

Per-page content rules + scoring rubric per dimension. Read by the skill orchestrator when compiling the input JSON.

---

## Page 1 — Cover (Dream Translation + Primary Constraint + Calculator Close)

**What renders:**
- Title: "Onboarding Strategy Report"
- Client name (accent color)
- Report date + prepared-by line
- **Dream Translation** — client's exact words from discovery, rendered as italic quote block
- **Primary Constraint callout** — large bordered box with:
  - "THE ONE CONSTRAINT" label
  - Dimension name (bold, dark)
  - Monthly cost (orange, large)
  - "Annual Ignorance Tax: $X"
  - Closing italic: "This is what it costs to not solve this one thing."
- **Rationale line** — one sentence explaining why this is the primary constraint

**What NEVER renders on this page:**
- Composite 0–100 score
- Letter grade (A+ → F)
- Founder story, agency mission, logo carousel
- Technical jargon without explanation

## Page 2 — Diagnostic Dashboard (1–5 RYG)

**What renders:**
- Heading: "Diagnostic: Where You Stand"
- Intro paragraph: "We scored five dimensions... One dimension is flagged as The Primary Constraint..."
- **RYG diagnostic table** (4 columns):
  - Dimension (bold name)
  - Score (1–5 format "3 / 5")
  - Band (Strong / Needs Work / Critical) — colored per band
  - Prescribed Action (one line)
- Primary constraint row is highlighted with gold background + bold border
- **Calculator Close** narrative block — explains the dollar math in plain language

**Scoring rubric per dimension (applied by orchestrator):**

### Audience Clarity (vertical-agnostic)
- **5** — Avatars + sophistication audit + negative audiences all present, verified against external research
- **4** — Avatars + sophistication audit present, negatives pending
- **3** — Avatars only, no sophistication audit
- **2** — ICP document only, no structured avatars
- **1** — Nothing beyond a vague target audience description

### Creative Direction (benchmark-driven)
- **5** — Sophistication-matched creative currently running at or above vertical benchmark CTR
- **4** — Creative aligned with sophistication level, performance TBD
- **3** — Generic creative performing near vertical benchmark average
- **2** — Generic creative performing materially below benchmark
- **1** — No creative yet, or creative severely below benchmark (>50% gap)

### Funnel Architecture (vertical-agnostic)
- **5** — Landing page + lead-capture form + CRM sync + email follow-up sequence all wired
- **4** — Landing page + lead capture wired, CRM or email pending
- **3** — Landing page exists but no lead capture or CRM integration
- **2** — Landing page only (link in bio, no conversion path)
- **1** — No landing page

### Competitive Position (vertical-agnostic)
- **5** — Differentiation wedge identified + blue ocean angle confirmed in swipe file
- **4** — Differentiation wedge identified, blue ocean TBD
- **3** — Standard positioning, no clear wedge
- **2** — Commodity positioning, same as 10+ competitors
- **1** — No positioning work done

### Budget Readiness (benchmark-driven)
- **5** — Budget ≥ vertical floor + 70/20/10 split (proven/scaling/testing) planned
- **4** — Budget ≥ vertical floor, split TBD
- **3** — Budget at 50–100% of vertical floor
- **2** — Budget at 25–50% of vertical floor
- **1** — Budget <25% of vertical floor OR no stated budget

### Primary Constraint Selection Rule
Pick the dimension where a score improvement has the **highest leverage** on the client's dream outcome. Not necessarily the lowest-scoring dimension — sometimes a 3 in Creative Direction is a bigger lever than a 2 in Funnel Architecture if the dream outcome is scaling ads.

**Tiebreaker:** If two dimensions tie, pick the one where the client has the most resources already (existing budget, existing audience) — making it easier to solve fast.

### Calculator Close Math
```
monthly_cost_of_constraint = current_monthly_spend × (benchmark_metric / current_metric - 1) × net_margin
annual_ignorance_tax = monthly_cost_of_constraint × 12
```

Benchmark metric comes from `benchmarks-registry.md`. If no current metric is known, use `benchmarks-registry.yaml → default` and flag the Calculator Close as "estimated".

## Page 3 — Avatar Deep-Dive

**What renders:**
- Heading: "Who We're Actually Talking To"
- Intro paragraph
- For each avatar (up to 3 per page):
  - Name (subheading)
  - Awareness/Sophistication chip (inline)
  - **Top pains** (bullet list)
  - **Buying trigger** (one line)
  - **Angle themes we'll test** — arrow list, declarative only

**Critical rule:** `angle_themes` must be **themes** ("Islamic-financing-friendly angle", "Named-couple testimonial"), NOT finished copy ("Stop paying riba — here's the Shariah way to upgrade"). Finished copy is the engagement, not the PDF.

## Page 4 — Strategic Positioning + Mechanism

**What renders:**
- Heading: "Strategic Positioning"
- **Mechanism name** (bold, dark)
- **Positioning angle** (one paragraph)
- **Differentiation wedge** (one paragraph)
- **Angle themes per avatar** (reiterated)
- Explicit footer in gray italic: "Execution specifics — finished headlines, ad copy, landing pages, and automation logic — are delivered as part of the engagement. This page shows the what; the how is the work itself."

## Page 5 — Existing Ads Audit (conditional)

**Skipped entirely if** `existing_ads_audit.enabled == false`.

**What renders when enabled:**
- Heading: "Your Current Ads: What We Found"
- **Zero Blame header** in blue italic: "Nothing that happened before today is anyone's fault. This page exists so we can solve the problem together."
- For each finding:
  - Finding statement (bold)
  - **Acknowledge:** past logic validated ("It was reasonable to target broad interests given your starting data")
  - **Associate:** peer success link ("Sarah had this exact issue before...")
  - **Ask:** pivot to solution ("Can I show you what changed for her?")
  - **Skill-deficiency reframe** in accent-color italic ("Meta works — the gap is a learnable skill in X")
  - **Monthly cost of this gap** in orange bold
- **Total monthly spend at risk** at bottom of page

**Critical rule:** Never write findings as "you did X wrong". Always: "we noticed X is happening, here's why it's costing money, here's how we fix it."

## Page 6 — Plus/Minus Potential Map

**What renders:**
- Heading: "The Two Paths Forward"
- Intro: "Two futures. The choice is yours."
- **Two-column table:**
  - Left column (green-tinted bg): "Work With Us" — subtitle, then "More of:" list + "Less of:" list
  - Right column (red-tinted bg): "Stay Current Path" — subtitle, then "More of:" list + "Less of:" list

**Data source:** `more` items come from dream outcome translations; `less` items come from avatar pains. Mirror the same themes — if "family time" is a dream, "family evenings lost to cold viewings" is the pain on the opposite side.

## Page 7 — 90-Day Roadmap (Activation / Value / Lock-In)

**What renders:**
- Heading: "Your Next 90 Days"
- Expectation anchor line in italic ("On average, X happens in Y time. Half achieve more, half achieve less.")
- **3-phase table:**
  - Phase (Activation / Value / Lock-In) + day range
  - Focus (one sentence)
  - What You'll See (bullet list — micro-promises, activation points, deliverables, quick wins)
- **Next Meeting section:**
  - "Next meeting booked for: _______________" (fillable at the call)
  - Purpose line in small gray italic

**Phase content rules:**

### Activation (Days 1–30)
- 4–6 **micro-promises** delivered in first 48h (Hormozi: combat buyer's remorse early)
- 2–3 **activation points** — actions successful clients always take
- Concrete deliverables (DCT tracker draft, Meta campaign paused, etc.)

### Value (Days 31–60)
- ONE specific **quick win target** — measurable, leading indicator
- **Monthly value reminder** — documented wins sent to client
- Iteration deliverables

### Lock-In (Days 61–90)
- **Documented wins** — quantified, comparable to Day 1 baseline
- **QBR deck** or equivalent
- Next-quarter scope proposal

**Expectation-setting language rules (from Hormozi consultation):**
- Sell cold: anchor to bottom-25% of past results
- "Half our clients achieve more, half achieve less"
- Timelines only for **controllable actions** ("Ads go live in 48h"), NEVER for outcomes
- Never promise specific dollar amounts unless you have the data to prove it's the standard
- Never use "guaranteed" in any form

## Page 8 — Black Book Appendix

**What renders:**
- Heading: "What You'll Receive In Your First Week"
- Intro: "These assets are yours as part of the engagement. Many of them would cost thousands of dollars or hundreds of hours to build from scratch."
- **Table:**
  - Asset name
  - Perceived Value ($X,XXX)
- Bottom row highlighted with gold background: "Total perceived value: $X,XXX"

**Only rendered if** `black_book_handoff.assets_included` is non-empty.

**Companion folder:** Generator does NOT copy the actual asset files — the orchestrator creates `clients/<project>/deliverables/black-book-YYMMDD/` with copies or symlinks before or after the PDF run.

---

## Cross-page consistency rules

- All dollar figures formatted as `$X,XXX` (thousands separator, no cents)
- All colors use the palette in `pdf_helpers.COLORS`
- Band colors: red for critical, amber for yellow/warn, green for strong
- Primary constraint always highlighted with gold (`constraint_bg`) + bold
- No hardcoded client-specific strings in the Python script — all content flows from the input JSON

## Forbidden content

See `references/forbidden-content.md` for the full blacklist (Hormozi-derived). Summary:
- No founder stories, agency mission, vision
- No technical jargon without explanation
- No generic templates
- No vague outcomes or unsubstantiated promises
- No procedural content (finished copy, scripts, SOPs)
- No data that doesn't change client action
