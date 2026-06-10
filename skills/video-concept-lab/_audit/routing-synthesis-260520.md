# Routing Test Synthesis — video-concept-lab

**Date:** 260520
**Version:** v2 (post-verification — see §Verification Round 2 at bottom)
**Target:** `/Users/jerel/Documents/Jerel's brain/jerel's brain/Marketing/skills/video-concept-lab/SKILL.md` + `references/` tree (24 files)
**Persona:** `video-concept-seeder` (`/Users/jerel/.claude/agents/video-concept-seeder.md`)
**Persona justification:** SKILL.md L33 + INDEX.md L9 name `video-concept-seeder` as the single runtime concept generator. Routing-tester's 2026-05-20 corrections.md documents this exact target/persona pair as the canonical example of correct persona selection.
**Test cases:** 5 (cold) + 5 verification subagent reads
**Overall verdict:** **PARTIAL**

> **v2 note:** This synthesis was updated 260520 after 5 verification subagent reads. The earlier Tier 1/2/3 trim list was wrong on 3 of 5 files (verified-live content was misclassified as deadweight). §Recommended fixes and §Reference-tree trim/compress summary have been corrected. §Verification Round 2 documents the overturned calls in full.

---

## Test matrix

| Case | Archetype | Loadout | Files loaded | Verdict | Key finding |
|---|---|---|---|---|---|
| A1 | Happy path | `dr_standard_concept` | 11 (+funnel.md) | PARTIAL | Conditional triggers (`lanes`, `duration`) lack explicit `when:` conditions in graph |
| A2 | Brand counterpart | `brand_awareness_concept` | 9 | PASS | DR stack correctly skipped. Conditional `video-compression-by-duration.md` loaded but inapplicable (DR-native) |
| A3 | Singing × Solution-Aware L3+ | `dr_singing_solution_aware_l3_concept` | 14 | PASS | 3-level extends chain accumulated cleanly. Both forbidden_nodes blocked. |
| A4 | Pack audit | `pack_audit` | 4 | PARTIAL | Loadout exists in graph but invisible from agent spec + SKILL.md — would fall through to DR generation without operator forcing |
| A5 | Image handoff only | `image_handoff_only` | 1 (+nav) | PASS | Cleanest routing. DR foundation correctly skipped. Product reference gate reachable. |

---

## File load classification (across all 5 cases)

### Always loaded on DR paths (3+ of 3 DR cases — A1, A3)
- `dr-foundation.md` — runtime DR methodology ✓ correctly always-loaded
- `concept-taxonomy.json` — taxonomy fields enum
- `concept-generation.md` — N-concept method
- `hook-and-format-rules.md` — hook field schema
- `scoring-and-analysis.md` — V2V matrix
- `success-criteria.md` — quality bar
- `output-schema.md` — output contract

### Conditionally loaded (when trigger present)
- `creative-lanes-methodology.md` — A1, A2, A3 (loaded when `_brand/funnel.md` exists). Trigger condition **not explicit in REFERENCE_GRAPH.json** — A1 had to infer.
- `video-compression-by-duration.md` — A1, A2, A3 (loaded when `duration_target_seconds` declared). **DR-biased — A2 flagged loaded-but-inapplicable for brand-awareness.**
- `singing-ads-layer.md` — A3 only (loaded when `script_mode: "singing"`)
- `stage-4-discrediting.md` — A3 only (loaded on solution-aware L3+)
- `common-enemy-bridge.md` — A3 only (loaded on solution-aware L3+)
- `image-handoff.md` — A5 only (narrow scope)
- `brand-awareness-methodology.md` — A2 only

### Rarely / cross-purpose loaded (flag)
- `growthhub-creative-diversity-2026.md` — A1, A3, A4. **Required on every DR path AND pack-audit path.** Two agents independently flagged: this is a pack-audit-stage tool, not a per-concept-seed tool. Currently filed under `references/direct-response/` — misleading.

