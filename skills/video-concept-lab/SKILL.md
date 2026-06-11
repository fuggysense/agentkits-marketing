---
name: video-concept-lab
version: "0.2.0"
brand: AgentKits Marketing by AityTech
category: content
difficulty: advanced
description: "Paid AI-video concept methodology for the main video-concept-seeder agent: 5 concepts + winner scoring before render. Hooks, narrative format, proof mode, strategic angle. Approval Gate 1. In the v0.5 pipeline this is a rubric/reference, not a second runtime concept generator."
triggers:
  - video concept lab
  - video ad concepts
  - paid video concepts
  - singing ad concept
  - no-dialogue ad
  - UGC video concept
  - founder-led video concept
  - demo video ad concept
  - avatar acting script
  - visual hook
  - video script concept
related_skills:
  - source-of-truth
  - avatar-research
  - ad-concept-engine
  - script-skill
  - video-brief-normalizer
  - gpt-image-2-director
  - video-factory
output_schema: video-concept-pack
---

# Video Concept Lab

Marketing-side methodology for paid AI-video concepts. In the v0.5+ orchestrated pipeline, `~/.claude/agents/video-concept-seeder.md` is the **single runtime concept generator** and this skill is its rubric/reference pack. **Never run this skill as a second independent generator in the same workspace.** It decides strategic concept, micro-persona, on-screen persona, hook, visual world, storyboard direction, format, and winner — then stops at Approval Gate 1. After AG1, `video-brief-normalizer` and `video-prompt-pack-builder` take over.

## Boundary

**Owns:** concept methodology used by `video-concept-seeder`; five concepts + recommended winner; hook audit/creation (verbal, quiet visual, rendered text, subtitle policy); taxonomy selection; concept scoring; AG1 review-visual requirements (production design guide + pencil sequence sheet); target video frame; image/style-sheet requirements; AG1 itself.

**Does not own:** Meta primary text / headlines (→ `ad-concept-engine` / `headline-bank`); DCT tracker; client-facing Google Docs brief and internal AI production brief (→ `video-brief-normalizer`); AG2; beat sheets; GPT Image 2 rendering; Higgsfield / Seedance / Kling / Suno calls; `video-factory-handoff.json` (→ `video-prompt-pack-builder`).

## Invocation Rule

Inside `vid-director`, do not invoke this skill as a separate generator. Dispatch `video-concept-seeder`; it reads this skill and writes the artifacts.

If invoked from `ad-concept-engine`, confirm video intent first:
> "Are we turning this wave/batch into video ads, or should this stay as static/carousel creative?"

If static/carousel → return control to `ad-concept-engine` Phase 2a.

## Orchestrator Dispatch Contract

This is the contract `vid-director` MUST honor when dispatching `video-concept-seeder`. It is the single point where loadout selection, workspace paths, and receipt validation meet.

**Orchestrator → seeder task envelope:**

```json
{
  "brief_path": "<workspace>/concept-brief.json",
  "workspace_path": "<workspace>/",
  "methodology_loadout_id": "<one of 7 — see INDEX.md table>",
  "expected_methodology_loadout_id": "<same id; passed to evaluators>",
  "creative_diversity_map_path": "<workspace>/01_strategy/creative-diversity-map.json"
}
```

**Seeder → orchestrator outputs:**

- `<workspace>/02_ag1-options/concepts-draft.json` — N seeded concepts
- `<workspace>/02_ag1-options/inputs-used.json` — contains the `methodology_receipt`

**`methodology_receipt` schema (required fields):**

```json
{
  "methodology_loadout_id": "dr_singing_concept",
  "graph_path": "skills/video-concept-lab/REFERENCE_GRAPH.json",
  "loaded_files": ["..."],
  "skipped_files": ["..."],
  "missing_files": [],
  "routing_reason": "DR brief + script_mode=singing → dr_singing_concept extends dr_standard_concept"
}
```

**Evaluator verification gate:** `eval-video-universal` and `eval-video-flow-compliance` MUST verify `receipt.methodology_loadout_id == expected_methodology_loadout_id` and emit `routing_verdict.methodology_receipt_check: pass|fail` before AG1 renders. Mismatch → reject and force re-dispatch.

## Compact Runtime Routing

Before loading methodology references, read **two files only**:

1. `REFERENCE_GRAPH.json` — machine-readable loadout contract (single source of truth for which files to load).
2. `INDEX.md` — human-readable loadout table + path rules.

