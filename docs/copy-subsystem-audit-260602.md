# Copywriting Subsystem Audit — 2026-06-02

**Scope:** every copy-touching component across three roots — global (`~/.claude/`), the Marketing project, and the CCC `copy-coach` persona layer. Produced by an 8-mapper parallel audit + cross-zone conflict synthesis (9 agents, ~1M tokens). Every "CONFIRMED" claim below was checked against files on disk.

**The one-line diagnosis:** the copy system is not broken — it's *triplicated*. Two architecture generations (older `/content:*` + `./docs/` paths, newer `/copy:*` + `clients/<slug>/` paths) coexist and wrap each other while assuming incompatible folder layouts. On top of that, the global `/writing` skill enforces a third, separate copy doctrine that never meets the project stack. The result: 4–6 ways to start any copy task, no deterministic router, and several silent path/agent bugs.

---

## 1. The flows you have today (when each *actually* fires)

| Deliverable | Canonical engine today | Wrappers / duplicates on top | Persona layer |
|---|---|---|---|
| **Sales letter** | `/content:sales-letter` (v1.0.0, real 5-phase engine, `clients/<slug>/` paths) | `/copy:sales-letter` (wraps it, adds 9 reviewers → 12 total), `sales-letter-method` skill, `copy-sales-letter` global agent | `ccc` for Big-Idea/spine front-half |
| **Headlines / ad copy** | `/ads:headlines` + `headline-bank` skill (bank); `ad-concept-engine` assembles DCT, delegates angles to `big-angle-spotter` | `/copy:headline`, `/copy:ad` (thin v0.1.0 wrappers), `/content:ads` (near-dead stub) | — |
| **Email / sequence** | `/content:email` (v1.0.0 engine) + `email-sequence` / `email-marketing` skills | `/copy:email` (wraps, 3 layers deep), `/sequence:*` commands | — |
| **Edit / de-AI** | context-dependent, **no single owner** | `copy-editing`, `unslop`, `forbidden-content-audit`, `brand-voice-guardian`, `/writing` hook, `verification-loops`, `self-contained-reviewer`, copy-coach cold-reader — 5–6 overlapping | `ccc` stylize/cold-reader |
| **Offer** | `offer-builder` (declared nucleus) | `client-onboarding` Path B + `brand-scaffolder` also write `offer.md`; `copywriting` skill ignores all three and interviews the user | — |
| **Buyer research** | `avatar-research` (`buyer-profile.md`) | `buyer-language-researcher` agent, `/research`, `source-of-truth` — 2–3 unreconciled producers | — |

The CCC pattern (`ccc()` zsh function loads `copy-coach/SKILL.md` as `--system-prompt-file`, replacing the coding harness) **already does** what you described wanting — it's proven and clean. The work is extending/consolidating around it, not inventing it.

---

## 2. Duplicate entry points (the "I don't know which to use" problem)

**Six deliverables, each with 4–8 competing front doors.** Full detail:

