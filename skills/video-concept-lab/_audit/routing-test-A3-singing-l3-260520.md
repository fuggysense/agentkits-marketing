# Routing Test A3 — Singing × Solution-Aware L3+ (cold)

_Date: 2026-05-20 | Agent: video-concept-seeder cold-routing audit_

---

## A. Selected loadout

- **methodology_loadout_id:** `dr_singing_solution_aware_l3_concept`
- **extends chain:**
  1. `dr_singing_solution_aware_l3_concept` extends `dr_solution_aware_l3_concept`
  2. `dr_solution_aware_l3_concept` extends `dr_standard_concept`
  3. `dr_standard_concept` has no parent (base DR loadout)
- **Chain depth:** 3 loadouts (combined → solution-aware L3 → standard)
- **Did you load BOTH conditions' references?** YES — singing condition (`singing_layer`) + Solution-Aware L3 condition (`stage4_discrediting`, `common_enemy`, `six_proof_types`, `proof_density`) both present in the accumulated required_nodes set.

---

## B. Navigation log

| Order | File opened | Pointed-to-by | Why | Lines |
|---|---|---|---|---|
| 1 | `skills/video-concept-lab/SKILL.md` | agent spec | Entrypoint — boundary, brief type gate, sub-type gate table, routing | ~320 |
| 2 | `skills/video-concept-lab/REFERENCE_GRAPH.json` | SKILL.md §Compact Runtime Routing | Machine-readable loadout contract — single source of truth | 145 |
| 3 | `skills/video-concept-lab/INDEX.md` | SKILL.md §Compact Runtime Routing | Human-readable loadout table + path rules | ~50 |
| 4 | `REFERENCE_GRAPH.json` → `dr_singing_solution_aware_l3_concept` → `extends: dr_solution_aware_l3_concept` | REFERENCE_GRAPH.json | Recurse chain: resolve parent required_nodes | — |
| 5 | `REFERENCE_GRAPH.json` → `dr_solution_aware_l3_concept` → `extends: dr_standard_concept` | REFERENCE_GRAPH.json | Recurse chain: resolve grandparent required_nodes | — |
| 6 | `references/direct-response/dr-foundation.md` | dr_standard_concept required_nodes[dr_runtime] | Runtime DR methodology — spine, modules, checklist | ~200 |
| 7 | `references/general/concept-taxonomy.json` | dr_standard_concept required_nodes[taxonomy] | Required concept field taxonomy | — |
| 8 | `references/general/concept-generation.md` | dr_standard_concept required_nodes[concept_generation] | Seed structure and diversity rules | — |
| 9 | `references/general/hook-and-format-rules.md` | dr_standard_concept required_nodes[hook_rules] | Hook, rendered text, subtitle policy | — |
| 10 | `references/general/scoring-and-analysis.md` | dr_standard_concept required_nodes[scoring] | Concept scoring — V2V matrix | — |
| 11 | `references/general/success-criteria.md` | dr_standard_concept required_nodes[success_criteria] | AG1 quality bar | — |
| 12 | `references/general/output-schema.md` | dr_standard_concept required_nodes[output_schema] | Concept pack shape | — |
| 13 | `references/direct-response/growthhub-creative-diversity-2026.md` | dr_standard_concept required_nodes[diversity_audit] | Pack-level diversity audit | — |
| 14 | `references/general/stage-4-discrediting.md` | dr_solution_aware_l3_concept required_nodes[stage4_discrediting] | 4 moves for solution-aware L3+ (anger/validation/mechanism/pain stacking) | ~120 |
| 15 | `references/general/common-enemy-bridge.md` | dr_solution_aware_l3_concept required_nodes[common_enemy] | Named enemy composition + Schwartz authenticity gate | ~120 |
| 16 | `.claude/references/copywriting-os/frameworks/six-proof-types.md` | dr_solution_aware_l3_concept required_nodes[six_proof_types] | Proof type taxonomy | — |
| 17 | `.claude/references/copywriting-os/reviewers/proof-density-audit.md` | dr_solution_aware_l3_concept required_nodes[proof_density] | Proof stack density audit | — |
| 18 | `references/direct-response/singing-ads-layer.md` | dr_singing_solution_aware_l3_concept required_nodes[singing_layer] | Singing DR spine rules, word budgets, Suno schema, multi-character labels | ~280 |
| 19 | `references/general/creative-lanes-methodology.md` | dr_standard_concept conditional_nodes[lanes] | Client funnel lane mapping — triggered because brief has `_brand/funnel.md` for DR | — |
| 20 | `references/general/video-compression-by-duration.md` | dr_standard_concept conditional_nodes[duration] | Duration-based beat compression — triggered because `duration_target_seconds: 20` | — |

