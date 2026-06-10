---
name: source-of-truth
version: "1.0.0"
brand: AgentKits Marketing by AityTech
category: foundation
difficulty: advanced
description: "Generate paid ads source-of-truth: 26 core sections + 2 Ferres research-flow sections (§27 says-vs-addresses gap analysis, §28 competitor opportunity matrix). Auto-triage input, parallel research (scrapecreators, buyer-language, deep-research, product), synthesize via business-profile/avatar-research/ab-test. 4 checkpoints. Output: md + 5 derivatives for downstream skills."
triggers:
  - source of truth
  - paid ads source of truth
  - ads source of truth
  - ads strategy doc
  - paid ads brief
  - 26 section doc
  - paid ads sot
  - sot doc
  - ads sot
  - "/ads:source-of-truth"
prerequisites:
  - paid-advertising
related_skills:
  - business-profile
  - avatar-research
  - ad-concept-engine
  - offer-builder
  - scrapecreators
  - deep-research
  - paid-media-audit
  - marketing-psychology
  - ab-test-setup
agents:
  - researcher
  - persona-builder
  - brainstormer
  - brand-voice-guardian
mcp_integrations:
  optional:
    - scrapecreators
    - dataforseo
    - linkup
    - meta-ads
success_metrics:
  - completeness_26_sections
  - research_source_diversity
  - downstream_consumption_rate
  - strategic_checkpoint_alignment
  - buyer_language_verbatim_count
output_schema: source-of-truth-v1
---

# Source of Truth — Paid Ads Strategic Document

> Generates the complete paid ads source-of-truth for any client, product URL, or idea: the 26-section spine plus §27 (says-vs-addresses gap analysis) and §28 (competitor opportunity matrix) from the Ferres research flow. Self-triages input, runs parallel research, synthesises every section from real buyer language (not guesses), and asks only the 4 strategic decisions humans must make. Single artifact (`source-of-truth.md`) + 5 derivative files for downstream consumption.

## Graph Links

- Feeds into: `[[avatar-research]]`, `[[ad-concept-engine]]`, `[[meta-ads-uploader]]`, `[[campaign-runner]]`, `[[ab-test-setup]]`
- Draws from: `[[business-profile]]`, `[[offer-builder]]`, `[[scrapecreators]]`, `[[deep-research]]`, `[[paid-media-audit]]`, `[[marketing-psychology]]`
- Used by agents: `[[researcher]]`, `[[persona-builder]]`, `[[brainstormer]]`, `[[brand-voice-guardian]]`
- Related: `[[paid-advertising]]`, `[[copywriting]]`, `[[content-moat]]`, `[[unslop]]`

## When to Use This Skill

- New client onboarding where paid ads are in scope
- Existing client launching a new product, offer, or audience segment
- Ad performance has plateaued and messaging needs a refresh from real buyer research
- A product URL exists but no client file structure has been built yet
- A founder pitches an idea and wants the paid-ads strategic doc before writing a single ad
- User says "source of truth", "ads strategy doc", "paid ads brief", "26-section doc", "paid ads SOT"
- Command: `/ads:source-of-truth [url | description | client-name]`

## Operating Modes

The skill self-triages on input type. No mode flags — the input itself disambiguates.

### Mode A — Existing Project
- **Input:** client/project slug (e.g. `propwise-sg`, `neezanizam`)
- **Detected by:** input matches a directory under `clients/`
- **Foundation load:** `clients/<project>/context-profile.json`, `icp.md`, `offer.md`, `buyer-profile.md`, `brand-voice.md`, `learnings.md`
- **Behavior:** skips foundation intake, goes straight to research + synthesis
- **Refresh check:** if `clients/<project>/source-of-truth.md` exists and is <90 days old, offer refresh / extend / skip

