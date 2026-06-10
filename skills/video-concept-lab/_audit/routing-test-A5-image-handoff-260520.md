# Routing Test A5 — Image Handoff Only (cold)

## A. Selected loadout
- methodology_loadout_id: `image_handoff_only`
- Found via: `REFERENCE_GRAPH.json` → `loadouts.image_handoff_only` (lines 223-239); confirmed in `INDEX.md` → loadout table row "Initial image/style-sheet requirements only"

## B. Navigation log

| Order | File opened | Pointed-to-by | Why | Lines read |
|---|---|---|---|---|
| 1 | `~/.claude/agents/video-concept-seeder.md` | Orchestrator dispatch | Agent spec — required to adopt persona | 1–224 |
| 2 | `skills/video-concept-lab/SKILL.md` | Agent spec §"Your methodology lives at" | Entry point and boundary; also confirms §7 product reference gate + image-handoff pointer | 1–279 |
| 3 | `skills/video-concept-lab/REFERENCE_GRAPH.json` | SKILL.md §"Compact Runtime Routing" + agent spec | Machine-readable loadout contract; found `image_handoff_only` loadout here | 1–255 |
| 4 | `skills/video-concept-lab/INDEX.md` | SKILL.md §"Compact Runtime Routing" | Human-readable routing table; confirmed `image_handoff_only` row | 1–42 |
| 5 | `skills/video-concept-lab/references/general/image-handoff.md` | `REFERENCE_GRAPH.json` → `image_handoff_only.required_nodes[0]` = `image_handoff` → node path | Single required file for this loadout; contains full product reference gate + handoff schema | 1–101 |

Files NOT opened: `dr-foundation.md`, `concept-generation.md`, `hook-and-format-rules.md`, `scoring-and-analysis.md`, `success-criteria.md`, `output-schema.md`, `diversity_audit`, `stage4_discrediting`, `common_enemy`, `six_proof_types`, `proof_density`, `singing_layer`, `brand-awareness-methodology.md`. DR foundation and concept methodology stack skipped entirely.

## C. image_handoff_only loadout — verified loaded

- **Required nodes loaded:** `image_handoff` → `references/general/image-handoff.md` ✓
- **Conditional nodes declared (not triggered):** `taxonomy`, `success_criteria` — the concept (c03) is already approved at AG1; neither was needed for a routing-trace-only task.
- **Did your spec let you skip DR foundation?** YES. REFERENCE_GRAPH.json `image_handoff_only` has zero DR nodes in `required_nodes`. The agent spec's "Read only the selected loadout plus explicitly triggered conditionals" rule cleanly prevents DR load. No SKILL.md prose forces DR on this path.

## D. Product reference gate check

- **Did you find `scripts/check_product_reference_gate.py`?** YES. Confirmed present at `skills/video-concept-lab/scripts/check_product_reference_gate.py` (directory listing verified). SKILL.md §Tooling documents it explicitly at line 272-273.
- **Did you find the inline equivalent in `references/general/image-handoff.md`?** YES. `image-handoff.md` §"Product Reference Gate" (lines 7-31) contains the full pass condition, bash invocation, and fallback checklist. The inline gate is complete and usable without running the script.
- **Is the gate easy to invoke from this narrow entry point?** YES, with one caveat. The script call and inline checklist are both in `image-handoff.md` — the single file the loadout requires. No additional file reads are needed to know the gate exists and how to run it.

### Takekine / Ferrovia gate pre-check (observation only)

`clients/takekine/_brand/brand-assets/ferrovia/` exists and contains: `product-packshots/`, `packaging/`, `strip-references/`, `product-reference-manifest.json`. Pass condition (≥1 packshot + ≥1 strip reference) appears met without running the script. Gate would likely PASS for Ferrovia.

## E. Routing clarity

- **Was the narrow entry point first-class?** YES. `image_handoff_only` is an explicit named loadout in REFERENCE_GRAPH.json with a clear `when` field ("define initial image/style-sheet requirements after concept direction is chosen"). INDEX.md lists it in the loadout table. No guessing required.
- **Did you have to skim full SKILL.md?** YES — partial. The agent spec directs "Read `SKILL.md` for boundary/routing, then read `REFERENCE_GRAPH.json`." SKILL.md must be read first as the entrypoint; REFERENCE_GRAPH.json is the fast exit to the correct loadout (5 short sections in). Practically, SKILL.md is ~279 lines and you scan it top-down until you hit "Compact Runtime Routing" (~line 88), which immediately says "read REFERENCE_GRAPH.json + INDEX.md and stop." A cold agent without this test's foreknowledge would read 88 lines of SKILL.md before exiting to the graph.
- **Where you guessed:** None. All navigation was deterministic from file pointers.

## F. Missing routing

1. **Agent spec does not mention `image_handoff_only`** by name. The spec lists the graph-selection instruction generically ("selected `methodology_loadout_id` from the orchestrator"), but does not enumerate available loadouts or confirm narrow-scope modes. A cold agent dispatched with task_type `image-style-sheet-requirements-only` must derive the loadout ID from INDEX.md/REFERENCE_GRAPH.json rather than the spec.
2. **No `image_handoff_only` routing example in agent spec** — the spec's methodology section reads entirely as a concept-generation flow. Narrow-scope entry is reachable but implicit.
3. **SKILL.md §7 (Image/Style-Sheet Requirements)** and §6 (AG1) list image-handoff as part of the full DR pipeline. A reader could mistake it for exclusively a post-DR-concept step rather than a standalone entrypoint. The loadout in REFERENCE_GRAPH.json contradicts this framing, but the prose doesn't flag the split.

## G. Redundant loads (DR files you opened that you didn't need)

None. The `image_handoff_only` loadout required only `image_handoff`. No DR files were opened. The REFERENCE_GRAPH.json machine contract worked as designed.

The only "extra" reads were:
- Full agent spec (required to adopt persona per orchestrator instructions)
- Full SKILL.md entry section (required by agent spec; contains routing exit in first 90 lines)
- Full REFERENCE_GRAPH.json (required to select loadout; 255 lines but compact JSON)
- Full INDEX.md (42 lines; fast confirm)

These are all necessary routing reads, not redundant DR loads.

## H. Reference-tree trim/compress candidates

- **`image-handoff.md`** — Reachable: YES. Right size: YES (101 lines, self-contained). Location in `general/`: appropriate — it's flow-agnostic and downstream consumers (`video-brief-normalizer`, `video-prompt-pack-builder`) are not DR-specific. No case for moving it to its own folder at current size.
- **Should `image_handoff_only` be a top-level "narrow-scope mode" in the agent spec?** YES. Recommendation: add a §"Narrow-scope modes" table in the agent spec that lists `image_handoff_only` (and `pack_audit`) as valid `methodology_loadout_id` values an orchestrator may forward for post-AG1 or audit-only dispatches. This makes narrow entries first-class without reading INDEX.md to discover them. One 3-row table, ~8 lines added to spec.
- **SKILL.md §7 prose framing** should note "(or as standalone `image_handoff_only` loadout when concept is already approved)" to prevent future readers from treating image-handoff as exclusively a post-DR-pipeline step.

## I. One-sentence routing verdict

PASS-clean: `image_handoff_only` was reachable in 5 ordered reads, DR foundation was skipped entirely, the product reference gate was confirmed in the single required file, and no guessing was required — the only structural gap is that the agent spec does not enumerate narrow-scope loadouts by name.