**Note on conditional_nodes:** `lanes` fires because takekine/CLAUDE.md confirms `_brand/funnel.md` is present and required for DR briefs. `duration` fires because `duration_target_seconds` is specified in the brief. Both belong to `dr_standard_concept`'s `conditional_nodes` and accumulate through the chain.

---

## C. Loadout's extends-chain — verified loaded

### From dr_standard_concept (base)
- `references/direct-response/dr-foundation.md` ← `dr_runtime` node
- `references/general/concept-taxonomy.json` ← `taxonomy` node
- `references/general/concept-generation.md` ← `concept_generation` node
- `references/general/hook-and-format-rules.md` ← `hook_rules` node
- `references/general/scoring-and-analysis.md` ← `scoring` node
- `references/general/success-criteria.md` ← `success_criteria` node
- `references/general/output-schema.md` ← `output_schema` node
- `references/direct-response/growthhub-creative-diversity-2026.md` ← `diversity_audit` node
- _(conditional)_ `references/general/creative-lanes-methodology.md` ← `lanes`
- _(conditional)_ `references/general/video-compression-by-duration.md` ← `duration`

### From dr_solution_aware_l3_concept extension (adds to base, does NOT replace)
- `references/general/stage-4-discrediting.md` ← `stage4_discrediting` node
- `references/general/common-enemy-bridge.md` ← `common_enemy` node
- `.claude/references/copywriting-os/frameworks/six-proof-types.md` ← `six_proof_types` node
- `.claude/references/copywriting-os/reviewers/proof-density-audit.md` ← `proof_density` node

### From dr_singing extension (adds to dr_solution_aware_l3, does NOT replace)
- _(none — dr_singing_concept exists as a sibling, not a direct parent of dr_singing_solution_aware_l3_concept)_

### From dr_singing_solution_aware_l3_concept combined loadout (top-level)
- `references/direct-response/singing-ads-layer.md` ← `singing_layer` node

**Total files in accumulated required set:** 12 required + 2 conditional = **14 files**

**Extends semantics verified:** `required_nodes` accumulate across the chain — the combined loadout does not replace its parent's nodes, it adds `singing_layer` on top of `dr_solution_aware_l3_concept`'s full set. This matches SKILL.md's stated rule: "recurse the full chain — required_nodes accumulate, they do not replace."

---

## D. forbidden_nodes verified blocked

- **`script-and-music.md`**: blocked because `dr_singing_solution_aware_l3_concept.forbidden_nodes` lists it explicitly. SKILL.md §Compact Runtime Routing confirms: "This is how legacy files like `script-and-music.md` / `suno-manual-target.md` are kept out of singing routes." `singing-ads-layer.md` §"See also" explicitly states: "do NOT load `script-and-music.md` for singing concepts." File exists on disk at `references/general/script-and-music.md` — presence confirmed, load blocked.

- **`suno-manual-target.md`**: blocked because `dr_singing_solution_aware_l3_concept.forbidden_nodes` lists it explicitly. `singing-ads-layer.md` §"See also" states: "do NOT load `suno-manual-target.md` for singing concepts." The singing-ads-layer absorbed the Suno output schema and policy 2026-05-19 (confirmed in file). File exists on disk at `references/general/suno-manual-target.md` — presence confirmed, load blocked.

**Verification:** Both files are in `references/general/`, not `references/direct-response/`. The `forbidden_nodes` spec in REFERENCE_GRAPH.json lists bare filenames. This introduces a **path ambiguity risk**: agents must resolve the basename against the known reference tree to find the actual path. Neither file is referenced by any active loadout node, so the block holds cleanly in practice — but the spec would be more robust with full relative paths (see §G).

---

## E. Solution-Aware × Stage-3 checklist gate

- **Did you find the 4-point mandatory checklist (named jaded prior failure / big_idea reframe / ≥3 Specificity Shock / named common enemy)?** YES.

- **Which file documents it?** Two sources, cross-confirmed:
  1. **Agent spec** `/Users/jerel/.claude/agents/video-concept-seeder.md` lines 82–88 (§6.5) — defines all 4 points verbatim as a pre-write gate. Concepts failing <4/4 are DROPPED and replaced, not flagged.
  2. **`references/general/stage-4-discrediting.md`** — documents the 4 moves operationally (Anger Recruitment / Validation Flattery / Mechanism-as-Foreclose / Pain Stacking) which map directly to the checklist's logic.
  3. **`references/general/common-enemy-bridge.md`** — documents the Schwartz authenticity gate and named-enemy composition, which is the source contract for checklist point 4.

