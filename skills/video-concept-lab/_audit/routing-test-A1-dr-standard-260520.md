# Routing Test A1 — DR Standard (cold)

**Date:** 2026-05-20 | **Agent:** video-concept-seeder (cold dispatch, no workspace state)

---

## A. Selected loadout

- **methodology_loadout_id:** `dr_standard_concept`
- **Why this loadout:** Brief signals — `brief_type: "direct-response"` → DR family (SKILL.md §Brief Type Gate). `awareness_stage: "problem-aware"` + `sophistication_level: "L2"` → per SKILL.md §Brief Sub-Type Gate table: "unaware / problem-aware | any | `dr_standard_concept`". `script_mode: "voiceover"` → not singing (eliminates `dr_singing_concept`). Sophistication L2 not ≥ L3 → eliminates `dr_solution_aware_l3_concept`.
- **Routing line in SKILL.md that determined this (§Brief Sub-Type Gate table, lines 121-128):**

  > | `unaware` / `problem-aware` | any | `dr_standard_concept` |
  > | `solution-aware` | L1-L2 | `dr_standard_concept`; add `six_proof_types` if proof density material |
  > | `solution-aware` | L3+ | `dr_solution_aware_l3_concept`. If singing: `dr_singing_solution_aware_l3_concept` |

- **INDEX.md confirmation (lines 15-16):**

  > | Standard direct-response concepts | `dr_standard_concept` | `dr-foundation.md` + taxonomy + generation/scoring refs |

---

## B. Navigation log

| Order | File opened | Pointed-to-by | Why I loaded it | Lines read |
|---|---|---|---|---|
| 1 | `agents/video-concept-seeder.md` | Dispatch envelope (orchestrator) | Agent spec — adopt persona, learn methodology paths | 1–224 (full) |
| 2 | `skills/video-concept-lab/REFERENCE_GRAPH.json` | Agent spec line 19: "Read `SKILL.md` for boundary/routing, then read `REFERENCE_GRAPH.json` and the selected `methodology_loadout_id`" | Machine-readable loadout contract — source of truth for which files to load | 1–255 (full) |
| 3 | `skills/video-concept-lab/SKILL.md` | Agent spec line 12: "`/Users/jerel/.../video-concept-lab/SKILL.md`" — first file named in §"Your methodology lives at" | Boundary + routing; Brief Type Gate + Sub-Type Gate; determines loadout id | 1–297 (full) |
| 4 | `skills/video-concept-lab/INDEX.md` | SKILL.md §"Compact Runtime Routing" lines 88-93: "read two files only: 1. `REFERENCE_GRAPH.json` — machine-readable loadout contract. 2. `INDEX.md` — human-readable loadout table + path rules." | Human-readable loadout table to confirm dr_standard_concept; path rules (02_ag1-options/, concept-brief.json canonical) | 1–42 (full) |
| 5 | `skills/video-concept-lab/references/direct-response/dr-foundation.md` | REFERENCE_GRAPH.json node `dr_runtime`, loadout `dr_standard_concept` required_nodes[0]; INDEX.md line 16: "`dr-foundation.md` + taxonomy + generation/scoring refs" | Single runtime DR concept methodology — 6-module order, 3 Iman Pillars, Format-Last 4-gate rubric | 1–325 (full) |
| 6 | `skills/video-concept-lab/references/general/concept-taxonomy.json` | REFERENCE_GRAPH.json node `taxonomy`, loadout `dr_standard_concept` required_nodes[1] | Required concept field taxonomy — all enum ids for recommended_ad_format, presentation_context, style_profile, angle_family, creative_mechanism, proof_mode, script_mode | 1–460 (full) |
| 7 | `skills/video-concept-lab/references/general/concept-generation.md` | REFERENCE_GRAPH.json node `concept_generation`, loadout `dr_standard_concept` required_nodes[2] | Portable worker prompt with diversity rules, claim safety, Solution-Aware × Stage-3 checklist, output schema | 1–363 (full) |
| 8 | `skills/video-concept-lab/references/general/hook-and-format-rules.md` | REFERENCE_GRAPH.json node `hook_rules`, loadout `dr_standard_concept` required_nodes[3] | Hook field definitions (verbal/quiet-visual/rendered-text/subtitle), knob separation table, format enum | 1–87 (full) |
| 9 | `skills/video-concept-lab/references/general/scoring-and-analysis.md` | REFERENCE_GRAPH.json node `scoring`, loadout `dr_standard_concept` required_nodes[4] | V2V Matrix (6 criteria 1–10), hard penalties, tiebreakers, output schema | 1–114 (full) |
| 10 | `skills/video-concept-lab/references/general/success-criteria.md` | REFERENCE_GRAPH.json node `success_criteria`, loadout `dr_standard_concept` required_nodes[5] | AG1 quality bar — required pass criteria, scoring bar (42/60 min, 48/60 winner), failure conditions | 1–52 (full) |
| 11 | `skills/video-concept-lab/references/general/output-schema.md` | REFERENCE_GRAPH.json node `output_schema`, loadout `dr_standard_concept` required_nodes[6] | Markdown + JSON contract, saved folder path, approval-1.json shape | 1–260 (full) |
| 12 | `skills/video-concept-lab/references/direct-response/growthhub-creative-diversity-2026.md` | REFERENCE_GRAPH.json node `diversity_audit`, loadout `dr_standard_concept` required_nodes[7] | GrowthHub 5-pillar Entity ID diversification framework (Persona/Angle/Awareness/Format/Actor) | 1–132 (full) |
| 13 | `skills/video-concept-lab/references/general/creative-lanes-methodology.md` | REFERENCE_GRAPH.json loadout `dr_standard_concept` conditional_nodes[0] = `lanes`; triggered because TakeKine CLAUDE.md §Funnel Architecture states "`_brand/funnel.md` — MUST be read before any ad-concept, script, or landing-page work"; SKILL.md §2.5: "Apply only when `_brand/funnel.md` defines them" | Lane anatomy, selection protocol, angle_family compatibility table, cross-link stubs for L1/L3/L5 | 1–199 (full) |
| 14 | `skills/video-concept-lab/references/general/video-compression-by-duration.md` | REFERENCE_GRAPH.json loadout `dr_standard_concept` conditional_nodes[1] = `duration`; triggered by `duration_target_seconds: 15` in brief; creative-lanes-methodology.md §"Ad Length Budget Reality" line 56: "See `video-compression-by-duration.md` for beat-sheet specifics" | 15s beat sheet (PAS-15s + Transformation-15s), rung-lift capacity table (15s = 0.5 rung max) | 1–164 (full) |
| 15 | `clients/takekine/_brand/funnel.md` | SKILL.md §2.5 line 171: "Read `_brand/funnel.md` §'Strategic Ad Lanes'"; agent spec line 34: "Required reading for DR briefs with lane-enabled clients before Step 2.5"; creative-lanes-methodology.md §"Lane Selection Protocol" step 2 | Iman's 5 locked lanes + Persona→Lane→Handoff mapping — revealed critical awareness mismatch (see §E) | 1–180 (full) |