### Mode B — Product URL
- **Input:** URL (e.g. `https://acmecorp.com/pricing`)
- **Detected by:** input starts with `http://` or `https://`
- **Foundation load:** WebFetch the URL + dev-browser scrape (pricing page, testimonials, claims, FAQs)
- **Behavior:** asks 5-7 minimum questions to fill what scraping cannot determine (KPI, target market segment, price tier confirmation, current ad state, brand constraints)
- **Project slug:** derived from domain or asked

### Mode C — Description / Idea
- **Input:** free-text description (e.g. `"an AI scheduling tool for SG property agents"`)
- **Detected by:** input is neither a known project slug nor a URL
- **Foundation load:** none — pure idea
- **Behavior:** asks 5-7 minimum questions, then spawns research from the description alone
- **Project slug:** asked or auto-suggested from description

If input is ambiguous (e.g. could be a slug or a description), use AskUserQuestion to disambiguate before proceeding.

## Process: 5 Phases + 1 HITL Gate

### Phase 0: Context Gate + Triage

**Role:** Orchestrator (main context)

1. **Marketing CLAUDE.md Context Gate** — detect WHO (voice profile) and WHAT PROJECT.
   - Load `voice/<person>/` files if a voice profile is established for the session.
   - If no project established and Mode A input given, set project from input.
2. **Triage** input type → Mode A, B, or C (rules above).
3. **ASK about onboarding artifacts BEFORE spawning research** (learned 260417, neezanizam run):
   - Before Phase 2 research starts, ALWAYS ask the user: "Do you have any onboarding form responses, intake PDFs, business-profile documents, or founder-interview transcripts for this client?"
   - If yes → read + structure into `clients/<project>/context-profile.json` FIRST (if not already present)
   - This prevents re-running expensive research (buyer-language-researcher, deep-research) on assumptions that the founder has already answered in their own words
   - Onboarding artifacts typically validate 30-60% of §5 Buyer Profile + §6 Pain + §7 Objections + §8 Proof — without them, the skill fabricates what the founder could have told us directly
4. **Mode A freshness check:**
   - If `clients/<project>/source-of-truth.md` exists, read its first 50 lines to determine date and offer refresh / extend / skip via AskUserQuestion.
   - If `context-profile.json` missing in Mode A, check step 3 BEFORE warning — onboarding artifacts may fill this gap. Only warn if step 3 returns nothing.
5. **Determine project slug** for all output paths.
6. **Industry pool check** — read `clients/<project>/context-profile.json` for the industry slug (e.g. `property-sg`). If `swipe-files/<industry>/stage-analysis.md` exists, **load it as the canonical strategic brief BEFORE Phase 2 research** — it shapes which competitors and angles Phase 2 needs to dig deeper on, and prevents re-discovery of stage / mechanism / blue-box findings already validated industry-wide. If missing, surface to user: "No industry stage-analysis exists for `<industry>` — recommend running `/ads:scrape-library <industry>` first; proceeding without it now."

### Phase 1: Foundation Intake (Mode B/C only)

**Role:** Orchestrator + AskUserQuestion (single batched call, 5-7 questions)

For Mode B and Mode C ONLY. In Mode A, skip this phase entirely.

Ask the minimum 5-7 questions defined in `references/triage-questions.md`. These cover only what research cannot determine on its own:
- Primary conversion goal (purchase / lead / application / call / signup / trial)
- Target market segment / ICP focus
- Price point / AOV (confirm if scraped, ask if Mode C)
- Current ad state (no ads yet / running paid / failed previous launch / scaling existing)
- Brand constraints (compliance area, claims that cannot be made, words to avoid)
- (Mode C only) Primary platform focus (Meta / Google / TikTok / LinkedIn)
- (Mode C only) Brand assets that already exist (testimonials, founder credibility, demo footage)

Save answers to `clients/<project>/source-of-truth-intake.json` for traceability.

### Phase 2: Parallel Research Pipeline

**Role:** Orchestrator → spawns 4-5 sub-agents/skills in ONE message (parallel)

Critical: spawn all of these in a single message with parallel tool calls. Do NOT serialise.

