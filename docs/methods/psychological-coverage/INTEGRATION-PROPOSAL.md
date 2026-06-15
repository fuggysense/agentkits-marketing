# Psychological Coverage — Integration Proposal

> **⚠️ SUPERSEDED IN PART (260614 retro-tag proof).** Two load-bearing claims here failed against real cold waves: the "only genuinely new thing is one new dial — loud vs quiet" (TL;DR / idea #1) and shipping **Ought-Self as a cold angle** (idea #2). On both NeezaNizam DCT010 and Eugene DCT002 the loud dial never moved (brand contracts forbid loud) and duty is avatar-kill-listed cold. The vocab was re-cut → see `VOCABULARY.md` v2. Loud + duty are now **tripwires, not targets**; the cold map = valence/arc + mirror-vs-aspiration. Part 5's phased plan still holds *structurally*, but it assumed the full 4-room grid — build P1 against the v2 trimmed shape, not the grid below.

**Status:** PROPOSAL (nothing built). Partially superseded — see banner. Awaiting **"lock v2"**.
**Created:** 260613 · **Proof + re-cut:** 260614
**Author:** Claude (ground-truth map of 5 parallel repo readers + 2 source inputs)
**Sources fed in:** DTC "how we use Claude across creative strategy" mastermind transcript + the "Operational Efficiency / Psychological Coverage" long-form article (Valence × Self-Concept × Intensity).
**Extends:** `docs/methods/10-5-5/` (this sharpens the 10-5-5 diversity thesis; it is not a new pipeline).

---

## TL;DR (read this, skip the rest if pressed)

1. **You already own ~80% of the "operating system" the video describes.** Their CSOS-on-Notion = our `_brand/` folders. Their persona bank = our `MICRO-PERSONA MAP` + avatar files (ours is richer). Their script grader = our big-angle-spotter hardened gate. Their reasoning traces = our `corrections.md` + `feedback-decision.json` + `learnings.md`. Do **not** rebuild any of that on Notion/Supabase. It would fork your single source of truth.

2. **Two of the article's three "new" axes are mostly re-labels of axes you already track.**
   - **Valence (positive/negative)** is already in the six-emotional-states copy arc *and* big-angle-spotter's `emotional driver` tags. The only additive half is **AROUSAL** (high/low). The article's 4-quadrant model = valence × arousal; you have valence, you're missing arousal.
   - **Self-Concept (Actual / Ideal / Ought)** — Actual Self = sophistication L4 "mirror" + avatar "Image They Project"; Ideal Self = desire-state future-pacing + "Status They Aspire To". The genuinely under-used anchor is **OUGHT SELF** (duty / "do it for them" / social-expectation). **Correction after repo verification:** the Ought *material* already exists in avatars (Eugene avatar-1 §4 + §16, "a legacy to leave for our kids") — what's missing is shipping it as a deliberate *angle* (it's absent from the `Best Angle Types` shortlist). So this is surface-into-angle, not source-from-scratch. The article itself flags Ought as the under-used one.
   - **Language Intensity** collides with three controls you already run (funnel-stop logic, the L1–L5 CTA-pressure ladder, per-persona tonal contracts). It is the riskiest add. Recommend: don't make it a 4th dial — name it as the existing CTA-pressure ladder so we stop pretending it's new.