---

## C. Files in the loadout's required_nodes — verified loaded

`dr_standard_concept` required_nodes (8 total):

- [x] `dr_runtime` → `references/direct-response/dr-foundation.md` — loaded (order 5)
- [x] `taxonomy` → `references/general/concept-taxonomy.json` — loaded (order 6)
- [x] `concept_generation` → `references/general/concept-generation.md` — loaded (order 7)
- [x] `hook_rules` → `references/general/hook-and-format-rules.md` — loaded (order 8)
- [x] `scoring` → `references/general/scoring-and-analysis.md` — loaded (order 9)
- [x] `success_criteria` → `references/general/success-criteria.md` — loaded (order 10)
- [x] `output_schema` → `references/general/output-schema.md` — loaded (order 11)
- [x] `diversity_audit` → `references/direct-response/growthhub-creative-diversity-2026.md` — loaded (order 12)

Conditional nodes triggered and loaded:

- [x] `lanes` → `references/general/creative-lanes-methodology.md` — loaded (order 13); triggered by funnel.md presence
- [x] `duration` → `references/general/video-compression-by-duration.md` — loaded (order 14); triggered by `duration_target_seconds: 15`

---

## D. Files mentioned but SKIPPED (and why)

| File | Skipped because |
|---|---|
| `references/direct-response/core-framework.md` | REFERENCE_GRAPH.json node `dr_source_core`: `"role": "audit/source reference, not default runtime"`. Loadout `dr_standard_concept` lists it under `source_nodes_available_on_conflict` only — not required_nodes. INDEX.md line 27: "The older split files…are **audit/source references**". |
| `references/direct-response/lf8-market-translation.md` | Same as above — `dr_source_lf8` is `source_nodes_available_on_conflict` only. No conflict detected in this routing. |
| `references/direct-response/concept-stage-mandatory-checks.md` | Same — `dr_source_checks` is `source_nodes_available_on_conflict` only. |
| `references/general/stage-4-discrediting.md` | Required only in `dr_solution_aware_l3_concept`. Brief is `problem-aware` × L2 — gate does NOT fire. REFERENCE_GRAPH.json node `stage4_discrediting` is a required_node of `dr_solution_aware_l3_concept`, not `dr_standard_concept`. |
| `references/general/common-enemy-bridge.md` | Same as above — required in `dr_solution_aware_l3_concept` only. |
| `.claude/references/copywriting-os/frameworks/six-proof-types.md` | Required in `dr_solution_aware_l3_concept`. Brief L2 ≠ L3+. SKILL.md §Sub-Type Gate: "solution-aware | L1-L2 | dr_standard_concept; add six_proof_types **if proof density material**" — brief does not flag this. |
| `.claude/references/copywriting-os/reviewers/proof-density-audit.md` | Required in `dr_solution_aware_l3_concept` only — not this brief. |
| `references/direct-response/singing-ads-layer.md` | `dr_singing_concept` required_node. Brief `script_mode: "voiceover"` — not singing. |
| `references/general/brand-awareness-methodology.md` | `brand_awareness_concept` loadout. Brief is `direct-response` — DR gate fires, brand awareness gate explicitly skipped per SKILL.md §Brief Type Gate: "SKIP the DR stack entirely." |
| `references/general/context-pack.md` | REFERENCE_GRAPH.json node role: "intake repair only." No intake repair triggered. |
| `references/general/concept-input-packet.md` | REFERENCE_GRAPH.json node role: "intake repair and legacy alias reference." No legacy alias resolution needed — brief is inline. |
| `references/general/image-handoff.md` | `image_handoff_only` loadout. This is a routing test, not a production run. |
| `references/general/format-prompt-recipes.md` | Not a REFERENCE_GRAPH node. Referenced in output-schema.md as an optional format_recipe source. Not loaded — no recipe lock in brief. |
| `_brand/buyer-profile.md`, `_brand/offer.md`, `_brand/brand-voice.md`, etc. | These are client context files listed in agent spec lines 25-39. They are input-layer files, not methodology loadout nodes. A production run would require them; this is a routing trace only. |

