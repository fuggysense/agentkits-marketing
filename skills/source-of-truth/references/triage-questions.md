# Triage Questions — Phase 1 Foundation Intake

Used in Mode B (URL) and Mode C (description/idea) ONLY. In Mode A (existing project), skip this phase entirely.

**Rule: ask only what research CANNOT determine.** Everything the parallel research pipeline can discover — buyer psychology, pain points, objections, competitor angles, awareness levels — should NOT appear in this question list.

**Delivery:** single batched AskUserQuestion call with 5-7 questions. Minimum user time: 3 minutes.

---

## Question Bank

### Q0 — Product Type (ALWAYS asked first — drives all downstream branching)

**Header:** `Product type`
**Single-select with Other:**
- E-commerce (physical product, online checkout)
- SaaS (software, recurring subscription)
- Service (local / professional — appointments, consultations, in-person)
- Info product (course, coaching, community, info-as-a-product)
- Marketing/B2B agency (done-for-you services to other businesses)
- Property / real-estate (consulting, agent services, property tech)

**Why asked:** drives the product-type branching matrix in `section-synthesis-frameworks.md` — affects KPI defaults (§2), proof types (§8), CTA grammar (§15), format weighting (§12), urgency triggers (§3), angle-pool defaults (§10). Without this, synthesis defaults to property/service patterns and breaks for ecom/SaaS/info.

**Cascade rule:** Q0 answer pre-fills the recommended option for Q1 (Conversion Goal). Examples: ecom → "Purchase" pre-recommended; SaaS → "Trial / signup" pre-recommended; service/property/agency → "Lead / application" pre-recommended; info → "Purchase" or "Trial" depending on offer structure.

### Q1 — Primary Conversion Goal (always asked)

**Header:** `Conversion goal`
**Single-select, 4 options:**
- Purchase (buy the product / subscribe)
- Lead / application (book call, fill form, apply)
- Trial / signup (free trial, sandbox, free tier)
- Other (custom answer)

**Why asked:** determines §2 Primary KPI draft candidates. E-commerce → ROAS/MER; lead gen → CPA/CPL; SaaS → CAC payback.

### Q2 — Target Market Segment (always asked)

**Header:** `Target market`
**Single-select with Other, example options (customise per category):**
- Consumers (B2C, end-user)
- SMB / small business owners
- Mid-market operators
- Enterprise / decision-makers
- Mixed — we serve multiple segments

**Why asked:** research can surface who's TALKING about the category, but the brand's INTENDED target may be a subset. Sharpens buyer-language-researcher prompt targeting.

### Q3 — Price Point / AOV (almost always asked — skip in Mode B only if pricing page scraped cleanly)

**Header:** `Price`
**Single-select with Other:**
- Under $50 (impulse / low-friction)
- $50-200 (considered purchase)
- $200-1K (high-consideration)
- $1K-10K (major decision)
- $10K+ (enterprise / investment-grade)
- Free / freemium with upsell

**Why asked:** sophistication strategy shifts with price. Sub-$50 wants speed of comprehension; $1K+ wants proof density + objection handling.

### Q4 — Current Ad State (always asked)

**Header:** `Ad state`
**Single-select, 4 options:**
- No paid ads yet — this is the first launch
- Running paid ads, scaling what works
- Ran paid ads before, paused/killed — need restart
- Running but performance has plateaued — need refresh

**Why asked:** determines whether Section 18 (Performance Feedback Loop) is pre-populated from paid-media-audit data, whether Section 16 recommends aggressive testing variables, whether Section 8 can pull existing creative-performance proof.

### Q5 — Brand / Compliance Constraints (almost always asked)

