# CONTEXT — Phase eval: Buyer-Fit Gate

Canonical stage contract. Per-concept `eval/CONTEXT.md` points here. Not a sequential phase — fires twice per concept lifecycle, before AG1 and before AG2.

## Inputs

- Layer 4 (working): the artifact being evaluated — `../02_ag1-options/concepts.json` + `hook-variants.json` (pre-AG1) OR `../07_review/` stitched preview (pre-AG2)
- Layer 3 (reference): `clients/takekine/_brand/buyer-profile.md` (resolve target `micro_persona_id`)
- Layer 3 (reference): `clients/takekine/_brand/funnel.md` (lane × rung × persona match)
- Layer 3 (reference): `~/.claude/agents/eval-buyer-fit.md` (agent spec)

## Process

`eval-buyer-fit` agent (Sonnet, persistent, 3-cycle cap per vid-director.md §12). Scope is buyer fit only — does the artifact land for the named persona at the named awareness rung. Claim safety is NOT this agent's job (owned by `video-concept-seeder` + `video-prompt-pack-builder`). Three-cycle cap: if not PASS by cycle 3, escalate to operator. Each cycle writes one `buyer-fit-cycle-<N>.json`.

## Outputs

- `buyer-fit-cycle-<N>.json` — per-cycle verdict (`PASS` / `REVISE` + reasoning, `fired_at_phase: "4.6"` for AG1 / `"6.5"` for AG2)
  - **Hard precondition:** Latest cycle MUST be `verdict: "PASS"` before `html-publisher` renders AG1 or AG2 (enforced at routing layer)
  - **Bypass:** Only via `pipeline-state.json.eval_override` with operator timestamp + reason