- **Where in your spec was this gate triggered?** Agent spec §6.5 states: "Solution-Aware × Stage-3 checklist gate (mandatory when `awareness_stage == "solution-aware"` AND `sophistication_level >= L3`)." Brief provides `awareness_stage: "solution-aware"` and `sophistication_level: "L3"` — both conditions met. Gate fires before any concept is written to disk.

---

## F. Routing clarity

- **Was the COMBINED loadout obvious from INDEX.md?** YES. INDEX.md contains an explicit row: `"Singing + Solution-aware L3+ concepts" → dr_singing_solution_aware_l3_concept`. No ambiguity — the table handles the combined condition as a first-class entry.

- **Where you guessed:**
  - The `extends` chain depth required checking REFERENCE_GRAPH.json directly. INDEX.md's "What to read" column says "Solution-aware L3+ + `singing-ads-layer.md`" but doesn't list all base nodes — an agent must recurse the graph to accumulate the full set. Guessing stopped once the graph was read.
  - `conditional_nodes` (`lanes`, `duration`) are defined on `dr_standard_concept` but not re-listed on child loadouts. Whether they propagate through the extends chain is not explicitly stated in REFERENCE_GRAPH.json. Inferred YES based on SKILL.md's "required_nodes accumulate" rule and the agent spec's instruction to load `funnel.md` for DR briefs. Could be a source of ambiguity for a cold agent.

- **Were the `extends` semantics clear (accumulate vs replace)?** MOSTLY. SKILL.md §Compact Runtime Routing states "required_nodes accumulate, they do not replace" — this is clear for required_nodes. However, REFERENCE_GRAPH.json does not specify whether `conditional_nodes` from parent loadouts also accumulate. Inferred accumulate; not explicitly confirmed in the graph schema.

---

## G. Missing routing

1. **`forbidden_nodes` paths are basenames only** — `"script-and-music.md"` and `"suno-manual-target.md"` in REFERENCE_GRAPH.json have no path prefix. A cold agent resolving these against the reference tree must search both `references/general/` and `references/direct-response/`. Both files are in `references/general/`, but the spec could point a cold agent to the wrong directory. Recommendation: expand to relative paths matching node schema (e.g., `skills/video-concept-lab/references/general/script-and-music.md`).

2. **`conditional_nodes` inheritance not specified** — REFERENCE_GRAPH.json's loadout schema has no explicit rule about whether `conditional_nodes` from parent loadouts propagate to child loadouts via `extends`. The child loadouts (`dr_solution_aware_l3_concept`, `dr_singing_solution_aware_l3_concept`) do not redeclare `conditional_nodes`. A strict reading says they inherit none; a semantic reading says they inherit all. This needs an explicit `"conditional_nodes_inherit": true` flag or equivalent in the schema.

