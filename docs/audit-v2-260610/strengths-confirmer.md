# Strengths Confirmer — What Works and Must Survive the Rebuild

Audit date 2026-06-10 (SGT). Repo root: `/Users/jerel/Documents/Jerel's brain/jerel's brain/Marketing`.
Method: every candidate re-read against the cited artifact THIS session (FACT) or interpreted (JUDGMENT). Paths repo-relative unless `~`-prefixed.
Jargon: **gate** = checkpoint that must pass before the next stage runs; **fail-closed** = refuses to proceed when an input is missing rather than guessing; **DCT** = one Meta ad test; **sidecar** = a `.json` file written next to an output recording how it was made.

Verdict legend: CONFIRMED (re-verified, protect it) · PARTIAL (works but has a caveat) · NOT-CONFIRMED.

---

## Candidate-by-candidate

### 1. Hardened angle gate — CONFIRMED (the single strongest safety mechanism in the repo)
- FACT — `~/AI workflows/big-angle-spotter/scripts/run_pipeline.py:1197-1210`: `--hardened` is fail-closed — `OFFER is required`, `--buyer-profile is required`, buyer-profile must exist AND be ≥80 chars ("a stub file can't ground real scoring"). Verified by reading the lines.
- FACT — The gate is **code-authoritative, not model-authoritative**: `run_pipeline.py:791` `decided = "PASS" if min_score >= threshold else "FAIL"`; the scoring prompt at :375 literally tells the model "downstream code computes pass/fail from a fixed threshold, so score honestly rather than steering a verdict." Malformed scores fail closed (:767 "min_score 0").
- FACT — Real run proof: `clients/eugene-chieng/campaigns/upgrader-ads/dcts/dct-002-math-blind/angle-run-260609/_run.log:2-18` — loop 1 banked only 2/10 → REVISE with named regen targets → loop 2 banked 6/10 → SET PASS. The regen loop is monotonic (banked winners locked, only failures regenerate — `run_pipeline.py:954-987`).
- FACT — The scored JSON is genuine machine output: `02_gate_resonance_loop2.json` carries per-angle 1-5 scores on 5 dimensions (voc_mirror, core_pain_hit, awareness_match, distinct, not_saturated), per-angle verdict, weakest dimension, evidence quote, fix-if-fail, code-set `set_verdict`, `banked_ids`. Verified by parsing.
- CAVEAT (knocks it to "protect with a fix"): the gate is **opt-in and undocumented** — SKILL.md never mentions `--hardened` (A1:31). It only fires if the operator remembers a flag. The citation audit is **advisory only** — it warned A01/A03 cite non-verbatim evidence and did not block (`_run.log:13`); A01 still shipped.
- PROTECT: make `--hardened` the default for client work and document it; promote the advisory citation audit to a blocking gate. This is the one place where "code decides, model judges" is implemented correctly — the rebuild's whole grounding story should be built on this pattern, not around it.

### 2. Copy → dct.json byte-fidelity — CONFIRMED
- FACT — A02 `primary_text` in `dct-002-math-blind/dct.json` is byte-identical to the signed-off source `wave-1-copy-260610-v2.md:38-52` — every sentence matched, including "He was sitting on close to a negative $200,000." Verified by reading both.
- FACT — 10/10 render sidecar `prompt` fields exactly equal the matching `dct.json image_pool.images[].image_prompt` — re-confirmed programmatically this session (parsed all 10 sidecars + dct.json: `sidecars: 10, exact prompt matches: 10`).
- JUDGMENT — The operator's hand-assembly stage does NOT corrupt the signed-off text. What a human approved is what got rendered. That fidelity is the trust spine of the whole money path.
- PROTECT: whatever replaces hand-assembly (an emitter that writes the new `dct.json` shape) must preserve verbatim copy and prompt strings — add a diff-check between approved-copy and emitted-dct as a gate so fidelity survives automation.

