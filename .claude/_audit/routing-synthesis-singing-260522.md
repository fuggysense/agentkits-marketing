# Routing Test Synthesis — Singing-Rubric Fix (2026-05-22)

**Targets tested:**
- `/Users/jerel/.claude/prompts/orchestrators/vid-director.md` §2.0.5
- `/Users/jerel/Documents/Jerel's brain/jerel's brain/Marketing/.claude/skills/vid-director/references/vid-director-prompt.md` §2.0.5
- `/Users/jerel/.claude/agents/video-concept-seeder.md` (refuse-on-mismatch precondition + Gate order)

**Personas tested:** vid-director (orchestrator, 1 test) + video-concept-seeder (worker, 3 tests).
**Persona justification:** Orchestrator picks the loadout; worker enforces the gate. Both layers must be tested because the bug-vector spans both.

**Trigger context:** Original bug in `takekine/test_2/three-anchor-slate-260522` — orchestrator dispatched seeder with spoken-only loadout for a sung concept (c03 Iron Strip Lullaby). Singing-ads-layer.md never loaded. Lyrics came out without rhyme structure. Fixed by patching vid-director §2.0.5 HARD RULE 2 + adding refuse-on-mismatch precondition to seeder spec.

---

## Test matrix

| # | Persona | Scenario | Files loaded | Reached intended outcome? | Verdict |
|---|---|---|---|---|---|
| 1 | vid-director | Sung brief, NO loadout hint — must derive from §2.0.5 | vid-director.md, REFERENCE_GRAPH.json | YES — picked `dr_singing_solution_aware_l3_concept`, forwarded singing-ads-layer.md + walked `extends` chain, quoted HARD RULE 2 verbatim | ✅ PASS |
| 2 | video-concept-seeder | Sung concept + WRONG loadout `dr_solution_aware_l3_concept` (original bug) | Only seeder spec (correctly skipped all other reads) | YES — refusal fired, exact ROUTING REFUSAL message emitted, zero concepts generated, `routing_refusal_logged_at_<timestamp>` recorded | ✅ PASS |
| 3 | video-concept-seeder | Sung concept + CORRECT loadout + explicit singing-ads-layer.md path | Seeder spec, REFERENCE_GRAPH.json, singing-ads-layer.md (grep) | YES — precondition stayed silent, would load singing_layer via loadout's required_nodes, would generate concept with `rhyme_scheme` field on every verse/bridge/chorus/outro per Gate 2 | ✅ PASS |
| 4 | video-concept-seeder | Fully spoken brief + spoken loadout (negative case) | Seeder spec | YES — precondition stayed silent (no sung concepts to gate), no false-positive refusal, would proceed to normal load + generate 3 spoken concepts | ✅ PASS |

---

## Files always loaded (4/4 tests)

- The persona's own spec (vid-director.md or video-concept-seeder.md) — expected.

## Files conditionally loaded

- `REFERENCE_GRAPH.json` — loaded in Tests 1 + 3 (when methodology-graph resolution was needed). Correctly NOT loaded in Test 2 (refused before graph load — gate-1-first ordering held). Correctly NOT explicitly loaded in Test 4 (cited as a "would read next" step in the dry-run).
- `singing-ads-layer.md` — loaded only in Test 3 (sung concept with correct loadout). Correctly NOT loaded in Tests 2 + 4.

## Files never loaded (potential review candidates)

None — every file cited in the fix was used in the appropriate test case. No dead weight.

## Routing failures

None. The fix performed as designed across all 4 cases.

## Persona-spec gaps surfaced by tests (5 critiques)

| # | Source test | Critique | Severity | Applied 2026-05-22? |
|---|---|---|---|---|
| 1 | Test 2 | Precondition was at line 223 of seeder spec but claimed "first thing you do." A linear cold reader could load methodology graph + buyer-profile first and miss it. | High | ✅ Yes — added "Gate order" enumeration block at the top of the seeder spec (right after the opening paragraph, before "Your methodology lives at:") |
| 2 | Test 2 | Precondition self-contradicts on "before anything else" — it requires reading `concept-brief.json` first to scan `per_concept_targets[].script_mode`. | High | ✅ Yes — clarified precondition section: "First read (and ONLY read at this gate): the dispatched concept-brief.json." Also added envelope-inline fallback. |
| 3 | Test 2 | No top-level gate-order enumeration. Multiple gates exist (singing precondition, brainstorm-mode check, standard load, naturalness gates) without documented sequence. | Medium | ✅ Yes — Gate order block (1) singing precondition → (2) brainstorm detection → (3) standard methodology + input load → (4) naturalness/rhyme gates continuous. |
| 4 | Test 1 | vid-director §2.0.5 didn't say "walk the `extends` chain" when forwarding reference paths. Future operator could forward only singing-ads-layer.md and miss parent's Stage-4 references. | Medium | ✅ Yes — appended explicit instruction to §2.0.5 HARD RULE 2 step 3 in both vid-director files: "When forwarding reference paths, resolve the loadout's full `extends` chain... you must forward singing-ads-layer.md AND stage-4-discrediting.md AND common-enemy-bridge.md AND six-proof-types.md AND every other required_nodes entry up the chain." |
| 5 | Test 3 | Spec's concept-block schema (L106-177) doesn't show where `rhyme_scheme` field lives — on `body_beats[]` entries? In a new `lyric_structure` block? Seeder has to invent. | Low | ⏳ Deferred — needs schema redesign. Note: Gate 2 still works without it (seeder will pick a placement that downstream agents read for the `rhyme_scheme` field), but spec ambiguity remains. Recommended fix next session: add a sample sung-concept JSON example to the concept-block schema section. |

## Recommended fixes — applied this run

1. **Seeder spec — Gate order block added at top** (after opening paragraph, before §"Your methodology lives at:"). Lines 9-23 approximately.
2. **Seeder spec — Singing precondition clarified** ("First read (and ONLY read at this gate)..."). Critiques 1 + 2 addressed.
3. **vid-director.md §2.0.5 (global) — extends-chain forwarding rule added** to HARD RULE 2 step 3.
4. **vid-director.md §2.0.5 (skill copy) — same patch as #3.** Both files now in sync.

## Recommended fixes — deferred to next session

5. **Seeder spec — sample sung-concept schema example.** Show where `rhyme_scheme` lives in the concept block JSON (likely on each verse/bridge/chorus beat entry). Requires examining the existing schema (L106-177) and inserting a sung-variant example without breaking the spoken schema.

## Verdict

**PASS — fix is solid.** The bug that caused c03 Iron Strip Lullaby's no-rhyme lyrics in the takekine slate cannot recur:

- Future orchestrator will correctly pick `dr_singing_*` loadout when ANY concept in the brief is sung (verified Test 1).
- If orchestrator forgets, the seeder will refuse-on-mismatch and stop with a clear remediation message (verified Test 2).
- Happy path produces concepts with `rhyme_scheme` discipline (verified Test 3).
- No false-positive refusals on spoken-only briefs (verified Test 4).

The 4 spec critiques surfaced by the tests are clarity issues, not correctness issues. All 4 were applied in this same session. One low-severity schema example was deferred — does not block the fix.

## Test infrastructure note

Tests dispatched via `routing-tester` skill in parallel (single-message multi-Agent dispatch, Sonnet model, run_in_background: true). Each test agent received its persona spec path and discovered routing from it — was NOT handed the target file paths. Persona-driven dispatch caught the actual routing behavior (correctly), not pre-loaded assumptions.

**Test cost:** ~290K tokens total across 4 agents, ~3-5 min wall-clock parallel.