- **Sales letter — 6 entries.** CONFIRMED bug: `/copy:sales-letter` declares output `clients/<slug>/copy-system/outputs/sales-letters/` (line 77) while the engine it calls, `/content:sales-letter`, writes to `clients/<slug>/sales-letters/` (lines 214/223). Silent path divergence — whichever runs last wins. The global `copy-sales-letter` agent hardcodes an absolute path to the project skill (line 12) — breaks off-machine.
- **Headlines — 8 entries.** `big-angle-spotter` AND `headline-bank` both emit "headlines"; trigger words collide. `/copy:headline` admits it's a stopgap pending a "Phase 2.6" upgrade that may not exist.
- **Email — 6 entries, 3 nested command layers** for one deliverable. `email-sequence` vs `email-marketing` have a circular feeds-into relationship and share the same agent + metric.
- **Edit/de-AI — 9 entries, no owner.** ~70% identical kill-lists duplicated in FOUR places (forbidden-content-audit F4, unslop profiles, copy-editing Sweep 8, global /writing banned-words). Dedup is a tracked-but-DEFERRED cleanup ("Move 4").
- **Offer — 5 entries.** Three skills can each write `_brand/offer.md`; `copywriting` bypasses all of them by interviewing. FOUR different `offer.md` shapes exist across clients.
- **Anti-slop — 4 entries in mutual ignorance.** CONFIRMED zero cross-references between global `/writing` and the V4 stack. A V4 sub-agent propagates `forbidden-content-audit` but never loads `/writing` (sub-agents don't inherit the hook).

---

## 3. Principle conflicts (real contradictions, not just overlap)

| Severity | Topic | The conflict |
|---|---|---|
| **HIGH** | Readability target | `/writing` mandates FIXED Hemingway grade 4–6 + "read aloud literally"; copy-coach + sales-letter-method mandate AUDIENCE-RELATIVE register (3rd-grade SG-English for ESL, professional/technical for insiders). For a B2B/insider letter these genuinely disagree. |
| **HIGH** | Self-critique vs fresh-eyes | Global CLAUDE.md §8 + verification-loops + copy-coach cold-reader FORBID self-critique, mandate a fresh sub-agent. But `prompt-contracts` step 5 and `/writing`'s 16-item self-check run inline in the drafting context. Opposite mechanisms. |
| **HIGH** | Canonical brand-voice file | FOUR "brand voice" artifacts at three locations. `copywriter` and `brand-voice-guardian` — two agents in the SAME pipeline — name different canonical voice files. |
| **HIGH** | Selective vs verbatim offer load | `clients/README.md` permits selective `_brand/` loading; repo CLAUDE.md line 32 says copy sessions MUST load offer verbatim; `copywriting` skill does neither (interviews). Three docs disagree; enforcement is prose-only. |
| MED | Master-selection | `/writing` picks ONE primary master via diagnostic; V4 runs ALL masters as parallel gates. Same masters, opposite orchestration. |
| MED | Language rule | Several v1.0.0 skills carry "respond in user's language" boilerplate — contradicts your global "always reply in English." Latent. |
| MED | Activation gate | `skill-activation.md` requires confirm-before-running; `routing-overrides.md` says copy auto-loads; One-Word Mode says just execute. Copy auto-fires, contradicting the confirm gate. |
| LOW | Master pantheon | `/writing` canonizes Hopkins/Caples/Ogilvy; V4 drops them, adds Hormozi + "Mark Masters." Different lineages. |

---

## 4. Routing ambiguities

- **Generic "write copy"** routes to copywriting / copy-coach / copy-editing / `/copy` router with NO precedence. Only guardrail is one `routing-overrides.md` hard-skip. No override for the copywriting-vs-copy-editing-vs-copy-coach split.
- **Single angle/claim primitive** → 5 skeleton skills (persuasive-premise, problem-promise, usp-generator, unique-mechanism-problem/solution) from the same lineage, NO decision rule, all v0.1.0 unvalidated.
- **Review a finished letter** → 8–12 evaluation passes with 3+ rubrics can fire. No orchestrator decides which.
- **Two `routing-table.md` files** CONFIRMED (auto-generated `.claude/rules/` vs hand-curated `docs/system-rules/details/`) — stale-vs-fresh drift.
- **Persona evaluators partly PHANTOM:** CONFIRMED `eval-halbert` + `eval-sales-letter` exist; `eval-schwartz` + `eval-hormozi` do NOT, yet are referenced as siblings and counted in "4 independent evaluators." Dispatches expecting them silently get nothing.

---

## 5. Layering issues

- **Two architecture generations read different folder structures** — `/content:*` + `/brand:*` use `./docs/`; `/copy:*` uses `clients/<slug>/`. The `/copy` layer wraps the older layer but assumes incompatible paths. Deepest structural conflict.
- **copy-coach lives at `skills/` (non-dotted); vid-director at `.claude/skills/` (dotted).** copy-coach works only because `ccc` points straight at it; its YAML triggers likely don't fire as a normal Skill-tool skill. AND copy-coach / sales-letter-method / sales-letter-audit each exist at BOTH `skills/<name>/` and `.claude/skills/<name>/` (CONFIRMED) — edit-the-wrong-copy drift.
- **Reviewers exist in two rosters:** the 5 files in `sales-letter-method/reviewers/` ≠ the 5 NAMED in the Phase 3 spec. "The 5 reviewers" means two different things.
- **Offer-grounding mandated at the wrong layer** — only prose in CLAUDE.md, not in the copywriting skill or icm skill. No validator confirms `offer.md` is in `loaded_paths[]`.
- **A GLOBAL agent depends on a PROJECT skill by absolute path** (`copy-sales-letter.md` line 12).
- **Conflict-detection tooling exists but is unwired:** `scan_conflicts.py` / `scan_similarity.py` not wired into `refresh-registry.js`. New copy skills silently increase ambiguity.

---

## 6. Offer-grounding gaps (the "know the offer in the client folder" goal)

- The base `copywriting` skill is an offer-grounding ISLAND — grep found ZERO references to `_brand/offer.md`, `buyer-profile.md`, `context-profile.json`, or `context_receipt`. It learns the offer by INTERVIEW.
- Even the grounded path (copywriting-OS gates) reads `buyer-profile.md`/testimonials for DESIRE language, NOT `offer.md` for offer TERMS.
- **Path drift breaks the gate:** gates reference flat `clients/<slug>/buyer-profile.md`, current ICM layout is `_brand/buyer-profile.md`.
- **`offer.md` has 4 inconsistent shapes** across clients (template, takekine research-stage, harmony service-catalog, hazecraft/aura flat-root with no `_brand/`).
- For takekine, "knowing the offer" requires a **9-hop traversal** ending at an empty `brand-voice.md` stub.

---

## 7. Testing / iteration infra (the "test → reiterate → 80%" goal)

**Exists (reusable bones):**
- `evals/assertion-library.json` — 118 assertions across 18 axes, severity-calibrated. **Sales-letter ONLY.**
- `evals/evals.json` — 1 real eval + 2 TODO stubs; has an iteration_protocol + decision_gate.
- `skill-creator` harness (`run_loop.py` + `run_eval` + `aggregate_benchmark.py`) — the spawn-with-skill-vs-baseline / grade / aggregate / diff engine.
- `verification-loops` (Implement→Review→Resolve), `multi-agent-consensus` (N-agent scoring + variance), `prompt-contracts` (GOAL/CONSTRAINTS/FORMAT/FAILURE — the natural front for an "80% / beats-baseline" target), Phase-3 reviewer stack, `forbidden-content-audit` (the one NUMERIC pass primitive), `routing-tester`.

**Gaps:**
- No automated runner wired for copy evals — the harness has only ever been run BY HAND. No `/eval` command.
- No assertion library for landing / ad / email / headline — rubric exists for exactly ONE copy type.
- No numeric pass-THRESHOLD primitive — gates output PASS/HOLD/REWRITE, not a %. The "80%" target has nothing to attach to.
- No single orchestrator composes prompt-contracts + verification-loops + consensus into one "contract → generate → score → iterate to 80%" loop.
- The "mini-regression" pattern referenced in handoffs returned ZERO files on grep — likely unbuilt.

---

## 8. Orphans / dead / cruft (deletion candidates)

- `copy-coach/corrections.md` + `learnings.md` — 0 bytes, never written.
- `copy-coach/references/awareness-sophistication-quickref.md` + `headline-openings-quickref.md` — ORPHANED, not in the dispatch table.
- 5 skeleton skills (persuasive-premise etc.) — all v0.1.0, TODO examples, reference a `canonical-sources.md` that doesn't exist; two share identical copy-pasted boilerplate.
- `eval-schwartz` + `eval-hormozi` — PHANTOM.
- `/content:ads` — strongest deletion candidate (generic stub).
- `/content:*` — marked DEPRECATED in `_index.md` but files still physically present and routable.
- Stale: `markup-convention` retired but still cited as a live CONSTRAINT; `claude-opus-4-7` model pin; `big-angle-spotter` hardcodes a foreign user's path (`/Users/kayhng/...`); `_template.old/`, `neezanizam-260504-pre-reorg/`, `.DS_Store`.

---

## 9. Prioritized streamline opportunities (agent-proposed, payoff-sorted)

| Effort/Payoff | Move |
|---|---|
| **S / HIGH** | Fix wrapper-vs-engine output-path conflicts (sales-letter, headline). Wrapper inherits engine's path. |
| **M / HIGH** | ONE canonical kill list (`forbidden-content-audit`); every other anti-slop surface becomes a pointer. Cross-reference `/writing` ↔ V4. |
| **M / HIGH** | Delete/hard-deprecate the `/content:*` `./docs/`-path layer the `clients/<slug>/` migration superseded. |
| **M / HIGH** | Resolve phantom evaluators; reconcile the two reviewer rosters. |
| **M / HIGH** | Programmatic offer-grounding check + make `copywriting` READ `offer.md` instead of interviewing. |
| **L / HIGH** | Build the generic "test → 80%" loop on existing bones (contract → generate → fresh-eyes score → assertion-lib → run_loop). Needs: per-type assertion libs, numeric threshold primitive, `/eval` runner. |
| **L / MED** | Disambiguate or merge the 5 skeleton angle primitives. |
| **M / MED** | Resolve twin `routing-table.md`; wire `scan_conflicts.py` into registry refresh. |
| **S / MED** | Collapse duplicate skill installs (`skills/` vs `.claude/skills/`) to one home. |
| **M / MED** | Standardize `offer.md` to one shape; migrate flat-root clients. |
| **S / LOW** | Reconcile readability contradiction (audience-relative overrides fixed-grade for insider copy). |
| **S / LOW** | Strip dead/stale references. |

---

*Next step: streamlining plan, pending Jerel's direction on scope, operating mode, testing-loop scope, and offer-grounding strictness.*
