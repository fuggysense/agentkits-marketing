# Routing Test Synthesis — Singing Routing FINAL (2026-05-22)

**Persona tested:** vid-director (orchestrator, Test 1) + video-concept-seeder (worker, Tests 2/3/4) + video-prompt-pack-builder (worker, Test C) + general-purpose Sonnet (Tests A/B/D + end-to-end Sonnet)

**Test cycle:** 8 cold-context Sonnet agents across two rounds (4 PASS-gate tests + 4 routing-layer A/B tests).

---

## Test matrix

| # | Persona | Scenario | Verdict | Singing layer reached at |
|---|---|---|---|---|
| 1 | vid-director | Sung brief, no loadout hint | ✅ PASS | Step 2 (via §2.0.5 HARD RULE 2) |
| 2 | seeder | Wrong loadout (original bug) | ✅ PASS | Step 1 = REFUSE on mismatch |
| 3 | seeder | Correct loadout | ✅ PASS | Step 1 silent → load via required_nodes |
| 4 | seeder | All-spoken brief | ✅ PASS | Gate silent (no false positive) |
| End-to-end | Sonnet | "Get me a Suno brief for c03 cold" | ✅ PASS | Reached final Suno brief drafted inline |
| A PRE-FIX | Sonnet | Suno keywords, no path | ❌ Routing dead-ends, agent improvises | — never reached |
| A POST-FIX | Sonnet | Same | ✅ PASS | Step 2 (5 keyword triggers fire simultaneously) |
| B PRE-FIX | Sonnet | Workspace path, no keywords | ⚠ Fragile (reaches via 3-hop prose chain) | Step 6 |
| B POST-FIX | Sonnet | Same | ✅ PASS | Step 5 (data-driven `script_mode` regex on first file read) |
| C POST-FIX | pack-builder | Direct dispatch bypassing orchestrator | ✅ PASS | Step 0a self-defense fires |
| D POST-FIX | Sonnet | Mixed script_mode value `"mixed (... 1 sung c03)"` | ✅ PASS | `script_mode.*sung` pattern catches it |

---

## Defense-in-depth (final state, 4 layers)

| Layer | What | When it fires |
|---|---|---|
| **L1 — Operator keyword triggers** | `routing-overrides.md` Disambiguation block lists 11 singing/Suno/jingle/lullaby keyword phrases → routes to `singing-ads-layer.md` + vid-director skill + `dr_singing_*` loadout | On natural-language operator prompts |
| **L2 — Data-driven content scan** | `routing-overrides.md` data-driven rule fires on regex `script_mode.*(singing\|sung\|lullaby\|jingle\|suno\|song)` matched against any `.json` file inside a `video-concepts/` workspace | When orchestrator reads workspace files (or any agent that scans them) |
| **L3 — Orchestrator HARD RULE** | `vid-director.md §2.0.5` HARD RULE 2 — "if any per_concept_target has script_mode: singing, dispatch seeder with `dr_singing_*` loadout AND forward full `extends` chain" | At orchestrator dispatch composition time |
| **L4 — Per-agent self-defense** | `video-concept-seeder` refuse-on-mismatch precondition + `video-prompt-pack-builder` Step 0a + `eval-buyer-fit` pre-Required-Inputs scan. Each independently scans dispatch + workspace-root files. Mandatory reads include `pipeline-state.json` + `concept-brief.json` + `concepts.json` regardless of forwarding. | At agent dispatch — catches direct-dispatch bypasses |

A failure in any one layer is caught by the next. The bug-vector that produced c03's no-rhyme lyrics in the original takekine slate cannot recur — it would have to fail all 4 layers simultaneously.

---

## Routing failures surfaced + fixed this session

| # | Failure mode | Root cause | Fix layer | Test that proved fix |
|---|---|---|---|---|
| 1 | Spoken-loadout dispatched for sung concept | Doc-contradiction in vid-director §2.0.5 vs §2.1 + no orchestrator HARD RULE | L3 (HARD RULE 2 added) | Test 1 |
| 2 | Seeder accepted wrong loadout silently | No agent-level self-defense | L4 (seeder refuse-on-mismatch precondition) | Test 2 |
| 3 | Natural-language Suno asks reached zero pipeline | No keyword triggers in routing-overrides | L1 (11 keyword triggers added) | Test A |
| 4 | Workspace-path-only required 3-hop prose discovery | No data-driven content rule | L2 (data-driven `script_mode` regex added) | Test B |
| 5 | Direct-dispatch bypass missed singing rubric | Pack-builder had no own self-defense | L4 (Step 0a added) | Test C |
| 6 | Mixed script_mode value didn't match clean regex | Pattern too narrow | L2 (broadened to `(singing\|sung\|lullaby\|jingle\|suno\|song)` consolidated regex) | Test D |
| 7 | Direct-dispatch narrow envelope omits workspace-root files | Step 0a scanned only forwarded files | L4 (mandatory workspace-root reads added — `pipeline-state.json` + `concept-brief.json` + `concepts.json`) | Test C residual |
| 8 | Doc-order vs execution-order in seeder spec | Refuse-gate at line 223 but claims "first" | Spec (Gate order block hoisted to top) | Test 2 |
| 9 | Spec self-contradicts on "before anything else" | Gate needed concept-brief.json read first | Spec (clarified "first read = concept-brief.json for gate check") | Test 2 |
| 10 | vid-director §2.0.5 didn't say "walk extends chain" | Operator could forward only singing-ads-layer | Spec (extends-chain note added to HARD RULE 2 step 3) | Test 1 |

10 routing failures identified, **10 fixed in this session.**

---

## Files modified (final inventory)

| File | Edits |
|---|---|
| `~/.claude/prompts/orchestrators/vid-director.md` §2.0.5 | HARD RULE 2 added + extends-chain walk note |
| `~/Marketing/.claude/skills/vid-director/references/vid-director-prompt.md` §2.0.5 | Same patch as global |
| `~/.claude/agents/video-concept-seeder.md` | Gate order block at top + Singing precondition (refuse-on-mismatch) + Conversational naturalness + rhyme discipline gates |
| `~/.claude/agents/video-prompt-pack-builder.md` | Step 0a singing self-defense + mandatory workspace-root scan reads |
| `~/.claude/agents/eval-buyer-fit.md` | Singing self-defense before Required Inputs + mandatory workspace-root scan reads |
| `~/Marketing/.claude/rules/routing-overrides.md` | 11 keyword triggers + data-driven rule with consolidated regex `(singing\|sung\|lullaby\|jingle\|suno\|song)` |

---

## Verdict

**PASS — singing routing is hardened across 4 independent layers.** All 10 surfaced failure modes have spec or agent-level fixes. The bug-vector that produced c03's no-rhyme jargon lyrics cannot recur without simultaneous failure of every layer.

**Outstanding deferred:** sung-concept schema example in seeder spec (low severity — Gate 2 works without it; concepts get `rhyme_scheme` field on each verse/bridge object whether the schema doc shows the placement or not).

**Cost of audit:** ~8 test agents × ~40-90K tokens each ≈ 480K tokens across the session. Spec edits: 11 across 6 files. Time: ~3 hours wall-clock (most was test-agent runtime in parallel).
