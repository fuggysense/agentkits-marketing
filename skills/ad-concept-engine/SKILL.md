---
name: ad-concept-engine
version: "2.0.0"
brand: AgentKits Marketing by AityTech
preferred_invocation: /copy:ad  # wraps this skill with copywriting-OS gates + reviewers + mechanism-diversity (see .claude/references/copywriting-os/)
category: content
difficulty: advanced
description: "DCT-aware ad concept pipeline: 3 creatives × 2 headlines × 2 copies = 12 Meta combinations per batch. Per-micro-persona angles, visual style variety, standalone text hooks. Triggers: ad concepts, new ad angles, DCT, dynamic creative testing, ad brainstorm, meta ad concepts."
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
  - video-concept-lab
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

> Generate per-micro-persona ad angles, assemble complete DCT batches, and compile a tracker for Meta dynamic creative testing. Each batch = 3 creatives x 2 headlines x 2 ad copies = 12 combinations Meta tests automatically.

## Graph Links

- Feeds into: `[[image-generation]]`, `[[video-concept-lab]]`, `[[video-factory]]`, `[[meta-ads-uploader]]`, `[[campaign-runner]]`
- Draws from: `[[avatar-research]]`, `[[marketing-psychology]]`, `[[content-moat]]`, `[[copywriting]]`, `[[paid-advertising]]`
- Used by agents: `[[brainstormer]]`, `[[copywriter]]`, `[[brand-voice-guardian]]`, `[[researcher]]`
- Related: `[[paid-media-audit]]`, `[[ab-test-setup]]`, `[[multi-agent-consensus]]`

## When to Use This Skill

- Client needs fresh ad concepts organized for Meta DCT testing
- Multiple micro-personas need distinct creative per audience segment
- User says "ad concepts," "DCT," "dynamic creative testing," "ad brainstorm"
- Entry is **by intent, not a command** — see Conductor Mode below. The routing layer (`.claude/rules/routing-overrides.md`) lands plain-English DCT asks here; there is no `/ads:concepts` to memorise.

## Conductor Mode — Entry & Resume Protocol (10-5-5 clients)

> **Scope:** this protocol governs the **10-5-5** opt-in clients (neezanizam, eugene). For 3-2-2 clients the skill runs exactly as the sections below describe, with no state file. The conductor is what makes a DCT **pausable, resumable, and self-navigating** — you never restart a run from scratch and you never need to remember a command.

When the operator says something like *"new ad concepts for neezanizam buyers,"* *"continue the DCT,"* *"next angle wave,"* or *"resume the neezanizam ads"* — **you are the conductor.** You don't generate angles or copy yourself; you cue the specialist skills in order (big-angle-spotter → headline-bank → render → …) and keep the state file honest about where you are. On EVERY entry, in order:

1. **Establish the context receipt** (AGENT ENTRY CONTRACT — non-negotiable): read the client's `CLAUDE.md` + `CONTEXT.md` + `context-profile.json`, then `campaigns/_campaigns-index.json` to resolve WHICH campaign + metrics-campaign. (neezanizam runs two — `buyer-funnel` vs `asset-progression` — never guess; confirm from the index.)
2. **Locate the DCT workspace** — `clients/<client>/campaigns/<campaign>/dcts/<dct>/`. If the operator named one, use it. If ambiguous (>1 active DCT, or funnel unclear), **ask one question** — do not assume.
3. **Read `pipeline-state.json`** in that workspace:
   - Missing → NEW DCT → `pipeline_state.py init`.
   - Exists with any phase past `phase_0_context` marked `complete` → **RESUME**: print the card (`pipeline_state.py resume`), act on `next_action`, and **do NOT regenerate completed phases.**
4. **Walk the phases**, pausing at each HITL gate. After every state-changing step, `pipeline_state.py advance` and append to `event-log.jsonl`. The state file is the single source of truth for "where are we."
5. **Conflict → ask, don't paper over.** A saturated-angle clash, a missing `_brand/` file, funnel ambiguity, or a gate that contradicts a prior approval is a one-question stop — not a silent guess.

