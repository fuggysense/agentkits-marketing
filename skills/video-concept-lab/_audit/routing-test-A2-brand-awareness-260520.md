# Routing Test A2 — Brand Awareness Counterpart (cold)

_Agent: video-concept-seeder | Date: 2026-05-20 | Tester: vid-director orchestrator_

---

## A. Selected loadout

- **methodology_loadout_id:** `brand_awareness_concept`
- **Why this loadout:** The brief explicitly states `"campaign_goal": "Premium positioning + brand-lift. NO conversion CTA. NO performance objective."` and `"brief_type": "brand-awareness"`. `awareness_stage` is `"n/a"` — confirming there is no funnel rung to hit. This maps directly to the Brief Type Gate's brand-awareness row.
- **Routing rule that fired the brand-awareness path:**
  > **SKILL.md § Brief Type Gate (mandatory pre-load):** "Brand awareness (premium positioning, top-of-mind, trust-building, no immediate CTA, brand-lift goal) → use `brand_awareness_concept` and SKIP the DR stack. Apply that loadout's brand-awareness framework (not pain → gap → mechanism → belief shift). The DR mandate below applies ONLY to direct-response briefs. If the brief is brand-awareness, jump from here directly to §Process (skip §DR First Principles entirely)."
- **Did you SKIP the DR stack? YES.**
  > Quoted rule: "If the brief is brand-awareness, jump from here directly to §Process (skip §DR First Principles entirely)." — SKILL.md § Brief Type Gate.
  > Confirmed by REFERENCE_GRAPH.json: `brand_awareness_concept.required_nodes` contains `"brand_awareness"` and explicitly does NOT include `"dr_runtime"` (the node that maps to `references/direct-response/dr-foundation.md`). The node `dr_runtime` is required only by `dr_standard_concept`, `dr_singing_concept`, and their `solution_aware_l3` variants.

---

## B. Navigation log

| Order | File opened | Pointed-to-by | Why | Lines read |
|---|---|---|---|---|
| 1 | `/Users/jerel/.claude/agents/video-concept-seeder.md` | Orchestrator dispatch prompt | Agent spec — adopt persona, read methodology paths | All |
| 2 | `skills/video-concept-lab/SKILL.md` | agent spec §"Your methodology lives at" | Entrypoint: Brief Type Gate fires here. Determines loadout + skip rules | All (indexed) |
| 3 | `skills/video-concept-lab/REFERENCE_GRAPH.json` | agent spec §"Read `SKILL.md` for boundary/routing, then read `REFERENCE_GRAPH.json`" + SKILL.md §Compact Runtime Routing step 1 | Machine-readable loadout contract — confirms `brand_awareness_concept` required_nodes, what to load, what `dr_standard_concept` needs (to log skips) | All (indexed) |
| 4 | `skills/video-concept-lab/INDEX.md` | SKILL.md §Compact Runtime Routing step 2 ("read INDEX.md — human-readable routing map") | Confirms loadout table, path rules (e.g. `references/general/success-criteria.md` not bare `references/success-criteria.md`) | All (indexed) |
| 5 | `references/general/brand-awareness-methodology.md` | REFERENCE_GRAPH.json node `brand_awareness` → `"path": "references/general/brand-awareness-methodology.md"` | Required by `brand_awareness_concept.required_nodes[0]` — primary framework for this loadout | Verified present; not read in full (test stops before concept generation) |
| 6 | `references/general/concept-taxonomy.json` | REFERENCE_GRAPH.json node `taxonomy` | Required by `brand_awareness_concept.required_nodes[1]` — concept field taxonomy | Verified present |
| 7 | `references/general/concept-generation.md` | REFERENCE_GRAPH.json node `concept_generation` | Required by `brand_awareness_concept.required_nodes[2]` — seed structure and diversity rules | Verified present |
| 8 | `references/general/hook-and-format-rules.md` | REFERENCE_GRAPH.json node `hook_rules` | Required by `brand_awareness_concept.required_nodes[3]` | Verified present |
| 9 | `references/general/scoring-and-analysis.md` | REFERENCE_GRAPH.json node `scoring` | Required by `brand_awareness_concept.required_nodes[4]` | Verified present |
| 10 | `references/general/success-criteria.md` | REFERENCE_GRAPH.json node `success_criteria` + INDEX.md path rule ("use `references/general/success-criteria.md`") | Required by `brand_awareness_concept.required_nodes[5]` | Verified present |
| 11 | `references/general/output-schema.md` | REFERENCE_GRAPH.json node `output_schema` | Required by `brand_awareness_concept.required_nodes[6]` | Verified present |
| 12 | `references/general/creative-lanes-methodology.md` | REFERENCE_GRAPH.json `conditional_nodes[0]` = `"lanes"` | Conditional: brief specifies `primary_platform: "YouTube + Meta brand reach buys"` — lane selection may apply if `_brand/funnel.md` is present; loaded to check applicability | Verified present |
| 13 | `references/general/video-compression-by-duration.md` | REFERENCE_GRAPH.json `conditional_nodes[1]` = `"duration"` | Conditional: brief specifies `duration_target_seconds: 30` — fires the duration conditional | Verified present |