1. **`scrapecreators`** skill → competitor ads from Meta Ad Library + TikTok Creative Center
   - Targets: top 5-10 competitors in category (provided in Phase 1 OR inferred from product description)
   - Output: `clients/<project>/competitor-ads/raw.json`

2. **`buyer-language-researcher`** agent (at `~/.claude/agents/buyer-language-researcher.md`)
   - Pulls Reddit threads, NotebookLM corpora, social sentiment, Instagram comments, TikTok comments
   - Goal: verbatim buyer phrasings — how they describe the problem, what they've tried, what they're tired of, what they want, why they hesitate
   - Output: `clients/<project>/research/buyer-language-dossier.md`

3. **`deep-research`** skill → market sentiment + awareness/sophistication mapping
   - MECE decomposition: market state, competitor positioning, Schwartz awareness distribution, sophistication level (1-5)
   - Output: `clients/<project>/research/market-research.md`

4. **WebFetch** (Mode B only) → product page deep scrape
   - Targets: pricing page, testimonials page, FAQ, About, any case studies linked
   - Output: `clients/<project>/research/product-snapshot.md`

5. **`paid-media-audit`** skill (conditional — only if `clients/<project>/.meta-ad-account-id` exists)
   - Pulls existing account performance, top-performing creatives, fatigue signals
   - Feeds Section 8 (Proof Inventory) and Section 18 (Performance Feedback Loop)

**Cost optimisation:** for sub-agent synthesis where Claude-quality is overkill (e.g. transcribing Reddit quotes, summarising competitor landing pages), use `scripts/research-llm.sh kilo "<prompt>"` to route to MiniMax M2.5 / Nemotron 3 Super via Kilo Gateway.

**Target completion:** 5-10 minutes for all parallel research.

**Failure handling:** if any single research source fails, continue with the others. Mark missing sections as "⚠️ NOT AVAILABLE — [source] unavailable" rather than fabricating. NEVER hallucinate buyer quotes — if buyer-language-researcher returns thin results, flag the section.

### Phase 3: Section-by-Section Synthesis

**Role:** Orchestrator (with `references/section-synthesis-frameworks.md` loaded)

Synthesise each of the 26 sections per the frameworks. Reuses existing skill frameworks (no duplication):

| Sections | Source / Framework |
|---|---|
| §1 Brand Snapshot | `business-profile` JSON schema fields |
| §2 Paid Media Objective | `paid-advertising` skill knowledge + Phase 1 intake |
| §3 Product/Offer | `offer-builder` framework + WebFetch/intake |
| §4 Audience Profile | `marketing-psychology` Schwartz model + buyer-language dossier |
| §5 Buyer Profile (14 dims) | `avatar-research` Phase 1.5 sales-copy extraction framework, applied to research dossiers |
| §6 Pain Points | distill from buyer-language-dossier — rank by frequency |
| §7 Objections | distill from dossier + competitor-ads (objections their ads attempt to handle) |
| §8 Proof Assets | inventory from product-snapshot + (if exists) paid-media-audit data |
| §9 Messaging Hierarchy | **net-new** — synthesise core + supporting messages from §1-8 |
| §10 Ad Angles | **net-new** — combine buyer language + competitor swipe inspiration |
| §11 Hook Library | **net-new** — generate per-angle hooks using `marketing-psychology` mental models |
| §12-15 Formats/Scripts/Visuals/CTAs | **static reference** — load from `paid-advertising` + `ad-concept-engine` knowledge |
| §16 Testing Framework | `ab-test-setup` framework + research-driven priority recommendations |
| §17 Iteration Rules | `ab-test-setup` decision matrix |
| §18 Performance Feedback Loop | `paid-media-audit` patterns + (if exists) account data |
| §19 Asset Request Checklist | static reference — flag gaps based on what research found vs. didn't |
| §20 AI Prompt for Creative | reusable prompt template referencing this doc's outputs |
| §21 Script QA Checklist | `ad-concept-engine` references/headline-validation-checklist.md |
| §22 Strategy Summary | one-page synthesis of §1-21 |
| §23 Quick-Start Fill | minimum-viable extract for fast handoff |
| §24 Recommended Workflow | static reference (process map) |
| §25 Naming Convention | static reference |
| §26 Final Notes | living-doc reminder + version stamp |
| §27 Says-vs-Addresses Gap Analysis | **net-new** — buyer verbatim (§5/§6) cross-checked against the client's live messaging (sales page, current ad scripts, landing headlines); table the gaps. Source: `_shared-knowledge/ferres/02-research-flow.md` prompt 1 (ICP Deep Dive gap analysis). |
| §28 Competitor Opportunity Matrix | **net-new** — per-competitor profiles + saturation + blue-box/blue-ocean/weak-proof/unmarketed-advantage matrix + differentiation strategy. Built from §7 + competitor-ads research + competitor review mining; reuse `stage-analysis.md` blue boxes/gaps if present. Source: `_shared-knowledge/ferres/02-research-flow.md` prompt 2 (Competitor Analysis opportunity matrix). |

