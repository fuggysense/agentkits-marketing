# Creative Pipeline — 6-Stage Workflow

The end-to-end paid-ads creative loop. Six stages, six tools, HITL gates between each. No monolithic orchestrator — each skill owns its stage.

```
   ┌──────────────────────────────────────────────────────────────────────────┐
   │                                                                          │
   ▼                                                                          │
Research ──► Concept ──► Brief (video) + Hooks (static) ──► Create ──► Test  │
                ▲             ▲                                ▲              │
                │             │                                │              │
                └─── BETTER ──┘                                │              │
                              │                                │              │
                              └─────────── MORE ───────────────┘              │
                                                                              │
                              ┌─── NEW ──────────────────────────── Feedback ─┘
                              │
                              └──► back to Research
```

---

## Stage map

| # | Stage | Skill / Command | Output | HITL gate |
|---|---|---|---|---|
| 1 | **Research** (what they want) | `source-of-truth` · `/ads:source-of-truth <slug>` | `clients/<slug>/source-of-truth.md` (26 sections) + derivative files | Phase 4: 4 strategic decisions (KPI, core message, top-3 angles, first test variable) |
| 1.5 | **Headline Reservoir** (what to say — OPTIONAL) | `headline-bank` · `/ads:headlines <slug>` | `clients/<slug>/angles/wave-<N>-headline-bank.md` — 75+ headlines across 5 awareness levels × 10 angle banks, anchored to one mass desire | Phase 1: mass-desire selection (user picks or skill suggests top 3 candidates). Phase 5: approve bank before write |
| 2 | **Concept** (what to show) | `ad-concept-engine` Phase 1 · `/ads:concepts <slug>` | 6-8 angles per avatar, scored. Phase 2a reads headline-bank (if exists) as primary Meta headline reservoir | Phase 1 HITL Gate: pick top 2 angles per avatar |
| 3a | **Hooks** (statics) | `ad-concept-engine` Phase 2a | Per-creative: text-on-image hook + visual concept type + image prompt + headlines + copy | Phase 2 HITL Gate: per-batch approval |
| 3b | **Brief** (videos) | `ad-concept-engine` Phase 2b | Per-creative: 6-scene breakdown + performer notes + audio + graphics + technical specs + timing map + headlines + copy | Phase 2 HITL Gate: per-batch approval |
| 4a | **Create — statics** | `image-generation` (called by ad-concept-engine Phase 3a) | Image files at `clients/<slug>/campaigns/dct-YYMMDD/batch-NN/assets/` | Phase 3 HITL Gate: per-image approval |
| 4b | **Create — videos** | `video-director` (called by ad-concept-engine Phase 3b) | Video prompts (Sora 2 Pro / Kling / VEO) OR Vertex AI direct generation OR brief handed to UGC creator | Phase 3 HITL Gate: per-video approval |
| 5 | **Test** | `meta-ads-uploader` · `/ads:upload <slug>` | Ads created PAUSED in Meta Ads Manager | User reviews + un-pauses |
| 6 | **Feedback** | `feedback-router` · `/ads:feedback <slug> <wave>` | Routing decision (NEW/BETTER/MORE) + auto-appended learnings | User approves the routed next slash command |

---

## End-to-end run (Wave 1, new client)

```bash
# Stage 1 — Research
/ads:source-of-truth <slug>
# → produces source-of-truth.md, avatars/avatar-N.md, angles/wave-1.md, etc.
# → HITL: pick KPI, core message, top 3 angles, first test variable
# → ~10-15 min including HITL

# Stage 1.5 — Headline Reservoir (optional — skip for quick pilots)
/ads:headlines <slug>
# → asks: "Which mass desire?" → user picks or skill suggests top 3
# → generates 75+ headlines across 5 awareness levels × 10 angle banks
# → writes clients/<slug>/angles/wave-<N>-headline-bank.md
# → feeds ad-concept-engine Phase 2a as the primary Meta headline reservoir

# Stages 2 + 3 — Concept + Brief/Hooks (one command, multiple HITL gates)
/ads:concepts <slug>
# → Phase 1: generates 6-8 angles per avatar [HITL Gate 1: angle approval]
# → Phase 2a (per Static/Carousel batch): hooks + visual concepts + image prompts
# → Phase 2b (per UGC/Founder/VSL/Demo batch): full video briefs
# → [HITL Gate 2: per-batch approval]
# → produces clients/<slug>/campaigns/dct-YYMMDD/dct-tracker.json

# Stage 4 — Create
# 4a: ad-concept-engine Phase 3a auto-routes to image-generation per Phase 2a output
# 4b: ad-concept-engine Phase 3b auto-routes to video-director per Phase 2b output
# → [HITL Gate 3: per-creative approval]

# Stage 5 — Test
/ads:upload <slug>
# → ads created PAUSED in Meta Ads Manager
# → user reviews + un-pauses

# (wait 7-14 days for sufficient spend)

# Stage 6 — Feedback
/ads:feedback <slug> 1
# → reads CREATIVES + COPY sheet metrics + dct-tracker.json Performance table
# → routes: NEW / BETTER / MORE
# → auto-appends learnings to learnings.md + angles/iteration-log.md
# → outputs the recommended next slash command
```

