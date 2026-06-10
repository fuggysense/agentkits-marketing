# Copy Subsystem Streamline — Execution Plan (2026-06-02)

Companion to `copy-subsystem-audit-260602.md`.

## STATUS — 2026-06-02 (post-validation execution)

After a validation fan-out against Jerel's session history + repo/global memory (his steer: "you don't know good taste — take what I gave you and validate; prefer deletion; 80/20"), several audit claims were **disproven on disk** and the plan shrank:

- **DONE — Phase 1 (bug fixes):** unified the sales-letter output-path divergence (`commands/copy/sales-letter.md`); removed 3 hardcoded absolute paths + phantom `eval-schwartz`/`eval-hormozi` "exists" refs from `agents/eval-halbert.md`, `agents/eval-sales-letter.md`, `~/.claude/agents/copy-sales-letter.md`. Verified clean.
- **DONE — Phase 2a (routing):** created `docs/copy-routing-map.md` (the "when to use which" deliverable); added terse canonical-owner precedence + the copywriting/copy-editing/copy-coach split + readability(audience-relative) / English-only / one-kill-list overrides to `routing-overrides.md`; clarified twin `routing-table.md` + pointer in `_index.md`. Trimmed duplicated lines after a deletion-bias pass.
- **CANCELLED — Phase 2b:** `/content:ads` is NOT dead — `/copy:ad` delegates to it (engine layer, not redundant). `/content:*` is the engine `/copy:*` wraps. Nothing to delete; the "start at /copy" signpost already exists in `_index`.
- **NO-OP — Phase 3 (CCC):** `copy-coach/SKILL.md` is already aligned (lean, references-not-duplicates, points at `forbidden-content-audit`). Adding a dispatch table would violate Jerel's locked "orchestration lives in folder CLAUDE.md, not the persona" decision. The "dual install" was a false positive — `.claude/skills` is a symlink to `../skills` (one inode).
- **TASTE-GATED — Phases 4–7:** kill-list dedup (different registers, not pure dup), offer-grounding standardization (needs active client), markup-convention retire-vs-keep, model-pin, kayhng path, eval-persona build, testing rig. All require Jerel's decision — surfaced to him, not freelanced.

**Original plan below retained for reference.** — Plan only; no further edits until Jerel decides the taste-gated items.

## Decisions locked (from Jerel)

1. **Scope:** Fix confirmed bugs + lock routing. NO deep skill merges this pass (the 5 angle-primitive merge, email-sequence/marketing merge, /content↔/copy namespace merge are explicitly deferred to a v2).
2. **Front door:** `ccc` becomes the flexible copy-and-writing brain — handles one-off copy with no client, grounds on the offer when a client is active, and routes to other writing skills (LinkedIn, hooks, etc.). A dispatch table, not a rigid pipeline.
3. **Testing rig:** Sales-letter first. Finish the half-built letter rig, add a score-out-of-100, wire a one-line `/eval`. Hooks / ad / email / landing / LinkedIn checklists come later.
4. **Offer grounding:** Enforce + standardize, but the hard gate fires ONLY when a client is confirmed/active. One-off no-client work is never blocked.

## Target end-state (the streamlined model)

**Routing law: ONE canonical owner per deliverable; everything else is a signpost that redirects.**

| Deliverable | Canonical owner (engine) | Single command | Signpost / retire |
|---|---|---|---|
| Sales letter | `sales-letter-method` skill | `/copy:sales-letter` | `/content:sales-letter`, global agent → thin pointer |
| Headlines / ad text | `headline-bank` (Meta fields) | `/ads:headlines` | `/copy:headline`, `/content:ads` (delete) |
| Angles | `big-angle-spotter` | via `ad-concept-engine` | — |
| DCT ad batch | `ad-concept-engine` | `/ads:concepts` | — |
| Email / sequence | `email-sequence` (copy) + `email-marketing` (strategy) | `/content:email` (the live engine) | `/copy:email` simplified |
| Edit / de-AI | `copy-editing` | — | unslop / Sweep8 / writing all point to ONE kill-list |
| Offer | `offer-builder` (sole writer of offer.md) | `/offer:build` | onboarding/scaffolder write the same shape |
| Hooks | `viral-hooks-content-creator` / `script-skill` / `video-hook-variants` | (CCC recognizes "hook" intent) | — |
| Buyer research | `avatar-research` (profile) + `buyer-language-researcher` (dossier) | `/research` | clarified "which when" |

**The CCC brain (system-prompt layer):** `copy-coach/SKILL.md` gains a small DISPATCH TABLE + CONTEXT rule:
- Detect intent → name the canonical skill/command above.
- If a client context is active AND confirmed → load `_brand/offer.md` + `_brand/buyer-profile.md` first; refuse to write client copy if they're missing.
- If no client → proceed as one-off, no gate.
- Anti-slop floor = the global `/writing` skill (referenced, not duplicated). copy-coach = the persuasion layer on top.

**Anti-slop: one kill-list.** `forbidden-content-audit.md` is canonical. `/writing`, `unslop`, `copy-editing` Sweep 8 reference it instead of carrying their own copy. Readability conflict resolved by explicit rule: **audience-relative register (V4) overrides `/writing`'s fixed grade 4–6 for insider/B2B copy; the grade target is scoped to consumer short-form.**

---

## Phases (each ≤5 files, verify between, decision point after)