3. **The genuinely additive 20%, ranked:**
   - **(A) A coverage map + white-space report** — tag creative on the axes, show the operator where the account is clustered before they approve. This is the article's actual gift and it maps 1:1 onto Meta Andromeda's Creative Similarity penalty. Highest leverage.
   - **(B) Creation-time hypothesis capture** — one `hypothesis` field per angle, written *before* the wave, read back by feedback-router as predicted-vs-actual. This was already planned (ad-concept-engine corrections, 260418, gap #3) and never built. Closes the learning loop.
   - **(C) Live-account coverage report** — the video's "valence gap analysis": read live ads, tag each, show white space on the running account (not just the concept wave). Higher build cost. Defer until (A) proves out.

4. **What I'd refuse to build:** the Supabase vector "brain" (your corpus is tiny, access is sequential-per-client, maintenance > value); a parallel valence axis that duplicates six-states; a second coverage gate competing with the diversity map.

5. **One hard constraint:** big-angle-spotter's `run_pipeline.py` is a **symlink to a global, shared repo** (`~/AI workflows/big-angle-spotter/`). Its own SKILL.md says don't edit the pipeline to force new behavior — a change there hits every client. So coverage logic lives in the **orchestrator + diversity-map layer**, not baked into the global gate (unless behind an opt-in flag).

---

## Part 1 — What the two sources actually argue

**The video (DTC mastermind):** context > prompts. Build a single source of truth (CSOS), a framework/best-performer database with logged hypotheses, skills with routing logic + QA gates, and — the one idea they say to take away — **reasoning traces**: log *why* each strategic decision was made, bucket it (strategic decisions / hypothesis edits / context rules), feed it back so the system compounds like a senior strategist instead of a junior one. Plus a valence heatmap/gap analysis on the live account.

**The article:** volume is not the strategy; **psychological coverage** is. Meta Andromeda penalises Creative Similarity (psychologically redundant ads → higher CPMs). So map every ad across three axes — Valence Zone, Self-Concept Anchor, Language Intensity — find the white space, and produce *into the gaps* rather than making 50 variants of the same emotional message. Discovery before volume.

Both converge on the same operational move: **stop measuring output, start measuring coverage of the psychological landscape, and log why.**

---

## Part 2 — Map to what we already have (the 80%)

| Their concept | Our equivalent | Verdict |
|---|---|---|
| CSOS (Notion single source of truth) | `clients/<c>/_brand/` + `context-profile.json` + `buyer-profile.md` | **Have it.** Don't move to Notion. |
| Persona bank | `MICRO-PERSONA MAP` + `_brand/avatars/*.md` (12-pt + 16-pt + provenance) | **Have it, richer than theirs.** |
| Framework / best-performer DB | `ad-library-scraper` + `swipe-files/<industry>/` + `ferres-corpus` | **Have the scraping.** Weaker on "logged why-it-won → auto-feeds generation." |
| Script-writing skill (8 phases) | `headline-bank` + `ad-concept-engine` + `big-angle-spotter` | **Have it, arguably more rigorous** (citation audit, deterministic gate). |
| Script grader (10 criteria, hard floor) | big-angle-spotter `_GATE_DIMS` (5 dims, threshold 4) + `copy-prelaunch-rubric` | **Have it.** Theirs scores valence-consistency + self-concept; ours doesn't yet. |
| Reasoning traces (3 buckets) | `corrections.md` + `feedback-decision.json` + `iteration-log.md` + `learnings.md` | **~65% covered.** Gap = creation-time hypothesis. |
| Reporting skill + valence heatmap | `metrics-wire` + `sheets-updater` + `feedback-router` | **Have the metrics.** Missing the valence/coverage gap report. |
| Static generator (framework→Nano Banana) | `scripts/ad-images/` + `static-image-method` + `image-generation` | **Have it.** |

The takeaway: you don't need their architecture. You need three targeted grafts onto the architecture you have.

---

## Part 3 — The genuine 20% (what to actually build)

### (A) Psychological Coverage axis + white-space report — HIGHEST LEVERAGE

**What's new:** AROUSAL (the missing half of valence — a *new field*, do NOT reuse the existing `intensity 1-5` score in six-emotional-states, which rates one emotion's strength, not loud-vs-quiet) and OUGHT-SELF as a shipped angle (the *material* already exists in avatars; the angle doesn't). Everything else is a re-label.

**The single best integration point is the diversity map** (`clients/<slug>/angles/diversity-map-<date>.md`). It already exists *specifically* to force psychological spread, already tags each reason-to-buy with `awareness level` + `emotional driver`, and already enforces a "≥6 distinct entries" coverage rule + a 1%-remix de-dup (which is literally the Andromeda-similarity defense). We extend it, we don't replace it.

Concrete moves:
1. **Tag once, upstream.** Add `valence_zone` (2×2: valence × arousal), `self_concept_anchor` (Actual/Ideal/Ought), and a `coverage_tag` to:
   - `avatar-template.json` (the one machine-readable schema) + the per-avatar **Quick Reference** table as evidence-cited rows — but as a *persona default*, obeying the existing Quote-Provenance gate (inferred values carry `[HYPOTHESIS - not customer language]`).
   - each **diversity-map entry** as two more per-entry tags (this is where the spread actually gets forced).
2. **Extend the coverage rule.** "≥6 distinct entries" → "…and the banked set spans both arousal levels + all 3 self-concept anchors." This stays a **set-level check**, not a per-angle gate (see Part 4 for why).
3. **Show the operator the map at HITL Gate 1 (Angle Approval).** When banked angles first meet the human (`ad-concept-engine` SKILL.md:355), print a coverage tally: "Wave covers high-arousal/negative ✓✓✓✓, low-arousal/positive ✗, Ought-self ✗." That's the article's "stare at the white space" moment, made operational. Advisory — the human decides whether the gap is worth filling.
4. **Make the live account auditable.** Add optional columns to the **CREATIVES** sheet tab (`VALENCE ZONE`, `SELF CONCEPT ANCHOR`, `COVERAGE TAG`) following the existing optional-column pattern (same guard as `CANVA LINK`). Now the running account can be plotted on the map — the article's "pull up your ad account."

### (B) Creation-time hypothesis capture — closes the learning loop

The reasoning-trace system is ~65% built. The **one** real gap: we log what *won* (feedback-decision.json) but never recorded what we *predicted*, so we can't compare. Minimum-viable fix, already planned and never shipped:
1. Add a `hypothesis` field to each angle in `dct.json` at creation time (1–2 sentences: what we expect + why, keyed to the axis values).
2. Have `feedback-router` read it back into `feedback-decision.json` next to `failure_pattern_identified` as **predicted-vs-observed**.

One field + one read. Lives inside existing JSON artifacts. Zero new infrastructure. This is the video's "reasoning trace" idea, scoped to the only part that isn't already covered.

### (C) Live-account coverage / valence gap report — DEFER

The video's "download all live ads → tag → show gaps." Real value, but it needs creative-level Meta reads + a tagging pass over existing ads. Build cost is higher and it depends on (A)'s tagging vocabulary being settled. Defer until (A) is proven on one wave.

---

## Part 3.5 — Structural coverage layer (persona hierarchy) — added 260613 per Jerel

Jerel's "1 persona, 48 unique ads" grid (Macro → Micro → Angle → Vehicle) is the **structural** twin of the psychological coverage map. Both are columns on the same CREATIVES rows; both roll up into a grid view. The skeleton the emotional tags hang on.

**Mapping to the current pipeline (NeezaNizam, live 10-5-5):**

| Grid layer | Current home | Action |
|---|---|---|
| Macro persona (umbrella) | **Missing** — avatars are flat `avatar-<N>` siblings | Add one `MACRO PERSONA` grouping (umbrella over existing avatars). NOT a re-code. |
| Micro persona | `avatar-<N>` = one DCT = one ad set; sheet `PERSONA` column | Keep as-is (canonical Avatar Naming Contract) |
| Angle | `A01–A05` (the 5 texts in 10-5-5) | Already tracked in `ANGLE` |
| Vehicle | `FORMAT` column (UGC/static/founder) + image pool | Promote FORMAT to a deliberate coverage axis |

**Two hard constraints:**
1. **No persona reinvention / Avatar Naming Contract** (NeezaNizam CLAUDE.md). The macro layer is an additive *umbrella that references existing `avatar-<N>`* — never a rename to P1.1. Adopt the other agency's structure, not their labels.
2. **Meta flex can't give per-cell conversions.** Per NeezaNizam CLAUDE.md, a 10-5-5 Flexible Ad yields per-image/text/headline CTR *directional only — no per-combination, no conversions*, plus one blended ad-set CPL. So the 48-grid is a **briefing/coverage map + directional CTR read**, NOT a 48-row conversion scoreboard. True per-cell conversion = isolate the cell into its own ad set (trades 10-5-5 efficiency for clean attribution). Do not over-promise the grid as conversion truth.

**Where it lives:** `MACRO PERSONA` column on CREATIVES (alongside the coverage tags); the umbrella definition in each client's `_brand/avatars/_index.md` + `avatar-coverage-map.md` (which already do cross-avatar coverage). The grid view is a rollup/pivot of CREATIVES — candidate new tab `COVERAGE GRID` or a generated view, P1/P2.

**Macro/micro framework — refinement (260613).** The framework = write at the MICRO (specificity → Andromeda reach), organize/budget/coverage-check at the MACRO. The repo already runs it half-formalized: `avatar-<N>` files = micros (built); `buyer-profile.md` cohort sections (THE CORE PROBLEM, TOP 5 EMOTIONS) = the macro psychology (unlabelled); and **NeezaNizam's two metrics-campaigns (`buyer-funnel` vs `asset-progression`) ARE two macros** — the tab split is the macro layer. So the work is *naming and connecting* layers already in use, not building new ones.

- **Sheet:** micro = existing `PERSONA` column; macro = the tab/metrics-campaign by default. Add a `MACRO PERSONA` *column* only when one tab holds >1 macro. The real win is two-altitude rollup (by-macro on top of by-micro), not a new column.
- **Pipeline:** `macro_persona` flows as one inherited field. avatar-research labels the cohort layer + each avatar declares `macro:`; big-angle-spotter coverage gains a macro level ("all micros under this macro briefed?"); headline-bank UNCHANGED (copy stays micro-level); ad-concept-engine keeps one-DCT=one-micro=one-adset and carries `macro_persona` in dct.json; sheet writer one passthrough; feedback-router gains macro-level rollup ("Sellers CPL half of Buyers → shift budget").
- **Earns-its-place filter:** micros everywhere (already have them); macro layer ONLY where there's >1 macro. Eugene (1 umbrella, 2 micros) = leave macro as a one-line label, no column. NeezaNizam (2 macros) = formalize. Don't impose a macro column on single-macro clients.

---

## Part 4 — What NOT to build (the skeptical core)

- **Don't add a parallel valence axis.** Positive/negative is already double-encoded (six-emotional-states arc + emotional-driver tags). Only model valence as a 2×2 *where it adds the arousal axis*. Otherwise you're re-labeling.
- **Don't make Language Intensity a 4th temperature dial.** It collides with funnel-stop logic, the L1–L5 CTA-pressure ladder, and per-persona tonal contracts. Map it onto that machinery, or you'll generate contradictory CTA-temperature instructions.
- **Don't add Self-Concept as a competing ladder.** L4 says "mirror their exact situation" (= Actual Self); a flat "Ideal Self = aspiration" tag will issue contradictory lead-with instructions. Position self-concept as a *modifier* on the sophistication ladder, and only Ought-Self as net-new content.
- **Don't build the vector DB.** Corpus is tiny, access is sequential-per-client, maintenance exceeds value. Fix the capture (B) before building retrieval around it.
- **Don't bake coverage into the global gate as strict-AND.** Adding dims to `_GATE_DIMS` tightens an AND-gate that *already* HALTs Eugene at 4/5 winners. More strict dims = more HALTs. Keep coverage as a set-level spread check. If you ever want hard per-angle gating, use the deferred weighted-floor aggregation (HANDOFF §6.5), not strict-AND.
- **Don't edit `run_pipeline.py` to force coverage.** It's a global symlink. Coverage lives in the orchestrator + diversity-map, or behind an opt-in flag.

---

## Part 5 — Phased build plan

**P0 — Vocabulary lock (no code).** Write the axis definitions: arousal high/low anchors, Ought-Self definition + how it differs from Relationship-Impact-on-Parents, and the explicit statement that "Language Intensity = existing CTA-pressure ladder." One reference file under this folder. ~1 session. *Gate: Jerel signs off the vocabulary before any tagging.*

**P1 — Coverage tagging + advisory report (the article's core).**
- avatar-template.json + Quick Reference rows (persona defaults, provenance-gated).
- diversity-map per-entry tags + extended coverage rule.
- HITL Gate 1 coverage tally print.
- CREATIVES sheet optional columns + `_adapt_dct_json()` passthrough + `_build_creatives_row()` writes.
- Run it on **one** Eugene or NeezaNizam wave as the proof. ~2–3 sessions, phased ≤5 files each.

**P2 — Hypothesis capture (the learning loop).**
- `hypothesis` field in dct.json at creation.
- feedback-router reads it back as predicted-vs-observed.
- ~1 session.

**P3 (optional, later) — Live-account coverage report.** Only after P1 proves the tagging vocabulary holds up against a real wave.

---

## Part 6 — Open design decisions (my recommendation on each)

1. **Persona-scoped or creative-scoped tags?** → **Both.** Persona *default* in the avatar (home base), per-creative *override* in the diversity-map/dct.json. Mirrors how awareness/sophistication already work.
2. **Valence flat or 2×2?** → **2×2 (valence × arousal).** Flat is redundant; only arousal is additive.
3. **Self-concept: all three or just Ought?** → **Coverage tag spans all 3** (so you can see the spread); **avatar content work focuses on surfacing Ought-Self** (the only missing one).
4. **Intensity: include or drop as a standalone axis?** → **Drop as standalone.** Document it as the existing CTA-pressure ladder.
5. **Coverage check: advisory or code-enforced?** → **Advisory first** (orchestrator checklist + HITL Gate 1 report). Code-enforce only if it proves out — 10-5-5 is still Phase 1 with zero proven results; don't over-constrain an unvalidated shape, and respect the global-symlink caution.

---

## Appendix — Exact insertion points (for the build session)

**avatar-research / brand context**
- `clients/<c>/_brand/avatars/avatar-template.json` — add typed keys `valence_zone` (valence × arousal — arousal is a NEW field, not the existing `intensity 1-5`), `self_concept{actual,ideal,ought}` (or scalar `self_concept_anchor`), `coverage_tag`. (Intensity intentionally omitted — it's the existing CTA-pressure ladder.)
- Ought-Self is **surface-into-angle, not source-from-scratch**: the material already sits in avatar files (e.g. `avatar-1-cash-anxious-upgrader.md` §4 + §16). P1 work = add it to the `Best Angle Types` shortlist + tag it, not re-research it.
- Per-avatar **Quick Reference** table — add evidence-cited rows beside `Awareness Level` / `Sophistication Level`. Provenance gate applies.
- `_brand/avatars/sophistication-map.md` + `avatar-coverage-map.md` — the existing cross-avatar coverage files; home for the roster-level coverage check.

**big-angle-spotter (orchestrator/diversity-map layer ONLY — not run_pipeline.py)**
- `clients/<slug>/angles/diversity-map-<date>.md` — per-entry tags (currently `awareness level` + `emotional driver` at SKILL.md L186–188); add `valence_zone` + `self_concept_anchor`. Extend the "≥6 distinct entries" rule (L192) to per-axis spread.

**ad-concept-engine**
- HITL Gate 1 Angle Approval (SKILL.md:355) — coverage tally print; ride `pipeline_state.py advance --gate-status` on `gate_1_angles`.
- `dct.json` per-angle — add `valence_zone`, `self_concept_anchor`, `coverage_tag`, and `hypothesis` (P2). Update `docs/dct-json-schema.md` + `dct-tracker-10-5-5.schema.json` together.
- Conductor `event-log.jsonl` — optional `reasoning` field on advance entries.

**Google Sheet (`scripts/ad_concept_sheet_writer.py`)**
- `CREATIVES_STRATEGY_COLUMNS` (L90–99) — append `VALENCE ZONE`, `SELF CONCEPT ANCHOR`, `COVERAGE TAG`.
- `_build_creatives_row()` (L478–507) — add `row[...] = batch.get(...)` after the PERSONA entry, in the optional-column block.
- `_adapt_dct_json()` (L341–376) — add passthrough lines so the 10-5-5 `dct.json` path carries the new fields.
- `_validate_headers()` (L448–474) — guard the new columns as optional (same as `CANVA LINK`).
- `dct-tracker-10-5-5.schema.json` — add the four optional properties; none in `required[]`.

**feedback-router (P2)**
- Phase 1 Performance Read — aggregate by `valence_zone` / `self_concept_anchor`.
- Phase 3 Learnings Capture + `learnings-template.md` — persist construction-WHY keyed to won/lost axis values.
- `feedback-decision.json` — read back the creation-time `hypothesis` as predicted-vs-observed.

**Schema-1.0 caveat:** the 10-5-5 `--top-n` change (`pipeline-diff-proposal.md`) is still UNAPPLIED; the gate emits/banks against 10 angles regardless of 3 vs 5 winners, so a coverage check works unchanged in both 3-2-2 and 10-5-5.
