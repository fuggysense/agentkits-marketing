# Findings — Copywriting OS

Research storage for the Phase 1 scrape + audit. All external web content lives here (not in task_plan.md per security boundary).

## §1 Archive Map — copywriting.ai/archive

> **CORRECTION (post-session Jerel review):** Initial scrape found only 12 because beehiiv's `/archive` uses **client-side JavaScript pagination** — static `ctx_fetch_and_index` only returns page 1's 12 newest posts (pager "1234" renders client-side). The `?page=N` query string is ignored server-side. Verified via `/sitemap.xml` fetch + JS regex extraction: **TOTAL NEWSLETTERS = 47**. This session deep-extracted only the newest 12 (below §1.A). Remaining 35 are listed in §1.C and will be deep-read in Phase 1.5.

**Scraped:** 2026-04-24 via `ctx_fetch_and_index` + `/sitemap.xml` authoritative URL list
**Publisher:** beehiiv newsletter "Copywriting AI"
**Pagination gotcha:** client-side only; use sitemap or dev-browser for full enumeration
**Total newsletters identified (sitemap):** **47**
**Deep-extracted this session:** 12 (the most recent — #35 through #45 + Schwartz post)
**Authors seen:** Mark Masters (Masters Academy / 25K+ project author), Peggy Burnett (AI copy teardown author), NOVA (principle/history-leaning author)

### §1.A Deep-extracted this session (12 — most recent)

| # | Issue | Title | Author | Date | Length | URL slug (prefix `https://www.copywriting.ai`) |
|---|-------|-------|--------|------|--------|--------------------------------------------------|
| 1 | #45 | The Worst AI Sales Page I Read This Month | Peggy Burnett | 2026-04-16 | 14 min | `/p/worst-ai-sales-page-teardown` |
| 2 | #44 | Halbert Would Have Loved This (And Hated Most of It) | Mark Masters | 2026-04-13 | 13 min | `/p/halbert-ai-copywriting-one-person` |
| 3 | #43 | The (AI) Swipe File Engine | Mark Masters | 2026-04-09 | 14 min | `/p/swipe-file-engine-claude-project` |
| 4 | #42 | The Best Prompting Advice Is From 1937 | NOVA | 2026-04-04 | 10 min | `/p/most-important-prompting-principle-1937` |
| 5 | #41 | Proof: Where AI Helps Your Copy More | Peggy Burnett | 2026-03-31 | 11 min | `/p/first-draft-vs-edit-layer` |
| 6 | (gap) | Schwartz Knew Why Your AI Copy Feels Hollow | Peggy Burnett | ~2026-03-25 | ? | `/p/schwartz-copy-cant-create-desire` |
| 7 | #40 | Two Claude Skills. Yours Free. | Mark Masters | 2026-03-21 | 12 min | `/p/two-claude-skills-yours-free` |
| 8 | #39 | The Headline Lab That Controls 80% of Your Results | Mark Masters | 2026-01-05 | 7 min | `/p/headline-laboratory-claude-project-skill` |
| 9 | #38 | Add Undeniable & Convincing Proof In Your Copy (with AI) | Mark Masters | 2025-12-29 | 7 min | `/p/proof-arsenal-claude-project-skill` |
| 10 | #37 | Advanced "AI Emotion Engine" for High-Converting Copywriting | Mark Masters | 2025-12-16 | **32 min** | `/p/emotional-sequencing-engine-claude-project-skill` |
| 11 | #36 | Your Copy Is Leaking Money (Here's How To Plug the Leak) | Mark Masters | 2025-12-01 | **30 min** | `/p/objection-destroyer-claude-project-skill` |
| 12 | #35 | The Copy Scout System Behind 25K Projects | Mark Masters | 2025-11-24 | 16 min | `/p/research-command-center-scout-system-claude-projects-skills` |

**All 12 slugs confirmed** (of 47 total in archive). Schwartz post sits between #40 and #41 chronologically — unnumbered guest post or #40.5.

### §1.B Correction: sitemap-sourced full count = 47 newsletters

Extracted via JS regex against `https://www.copywriting.ai/sitemap.xml` in the context-mode sandbox. Sitemap is the authoritative list since archive pagination is JS-only.

### §1.C Remaining 35 newsletters — NOT YET DEEP-READ (pending Phase 1.5)

Sorted newest to oldest by sitemap `<lastmod>`. Slug titles inferred from URL + publication pattern; exact authors/min-read require Phase 1.5 fetch.

| # | Date | Slug | Likely topic (inferred from slug) |
|---|------|------|------------------------------------|
| 13 | 2025-11-05 | `/p/client-system-claude-project-skills` | Client-management Claude Project skills |
| 14 | 2025-11-01 | `/p/framework-arsenal-claude-projects-skills` | Copy framework arsenal (likely inventory of canonical frameworks) |
| 15 | 2025-08-28 | `/p/infinite-loop-system-revenue` | Revenue system / recurring-touch loop |
| 16 | 2025-08-25 | `/p/masters-orchestration-system-47-touchpoints` | Orchestration system, 47-touchpoint customer journey |
| 17 | 2025-08-21 | `/p/masters-command-sequence-story-structure-ai-hollywood` | Story structure / Hollywood narrative pattern |
| 18 | 2025-08-11 | `/p/100m-copywriting-offer-alex-hormozi` | **Hormozi $100M offer framework applied to copywriting** |
| 19 | 2025-08-07 | `/p/5-day-revenue-generation-blueprint` | 5-day campaign blueprint |
| 20 | 2025-08-02 | `/p/5-ai-email-templates-prompts` | 5 email templates + prompts |
| 21 | 2025-07-29 | `/p/copywriter-guide-standing-out-online-2025` | Positioning / differentiation guide |
| 22 | 2025-07-23 | `/p/predict-customers-do-31-days-future` | Predictive-behavior copy / customer-future framework |
| 23 | 2025-07-19 | `/p/data-pick-your-client-niche-copywriters` | Niche selection via data |
| 24 | 2025-07-10 | `/p/market-research-ai-solves-this` | Market research with AI |
| 25 | 2025-07-08 | `/p/70-hour-weeksfinancial-freedom` | Freelancer productivity / positioning |
| 26 | 2025-07-07 | `/p/hidden-ai-patterns-emails-revenue` | **AI patterns in emails (de-AI for email, likely maps to our `unslop`)** |
| 27 | 2025-07-02 | `/p/3-fears-copywriters-about-niching` | Niching psychology |
| 28 | 2025-07-01 | `/p/secure-four-clients-ai-precision` | Client acquisition via AI |
| 29 | 2025-06-11 | `/p/legend-architecture-your-origin-story-clients` | **Origin-story architecture / legend-building for clients** |
| 30 | 2025-06-11 | `/p/ai-client-acquisition-matrix` | Client acquisition matrix |
| 31 | 2025-06-06 | `/p/scott-adams-today-you-become-better-writer` | Scott Adams writer improvement |
| 32 | 2025-06-03 | `/p/4-evergreen-ai-email-templates-converts` | 4 evergreen email templates |
| 33 | 2025-05-21 | `/p/b2b-b2c-ai-emails-5-triggers-boost-sales-prompts` | B2B/B2C email triggers |
| 34 | 2025-05-19 | `/p/aics` | "AICS" framework (unclear) |
| 35 | 2025-05-01 | `/p/ai-copywriting-advertising` | AI copywriting for advertising |
| 36 | 2025-04-24 | `/p/ai-copywriting-foundations` | **Foundations (likely high-value primer)** |
| 37 | 2025-04-21 | `/p/ai-copywriting-landing-pages` | **Landing-page copy with AI** (directly overlaps our `copywriting` skill) |
| 38 | 2025-04-21 | `/p/ai-copywriting-short-form` | Short-form copy with AI |
| 39 | 2025-04-21 | `/p/ai-copywriting-email-marketing` | **Email marketing with AI** (overlaps `email-sequence` + `email-marketing`) |
| 40 | 2025-04-17 | `/p/using-ai-to-get-what-you-need-from-clients` | **Onboarding from clients with AI** (directly relevant to our onboarding rewrite in §6) |
| 41 | 2025-04-17 | `/p/value-based-pricing-models-ai-copywriting` | Value-based pricing for AI copy service |
| 42 | 2025-04-17 | `/p/how-to-position-ai-copywriter` | **Positioning AI copywriter (DWY-relevant)** |
| 43 | 2025-04-17 | `/p/ai-copywriting-glossary` | AI copywriting glossary |
| 44 | 2025-04-17 | `/p/fundamentals-ai-copywriting` | Fundamentals of AI copywriting |
| 45 | 2025-04-17 | `/p/direct-response-copywriting-glossary` | Direct response glossary |
| 46 | 2025-04-17 | `/p/fundamentals-direct-response-copywriting-part-2` | DR fundamentals part 2 |
| 47 | 2025-04-17 | `/p/fundamentals-direct-response-copywriting-part-1` | DR fundamentals part 1 |

### §1.D High-priority candidates from the remaining 35 (pre-read hypothesis)

Based on slug + relevance to copy-OS goals, these are the **top 10 to prioritize** in Phase 1.5:

1. **#18 Hormozi $100M offer applied to copywriting** — direct input for our `offer-builder` skill + sales-letter-method offer component
2. **#40 Using AI to get what you need from clients** — direct input for our §6 onboarding form rewrite
3. **#42 How to position AI copywriter** — DWY productization positioning
4. **#37 AI copywriting landing pages** — benchmark against our `copywriting` skill + #40's landing page skill
5. **#39 AI copywriting email marketing** — benchmark against `email-sequence` + `email-marketing`
6. **#14 Framework Arsenal** — likely canonical copy-framework inventory (PAS, AIDA, 4Ps, FAB, etc.)
7. **#26 Hidden AI patterns in emails, revenue** — input for `unslop` email-domain profile
8. **#17 Masters command sequence story structure AI Hollywood** — narrative architecture for long-form
9. **#29 Legend architecture / origin story** — direct input for brand-building + sales-letter founder-story component
10. **#36 / #44 AI copywriting foundations + fundamentals** — canonical primers (likely condense many later frameworks)

**Open question for Jerel:** run Phase 1.5 now (35 more fetches + extractions) OR proceed to Phase 2 build with the 12 we have, then loop back for 1.5 as enrichment later? See §7.

**Author distribution:** Mark Masters 8, Peggy Burnett 3, NOVA 1.
**Total read time:** ~165 min (~2h45m) if deep-read linearly. Phase 1.3 workers will extract structured data, not consume full bodies into main context.
**Strong Mark Masters "Claude Project Skill" pattern:** 8 of 12 slugs end in `-claude-project-skill`. He's shipping packaged skills — a direct inspiration for our `copywriting-os` umbrella.

### Structural notes

- **Format:** beehiiv newsletter, clean HTML → markdown conversion
- **No paywall / no auth wall.** `ctx_fetch_and_index` works directly.
- **2 slugs uncertain** (Issues 36, 38). Will resolve via Phase 1.3 bulk fetch — if the slug cannot be reverse-resolved from the archive HTML, I'll search the site for the title directly.
- **Recommended Phase 1.3 tool chain:** `ctx_fetch_and_index` each of 12 URLs → `ctx_search` across indexed content with structured-extraction queries (frameworks, tactical moves, copy examples, Claude skill references).

### High-value candidates (pre-read hypothesis — to validate in Phase 1.3)

1. **Issue 36 "Your Copy Is Leaking Money" — 30 min read (longest by 2x)** → likely the densest framework doc
2. **"The Copy Scout System Behind 25K Projects"** → deployable research-scout workflow; directly maps to our `researcher` agent + `deep-research` skill
3. **Issue 43 "The (AI) Swipe File Engine"** → active swipe-file tool; maps to our `ad-library-scraper` + `swipe-files/` structure
4. **Issue 37 "AI Emotion Engine"** — "6 emotions between no and yes, exact order" → direct input for `sales-letter-method` Phase 2 stitcher
5. **Issue 40 "Two Claude Skills. Yours Free."** — landing page skill + sales email skill → direct skill references to benchmark our `copywriting` + `email-sequence` against
6. **Issue 45 "Worst AI Sales Page" teardown** — failure modes + prompts that caused them → direct input to `unslop` profile for "long-form-sales-letter"
7. **"Halbert Would Have Loved This" (#44)** — Halbert A-pile test, coat of arms, one-person rule → directly applicable to `sales-letter-method` Phase 3 reviewer
8. **"Schwartz Knew Why Your AI Copy Feels Hollow"** — Schwartz awareness + why AI copy fails → validates our existing Schwartz 5-stage brief approach

## §2 Current Marketing Profile Audit

### §2.A Copywriting-relevant skills (frontmatter confirmed via sandbox)

| Skill | Cat / Diff | Scope | Reusable in copywriting-OS as... |
|-------|------------|-------|----------------------------------|
| `sales-letter-method` v1.0.0 | content / advanced | 800–2000+ word cold-traffic sales letter; 12-component framework; 5-phase pipeline (Context Scan → parallel drafters → stitcher → Conversion Gate → polish); 3-reviewer stack | **Sales-letter module** — invoked when output = long-form cold-traffic letter |
| `copywriting` v1.0.0 | content | Marketing page copy, headlines, CTAs | **Page-copy module** (homepage, pricing, features, about) |
| `copy-editing` v1.0.0 | content | Multi-pass editing sweeps (Sweep 8 = De-AI) | **Polish module** — universal post-write pass |
| `email-sequence` v1.0.0 | content | Drip/welcome/nurture/re-engagement/lifecycle | **Email module** |
| `email-marketing` | content | Deliverability, subject lines, broader strategy | Email supporting skill |
| `ad-concept-engine` v2.0.0 | content / advanced | DCT-aware ad concept pipeline, multi-avatar, Meta batch assembly | **Ad module orchestrator** |
| `big-angle-spotter` | content | 12-step Opus/Sonnet pipeline per angle; 1 angle = 1 DCT = 1 Ad Set; outputs 1 angle + 3 headlines + 3 ad prompts + 3 image prompts | Called by ad module for angle generation |
| `headline-bank` | content | 75+ headlines × 5 awareness levels × 10 angle banks, single mass-desire anchor | Headline reservoir (alternate path to big-angle-spotter) |
| `avatar-research` | research | 16-point psychological breakdown (Schwartz + Top 5 Deep Fears + Raw Inner Dialogue + Desired Transformation + Relationship Impact) | **Avatar module** — feeds every copy domain |
| `source-of-truth` | research | 26-section paid-ads SoT; multi-product (ecom/SaaS/service/info/agency/property) | Strategic research foundation |
| `client-onboarding` v2.1.0 | core | 6-section / 21-question intake; scaffolds `context-profile.json`; quit-and-resume checkpoints | **Onboarding flow — needs a general-copy sibling** |
| `business-profile` v2.0.0 | core / Fuggy's | Fuggy's ad-optimized questionnaire, 6 sections, writes `context-profile.json` | Property-agent onboarding — keep as-is; copy-OS spawns sibling |
| `content-moat` v1.0.0 | content | Originality-first ideation, 10 layer types, copycat resistance scoring | **Differentiation module** — prevents generic output |
| `unslop` v1.0.0 | utility | Domain-specific AI pattern detection; Layer 1 of 4-layer de-AI stack | **De-AI Layer 1** — universal polish |
| `brand-building` v1.0.0 | core | Brand voice, identity, positioning | Voice/positioning input |
| `content-strategy` | content | Content planning, editorial calendars | Distribution planner |
| `scrapecreators` | utility | 25+ platform social intelligence API (TikTok/IG/YT/LI/FB/X/Reddit/Threads/etc.) | **Scrape input layer** (auto-fill onboarding) |
| `transcribe` | utility | yt-dlp + faster-whisper (Groq alt per memory) for 1000+ video sites | **Scrape input layer** (YouTube + testimonial transcription) |

### §2.B Copywriting-relevant agents

| Agent | Role | Copy-OS relevance |
|-------|------|-------------------|
| `copywriter` | Content creation, headlines, CTAs | Primary writer — called by every copy domain |
| `brand-voice-guardian` | Tone/voice consistency review | Post-write QA |
| `conversion-optimizer` | CRO psychology review | Pre-publish gate |
| `brainstormer` | Angles, messaging, ideation | Upstream exploration |
| `persona-builder` | 3-mode buyer profile (extract/interactive/enrich) | Avatar prep (alt to avatar-research) |
| `researcher` | Market + competitive research | Upstream inputs (esp. for SoT + avatar) |

### §2.C Current onboarding + client structure

**`clients/_template/` scaffold:**
- Core files: `offer.md`, `icp.md`, `brand-voice.md`, `buyer-profile.md`, `channels.json`, `learnings.md`, `asset-map.md`, `story-bank.md`, `metrics-config.json`
- Subfolders: `avatars/_index.md`, `brand/README.md` + `brand/reference/` (empty), `campaigns/`, `deliverables/`, `feedback/README.md`

**Current onboarding skills:**
- `client-onboarding` v2.1.0 — orchestrates the intake, scaffolds project, routes to agents, validates readiness
- `business-profile` v2.0.0 — the Fuggy's questionnaire itself → `context-profile.json`

**Current Fuggy's form (what user shared in-message) — 14 sections, ~21 questions:**
1. Contact info + Business Manager ID
2. Brand assets (Drive link, logo, guidelines, socials, "why you" statement, banned words)
3. Ideal client deep dive (top 2-3 clients + their exact words + 3 FAQs + the "one sentence" that excites)
4. Unique edge / proprietary framework + real-world example
5. Objections / sales process / where prospects stick
6. Benefits / features / selling points (×3 each)
7. Client pains / frustrations
8. Proof / testimonials (Drive link)
9. Content that already works (top-performing piece, trigger events)
10. Competitors
11. Target audience demographics
12. 90-day goals
13. Final check / anything else

### §2.C.ii Onboarding automation matrix (Phase 1.4 seed — maps to §6 rewrite sketch)

**✅ Replaceable by Claude Code scraping (drop from form, ask for URL instead):**

| Current question | Replaced by | Tool chain |
|------------------|-------------|------------|
| Voice samples / "how would you answer in your own words" | YouTube channel URL + 3 recent videos | `transcribe` + `scrapecreators` |
| Content that works / top-performing post | Social handles (IG/TT/LI/YT) | `scrapecreators` (engagement-ranked) |
| Testimonials / Google reviews | Testimonial folder URL (Drive or website proof section) | `transcribe` (videos) + `chrome-mcp` (review pages) |
| Brand assets (logo, colors, typography) | Website URL | `chrome-mcp` logo SVG + color + font extraction → `design-system` skill |
| Competitor list | Industry tag (e.g., "sg-property-agents") | `ad-library-scraper` (already ships per-industry pools) |
| Benefits / features / selling points | Website URL | `ctx_fetch_and_index` on product/services page |
| Offer structure / pricing | Website URL + pricing page | Same |
| Services / what you sell | Website URL | Same |

**⚠️ Must still ask human (can't infer):**
- Pricing/offer specifics when not on site
- Banned words / voice preferences (personal taste)
- Unique edge / proprietary framework (often not public)
- Sales process internals (stages, typical friction)
- 90-day goals (forward-looking)
- Business Manager ID (private identifier)
- The "exact sentence that makes prospects lean in" (internal knowledge)

**Net result:** form shrinks from ~21 questions to ~8–10 questions + 3 URL drops (site, YouTube channel, testimonial folder).

### §2.D Supporting infrastructure

- **V.O.I.C.E. system (voice/<person>/):** Confirmed `voice/jerel/` contains `about-me.md`, `brand-voice.md`, `compound-ideas.md`, `deep-profile.md`, `voice-examples.md`, `working-style.md`. Per-person, not per-project. "Voice = the person (how you write). Project = the business."
- **6-stage creative pipeline** (`.claude/workflows/creative-pipeline.md`): Research → Angle → Concept → Create → Test → Feedback. Uses `/ads:feedback <slug> <wave>` for stage 6. **Copy-OS sits orthogonal as a writing layer that feeds every stage.**
- **MCP integrations wired:** `scrapecreators`, `chrome-mcp`, `dataforseo`, `postiz`, `kilo-gateway`, `gemini-cli`, `ollama` (Qwen3 local), `netlify`, `paper`
- **Research LLM router** (`scripts/research-llm.sh`): offloads synthesis to Nemotron/Minimax/Gemini/Qwen — saves Claude tokens on research-heavy tasks (like the 12 newsletter deep-reads I'm about to do)

### §2.E Pre-existing "copy OS"-ish artifacts

**NONE as a unified orchestrator.** The components exist but no umbrella skill:
1. Asks "what copy do you need?" and routes
2. Shares research/avatar/voice context across copy types (today: each skill re-reads `context-profile.json` independently → no shared "copy brief" artifact that carries from sales letter → emails → ads → landing pages)
3. Provides a single dogfood-able command for a trainee to follow end-to-end
4. Is exportable as a DWY productized package

**This validates the Phase 2 umbrella-skill build plan.**

### §2.F Top gaps vs. copywriting-OS goal

1. **No unified router skill** (`skills/copywriting-os/` doesn't exist)
2. **No auto-scrape onboarding path** (`client-onboarding` is 100% manual Q&A)
3. **No shared "copy brief" artifact** carrying research/avatar/voice across skill boundaries
4. **No `clients/_template/copy-system/` folder scaffold**
5. **No human-training docs** teaching a new user the end-to-end flow
6. **No DWY export package** (current system assumes full operator access)
7. **No generalized "unslop long-form-sales-letter" profile** (current unslop profile is generic)
8. **No feedback loop from shipped copy → skill learnings** at the copy-domain level (exists for ads via `feedback-router`, missing for sales letters / emails / pages)

## §3 Newsletter Extractions

All 12 newsletters fetched + indexed into context-mode sandbox (cai #35–#45 + Schwartz). Total indexed: ~241KB across 12 sources. Extractions below are structured per the schema in §3 header. Dense bodies stay in sandbox — only the distilled gold lands here.

---

#### Newsletter #45 — "The Worst AI Sales Page I Read This Month"
- **URL:** https://www.copywriting.ai/p/worst-ai-sales-page-teardown
- **Author:** Peggy Burnett | **Date:** 2026-04-16 | **Length:** 14 min
- **Core thesis (1 sentence):** Most LLM-generated sales pages fail in the same stackable ways; this is a live teardown that names each failure mode so you can pattern-match your own drafts.
- **Frameworks introduced:**
  - **Element-by-Element Teardown** — a reviewer stance that walks a page hero → lead → body → proof → CTA, surfacing category-specific failure modes at each stage
  - **"4 problems in 12 words" diagnostic** — naming how many distinct failures stack in a single headline
- **Tactical moves:**
  - Delete any "transform-class" verb ("transform", "elevate", "unlock", "revolutionize") unless followed by a specific, named, measurable outcome — if Claude reached for it, it doesn't know what the product actually does
  - Read hero aloud → ask "would the buyer recognize her own Tuesday morning here, or is this category-speak a PM would write in a user story?"
  - Pattern-match against ~12 failure modes seen in LLM pages across the quarter
- **Copy examples cited:**
  - BAD hero: "Transform Your Booking Experience With The Ultimate All-In-One Scheduling Solution" — "transform" = filler, "booking experience" = category-speak, "ultimate all-in-one" = uncommitted superlative stack, no specific outcome named
  - Product context: scheduling tool for solo service providers (massage therapists, tutors, trainers) — but the page never mentions the 10am-text-cancel reality the buyer actually lives in
- **Novel vs. our stack:** The TEARDOWN AS REVIEWER STANCE is missing from our `sales-letter-method` Phase 3. Our current 3-reviewer stack (buyer-lens + copy-chief + self-contained) doesn't do element-by-element pattern-matching against a named failure-mode library.
- **Quotable gold:**
  - > "If you've been using Claude or ChatGPT for long-form sales copy, you've probably shipped something that hit at least two of these. I have too."
  - > "'Transform' is a word Claude reaches for by default when it doesn't know what the product actually does."
- **Cross-links:** Feeds `unslop` (domain profile for "long-form-sales-letter" or "landing-page"), `copy-editing` Sweep 8, new `teardown-reviewer` we should build.

---

#### Newsletter #44 — "Halbert Would Have Loved This (And Hated Most of It)"
- **URL:** https://www.copywriting.ai/p/halbert-ai-copywriting-one-person
- **Author:** Mark Masters | **Date:** 2026-04-13 | **Length:** 13 min
- **Core thesis:** Halbert's three most famous ideas (A-pile test, Coat of Arms, One-Person Rule) are the exact fix for what's wrong with most LLM-generated copy — and each has a prompt-level translation.
- **Frameworks introduced:**
  - **A-pile / B-pile test** — readers sort inbox in a quarter-second by whether message feels personal or generic. A-pile = opens. B-pile = ignored. Applies to subject lines + sender names + hero lines.
  - **Coat of Arms method** — audience portrait doc (~200 words) with concrete, non-demographic specifics: who they are, what they read, what they fear, what they spend on without thinking, what they lied about at parties, what they'd never admit wanting. Loaded as Claude Project knowledge file, referenced before every write.
  - **One-Person Rule** — write to ONE real human (name, job, single moment), not a persona or segment. Prompt add-on forces the model to name who it wrote to at the end of the response.
- **Tactical moves:**
  - **Coat of Arms template** (verbatim copyable into prompt):
    > AUDIENCE COAT OF ARMS: [name]
    > Who they are (specific, not demographic): "Marketing directors at B2B SaaS companies between Series A and Series C, typically the 2nd or 3rd marketing hire, reporting to a founder who doesn't quite understand what they do" (NOT "B2B marketing directors age 35-50")
    > What they read / podcasts they listen to in the car / Twitter accounts they actually open...
  - **System operating procedure** (put in Claude Project instructions):
    1. Reference coat of arms specifics before generating any copy
    2. Name the specific person you're writing to (one real moment, not a demographic)
    3. Produce the copy aimed at that one person
    4. If output is subject line / headline / first-seen element, apply A-pile test: "does this look like it came from a person or a marketing department?"
    5. **At the end of each response, briefly state which coat-of-arms specifics you used and who you imagined writing to. Do not skip step 5. It's how the user checks your work.**
  - **One-person prompt add-on** (drop into any writing prompt):
    > Before you write, think of a specific person this copy is being written to. Give them a name, a job, and a one-sentence description of the moment they're in when they read this. Then write as if you were sending this directly to that person. Do not write for the audience. Write for that one person. At the end of your response, tell me who you imagined. Name, job, moment.
- **Copy examples cited:**
  - Specific vs. generic person: "Priya, Head of Growth at a 40-person Series A SaaS, reading this at 7:45pm on a Tuesday with her d[inner warming in the microwave]" vs "Sarah, marketing manager, busy"
- **Novel vs. our stack:** The ENFORCEMENT MECHANISM ("tell me who you imagined") is what we're missing. Our skills have voice rules but don't force post-hoc declaration. This single line added to `sales-letter-method`, `copywriting`, `email-sequence`, and `ad-concept-engine` would measurably improve every output.
- **Quotable gold:**
  - > "Your reader sorts their inbox the same way. Not consciously. In the first quarter-second of looking at a subject line and sender name, their brain decides whether this feels like something from a person or something from a marketing department."
  - > "The audience understanding never makes it into the prompt."
  - > "The 'tell me who you imagined' line is the enforcement mechanism."
- **Cross-links:** Coat of Arms ↔ our `buyer-profile.md` + `avatar-research` 16-point breakdown (which is RICHER but not prompt-ready). One-Person Rule ↔ new `one-person-enforcement.md` prompt fragment loaded by every copy skill.

---

#### Newsletter #43 — "The (AI) Swipe File Engine"
- **URL:** https://www.copywriting.ai/p/swipe-file-engine-claude-project
- **Author:** Mark Masters | **Date:** 2026-04-09 | **Length:** 14 min
- **Core thesis:** Swipe files are graveyards unless each entry has structured metadata + the project has retrieval-ready query prompts; then you can pull the right reference in 30 seconds instead of scrolling for 4 minutes and giving up.
- **Frameworks introduced:**
  - **Swipe File Engine** — Claude Project holding entire swipe file; each entry = full text + metadata (what the copy is doing, who it targets, what problem it solves); custom query prompts that retrieve by audience-awareness level / objection / element type
- **Tactical moves:**
  - Structure each swipe entry with metadata: audience, awareness stage, objection handled, copy element (hook / lead / body / proof / CTA / close), source, known performance
  - Build query prompts: e.g. "what have I saved that handles a skeptical B2B audience at the awareness stage of 'knows the problem, hates the usual solutions'"
  - Two actions the project does: (1) turn each piece into a reason-able structured entry, (2) provide query prompts so the file gets pulled into work instead of sitting next to it
- **Novel vs. our stack:** We have `ad-library-scraper` with SQLite + Ghost Postgres enrichment (L1 always, L2 transcripts/OCR for >30d ads, L3 Nemotron classifier) + per-industry Schwartz brief. **We DON'T have the same for non-ad copy** — sales letters, emails, landing pages, headlines from competitors or our own shipped work. Gap: a `copy-swipe-engine` that does the same for long-form copy.
- **Quotable gold:**
  - > "Your swipe file is a graveyard."
  - > "You're not using research. You're hoarding it." (cross-quote from #35)
  - > "A folder of files isn't a working resource. It's a pile."
- **Cross-links:** `ad-library-scraper` (pattern-match for how we'd build it), `swipe-files/` directory.

---

#### Newsletter #42 — "The Best Prompting Advice Is From 1937"
- **URL:** https://www.copywriting.ai/p/most-important-prompting-principle-1937
- **Author:** NOVA | **Date:** 2026-04-04 | **Length:** 10 min
- **Core thesis:** Robert Collier's 1937 principle — "Enter the conversation already happening in the customer's mind" — is the single most useful instruction you can give an AI before asking it to write anything.
- **Frameworks introduced:**
  - **Single-sentence pre-prompt gate:** every prompt for AI copy must carry explicit info about the conversation the reader is already having (worries, desires, frustrations, half-formed thoughts) — otherwise the model starts from the product and works outward
- **Tactical moves:**
  - BAD prompt: "Write a sales email for a project management tool targeting small business owners" → starts from product, manufactures generic features/benefits
  - GOOD prompt: starts from where the reader already is (explicit named conversation: e.g., "the conversation a small-business owner is having at 11pm on Sunday when they're still working on invoices they should have sent Friday")
- **Copy examples cited:**
  - Prompt-structure-only advice (the Twitter thread variety: role assignments, constraints, output format) produces structurally sound prompts that generate copy nobody reads
  - Collier's principle IS about human psychology first, technique second
- **Novel vs. our stack:** Our `sales-letter-method` Phase 0 Context Scan captures the offer + buyer but doesn't explicitly prompt "what internal conversation is this reader having at the moment they see this?" as a REQUIRED field. Adding it would sharpen every downstream component.
- **Quotable gold:**
  - > "Enter the conversation already happening in the customer's mind."
  - > "It's obvious to us now but I wonder how many keep this in mind at all times?"
  - > "Your letter — your copy, your email, your landing page — has to meet them inside that existing conversation or it gets ignored."
- **Cross-links:** Foundational — feeds every copy skill. Becomes a universal pre-write gate in `copywriting-os`.

---

#### Newsletter #41 — "Proof: Where AI Helps Your Copy More"
- **URL:** https://www.copywriting.ai/p/first-draft-vs-edit-layer
- **Authors:** Peggy Burnett (+ Mark Masters) | **Date:** 2026-03-31 | **Length:** 11 min
- **Core thesis:** Head-to-head test between Mark's "Claude-first draft → human edits" workflow and Peggy's "human first draft → Claude 3-pass edit layer" workflow on the same project. Subtitle says "one winner" but Phase 1 preview only captured the setup, not the verdict — **FLAG: read full body in Phase 2 to extract the winner + nuance.**
- **Frameworks introduced:**
  - **Workflow A (Claude-first draft):** feed full brief + audience research + positioning + customer interviews to Claude in a project → ask for complete landing page draft → writer edits into shippable
  - **Workflow B (Human-first + Claude edit layer):** writer drafts from same materials → 3 separate Claude passes: (1) clarity, (2) persuasion gaps, (3) voice consistency with client's existing copy
  - **Clean-test rules:** same project folder, same inputs, same writer, same total time, only sequence differs
- **Tactical moves:**
  - Load everything (brief, positioning doc, customer interviews, client copy samples) into Claude Project BEFORE any prompt
  - 3-pass edit layer = distinct prompts per dimension (not one mega-review)
- **Novel vs. our stack:** Validates our `sales-letter-method` Phase 4 Polish (edit-layer after Phase 1 drafters). Suggests a `copy-workflow-router` meta-decision in `copywriting-os`: pick Workflow A vs B based on (a) copy type, (b) human skill level, (c) amount of usable research loaded.
- **Quotable gold:**
  - > "Same inputs. Same writer. Same amount of total time. Different sequence."
  - > "Everything Claude needed to reference was already in context before I typed a single prompt."
- **Cross-links:** `sales-letter-method` Phase 4, `copy-editing` multi-sweep pattern. **Open thread for Phase 2: extract the verdict.**

---

#### Newsletter ~#40.5 — "Schwartz Knew Why Your AI Copy Feels Hollow"
- **URL:** https://www.copywriting.ai/p/schwartz-copy-cant-create-desire
- **Author:** Peggy Burnett | **Date:** 2026-03-28 (between #40 and #41)
- **Core thesis:** Schwartz's 1966 principle — "copy cannot create desire, only channel existing desire" — is a DIAGNOSTIC TOOL, not philosophy. Peggy audited 34 AI-generated pieces; 23 tried to create desire, 11 channeled existing. The 11 channelers had ~40% higher time-on-page.
- **Frameworks introduced:**
  - **Channeling vs. Creating** binary — pass/fail gate on first two paragraphs of any AI-generated copy
  - **Why AI defaults to creating:** "If you don't put the existing desire into the prompt, the AI has no choice but to manufacture one." The prompt is written from the seller's perspective → output centers on product → reader's existing desires never enter the equation.
- **Tactical moves:**
  - Pre-prompt gate: "Am I channeling a desire that exists, or trying to create one? If creating, stop. Go find the real one. The prompt can wait."
  - Post-write check: read first 2 paragraphs — if they describe the reader's world = channeling. If they describe the product or paint a fantasy = creating. No gray area.
- **Novel vs. our stack:** Our prompts reference `buyer-profile.md` but don't enforce "existing desire naming" as a REQUIRED prompt field. Our Phase 3 reviewers don't do a "channeling check." This becomes a universal gate in `copywriting-os`.
- **Quotable gold:**
  - > "AI is fast at producing language. It is not fast at understanding what a specific person already wants at 9pm on a Tuesday when they're three tabs deep in competitor research and questioning their vendor choice."
  - > "The risk with AI is speed. The machine produces something in seconds. It sounds professional. It has good structure. And you ship it without catching that it started from the product instead of the reader. I've done this myself. More than once."
- **Cross-links:** `avatar-research` (where existing desires live), `buyer-profile.md` (quotes mining), universal pre-write gate.

---

#### Newsletter #40 — "Two Claude Skills. Yours Free."
- **URL:** https://www.copywriting.ai/p/two-claude-skills-yours-free
- **Author:** Mark Masters | **Date:** 2026-03-21 | **Length:** 12 min
- **Core thesis:** Two paste-and-go Claude Skills (Landing Page + 4-Day Sales Email) — and understanding how they're structured lets you modify for anything.
- **Frameworks introduced:**
  - **Skill #1 — Landing Page Copy Generator**
    - Deployment: `claude.ai > Settings > Customize > Skills > Upload a skill` (skill file = `SKILL.md` in a folder, zipped)
    - **3 inputs only** (explicit "don't overwhelm them"): (1) product/service + core promise, (2) target buyer + frustrations + what they've tried, (3) offer (price, guarantee, bonuses, deadline)
    - If user provides all 3 upfront, skip questions and start writing
    - Output structure: headline options, lead section, benefits, social proof structure, objection handling, CTA
  - **Skill #2 — 4-Day Sales Email Sequence Builder**
    - Structure: Day 1 opens conversation, Day 4 closes it
    - Each email: subject line options, body copy, CTA
    - **Voice rules (verbatim applicable to all copy):**
      - Write like one person talking to one person. Not a brand talking to a list.
      - Short paragraphs. 1–3 sentences max.
      - Reader's language, not marketing jargon. "Getting more clients" NOT "scaling your customer acquisition pipeline."
      - Readable in under 2 minutes on a phone screen.
      - No fake urgency. If there's no deadline, don't invent one.
      - Subject lines: short, specific, openable between meetings. Not clever for the sake of clever.
- **Tactical moves:**
  - Paste the full skill text directly into a Project's custom instructions if preferred
  - Single-file uploadable skill pattern: one `SKILL.md` = one capability
- **Novel vs. our stack:** This is the **DWY (Done-With-You) productization template**. Our skills are embedded in the agent kit — NOT single-file uploadable. To sell the system, we need to produce CLEAN, single-file, claude.ai-uploadable versions of our top copy skills. Candidate DWY pack: `sales-letter-method-lite.md`, `landing-page.md`, `email-4-day.md`, `headline-lab.md`, `proof-arsenal.md`.
- **Quotable gold:**
  - > "Write like one person talking to one person. Not a brand talking to a list."
  - > "Not clever for the sake of clever."
  - > "If there's no deadline, don't invent one. Use a different closing angle."
- **Cross-links:** Our `copywriting` (landing page), `email-sequence`. **DWY productization path is now visible.**

---

#### Newsletter #39 — "The Headline Lab That Controls 80% of Your Results"
- **URL:** https://www.copywriting.ai/p/headline-laboratory-claude-project-skill
- **Author:** Mark Masters | **Date:** 2026-01-05 | **Length:** 7 min
- **Core thesis:** Headlines drive 80% of results; most copywriters spend 80% of time on body copy. Stop writing headlines — engineer them via laboratory.
- **Anchor result:** Client landing page 2.1% → 4.7% conversion from single headline swap. +$34K/month.
- **Frameworks introduced:**
  - **5 Headline Mechanisms** (psychological categories, not formats):
    1. **Curiosity Gap** — incomplete pattern the brain must resolve. *"The Weird Reason Most Diets Fail After Day 11"*
    2. **Specific Benefit** — concrete outcome with numbers, timeframes, precise results. *"Add 2.3 Pounds of Muscle in 28 Days Without Changing Your Diet"*
    3. **Contrarian Hook** — challenges an assumed belief. *"Why Everything You Know About SEO Is Costing You Traffic"*
    4. **Fear / Risk** — cost of inaction, loss aversion. *"The $47,000 Mistake Hiding in Your Sales Page Right Now"*
    5. **Identity Call** — tribal recognition. *"For Copywriters Who Refuse to Compete on Price"*
  - "Every winning headline activates one or more of these. No exceptions."
  - **Headline Laboratory** = Claude Project with 3 knowledge files, starting with `headline-formulas.md` grouping formulas by mechanism
- **Tactical moves:**
  - Generate N headlines per (mechanism × angle) — lab output not single craft
  - Each formula in `headline-formulas.md` has variable slots: `[Unexpected Adjective]`, `[Common Belief]`, `[Authority/Group]`, `[Number]`
- **Novel vs. our stack:** Our `headline-bank` currently organizes by **awareness level (5 Schwartz) × angle bank (10 Cashvertising LF8/Halbert)** → 75+ headlines per mass desire. **It does NOT tag by psychological mechanism.** Upgrade path: add mechanism as a third axis → awareness × angle × mechanism (5 × 10 × 5 = 250 headline slots, or subset per mass desire). Also: our `big-angle-spotter` Step produces 3 ranked headlines per angle — these could be REQUIRED to cover ≥3 different mechanisms (diversification).
- **Quotable gold:**
  - > "You're polishing the furniture in a house nobody's entering."
  - > "The difference between amateurs and professionals isn't talent. It's systems. Amateurs write headlines. Professionals deploy headline laboratories."
- **Cross-links:** `headline-bank` upgrade, `big-angle-spotter` Step 10-12, `copywriting` hero section output.

---

#### Newsletter #38 — "Add Undeniable & Convincing Proof In Your Copy (with AI)"
- **URL:** https://www.copywriting.ai/p/proof-arsenal-claude-project-skill
- **Author:** Mark Masters | **Date:** 2025-12-29 | **Length:** 7 min
- **Core thesis:** Claims without proof are noise. 6 proof types — stacked throughout copy — collapse skepticism. "Proof density" is a measurable metric.
- **Anchor example:**
  - Copywriter A: *"Our software saves you time."*
  - Copywriter B: *"Our software saved Meridian Corp 14.3 hours per week within 60 days. Their ops manager called it 'the best $297 we've ever spent.'"*
  - Same claim. One ignored, one believed. Diff = proof density.
- **Frameworks introduced:**
  - **6 Proof Types:**
    1. **Social Proof** — testimonials, case studies, user counts, reviews
    2. **Credentials Proof** — authority markers, education, media mentions, client logos ("After writing for Apple, Nike, Salesforce..." / "Featured in Forbes, Entrepreneur, Inc.")
    3. **Demonstration Proof** — screenshots, video walkthroughs, before/after comparisons, live examples
    4. **Logical Proof** — if-then reasoning, analogies, mechanisms explained ("Because the system automates follow-up, you're no longer limited by your own memory...")
    5. **Specificity Proof** — concrete numbers, exact processes, precise timeframes ("2.3 pounds in 28 days" hits harder than "lose weight fast." Specificity implies measurement implies truth.)
    6. **Implied Proof** — embedded in HOW you communicate: confidence, detail depth, calm refusal to oversell (preview cut at this point — read full body in Phase 2 for complete definition)
- **Tactical moves:**
  - **Proof density rule:** every major claim gets ≥1 proof type attached; ideally stack 2-3 across different types
  - **Specificity hack:** any round number is a red flag. "14.3 hours" beats "a lot of hours." "$297" beats "affordable."
- **Novel vs. our stack:** Our `sales-letter-method` has Testimonial and Guarantee components but doesn't systematize the 6 types as a coverage matrix. Adding proof-density audit as a Phase 3 reviewer module is high-ROI.
- **Quotable gold:**
  - > "Your prospect wants to believe you. They're looking for permission to buy. But their brain is running a constant filter: Prove it. Prove it. Prove it."
  - > "Every claim without proof is a leak in your conversion bucket."
  - > "Most copywriters know they need testimonials. That's amateur hour. Professionals deploy six distinct proof types, strategically layered."
- **Cross-links:** `sales-letter-method` Phase 3 new `proof-density-audit.md` reviewer; every copy domain (emails, landing, ads, headlines use #3 Specificity heavily).

---

#### Newsletter #37 — "Advanced AI Emotion Engine for High-Converting Copywriting" (32 MIN — DENSEST)
- **URL:** https://www.copywriting.ai/p/emotional-sequencing-engine-claude-project-skill
- **Author:** Mark Masters | **Date:** 2025-12-16 | **Length:** **32 min** (densest of the 12)
- **Core thesis:** Every prospect moves through 6 emotional states between "no" and "yes." Sequential, can't skip. Amateur throws compelling elements at the page; professional maps the journey and places each element at its optimal emotional point. "The difference between 0.9% and 2.4% isn't talent. It's architecture."
- **Frameworks introduced:**
  - **6 Emotional States (in order — each requires the previous):**
    1. **Indifference** — "I don't care about this." (default starting state — scrolling, distracted, thinking about lunch)
    2. **Pain** — they feel the problem
    3. **Understanding** — they grasp the mechanism behind the problem
    4. **Hope** — they believe a solution to this problem exists
    5. **Belief** — they believe YOUR specific solution works
    6. **Desire** — they want it now
  - **The Chain Rule** (verbatim): "You can't make someone desire something they don't believe will work. You can't make them believe something works if they have no hope. You can't give them hope if they don't understand their problem. You can't make them understand their problem if they don't feel pain. You can't make them feel pain if they're indifferent. Every stage builds on the one before it."
- **Tactical moves:**
  - Map every component of your copy to which emotional state it serves
  - Identify gaps where no component serves a state → that's where prospects fall off
  - Order components so emotional sequence is enforced (no "throw proof before pain" mistakes)
- **Novel vs. our stack:** MASSIVE — this is the most structurally-integrable framework of the 12. Our `sales-letter-method` has a 12-component framework (Hook / Problem / Agitation / Mechanism / Solution / Social Proof / Offer / Guarantee / Bonus / Urgency / CTA / PS) — **we can MAP each component to one of the 6 emotional states** and have Phase 3 reviewers check state coverage + order. Same for 4-day email sequences: Day 1 = Indifference→Pain, Day 2 = Pain→Understanding→Hope, Day 3 = Belief, Day 4 = Desire→Action.
- **Quotable gold:**
  - > "You can write the most compelling copy in the world and still lose the sale if the emotional sequence is wrong."
  - > "Amateur Approach: Throw compelling elements at the page. Hope the reader sorts it out. Wonder why 'great copy' doesn't convert. Professional Approach: Map the emotional journey from skeptic to buyer. Place each element at its optimal emotional point."
  - > "The difference between 0.9% and 2.4% isn't talent. It's architecture."
- **Cross-links:** `sales-letter-method` (component-to-state mapping), `email-sequence` (per-email state targeting), `ad-concept-engine` (hook targets Indifference→Pain flip in <3 seconds).

---

#### Newsletter #36 — "Your Copy Is Leaking Money (Here's How To Plug the Leak)" (30 MIN)
- **URL:** https://www.copywriting.ai/p/objection-destroyer-claude-project-skill
- **Author:** Mark Masters | **Date:** 2025-12-01 | **Length:** **30 min**
- **Core thesis:** 6 objection categories × ~60 variations. Systematic pre-emptive handling throughout copy. One unhandled objection = leaking money.
- **Anchor case:** $997 product, unhandled price objection → 0.3% conversion, $23K wasted ad spend. 3-week rewrite with objection handling throughout → **3.2% conversion (10×)**. Same traffic, same offer, same price.
- **Frameworks introduced:**
  - **6 Objection Categories** (categories 1, 2, 3, 5 confirmed from preview + search; **4 and 6 FLAGGED for Phase 2 confirm — not surfaced in preview**):
    1. **Price** — "This costs too much." Variations: too expensive, can't afford, seen similar for less, price doesn't match value, wait until I have more money, vs. competitor, discount, wasted money, can't justify to spouse, payment plan still too much
        - Pre-emptive: price anchoring vs. higher alternatives, ROI calcs, cost-of-inaction framing, payment plan, daily/weekly equivalents, "investment vs. expense" reframe
    2. **Timing** — "Not right now." Variations: later, busy, after [event], think about it, more research, not ready, next month/quarter/year, too much on plate
        - Pre-emptive: future pacing cost of delay, "perfect timing" myth destruction, quick-start positioning, implementation timeline clarity, "waiting makes it harder" framing, immediate small win demo
    3. **Trust** — "How do I know this works?" Variations: who are you, is this a scam, too good to be true, been burned before
        - Pre-emptive: proof stacking (see #38), founder story, money-back guarantee, specificity
    4. **[TBD — likely Need/Fit: "this isn't for my situation"]** — to confirm in Phase 2 full-read
    5. **Authority** — "I can't decide alone." Variations: need to ask spouse/boss/partner/team/accountant/board, don't make purchasing decisions, need approval for this amount, stakeholder wouldn't approve
        - Pre-emptive: shareable summary creation, stakeholder objection anticipation, decision-maker benefits, "how to pitch this to your [stakeholder]" content, money-back guarantee for "permission" safety, testimonials from similar decision dynamics, ROI docs for approval
    6. **[TBD — likely Skepticism/Market-fit OR Urgency]** — to confirm in Phase 2 full-read
  - **Objection coverage matrix:** for each copy piece, 6 categories × "addressed | explicitly not applicable | LEAK"
- **Tactical moves:**
  - Map your current best copy against 6 categories — identify leaks
  - Build pre-emptive handlers into headline, body, FAQ, PS
  - For high-ticket: every category must be addressed
- **Novel vs. our stack:** Our `sales-letter-method` 12-component framework includes Objection Handling but doesn't enforce the 6-category matrix. Adding `objection-coverage-audit.md` as Phase 3 reviewer closes the leak. Also feeds `context-profile.json` — add explicit fields for each of the 6 objection categories during onboarding.
- **Quotable gold:**
  - > "Every prospect who landed on that page thought the same thing: 'Why is this so expensive?' And the copy gave them no answer. So they left."
  - > "One unhandled objection. $23K in wasted ad spend. Launch declared a failure."
- **Cross-links:** `sales-letter-method` Phase 3 reviewer; onboarding form enhancement to capture objections-per-category; `email-sequence` nurture emails map to specific objection categories.

---

#### Newsletter #35 — "The Copy Scout System Behind 25K Projects"
- **URL:** https://www.copywriting.ai/p/research-command-center-scout-system-claude-projects-skills
- **Author:** Mark Masters | **Date:** 2025-11-24 | **Length:** 16 min
- **Core thesis:** Research scattered across Google Docs / Excel / Notion / Apple Notes = hoarding. Research Command Center™ = one Claude Project with specialized scout custom instructions that turn scattered data into active field intelligence.
- **Anchor case:** $25K VSL project won by student who referenced 47 support tickets + review mining vs. competitor pitching "proven frameworks + 15 years experience." Client increased scope to $63K on the spot.
- **Frameworks introduced:**
  - **Research Command Center™** — dedicated Claude Project, project knowledge base includes:
    - Customer interview transcripts (word-for-word)
    - Survey results with raw response data
    - Competitor campaign teardowns
    - Sales call recordings (transcribed)
    - Review mining results (Amazon, G2, Trustpilot)
    - Support ticket patterns
    - Lost deal analysis reports
    - Industry trend reports
    - Swipe file of converting campaigns
    - Customer success stories with transformation language
  - **Scout Custom Instructions** (verbatim copyable, feeds into our `copywriting-os`):
    > You have access to comprehensive market research for copywriting projects. You are a scout gathering intelligence.
    > ALWAYS:
    > - Extract exact customer language from transcripts (verbatim quotes)
    > - Scout for patterns across multiple data sources
    > - Reference specific data points with numbers when making claims
    > - Address real objections using actual words from sales calls
    > - Use proven hooks from the swipe file with performance data
    > - Scout competitor territories for gaps and opportunities
    > - Ground all copy in actual field intelligence, not assumptions
    > - Identify emotional triggers competitors are missing
    > - Spot emerging trends before they become obvious
    > - Report opportunities with specific evidence and examples
    > - Connect disparate data points...
- **Tactical moves:**
  - Tagline "Handle 12 clients like you're handling one" — multi-client manager at scale
  - Don't re-hunt for research each write. Load once. Query many.
- **Novel vs. our stack:** We have `researcher` agent, `deep-research` skill, `scrapecreators`, `ad-library-scraper`, `source-of-truth` 26-section SoT, `avatar-research` 16-point breakdown — **but no unified Research Command Center custom instruction pattern** that binds the data sources into a scout-mode writing assistant. BIGGEST gap of the 12 newsletters relative to our stack.
- **Quotable gold:**
  - > "You're not using research. You're hoarding it."
  - > "Your clients aren't hiring you to only write. They're hiring you to figure out things their competitors don't."
  - > "One copywriter had scouts in the field. The other was guessing."
- **Cross-links:** Core of `copywriting-os` Pre-Write layer. Subsumes how `source-of-truth` + `avatar-research` + scraped assets get loaded into a client's copy-system folder.

### §3 Extraction schema (required fields per newsletter)

```
#### Newsletter <N>: <Title>
- URL: <direct link>
- Author: <name>
- Publish date: <YYYY-MM-DD>
- Word count: <approx>
- Core thesis (1 sentence):
- Frameworks introduced: [name + 1-line definition × N]
- Tactical moves (copy-and-paste plays): [<concrete instruction> × N]
- Copy examples cited: [<quote + why it works>]
- Novel ideas not already in our repo:
- Quotable gold (for SKILL.md quotes or training):
- Cross-links to existing skills/agents: <which of our existing skills this maps to>
- "Would beat most copywriters" insights:
```

## §4 Synthesis — Cross-newsletter patterns

### §4.A Consensus signals (repeated across 3+ newsletters)

1. **Channel existing desire, don't create it** — #42 Collier, Schwartz, #44 Halbert (coat of arms = channeling prep), #45 (category-speak fails because it doesn't meet reader where they are), #35 (scout customer language = channeling material)
2. **Write to ONE specific person, not a segment** — #44 Halbert One-Person Rule, #40 Voice Rules #1, #42 Collier "this specific person at 9pm Tuesday"
3. **Specificity over abstraction at every turn** — #38 Proof #5 Specificity, #45 Transform/category-speak fail, #40 Voice Rules ("getting more clients" not "scaling customer acquisition pipeline"), #44 Coat of Arms "not demographic" rule
4. **AI skills should be single-file, paste-and-go, 3-input max** — #40 both skills, #39 Headline Lab, #38 Proof Arsenal, #36 Objection Destroyer, #35 Scout System — Mark Masters's entire skill pattern
5. **Claude Projects as deployment unit** — 8 of 12 slugs end in `-claude-project-skill`. Project = knowledge base + custom instructions + query prompts. This is the productization pattern.
6. **Enforcement mechanisms > voice rules** — #44 "tell me who you imagined" is the canonical example. Mark reuses this pattern (state-coverage check, mechanism declaration, etc.). Without enforcement, the model nods and writes generic.
7. **Systems beat talent** — explicit quote in #37 ("architecture not talent") and #39 ("difference between amateurs and professionals isn't talent, it's systems"). Every framework is a SYSTEM, not a vibe.

### §4.B Contradictions (where taste decides)

1. **#41 Mark-vs-Peggy: Claude-first draft vs. Human-first + Claude edit layer** — head-to-head A/B test, verdict NOT surfaced in Phase 1 preview. **Open thread for Phase 2 full-read.** Likely conclusion: both work; choice depends on copy type + human skill level + research depth loaded. This becomes a `copy-workflow-router` decision in `copywriting-os`.
2. **Depth vs. speed** — #37 Emotion Engine is 32 min of deep architecture; #40 Two Skills has "3 inputs only, don't overwhelm." Both valid. Reconciled by: depth at the SYSTEM level (our skill architecture), speed at the USE level (the end-user asking for copy gets ≤3 questions).
3. **Breadth vs. intelligence** — #39 Headline Lab generates breadth (5 mechanisms × many formulas), #35 Scout System grounds every line in field data. Not contradictory — use both. Scout provides the "existing desire" inputs → Headline Lab generates the combinatorial outputs.

### §4.C Gaps vs. our current skill stack (what we're missing → Phase 2 build targets)

| Rank | Gap | Source newsletter(s) | Phase 2 action |
|------|-----|----------------------|----------------|
| 1 | **Research Command Center** custom-instruction pattern | #35 | New skill `research-command-center` OR prompt layer inside `copywriting-os` that wraps existing data sources |
| 2 | **Coat-of-Arms prompt-ready template** (our `buyer-profile.md` is richer data but not prompt-ready) | #44 | Add `coat-of-arms.md` generator that derives from `buyer-profile.md` + `context-profile.json` |
| 3 | **One-Person Rule enforcement mechanism** | #44 | `one-person-enforcement.md` prompt fragment loaded by every copy skill — forces model to declare "name / job / moment" at end of each write |
| 4 | **6 Emotional States → Sales-Letter-Method component mapping** | #37 | Tag each of the 12 sales-letter components with its emotional state; add Phase 3 reviewer `emotional-sequence-audit.md` |
| 5 | **6 Objection Categories coverage matrix** | #36 | New onboarding field (per category), Phase 3 reviewer `objection-coverage-audit.md`, email-sequence per-email objection targeting |
| 6 | **6 Proof Types + Proof Density metric** | #38 | Phase 3 reviewer `proof-density-audit.md`; onboarding field to inventory available proof per type; "every claim + proof type" rule in `copywriting` |
| 7 | **5 Headline Mechanisms as orthogonal axis** to our awareness × angle bank matrix | #39 | Upgrade `headline-bank` → awareness × angle × mechanism; enforce mechanism diversity in `big-angle-spotter` Step 10-12 outputs |
| 8 | **Channeling-vs-Creating pre-write gate** | Schwartz, #42 | Universal pre-write gate in `copywriting-os` — explicit "existing desire" field required before any write |
| 9 | **Element-by-element teardown reviewer** | #45 | New reviewer for `sales-letter-method` Phase 3: walks hero → lead → body → proof → CTA against named failure modes |
| 10 | **Copy Swipe Engine for non-ad copy** (we have ad swipe via `ad-library-scraper`, missing for sales letters / emails / landing pages) | #43 | New skill `copy-swipe-engine` — structured metadata + query prompts, mirrors ad-library-scraper architecture |
| 11 | **DWY single-file skill exports** | #40 | Post-Phase-2: extract `sales-letter-method-lite.md`, `landing-page.md`, `email-4-day.md`, etc. as claude.ai-uploadable single files |
| 12 | **Copy-workflow-router** (Claude-first vs. human-first + edit layer) | #41 | `copywriting-os` decision logic based on copy type + human skill + research loaded |

### §4.D Gold we already own (no rebuild, just cite/integrate)

| Existing asset | What it already does | Copy-OS integration |
|----------------|----------------------|---------------------|
| `sales-letter-method` 12-component framework | Long-form cold-traffic letter architecture | Map components to 6 emotional states; add 6-objection-category matrix; add proof-density + one-person-enforcement reviewers |
| `avatar-research` 16-point breakdown | Schwartz awareness + Top 5 Deep Fears + Raw Inner Dialogue + Desired Transformation + Relationship Impact | Already richer than Halbert coat of arms — generate coat-of-arms.md AS A DERIVATIVE |
| `source-of-truth` 26-section SoT | §5.5 Golden Nuggets, §5.7 ICP Language Analysis, §7.5 Misconceptions | Feeds Research Command Center scout knowledge base directly |
| `ad-library-scraper` SQLite + Ghost + Nemotron classifier | Per-industry ad swipe file with enrichment | Pattern to clone for `copy-swipe-engine` |
| `unslop` + Layer 1 de-AI | Domain-specific AI pattern avoidance | Generate new profile per copy domain (sales-letter, email, landing-page) seeded with teardown failure modes from #45 |
| `headline-bank` 5 awareness × 10 angle banks | 75+ headlines per mass desire | Add mechanism as 3rd axis |
| `big-angle-spotter` 12-step Opus→Sonnet pipeline | Produces 1 angle + 3 headlines + 3 ad prompts + 3 image prompts | Enforce mechanism diversity in Step 10-12 |
| `copy-editing` Sweep 8 (De-AI) | Multi-pass editing | Add Sweep 9 (channeling check) + Sweep 10 (one-person enforcement) + Sweep 11 (teardown stance) |
| `ad-concept-engine` 6-stage pipeline | DCT-aware ad concept | Already the model for how skill orchestration should work; `copywriting-os` borrows this structure |
| `buyer-profile.md` per client | Target buyer data | Source for auto-generated coat-of-arms.md |
| `voice/<person>/` V.O.I.C.E. files | Writer-level voice, stable across projects | Loaded by every copy skill (already works); now also source for one-person-rule anchor voice |

**Bottom line:** we already own 70% of the raw material. The copy-OS build is mostly **integration + enforcement layer + productization**, not greenfield skill building.

## §5 Proposed Architecture Sketch

> **⚠️ §5 SUPERSEDED BY §7.C — revised architecture is command-based, not skill-based.** The rest of §5 is preserved below as the original proposal (skill-based) for reference. Phase 2 implementation follows §7.C: `/copy` command + `.claude/references/copywriting-os/` fragments + context-mode sandbox for reference library + sub-agent delegation for heavy modules. Same benefits, none of the auto-skill system-prompt bleed.

### §5.A One-line integration story

> **`copywriting-os`** = the router + shared-context + enforcement layer that turns our existing 18 copywriting skills and 6 copy-related agents into a single coherent system. It asks "what copy do you need?", pre-loads the research + avatar + voice context once, picks the right domain module (sales letter / landing / email / ad / headline), runs universal pre-write gates (Channeling / Coat-of-Arms / One-Person), routes to the module, then runs universal post-write gates (Proof-Density / Emotional-Sequence / Objection-Coverage / Teardown / Voice / De-AI), and logs everything.

### §5.B Proposed skill structure — `skills/copywriting-os/`

```
skills/copywriting-os/
├── SKILL.md                            # Orchestrator + frontmatter + triggers
├── references/
│   ├── copy-domain-router.md          # Decision tree: which module for which output
│   ├── five-headline-mechanisms.md    # #39 Mark Masters
│   ├── six-proof-types.md             # #38 Mark Masters
│   ├── six-emotional-states.md        # #37 Mark Masters
│   ├── six-objection-categories.md    # #36 Mark Masters
│   ├── halbert-trio.md                # #44 A-pile + Coat of Arms + One-Person
│   ├── collier-principle.md           # #42 NOVA (1937)
│   ├── schwartz-channeling.md         # Schwartz post (Peggy)
│   ├── teardown-failure-modes.md      # #45 Peggy
│   ├── scout-mode-instructions.md     # #35 Mark Masters
│   └── dwy-single-file-pattern.md     # #40 single-file skill structure
├── prompts/
│   ├── copy-brief-template.md         # Shared input schema — one brief, all outputs
│   ├── channeling-check.md            # Pre-write gate (Schwartz/Collier)
│   ├── coat-of-arms-generator.md      # From buyer-profile.md → prompt-ready portrait
│   ├── one-person-enforcement.md      # Post-write forcing function
│   ├── proof-density-audit.md         # Phase-3 reviewer fragment
│   ├── emotional-sequence-audit.md    # Phase-3 reviewer fragment
│   ├── objection-coverage-audit.md    # Phase-3 reviewer fragment
│   └── teardown-reviewer.md           # Phase-3 reviewer fragment (element-by-element)
├── modules/                           # POINTERS to existing skills (not rewrites)
│   ├── sales-letter.md                # → delegates to skills/sales-letter-method
│   ├── landing-page.md                # → delegates to skills/copywriting (upgraded)
│   ├── email.md                       # → delegates to skills/email-sequence
│   ├── ad.md                          # → delegates to skills/ad-concept-engine
│   ├── headline.md                    # → delegates to skills/headline-bank (upgraded)
│   └── proof-element.md               # NEW integration layer (standalone proof blocks)
├── workflows/
│   ├── dfy-run.md                     # Done-for-you full run (default)
│   ├── dwy-run.md                     # Done-with-you (client in driver's seat)
│   └── workflow-router.md             # Claude-first vs human-first + edit layer (#41)
├── training/
│   ├── operator-quickstart.md         # For the person running the OS (Jerel or his team)
│   ├── trainee-first-project.md       # For a junior copywriter learning the system
│   └── dwy-client-onboarding.md       # For a client using the exported pack
├── learnings.md
└── corrections.md
```

### §5.C Orchestration flow (what happens when user triggers the OS)

```
1. TRIGGER: user says "I need a sales letter / email / ad / landing page" OR /copy
2. CONTEXT GATE: load clients/<slug>/context-profile.json + voice/<person>/* + copy-system/copy-brief.md
   ↓ if copy-brief.md missing, generate it from context-profile + buyer-profile + avatars (one-time)
3. DOMAIN ROUTER: ask "what output?" OR infer from the trigger verb
4. UNIVERSAL PRE-WRITE GATES (run in order — HITL on fail):
   a) Channeling Check — "what existing desire are we channeling?" (Schwartz/Collier)
   b) Coat-of-Arms — auto-generated from buyer-profile + avatars, human confirms specificity (Halbert)
   c) One-Person Seed — identify the specific reader (name / job / one-sentence moment)
5. WORKFLOW ROUTER (#41):
   - Claude-first-draft (Mark) if: copy type is structural + research is loaded deeply
   - Human-first + Claude-edit-layer (Peggy) if: client has strong voice + nuanced positioning + trainee operator
6. DOMAIN MODULE RUNS — existing skill does its pipeline (sales-letter-method Phase 0→4, email-sequence, etc.)
   - Pre-write gates already injected
   - Module's own internal reviewers + ours stack
7. UNIVERSAL POST-WRITE GATES (run in parallel — fail any → back to step 6):
   a) One-Person Enforcement — model must declare "name / job / moment" — if generic, reject (Halbert)
   b) Proof Density — every major claim has ≥1 of 6 proof types (#38)
   c) Emotional Sequence — 6 states covered in order without skips (#37)
   d) Objection Coverage — 6 categories addressed OR explicitly N/A (#36)
   e) Teardown Reviewer — element-by-element failure-mode check (#45)
   f) Existing: brand-voice-guardian + conversion-optimizer + unslop + copy-editing Sweep 8
8. OUTPUT + LEARNINGS — write to clients/<slug>/copy-system/outputs/<domain>/<date>-<name>.md
   - Append to quality-gates/ log files
   - Append per-skill learnings.md
   - Optional: feed back into copy-swipe-engine for future reference retrieval
```

### §5.D Client-side folder scaffold — `clients/_template/copy-system/`

```
clients/_template/copy-system/
├── README.md                          # What this folder does, one-page onboarding
├── copy-brief.md                      # Single shared brief read by every copy skill
├── coat-of-arms.md                    # Per-avatar (or per-audience) Halbert portrait
├── scout-instructions.md              # Per-client Research Command Center custom instructions
├── proof-inventory.md                 # Available proof cataloged by 6 types (#38)
├── objection-matrix.md                # 6 categories populated with client-specific variations (#36)
├── swipe-file/                        # Structured copy reference library (#43)
│   ├── sales-letters/
│   ├── emails/
│   ├── landing-pages/
│   ├── headlines/
│   └── ads -> ../../../swipe-files/<industry>   # Symlink to existing ad pool
├── outputs/                           # All generated copy lands here
│   ├── sales-letters/
│   ├── emails/
│   ├── landing-pages/
│   ├── ads/
│   └── headlines/
├── quality-gates/                     # Audit logs — one entry per write
│   ├── channeling-log.md              # Each write's Schwartz check outcome
│   ├── one-person-log.md              # Who the model imagined (Halbert enforcement)
│   ├── proof-density-reports.md
│   ├── emotional-sequence-reports.md
│   ├── objection-coverage-reports.md
│   └── teardown-reports.md
└── metrics.md                         # Per-output performance if shipped (conversion, opens, etc.)
```

### §5.E Integration with existing 6-stage creative pipeline

`copywriting-os` is **orthogonal** to the 6-stage pipeline — it feeds every stage where copy is produced:

- **Stage 1 Research** → `research-command-center` (new) subsumes `source-of-truth` + `avatar-research` + scraped social + scraped ads + transcribed testimonials. Outputs populate `copy-system/` foundation files.
- **Stage 2 Concept (Angle)** → `big-angle-spotter` stays, BUT gets mechanism-diversity enforcement in Step 10-12 (from #39).
- **Stage 3 Create** → image/video stays; ALL TEXT (headlines, primary copy, body) routes through `copywriting-os`.
- **Stage 5 Test** → `meta-ads-uploader` stays.
- **Stage 6 Feedback** → `feedback-router` stays; learnings now also flow to `copy-system/quality-gates/` and per-skill `learnings.md`.

### §5.F DFY vs. DWY path (open for both, same foundation)

- **DFY (Jerel's agency runs it):** operator triggers skills, client signs off at HITL gates. Delivery: polished copy files in `outputs/`.
- **DWY (sold as a product):** client buys the agent kit (single-file versions of top skills from #40 pattern) + onboarding training + `copy-system/` scaffold. They run it themselves with Claude Code. Quality gates force the enforcement mechanisms, so their output stays high even without Jerel's taste.
- **Shared foundation:** same `copy-system/` folder structure, same skill stack. DWY just removes Jerel-manual-overrides from HITL gates and adds self-serve training docs.

### §5.G Beats-most-copywriters thesis (the quality ceiling)

Why this system produces output that beats most copywriters:

1. **Research moat** — scout-mode custom instructions force every write to reference verbatim customer language, specific data points, and competitor gaps. Most copywriters write from assumption.
2. **Architecture** — emotional sequence (#37) + objection coverage (#36) + proof density (#38) guarantees structural completeness. Most copywriters miss at least one.
3. **Enforcement mechanisms** — one-person rule + channeling check + teardown reviewer catch the failure modes that ship in polished-looking copy. Most copywriters don't have post-write forcing functions.
4. **Specificity-by-default** — voice rules + unslop + copy-editing Sweep 8 strip abstraction. Most AI-assisted copy doesn't.
5. **Compounding asset** — every write adds to swipe-file + learnings + quality-gate logs → the next write is sharper. Most copywriters start from scratch each time.
6. **Human taste at the top** — Jerel's 20% (or trainee's taste after reps) fills the final variable. System does 80-90% so that 20% is spent on direction, not syntax.

## §6 Onboarding Form Rewrite Sketch

### §6.A Target

Cut the Fuggy's-Media-style 21-question / 14-section form down to **≤10 questions + 3 URL drops**, delivered in ≤15 minutes of client time, with Claude Code scraping everything else.

### §6.B Form v2 — DFY General Copywriting Service

**Section 1 — Identity (2 Qs, ~2 min)**
1. Contact name(s) + email(s)
2. Business Manager ID (only if running Meta ads)

**Section 2 — URL drops for Claude to scrape (3 inputs, ~2 min)**
3. **Primary website URL** → scraped for: offer, pricing, services, about, positioning, existing voice samples, testimonials embedded on site, logo + brand assets
4. **Social handles** (any you have — IG / TikTok / LinkedIn / YouTube / Facebook / X — comma-separated) → scraped for: top-performing content by engagement, voice samples, content pillars, posting cadence, audience language in comments
5. **Testimonial asset folder** (Google Drive URL, or "see website", or "none yet") → scraped for: video testimonials transcribed, written reviews, exact client language

**Section 3 — What Claude genuinely can't infer (5 required Qs + 1 optional, ~8 min)**
6. **Exact offer + pricing** (if not clear on site): the deliverable, price, guarantee, any bonuses, deadline
7. **Unique edge / proprietary framework** (what you do that competitors don't — with 1 real client example ideally)
8. **Sales process map** (first contact → closed deal, where prospects typically hesitate + the objection you're most nervous about)
9. **90-day goals** (primary outcome + success metric)
10. **Banned words / voice preferences** (anything you NEVER want to hear in marketing — or "no banned words")
11. *(Optional)* **"The one sentence"** — what you say in consultations that makes prospects lean in (if you have it, drop it; if not, skip)

**Total surface area:** 2 identity + 3 URL drops + 5 required + 1 optional = **10 questions max**, structurally 4 screens.

### §6.C Autofill pipeline (runs after submit, before human review)

Runs in parallel sub-agents (when rate limit permits) or sequential main-agent fallback:

| Source | Tool chain | Populates |
|--------|------------|-----------|
| Website (primary URL) | `ctx_fetch_and_index` (light) + `chrome-mcp` (auth-required sections, logo extraction via SVG + color + font) → `design-system` skill | `offer.md`, `icp.md`, `brand/` (logo + tokens), draft `buyer-profile.md` from testimonials |
| YouTube channel (3-5 recent + top-viewed videos) | `transcribe` (yt-dlp + Groq whisper-large-v3 per memory) → voice extraction → `brand-voice.md` update | `voice/<person>/` (if this is the founder's personal voice) or `brand-voice.md` (if brand voice) + `story-bank.md` (anecdotes) |
| Social profiles | `scrapecreators` (25+ platforms) → engagement-ranked top posts | `channels.json` (cadence + platforms), `story-bank.md` (content that worked), "content that already works" section |
| Testimonial folder | `transcribe` (videos) + `chrome-mcp` (web pages) → exact client language extraction | `buyer-profile.md` verbatim quotes, `proof-inventory.md` by 6 types |
| Google Reviews / G2 / Trustpilot (if applicable) | `chrome-mcp` scrape + language mining | `buyer-profile.md` quotes, `objection-matrix.md` inferred objections |
| Industry Meta Ad Library | `ad-library-scraper` (if industry pool not yet scraped, runs `/ads:scrape-library <industry>`) | `swipe-files/<industry>/` + Schwartz 5-stage sophistication brief |

### §6.D Human review gate (HITL)

After autofill pipeline completes:
1. Claude generates a **preview of the auto-filled `context-profile.json`** + all derived files
2. Presents as a checklist: "Here's what we found. Confirm, correct, or fill the blanks."
3. Human reviews section-by-section (10-15 min). Common corrections:
   - Pricing changes (site-listed price may be outdated)
   - Voice tweaks ("sound more casual / technical / warm")
   - Objection corrections (Claude often misses the 2-3 objections only heard in 1:1 calls)
   - Unique-edge precision (Claude can describe what you do; only you can articulate what's proprietary)
4. Missing fields trigger **≤5 targeted follow-up questions** (not a re-run of the whole form)
5. On approval → project state flips to "activated" and all downstream skills can be triggered

### §6.E Net impact

| Metric | v1 (current Fuggy's form) | v2 (Copy-OS General) |
|--------|---------------------------|----------------------|
| Questions asked | ~21 | ≤10 |
| Client time | 60–90 min | ≤15 min |
| Data richness | ~3-sentence answers per field | Full-text scraped content + structured extraction |
| Buyer-language verbatim quotes | 0–3 | 20–50 (from testimonials + reviews + social) |
| Competitor audit | 1 field listing names | Full Meta Ad Library pool + Schwartz brief |
| Voice samples | 1 "why you" paragraph | 3–5 full video transcripts + top social posts |
| Time-to-first-campaign | Days (manual enrichment) | Hours (autofill + HITL review) |

### §6.F DWY version (future, sold as product)

Same form structure. Client runs the autofill themselves via their own Claude Code + the exported skill pack. The HITL review becomes self-review. System forces the same quality gates, so output doesn't degrade without Jerel's taste — because the enforcement mechanisms (one-person, channeling, proof-density, emotional-sequence, objection-coverage, teardown) don't require taste to run, only a human to sign off.

---

## §7 Context-Bleed Viability Analysis (Jerel's question, 2026-04-24)

> "If we compress all of this into one scale, is it viable in the long run because of context bleed and whatever?"

Direct answer: **the naive build would bleed. The architecture I originally sketched in §5 needs one structural shift to be viable long-run. Here's the honest read.**

### §7.A What would bleed in a naive `skills/copywriting-os/` build

1. **Auto-activation cost:** Claude Code preloads SKILL.md frontmatter + description for every skill into the system prompt. A fat OS skill that references 47 newsletters + 11 framework docs + 7 gate prompts = system-prompt bloat even on sessions NOT using copy work.
2. **Per-invocation stacking:** when the OS triggers, naive flow loads: OS SKILL.md (~3K) + pre-write gates (~2K) + context-profile (~2K) + buyer-profile (~2K) + voice/*.md (~4K) + module SKILL.md (e.g. sales-letter-method ~8K) + coat-of-arms (~1K) = **~22K tokens before any writing**.
3. **Post-write compounding:** 4 reviewers in-thread (~8K combined) + draft output (~4K) + revision loop (~6K) = another **~18K**.
4. **Session drift:** multiple copy outputs per session (sales letter + emails + ads) share the baseline → 40K+ carried forward → compaction kicks in at 167K → state loss.
5. **47-newsletter reference library bloat:** if reference docs live as skill files, they either preload into context or get lazy-read but still hit the 2K line cap per read.

In a 200K window this is survivable for one output, **fragile for a multi-output session, dangerous for week-long client projects.**

### §7.B Architecture shift that eliminates the bleed

**Ship `copywriting-os` as a `/copy` command + `references/copywriting-os/` fragments, NOT as an auto-activating skill.**

| Layer | Naive build | Lean build |
|-------|-------------|------------|
| Trigger | Auto-activating skill (always in system prompt) | Explicit command `/copy` (zero weight when not invoked) |
| Reference library (47 newsletters + frameworks) | Skill files loaded on demand (still hit 2K-line cap) | **Context-mode sandbox index** — retrieved via `ctx_search` only when a gate needs a specific fact. Zero main-thread cost. |
| Copy-brief generation | Module re-reads context-profile + buyer-profile + avatars + voice every invocation | **Generate ONCE** → `clients/<slug>/copy-system/copy-brief.md` (~2K compressed). Modules read the brief, not the sources. |
| Module execution (sales-letter-method full pipeline, email-sequence, etc.) | In main thread → stacks skill body + pipeline state | **Sub-agent delegation** — module runs in fresh sub-agent context, returns only the output |
| Post-write reviewers (4 × ~2K) | In-thread, stacks | **Each reviewer fires as a sub-agent** (`verification-loops` pattern). Main thread never carries their bodies. |
| Iteration loop (draft → feedback → revise) | Main thread accumulates | Revisions done in sub-agent; main thread sees only the improved output |
| Multi-output session | Baseline carries forward | **Per-output context budget ≤10K.** After each output ships: write state → disk, compact. |
| Multi-client session | Clients stack | **One client per session.** Switching = fresh load. |

**Resulting per-invocation cost:** ~5-8K tokens (command execution layer + copy-brief + one-person-seed) + sub-agent work invisible to main thread. Session survives 5+ outputs before compaction.

### §7.C What we'd rewrite in §5 to reflect this

- Replace `skills/copywriting-os/SKILL.md` (auto-activating) → `commands/copy.md` (explicit router) + `commands/copy/<subcommand>.md` for each copy type
- Move `references/` and `prompts/` out of any skill and into `.claude/references/copywriting-os/` so they're pure lazy-load files
- Move heavy reference data (47 newsletter extractions, 6 emotional-state examples, coat-of-arms library) → **context-mode sandbox**, fetched via `ctx_search` at gate-run time only
- Modules stay as pointers (delegation by sub-agent invocation), not embeds
- Shared `copy-brief.md` is client-side disk state, not skill-embedded

**Net result:** the "OS" is a discipline + a set of files + a router command, not a heavy auto-skill. Long-run viable.

### §7.D Secondary viability risks + mitigations

1. **Skill drift** — as modules (sales-letter-method, email-sequence) evolve, the OS must stay in sync → solved by keeping modules as delegation targets, not rewrites. OS doesn't version-lock modules.
2. **Reference staleness** — 47 newsletters today, more next month → `ctx_fetch_and_index` re-run on a cron; sitemap delta detection → auto-index new posts.
3. **Multi-user conflict** (DWY buyers) — every DWY user has their own disk state; no shared server-side resources until we explicitly build them.
4. **Sub-agent rate limits** (what hit us this session) — when sub-agents unavailable, main-thread fallback uses context-mode + compaction checkpoints. Already proven works (this session is the test case).

### §7.E Bottom line

- **Viable long-run: YES** — but ship as command + references + sandbox + sub-agent delegation, not as a fat auto-skill.
- **Alternative: build NO umbrella** — put enforcement gates directly inside each existing skill. Lighter but loses DWY productization story + cross-copy context sharing + single-entry-point UX.
- **Recommendation:** take the command-based architecture. It's the lean version of §5 with the same benefits and none of the system-prompt bleed risk. I'll reflect this shift in §5 before Phase 2 starts.

---

## §8 Open decisions for Jerel before Phase 2

Triggered by this session's course-corrections:

1. **Phase 1.5 — deep-read remaining 35 newsletters?** (see §1.C + §1.D priority list) — YES (full coverage before build) / PARTIAL (top 10 priority only) / NO (proceed with 12, loop back later as enrichment)
2. **Architecture shift (§7.C) — command-based `copy` + references + sandbox, instead of auto-skill?** YES / NO / discuss
3. **Phase 2 sequencing** (already from previous handoff) — all 10 subphases at once / phased / 2.1-2.6 first then pause
4. **NeezaNizam dogfood** (already from previous handoff) — 2.10 end / 2.5 integration test
5. **Phase 4 gap-fills** (already from previous handoff) — before Phase 2 / after