---

## E. Routing clarity

- **Path obvious?** PARTIAL-ambiguous — the loadout selection was clean, but two decision points required judgment calls without explicit resolution criteria.

- **Where I guessed:**

  1. **Conditional node trigger for `lanes`:** REFERENCE_GRAPH.json lists `lanes` as a `conditional_node` but provides no trigger condition. SKILL.md §2.5 says "Apply only when `_brand/funnel.md` defines them." The agent spec says funnel.md is "Required reading for DR briefs with lane-enabled clients." TakeKine CLAUDE.md confirms funnel.md exists and MUST be read. I loaded `lanes` and then `funnel.md` — but the explicit instruction "load the `lanes` conditional node when X" is never stated in REFERENCE_GRAPH.json. I inferred: funnel.md exists + DR brief → lanes conditional fires. This is implied, not explicit.

  2. **Conditional node trigger for `duration`:** REFERENCE_GRAPH.json lists `duration` as a `conditional_node` with no trigger condition. dr-foundation.md §Layer 6 already inlines the 15s body structure. I loaded the file anyway because (a) brief declares `duration_target_seconds: 15`, (b) creative-lanes-methodology.md §"Ad Length Budget Reality" explicitly says "See `video-compression-by-duration.md` for beat-sheet specifics." But whether the seeder must load it vs use dr-foundation.md's inline table was ambiguous.

  3. **Read order between SKILL.md and REFERENCE_GRAPH.json:** Agent spec line 17 says "read `SKILL.md` for boundary/routing, then read `REFERENCE_GRAPH.json`." SKILL.md §"Compact Runtime Routing" line 88 says "read two files only: 1. REFERENCE_GRAPH.json. 2. INDEX.md." These are contradictory on whether SKILL.md or REFERENCE_GRAPH.json is first. I resolved this by reading agent spec's order (SKILL.md first, REFERENCE_GRAPH.json second), then INDEX.md — all three before loading any references.

