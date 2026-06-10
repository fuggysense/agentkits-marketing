# Routing Test A4 — Pack Audit Edge Case (cold)

## A. Selected loadout

- **methodology_loadout_id:** `pack_audit`
- **Found via:** `REFERENCE_GRAPH.json` → `loadouts.pack_audit` (lines ~207–216), confirmed by human-readable alias in `INDEX.md` → Loadout Selection table row: "Existing pack quality/diversity audit → `pack_audit`"
- **How long to realize this was audit-not-generation:** Immediately, from the orchestrator envelope's `task_type: "pack-level-audit"` and `"NO new concepts"` instruction. The REFERENCE_GRAPH `when` clause matched verbatim: *"audit an existing concept pack for diversity or quality without generating new concepts."* Zero ambiguity from the envelope. However — the agent spec itself has NO dispatch gate that reads `task_type`. Recognition depended entirely on the orchestrator being explicit. If the envelope had omitted `task_type`, the spec's default "How you operate" section starts at Step 1 (read methodology and all inputs) and flows directly into concept generation with no branch check.

---

## B. Navigation log

| Order | File opened | Pointed-to-by | Why | Lines read |
|---|---|---|---|---|
| 1 | `/Users/jerel/.claude/agents/video-concept-seeder.md` | Orchestrator dispatch | Adopt persona; find methodology pointers | 224 (full) |
| 2 | `skills/video-concept-lab/SKILL.md` | Agent spec §Your methodology lives at | Boundary/routing; Brief Type Gate; Compact Runtime Routing section | ~200 |
| 3 | `skills/video-concept-lab/REFERENCE_GRAPH.json` | Agent spec §Your methodology lives at + SKILL.md §Compact Runtime Routing | Machine-readable loadout contract; source of truth for which files to load | Full |
| 4 | `skills/video-concept-lab/INDEX.md` | SKILL.md §Compact Runtime Routing ("read two files only: REFERENCE_GRAPH.json and INDEX.md") | Human-readable loadout table; confirmed `pack_audit` label and required_nodes | Full |

Files 3 and 4 were sufficient to confirm `pack_audit`. No further reads were needed because `pack_audit` requires only 4 nodes (`diversity_audit`, `scoring`, `success_criteria`, `output_schema`) and none require conditional expansion.

---

## C. pack_audit loadout — verified loaded

**Required nodes (from REFERENCE_GRAPH):**

| Node ID | Resolved path |
|---|---|
| `diversity_audit` | `skills/video-concept-lab/references/direct-response/growthhub-creative-diversity-2026.md` |
| `scoring` | `skills/video-concept-lab/references/general/scoring-and-analysis.md` |
| `success_criteria` | `skills/video-concept-lab/references/general/success-criteria.md` |
| `output_schema` | `skills/video-concept-lab/references/general/output-schema.md` |

**Writes:** `"audit report only unless explicitly asked"` — no `concepts-draft.json`, no `inputs-used.json` (the telemetry file is a generation artifact; `pack_audit` does not own it).

**Downstream consumers:** `routing-tester`, `eval-video-universal`

**Was the loadout obviously findable from your agent spec?** PARTIAL. The agent spec says "Read `SKILL.md` for boundary/routing, then read `REFERENCE_GRAPH.json` and the selected `methodology_loadout_id` from the orchestrator." This implies the orchestrator always provides the `methodology_loadout_id` — the agent doesn't self-select it. The spec never mentions `pack_audit` by name, nor does it define what to do when no generation is wanted. The REFERENCE_GRAPH and INDEX.md are where `pack_audit` becomes a named, first-class option. Finding it required two hops: agent spec → SKILL.md → REFERENCE_GRAPH/INDEX.md.

---

## D. Implicit-routing failure mode check

**Did anything almost funnel into generation by default?**

YES. Two strong gravity wells toward generation:

1. **Agent spec title/description:** *"Generates N concept seeds for paid-video ads"* — the entire framing is generative. There is no mention of audit/evaluation in the description, the `## What you never do` section, or the `## Iterative mode` section.

2. **SKILL.md §Brief Type Gate (mandatory pre-load):** This gate classifies briefs into Direct-response, Brand awareness, or Ambiguous — and routes to DR or brand-awareness loadouts. There is no branch for "audit task." A cold agent reading the Brief Type Gate in sequence would be pushed toward `dr_standard_concept` (DR brief default) or asked "Conversion or brand lift?" — not "Is this a generation task at all?"

**Ambiguous lines:**

> *"Read `SKILL.md` for boundary/routing, then read `REFERENCE_GRAPH.json` and the selected `methodology_loadout_id` from the orchestrator."* — Agent spec, opening methodology section.

This line implies the orchestrator always selects the loadout, which would rescue an audit dispatch — but only if the orchestrator sends `methodology_loadout_id: "pack_audit"`. If the envelope sends `task_type: "pack-level-audit"` with no `methodology_loadout_id`, the spec gives no mapping from `task_type` to loadout. The agent would have to infer via REFERENCE_GRAPH.json `when` fields — which is possible but requires correct reasoning under ambiguity.

> *"Step 1. Read graph-selected methodology and all exact inputs."* — Agent spec §How you operate.