### Phase 1 — Confirmed bug fixes (low-risk, reversible)
1. Unify sales-letter output path: `commands/copy/sales-letter.md` + `commands/content/sales-letter.md` write to the SAME path (wrapper inherits engine's `clients/<slug>/sales-letters/`).
2. `~/.claude/agents/copy-sales-letter.md` — remove hardcoded absolute path (invoke skill by name); correct "4 independent evaluators" count.
3. `agents/eval-halbert.md` + `agents/eval-sales-letter.md` — remove phantom `eval-schwartz`/`eval-hormozi` sibling refs; fix the bogus "12-reviewer stack" count.
**Verify:** grep confirms no remaining refs to the old path or the two phantom agents; counts match reality.
**Checkpoint:** offer to `git commit` before starting (local only, no push).

### Phase 2a — Routing decision logic (the "when to use which")
4. NEW `docs/copy-routing-map.md` — one-page decision map (the canonical "which front door for what"). This is the artifact that solves "I don't know which to use."
5. `routing-overrides.md` — add copy precedence rules: canonical owner per deliverable, the copywriting-vs-copy-editing-vs-copy-coach split, the readability override, the language-rule override (always English).
6. `.claude/rules/_index.md` — resolve the twin `routing-table.md` naming (mark which is authoritative); point to the new routing map.
**Verify:** the routing map names exactly one owner per deliverable; routing-overrides has no contradictions with _index.

### Phase 2b — Apply signposts to duplicates
7. Delete `/content:ads` (dead stub).
8. Add a short DEPRECATED→redirect header to the live-but-superseded `/content:*` duplicates (they currently still route silently). Batch ≤5 files; second batch if needed.
**Verify:** every deprecated command now redirects to its canonical owner; nothing routes silently.

### Phase 3 — CCC front-door upgrade (riskiest for daily use)
9. `skills/copy-coach/SKILL.md` — add the DISPATCH TABLE + client-context grounding rule + `/writing`-as-floor reference. Keep it lean (it's the system prompt; token budget matters).
10. Resolve the dual install: `skills/copy-coach/` stays canonical (ccc points there); `.claude/skills/copy-coach/` becomes a symlink. Same for `sales-letter-method` + `sales-letter-audit`.
**Verify:** `ccc "test"` still launches and loads the persona (manual — I can't fully verify a bg launch from here; Jerel confirms or I dry-run the path). The `--system-prompt-file` target path is unchanged.

### Phase 4 — Anti-slop single source
11. Confirm `forbidden-content-audit.md` canonical; convert `copy-editing` Sweep 8 + `unslop` integration to pointers.
12. Add a cross-reference between global `/writing` and the V4 kill-list (so they stop operating in mutual ignorance) + the readability override note.
**Verify:** one kill-list of record; others reference it by path; no contradictory readability targets.

### Phase 5 — Offer grounding (client-confirmed gate)
13. `skills/copywriting/SKILL.md` — read `_brand/offer.md` first; interview only fills genuine gaps.
14. Fix the path drift: copywriting-OS gates read `_brand/buyer-profile.md` (not flat root).
15. Add the conditional gate to the AGENT ENTRY CONTRACT: when a client is confirmed/active, block client-copy writes unless `offer.md` + `buyer-profile.md` are in `loaded_paths[]`. (A lightweight validator note; full validator script optional.)
16. Standardize `offer.md` shape doc; migrate ONLY confirmed/active clients (identify them first; reconcile takekine's research-stage shape, migrate hazecraft/aura out of flat-root).
**Verify:** copywriting skill references offer.md; gate logic documented; active clients on one shape.

### Phase 6 — Testing rig (sales-letter first)
17. `evals/evals.json` — build eval #2 (cross-vertical) at minimum; mark #3.
18. Numeric scorer — weighted pass-rate from `assertion-library.json` → score-out-of-100 (the "80%" primitive).
19. `/eval` (or `/copy:eval`) command — runs the letter eval set on a draft, returns score + failed assertions, wired to `skill-creator/run_loop.py`.
20. Resolve prompt-contracts self-verify vs fresh-eyes (fresh-eyes wins; document it). Stub a "hooks/ad/email checklist = next" note.
**Verify:** `/eval <draft>` returns a number + failed-assertion list on a real letter.

### Phase 7 — Dead/stale strip (cleanup)
21. Remove: empty `corrections.md`/`learnings.md` stubs (or populate intent), `markup-convention` live-constraint refs, `claude-opus-4-7` pin, kayhng foreign path in `big-angle-spotter`, orphaned copy-coach quickrefs (wire into dispatch table OR delete), `_template.old/`, `neezanizam-260504-pre-reorg/`, `.DS_Store`.
**Verify:** grep for each stale token returns empty.

---

## Reality check / cost / risk

- **Compute cost: low.** This is markdown/prompt/config editing, not heavy generation. The testing rig (Phase 6) is the only part that spends on eval runs (~$0.40/eval per the existing protocol).
- **Biggest risk: Phase 3** — it edits the file `ccc` loads as its live system prompt. A bad edit breaks your daily copy workflow. Mitigation: keep the change additive, verify the launch path, commit before.
- **Reversibility:** git-tracked repo. I'll offer a checkpoint commit before Phases 1, 3, 5. No pushes without explicit say-so.
- **What this does NOT fix (deferred to v2, by your choice):** merging the 5 skeleton angle skills, the email-sequence/marketing overlap, the full `/content`↔`/copy` namespace collapse, and per-type testing checklists (hooks/ad/email/landing/LinkedIn).
- **Honest caveat:** I can't 100% verify a backgrounded `ccc` launch from this session. After Phase 3 I'll dry-run the system-prompt-file path resolves, but you may need to fire one `ccc` to confirm it feels right.

## Definition of done

- One canonical owner per deliverable, documented in `copy-routing-map.md`; every duplicate redirects.
- `ccc` launches, grounds on the offer when a client is active, routes one-offs cleanly.
- One kill-list; no contradictory readability rules.
- `/eval <letter-draft>` returns a score-out-of-100 + failed assertions.
- No phantom agents, no path divergence, no foreign/stale absolute paths.