- **Explicit vs implied routing decisions:**

  | Decision | Explicit or implied |
  |---|---|
  | DR family because `brief_type: "direct-response"` | Explicit — SKILL.md §Brief Type Gate |
  | `dr_standard_concept` because `problem-aware` × any | Explicit — SKILL.md §Brief Sub-Type Gate table |
  | Not `dr_singing_concept` because `script_mode: "voiceover"` | Explicit — REFERENCE_GRAPH.json `dr_singing_concept.when` |
  | Not `dr_solution_aware_l3_concept` because L2 | Explicit — SKILL.md table |
  | Load `lanes` conditional | Implied — no explicit trigger in REFERENCE_GRAPH.json |
  | Load `duration` conditional | Implied — no explicit trigger in REFERENCE_GRAPH.json |
  | Read SKILL.md before REFERENCE_GRAPH.json | Implied from agent spec; contradicted by SKILL.md itself |

---

## F. Missing routing / wished-existed

1. **REFERENCE_GRAPH.json lacks trigger conditions for conditional_nodes.** The graph lists `conditional_nodes: ["lanes", "duration"]` but provides no `when` field for conditionals (unlike `loadouts[].when` which is populated). An agent dispatched without knowing the client has funnel.md would not know to load `lanes`. Recommended: add `"conditional_trigger": "funnel.md present + DR brief"` to each conditional node in the graph.

2. **Read-order conflict between agent spec and SKILL.md.** Agent spec line 17 says read SKILL.md first, then REFERENCE_GRAPH.json. SKILL.md §"Compact Runtime Routing" says read REFERENCE_GRAPH.json first, then INDEX.md. These conflict. The agent spec should be canonical since it's the persona definition. SKILL.md should remove its own read-order directive or say "see agent spec for read order."

3. **Awareness mismatch not surfaced in routing.** The brief declares `awareness_stage: "problem-aware"` + `duration_target_seconds: 15`. The funnel.md (loaded at order 15) reveals: 15s ads can lift max 0.5 rung, but Problem-Aware → Solution-Aware (SL handoff requirement) is a 1-rung lift. This is a concept-blocking conflict. The REFERENCE_GRAPH.json has no node or rule that would surface this at the routing layer — it only appears after funnel.md is read during concept generation. A routing-layer pre-check rule in REFERENCE_GRAPH.json or SKILL.md's §Brief Sub-Type Gate would catch this earlier.

4. **`MP-04-tired-mom` persona mismatch.** The brief's `micro_persona_id: "MP-04-tired-mom"` maps to `Tired Mom Reset` in funnel.md's Persona→Lane table (Lanes 1/2/3, Medium handoff). However, funnel.md's 2026-05-19 retarget note explicitly says the pilot was retargeted to `Iron-Pill-Quitter (Solution-Aware × Stage-3)` for the cleanest SL handoff. `MP-04-tired-mom` at Problem-Aware with a 15s ad cannot reach the SL's Solution-Aware opening. This conflict should have been caught in `campaign-selection.json` but there is no campaign-selection.json in the forwarded paths. No routing rule explicitly halts on persona/awareness/funnel mismatch before reading funnel.md.

5. **No disambiguation rule for `ugc-flow` + 15s.** The brief declares `workflow_flow: "ugc-flow"` and `multi_clip_flow: true`. dr-foundation.md §Format-Last says to treat `workflow_flow` as a hypothesis. But for a 15s ad with ugc-flow, the single-clip vs multi-clip routing in the agent spec (step 2) would produce N×2 separate concepts for single-clip, or N with one hook each for multi-clip. The REFERENCE_GRAPH.json and SKILL.md provide no explicit gate on whether ugc-flow at 15s is "multi-clip" or "single-clip."

---

## G. Redundant loads (opened but didn't need)

1. **`video-compression-by-duration.md` (order 14)** — dr-foundation.md §Layer 6 already inlines the 15s rule: "15 seconds | hook + ONE pain image + ONE mechanism cue. Nothing else." The duration file is more detailed (PAS-15s beat sheet with timestamps), but the seeder already has sufficient 15s instruction from dr-foundation.md. The conditional trigger should specify "load when brief needs beat-sheet specifics beyond dr-foundation.md inline coverage" — which for a routing test with 15s is borderline.