**Header:** `Constraints`
**Multi-select, 4 options:**
- Regulated industry (finance, health, legal, cannabis, gambling, political) — compliance guardrails apply
- Religious / cultural sensitivity required (halal, kosher, religious identity)
- Platform policy risk (claims we can't make on Meta/Google)
- No specific constraints

**Why asked:** filters angle/hook generation in §10-11. SG Malay-Muslim audiences need Shariah compliance flagged (routes to `skills/ad-concept-engine/references/sg-cultural-guidelines.md`).

### Q6 — Primary Platform Focus (Mode C only)

**Header:** `Platform`
**Multi-select, 4 options:**
- Meta (Facebook + Instagram) — priority
- Google (Search + YouTube) — priority
- TikTok — priority
- LinkedIn — priority

**Why asked:** format recommendations in §12 are platform-specific. VSL on YouTube, static on Meta, UGC on TikTok, expert on LinkedIn.

### Q7 — Brand Assets That Already Exist (Mode C only, optional)

**Header:** `Assets`
**Multi-select, 4 options:**
- Founder / subject-matter-expert who can be on camera
- Customer testimonials / UGC (raw footage or screenshots)
- Product demo footage / screen recordings
- None of the above — starting with no assets

**Why asked:** §14 visual guidance and §19 asset request checklist adjust based on what already exists. Also influences format prioritisation in §12 (can we make founder videos? UGC-style?).

---

## Question Selection Logic

**Mode B (URL provided):**
- Always ask: Q0, Q1, Q4
- Conditionally ask: Q2 (if product page doesn't specify target), Q3 (if pricing page missing/unclear), Q5 (always ask — hard to scrape)
- Usually skip: Q6, Q7 (infer from brand context)

**Mode C (description/idea only):**
- Ask all 8 (Q0 + Q1-Q7)

**Mode A (existing project):**
- Skip Q1-Q7 if `clients/<project>/context-profile.json` is populated.
- Q0 (product_type) MUST be confirmed — if not in context-profile.json, ask once. Add to context-profile.json after answer.

---

## AskUserQuestion Payload Construction

Build the payload as a single call with all selected questions. Example for Mode C:

```json
{
  "questions": [
    {
      "question": "What's the primary conversion goal for this campaign?",
      "header": "Conversion goal",
      "multiSelect": false,
      "options": [
        {"label": "Purchase", "description": "Direct sale — e-commerce, subscription, one-time buy"},
        {"label": "Lead / application (Recommended)", "description": "Book a call, fill a form, apply. Most common for services and high-consideration offers."},
        {"label": "Trial / signup", "description": "Free trial, freemium signup, sandbox access"},
        {"label": "Other conversion event", "description": "Custom answer"}
      ]
    },
    ...
  ]
}
```

**Rules for payload:**
- 5-7 questions max per batched call
- Recommended option listed first with "(Recommended)" label where a sensible default exists
- Every question has a clear "why this matters" in the label description (not in the question text)
- Use "Other" as the final option only when user custom input is genuinely likely (not forced)

---

## Fail-Safe: When User Answers Are Thin

If the user provides "I don't know" or skip for 3+ questions, DO NOT proceed with degraded research. Instead:
- Surface the gap: "Without target market and price point, the source-of-truth synthesis will produce generic output. Recommend you either: (a) fill these in now, or (b) run `/project:profile` first to build a proper context-profile.json."
- Stop. Don't burn research tokens on a foundation that's too thin.

## Output

Save all Phase 1 answers to `clients/<project>/source-of-truth-intake.json` for traceability. Research pipeline reads this file to customise sub-agent prompts.

```json
{
  "mode": "B",
  "intake_date": "2026-04-17",
  "answers": {
    "product_type": "agency",
    "conversion_goal": "Lead / application",
    "target_market": "SMB / small business owners",
    "price_point": "$200-1K",
    "ad_state": "Running but performance has plateaued",
    "constraints": ["Platform policy risk"],
    "platform_focus": ["Meta", "Google"],
    "existing_assets": ["Customer testimonials / UGC"]
  },
  "notes": "User flagged that the previous agency's creative felt generic and didn't match their actual buyer."
}
```