### NEVER loaded across all 5 cases (review required)
- `references/general/context-pack.md` — 0/5. Mentioned in SKILL.md §Context Load (L110) but never opened — agents went directly to the named context files.
- `references/general/format-prompt-recipes.md` — 0/5. No path of any tested loadout includes it. No explicit trigger.
- `references/general/concept-input-packet.md` — 0/5. SKILL.md L105 declares it a legacy alias. Confirmed unused — candidate for explicit deprecation note.
- `references/direct-response/core-framework.md` — 0/5. **By design** per SKILL.md L138 — audit/source reference only.
- `references/direct-response/lf8-market-translation.md` — 0/5. **By design** — audit-only.
- `references/direct-response/concept-stage-mandatory-checks.md` — 0/5. **By design** — audit-only.
- `references/direct-response/iman-take-260518.md` — 0/5. **By design** — audit-only.

The 4 DR audit-only files are correctly never-loaded in generation paths (that's the design). We did NOT test an evaluator-path scenario that would surface them — that's a gap in this test matrix, not necessarily a file problem.

### Forbidden (verified blocked)
- `references/general/script-and-music.md` — blocked under singing loadouts (A3 verified ✓)
- `references/general/suno-manual-target.md` — blocked under singing loadouts (A3 verified ✓)

---

## Routing failures

### Pattern A — Implicit narrow-scope routing (A4 + A5 convergent)
**Symptom:** Both `pack_audit` and `image_handoff_only` exist as first-class loadouts in `REFERENCE_GRAPH.json` and INDEX.md, but neither appears by NAME in the agent spec (`video-concept-seeder.md`) or in SKILL.md's "Brief Type Gate" / "Process" sections. Cold agents have to discover them by reading INDEX.md.
**Fix:** Add a **§Narrow-scope modes** (or §Dispatch modes) section to `video-concept-seeder.md` and SKILL.md naming all 7 loadouts with one-line triggers. Estimated effort: small (~10 lines per file).

### Pattern B — Implicit conditional triggers (A1)
**Symptom:** `REFERENCE_GRAPH.json` conditional nodes (`lanes`, `duration`) lack explicit `when:` conditions. Agent inferred `lanes` from "funnel.md exists" and `duration` from "`duration_target_seconds` is set" — but neither inference is documented. Cold agents will either over-load or under-load.
**Fix:** Add `when:` field to every conditional node in REFERENCE_GRAPH.json. Example:
```json
"creative_lanes_methodology": {"when": "client._brand.funnel.md exists AND declares strategic_ad_lanes"}
```
Estimated effort: small (~4 lines × N conditional nodes).

### Pattern C — Misfiled file (A3 + A4 convergent)
**Symptom:** `growthhub-creative-diversity-2026.md` lives under `references/direct-response/` but is a generic pack-audit reference used by the pack-audit loadout AND required on every DR generation path even though seeders don't need it at concept-seed stage.
**Fix:** Two parts.
  1. **Move** `growthhub-creative-diversity-2026.md` → `references/audit/` (new folder) or `references/general/`.
  2. **Demote** from required_node on `dr_standard_concept` to conditional_node triggered by `{pack_audit_requested: true}` OR remove entirely and let `pack_audit` loadout own it. This trims 1 file from every DR seed run.

### Pattern D — Loaded-but-inapplicable conditional (A2)
**Symptom:** `video-compression-by-duration.md` is conditionally loaded under `brand_awareness_concept` (because brief declares duration) but the file's templates are all DR-native (CTA-terminated beat sheets). A2 loaded it and discarded it.
**Fix:** Either (a) add a `brand-awareness-30s` section to the file, or (b) remove `video-compression-by-duration` from `brand_awareness_concept.conditional_nodes`. Recommended: (b), since brand-awareness duration logic differs structurally from DR.

### Pattern E — Untested path (gap, not failure)
**Symptom:** 4 audit-only DR files (`core-framework.md`, `lf8-market-translation.md`, `concept-stage-mandatory-checks.md`, `iman-take-260518.md`) are correctly never loaded by generators — by design. But we never tested an evaluator/conflict-resolution path that would actually surface them.
**Fix:** Add a 6th archetype on re-test — an evaluator dispatch invoking these audit refs — to confirm they're still reachable and current.

---

## Recommended fixes (priority order — v2, post-verification)

1. **[HIGH-IMPACT]** Add `§Narrow-scope modes` section to `video-concept-seeder.md` and `SKILL.md` naming all 7 loadouts. Surfaces `pack_audit` + `image_handoff_only` + `brand_awareness_concept` as first-class. Effort: SMALL.
2. **[HIGH-IMPACT]** Move `growthhub-creative-diversity-2026.md` from `references/direct-response/` to `references/general/` (NOT a new `audit/` folder — keep tree flat) AND demote from required-on-every-DR to `pack_audit` conditional. Effort: SMALL.
3. **[MEDIUM]** Add explicit `when:` triggers to every conditional_node in `REFERENCE_GRAPH.json`. Effort: SMALL.
4. **[MEDIUM]** Remove `video-compression-by-duration.md` from `brand_awareness_concept.conditional_nodes` (or add brand-awareness template). Effort: TRIVIAL.
5. **[ROUTING FIX, NOT FILE FIX]** Register `format-prompt-recipes.md` in `REFERENCE_GRAPH.json` + INDEX.md with explicit trigger. Live content, referenced by 4 other ref files, invisible from the graph. Effort: SMALL.
6. **[ROUTING FIX, NOT FILE FIX]** Add conditional trigger for `script-and-music.md` when `script_mode in ['voiceover', 'direct_to_camera', 'no_dialogue']`. It's the only doc for non-singing script direction — don't archive. Effort: SMALL.
7. **[CLEANUP]** Add a top-line clarification to `concept-input-packet.md`: "schema spec for `concept-brief.json` runtime files — not a runtime filename." Effort: TRIVIAL.
8. **[CLEANUP, SEPARATE]** Migrate 3 active TakeKine `concept-input-packet.json` workspace files to `concept-brief.json` filename. Effort: SMALL.
9. **[DELETE — SAFE]** Delete `suno-manual-target.md`. 100% absorbed into `singing-ads-layer.md`. Only references are `forbidden_nodes` blocks. Git history preserves it. Effort: TRIVIAL.
10. **[RE-TEST]** Add evaluator/conflict-resolution archetype to next test cycle to verify the 4 audit-only DR files are still reachable when evaluators need them.

---

## What survived the test (don't touch)

- **`dr-foundation.md`** as the runtime DR methodology hub — every DR test loaded it cleanly via the graph. The 2026-05-19 consolidation (absorbing singing-flow content into `singing-ads-layer.md` and blocking legacy `script-and-music.md`/`suno-manual-target.md` via `forbidden_nodes`) works as designed (A3 verified).
- **The 3-level `extends` chain** (`dr_singing_solution_aware_l3_concept` → `dr_solution_aware_l3` → `dr_standard`) — A3 navigated it without guessing. `extends` semantics are clear.
- **Brand-awareness branch SKIP rule** — A2 fired the Brief Type Gate immediately, never opened a DR file. The "MUST SKIP the DR stack entirely" language at SKILL.md L117 is doing its job.
- **`image_handoff_only` loadout's minimalism** — A5 loaded exactly 1 reference file. Narrow-scope mode works once discovered.
- **Forbidden_nodes enforcement** — A3 blocked both legacy files correctly.

---

## Reference-tree trim/compress summary (v2 — post-verification)

| File | Load freq | v2 Action |
|---|---|---|
| `direct-response/dr-foundation.md` | 2/5 (every DR) | KEEP — runtime DR hub |
| `general/concept-taxonomy.json` | 3/5 | KEEP — schema enum |
| `general/concept-generation.md` | 3/5 | KEEP |
| `general/hook-and-format-rules.md` | 3/5 | KEEP |
| `general/scoring-and-analysis.md` | 4/5 | KEEP |
| `general/success-criteria.md` | 4/5 | KEEP |
| `general/output-schema.md` | 4/5 | KEEP |
| `general/image-handoff.md` | 1/5 (A5 narrow) | KEEP — narrow mode |
| `general/brand-awareness-methodology.md` | 1/5 (A2) | KEEP — counterpart branch |
| `general/creative-lanes-methodology.md` | 3/5 conditional | KEEP — add explicit `when:` trigger |
| `general/video-compression-by-duration.md` | 3/5 conditional | KEEP — **remove from brand_awareness conditionals** |
| `general/stage-4-discrediting.md` | 1/5 (A3) | KEEP — L3+ chain |
| `general/common-enemy-bridge.md` | 1/5 (A3) | KEEP — L3+ chain |
| `general/context-pack.md` | 0/5 | **KEEP-AS-IS** ⚠ overturned. Verified: contains JSON schemas SKILL.md §Context Load deliberately delegates to. SKILL.md L110 explicit pointer. Complementary, not redundant. |
| `general/format-prompt-recipes.md` | 0/5 | **KEEP + ADD TRIGGER** ⚠ overturned. Verified: live content (213 lines), referenced by 4 other ref files. Invisible from graph — routing bug, not deadweight. |
| `general/script-and-music.md` | 0/5 (forbidden under singing) | **KEEP + ADD CONDITIONAL** ⚠ partial overturn. Singing content absorbed, but VO/avatar/no-dialogue/6-checkpoint sections are unique and load-bearing for 80% of paid ads. Add `script_mode in ['voiceover','direct_to_camera','no_dialogue']` trigger. |
| `general/suno-manual-target.md` | 0/5 (forbidden under singing) | **DELETE** — 100% absorbed into `singing-ads-layer.md`. Only refs are forbidden_nodes blocks. Safe. |
| `general/concept-input-packet.md` | 0/5 (legacy) | **KEEP + CLARIFY** ⚠ overturned. Referenced by 4 live agent files + 3 active TakeKine workspaces still use the legacy filename. Add top-line clarification ("schema spec, not runtime filename"). Migrate workspaces separately. |
| `direct-response/growthhub-creative-diversity-2026.md` | 3/5 (DR + audit) | **MOVE to `references/general/`, DEMOTE to pack_audit conditional** |
| `direct-response/singing-ads-layer.md` | 1/5 (A3) | KEEP |
| `direct-response/core-framework.md` | 0/5 (audit-only) | KEEP — by design (INDEX.md L26) |
| `direct-response/lf8-market-translation.md` | 0/5 (audit-only) | KEEP — by design |
| `direct-response/concept-stage-mandatory-checks.md` | 0/5 (audit-only) | KEEP — by design |
| `direct-response/iman-take-260518.md` | 0/5 (audit-only) | **KEEP-AS-AUDIT-REF** ⚠ overturned. Verified: 18KB primary-source Iman transcript. By-design audit reference per INDEX.md L26. 0/5 is correct behavior. |

**v2 verified trim potential: 1 file deleted** (`suno-manual-target.md`) **+ 1 file moved** (`growthhub-creative-diversity-2026.md` → `general/`) **+ 3 routing fixes** that surface dormant live content.

Down from the v1 estimate of 3-5 deletions. The lesson: **most "never loaded" files were routing bugs, not deadweight.**

---

---

## Verification Round 2 (post-subagent reads — 260520)

After the initial cold-routing tests flagged 5 files as "0/5 loaded → probable trim candidates," 5 verification subagents (Haiku, parallel, ~30s each) read those files end-to-end and grep'd for inbound references. **3 of 5 calls were overturned.** The synthesis above has been corrected.

### Calls overturned (was wrong to recommend trim)

| File | Initial v1 call | v2 verified call | Why I was wrong |
|---|---|---|---|
| `context-pack.md` | MERGE-INTO-SKILL.md | **KEEP-AS-IS** | Contains JSON schemas (Context Pack shape, Concept Input Packet shape, missing-context rule) that SKILL.md §Context Load deliberately delegates to via "see references/general/context-pack.md" at L110. 136-line implementation manual, not redundant prose. |
| `format-prompt-recipes.md` | DELETE-or-MERGE | **KEEP + ADD TRIGGER** | 213-line live file last modified May 15. Referenced by 4 other ref files (`hook-and-format-rules`, `brand-awareness-methodology`, `output-schema`, `concept-taxonomy`) but absent from `REFERENCE_GRAPH.json` + INDEX.md. Owns named recipe-template logic distinct from hook rules + taxonomy. Reason it never loaded: routing bug, not deadweight. |
| `concept-input-packet.md` | DEPRECATE/DELETE | **KEEP + CLARIFY** | 175-line schema spec. 8 references across 4 live agent files (`eval-buyer-fit`, `eval-video-flow-compliance`, `eval-video-universal`, `video-prompt-pack-builder`). 3 active TakeKine workspaces still use the `concept-input-packet.json` filename. Deletion would orphan live workspaces and break 4 agent file fallbacks. |
| `iman-take-260518.md` | (Tier 3 — "needs re-test") | **KEEP-AS-AUDIT-REF** | Verified by-design. 18KB primary-source Iman Gadzhi interview on seeder methodology. INDEX.md L26 explicitly classifies it (and 3 siblings) as audit-only — load only when evaluator requests primary evidence. 0/5 is correct behavior, not neglect. |

### Calls partially overturned

| File | Initial v1 call | v2 verified call | Nuance |
|---|---|---|---|
| `script-and-music.md` | DELETE-if-absorbed | **KEEP + ADD CONDITIONAL** | 70% absorbed into `singing-ads-layer.md` (singing content). 30% unique: VO Script + Avatar Acting Script + No-Dialogue Ad + Six-Checkpoint Script Analysis. Those 4 sections are the **only doc for non-singing scripts** in the skill — and ~80% of paid ads are non-singing. Archiving = data loss. Add a conditional load trigger for non-singing script_modes instead. |

### Calls confirmed (was right to recommend action)

| File | v1 call | v2 verified call | Status |
|---|---|---|---|
| `suno-manual-target.md` | DELETE | **DELETE** | 100% absorbed into `singing-ads-layer.md`. Only refs are `forbidden_nodes` blocks. Safe. |
| `growthhub-creative-diversity-2026.md` | MOVE + DEMOTE | **MOVE to `general/` + DEMOTE** | Confirmed misfiled. Move target: `references/general/` (NOT a new `audit/` folder). |

### Lesson logged

The cold-routing test's "files never loaded" signal is **necessary but not sufficient** evidence for trim. Without an inbound-reference grep + content-uniqueness check, the test conflates "deadweight" with "live-content-routing-bug." Future runs of `/routing-tester` against any skill should pair the load-frequency table with a parallel verification subagent fan-out for any file at 0/5 before recommending deletion.

This should probably be appended to `~/.claude/skills/routing-tester/corrections.md`.

---

## Audit file references

- `_audit/routing-test-A1-dr-standard-260520.md`
- `_audit/routing-test-A2-brand-awareness-260520.md`
- `_audit/routing-test-A3-singing-l3-260520.md`
- `_audit/routing-test-A4-pack-audit-260520.md`
- `_audit/routing-test-A5-image-handoff-260520.md`

---

## When to re-test

After applying any of the HIGH-IMPACT fixes (narrow-scope-modes section, growthhub file move/demote). Reuse the same 5 archetypes for regression. Add a 6th evaluator-path archetype to verify the 4 audit-only DR files are still reachable.