### 3. Eugene avatar traceability — CONFIRMED
- FACT — Persona quote "to be honest, I also did not really go and look into it" is tagged `[VERBATIM — v10 [00:21]]` in `_brand/avatars/avatar-2-math-blind-upgrader.md:51,68,136` and the raw transcript `_brand/brand-assets/testimonials/transcripts/raw/v10-square2.txt` exists on disk (line 5 = "me and my wife, we were really shocked to see this figure").
- FACT — The "accrual interest … out of my mind" quote traces to `avatar-2…md:172` cited `v01 [11:24-11:37]`; the v01 transcript exists (`v01-2nd-couple.txt:42-43` = the "HDB after HDB" line). The avatar file header (:2) records Eugene's own sign-off 2026-06-09.
- JUDGMENT — This is a real grounded chain: persona claims trace to client-testimonial transcripts on disk, with timestamps, not model memory. Strongest VoC grounding observed across clients.
- PROTECT: keep raw transcripts in `_brand/` and keep timestamp citations inline in avatar files; the rebuild should make this traceability *checkable* (a script that verifies every VERBATIM tag resolves to a transcript line) rather than convention.

### 4. eval-buyer-fit HARD gate (video lane) — CONFIRMED
- FACT — `skills/vid-director/SKILL.md:48`: eval-buyer-fit is a "Brand-alignment **HARD GATE** on AG1, AG2, and any html-publisher dispatch," persistent with a 3-cycle cap.
- FACT — Enforced at the render layer, not just declared: `.claude/rules/routing-overrides.md:97-102` — any AG1/AG2 HTML publish MUST verify `<workspace>/eval/buyer-fit-cycle-<N>.json` has `verdict: "PASS"`; if missing/non-PASS, "Refuse to render." Bypass requires an operator-logged `eval_override` with timestamp + reason. Defense-in-depth: every downstream agent carries the same self-check (:30).
- JUDGMENT — This is the strongest gating architecture in the repo and the statics lane has no equivalent (the statics lane's analogue — a buyer-fit/claim gate before spend — is exactly the hole that let invented numerals ship; see the gaps report). 
- PROTECT: port the eval-buyer-fit pattern (refuse-to-publish unless a PASS verdict file exists, operator-override logged) into the statics lane before render/upload. It is the template for closing the statics claim-gate gap.

### 5. sales-letter-method reviewer chain — CONFIRMED (strongest gate stack in the repo)
- FACT — `skills/sales-letter-method/SKILL.md:82` "Drafters running without the Phase 0.7 document is a hard error"; :88 "Five reviewers fire in parallel in isolated contexts. Skip any one and the review is broken"; :91 "Any FAIL stops the ship."
- FACT — The five reviewer files physically exist (`reviewers/`: buyer-lens, coherence, copy-chief, pre-ship-checklist, self-contained) plus two eval agents (eval-halbert, eval-sales-letter) wired in `references/phase-3-reviewer-stack.md:16-24`.
- FACT — Phase 4 ship-gate runs in isolation: `references/phase-4-preship.md:22` "Spawn the `sales-letter-auditor` agent in an **isolated context window**. Do not run this in the same session that wrote the letter"; :52 "any lens marked FAIL → the letter does not ship until the proposed fix is applied."
- CAVEAT — `prompt-template.md` contains "MECHANISM NAME … If none, invent one that fits" (A1:80) — an invite to mechanism-wash thin offers, sitting beside the Phase 0.5 claim audit. Watch this in rebuild.
- PROTECT: this is the gold-standard "isolated fresh-eyes reviewer + FAIL-stops-ship" pattern. Keep it; make it the model for any high-stakes deliverable gate.

### 6. feedback-router fail-closed thresholds — PARTIAL (logic sound, wiring dead)
- FACT — `skills/feedback-router/references/routing-criteria.md:9-19`: hard pre-routing gates (min S$200/creative, S$600/batch, 7 days, 5,000 impressions, populated tracker); "If any pre-routing gate fails → output: `INSUFFICIENT_DATA`. Do not route." Client-overridable. The most fail-closed decision logic in the repo.
- CAVEAT 1 — The gate reads a **dead data shape**: it requires "dct-tracker.json Performance table populated" (:14), but the pipeline migrated off `dct-tracker.json` to `dct.json` on 2026-06-08 (A2:§1). The source-of-truth the gate checks no longer exists for new waves.
- CAVEAT 2 — Frontmatter requires a `meta-ads` MCP that does not exist (`SKILL.md:28-29`; the repo rule says "Meta = CLI, not MCP"). All three routes resolve to the retired `/ads:concepts` command (A1:115). The router's *output* is a recommendation the operator cannot run verbatim.
- PROTECT: keep the threshold logic verbatim (S$ floors, 7d, 5k impressions, INSUFFICIENT_DATA fail-closed) — it is correct. Repoint the data source to `dct.json`, swap the MCP requirement for the `meta` CLI, and give it a live route target. The *brain* survives; the *plumbing* must be rebuilt.

### 7. PAUSED-only Meta uploads — CONFIRMED (code-enforced, defense-in-depth)
- FACT — Not just a default: `skills/meta-ads-uploader/scripts/meta_api.py:513-515` — `if status != "PAUSED": self._log("WARNING: Overriding status to PAUSED …"); status = "PAUSED"`. The code forces PAUSED even if a caller passes something else. SKILL.md:252 confirms "the `create_ad` method forces PAUSED regardless of input."
- FACT — Operator-enables-in-Ads-Manager is the documented rule: `docs/system-rules/hitl-gates.md:5-6` (any spend / publishing to live platforms = BLOCK+ASK); D-stakeholders.md §4 "ads created PAUSED; only a human un-pauses in Ads Manager ('Founder reviews → enables. NEVER enable from here')."
- PROTECT: keep the code-level forcing (not just a config default) — it is the single firewall preventing an agent from spending money. Any rebuilt uploader must retain the same "force PAUSED in the create call" guarantee.

### 8. Secrets hygiene — CONFIRMED (re-verified this session)
- FACT — `git check-ignore` matches all real secrets: `credentials/gsheets-service-account.json`, `credentials/oauth_token.json`, `scripts/modal/credentials.json`, `.env`, `.env.bak-260607-171106`. `git ls-files credentials/ scripts/modal/credentials.json` returns EMPTY (untracked). Only `.env.example` + `.claude/.env.example` are tracked.
- JUDGMENT — Real service-account private keys and tokens sit on disk but have never been committed. The gitignore discipline holds.
- PROTECT: keep `credentials/` and `scripts/modal/credentials.json` in `.gitignore`; the rebuild must not relocate secrets into a tracked path. Pair with a pre-commit secret-scan if the rebuild adds CI.

### 9. Render sidecar provenance — CONFIRMED (pervasive, not a one-off)
- FACT — `scripts/ad-images/render.py:158-188` writes a `.png.meta.json` sidecar for EVERY render recording engine, style, size, refs, `source` (`--from-tracker` path or `inline-prompt`), prompt, and out path.
- FACT — Sidecars are pervasive: 52 across `clients/` (incl. neezanizam buyer-funnel proof wave: `BF11_…png.meta.json`, `BF17_…`, `BF04_…`), not just the eugene workspace. Each records exactly what generated the image.
- JUDGMENT — This is the cleanest provenance layer in the repo: you can always reconstruct what prompt + engine produced any creative. It is what made the 10/10 fidelity check (candidate 2) possible.
- PROTECT: keep the every-render-writes-a-sidecar invariant. The rebuild should extend the same provenance pattern to the copy and sheet stages (which currently have no equivalent record — see gaps).

### 10. Pipeline-state phase gating + ICM validator — CONFIRMED
- FACT — `skills/ad-concept-engine/SKILL.md:234,276,356,570,618` documents 5 HITL gates (Gate 0 persona, Gate 1 angle, Gate 2 batch, Gate 3 creative, Gate 4 tracker). vid-director AG0/AG1/AG2 ceremony (candidate 4). Eugene `pipeline-state.json` is at `current_phase: phase_5_upload` with launch gates outstanding — the state machine is real and observed.
- FACT — The ICM validator is live machinery: `~/.claude/skills/icm/marketing-scaffold/scripts/validate-icm.sh` exists + is executable; per-client JSON output (e.g. `validate-harmony-wellness.json` = `{score:"7/7", verdict:"PASS — ICM Compliant", rules:[7 PASS/FAIL rows]}`). It scores 7 structural rules and is honest about failures (the template itself scores 3/7).
- CAVEAT — ACE has a "Legacy mode" escape hatch that lets the DCT engine run without avatar research (A1:46); the corrections.md compounding loop is healthy ONLY for ad-concept-engine (12+ dated entries, re-read: em-dash bans, AI-hook bans, "validate fears then reframe") and dormant/empty for most other skills (A1:§3.4).
- PROTECT: keep the explicit-phase state file + per-stage HITL gates as the orchestration backbone; keep the ICM validator as the structural conformance check. The rebuild should make these the default (not opt-out) and revive the corrections loop repo-wide.

### 11. Cold-context review pattern — CONFIRMED (triple-anchored)
- FACT — `agents/sales-letter-auditor.md:11` "You are a fresh-eyes auditor. You have never seen this letter before … That isolation is the entire reason this agent exists." Description (:5) mandates spawning in an isolated window with no generation history.
- FACT — `skills/verification-loops/SKILL.md:72` "Spawn a single reviewer agent with fresh context. The reviewer has NO access to the implementation reasoning — only the output and the requirements … fresh eyes, no bias."
- FACT — Global `~/.claude/CLAUDE.md:281-290` "Drafting-agent self-critique is forbidden … Spawn a fresh sub-agent to read the artifact cold … never paste contents — pasting loads your anchoring into the sub-agent." Structured JSON return contract.
- JUDGMENT — The same principle (isolation defeats anchoring) is independently implemented at agent, skill, and system-prompt layers — a genuinely load-bearing institutional pattern, and the reason DCT002's "cold-context reviewer pass" caught the wrong-gender testimonial.
- PROTECT: keep cold-context review as a first-class pattern; the rebuild should standardize the JSON return envelope (artifact path in, structured findings out) so every gate can reuse it.

---

## Strengths the candidate list missed

### M1. "Code decides, model judges" separation (the deepest reusable idea) — CONFIRMED
- FACT — `run_pipeline.py:283` comment: "still JUDGES (probabilistic scoring), but CODE DECIDES (a fixed threshold)"; :760 `compute_gate_verdicts` derives the verdict "from the threshold — never trusting the model's own," failing closed on malformed scores. This is the architectural primitive under candidate 1, and it generalizes to every gate in the system.
- PROTECT: this is the most important pattern to carry forward — anywhere the rebuild has an LLM grading, the pass/fail must be computed in code from the numeric scores, never read from the model's self-declared verdict.

### M2. Honest self-declared blockers — CONFIRMED
- FACT — `skills/ad-concept-engine/SKILL.md:116` openly tracks open blockers (G1 emitter writes legacy shape, G3 allocate unbuilt, G4 sheet writer reads old format); `dct.json` launch_gates item 7 self-declares the render/sheet shape mismatch; pipeline-state notes record every manual bypass. The drift is documented by its owner, not silently rotting.
- JUDGMENT — The system tells the truth about its own gaps. That epistemic honesty (also: ad-concept-engine learnings.md opens "N=1 WARNING … priors, not laws") is rare and worth preserving as a cultural invariant.

### M3. Sheet-writer safety gates where they exist — CONFIRMED (PARTIAL system-wide)
- FACT — `scripts/tr_10_5_5_sheet_writer.py` defaults to dry-run and "aborts live write unless all 5 DCTs have 5/5 copy" (A2:§1.4); `meta-ads-uploader` has no budget control + resumable results sidecar. Where a writer exists for the current data shape, it is gated.
- CAVEAT — this writer is hardcoded to one client (neezanizam/thomson). For any other 10-5-5 wave there is currently NO gated writer; operators fall back to raw `gws` calls and lose the snapshot safety (C-trace §8). So the *pattern* is a strength; its *coverage* is the gap.

---

## How the rebuild must protect these (one-line each)
1. Hardened gate → make `--hardened` default + document it; promote citation audit from advisory to blocking.
2. Copy fidelity → add an approved-copy↔emitted-dct diff gate so automation can't corrupt signed-off text.
3. Avatar traceability → script-verify every VERBATIM tag resolves to a transcript line.
4. eval-buyer-fit → port the refuse-to-publish-without-PASS pattern into the statics lane.
5. Reviewer chain → keep as the template for every high-stakes gate (isolated reviewers + FAIL-stops-ship).
6. feedback-router → keep thresholds verbatim; repoint to `dct.json` + `meta` CLI + a live route.
7. PAUSED uploads → retain code-level forcing (not a config default).
8. Secrets → keep credentials gitignored; add pre-commit scan if CI lands.
9. Sidecars → keep every-output-writes-provenance; extend to copy + sheet stages.
10. Phase gating + ICM validator → make default not opt-out; revive corrections loop repo-wide.
11. Cold-context review → standardize the JSON return envelope so all gates reuse it.
12. (M1) "Code decides, model judges" → apply to every LLM-grading gate in the rebuild.