---

## Loop closure (Wave 2 onwards)

After `/ads:feedback` returns a routing decision, the user runs the recommended next command. Each route re-enters the pipeline at a different stage:

### Route NEW — back to Research

```bash
/ads:source-of-truth <slug>     # Stage 1 refresh — buyer shifted, regenerate dossier
/ads:concepts <slug>            # Stages 2-3 again with refreshed inputs
/ads:upload <slug>              # Stage 5
/ads:feedback <slug> 2          # Stage 6 again
```

**Cost:** highest. Reserve for genuine buyer shifts (≥40% CPA delta from baseline OR all angles underperformed OR external market signal).

### Route BETTER — back to Brief/Hooks

```bash
/ads:concepts <slug> --refine "Angle 2: Wife-Initiator Reframe"
# → Phase 1 SKIPPED (winning angle locked)
# → Phase 2a + 2b re-run within winning angle, generating 5-8 new variants
# → focus: address identified failure pattern (low hold-rate, low CTR, format gap, etc.)
/ads:upload <slug>
/ads:feedback <slug> 2
```

**Cost:** medium. Most common route after Wave 1.

### Route MORE — back to Create

```bash
/ads:concepts <slug> --expand "DCT004"
# → Phase 1 + 2 SKIPPED (winning combo locked)
# → spawn 5-8 new variants mirroring DCT004 (same angle, format, hook pattern, copy framework)
# → vary: secondary visual element, performer cast, scene 1 entry, copy framework variant
/ads:upload <slug>
/ads:feedback <slug> 2
```

**Cost:** lowest. Use when winning combo is decisive and headroom to scale exists (frequency <2.5, CTR holding).

---

## HITL gate map

| Gate | Stage | What user reviews | What user can do |
|---|---|---|---|
| Phase 4 (source-of-truth) | Research | 4 strategic decisions: KPI, core message, top 3 angles, first test variable | Pick / "Other" custom answer per question |
| Phase 1 (ad-concept-engine) | Concept | 6-8 angles per avatar, scored | Pick top 2 per avatar / reject / replace / re-rank / move across avatars |
| Phase 2 (ad-concept-engine) | Brief + Hooks | Each batch as a card with headlines, copy, visual concept (statics) OR scene breakdown (videos) | Approve / edit headlines / change image concepts / swap visual styles / regenerate / adjust performer notes |
| Phase 3 (ad-concept-engine → image-generation / video-director) | Create | Generated images + video previews grouped by batch | Approve / request regeneration / adjust prompt / approve sub-set |
| Pre-launch (meta-ads-uploader) | Test | Ads created PAUSED in Meta Ads Manager | Review in Meta UI / un-pause / pause / kill |
| Post-feedback (feedback-router) | Feedback | Routing decision + recommended next command | Approve and run / override route / extend wave |

---

## What lives where

```
clients/<slug>/
  source-of-truth.md                               ← Stage 1 output (slow-moving foundation)
  source-of-truth-draft.json                       ← Stage 1 machine-readable summary
  avatars/avatar-N.md                              ← Stage 1 derivative (16-point breakdown each)
  angles/                                          ← Built upon SoT, iterates wave-by-wave
    README.md                                      
    wave-1.md, wave-2.md, ...                      ← Stage 1 derivative + Stage 6 wave updates
    hook-library.md                                
    iteration-log.md                               ← Stage 6 auto-appends here
  campaigns/dct-YYMMDD/
    dct-tracker.json                               ← Stages 2-3 output (creative specs + Performance table)
    batch-NN/
      assets/                                      ← Stage 4a (image files)
      video/                                       ← Stage 4b (video files / prompt logs)
    feedback-read.json                             ← Stage 6 aggregated read
    feedback-decision.json                         ← Stage 6 routing decision
  learnings.md                                     ← Stage 6 auto-appends here (wave conclusions)
  metrics-config.json                              ← Sheet IDs + tab gids for all stages
```

---

## Why decentralised (not one orchestrator)

We considered building a single `creative-pipeline` orchestrator skill that runs all 6 stages with one command. Rejected because:

1. **HITL gates need stage boundaries.** Each stage has different review criteria (strategic decisions vs creative direction vs image quality vs performance metrics). One orchestrator would either flatten the gates or become a state machine that's harder to debug than the underlying skills.
2. **Each skill is independently useful.** `image-generation` gets called by `tiktok-slideshows`, `linkedin-content`, `script-skill`. Burying it inside an orchestrator hides that reusability.
3. **Failure isolation.** If `meta-ads-uploader` breaks, we don't want it taking down the whole pipeline. Each stage runs in its own slash command — the user can resume at any boundary.
4. **`buyer-language-researcher` agent is a single-deliverable worker, not an orchestrator** — its own rules say "Don't over-engineer. Produce the dossier. One deliverable, done well." Orchestration would dilute its discipline.

The workflow doc IS the glue. Skills stay focused. HITL is preserved at every boundary.

---

## Multi-product readiness

Every stage now branches off `product_type` (set in `clients/<slug>/offer.md` Product Classification block: ecom / SaaS / service / info / agency / property):

- Stage 1: `source-of-truth` `references/section-synthesis-frameworks.md` Product-Type Branching matrix drives KPI defaults, proof types, CTA grammar, format weighting, urgency triggers per type
- Stages 2-3: `ad-concept-engine` `references/sophistication-creative-map.md` shows 6 product-type examples per Schwartz level
- Stage 6: `feedback-router` thresholds can be overridden per client in `metrics-config.json` (so a $14 ecom AOV doesn't get judged against a $1500 service CPA)

If `product_type` is missing from offer.md, every stage surfaces the gap and asks before defaulting.

---

## Related

- All 7 skills live under `skills/` — see individual SKILL.md for phase details (source-of-truth, avatar-research, headline-bank, ad-concept-engine, image-generation, video-director, meta-ads-uploader, feedback-router)
- All 6 slash commands live under `commands/ads/` — `source-of-truth.md`, `avatars.md`, `headlines.md`, `concepts.md`, `upload.md`, `feedback.md`
- This workflow doc is referenced from each SKILL.md "Integration with the 6-stage pipeline" section
- For multi-client wave coordination, see `.claude/workflows/primary-workflow.md`

---

## Niche Claim System (per industry)

When multiple clients operate in the same industry niche (e.g. `property-sg`), the pipeline enforces shared research + exclusive creative territory.

### The rule in one sentence

The niche **research pool is shared** — all clients benefit from every source mined and every phrase extracted. The **avatar slice claimed** and **buyer-language phrases used in copy** are exclusive to one client at a time.

### How it works

Two JSON files per industry in `swipe-files/<industry>/`:

| File | Purpose |
|---|---|
| `research-pool.json` | All sources mined + all extracted phrases. Tracks which client first mined each source and which client has claimed each phrase for copy use. |
| `avatar-registry.json` | All psychographic slices claimed by each client. New clients must claim a distinct slice. |

**Shared (anyone can use):**
- Sources listed in `sources_mined` — avoids re-mining the same subreddit/forum twice
- Phrases as research context — any client can cite a phrase in their strategy doc

**Exclusive (one client at a time):**
- `claimed_by_client` in `research-pool.json` — the phrase cannot appear in another client's ad copy
- `claimed_slices` in `avatar-registry.json` — the demographic + psychographic territory is locked

### Enforcement points

1. **`/ads:source-of-truth` Phase -1** — reads both files before research begins; injects source-avoidance and slice-conflict constraints into the research prompt
2. **`/ads:source-of-truth` Phase 5** — appends new sources + phrases to `research-pool.json`; adds new avatar slice to `avatar-registry.json`
3. **`big-angle-spotter` Step 6** — attaches `provenance` block to every headline; checks phrase claim before finalising top-3
4. **`/ads:source-of-truth` Phase 6** — citation verification via `scripts/verify-research-citations.py`; HITL gate blocks approval on failures

### Current property-sg claims

| Client | Slice | Phrases claimed |
|---|---|---|
| `neezanizam` | HDB upgraders 32-38, Malay-SG, dual income, upgrade anxiety | ph-001, ph-002, ph-003 (examples — replace with real IDs after populating research-pool.json) |

See `swipe-files/property-sg/avatar-registry.json` → `available_slices_property_sg` for unclaimed segments a new client can target.

### Adding a new client in property-sg

1. Run `/ads:source-of-truth <new-slug>` — Phase -1 will load both registries automatically
2. When prompted for avatar, pick from `available_slices_property_sg` or propose a new slice with a written non-overlap justification
3. After Phase 5 completes, both registries are auto-updated — no manual editing needed
4. Verify no phrase overlap with `neezanizam`'s `claimed_by_client` entries before copy goes live