Pick exactly one `methodology_loadout_id` (table in `INDEX.md`). Load only the selected loadout's `required_nodes` plus explicitly-triggered `conditional_nodes`. **Do not bulk-load `references/`.** When a loadout `extends` another, recurse the full chain — `required_nodes` accumulate, they do not replace.

`forbidden_nodes` in a loadout are hard-blocks: agents must not load those files even if other prose mentions them. This is how legacy files like `script-and-music.md` / `suno-manual-target.md` are kept out of singing routes.

## Context Load

Load the smallest sufficient client context. Defer to `Marketing/CLAUDE.md` §AGENT ENTRY CONTRACT for the full read order. Critical priorities at concept time:

1. `clients/<project>/context-profile.json`
2. Latest `clients/<project>/01_research/output/*audience-insights-synthesis.md` — priority buyer-language source.
3. `clients/<project>/_brand/{offer,buyer-profile,icp,brand-voice}.md`
4. **If present:** `clients/<project>/_brand/funnel.md` — required for DR briefs with lanes before §2.5.
5. Workspace-root `concept-brief.json` (canonical). Older `concept-input-packet*.json` is a legacy alias only.
6. `clients/<project>/_swipe/winning-ads/` for proven hooks and reuse notes.

`concept-brief.json` must specify big idea, selected micro-persona, optional on-screen persona, awareness, sophistication, offer mechanism, proof hooks, objection map, claim constraints. If critical context is missing, ask only for what blocks the concept decision.

See `references/general/context-pack.md` and `references/general/concept-input-packet.md`.

## Brief Type Gate (mandatory pre-load)

Classify before any methodology loads:

- **Direct-response** (conversion, lead-gen, performance CTA) → `dr_standard_concept` unless a sub-type below upgrades it.
- **Brand awareness** (premium positioning, no CTA, brand-lift) → `brand_awareness_concept`. **SKIP the DR stack entirely.** Apply that loadout's framework (not pain → gap → mechanism → belief shift). Jump from here to §Process.
- **Ambiguous** → ask: *"Conversion (load DR) or brand lift (load brand-awareness)?"* Do NOT default to DR.

## Brief Sub-Type Gate — Awareness × Sophistication (DR only)

| awareness_stage | sophistication | Loadout |
|---|---|---|
| `unaware` / `problem-aware` | any | `dr_standard_concept` |
| `solution-aware` | L1-L2 | `dr_standard_concept`; add `six_proof_types` if proof density material |
| `solution-aware` | L3+ | `dr_solution_aware_l3_concept`. If singing: `dr_singing_solution_aware_l3_concept` |
| `product-aware` | any | offer-led → route to `ad-concept-engine` + `headline-bank` |
| `most-aware` | any | out of scope for video-concept-lab v0.5 |

**Halt-and-ask:** if `awareness_stage` is missing/empty in `concept-brief.json`, halt and request operator input. Do NOT default to `problem-aware` — misclassification produces concepts that hand off to the wrong SL opening rung.

Solution-Aware × L3+ stack requires `concept-brief.json` to carry the extended `big_idea` + `credibility_stack` per `references/general/concept-input-packet.md`. Seeder refuses to emit concepts otherwise.

## Hook-Swap Variant Lane (clients with a proven control)

A cheap test lane — not a replacement for full concept seeding. When a client already has a **winning control video**, the highest-leverage, lowest-cost move is to keep the proven body and race new hooks against it, rather than seeding five fresh concepts from scratch. This is Ferres' Control Challenge spine: three new ads = (1) the control's own hook re-shot + (2) two brand-new hooks, all stitched onto the existing winning body, run head-to-head for 7 days (`_shared-knowledge/ferres/04-end-to-end-sop.md` stages 3-5).

**When to choose this lane (all must hold):**
- The client has a video ad with real performance data marking it the control.
- The body of that ad still converts — the suspected ceiling is the hook, not the offer or the proof.
- The goal is a fast, single-variable test (hook only), not a new angle or audience.

If any fails, fall back to full five-concept seeding (§Process). State the lane choice in one line before proceeding, per the Schwartz/sophistication pre-dispatch call.