2. **`INDEX.md` (order 4)** — REFERENCE_GRAPH.json is the machine-readable contract. INDEX.md is the human-readable version. Both contain the same loadout table. For a fully automated dispatch, only REFERENCE_GRAPH.json is needed. INDEX.md is useful for debugging but strictly redundant in production.

---

## H. Reference-tree trim/compress candidates (from THIS test)

| File | Verdict | Rationale |
|---|---|---|
| `references/direct-response/dr-foundation.md` | **KEEP — full** | Single runtime methodology file. Well-compressed. Replaces 3 older split files. |
| `references/general/concept-generation.md` | **MERGE candidate** | This is a portable worker prompt. It re-inlines all taxonomy enums already in `concept-taxonomy.json`. Significant redundancy. Consider: keep the diversity rules + claim safety + Solution-Aware checklist sections; strip the inlined taxonomy dictionary (point to concept-taxonomy.json instead). Estimated savings: ~60 lines. |
| `references/general/output-schema.md` | **KEEP — full** | Contains the approval-1.json shape, saved folder contract, and downstream brief-pack schema. Unique content not duplicated elsewhere. |
| `references/general/hook-and-format-rules.md` | **MERGE into concept-generation.md** | At 87 lines it covers hook field definitions and the knob-separation table. The hook field definitions are already in concept-generation.md's output schema. The knob-separation table is useful but could be a §appendix in concept-generation.md. Net savings: one fewer required_node load. |
| `INDEX.md` | **DEMOTE to "see-also"** | Fully redundant with REFERENCE_GRAPH.json for automated dispatch. Keep for human orientation; remove from agent read-order unless REFERENCE_GRAPH.json is unavailable or corrupt. |
| `references/direct-response/growthhub-creative-diversity-2026.md` | **KEEP but downgrade to conditional** | 132-line diversity audit framework. Useful for pack-level audit after concepts are drafted, not before. Could be triggered only when `concept_count >= 5` and `pack_audit` is requested — not as a required_node in `dr_standard_concept` since diversity rules are already stated in concept-generation.md §"Diversity rules." |
| `references/general/video-compression-by-duration.md` | **KEEP as conditional** | Good content, correctly gated. The conditional trigger in REFERENCE_GRAPH.json should be made explicit (e.g., `"conditional_trigger": "duration_target_seconds != null AND concept needs beat-sheet specifics"`). |
| `references/general/creative-lanes-methodology.md` | **KEEP — full** | Critical for lane-enabled clients. The cross-link stubs for L1/L3/L5 are clean. The `conditional_trigger` needs to be added to REFERENCE_GRAPH.json. |

---

## I. One-sentence routing verdict

**PARTIAL-ambiguous:** the loadout selection (`dr_standard_concept`) was unambiguous and explicit, but two conditional node triggers (lanes, duration) required inference with no explicit conditions in REFERENCE_GRAPH.json, and the brief contains a structural awareness × duration × funnel conflict that no routing layer rule surfaces before concept generation begins.

---

## Appendix: Awareness × Duration × Funnel Conflict (blocking)

This conflict would halt concept seeding in a production run and should be surfaced here for the orchestrator:

- **Brief declares:** `awareness_stage: "problem-aware"`, `duration_target_seconds: 15`, `micro_persona_id: "MP-04-tired-mom"`
- **funnel.md declares:** SL opens at Solution-Aware; 15s ads lift max 0.5 rung; Problem-Aware → Solution-Aware = 1-rung lift
- **Persona→Lane mapping:** `Tired Mom Reset` (Problem-Aware L2-L3) → Lanes 1/2/3 (Medium handoff, NOT cleanest)
- **funnel.md 2026-05-19 retarget note:** active pilot was retargeted to `Iron-Pill-Quitter (Solution-Aware × L3)` for cleanest handoff
- **Implication:** a 15s Problem-Aware concept with `MP-04-tired-mom` CANNOT reach the SL's opening rung. Concept would generate a rung gap. The agent spec does not have a routing rule that blocks this before concept generation; it would only surface during the lane selection step inside the seeder.
- **Orchestrator action needed:** either (a) change `duration_target_seconds` to 30s (minimum for 1-rung lift), or (b) change `micro_persona_id` to `iron-pill-quitter` and `awareness_stage` to `solution-aware` (which changes the loadout to `dr_solution_aware_l3_concept`), or (c) declare `lane_test_mode: true` for a specific lane 3 identity-match approach at 15s with a Medium handoff penalty accepted.
