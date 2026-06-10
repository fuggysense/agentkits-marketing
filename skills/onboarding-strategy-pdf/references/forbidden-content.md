# Forbidden Content — Onboarding Strategy Report PDF

Derived from Hormozi AI consultation (see plan file at `~/.claude/plans/zany-sprouting-prism.md` → Consultation Log → Q1 and Q2). This is an explicit blacklist of what MUST NEVER appear in the PDF. The orchestrator enforces this when compiling the input JSON; the script does not parse for banned terms.

---

## Never include

### Agency self-promotion
- **Founder stories** — "I started this agency after…"
- **Agency mission / vision / values** — "Our mission is to…"
- **Agency history or timeline** — "Since 2020 we've helped…"
- **Team bios** — client cares about their problem, not our origin story
- **Awards, press mentions, logo carousels** — zero buyer relevance pre-engagement

### Technical jargon without explanation
- CTR, ROAS, CPL, CAC, LTV used as acronyms without expansion
- "Dynamic creative testing" without a plain-language gloss
- "Lookalike audiences", "CAPI", "pixel events" — explain or metaphor
- Platform-specific slang ("CBO", "ABO", "Advantage+") — say what they mean
- **Rule:** if a non-marketer friend wouldn't understand it, rewrite or remove

### Generic templates
- Any sentence that could be copy-pasted between 10 different clients
- "We'll analyze your audience" — say WHICH audience, WHICH analysis
- "Implement best practices" — name the practice, explain why it's right for them
- Persona archetypes not drawn from the client's actual avatars
- **Rule:** if it reads the same for NeezaNizam and a US SaaS company, it's too generic

### Vague outcomes
- "Results guaranteed"
- "We'll grow your business"
- "Scale to the moon"
- "Transform your marketing"
- "Unlock your potential"
- "Drive meaningful results"
- **Rule:** Hormozi — "amorphous outcomes have banner blindness and carry zero weight"

### Unsubstantiated promises
- "We'll 10x your revenue" (unless it's the verified standard average)
- "You'll see results in X days" as a guarantee (say: "on average, clients see X by day Y, half see it faster, half see it slower")
- Specific dollar-amount outcomes you can't back with past data
- **Rule:** Hormozi — never promise an outcome that requires the client to act ("you will lose 20 lbs") if you can't "eat the food for them"

### Procedural content (the HOW)
This is the critical reveal/withhold rule from Hormozi Q2:

**NEVER in the PDF:**
- Finished headlines (e.g., "Stop paying riba — here's the Shariah way to upgrade")
- Finished ad copy (primary text, descriptions, CTAs)
- Landing page copy
- Landing page layouts or wireframes
- Automation trigger logic ("when contact does X, send Y")
- Email sequence content (subject lines, body copy)
- Ad platform SOPs ("go to Ads Manager → Create → Objective → Sales → …")
- Specific ad set targeting parameters
- Specific budget allocation numbers per campaign
- Actual conversion tracking code snippets

**YES in the PDF:**
- The **mechanism name** ("Sophistication-Matched DCT Method")
- The **angle themes** ("Islamic-financing-friendly angle", "3-number diagnostic mechanism")
- **Positioning** and **differentiation wedge** statements
- **Phase structure** (Activation → Value → Lock-In)
- **What the client will receive** (Black Book list)

**Rule:** Reveal the WHAT. Withhold the HOW. The withheld content IS the engagement.

### Noise metrics
- Metrics that don't map to getting more customers, making them worth more, or increasing enterprise value
- Vanity numbers (impressions, reach, engagement rate without conversion context)
- Industry benchmarks that don't change what the client should do next
- **Rule:** Hormozi behavioral test — "if a change in the metric wouldn't change the client's action, it's noise"

### Complexity for its own sake
- Explanations that require 3+ sentences to understand a basic concept
- Decision trees with more than 3 branches
- Flow diagrams with more than 7 nodes
- **Rule:** "If the value of something isn't immediately obvious, delete it or replace it with a metaphor"

---

## Spot-check before every delivery

Before running `generate_pdf.py`, orchestrator should grep the input JSON for:

```
mission
vision
founded
founder
guaranteed
guarantee
10x
2x your
scale to
transform your
unlock
drive results
meaningful results
proven strategies
best practices
industry-leading
cutting-edge
world-class
```

**Any match → investigate and remove or rewrite.** These terms are banner-blind; the client's eyes will glaze past them.

**Additional grep for procedural leakage** — check `angle_themes_per_avatar` and `strategy_preview.angle_themes` for:
- Any sentence ending in a period that reads like finished copy (e.g., "Stop X. Start Y.")
- Any quoted string in the JSON that looks like a headline
- CTA-like phrases ("Click here", "Sign up now", "Learn more")

If you find them, downgrade to theme form ("Start/stop headline style targeting pain point X").

---

## If in doubt

Ask yourself Hormozi's behavioral test: **"If this sentence were removed, would the client take a different action at the onboarding call?"**

- No → delete it
- Yes → keep it

The PDF is a decision-driving document. Everything in it must drive the decision to sign the engagement. Everything that doesn't is noise.
