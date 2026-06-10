---
name: business-profile
version: "2.0.0"
brand: Fuggy's Media
category: core
difficulty: beginner
description: "Fuggy's Media intake: 6 sections, ~21 questions + custom deep-dives. Outputs JSON context profile. Ad-optimized: big promise, objections, pain points, 90-day goals. Foundation for all downstream skills. Triggers: business profile, context profile, client intake, onboarding form."
triggers:
  - business profile
  - context profile
  - project profile
  - build profile
  - onboard business
  - onboarding form
  - client intake
  - fuggy's onboarding
  - 30 questions
prerequisites: []
related_skills:
  - client-onboarding
  - onboarding-strategy-pdf
  - avatar-research
  - ad-concept-engine
  - copywriting
agents: []
mcp_integrations:
  optional: []
success_metrics:
  - fields_completed
  - json_validity
output_schema: context-profile
---

## Graph Links
- **Feeds into:** [[onboarding-strategy-pdf]], [[avatar-research]], [[client-onboarding]], [[offer-builder]], [[copywriting]], [[ad-concept-engine]], [[campaign-runner]]
- **Draws from:** (independent — interview flow)
- **Related:** [[persona-builder]]

# Fuggy's Media Client Onboarding Questionnaire

You walk a paid client through Fuggy's Media's intake form and compile their answers into a structured JSON profile at `clients/<project>/context-profile.json`. This profile is the foundation layer — every downstream skill (onboarding-strategy-pdf, avatar-research, ad-concept-engine, copywriting) reads it to understand WHO this client is before producing anything.

## Context

**Schema v2.0 (updated 2026-04-11):** Replaces the previous generic 30-question business-identity interview with Fuggy's Media's actual 6-section intake form. The new form is **ad-optimized** — it gathers the psychological ammunition needed for paid media work: big promise, objections, unique value prop, daily troubles, the ONE pain point, 90-day goals.

This intake is designed to be handed to a paid client AFTER they've committed to the onboarding fee, BEFORE the paid onboarding call. The answers then become the input for `onboarding-strategy-pdf` which produces the PDF Jerel presents at that call.

## Core Philosophy

Without context, AI gives generic answers. With it, every downstream agent says: "Given that this client sells [X] to [audience] with the big promise of [Y] and their top objection is [Z], here's what I'd do next."

**Principles:**
- Ask in sections, one section per AskUserQuestion — never dump all ~21 questions at once
- Accept partial answers — mark unknowns as `null` or `""` in JSON, never invent content
- Works for new projects (create) AND existing projects (update)
- Output is ONLY the JSON file — no extra markdown commentary
- Section 3 has an OPERATOR DEEP-DIVE SLOT — customize 1-2 questions per client based on business type

---

## Mode Detection

On invocation:

1. **Check for existing profile:** Read `clients/<project>/context-profile.json`
   - If exists → **Update mode**: Show current profile summary, ask which sections to update
   - If not → **Create mode**: Run full interview from Section 1

2. **Check for existing project files:** If `clients/<project>/icp.md`, `offer.md`, `buyer-profile.md` have content beyond template defaults, pre-populate what you can from those files and SKIP the corresponding questions. Tell the user: "I pulled X fields from your existing project files. I'll only ask what's missing."

---

## Interview Flow

Ask one section at a time using AskUserQuestion. User answers in plain text — numbers don't need to match, just answer in order.

### Section 1 — Welcome (no questions)

**Show this message before starting:**

> Welcome to Fuggy's Media. This questionnaire is designed to streamline the onboarding process for all of our clients and for us to know you and your business better. It'll take about 15–20 minutes. When you're ready, we'll start with some basics about you and your business.

Then proceed to Section 2.

### Section 2 — Tell us about yourself