**Strategic sections (§2 KPI, §9 Core Message, §10 Top 3 Angles, §16 First Variable to Test) are DRAFTED here but NOT finalised** — they go to the HITL gate next. The skill drafts 2-3 options for each so the user can pick rather than freehand.

### Phase 4: HITL Gate — Strategic Checkpoint

**Role:** Orchestrator + AskUserQuestion (1 batched call with 4 multi-select/single-select questions)

Surface ONLY the 4 strategic decisions only humans should make. See `references/checkpoint-questions.md` for the question library and answer-mapping logic.

1. **§2 Primary KPI** — single-select: CPA / ROAS / CPL / MER / CAC payback
2. **§9 Core Message** — single-select between 3 drafted message hierarchies (with previews)
3. **§10 Priority Angles** — multi-select 3 of 6-8 drafted angles to test first
4. **§16 First Variable** — single-select: hook / angle / proof / format / CTA / offer

User answers → finalise the 4 sections in the in-memory draft → proceed to write.

### Phase 5: Write + Hand-off

**Role:** Orchestrator

1. **Write the consolidated artifact:**
   - `clients/<project>/source-of-truth.md` — full 26-section doc, single artifact for client deliverables and team alignment

2. **Write the derivative files** (so downstream skills don't parse the big doc):
   - `clients/<project>/01_research/output/<YYMMDD>-audience-insights-synthesis.md` — clean audience synthesis from pain points, failed solutions, desired outcomes, objections, misconceptions, golden nuggets, language notes, and Reddit/forum/review quotes
   - `clients/<project>/pain-objection-proof.md` — ranked tables from §6, §7, §8
   - `clients/<project>/swipe-file-buyers.md` — competitor ads filtered for buyer-side angles (the file `ad-concept-engine` already reads)
   - `clients/<project>/swipe-file-sellers.md` — competitor ads filtered for seller-side angles (same)
   - `clients/<project>/angles/` folder (built upon SoT, iterates wave-by-wave — see "Angles folder bootstrap" below)
     - `README.md` — explains the build-upon contract
     - `wave-1.md` — current wave's priority angles + 10 hooks each
     - `wave-2.md` — reserved angles
     - `hook-library.md` — master append-only hook bank + anti-pattern log
     - `iteration-log.md` — wave-by-wave changes
   - **NO `messaging-hierarchy.md` derivative** — core message + supporting messages live inline in SoT §9 (single source, no drift)
   - **NO `angles-hooks-library.md` root file** — replaced by `angles/` folder for wave stability (260418 architecture decision)

   **Angles folder bootstrap rule:** at SoT first generation, populate `angles/wave-1.md` from §10/§11 of the synthesized doc. Then strip §10 to a pointer block (3-line "moved to angles/" reference) and §11 likewise. SoT keeps §10/§11 as section anchors but the content lives in the angles folder.

3. **Write traceability artifacts:**
   - `clients/<project>/research/_manifest.json` — list of sources used + timestamps + record counts
   - Append to `clients/<project>/learnings.md`: `- YYMMDD | source-of-truth.md generated | research sources: [list] | strategic decisions: [§2, §9, §10, §16 chosen]`

4. **Hand-off message:**
   ```
   ✓ Source of truth complete: clients/<project>/source-of-truth.md (26 sections, [N] verbatim buyer quotes, [N] competitor swipes)

   Derivative files written for downstream consumption:
     - 01_research/output/<YYMMDD>-audience-insights-synthesis.md
     - pain-objection-proof.md
     - swipe-file-buyers.md / swipe-file-sellers.md
     - angles/ folder (README + wave-1.md + wave-2.md + hook-library.md + iteration-log.md)

   Suggested next steps:
     1. /ads:avatars <project>     → build 3+ DCT avatars from this
     2. /ads:concepts <project>    → generate DCT batches (3 creatives × 2 headlines × 2 copies per angle)
     3. /test:ab-setup             → design first DCT split test using §16 priority
   ```

## Language & Quality Standards

- **UK English** spelling throughout (analyse, recognised, colour, centre)
- **Verbatim buyer quotes** — preserve exact source phrasing in §4-7. Never paraphrase. Use blockquote format with source attribution: `> "I just want to know if I can afford this without doing the math myself" — r/singaporefi, 2025-12-08`
- **Brand-voice compliance** against `clients/<project>/brand-voice.md` (voice applies to skill-generated synthesis, NOT to verbatim buyer quotes)
- **Anti-AI slop check** via `skills/copy-editing/references/overused-ai-patterns.md` and (if exists) `skills/unslop/profiles/<domain>.md`
- **Data reliability rule** (Marketing CLAUDE.md): if research returns no data for a section, mark `⚠️ NOT AVAILABLE — [reason]` instead of fabricating. NEVER invent buyer quotes, statistics, or competitor data.
- **Cultural sensitivity** for SG-focused work: load `skills/ad-concept-engine/references/sg-cultural-guidelines.md` if project is SG-based

## Reference Files

- `references/26-section-template.md` — full 26-section markdown template (the skeleton this skill fills)
- `references/section-synthesis-frameworks.md` — section-by-section instructions for converting research data into doc content
- `references/triage-questions.md` — Phase 1 minimum question library for Mode B/C
- `references/research-pipeline.md` — Phase 2 parallel orchestration playbook with exact agent/skill prompts
- `references/checkpoint-questions.md` — Phase 4 strategic HITL question library + AskUserQuestion payload templates
- `references/derivative-file-templates.md` — Phase 5 templates for the 5 derivative files
- `references/audience-insights-synthesis-template.md` — clean audience synthesis from structured research fields and Reddit/forum/review quotes
- `references/buyer-language-extraction.md` — verbatim-quote handling rules + source-attribution format

## Self-Annealing

Per Marketing CLAUDE.md:
- Log corrections to `corrections.md` after every session correction (`- YYMMDD | what was wrong → what was right | context`)
- Promote 3+ repeating corrections to `learnings.md` during `/ops:weekly`
- If a section synthesis framework consistently produces output the user rewrites, update `references/section-synthesis-frameworks.md` for that section

## Open Questions / Limitations (v1.0.0)

- **Meta Ad Library scraping** depends on `scrapecreators` API coverage. For very niche categories or smaller brands, swipe file may be thin — flag rather than fabricate.
- **Mode A refresh** does not yet diff old vs new buyer language; full refresh overwrites. Future v1.1: surface what changed.
- **No web UI checkpoint** — the 4 HITL questions are CLI/AskUserQuestion only. For client-facing review of the doc, export step (PDF) is not built in v1.

<!-- skill-graph:start -->

## Related
<!-- auto-generated by scripts/link-skills.py — do not edit by hand -->

- [[business-profile]] (skill, 0.12)

<!-- skill-graph:end -->