```bash
PS=skills/ad-concept-engine/scripts/pipeline_state.py
# NEW DCT — init first (all of --dct --client --campaign required; --metrics-campaign/--method/--workspace optional):
python3 $PS init    clients/<c>/.../pipeline-state.json --dct DCT010 --client neezanizam \
                    --campaign buyer-funnel --metrics-campaign buyer-funnel --method 10-5-5 \
                    --workspace clients/neezanizam/campaigns/buyer-funnel/dcts/<dct>
# EXISTING DCT — resume / advance:
python3 $PS resume  clients/<c>/campaigns/<camp>/dcts/<dct>/pipeline-state.json   # you-are-here card
python3 $PS next    clients/<c>/.../pipeline-state.json                            # one-line next action
python3 $PS advance clients/<c>/.../pipeline-state.json --phase phase_1_angles --status complete --gate-status approved --output "5 angles"
```

The resume card's **NEXT** line is your instruction — execute that phase, then `advance`. Don't infer the doing-loop; the card drives it.

Full runbook: `references/dct-pipeline-map.md`. Canonical manifest shape: `docs/dct-json-schema.md`.

### Phase reconciliation — this skill's phase names ↔ the resume state ids

The phase names below predate the resume spine. When you `advance` state, use the **state id**, not the prose name:

| This skill's section | State id (in `pipeline-state.json`) | Gate |
|---|---|---|
| Phase 0: Context + Persona | `phase_0_context` | gate_0_personas |
| Phase 0.5: Swipe research | *(sub-step of phase_0 — no own state phase)* | — |
| Phase 1: Angle Generation (→ big-angle-spotter) | `phase_1_angles` | gate_1_angles |
| Phase 2: DCT Batch Assembly → **`dct.json`** | `phase_2_assembly` | gate_2_batch |
| Phase 3: Creative Execution | `phase_3_render` → `phase_3b_allocate` → `phase_3_creative_gate` | gate_3_creative |
| **Phase 4: DCT Tracker Compilation** | *folds into `phase_2` + `phase_4_sheet` — see note* | — |
| *(upload handoff)* | `phase_5_upload` | gate_4_preupload |

**The reconciliation that matters:** in 3-2-2 (legacy) the tracker was compiled as a separate "Phase 4." In 10-5-5 the manifest (`dct.json`) is born during **assembly (phase_2)** and the sheet writer just reads it — so "Phase 4: Tracker Compilation" collapses; the freed slot is the sheet write (`phase_4_sheet`).

> **Open blockers (tracked in `pipeline-state.json`, NOT silently fixed):** the Phase 2 emitter still writes legacy `dct-tracker.json` (**G1**), `allocate`/phase_3b is unbuilt (**G3**), and `ad_concept_sheet_writer.py` still reads the old format (**G4**). The conductor declares `dct.json` canonical and is resumable TODAY; those three downstream repoints are the next track. Until they land, a 10-5-5 run yields a resumable state file + a `dct.json` (via `migrate_tracker_to_dct.py`), while the live sheet/upload steps still touch the legacy artifact.

## Phase 0 — Delegate to Big-Angle-Spotter (v3.0 orchestrator mode)

**This skill NO LONGER generates angles or static hooks directly.** Those are delegated to the `big-angle-spotter` skill (`skills/big-angle-spotter/`, symlinked to `~/AI workflows/big-angle-spotter/`). Ad-concept-engine is now the orchestrator that:

1. **Loops big-angle-spotter N times** across selected micro-personas (sequential, not parallel — see "Multi-angle orchestration" below)
2. **Cross-pollinates EXISTING_ANGLES** so each successive run knows the prior winners and picks something different
3. **Wraps outputs into Meta hierarchy** per the new naming spec
4. **Routes video concept work to Video Concept Lab after user confirmation** (UGC/Founder/VSL/Demo/Singing/No-dialogue — those don't come from big-angle-spotter)
5. **Routes image prompts** from big-angle-spotter step 12 → image-generation for actual PNG rendering
6. **Writes dct-tracker + sheet** under new folder structure

### Multi-angle orchestration (sequential, EXISTING_ANGLES cross-pollinated)

Per wave target `N` angles. For each angle `i` in `1..N`:

```
1. Build EXISTING_ANGLES_i = saturated_angles (from learnings.md + iteration-log.md)
                          + [winning_angle_1, ..., winning_angle_{i-1}]
2. Pick target micro-persona for angle i (round-robin or per wave spec)
3. Write inputs.json with:
     OFFER, COMPANY (from context-profile.json)
     PERSONA (from `_brand/buyer-profile.md` Micro-Persona Map; legacy `_brand/avatars/avatar-<N>.md` only if required)
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
- Detects `clients/<project>/_brand/avatars/` directory → generates angles per avatar
- Assembles full DCT batches, Phase 2a hooks inline
- Outputs DCT tracker under old `campaigns/dct-<date>/` structure
- Kept for projects that haven't migrated yet

## Language & Quality Standards

- UK English spelling throughout (analyse, recognised, colour, centre)
- All headlines pass validation checklist (`references/headline-validation-checklist.md`)
- All angles pass scoring rubric (`references/angle-scoring-rubric.md`)
- Locale + cultural-sensitivity rules apply per-client (`clients/<project>/_brand/locale-rules.md` if present; template + SG example at `clients/_template/_brand/locale-rules.md`)
- Brand-voice compliance against `clients/<project>/_brand/brand-voice.md`
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

### Phase 0: Context Load + Micro-Persona Detection

**Role:** Orchestrator (main context)

1. Load client context files:
   - `clients/<project>/_brand/buyer-profile.md`
   - `clients/<project>/_brand/offer.md`
   - `clients/<project>/_brand/brand-voice.md`
   - `clients/<project>/_brand/icp.md`
   - `clients/<project>/_brand/story-bank.md`

2. Check buyer targeting:
   - If `clients/<project>/_brand/buyer-profile.md` contains `## MICRO-PERSONA MAP` → load the map and enter DCT mode
   - If only legacy `clients/<project>/_brand/avatars/` exists → mine it as compatibility input, then recommend migrating useful targeting into `_brand/buyer-profile.md`
   - If neither exists → offer to run `/ads:avatars` first, or proceed in Legacy mode

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

4. **HITL Gate 0 (DCT mode only):** Present the Micro-Persona Map. Ask:
   > "Which micro-personas do you want to target in this DCT run? (Select 2+ for meaningful testing)"

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

### Angle = problem + person + timing + proof

Keep it human. An angle is just:

`Angle = problem + person + timing + proof`

- **Problem (the barrier):** the real thing blocking them. Name it FIRST.
- **Person + awareness:** who they are, and how aware they already are of the problem and the options.
- **Timing:** what makes it matter *now* (the trigger).
- **Proof:** the evidence THIS person will actually believe.

**Example — speaking coach:** Barrier: they freeze on stage · Awareness: they know they need to speak better · Frame: "say less, land harder" · Proof: before/after clips, testimonials, speaking results.

**Example — iron supplement:** Barrier: they feel tired and foggy · Awareness: they know low energy is the problem · Frame: "steady energy without caffeine crashes" · Proof: ingredient credibility, reviews, results.

**The biggest mistake is starting with the frame before you understand the barrier.** Barrier first, frame last.

### Phase 1: Angle Generation (Per Micro-Persona)

**Role:** Brainstormer subagent (runs once per avatar)

For EACH selected micro-persona, load:
- The micro-persona row and supporting sections from `_brand/buyer-profile.md#micro-persona-map`
- The micro-persona's messaging guidance, language to use/avoid, proof needs, awareness, and sophistication
- Legacy `_brand/avatars/avatar-N.md` only when an older downstream tool requires it; treat it as compatibility, not authority
- The sophistication-to-creative reference (`references/sophistication-creative-map.md`)
- Swipe file patterns (`swipe-file-buyers.md` and/or `swipe-file-sellers.md` — blue ocean gaps, structural patterns, competitor angles to avoid duplicating)
- Existing ads exclusion list

**Subagent prompt includes:**
- The micro-persona's specific awareness level and sophistication level
- The micro-persona's sophistication-driven creative strategy: what to lead with, what to support with, what never to lead with
- The micro-persona's primary emotion and buying trigger
- Language to use/avoid from the micro-persona's messaging guidance
- Which proof elements resonate with this micro-persona specifically

**Generate 6-8 angles per micro-persona** (fewer than v1.1.0's 10, because they're more targeted).

Score using the angle-scoring rubric. Present grouped by avatar:

```
## Micro-Persona 1: [Name] (Awareness: [Level], Soph: L[N])

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

#### Phase 2.0 — Video Confirmation Gate

Before any Phase 2b video concept work, ask:

> Are we producing video ads for this batch/wave, or should this stay as static/carousel creative?

- If the user confirms video, route to `vid-director` / `video-concept-seeder` with `video-concept-lab` as methodology. The concept stage produces five video concepts, recommends a winner, defines early character/product/style-sheet requirements, and writes AG1 artifacts under `02_ag1-options/`.
- If the user says static/carousel, stay in Phase 2a. Do not load `video-concept-lab`.
- Do not touch Meta primary text or Meta headline generation in this gate.

**Format → Phase routing rule (260418):**

| Format | Path | Why |
|---|---|---|
| Static | **Phase 2a — Hooks** | Single-frame creative; deliverable is a text-on-image hook + headline + visual concept |
| Carousel | **Phase 2a — Hooks** | Multi-card statics; each card is a hook variant on the same angle |
| UGC (any video) | **Phase 2b — Briefs** | Performer + scene + timing + audio specs needed; deliverable is a production-ready brief |
| Founder Video | **Phase 2b — Briefs** | Founder on camera; brief covers scene/script/timing/aesthetic |
| UGC Testimonial | **Phase 2b — Briefs** | Performer-led; brief covers casting + interview structure + b-roll |
| Demo / Product Showcase | **Phase 2b — Briefs** | Screen-recording or product-in-action; brief covers shot list + voice-over + timing |
| Singing Ad | **Phase 2b — Video Concept Lab** | Lyrics + full music direction + visual beat map needed before production |
| No-dialogue Ad | **Phase 2b — Video Concept Lab** | Silent visual sequence + rendered text policy + sound design needed before production |
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

**Skills loaded:** `image-generation/SKILL.md`, `references/static-image-method.md`, `references/sophistication-creative-map.md`, plus `clients/<project>/_brand/locale-rules.md` **if present**.

**MANDATORY:** Load `references/static-image-method.md` as the active method before producing any static/carousel variant. It is the Ferres-grounded rebuild (replaces the retired `high-converting-static-brief.md`, now in `_archive/references-pre-ferres/`). The method runs four moves per batch: (1) choose a FORMAT (1 of 5 lanes) or a named PATTERN (1 of 11 — load `_shared-knowledge/ferres/patterns/statics-pattern-library.md` at generation time and cite the pattern by name); (2) 3-pass teardown-rebuild (why-it-wins → how-we-rebuild → the prompt); (3) inject the client offer + VOC with a source pointer on every specific, then run the Claim Gate on the prompt text; (4) post-render image QA gate (text legible + spelled, on-brand, product correct, compliance scan, claim gate green) and label by format + hook. The method carries ZERO locale content — load `clients/<project>/_brand/locale-rules.md` IF PRESENT for casting, regulated-document fidelity, currency/income bands, and the local compliance block. Store each variant's Nano Banana JSON in `clients/<project>/campaigns/<campaign>/image-prompts/<batch>-<variant>.json` — never inline the full prompt in dct-tracker.json, just reference the file.

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

#### Phase 2b — Video Concepts + Briefs (for video formats only)

> Path taken when batch `format ∈ {UGC, Founder Video, UGC Testimonial, Demo, Singing Ad, No-dialogue Ad, VSL}` AND the user has confirmed the batch/wave is video. Output starts with `vid-director` dispatching `video-concept-seeder` using the `video-concept-lab` graph loadout, then becomes a full production-ready brief per approved video creative. Deliverable is `creative_type: "brief"` in dct-tracker.json.

**Skills loaded:** `video-concept-lab/SKILL.md`, `video-concept-lab/REFERENCE_GRAPH.json`, `script-skill/SKILL.md`, `video-brief-normalizer/SKILL.md`, `clients/<project>/_brand/locale-rules.md` (if present), `references/sophistication-creative-map.md`

A brief is NOT the first concept output. A script is the words or visual beats. The brief pack is created only after Approval Gate 1 and script/visual refinement. It contains a client-facing Google Docs source brief plus an internal AI production contract that Video Factory can execute after Approval Gate 2.

Rules:
- `video-concept-seeder` produces five concepts by default plus a recommended winner using the selected `video-concept-lab` loadout. Approval Gate 1 approves the selected concept and first-pass visuals only.
- After Approval Gate 1, refine `03_scripts/final-script.md` and `03_scripts/visual-treatment.md`.
- `video-brief-normalizer` then creates `05_prompt-packs/brief-pack/google-docs-brief.md`, `05_prompt-packs/brief-pack/video-brief.md`, `05_prompt-packs/brief-pack/video-brief.json`, and `07_review/approval-2.json`.
- Only after Approval Gate 2 is approved should `05_prompt-packs/video-factory-handoff.json` be written.
- Existing hooks may be used or fresh hooks may be generated. Hooks must distinguish verbal hook, quiet visual hook, rendered text hook, and subtitle policy.
- 1 approved brief pack per video creative.
- The first implementation is AI-video only. Do not generate human creator filming instructions unless the user explicitly switches production mode later.
- The client-facing Google Docs brief shows the approved winner only.
- The internal video brief includes scene timing, asset requirements, style-sheet requirements, reference order, model assumptions, and open blockers.
- The 6-scene default is for short-form (≤30s) ads (UGC, Founder Video, UGC Testimonial, Demo). For VSL (long-form 2-10min), expand to act-based structure: Act 1 Hook → Act 2 Problem amplification → Act 3 Mechanism → Act 4 Proof + objection handling → Act 5 Offer + urgency. Document act timings + beat anchors.
- **Sophistication-driven aesthetic** (same map as Phase 2a but applied to video):
  - L1-L2: Polished demo / lifestyle, bold claims on screen
  - L3: Mechanism reveal / process walkthrough
  - L4: UGC-raw / authentic peer voice / shaky handheld OK
  - L5: Pure UGC / single-take / no production polish
- **Performer direction MUST come from the selected micro-persona** — performer profile, situation, and voice mirror the target buyer context. Use Raw Inner Dialogue from `_brand/buyer-profile.md` where applicable.
- New fictional or realistic avatar/persona characters are allowed only as proposed concepts until the user approves them.
- Singing ads must include lyrics plus full music direction. Do not assume Suno or any music API can be called; output a manual Suno-ready brief if needed.
- No-dialogue ads must not include subtitles in the final ad. If rendered text appears, state the exact text and its visual purpose.
- Character/product/environment/style-sheet requirements from `video-concept-lab` are early requirements. The final production asset contract is written by `video-brief-normalizer` after script/visual refinement.
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
    "concept_pack": "video-concepts/<slug>/02_ag1-options/concept-pack.json",
    "approval_1": "video-concepts/<slug>/02_ag1-options/approval-1.json",
    "final_script": "video-concepts/<slug>/03_scripts/final-script.md",
    "visual_treatment": "video-concepts/<slug>/03_scripts/visual-treatment.md",
    "google_docs_brief": "video-concepts/<slug>/05_prompt-packs/brief-pack/google-docs-brief.md",
    "video_brief_json": "video-concepts/<slug>/05_prompt-packs/brief-pack/video-brief.json",
    "approval_2": "video-concepts/<slug>/07_review/approval-2.json",
    "video_factory_handoff": "video-concepts/<slug>/05_prompt-packs/video-factory-handoff.json"
  },
  "headline_1": "[~40 char]",
  "headline_2": "[~40 char]",
  "copy_1": "[~125 char above-fold]",
  "copy_2": "[~125 char above-fold]",
  "cta": "[CTA pattern matching sophistication]"
}
```

**Quality bar:** if the internal brief reads as one paragraph of "creative direction notes" instead of a structured AI production contract, it failed. It must be sufficient for Video Factory to create input-image prompts without rereading the whole concept pack.

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

Execute approved Phase 2b video briefs via Video Studio / `video-factory`. Two execution paths:

1. **AI-generated video** — pass the Approval Gate 2-approved `05_prompt-packs/video-factory-handoff.json` to Video Studio / `video-factory`. Video Studio handles input-image prompts, input assets, Beat Sheet Director, model-specific prompts, render requests, and approvals.

2. **Human-creator brief handoff** — deferred. First implementation is AI-video only; do not package human filming instructions unless the user explicitly switches production mode later.

Save to: `clients/<project>/campaigns/dct-YYMMDD/batch-NN/video/`

For now, route Phase 3b to AI-generated video by default.

### Claim Gate (machine precondition — runs BEFORE HITL Gate 3)

Every number a creative asserts is a liability if no source backs it. A fabricated stat baked into an image is the worst case: it ships inside a pixel where no reviewer re-reads the body copy. So before the human ever sees the batch, run the claim gate on the assembled `dct.json`. It is a hard precondition for HITL Gate 3, not a suggestion.

```bash
python3 scripts/claim_gate.py --gate clients/<project>/campaigns/<campaign>/dcts/<dct-slug>/dct.json
```

The gate reads every claim-bearing field (primary text, headlines, copy, `text_on_image_hook`, `bridge_line`, `image_prompt`, `visual_style`) and extracts checkable claims: currency figures, percentages, "X out of Y" ratios, and quantified superlatives. It resolves each one in order against (1) a `claims:` ledger block in the dct itself, (2) prices that appear in `_brand/offer.md`, then (3) an auto-trace through the client research dirs and the research vault. Years, image dimensions, and layout percentages are not claims, so they pass untouched.

Exit 0 means every claim is sourced and the batch may move to HITL Gate 3. Exit 1 means at least one claim is unsourced, and the gate prints each one in plain language: the claim, the field it lives in, the file, and the three ways to clear it.

```
CLAIM GATE — FAIL  (3 unsourced of 27 claims)

  UNSOURCED: "73%"  (percent)
    at: DCT-SMOKE-01-image:DCT-SMOKE-01-img-03.text_on_image_hook
    in: clients/_smoketest/campaigns/wave-smoke-260611/dct.json
    fix one of: (a) add a source to the dct.json `claims:` ledger (path + line/anchor),
                (b) reword without the number, or (c) cut the claim.
```

On a fail, do exactly one of three things per claim: add a real source to the `claims:` ledger (a path plus line or anchor), reword the copy so the number is gone, or cut the claim. Then re-run the gate. Run `--audit` instead of `--gate` to see the full claim-by-source table without failing the build.

Never wave a failing gate through silently. If an operator decides to ship an unsourced number anyway, that is a recorded HITL override with a reason, never a skipped step.

### Copy Pre-Launch Rubric (fresh-context reviewer — runs AFTER the Claim Gate, BEFORE HITL Gate 3)

Once every number is sourced, the batch's copy still has to clear the Ferres quality bar before a human spends attention on it. Dispatch a **fresh-context reviewer** (a sub-agent with no anchoring from the drafting context) to score each ad against `references/copy-prelaunch-rubric.md` — six dimensions, 1-5 each: hook effort + two jobs, call-out + who-it's-NOT-for, copyboarding (every claim → objection → proof), native feel, word economy, compliance. The reviewer JUDGES; **code decides** the verdict (threshold 4, fail-closed on any missing/malformed score), reusing the repo's gate-scoring convention (`scripts/hook_gate.py`). On a `REVISE` verdict, route only the failed ads back to the copywriter with their scores + weakest dimension + evidence + fix, keep the passing ads verbatim, and re-run. Full procedure, anchors, JSON contract, and decision rule: `references/copy-prelaunch-rubric.md`.

The gate sequence before a human ever sees a batch:

```
Phase 2 assembly → dct.json
  → Claim Gate (machine: every number sourced or cut)            [scripts/claim_gate.py --gate]
  → Copy Pre-Launch Rubric (fresh reviewer scores; code decides) [references/copy-prelaunch-rubric.md]
  → HITL Gate 3: human creative approval
```

### HITL Gate 3: Creative Approval

Show generated images and video previews grouped by batch. User approves or requests regeneration. Do not enter this gate until the Claim Gate has returned exit 0 (or carries a recorded operator override) AND the Copy Pre-Launch Rubric verdict is PASS (or a recorded operator override).

---

### Phase 4: DCT Tracker Compilation

> **10-5-5 note:** this separate compilation step is **3-2-2-only**. In 10-5-5 the manifest (`dct.json`) is already assembled in Phase 2, so this phase collapses — the resume model's `phase_4_sheet` is just the sheet write (`ad_concept_sheet_writer.py` reading `dct.json`). Run the markdown tracker below only for legacy 3-2-2 waves.

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
- `avatar-research` skill → `_brand/buyer-profile.md#micro-persona-map` (REQUIRED for DCT mode)
- `avatar-research` Phase 2.5 → awareness/sophistication evidence inside `_brand/buyer-profile.md` (REQUIRED — drives creative strategy)
- Client files: `_brand/buyer-profile.md`, `_brand/offer.md`, `_brand/brand-voice.md`, `_brand/icp.md`
- Swipe file (built during Phase 0.5 or from previous run)

**Downstream:**
- `[[video-concept-lab]]` — generate five video concepts, pick a winner, draft scripts, and define early character/product/style-sheet requirements. Invoke only after user confirms the batch/wave is video.
- `[[video-brief-normalizer]]` — create the client-facing Google Docs source brief, internal AI production brief, Approval Gate 2, and Video Factory handoff.
- `[[video-factory]]` — turn Approval Gate 2-approved handoffs into AI-generated video ads. Video Factory creates input-image prompts, input assets, beat sheets, model-specific prompts, and render approvals.
- `meta-ads-uploader` — upload creatives + copy to Meta (paused)
- `campaign-runner` — integrate into active campaign
- `ab-test-setup` — design follow-up tests on winning combinations

**Rerun cadence:** Every 4-6 weeks, or when creative fatigue detected.

---

## References

- `references/sophistication-creative-map.md` — L1-L5 creative strategy framework (Schwartz market sophistication)
- `references/static-image-method.md` — **active** Ferres-grounded static/carousel image-prompt method (MANDATORY on every static batch; replaces the retired `high-converting-static-brief.md`, archived at `_archive/references-pre-ferres/`)
- `references/copy-prelaunch-rubric.md` — fresh-context reviewer rubric run after the Claim Gate, before HITL Gate 3
- `references/angle-scoring-rubric.md` — Scoring matrix for angle ranking
- `references/headline-validation-checklist.md` — Full validation checklist
- Locale (casting, regulated documents, currency, local compliance) lives **per-client** at `clients/<project>/_brand/locale-rules.md` — load it IF PRESENT (template + SG example: `clients/_template/_brand/locale-rules.md`). The old skill-global `sg-cultural-guidelines.md` is archived at `_archive/references-pre-ferres/`.
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

---

## 10-5-5 Mode (Meta Flex) — Opt-In

> **Default is 3-2-2.** Everything above this section is the default behaviour and does not change. 10-5-5 is an OPT-IN mode entered only by an explicit flag/instruction (`--method 10-5-5`, or a wave spec that sets `dct_structure.method == "10-5-5"`). Absent that signal, the skill runs exactly as it does today: 3 creatives x 2 headlines x 2 copies = 12 combinations. Per operator decision D3 (2026-06-03), 10-5-5 is enabled per-client — **neezanizam and eugene have opted in; every other client stays 3-2-2** until it opts in. Full spec: `docs/methods/10-5-5/SPEC.md`.

### What changed and why

Meta retired the standalone DCT toggle (capped at 3 images / 2 primary texts / 2 headlines) and replaced it with the **Flex** ad format (up to 10 media / 5 primary texts / 5 headlines). "10-5-5" is Meta Flex's maximum. The method is unchanged — research persona, mine buyer language, draft angles, over-draft headlines, narrow, pair with visuals. Only the multipliers moved.

### Batch structure: 5 angles x 2 variations

A 10-5-5 wave = ONE Meta Flex ad set = **5 angles** (operator decision D1, locked `angle_model: "five_x_two"`).

| Component | Count | Rule |
|-----------|-------|------|
| **Angles** | 5 | Each angle is the strategic bet — 1 locked copy + 1 locked headline + 2 visual variations |
| **Creatives** | 10 (5 x 2) | Per angle: 2 image variations sharing the SAME locked copy + headline, only the visual differs |
| **Copies** | 5 (1/angle) | One LOCKED primary text per angle. No second copy variant |
| **Headlines** | 5 (1/angle) | OVER-DRAFT ~5 per angle, then NARROW to 1 locked. Keep the drafts in `headline_drafts[]` for audit |

This is the same "one DCT = one angle = one Ad Set = ONE CREATIVES row + ONE COPY row" rule the 3-2-2 path already follows (corrections 260420) — the 2 visual variants are a property of the single angle row, not separate rows. The only deltas from 3-2-2: 5 angles instead of 3 creatives, copy/headline are angle-scoped (1 each, not 2 each), and the 2 variations are visual-only.

### Tracker → canonical manifest

> **Canonical manifest is `dct.json`** (shape locked in `docs/dct-json-schema.md`), assembled in Phase 2 and consumed by the sheet writer + uploader. The `dct-tracker-10-5-5.schema.json` below is the **legacy mirror** the current emitter still writes; convert it with `scripts/migrate_tracker_to_dct.py` (10-5-5, lossless) until the Phase 2 emitter is repointed (blocker G1). Read this subsection as describing the field semantics — they carry over to `dct.json` 1:1.

The 10-5-5 tracker follows `references/dct-tracker-10-5-5.schema.json` (sample fixture: `references/sample-10-5-5-tracker.json`). It carries a `dct_structure` block (`method: "10-5-5"`, `angle_model: "five_x_two"`, the count consts) plus a `creatives[]` array of **exactly 5 entries, one per angle**. Each entry holds `copy_1` + `headline_1` (the locked pair), `headline_drafts[]` (the over-drafted pool), and a `variations[]` array of exactly 2 visual variants. `copy_2` and `headline_2` stay EMPTY in 10-5-5 (they exist only for 3-2-2 back-compat). Image prompts still follow the file-reference convention (corrections 260418) — never inline the full JSON in the tracker. Personas use the canonical `avatar-<N> (Display Name)` form per the client's `_brand/avatars/_index.md`.

### Sheet writer: 5 angle-rows per wave

`scripts/ad_concept_sheet_writer.py` already consumes `creatives[]` one-row-per-entry, so a 10-5-5 tracker emits **5 CREATIVES rows + 5 COPY rows** (one per angle) with no wide-column rebuild — Meta Flex's copy and headline are angle-scoped, so we add rows, not columns. Batch ids are unique per angle, e.g. `DCT010-A01` .. `DCT010-A05`. The CREATIVES row carries the angle-level strategy columns; the COPY row carries that angle's 1 copy in `COPY 1` and 1 headline in `HEADLINE 1` (`COPY 2` / `HEADLINE 2` left blank). The 2 visual variants and the headline drafts live in the tracker only — they are NOT written to the sheet.

> **Known-open (O1):** under Flex, Meta mixes the 10 images x 5 texts x 5 headlines inside ONE ad and returns performance at the Flex-ad / asset-breakdown level, not 5 clean per-angle rows. The 5 angle-rows are authoring/tracking rows (what we wrote, why); angle-level performance is read in the Meta UI until the `meta_puller` reporting rework lands. See SPEC.md §3.

### How the HITL gates change

Same five gates, recounted for the 5-angle shape:

- **Gate 1 (Angle Approval):** approve **5 angles** for the wave (not 2 per avatar). All five can sit on one avatar or spread across avatars per the wave spec.
- **Gate 2 (Batch Approval):** review **5 angles / 10 creatives / 5 copies / 5 headlines** — one card per angle showing the locked copy, the locked headline (plus the ~5 drafts that were narrowed), and the 2 visual variants. Replaces the 3-2-2 card's "3 creatives x 2 headlines x 2 copies / 12 combinations" line.
- **Gate 3 (Creative Approval):** review the 10 rendered visuals grouped by their 5 angles.
- **Gate 4 (Tracker Sign-off):** the tracker summary reports 5 angles, 10 creatives, 5 copies, 5 headlines per wave (not N x 12 combinations) before handoff to `meta-ads-uploader`.

Per operator decision D4, the first proof wave writes to NEW sheet test tabs — never the live CREATIVES / COPY tabs — and stays paused for founder review like every other wave.

<!-- skill-graph:start -->

## Related
<!-- auto-generated by scripts/link-skills.py — do not edit by hand -->

- [[headline-bank]] (skill, 0.14)

<!-- skill-graph:end -->