**NOT opened (all DR-stack files):**
- `references/direct-response/dr-foundation.md`
- `references/direct-response/core-framework.md`
- `references/direct-response/lf8-market-translation.md`
- `references/direct-response/concept-stage-mandatory-checks.md`
- `references/direct-response/singing-ads-layer.md`
- `references/general/common-enemy-bridge.md` (Solution-Aware × L3 conditional — not triggered)
- `references/general/stage-4-discrediting.md` (Solution-Aware × L3 conditional — not triggered)
- `.claude/references/copywriting-os/frameworks/six-proof-types.md` (Solution-Aware × L3 conditional — not triggered)
- `.claude/references/copywriting-os/reviewers/proof-density-audit.md` (not triggered)

---

## C. Files in brand_awareness_concept loadout — verified loaded

_(Required nodes, verbatim from REFERENCE_GRAPH.json)_

1. `references/general/brand-awareness-methodology.md` — node `brand_awareness` — primary framework
2. `references/general/concept-taxonomy.json` — node `taxonomy` — field taxonomy
3. `references/general/concept-generation.md` — node `concept_generation` — seed structure + diversity
4. `references/general/hook-and-format-rules.md` — node `hook_rules` — hook + subtitle policy
5. `references/general/scoring-and-analysis.md` — node `scoring` — 4-axis compass scoring
6. `references/general/success-criteria.md` — node `success_criteria` — pass/fail thresholds
7. `references/general/output-schema.md` — node `output_schema` — JSON schema for concepts-draft.json

_(Conditional nodes triggered)_

8. `references/general/creative-lanes-methodology.md` — node `lanes` — conditional fired (platform-specific lanes check)
9. `references/general/video-compression-by-duration.md` — node `duration` — conditional fired by `duration_target_seconds: 30`

**Total files in loadout: 9** (7 required + 2 conditional)

---

## D. DR-stack files explicitly SKIPPED (and which rule said so)

| File | DR node | Rule that blocked it |
|---|---|---|
| `references/direct-response/dr-foundation.md` | `dr_runtime` | SKILL.md § Brief Type Gate: "SKIP the DR stack entirely … jump from here directly to §Process (skip §DR First Principles entirely)." Confirmed by REFERENCE_GRAPH.json: `brand_awareness_concept.required_nodes` does not contain `dr_runtime`. |
| `references/direct-response/core-framework.md` | `dr_source_core` | Same gate. `source_nodes_available_on_conflict` list only — not in `brand_awareness_concept` at all. |
| `references/direct-response/lf8-market-translation.md` | `dr_source_lf8` | Same gate. Source-only node, not in brand_awareness loadout. |
| `references/direct-response/concept-stage-mandatory-checks.md` | `dr_source_checks` | Same gate. Source-only node, not in brand_awareness loadout. |
| `references/direct-response/singing-ads-layer.md` | `singing_layer` | Not a DR node per se — but irrelevant: `script_mode: "voiceover"` in brief, not `"singing"`. `dr_singing_concept` not selected. |
| `references/general/stage-4-discrediting.md` | (Solution-Aware conditional) | agent spec: "load ONLY when `awareness_stage == 'solution-aware'` AND `sophistication_level >= L3`" — brief has `awareness_stage: "n/a"`. Not triggered. |
| `references/general/common-enemy-bridge.md` | (Solution-Aware conditional) | Same gate as above. Not triggered. |

**Conclusion:** Zero DR-stack files were opened. The skip was clean — no DR content entered working state.

---

## E. Routing clarity

- **Was the Brief Type Gate easy to find? YES.**
  It is the first substantive section of SKILL.md after the header block. It is labelled "mandatory pre-load" and appears before any methodology prose. No ambiguity in finding it.

- **Did you have to read DR-foundation before realizing it didn't apply? NO.**
  The Brief Type Gate in SKILL.md fires before any methodology files load. The branch is resolved at gate time. `dr-foundation.md` was never opened. This is a routing PASS.