1. **Contact name(s)** *(required)* — Who should we address in emails and calls?
2. **Email address(es)** *(required)* — Best email(s) for our communications
3. **Business Manager ID** *(optional — request only if they'll run Meta ads)* — If you plan to run Meta ads with us, paste your Business Manager ID so we can later request ad account access. Find it via: Business Manager → Business Settings → Business Info (bottom of the page) → copy the Business Manager ID.

### Section 3 — Brand & Assets

> **OPERATOR DEEP-DIVE SLOT:** Before asking the fixed questions below, add 1–2 custom questions specific to the client's business type. This is where deep context comes from — don't skip it.
>
> **Examples:**
> - Growth services client → "What's your profit margin per customer?" / "What's your customer acquisition cost today?"
> - Paid advertising client → "What's your best-selling service or product?" / "What's your AOV (average order value)?"
> - E-commerce client → "What are your top 3 SKUs by revenue?" / "What's your repeat purchase rate?"
> - B2B client → "What's your average deal size and sales cycle length?"
> - Info products / coaching → "What's your flagship offer and its price point?"
>
> Record both the question you asked AND the answer under `brand.custom_deep_dive` in the JSON.

Then the fixed questions:

4. **Marketing assets link** — Share a Google Drive link (or similar) with any marketing images and creatives you have. Include logo files, product photos, lifestyle shots, and videos. Throw in AS MANY as possible, professional or not — we can build ad angles from almost anything.
5. **Logo upload** — Attach or paste a link to your current logo file(s). PNG with transparent background preferred. If you have light/dark versions, send both.
6. **Branding guidelines** — Any brand guidelines, colors, fonts, or visual preferences we should follow? Even a simple "we like dark tones with gold accents, avoid cartoon illustrations" helps a lot.

### Section 4 — Social Media & Organic

7. **Social links** — Paste URLs for all your active social profiles: website, Instagram, Facebook, TikTok, LinkedIn, YouTube, Twitter/X, and any others. If you don't have one of these, just say "none".

### Section 5 — Customer Avatar (the critical section)

This is the MEAT of the intake. Answers here feed directly into creative strategy, avatar research, and the onboarding strategy PDF. Take your time.

8. **Why do your customers buy your service?** — What is the big promise? How does your service solve their needs? (1–3 sentences is fine)
9. **What is unique about your service** compared to everyone else selling something similar? (Your differentiation wedge)
10. **Why would someone NOT buy your service?** What are their common objections? (List 3–5)
11. **Top 3 benefits** of your best-selling service to your customer (ranked — most important first)
12. **Three selling points** for your service (different from benefits — these are the "why you" reasons)
13. **Features** of your service — list as many as relevant (what's included, what's delivered)
14. **Competitors** — Name some competitors selling a similar service or solution. For each: business name + 1-sentence description. (3–5 is ideal)
15. **Target audience age range** — Select all that apply: `18-24`, `25-34`, `35-44`, `45-54`, `55-64`, `65+`
16. **Target audience gender** — Select all that apply: `Male`, `Female`
17. **Daily troubles** — Do members of your audience have any common daily troubles, problems or frustrations? (Describe what a typical bad day looks like for them)
18. **THE ONE pain point** — What is THE MOST common problem AND THE MOST important pain point that your customers have that your service directly solves? (Pick ONE — the biggest. This becomes the primary constraint on the strategy PDF.)

### Section 6 — Final Details & Goal Settings

19. **Additional business info** — Is there any additional information about your business or goals you'd like us to know? (Anything we might have missed.)
20. **Marketing helpers** — Anything that you believe will help us in your marketing? (Past campaigns that worked, what didn't, internal data, customer quotes, anything.)
21. **90-day goal** *(critical)* — What do you hope for us to achieve for your business in 90 days? Be specific. **Use your own words.** This exact answer becomes your Dream Translation on the onboarding strategy PDF cover page.

---

## Post-Interview Processing

After all sections are answered:

1. **Parse answers** into the JSON schema below
2. **Set `_last_updated`** to today's date — use `bash -c 'date +%Y-%m-%d'`, NEVER model knowledge
3. **Derive `brand.vertical`** from answers — use one of the keys from `skills/onboarding-strategy-pdf/references/benchmarks-registry.md` (`sg_property`, `saas_b2b`, `ecommerce_dtc`, `local_service`, `info_products`, `real_estate_us`, `healthcare`, `agency`, `sg_property_malay_muslim`, `saas_b2c`, or `default`). If unsure → use `default` and flag it in the summary for Jerel to confirm.
4. **Cross-reference** with existing project files — if answers enrich `icp.md`, `offer.md`, or `buyer-profile.md`, note it but do NOT auto-update those files
5. **Write** the JSON to `clients/<project>/context-profile.json` (create the file if it doesn't exist)
6. **Show summary** — compact table: sections completed, field-fill rate, any flagged gaps
7. **Suggest next steps** — which downstream skill to run next. Usual order:
   - If avatars missing → `avatar-research` skill
   - If onboarding call scheduled → `onboarding-strategy-pdf` skill
   - If campaign ready to launch → `ad-concept-engine` skill
8. **Save uploads** — if the client provided a Google Drive link or logo, save the URL in the JSON. Flag for Jerel to manually download assets into `clients/<project>/assets/`.

---

## JSON Output Schema

```json
{
  "_schema_version": "2.0",
  "_intake_form": "Fuggy's Media Client Onboarding (6 sections)",
  "_last_updated": "",

  "contact": {
    "names": [],
    "emails": [],
    "business_manager_id": ""
  },

  "brand": {
    "business_name": "",
    "vertical": "",
    "google_drive_assets_link": "",
    "logo_path_or_url": "",
    "branding_guidelines": "",
    "custom_deep_dive": [
      { "question": "", "answer": "" }
    ]
  },

  "social_links": {
    "website": "",
    "instagram": "",
    "facebook": "",
    "tiktok": "",
    "youtube": "",
    "linkedin": "",
    "twitter_x": "",
    "other": []
  },

  "customer_avatar": {
    "big_promise": "",
    "unique_value": "",
    "common_objections": [],
    "top_3_benefits": [],
    "three_selling_points": [],
    "features": [],
    "competitors": [
      { "name": "", "description": "" }
    ],
    "target_audience": {
      "age_ranges": [],
      "genders": []
    },
    "daily_troubles": "",
    "primary_pain_point": ""
  },

  "final_details": {
    "additional_info": "",
    "marketing_helpers": "",
    "ninety_day_goal": ""
  }
}
```

### Field Rules

- **Strings:** Use `""` for unanswered, NEVER invent content
- **Arrays:** Use `[]` for unanswered, populate with as many entries as the user provides
- **`_last_updated`:** Set to current date in YYYY-MM-DD format using `bash -c 'date +%Y-%m-%d'`
- **`_schema_version`:** Increment on schema changes (2.0 → 2.1 when adding fields)
- **`brand.vertical`:** Must match a key in `skills/onboarding-strategy-pdf/references/benchmarks-registry.md`. Default to `"default"` and flag in summary if unsure.
- **`brand.business_name`:** Derived from user's answers or project slug if not explicitly asked
- **`target_audience.age_ranges`:** Array of strings from fixed set: `"18-24"`, `"25-34"`, `"35-44"`, `"45-54"`, `"55-64"`, `"65+"`
- **`target_audience.genders`:** Array of strings from fixed set: `"Male"`, `"Female"` (both can be selected)
- **`brand.custom_deep_dive`:** Array of question/answer pairs from Section 3's operator deep-dive slot. Can be empty.

---

## Downstream Field Mapping

Here's exactly how each new field flows into downstream skills:

| Field | Consumed by | How it's used |
|---|---|---|
| `customer_avatar.big_promise` | `onboarding-strategy-pdf` (page 4 positioning), `copywriting`, `ad-concept-engine` | Positioning angle + mechanism name seed |
| `customer_avatar.unique_value` | `onboarding-strategy-pdf` (page 4 differentiation wedge) | Why-you-not-them |
| `customer_avatar.common_objections` | `onboarding-strategy-pdf` (page 5 AAA framework if existing ads), `copywriting`, `ad-concept-engine` | Objection handling in ad copy + audit narrative |
| `customer_avatar.top_3_benefits` | `copywriting`, `ad-concept-engine` | Benefit-led ad angles |
| `customer_avatar.three_selling_points` | `copywriting` | Headline and hook material |
| `customer_avatar.features` | `copywriting` | Feature-to-benefit translation |
| `customer_avatar.competitors` | `ad-concept-engine`, `avatar-research`, swipe file research | Blue ocean gap analysis |
| `customer_avatar.target_audience` | `avatar-research`, Meta ad targeting setup | Targeting parameters |
| `customer_avatar.daily_troubles` | `avatar-research`, `onboarding-strategy-pdf` (page 3 avatar top_pains) | Avatar card content |
| `customer_avatar.primary_pain_point` | `onboarding-strategy-pdf` (page 1 primary constraint rationale), `ad-concept-engine` | The ONE pain that drives everything |
| `final_details.ninety_day_goal` | `onboarding-strategy-pdf` (page 1 Dream Translation) | **Client's exact words on the cover page** |
| `brand.vertical` | `onboarding-strategy-pdf` (benchmarks lookup for Calculator Close math) | Per-vertical CTR/CPL/ROAS benchmarks |
| `brand.google_drive_assets_link` | Manual — Jerel downloads assets | Source material for creative |
| `brand.branding_guidelines` | `image-generation`, `ad-concept-engine` | Visual style constraints |
| `contact.business_manager_id` | `meta-ads-uploader` | Ad account access when running Meta ads |

**Key insight:** `final_details.ninety_day_goal` is the single most important field for the onboarding call deliverable — it becomes the Dream Translation quote on Page 1 of the PDF, rendered in the client's own words. Make sure the client answers this in full sentences, not bullet points.

---

## Update Mode

When `context-profile.json` already exists:

1. Read the existing JSON
2. Show a summary: "Current profile has 6 sections. [X] populated, [Y] empty."
3. Ask: "Which sections do you want to update? (2-6, or 'all', or 'gaps' to fill empty fields only)"
4. Only ask questions for selected sections
5. Merge new answers into existing JSON — do NOT wipe fields the user didn't update
6. Update `_last_updated` and increment `_schema_version` if schema changed

---

## Integration with Other Skills

This profile is the FIRST file any skill should read when loading project context. Context load order (per root CLAUDE.md):

```
1. context-profile.json (business identity — WHO)  ← this skill produces it
2. voice/<person>/ (writing voice — HOW)
3. icp.md, offer.md, brand-voice.md (marketing specifics — WHAT)
4. buyer-profile.md (buyer psychology — TO WHOM)
5. learnings.md (accumulated intelligence — WHAT WORKS)
```

### Critical downstream: `onboarding-strategy-pdf`

The onboarding strategy PDF generator specifically needs these fields from this intake to build a real client PDF:

- `final_details.ninety_day_goal` → `dream_translation.client_exact_words` on page 1
- `customer_avatar.primary_pain_point` → feeds `diagnostic.primary_constraint_rationale`
- `customer_avatar.common_objections` → feeds page 5 AAA-framed audit if client has existing ads
- `customer_avatar.competitors` → feeds `strategy_preview.differentiation_wedge`
- `brand.vertical` → feeds benchmarks-registry lookup for Calculator Close math

A complete Fuggy's Media intake directly enables a real `onboarding-strategy-pdf` run with zero additional manual JSON compilation.

---

## Error Handling

- If user says "skip" for a section → leave those fields as defaults, move to next section
- If user says "I'll come back to this" → save what's collected so far, note incomplete sections in summary
- If JSON already exists and user runs create mode → warn and offer: overwrite, update, or cancel
- If no project folder exists → create it first from `clients/_template/`, then proceed
- For file uploads (logo, Google Drive link): save the URL/path in the JSON; don't attempt to download/process the actual files in this skill — that's a manual post-interview step for Jerel
- If the user's 90-day goal answer is vague ("grow my business") → push back once: "Can you be more specific? What does 'grow' look like numerically — leads, revenue, calls booked?" — but don't push twice. Accept what you get.

<!-- skill-graph:start -->

## Related
<!-- auto-generated by scripts/link-skills.py — do not edit by hand -->

- [[onboarding-strategy-pdf]] (skill, 0.17)

<!-- skill-graph:end -->
