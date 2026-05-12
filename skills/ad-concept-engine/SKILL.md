---
name: ad-concept-engine
version: "2.0.0"
brand: AgentKits Marketing by AityTech
preferred_invocation: /copy:ad  # wraps this skill with copywriting-OS gates + reviewers + mechanism-diversity (see .claude/references/copywriting-os/)
category: content
difficulty: advanced
description: "DCT-aware ad concept pipeline. Generates per-avatar advertising angles, assembles complete DCT batches (3 creatives x 2 headlines x 2 ad copies = 12 Meta combinations per batch), and compiles a DCT tracker. Supports multiple visual styles per batch (realistic, text-only, claymation, Pixar, UGC, etc.) with standalone text-on-image hooks. Backward compatible with single-persona mode."
triggers:
  - ad concepts
  - new ad angles
  - ad concept engine
  - generate ad ideas
  - fresh ad creative
  - ad brainstorm
  - Meta ad concepts
  - ads concepts
  - DCT
  - dynamic creative testing
prerequisites:
  - paid-advertising
related_skills:
  - avatar-research
  - copywriting
  - marketing-psychology
  - content-moat
  - image-generation
  - paid-advertising
  - unslop
  - copy-editing
  - multi-agent-consensus
  - scrapecreators
  - deep-research
agents:
  - brainstormer
  - copywriter
  - brand-voice-guardian
  - conversion-optimizer
  - researcher
mcp_integrations:
  optional:
    - scrapecreators
success_metrics:
  - angle_novelty_rate
  - headline_ctr
  - ad_engagement_rate
  - dct_winning_combination_rate
output_schema: dct-batches
---

# Ad Concept Engine v2.0 — DCT Mode

> Generate per-avatar ad angles, assemble complete DCT batches, and compile a tracker for Meta dynamic creative testing. Each batch = 3 creatives x 2 headlines x 2 ad copies = 12 combinations Meta tests automatically.

## Graph Links

- Feeds into: `[[image-generation]]`, `[[video-factory]]`, `[[meta-ads-uploader]]`, `[[campaign-runner]]`
- Draws from: `[[avatar-research]]`, `[[marketing-psychology]]`, `[[content-moat]]`, `[[copywriting]]`, `[[paid-advertising]]`
- Used by agents: `[[brainstormer]]`, `[[copywriter]]`, `[[brand-voice-guardian]]`, `[[researcher]]`
- Related: `[[paid-media-audit]]`, `[[ab-test-setup]]`, `[[multi-agent-consensus]]`

## When to Use This Skill

- Client needs fresh ad concepts organized for Meta DCT testing
- Multiple avatars need distinct creative per audience segment
- User says "ad concepts," "DCT," "dynamic creative testing," "ad brainstorm"
- Command: `/ads:concepts [project]`

## Phase 0 — Delegate to Big-Angle-Spotter (v3.0 orchestrator mode)

**This skill NO LONGER generates angles or static hooks directly.** Those are delegated to the `big-angle-spotter` skill (`skills/big-angle-spotter/`, symlinked to `~/AI workflows/big-angle-spotter/`). Ad-concept-engine is now the orchestrator that:

1. **Loops big-angle-spotter N times** across avatars (sequential, not parallel — see "Multi-angle orchestration" below)
2. **Cross-pollinates EXISTING_ANGLES** so each successive run knows the prior winners and picks something different
3. **Wraps outputs into Meta hierarchy** per the new naming spec
4. **Retains Phase 2b video briefs** (UGC/Founder/VSL/Demo — those don't come from big-angle-spotter)
5. **Routes image prompts** from big-angle-spotter step 12 → image-generation for actual PNG rendering
6. **Writes dct-tracker + sheet** under new folder structure

### Multi-angle orchestration (sequential, EXISTING_ANGLES cross-pollinated)

Per wave target `N` angles. For each angle `i` in `1..N`:

```
1. Build EXISTING_ANGLES_i = saturated_angles (from learnings.md + iteration-log.md)
                          + [winning_angle_1, ..., winning_angle_{i-1}]
2. Pick target avatar for angle i (round-robin or per wave spec)
3. Write inputs.json with:
     OFFER, COMPANY (from context-profile.json)
     PERSONA (from avatars/avatar-<N>.md)
     INDUSTRY (from context-profile.json)
     EXISTING_ANGLES = EXISTING_ANGLES_i
     PRODUCT_IMAGE_REFS = clients/<slug>/brand/ assets (optional)
4. Invoke: python3 ~/AI\ workflows/big-angle-spotter/scripts/run_pipeline.py \
             --inputs ./inputs.json \
             --locked-angle "<approved Big Idea claim/headline>" \
             --headline-count 25 \
             --run-dir clients/<slug>/angles/big-angle-spotter/wave-<N>/angle-<i>/
   Notes:
   - `--locked-angle` skips steps 1-6 (angle generation + gates) because the angle
     was pre-selected by upstream avatar-fit scoring against the Big Ideas pool.
     Pipeline enters at step 7 (expansion).
   - `--headline-count 25` widens step 8's headline pool for more breadth (Option-C
     headline-scale integration). Step 9 ranks all 25; step 10b extracts top-3
     unchanged.
5. Parse 10b_top_3.json → capture top 3 headlines
6. Parse 07_expansion.md → capture winning angle name + rationale
7. Capture 3 ad prompts (11_*.md) + 3 image prompts (12_*.md)
8. Append winning_angle_i to EXISTING_ANGLES state for next iteration
```

**Parallel is broken** — step 3 of big-angle-spotter prunes candidates against EXISTING_ANGLES. Parallel workers each see the same list → all three can pick the same angle. Sequential with incremental update is the only safe pattern.

**Wall-clock:** ~4 min per angle × N angles. For a 3-angle wave: ~12 min.

### Meta hierarchy mapping (post-big-angle-spotter)

| big-angle-spotter output | Meta concept | Folder / field |
|---|---|---|
| 1 pipeline run | Ad Set | `campaigns/<metrics-campaign>/<campaign-name>/<adset-name>/` |
| Top angle name | Ad Set name component | `Broad_None_<AngleShort>_<budget>` |
| 3 ranked headlines + 3 ad prompts + 3 image prompts | 3 Ads | `ads/YYMMDD_<AngleShort>_S1.json`, `..._S2.json`, `..._S3.json` |

Campaign naming: `[Objective]_[Test|Scale]_[Theme]_[MonYY]` → e.g. `CBO_Test_BuyerComfort_Apr26` (from wave spec in `angles/wave-<N>.md`).

### What big-angle-spotter does NOT produce (still ad-concept-engine's job)

- **Video briefs (Phase 2b)** — UGC / Founder / VSL / Demo 6-scene breakdowns. Big-angle-spotter only does statics. If the wave calls for video, ad-concept-engine generates the video brief for the winning angle using `references/video-brief-template.md`.
- **Sub-trigger variants** — e.g. divorce / widow / inheritance spin-offs of the same angle. Big-angle-spotter picks one angle frame; ad-concept-engine can fan out sub-triggers as additional Ad Sets within the same Campaign if the wave spec requires it.
- **Alternate copy variants** — if you need 2+ ad copy bodies per Ad (beyond the one big-angle-spotter produces), pull from `headline-bank` reservoir or generate fresh using `copywriting` skill.

## Operating Modes

**v3.0 Orchestrator Mode (default, post-integration):**
- Delegates all angle + static hook generation to big-angle-spotter
- Loops N times with EXISTING_ANGLES cross-pollination
- Retains Phase 2b video briefs
- Writes under new Meta hierarchy

**Legacy Mode (backward compatible, v2.0 behavior — use when big-angle-spotter unavailable):**
- Detects `clients/<project>/avatars/` directory → generates angles per avatar
- Assembles full DCT batches, Phase 2a hooks inline
- Outputs DCT tracker under old `campaigns/dct-<date>/` structure
- Kept for projects that haven't migrated yet

## Language & Quality Standards

- UK English spelling throughout (analyse, recognised, colour, centre)
- All headlines pass validation checklist (`references/headline-validation-checklist.md`)
- All angles pass scoring rubric (`references/angle-scoring-rubric.md`)
- Cultural sensitivity rules apply (`references/sg-cultural-guidelines.md`)
- Brand-voice compliance against `clients/<project>/brand-voice.md`
- Anti-AI slop check against `skills/copy-editing/references/overused-ai-patterns.md`

---

## DCT Batch Structure

Each DCT batch contains:

| Component | Count | Lives Where | Rule |
|-----------|-------|-------------|------|
| **Creatives** | 3 | Image files (generated) | Each a DIFFERENT visual style. Text on image = standalone visual hook, NOT the Meta headline |
| **Headlines** | 2 | Meta Ads Manager headline field | Different hooks for the same angle. Max ~40 chars |
| **Ad Copies** | 2 | Meta Ads Manager primary text field | Different frameworks (PAS, story, data-led, contrarian, testimonial, etc.) |

Meta mixes all combinations: 3 x 2 x 2 = **12 combinations per batch**.

**Visual style variety** (no two creatives in a batch share a style):
- Realistic photography (UGC selfie, editorial, documentary)
- Text-only bold graphic (dark background, large typography)
- 3D / Claymation / Pixar-style illustration
- Split-screen before/after
- Infographic / data overlay on photo
- Screenshot / WhatsApp / social media post aesthetic

**Text-on-image hooks:**
- Short, punchy, scroll-stopping (2-8 words)
- Works as standalone visual communication even without reading Meta text fields
- DIFFERENT from both the Meta headline and primary text
- One unique hook per creative

---

## Process: 5 Phases + 5 HITL Gates

### Phase 0: Context Load + Avatar Detection

**Role:** Orchestrator (main context)

1. Load client context files:
   - `clients/<project>/buyer-profile.md`
   - `clients/<project>/offer.md`
   - `clients/<project>/brand-voice.md`
   - `clients/<project>/icp.md`
   - `clients/<project>/story-bank.md`

2. Check for avatars:
   - If `clients/<project>/avatars/` exists → load `_index.md`, enter DCT mode
   - If not → offer to run `/ads:avatars` first, or proceed in Legacy mode

3. **NotebookLM context enrichment (2nd-pass validation):**

   a. **General marketing notebook** (client-agnostic — apply to ALL projects):
      Query `notebooklm use 1644f7b5` then ask targeted questions to validate angles and creative strategy against Schwartz's full framework (awareness + sophistication + intensification/gradualization/mechanization), Cashvertising LF8 triggers, and proven SG campaign patterns. Use as a 2nd check on:
      - Whether the sophistication level assignment is correct (the notebook has the full Schwartz sophistication framework)
      - Which LF8 biological desires the angle taps into
      - Whether the headline uses the right intensification technique for the awareness level
      - Structural patterns from proven campaigns (PropWise SG scripts, etc.)

   b. **Client-specific notebook** (if registered in client config):
      Check `clients/<project>/notebooklm.json` for a notebook ID. If found, query it for:
      - Brand voice validation (does the copy sound like the client?)
      - Domain knowledge (technical details, case studies, methodology explanations)
      - Content the client has already published (to avoid repeating and to borrow proven framing)
      - Client's own positioning language and philosophy

   **How to query:** Use `notebooklm use <id> && notebooklm ask "<question>"`. Keep queries specific and targeted — don't dump the full brief. Ask one focused question per query.

   **When to query:**
   - Phase 0: Context enrichment (client voice, positioning, domain knowledge)
   - Phase 1: Angle validation (Schwartz check, LF8 check, does the angle match the client's real expertise?)
   - Phase 2: Copy validation (does the headline sound like the client? does the body use correct terminology?)
   - Phase 4: Final tracker review (cross-check proof elements against source material)

4. **HITL Gate 0 (DCT mode only):** Present avatar index. Ask:
   > "Which avatars do you want to target in this DCT run? (Select 2+ for meaningful testing)"

5. Input existing ads (same as v1.1.0). Extract angles already in use.

6. Create campaign directory: `clients/<project>/campaigns/dct-YYMMDD/`

---

### Phase 0.5: Competitive Swipe File Research

**FIRST — load the industry pool (canonical, shared across all clients in this industry):**
- `swipe-files/<industry>/stage-analysis.md` — HITL-approved Schwartz brief: stage assessment, mechanism inventory, blue boxes, blue ocean gaps, winners by duration. **This is the strategic source of truth.** Map the client's industry slug from `clients/<project>/context-profile.json` (e.g. property-sg, saas-sg). If missing, suggest running `/ads:scrape-library <industry>` before generating angles.
- `swipe-files/<industry>/ads-db.sqlite` — queryable layer for ad-level lookups when an angle needs evidence.

**Then — load client-specific overlays:**
- `clients/<project>/swipe-file.md` — general swipe file (legacy/combined)
- `clients/<project>/swipe-file-buyers.md` — buyer-focused competitor ads, angles, landing pages
- `clients/<project>/swipe-file-sellers.md` — seller-focused competitor ads (if client does seller marketing)
- `clients/<project>/competitor-ads/` — raw Meta Ad Library scrapes (reference, don't load fully — too large)

If any swipe file is <60 days old, skip the research step and use existing data. If >60 days old or missing, run the competitive research process (see `references/swipe-file-template.md`).

**How swipe files feed into angle generation:**
- **Deduplication** — angles competitors are already running are flagged (don't duplicate, differentiate)
- **Blue ocean gaps** — angles NO competitor addresses become priority targets
- **Structural patterns** — proven ad formats (pain-stack, contrarian, exit-math) to adapt
- **Language to borrow** — exact phrases from competitor copy that resonate with the audience
- **Longevity signals** — ads running 3+ months are confirmed performers; study their structure

---

### Phase 1: Angle Generation (Per Avatar)

**Role:** Brainstormer subagent (runs once per avatar)

For EACH selected avatar, load:
- The avatar's 12-point breakdown (`avatars/avatar-N.md`)
- The avatar's messaging guidance section
- The sophistication map (`avatars/sophistication-map.md`) — creative strategy per level
- The sophistication-to-creative reference (`references/sophistication-creative-map.md`)
- Swipe file patterns (`swipe-file-buyers.md` and/or `swipe-file-sellers.md` — blue ocean gaps, structural patterns, competitor angles to avoid duplicating)
- Existing ads exclusion list

**Subagent prompt includes:**
- The avatar's specific awareness level and sophistication level
- The avatar's sophistication-driven creative strategy (from `sophistication-map.md`): what to lead with, what to support with, what never to lead with
- The avatar's primary emotion and buying trigger
- Language to use/avoid from the avatar's messaging guidance
- Which proof elements resonate with this avatar specifically

**Generate 6-8 angles per avatar** (fewer than v1.1.0's 10, because they're more targeted).

Score using the angle-scoring rubric. Present grouped by avatar:

```
## Avatar 1: [Name] (Awareness: [Level], Soph: L[N])

| Rank | Angle | Psych Trigger | Score |
|------|-------|---------------|-------|
| 1    | ...   | ...           | 9.2   |
```

### HITL Gate 1: Angle Approval

Present angles grouped by avatar. User actions:
- Pick top 2 angles per avatar (for 2 DCT batches each)
- Reject/replace angles
- Rerank
- Move an angle from one avatar to another

**After approval:** 2 angles per avatar x N avatars = the DCT batch list.
Name them: DCT001, DCT002 (avatar 1), DCT003, DCT004 (avatar 2), etc.

---

### Phase 2: DCT Batch Assembly — Routes by Format

**Role:** Copywriter subagent (runs once per batch)

For each approved angle (now a named DCT batch), the assembly path branches by format:

**Format → Phase routing rule (260418):**

| Format | Path | Why |
|---|---|---|
| Static | **Phase 2a — Hooks** | Single-frame creative; deliverable is a text-on-image hook + headline + visual concept |
| Carousel | **Phase 2a — Hooks** | Multi-card statics; each card is a hook variant on the same angle |
| UGC (any video) | **Phase 2b — Briefs** | Performer + scene + timing + audio specs needed; deliverable is a production-ready brief |
| Founder Video | **Phase 2b — Briefs** | Founder on camera; brief covers scene/script/timing/aesthetic |
| UGC Testimonial | **Phase 2b — Briefs** | Performer-led; brief covers casting + interview structure + b-roll |
| Demo / Product Showcase | **Phase 2b — Briefs** | Screen-recording or product-in-action; brief covers shot list + voice-over + timing |
| VSL (long-form video) | **Phase 2b — Briefs** | Multi-act narrative; brief covers act breakdown + objection beats + proof placement |

**Choose ONE path per batch — never both for the same DCT batch.** The angle is the same; the deliverable shape differs because video and static creative are produced differently.

A batch's `creative_type` field in `dct-tracker.json` records which path: `"hook"` for Phase 2a, `"brief"` for Phase 2b.

**Headlines + Ad Copy + CTA (steps below) are produced for BOTH paths** — they fill the Meta headline + primary text fields regardless of format. Only the visual deliverable differs.

For each approved angle (now a named DCT batch), generate the complete batch using the routed path:

#### 2a. Headlines (2 per batch)

**Skills loaded:** `copywriting/references/direct-response-copy.md`, `copywriting/references/frameworks-library.md`, `references/sophistication-creative-map.md`

**Headline reservoir priority (260418):**

Before generating fresh headlines, check for an existing headline bank at `clients/<project>/angles/wave-<N>-headline-bank.md` (produced by the `headline-bank` skill via `/ads:headlines <project>`).

1. **If the bank exists**, it becomes the PRIMARY reservoir:
   - Go to the section matching the batch's `market_awareness` field (Most Aware / Product Aware / Solution Aware / Problem Aware / Completely Unaware)
   - Filter by the angle bank cluster that matches the batch's `angle` (use `skills/headline-bank/references/awareness-angle-matrix.md` as the crosswalk)
   - Prefer the ★★★ clusters first; fall back to ★★ if the ★★★ pool is thin
   - Pick the TOP 2 headlines that pass anti-slop + brand-voice + the sophistication-driven structure rules below
   - If the bank's matching awareness level has fewer than 2 viable headlines, top up from `clients/<project>/angles/wave-<N>.md` hooks, then from a fresh generation as a last resort
2. **If the bank does NOT exist**, fall back to `clients/<project>/angles/wave-<N>.md` (the 10 hooks per angle) and fresh generation. The bank is optional, not mandatory.
3. Record which path was taken in the batch's `_headline_source` field in `dct-tracker.json` (values: `"bank"` / `"wave-hooks"` / `"fresh"` / `"bank+topup"`).

Rules:
- Max ~40 characters (Meta headline field constraint)
- Two DIFFERENT hooks for the same angle
- UK English
- Must pass headline validation checklist
- Anti-AI slop check
- **Sophistication-driven structure** (from `references/sophistication-creative-map.md`):
  - L1-L2: Headline leads with claim or enlarged claim
  - L3: Headline leads with named mechanism
  - L4: Headline leads with identification/mirror (their exact situation)
  - L5: Headline uses ultra-specific insider language
  - Split sophistication (e.g., L2 marketing / L4 domain knowledge): headline at LOWER level, body at HIGHER level

#### 2b. Ad Copy (2 per batch)

**Skills loaded:** `copywriting/SKILL.md`, `copywriting/references/ad-creative-frameworks.md`, `references/sophistication-creative-map.md`

Rules:
- Max ~125 characters above the fold (Meta primary text)
- Two DIFFERENT frameworks per batch. **Framework selection MUST match sophistication level:**

  | Soph Level | Preferred Frameworks | Avoid |
  |-----------|---------------------|-------|
  | L1-L2 | PAS, Data-led, Story | Contrarian (nothing to contrast) |
  | L3 | Story (mechanism reveal), Data-led | Pure claim |
  | L4 | Fear-validation, Question-driven, Contrarian, Permission-granting | PAS (too formulaic, they recognise it), Data-led alone |
  | L5 | Story (peer voice), Permission-granting | Anything that reads like "ad copy" |

- UK English
- Anti-AI slop check
- Brand-voice compliant
- **CTA pressure must match sophistication level:**
  - L1-L2: Direct CTA ("Take the free assessment")
  - L3: Mechanism-led CTA ("See your 3 numbers in 2 minutes")
  - L4: Low-pressure CTA ("No agent call. No obligation. Just clarity.")
  - L5: Whisper CTA ("When you're ready.") or no explicit CTA

#### Phase 2a — Hooks (for Static + Carousel formats only)

> Path taken when batch `format ∈ {Static, Carousel}`. Output: text-on-image hook + visual concept + image prompt per creative. Deliverable is `creative_type: "hook"` in dct-tracker.json.

**Skills loaded:** `image-generation/SKILL.md`, `references/sg-cultural-guidelines.md`, `references/sophistication-creative-map.md`, `references/high-converting-static-brief.md`

**MANDATORY:** Load `references/high-converting-static-brief.md` as hard constraints before producing any static/carousel variant. That file encodes the 9-point scroll-stop bar (unique variants, SG ethnic distribution, real-not-AI faces, clear headline on image, bridge line when needed, editorial/documentary/cinematic aesthetic — not generic Meta-ad look, factually correct info, gut-punch emotional weight). Store each variant's Nano Banana 2 JSON in `clients/<project>/campaigns/<campaign>/image-prompts/<batch>-<variant>.json` — never inline the full prompt in dct-tracker.json, just reference the file.

Rules:
- 3 creatives per batch, each a COMPLETELY DIFFERENT visual style
- Each has a standalone text-on-image hook (2-8 words, NOT the Meta headline)
- 1:1 square (1024x1024) for Meta feed
- Full Nano Banana 2 JSON prompts
- Anti-AI negative prompts on all
- thinking_level: "high" for all with people
- **Visual concept type per creative** — pick one of the 4 approaches per creative (and vary across the 3 in the batch):
  - **Picture of the benefit** — show the desired outcome / transformed state
  - **Picture of the problem** — show the before-state pain or friction
  - **Picture of the product** — focus on the item / mechanism / interface
  - **Picture of the product in action** — demonstrate use, show the moment of transformation
- **Visual style must match sophistication level:**
  - L1-L2: Product/lifestyle imagery, bold claims on image
  - L3: Mechanism/process visuals, infographics
  - L4: UGC-style, raw/authentic, text-on-dark, WhatsApp aesthetic
  - L5: Pure UGC, meme format, screenshot aesthetic
- **Text-on-image hooks must match sophistication level:**
  - L1-L2: Claim or benefit (e.g. ecom: "Brighter skin in 7 days" · SaaS: "Cut reporting time by 80%")
  - L3: Mechanism tease (e.g. ecom: "The 3-step ritual" · SaaS: "The N-minute setup")
  - L4: Identification question or statement (e.g. SaaS: "Still copy-pasting between sheets at 11pm?" · service: "Third agent this year and still no buyers?")
  - L5: Insider language / colloquial — use specific buyer-language verbatim from §5 dossier

**Visual style assignment:** Distribute styles across the 3 creatives so no two in the same batch share a style. The skill should vary across batches too — if DCT001 uses [realistic, text-only, claymation], DCT002 should use [UGC, infographic, Pixar].

**Output schema (per creative, in dct-tracker.json):**
```json
{
  "creative_type": "hook",
  "format": "Static",
  "visual_concept_type": "Picture of problem",
  "visual_style": "UGC",
  "text_on_image_hook": "[2-8 words]",
  "image_prompt": { /* Nano Banana 2 JSON */ },
  "headline_1": "[~40 char]",
  "headline_2": "[~40 char]",
  "copy_1": "[~125 char above-fold]",
  "copy_2": "[~125 char above-fold]",
  "cta": "[CTA pattern matching sophistication]"
}
```

#### Phase 2b — Briefs (for UGC / Founder / Demo / VSL formats only)

> Path taken when batch `format ∈ {UGC, Founder Video, UGC Testimonial, Demo, VSL}`. Output: full production-ready brief per video creative. Deliverable is `creative_type: "brief"` in dct-tracker.json.

**Skills loaded:** `video-director/SKILL.md`, `script-skill/SKILL.md`, `references/sg-cultural-guidelines.md`, `references/sophistication-creative-map.md`, `references/video-brief-template.md`

A brief is NOT a script. A script is the words. A brief is the entire production direction: what to shoot, who shoots, what gear, what aesthetic, what timing, where the hook lands, where the CTA lands, what gets cut to. A copywriter or UGC creator should be able to read the brief and execute without further questions.

Rules:
- 1 brief per video creative (typical batch: 3 video creatives = 3 briefs, one per visual variant)
- Brief follows the structure in `references/video-brief-template.md`:
  1. **Creative Vision** (1 paragraph — tone, aesthetic, target emotion)
  2. **Scene Breakdown** (6 timed scenes: Hook 0-3s · Problem 3-8s · Mechanism 8-15s · Proof 15-18s · Transformation 18-22s · CTA 22-25s) — each scene specifies location, lighting, props, performer action, copy/VO, visual beat
  3. **Performer Notes** (age range, representation, personality, energy, eye contact, pacing, do's and don'ts)
  4. **Audio Specs** (music mood, VO style, silence beats)
  5. **Graphics / Overlays** (hook text on-screen with timing, mechanism visuals, CTA frame)
  6. **Technical Specs** (duration, aspect ratio, resolution, frame rate)
  7. **Timing Map** (which beat at which second — the spine the editor cuts to)
- The 6-scene default is for short-form (≤30s) ads (UGC, Founder Video, UGC Testimonial, Demo). For VSL (long-form 2-10min), expand to act-based structure: Act 1 Hook → Act 2 Problem amplification → Act 3 Mechanism → Act 4 Proof + objection handling → Act 5 Offer + urgency. Document act timings + beat anchors.
- **Sophistication-driven aesthetic** (same map as Phase 2a but applied to video):
  - L1-L2: Polished demo / lifestyle, bold claims on screen
  - L3: Mechanism reveal / process walkthrough
  - L4: UGC-raw / authentic peer voice / shaky handheld OK
  - L5: Pure UGC / single-take / no production polish
- **Performer direction MUST come from the avatar** — performer profile (age, ethnicity, situation) mirrors the target avatar's demographics. Copy the avatar's Raw Inner Dialogue (§14) verbatim into performer lines where appropriate.
- Anti-AI slop check on all VO scripts and on-screen text
- Brand-voice compliant (load `voice/<person>/brand-voice.md`)
- For Founder Video: founder is the performer; brief includes founder-specific direction (what to wear, where to film, what NOT to script)
- For UGC Testimonial: performer is a real customer (or actor playing one); brief includes interview structure + b-roll + testimonial framing rules

**Output schema (per video creative, in dct-tracker.json):**
```json
{
  "creative_type": "brief",
  "format": "Founder Video",
  "brief": {
    "creative_vision": "...",
    "scene_breakdown": [
      {"scene": 1, "name": "Hook", "timing": "0-3s", "location": "...", "lighting": "...", "props": [...], "performer_action": "...", "copy_or_vo": "...", "visual_beat": "..."},
      // ... 6 total scenes for short-form
    ],
    "performer_notes": "...",
    "audio_specs": "...",
    "graphics_overlays": [...],
    "technical_specs": {"duration": "25s", "aspect_ratio": "9:16", "resolution": "1080p", "frame_rate": "30fps"},
    "timing_map": [...]
  },
  "headline_1": "[~40 char]",
  "headline_2": "[~40 char]",
  "copy_1": "[~125 char above-fold]",
  "copy_2": "[~125 char above-fold]",
  "cta": "[CTA pattern matching sophistication]"
}
```

**Quality bar:** if a brief reads as one paragraph of "creative direction notes" instead of a structured production document, it failed. The whole point of the brief vs hook split is that videos need 10x more production information than statics. A one-line "creator: 32-45, in living room setting" is not a brief.

### HITL Gate 2: DCT Batch Approval

Present each batch as a card:

```
### DCT001 — Avatar: [Name] | Angle: [Title]
**Awareness:** [Level] | **Sophistication:** L[N]

| Component | Variant A | Variant B |
|-----------|-----------|-----------|
| Headline  | "[H1]" | "[H2]" |
| Ad Copy   | [Framework]: "[Copy A]" | [Framework]: "[Copy B]" |

**Creative 1** ([Style]): [Description] | Hook: "[text-on-image]"
**Creative 2** ([Style]): [Description] | Hook: "[text-on-image]"
**Creative 3** ([Style]): [Description] | Hook: "[text-on-image]"

Combinations: 12 | Est. cost: $0.20
```

User actions: Approve / edit headlines or copy / change image concepts / swap styles / regenerate

---

### Phase 3: Creative Execution — Routes by creative_type

Phase 3 mirrors Phase 2's routing rule. Each batch's `creative_type` field determines which downstream skill executes the creative spec:

#### Phase 3a — Image execution (for `creative_type: "hook"`)

Execute approved Phase 2a image prompts via the `image-generation` skill. The Nano Banana 2 JSON prompts produced in Phase 2a are passed directly — image-generation knows how to render them.

Save to: `clients/<project>/campaigns/dct-YYMMDD/batch-NN/assets/`

Cost reference: ~$0.07/image via Nano Banana 2 + Vertex AI direct generation.

#### Phase 3b — Video execution (for `creative_type: "brief"`)

Execute approved Phase 2b video briefs via the `video-director` skill. Two execution paths:

1. **AI-generated video** — pass the brief to video-director's Sora 2 Pro / Kling / VEO prompt pipeline. video-director translates the 6-scene brief into multi-shot AI prompts, optionally runs Vertex AI direct generation, and saves the rendered video files.

2. **Human-creator brief handoff** — the brief itself is the deliverable. Save the brief markdown to disk and hand off to a UGC creator, founder, or video editor for human production. video-director maintains the brief format spec; ad-concept-engine produces the brief content.

Save to: `clients/<project>/campaigns/dct-YYMMDD/batch-NN/video/`

The route between AI-generated vs human-creator is determined by the format + the user's HITL decision at Gate 2 (the Phase 2 batch approval step now includes a "produce via AI / produce via creator" toggle per video batch).

### HITL Gate 3: Creative Approval

Show generated images and video previews (or briefs handed to creators) grouped by batch. User approves or requests regeneration. For video briefs handed to humans, this gate is the final QA before sending to the creator.

---

### Phase 4: DCT Tracker Compilation

Compile all approved batches into the master tracker:

```markdown
# DCT Tracker — [Client] — [Date]

## Summary
- Avatars targeted: [N]
- DCT Batches: [N]
- Total combinations: [N x 12]
- Images generated: [N x 3]
- Est. total cost: $[N]
- Status: Ready for upload

## Batches

| Batch | Status | Avatar | Awareness | Soph | Angle | H1 | H2 | Copy A (framework) | Copy B (framework) | Img 1 (style) | Img 2 (style) | Img 3 (style) |
|-------|--------|--------|-----------|------|-------|----|----|--------------------|--------------------|----|----|----|
| DCT001 | READY | [Name] | [Level] | L[N] | [Angle] | "[H1]" | "[H2]" | [Framework] | [Framework] | [Style] | [Style] | [Style] |
| DCT002 | READY | [Name] | [Level] | L[N] | [Angle] | "[H1]" | "[H2]" | [Framework] | [Framework] | [Style] | [Style] | [Style] |
...

## Performance (fill after launch)

| Batch | CTR | CVR | CPA | Calls | Spend | Duration | Winning Combo | Notes |
|-------|-----|-----|-----|-------|-------|----------|---------------|-------|
| DCT001 | | | | | | | | |
...

## Kill/Scale Decisions
[To be filled — which batches to kill, which to scale, which to iterate]
```

### HITL Gate 4: Tracker Sign-off

Present the complete tracker. User approves before handoff to `meta-ads-uploader`.

---

## Pipeline Integration

**Upstream:**
- `avatar-research` skill → `avatars/` directory (REQUIRED for DCT mode)
- `avatar-research` Phase 2.5 → `avatars/sophistication-map.md` (REQUIRED — drives creative strategy)
- Client files: buyer-profile.md, offer.md, brand-voice.md, icp.md
- Swipe file (built during Phase 0.5 or from previous run)

**Downstream:**
- `[[video-factory]]` — turn approved DCT batches into AI-generated video ads. After Gate 4 (tracker approved), ask: "Want to turn any of these batches into video?" User selects batch(es) → video-factory loads in DCT Entry Mode → skips Phase 1-2, enters at Phase 3 with angle, avatar, headlines, copy framework, and image concepts pre-loaded. 3 image concepts expand to 6 video shots (hook → pain → mechanism → proof → transformation → CTA).
- `meta-ads-uploader` — upload creatives + copy to Meta (paused)
- `campaign-runner` — integrate into active campaign
- `ab-test-setup` — design follow-up tests on winning combinations

**Rerun cadence:** Every 4-6 weeks, or when creative fatigue detected.

---

## References

- `references/sophistication-creative-map.md` — L1-L5 creative strategy framework (Schwartz market sophistication)
- `references/high-converting-static-brief.md` — 9-point scroll-stop bar for Phase 2a static/carousel variants (MANDATORY on every static batch)
- `references/angle-scoring-rubric.md` — Scoring matrix for angle ranking
- `references/headline-validation-checklist.md` — Full validation checklist
- `references/sg-cultural-guidelines.md` — Singapore cultural sensitivity rules
- `references/swipe-file-template.md` — Competitive research template
- `references/dct-tracker-template.md` — DCT tracker output template
- `references/video-brief-template.md` — 6-scene video brief spec for Phase 2b
- `copywriting/references/ad-creative-frameworks.md` — Hook-Body-CTA, creative testing
- `copywriting/references/direct-response-copy.md` — Schwartz, Hopkins, Ogilvy, Halbert, Caples
- `copywriting/references/frameworks-library.md` — 40+ copywriting frameworks
- `marketing-psychology/SKILL.md` — 70+ mental models
- `content-moat/references/ideation-frameworks.md` — Originality-first ideation
- `image-generation/SKILL.md` — JSON prompt schema, generation pipeline

### NotebookLM Integration

- **General (all clients):** Notebook `1644f7b5` — "The AI Influencer & Marketing message" — Schwartz full framework (awareness + sophistication + intensification/gradualization/mechanization), Cashvertising LF8, PropWise SG campaign scripts. Use as 2nd-pass validation.
- **Client-specific:** Check `clients/<project>/notebooklm.json` for registered notebooks. Query for brand voice, domain knowledge, proof elements, and positioning language.

<!-- skill-graph:start -->

## Related
<!-- auto-generated by scripts/link-skills.py — do not edit by hand -->

- [[headline-bank]] (skill, 0.22)
- [[big-angle-spotter]] (skill, 0.17)
- [[avatar-research]] (skill, 0.13)

<!-- skill-graph:end -->