3. **`singing_layer` node path** — REFERENCE_GRAPH.json declares `"path": "skills/video-concept-lab/references/direct-response/singing-ads-layer.md"`. The actual file lives at `references/direct-response/singing-ads-layer.md` (confirmed). Node path is correct, but `references/general/` also exists — if a cold agent checks `general/` first (where the other condition's files live), it may miss this. The path difference (`direct-response/` vs `general/`) between the singing layer and the L3 condition files is not surfaced in INDEX.md.

4. **No explicit `solution-aware L3+ checklist` pointer in INDEX.md** — INDEX.md says "Solution-aware L3+" in the loadout description but does not link to where the 4-point checklist lives. The checklist is in the agent spec (§6.5), not in any skill reference file. A cold agent reading only SKILL.md + REFERENCE_GRAPH.json + INDEX.md would know the loadout to pick but would not know where the 4-point gate is documented without also reading the agent spec.

---

## H. Redundant loads

1. `growthhub-creative-diversity-2026.md` (via `diversity_audit` node on `dr_standard_concept`) is required in every DR path including this one. At concept-seeder stage, diversity rules are enforced via the 4-axis diversity gate in the agent spec — the `growthhub` file adds audit framing that is pack-level (post-concept) rather than per-concept. For the seeder, the diversity gate runs from agent spec rules, not this file. The file is more load-bearing for `pack_audit` than for the seeder at concept-seed time. Not a blocking issue — but worth flagging.

2. `six-proof-types.md` and `proof-density-audit.md` both load for this brief. For a 20-second singing ad, the proof density audit's full rubric (designed for longer-form content) may be over-specified. The seeder only needs the taxonomy (which proof types are available) and the "≥2 distinct proof types visible" rule. The full density audit is more useful for AG1 review than for seeding. Not blocking — but a trim candidate.

---

## I. Reference-tree trim/compress candidates

### `core-framework.md`
- **Node role:** `dr_source_core` — classified as "audit/source reference, not default runtime."
- **Singing + L3 path loads it?** NO. Not in any loadout's `required_nodes` or `conditional_nodes` for this path. `source_nodes_available_on_conflict` on `dr_standard_concept` makes it available but does not load it by default.
- **Verdict:** CORRECT NOT LOADED. `dr-foundation.md` is the runtime merge; `core-framework.md` is the source. Do not add to singing/L3 path. Load only if evaluator requests primary evidence.

### `lf8-market-translation.md`
- **Node role:** `dr_source_lf8` — "audit/source reference, not default runtime."
- **Singing + L3 path loads it?** NO. Not in any loadout's `required_nodes` for this path.
- **Relevant here?** MARGINALLY. `singing-ads-layer.md` §"How LF8 translates in music" explicitly references `lf8-market-translation.md` for the per-market dialect used in lyrics, and instructs the pack-builder to use it. However, the pack-builder is downstream of the seeder — at seeder stage, knowing LF8 principles exist is sufficient. The seeder does not write lyrics; it writes concept seeds.
- **Verdict:** CORRECT NOT LOADED at seeder stage. Becomes relevant when `video-prompt-pack-builder` runs and writes full lyrics. Consider adding to `singing_layer` node's `see_also` or a conditional node for the pack-builder stage.

### `iman-take-260518.md`
- **Node role:** `dr_source_lf8` area — source transcript referenced by `singing-ads-layer.md` (lines 143-209).
- **Singing + L3 path loads it?** NO. Not in any loadout's required_nodes. `singing-ads-layer.md` references it as a source but does not require it be loaded alongside.
- **Relevant here?** LOW at seeder stage. `singing-ads-layer.md` absorbed the relevant content. Loading the full transcript to re-derive what the layer already synthesizes is wasteful at concept-seed time.
- **Verdict:** CORRECT NOT LOADED. Useful only for conflict-resolution audits where primary source is needed.

### `concept-stage-mandatory-checks.md`
- **Node role:** `dr_source_checks` — "audit/source reference, not default runtime."
- **Singing + L3 path loads it?** NO.
- **Relevant here?** YES — but indirectly. `singing-ads-layer.md` references it 3 times ("See `concept-stage-mandatory-checks.md` Pillar 1 for the open-loop check", "standard concept-vs-content test", "4-gate rubric"). The seeder needs these checks — but `dr-foundation.md` (the runtime file) covers the DR spine checks operationally, and the agent spec §6.5 covers the L3 checklist. The `concept-stage-mandatory-checks.md` file contains the original source version of those checks; it is not additive at seeder stage if `dr-foundation.md` + agent spec cover them.
- **Verdict:** CORRECT NOT LOADED as a default. Would become necessary only if `dr-foundation.md` were found to be incomplete on the 4-gate rubric or open-loop checks. Flag as a conflict-resolution source node, not a runtime node.

### `growthhub-creative-diversity-2026.md`
- **Relevant here?** PARTIALLY — see §H. At concept-seeder stage, diversity enforcement runs from agent spec rules (4-axis check, lane diversity extension). The `growthhub` file adds audit scaffolding that is more relevant to a pack-audit run post-concept. For the seeder, its inclusion inflates context without adding decision-critical content.
- **Verdict:** TRIM CANDIDATE for seeder stage. Keep as `required_node` for `pack_audit` loadout; make it a `conditional_node` on `dr_standard_concept` (trigger: `pack_audit_requested: true` or post-seeder stage). This would trim ~1 file from every DR concept-seeding run.

---

## J. One-sentence routing verdict

**PASS-clean** — the combined loadout `dr_singing_solution_aware_l3_concept` was immediately identifiable from INDEX.md's explicit combined-condition row, the extends chain (`dr_solution_aware_l3_concept` → `dr_standard_concept`) accumulates all required references correctly across 3 loadout levels, `forbidden_nodes` are structurally enforced (both files on disk but blocked), and the Solution-Aware × Stage-3 4-point checklist gate is reachable from the agent spec §6.5 cross-confirmed by `stage-4-discrediting.md` and `common-enemy-bridge.md` — with the single biggest gap being that `forbidden_nodes` entries use bare filenames instead of repo-relative paths, creating a path-resolution ambiguity for cold agents.

---

_Routing test only — no concept seeds generated per orchestrator instruction._