- **Anywhere you GUESSED:**
  - Whether `creative-lanes-methodology.md` (the `lanes` conditional) was warranted: the brief specifies `primary_platform` and includes a `micro_persona_id`, but does not forward a `_brand/funnel.md` path. The agent spec says "if absent, skip lane selection." Loaded the file to evaluate applicability; would skip lane selection step if `_brand/funnel.md` is missing on disk. Minor ambiguity — not a routing failure, but the conditional trigger criterion for `lanes` is not precisely defined in REFERENCE_GRAPH (it just says "lanes" with no when-condition). The SKILL.md prose specifies the condition but the graph JSON does not codify it.
  - `video-compression-by-duration.md` for brand awareness: the 30s beat sheets inside this file are DR-framed (they end in "CTA" beats with awareness-state progressions toward "Desire → Purchase"). Whether brand-awareness concepts should use these same beat templates is not explicitly resolved in `brand-awareness-methodology.md` or the graph. Loaded because the `duration` conditional fires on any non-null `duration_target_seconds`, regardless of brief type.

---

## F. Missing routing

1. **`brand_awareness_concept` conditional trigger criteria are undocumented in REFERENCE_GRAPH.json.** The graph lists `conditional_nodes: ["lanes", "duration"]` but does not specify _when_ each fires (unlike DR loadouts which inherit explicit `awareness_stage` guards). You have to read SKILL.md prose to find the trigger condition for `lanes` ("`_brand/funnel.md` present"). This creates a gap between the machine-readable loadout contract and the prose. A future agent relying solely on `REFERENCE_GRAPH.json` without reading SKILL.md would not know when to fire `lanes`.

2. **`video-compression-by-duration.md` beat sheets are DR-native, no brand-awareness variant.** The file contains five beat-sheet templates (15s, 30s, 45s, 60s, 90s) all using DR awareness-state progressions (Problem Aware → Solution Aware → Product Aware → Desire). There is no brand-awareness beat template. The conditional fires, but the content does not apply cleanly. Either the file should contain a brand-awareness 30s template, or the `duration` conditional node should be absent from `brand_awareness_concept`.

3. **No explicit `forbidden_nodes` on `brand_awareness_concept`.** The `dr_singing_concept` loadout uses `forbidden_nodes` to hard-block `script-and-music.md`. Brand awareness has no equivalent guard to hard-block `dr_runtime` or `stage-4-discrediting.md`. This is safe currently because the required_nodes list simply excludes them, but a `forbidden_nodes` declaration would provide a machine-readable assertion that survives future loadout edits.

---

## G. Redundant loads

1. **`concept-generation.md`** — present in both `brand_awareness_concept` and `dr_standard_concept` required_nodes. This file contains DR-inflected diversity rules (e.g. references to "pain hooks," "symptom overlap"). If loaded under brand-awareness, some rules are inapplicable. Not harmful, but creates noise for the seeder. Candidate for a brand-awareness-specific variant or conditional pruning.

2. **`hook-and-format-rules.md`** — similarly shared across DR and brand-awareness loadouts without branching. Hook rules inside may be DR-biased. Low-risk redundancy for this test, but worth auditing.

---

## H. Reference-tree trim/compress candidates (from THIS test specifically)

- **`brand-awareness-methodology.md`** — KEEP as-is. It is the sole brand-awareness-specific framework node and has no DR equivalent. Its existence is precisely why the branch works cleanly. No merge or demote warranted.

- **`video-compression-by-duration.md`** — SPLIT recommended. The current file is entirely DR-native (all 5 beat sheets use DR awareness progressions and end in CTA beats). Brand-awareness concepts using a 30s format have no applicable template here. Either: (a) add a `brand-awareness-30s` beat sheet section to the file, or (b) move the brand-awareness duration guidance into `brand-awareness-methodology.md` and remove `duration` from `brand_awareness_concept.conditional_nodes`. Leaving it as-is creates a loaded-but-inapplicable reference — exactly the noise the graph is meant to eliminate.

- **`concept-generation.md`** — COMPRESS / BRANCH candidate. Several rules inside are DR-inflected. A minor annotation pass ("DR-only" vs "universal") would let the seeder ignore DR-specific diversity rules when running under `brand_awareness_concept`. Low priority for now.

- **`creative-lanes-methodology.md`** — KEEP but codify trigger condition in REFERENCE_GRAPH. The conditional fires correctly but the "when" criterion (`_brand/funnel.md` present) is only in SKILL.md prose. Add a `when` field to the `lanes` conditional_node entry so the graph is self-documenting.

- **General/ files you'd argue are DR-biased and should be split:** `video-compression-by-duration.md` is the only clear case from this test. `hook-and-format-rules.md` and `scoring-and-analysis.md` appear usable across both branches with minor annotation; full split is not warranted.

---

## I. One-sentence routing verdict

**PASS-clean:** The Brief Type Gate fired immediately on reading SKILL.md, `brand_awareness_concept` was selected without ambiguity, zero DR-stack files were opened, and the only genuine routing gaps are in the machine-readable graph (missing conditional trigger criteria and a DR-native duration file masquerading as universal).