"All exact inputs" in the generation context includes `concept-brief.json`, `creative-diversity-map.json`, campaign paths, brand files — a heavyweight load. For a pack-audit task, most of these are irrelevant. The spec does not trim the input load for audit tasks.

---

## E. Routing clarity

**Was the pack-audit entry point first-class or buried?**

BURIED in REFERENCE_GRAPH/INDEX.md; invisible in the agent spec.

- In `REFERENCE_GRAPH.json`: `pack_audit` is one of 7 loadout keys. It has a clear `when` clause. The `diversity_audit` node is well-defined and points to `growthhub-creative-diversity-2026.md`. This is structurally clean.
- In `INDEX.md`: `pack_audit` appears in the Loadout Selection table with a one-line description. Clear once you reach this file.
- In `SKILL.md`: The word "audit" appears in context of *hook audit* (Step 2), *proof-density-audit* (a file name), and *source references* (legacy DR files). No section is titled "Audit mode" or "Evaluation mode." No prose says "if the task is an audit, use `pack_audit`."
- In the **agent spec**: Zero mentions of `pack_audit`, audit mode, evaluation mode, or non-generative dispatch paths. The spec's entire structure assumes generation will occur.

**Where I guessed:**
- That the orchestrator's `task_type: "pack-level-audit"` maps to `pack_audit` (confirmed via REFERENCE_GRAPH `when` field — not a guess, but required inference since no explicit mapping exists in the spec).
- That `inputs-used.json` telemetry is NOT required for `pack_audit` (the spec mandates it unconditionally in step 8, but `pack_audit.writes` says "audit report only" — conflict unresolved in spec).

---

## F. Missing routing

**Does the spec mention an "EVALUATION mode" upfront?** NO. The word "evaluation" does not appear in the agent spec in the context of dispatch modes. "Evaluator" appears only to refer to downstream `eval-video-universal` and `eval-video-flow-compliance` agents that consume the seeder's output.

**If you were a brand-new agent — would you know audit is supported?** NO. A cold agent reading only the spec's title, description, and `## How you operate` section would conclude its only job is concept generation. Audit is discoverable only after:
1. Reading SKILL.md's §Compact Runtime Routing
2. Opening REFERENCE_GRAPH.json
3. Scanning all loadout `when` fields

This is a 3-hop discovery path for a capability the orchestrator may legitimately dispatch to this agent.

---

## G. Redundant loads

For `pack_audit`:
- `concept-brief.json`, `creative-diversity-map.json`, `campaign-selection.json`, all `_brand/*.md` files — generation-only inputs; irrelevant for audit. The agent spec's step-1 instruction to load "all exact inputs" would wastefully load these unless the orchestrator withholds them from the dispatch envelope.
- `dr_runtime` (`dr-foundation.md`) — NOT in `pack_audit.required_nodes`. Do not load.
- `taxonomy` (`concept-taxonomy.json`) — NOT in `pack_audit.required_nodes`. Do not load.
- `lanes`, `duration` — NOT in `pack_audit`. Do not load.

The `pack_audit` loadout is tight (4 nodes). The risk is the agent loading generation-stack files anyway because the spec's step-1 instruction reads "read … all exact inputs" without an audit-mode carve-out.

---

## H. Reference-tree trim/compress candidates

**`growthhub-creative-diversity-2026.md` — used here? Reachable? Verdict.**
- **Used here:** YES — it is the `diversity_audit` node, the only primary content node in `pack_audit`.
- **Reachable:** YES — file confirmed at `skills/video-concept-lab/references/direct-response/growthhub-creative-diversity-2026.md`.
- **Verdict:** ESSENTIAL. It is the entire methodology payload for pack-audit. Not a candidate for removal. It IS a candidate to surface more prominently: its node role is `"pack-level diversity audit"` but it lives under `references/direct-response/` — a path that suggests DR generation context, not auditing. Relocating to `references/general/` or `references/audit/` would reduce confusion.

**Should `pack_audit` have its own top-level entry in SKILL.md / agent spec?**
YES — this is the single highest-leverage fix. Recommended additions:

1. **Agent spec:** Add a `## Dispatch modes` section above `## Inputs the orchestrator hands you` listing generation vs. audit modes with their `methodology_loadout_id` and what the spec contract changes (no concept output, no `inputs-used.json` mandatory write, no 4-axis compass scoring).

2. **SKILL.md:** Add an `## Audit / Evaluation mode` subsection to §Compact Runtime Routing with one line: *"For pack-level diversity audits with no generation, use `pack_audit` loadout — output is a scorecard only, not `concepts-draft.json`."*

3. **REFERENCE_GRAPH.json:** The `pack_audit` node should include `"forbidden_nodes": ["dr_runtime", "taxonomy", "concept_generation", "hook_rules", "lanes", "duration"]` (mirroring the pattern used in `dr_singing_concept`). Currently no forbidden_nodes are declared, leaving the agent free to load generation files.

---

## I. One-sentence routing verdict

**PARTIAL-ambiguous:** `pack_audit` exists as a clean, named loadout in REFERENCE_GRAPH/INDEX.md and the correct file (`growthhub-creative-diversity-2026.md`) is reachable, but the agent spec has zero awareness of audit/evaluation as a dispatch mode — a cold agent given only `task_type: "pack-level-audit"` and no explicit `methodology_loadout_id` would likely fall through to generation-default behavior.