**Inputs:**
- Control transcript (the winning ad's full script — hook + body, clearly marked where the hook ends).
- The three research docs (ICP / competitor / market) per §Context Load — the new hooks must be traceable to a research insight, not invented.
- `_brand/{offer,buyer-profile}.md` for avatar fit.
- Performance note on WHY the control wins (retention past 3s = hook strength; click-rate among watchers = body strength). This confirms the body is the keeper.

**Hook engine — do not reinvent it.** This lane does not write hooks itself. Dispatch `video-hook-variants` (the skill that owns hook engineering for multi-clip paid video). It produces paired verbal + visual + rendered-text + subtitle-policy hook variants per concept. This lane's job is to set the brief, gate the output, and shape it for the existing AG pipeline.

- Default count: 2-3 new hooks (the control's own re-shot hook is a fourth contender the operator keeps "for free").
- Every variant inherits the control's body verbatim — the variant differs ONLY in the first 0-3 seconds.
- Tag each variant with the research insight it leverages (the same traceability §Process and Ferres stage 4 require).

**Gate (lighter than full AG1 — it is a hook test, not a new concept):**
- **Hook clarity:** clear beats clever; a confused viewer never buys. Reject hooks that need the body to make sense.
- **Avatar fit:** does the hook pull the RIGHT person? Ferres rejected "work 1 hour a day" because it attracts lazy buyers; he reworked it. Run the same filter.
- **Flow:** does the new hook stitch cleanly onto the proven body — same persona, same tone, no seam the viewer notices?
- **Insight tag present:** each surviving hook names its research insight. No tag = not ready.

Operator picks the top 2-3. Record the choice in `approval-1.json` with `lane: "hook_swap"` so downstream knows the body is fixed and only the hook clips are new.

**Outputs (hook clips spec for the existing AG pipeline):**
- A hook-clips spec per surviving variant: `verbal_hook`, `quiet_visual_hook`, `rendered_text_hook`, `subtitle_policy` (the §2 Hook Lab four-field shape), plus the insight tag and the exact frame where it hands off to the control body.
- A `control_body_ref` block naming the control transcript and the handoff point, so `video-prompt-pack-builder` renders only the new hook clips and the editor stitches them onto the untouched body.
- `approval-1.json` with `lane: "hook_swap"`, the chosen hooks, and the fixed-body note.

The hook clips then flow through the normal AG pipeline (AG1 here → `video-brief-normalizer` → `video-prompt-pack-builder` → AG2 → render). The difference from the full lane: only the hook is generated and rendered; the body is reused, so AG2 and the prompt pack scope to the hook clips alone.

## DR First Principles

`references/direct-response/dr-foundation.md` is the runtime DR methodology — loaded automatically via `dr_standard_concept` and its extensions. It combines spine, short-form adaptation, and operational checklist.

The older split files (`core-framework.md`, `lf8-market-translation.md`, `concept-stage-mandatory-checks.md`, `iman-take-260518.md`) are **audit/source references** — load only when `REFERENCE_GRAPH.json` flags them as conflict/source nodes or an evaluator requests primary evidence.

**Minimum-viable seeder directive (embed in dispatch):**

> "Know the level of awareness, hit one sharp pain, widen the gap, sell the mechanism, and only then choose the format that expresses it best."

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

**Format is module 5 of 6, chosen LAST.** If `concept-brief.json` declared a `workflow_flow`, treat it as a hypothesis. The seeder may override and flag at AG0 if the format rubric points elsewhere.

`references/general/concept-taxonomy.json` defines the required taxonomy fields per concept (`recommended_ad_format`, `presentation_context`, `style_profile`, `angle_family`, `creative_mechanism`, `proof_mode`, `script_mode`, `format_recipe`, `psychological_engine`). Never save recipe labels ("UGC talking head", "podcast setup", "2D animation") as `recommended_ad_format` — split into separate knobs plus `format_recipe`.

## Process

### 1. Direction Interview

Ask concise questions only when not inferable from context: client/offer, platform (Meta default), existing-hook-or-blank-slate, narrative job, delivery wrapper, style profile, target video frame/aspect ratio, duration, script mode preference, new-avatar permission, forbidden claims/compliance.

### 2. Hook Lab

If user gives a hook, audit it; otherwise generate candidates from client context. Every approved concept separates four hook fields:

- `verbal_hook` — words spoken in the first 0-3 seconds, if any.
- `quiet_visual_hook` — what stops the scroll without words.
- `rendered_text_hook` — text intentionally on-frame, if any.
- `subtitle_policy` — whether subtitles/captions are used.

**No-dialogue ads:** no subtitles in final ad. Rendered text only when intentional, declared, treated as visual creative (e.g. Snapchat-style text strip). Always declare whether rendered text is used.

See `references/general/hook-and-format-rules.md`.

### 2.5. Lane Selection (DR only)

Lanes are the psychological doorway constraining hook archetype + awareness rung before format is chosen. Apply only when `_brand/funnel.md` defines them.

1. Read `_brand/funnel.md` §"Strategic Ad Lanes" and §"Persona → Lane → Handoff Mapping."
2. Identify target persona from `concept-brief.json` `target_micro_persona.micro_persona_id`.
3. Use the mapping table to find valid lanes for that persona's awareness rung.
4. Assign one lane per concept slot. Default: spread across ≥ 3 distinct lanes across the 5-concept pack.
5. Operator may override to single-lane testing — record `lane_test_mode: true`.
6. Record commitment in each concept's `chosen_lane` block.

If no lanes defined: skip and flag the gap. Hook archetype in the lane MUST match the concept's `visual_hook.verbal_hook` premise.

See `references/general/creative-lanes-methodology.md` for full schema, lane anatomy, and `angle_family` compatibility rules.

### 3. Generate Five Concepts

In the pipeline, `video-concept-seeder` performs this and writes `02_ag1-options/concepts-draft.json`. This section defines method and quality bar.

Five distinct concepts by default. If operator requests another count, follow it and record `concept_count`. Every concept inherits the active `big_idea_id`; if none selected, ask whether to create a hypothesis or use an existing proven/testing angle.

Each concept must have a unique combination of: micro-persona + optional on-screen persona, environment, action sequence, hook delivery, psychological engine, `recommended_ad_format`, `presentation_context`, `style_profile`, `angle_family`, `creative_mechanism`, `proof_mode`, `script_mode`.

At least two concepts should use occupation/lifestyle match for the target audience when client context supports it.

See `references/general/concept-generation.md`.

### 4. Score And Pick Winner

Score every concept on the V2V matrix: scroll-stop velocity, emotional impact, narrative clarity, shareability, conversion potential, Video Studio feasibility. Recommend one winner; preserve all five for review.

See `references/general/scoring-and-analysis.md` and `references/general/success-criteria.md`.

### 5. Script / Format Direction

Directional pass only — never final scripts, lyrics, music, image prompts, or render prompts at this stage. The next workflow stage refines.

- `voiceover` → VO direction, not final copy.
- `direct_to_camera` → performer direction + line-shape notes.
- `dialogue` → character roles + dialogue intent.
- `singing` → musical premise + music direction (loaded via `singing-ads-layer.md` only through the singing loadouts).
- `no_dialogue` → visual-beat direction, rendered-text policy, sound-design intent, rough timing.

See `references/general/script-and-music.md` and `references/general/suno-manual-target.md` (loaded only when their loadout requires them).

### 5.5. Client Concept Visuals

Two artifacts per concept for AG1 review:

1. `production-design-guide` — art-direction board: on-screen persona/character treatment, product/props, set, palette, lighting, art notes.
2. `pencil-sequence-sheet` — storyboard table: shot #, size, angle, subject, description, VO/audio, pencil thumbnail direction.

Record `target_video_frame` in the concept pack and approval gate before creating these. Ask once if not inferable from platform. Pencil sequence sheet matches the final video frame (default `9:16 vertical` for Meta/TikTok/Reels). Production design guide may stay landscape for clearer art review.

Shot count is flexible — no six-shot cap. Store under `client-concept-visuals/concept-XX/`. These are first-pass AG1 visuals only — no Higgsfield commands or model-specific render prompts.

### 6. Approval Gate 1

Save `approval-1.json` with `status: pending`. Nothing proceeds to brief-pack creation until operator approves or requests revisions.

AG1 covers: selected concept, draft hook + script direction, recommended format + duration, target video frame, presentation/style/proof/script modes, initial visual concept, production design guide + pencil sequence sheet for the selected concept, initial image/style-sheet requirements.

### 7. Initial Image/Style-Sheet Requirements

Define likely image inputs before script/visual refinement: character style sheet, product style sheet, environment/scene plate, props/UI/mechanism sheet, style reference.

**Product reference gate:** before any product-inclusive image is generated, run `scripts/check_product_reference_gate.py` (or its inline equivalent in `references/general/image-handoff.md`). If client workspace lacks approved product references, halt and ask which external references to promote into `_brand/brand-assets/`.

`video-brief-normalizer` later turns the refined script + visual treatment into the approved asset contract.

See `references/general/image-handoff.md`.

### 8. Output Workspace

When dispatched by `video-concept-seeder`, the seeder writes only `02_ag1-options/concepts-draft.json` + `inputs-used.json`. The orchestrator's Phase 4 synthesis owns `concept-pack.{md,json,html}` + `approval-1.json`.

Standalone/manual use saves to `clients/<project>/campaigns/<campaign>/video-concepts/<slug>/` (see `clients/_template/CONTEXT.md` for the canonical folder map). If no campaign folder exists, output inline and ask whether to save.

`approval-1.json` is the concept HITL gate. Never create `video-factory-handoff.json` from this skill — that belongs to `video-prompt-pack-builder` after AG2.

## Output Contract

A final concept pack (standalone or Phase 4 synthesis) must include:

- Context summary.
- `methodology_receipt` — `methodology_loadout_id`, graph path, loaded files, skipped files, missing files, routing reason.
- Five concept briefs with all taxonomy fields (see §DR First Principles taxonomy enum list).
- `chosen_lane` block per concept when client has lanes; `null` otherwise.
- Solution-Aware × L3+ fields when that gate fires: `big_idea.reframe_mechanism`, `big_idea.named_enemy` (per `common-enemy-bridge.md`), ≥2 distinct proof types from `credibility_stack` in the visible ad.
- Two client concept visuals per concept (production design guide + pencil sequence sheet).
- V2V scoring table + recommended winner.
- Hook breakdown + script/refinement direction for the selected concept.
- Character/avatar approvals needed + initial image/style-sheet requirements.
- `approval-1.json` for concept approval.
- Downstream recommendation: script/visual refinement → `video-brief-normalizer`, or return to `ad-concept-engine`.

**HTML rendering:** any approval-gate / review HTML (concept-pack, AG1, AG2, input-image-review, render-prompt-review, internal/client reports) defaults to `skills/common/templates/hazecraft-agency-wrapper.md` as the agency shell. Client/product assets, final creative direction, and render prompts still preserve the client's approved brand.

See `references/general/output-schema.md`.

## Tooling

Two scripts live under `scripts/`. Both are read-only validators — safe to run anytime.

- **`scripts/validate_reference_graph.py`** — validates `REFERENCE_GRAPH.json` integrity end-to-end. Run before any commit that touches this skill or the orchestrator/agent contracts. Checks: every node's `path` resolves to a real file; no legacy `02_concepts` paths in active contracts; the combined `dr_singing_solution_aware_l3_concept` loadout extends `dr_solution_aware_l3_concept` and requires `singing_layer`; `video-concept-seeder` references `REFERENCE_GRAPH.json` and `methodology_receipt`; evaluators reference `concept-brief.json` + `expected_methodology_loadout_id` and emit `routing_verdict.methodology_receipt_check`; no weak `methodology_receipt_seen` flag in evaluators. Exit code 0 = PASS; non-zero with bullet list of failures = FAIL.

- **`scripts/check_product_reference_gate.py`** — enforces the product reference gate at §Process step 7. Called before any product-inclusive image is generated. See `references/general/image-handoff.md` for the equivalent inline checklist when the script isn't reachable.

```bash
python3 scripts/validate_reference_graph.py
# expect: REFERENCE_GRAPH_VALIDATION=PASS  nodes=N loadouts=N
```

## Integration Notes

- In `vid-director`, the only runtime concept generator is `video-concept-seeder`.
- This skill is the methodology/rubric read by the seeder — never dispatched beside it.
- `ad-concept-engine` calls this only after confirming video intent; still owns Meta copy, headlines, DCT packaging, tracker rows.
- Script/visual refinement follows AG1.
- `video-brief-normalizer` owns the client-facing brief, internal AI production brief, AG2, and Video Factory handoff prep.
- `video-prompt-pack-builder` owns scripts (`03_scripts/`), input-image manifests (`04_input-images/`), prompt packs (`05_prompt-packs/`), adapters, and the AG2 approval write.
- `video-factory` owns input-image prompts, beat sheets, model routing, render prompts — only after AG2.

<!-- skill-graph:start -->

## Related
<!-- auto-generated by scripts/link-skills.py — do not edit by hand -->

- [[video-brief-normalizer]] (skill, 0.21)
- [[vid-director]] (skill, 0.19)

<!-- skill-graph:end -->
