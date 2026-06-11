# CONTEXT.md Pattern — TakeKine ICM

The rules every CONTEXT.md in this client must follow. Read before adding or editing one.

## The ICM 5-Layer Hierarchy

Source: Van Clief & McDermott, *In-Context Modeling for Agentic Software* (arXiv:2603.16021v2).

| Layer | File | Question | Budget |
|---|---|---|---|
| L0 | `CLAUDE.md` | Where am I? | ~800 tok |
| L1 | `CONTEXT.md` (root) | Where do I go? | ~300 tok |
| L2 | `CONTEXT.md` (per stage) | What do I do? | 200–500 tok |
| L3 | `_brand/`, `_config/`, `_references/`, stage `references/` | What rules apply? | 500–2k tok |
| L4 | stage outputs (or stage folder if flat) | What am I working with? | varies |

**Factory vs product:** L3 = stable rules (voice, buyer, offer, conventions). L4 = per-run artifacts (concepts, scripts, renders). Never mix.

## The 3-section stage contract (ICM canonical)

Every L2 stage CONTEXT.md follows this shape:

```
## Inputs
- Layer 4 (working): ../<prior-stage>/<artifact>
- Layer 3 (reference): ../../_brand/<file>.md
- Layer 3 (reference): references/<stage-local>.md

## Process
[1-3 sentences: what the agent does in this stage. Name the agent.]

## Outputs
- <filename>: <what it is>
- <filename>: <what it is>
  - Done: <crisp condition for "this phase is complete">
```

Three sections. No separate "Done-looks-like" header — fold into Outputs as a sub-bullet on the last output line.

**Non-stage rooms** (like `_brand/`, `_swipe/`) use freer sections: `What lives here / Files / Subfolders / Load order`. Only include sections that have real content.

## Three justified deviations from canonical ICM

| Deviation | Why |
|---|---|
| **Flat-in-phase outputs** (no `output/` subfolder inside each phase) | The 7-phase concept pipeline is more granular than ICM's 3-stage example. Forcing `output/` subfolders breaks every vid-director path (`02_ag1-options/concepts.json` would become `02_ag1-options/output/concepts.json`). The phase folder IS the output. |
| **Concept-as-workspace** (each concept gets its own L0/L1 inside `campaigns/<c>/video-concepts/<slug>/`) | A campaign holds N concept variants; each is an independent run of the 7-phase pipeline. Treating each concept as its own ICM workspace gives clean isolation between variants. |
| **`_brand/` is client-shared L3** (not per-campaign) | Voice / buyer / offer don't change per campaign for the same client. Matches ICM's "configure the factory" — config once, reuse everywhere. |

These are intentional. Do not "fix" them by adding `output/` subfolders, hoisting `_brand/` into campaigns, or flattening concepts into a single workspace.

## Do not duplicate

The point of layered context is that each rule lives in *exactly one place*. Things that DO NOT belong in a CONTEXT.md:

| Don't put... | It already lives in... |
|---|---|
| Global rules (medical claims, asset promotion, manual-approval gates) | Root `CLAUDE.md` |
| Brand voice rules (banned phrases, tone) | `_brand/brand-voice.md` |
| Claim guardrails for the SL | `_brand/funnel-research/sales-letter-extract-*.md` |
| Big-Idea allowed/forbidden expressions | `_brand/big-ideas/<id>.md` |
| Higgsfield path conventions | `_brand/higgsfield-reference-routing.json` |
| "When this file changes…" boilerplate | This pattern doc — covered once, here |
| The agent's prompt or system instructions | The agent's spec file |

When this file (or any CONTEXT.md) changes — agents downstream pick it up on next read. No registry update, no rebuild step. The pattern is read-on-demand.

## One-screen rule

Target **~70 lines**, hard cap **~100 lines**. If a CONTEXT.md needs more than that to explain itself, the room is the wrong level of granularity. Push detail into a referenced `.md` file inside that room. CONTEXT.md is signage, not the map.

## How to add a new room's CONTEXT.md

1. Read this file
2. Pick the closest existing CONTEXT.md as your shape reference
   - Stage room? Copy from `_templates/concept-phases/03_scripts-CONTEXT.md`
   - Reference room? Copy from `_brand/CONTEXT.md`
   - Collection room (lists subfolders)? Copy from `campaigns/CONTEXT.md`
3. Use the right shape:
   - **L2 stage** → `Inputs / Process / Outputs`
   - **L3 reference / collection** → `What lives here / Files / Subfolders / Load order` (only sections with content)
4. Write minimum-viable content. Strip anything an agent could infer from filenames + this pattern doc.
5. Verify line count: `wc -l CONTEXT.md` — under 100 lines mandatory
6. If editing a phase template in `_templates/concept-phases/`, no per-concept change needed — concepts just point to the template.
