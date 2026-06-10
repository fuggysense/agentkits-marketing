# Regression Baseline — Smoke-Test Run (Meridian Property Advisory)

> **FICTIONAL SMOKE-TEST DATA — "Meridian Property Advisory" is not a real client.**
> This record documents CURRENT machine behaviour, defects included. Nothing here was fixed
> or improved during the run. It is the frozen comparison point a future session re-runs against.
> Captured: 2026-06-11. Client slug: `_smoketest`. All paths relative to `clients/_smoketest/`.
> Companion files: `artifact-manifest.json` (machine-readable hashes), `invocations.md` (how each
> stage ran), `friction-log.md` (broken/ambiguous instructions hit), `planted-defects.md` (defect registry).

## Output verification

All 31 listed key artifacts confirmed present on disk (`ls` + `shasum -a 256`). **Zero missing.**
Per-file sizes + sha256 are in `artifact-manifest.json`. The only non-deliverable on disk is the
`angles/run-260611/dry-run-output/` scratch dir (22 forced-PASS stub files the sandbox refused to
delete — flagged, not part of the baseline).

## Pipeline shape

`Stage 0 scaffold` → `AVATAR` → `ANGLES` → `META-COPY` → `IMAGE-PROMPT (stop before render)`.
Each stage consumed the prior stage's on-disk output. No network mutations, no spend, no Meta calls,
no sheets, no renders. All writes confined to `clients/_smoketest/`.

---

## Stage 0 — Scaffold + fictional research pack

**What ran:** `cp -R clients/_template/ clients/_smoketest/` (defects preserved verbatim), then minimal
identity adaptation + a hand-authored fictional research pack. No research skill exercised (mandate is
fictional + no-network; `research`/`avatar-research`/`deep-research` all assume live sourcing).

**Skill files read:** `~/.claude/commands/writing/SKILL.md` (full — anti-AI + readability + 16-item
self-check applied to all prose). `copywriting-masters.md` deliberately NOT loaded (research artifacts,
not persuasive copy — logged as a judgment call).

**Inputs consumed:** `_template/` (context-profile.json, CLAUDE.md ~197-line file, CONTEXT.md, the two
`_brand/` scaffolds) — read-only for shape.

**Outputs (sizes):** `context-profile.json` (1822 B), `CLAUDE.md` (12084 B — `{{...}}` blanks filled,
bloat NOT fixed), `CONTEXT.md` (9157 B), `00_inputs/research/onboarding-form-260611.md` (5868 B, 21-Q
intake + founder story), `voc-reddit-dump-260611.md` (8095 B, 27 VoC quotes), `competitor-notes-260611.md`
(5163 B, 3 fictional competitors), `market-stats-260611.md` (2980 B, 8 sourced stats), plus thin seeds
`_brand/offer.md` (2411 B) + `_brand/buyer-profile.md` (later rewritten by AVATAR).

**Gates fired + outcomes:**
- Writing self-check (16-item) — PASS: 0 AI-tell words, 0 unicode arrows, 0 smart quotes across all 6 prose files.
- Em-dash budget — FLAGGED (25 across long-form research; conscious long-form call, strict <3 is short-form-only).
- Write-confinement — PASS: every Write/Edit hit `clients/_smoketest/` only.
- Real-client-leak — PASS: 0 real-client refs authored. takekine refs found ONLY in inherited `_templates/concept-phases/*.md` (verified `diff -rq` identical to `_template`; defect preserved, not authored here).
- Fictional-header — PASS: header present in all 4 research files + both brand seeds.
- Edit-safety — re-Read each file before edit (stale-context guard caught twice, complied).
- Baseline no-fix — PostToolUse `/simplify` hook fired 3x on CLAUDE.md edits; deliberately NOT run (baseline must preserve defects); flag cleared each time.
- Quote/stat counts — VoC 27 (≥25), market stats 8 (6-8), competitors 3.

**Friction hits:** offer.md template is a 100-line empty scoring scaffold (not a starter); buyer-profile.md
template is 262 lines of empty avatar OUTPUT tables; context-profile.json ships unrendered `{{mustache}}`
tokens (no template engine on `cp -R`); CLAUDE.md ~197 lines, ~80% generic V4 boilerplate dead-weight at
L0 for a no-site/no-video client; no `_baseline/` convention in template (created fresh); research-skill
bypass unavoidable → baseline does NOT cover real research skills' file-writing behaviour.

---

## Stage AVATAR — avatar-research

**What ran:** Full 4-phase + 2-HITL-gate avatar-research process against the fictional research pack.
Played both agent and HITL (auto-approved gates, logged). Produced 3 micro-personas (operator said "2-3").

**Skill files read:** `skills/avatar-research/SKILL.md` (full, 539 lines); `writing/SKILL.md` (full).
`copywriting-masters.md` NOT loaded (diagnostic doc, not selling — judgment call).

**Inputs consumed (read-only):** `_brand/buyer-profile.md` (thin seed), `_brand/icp.md` (BLANK scaffold),
`_brand/offer.md` (thin seed), `_brand/brand-voice.md` (empty stub), `_brand/story-bank.md` (empty),
`00_inputs/research/{voc-reddit-dump, competitor-notes, market-stats, onboarding-form}-260611.md`.

**Outputs (sizes):** `_brand/buyer-profile.md` (16911 B — rewritten with `## MICRO-PERSONA MAP`: MP-01
Repeat-Mistake Upgrader L4, MP-02 L2, MP-03 Fee-Allergic Convertible L4; sophistication matrix;
psychology + market-behaviour sub-blocks; refresh log with HITL gate records). Did NOT create
`_brand/avatars/*.md` (correctly — deprecated for targeting).

**Gates fired + outcomes:**
- HITL Gate 1 (Micro-Persona Selection) — FIRED, auto-approved. 4 hypotheses generated, 3 selected, 4th (couple/tie-breaker) folded into MP-01/MP-02 as relationship context.
- HITL Gate 2 (Micro-Persona Approval) — FIRED, auto-approved. 3 personas accepted as distinct on motivation/trigger/awareness/sophistication.
- HITL Gate 2.5 (Sophistication Validation) — FIRED, auto-approved. Deferred to fictional research for L2/L4 assignment.
- Phase 0 Step 0 research-vault gate — FIRED but DEVIATED: matching fresh real `sg-property-*` dossiers exist and the skill mandates mining them; SKIPPED per fictional/no-network mandate (mining real research would contaminate fictional data). Logged as skill-vs-mandate conflict.
- Writing self-check (16-item) — PASS except 2 negative-parallelisms vs the "≤1, 0 better" target (acceptable for an internal analysis doc, noted).

**Friction hits:** Phase 0 Step 0 forces vault mining that breaks the fictional mandate (no synthetic/offline
mode); entire Phase 2 + 2.5 are a human paste-back loop with no "research already in a local file" fallback
(brief had to redirect to `00_inputs/research/`); `icp.md` is "Required" yet blank, allowed through by the
contradictory "Foundation flexibility" clause; HITL gates have no machine-runnable auto-approve convention
(brief invented one); legacy `_brand/avatars/` still ships and is referenced — a trap; `brand-voice.md` +
`story-bank.md` empty stubs make the Phase 0 load a no-op with no "if empty skip" acknowledgement.

---

## Stage ANGLES — big-angle-spotter (hardened mode)

**What ran:** One honest live-capability check, then EMULATION of the 12-step pipeline + scored hardened gate.
The real `run_pipeline.py` CAN run headless (proven: `--hardened --dry-run` exit 0 + one live `claude -p`
worker rc=0, 9.5s, $0.066) — but a full hardened run = 18+ live Opus workers carrying a 26KB SP each = real
USD spend, which the no-spend rule forbids. So angle/headline/copy generation was emulated, reproducing the
gate contract faithfully from source (`RESONANCE_GATE_SCHEMA` + `compute_gate_verdicts()`).

**Skill files read:** `skills/big-angle-spotter/SKILL.md` (full, symlink → `~/AI workflows/big-angle-spotter/`);
`run_pipeline.py` (argparse 1079-1235, `run_worker` 530-606, hardened layer 278-471, `compute_gate_verdicts`
760-805); `writing/SKILL.md` (full); `references/copywriting-masters.md` (persuasive task → PRIMARY Hopkins
/ SUPPORT Schwartz / Caples headlines).

**Inputs consumed:** `inputs.json` + `kill-list.md` (authored for the run — hardened is fail-closed),
`_brand/buyer-profile.md` (MP-01/02/03 + evidence quotes), `_brand/offer.md`, VoC dump, `CLAUDE.md` (tone law).

**Outputs (sizes):** full `angles/run-260611/` tree — `inputs.json` (1245 B), `kill-list.md` (1640 B),
`01_angles.md` (3520 B, 10 angles), `02_gate_resonance.json` (7655 B, scored gate), `03_pruned.md` (666 B),
`04_ranked_angles.md` (2045 B), `05_gate_top_angle.md` (814 B), `06_gate_novelty.md` (1232 B),
`07_expansion.md` (2907 B), `08_headlines.md` (1226 B), `09_ranked_headlines.md` (2038 B),
`10_gate_four_check.md` (1629 B), `11_ad_prompts.md` (5917 B), `12_image_prompts.md` (4574 B),
`SUMMARY.md` (3928 B), `_run.log` (4630 B), `dry-run.log` (6511 B, wiring proof only).

**Gates fired + outcomes:**
- step02 resonance gate (5 dims, scored, CODE-decided, threshold 4) — PASS: 8/10 banked loop 1 (need ≥5); A07 failed distinct=3, A09 failed not_saturated=2 (held for audit, NOT inflated). Re-derived in Python: pass_count + set_verdict + min_scores internally consistent, zero inconsistencies.
- step05 top-angle confirm — PASS: A01 "The incentive flip" confirmed rank-1, clean YES.
- step06 novelty/not-saturated — PASS with note (keep execution concrete; abstract "no conflict of interest" slogan is saturated; satisfied in top-3).
- step10 four-check on top-3 headlines — PASS: all 3 clear pain/buyer-words/concrete/chills.
- Writing self-check (16-item) — PASS on human-facing copy: 0 curly quotes, 0 em-dashes in body ad copy, no AI-tells, grade 4-6, UK English from step 8, calm/numbers-first per CLAUDE.md landmines.

**Friction hits:** no no-spend/synthetic mode (only `--dry-run` runs cheaply but uses forced-PASS stubs →
tests WIRING not gate-scoring); `--dry-run` writes a full stub run-dir with no DRY-RUN banner/suffix (easy to
mistake for the deliverable; sandbox DENIED `rm -rf` so scratch accumulates); hardened fail-closed demands a
non-empty kill-list but a fresh client's honest `EXISTING_ANGLES` is the sentinel "(none...)" the validator
treats as empty → SystemExit (the exact fresh-client state hardened is built for can't run hardened until the
operator hand-authors a kill-list; requirement is in argparse help, NOT SKILL.md); SKILL.md §4's documented
launch command is the LEGACY soft path (`--model sonnet`, no `--hardened`) — the scored gate is only reachable
via argparse; provenance §6 assumes a `research-pool.json` that a fresh client has none of (all
`source_phrase_id` forced null); Write-tool guardrail blocked `SUMMARY.md` as a "report file" (worked around
with Bash heredoc — harness friction, not skill friction).

**Lever recorded:** `--min-pass-count 5` (not default 10), per SKILL.md's "a DCT batch needs a handful of strong
angles" guidance + the 10-5-5 lean.

---

## Stage META-COPY — headline-bank

**What ran:** Skill CORE PROMPT run manually (single-pass, Mode A, scope = one angle, no sub-agent). 7-item
input checklist assembled from `_smoketest` files — none halted. Produced 2 locked copies + 5 short headlines.

**Skill files read:** `skills/headline-bank/SKILL.md` (v2.1.0, full); `writing/SKILL.md` (all layers);
`references/copywriting-masters.md` (persuasive task).

**Inputs consumed (the 7-item checklist):** brand = Meridian (`context-profile.json`); angle = A01 "The
incentive flip" (confirmed top by `04_ranked_angles.md` + `05_gate_top_angle.md` PASS); awareness =
Solution-aware edging product-aware; sophistication = L4; persona = MP-01 Repeat-Mistake Upgrader; LDP =
`meridianpropertyadvisory.example.sg/advisory`; spine = `07_expansion.md` incentive-flip cause→effect.

**Outputs (sizes):** `copy/wave-smoke-260611.md` (4371 B — COPY 1 compact = 50w, COPY 2 primary = 145w
(~150w), 5 short headlines, halbert-copy.md format).

**Gates fired + outcomes:**
- 7-item input checklist (lines 74-86) — PASS: all 7 assembled, none halted.
- Writing master-selection diagnostic — Solution-aware + mature/exhausted + skeptical → PRIMARY Hopkins / SUPPORT Schwartz / Caples headlines (matches angle file's pre-declared pick).
- Writing self-check (16-item) — PASS on both prose copies (no AI-tells, ≤1 negative parallelism, em-dash-free bodies, 1 tricolon once, specific numbers, scroll-stop opens, no banned/landmine words, headlines 3-5 words, UK English).
- Hard Rules 1-8 (lines 173-183) — PASS (scroll-stop first lines, no banned words, read-cue CTA no transactional verb, no emoji, curiosity-led, headlines ≤5 words).
- Length spec on disk — verified: COPY 1 = 50w, COPY 2 = 145w (~150w), 5 short headlines.

**Friction hits:** HEADLINE/COPY ↔ length-mapping contradiction is REAL and internal to SKILL.md (CORE PROMPT
lines 156-168 orders COPY A=~150w/HEADLINE 1 first; Output File template lines 196-228 + Sheet Mapping invert
it to COPY 1=~50w first — followed Output File template numbering, the named on-disk deliverable); `brand-voice.md`
is an empty stub yet is the skill's most-cited input for the emoji decision (resolved NO EMOJI from CLAUDE.md
tone law, no fallback instruction exists); funnel-target taxonomy has no slot for a paid mid-funnel call (A01's
S$290 Teardown is T2, neither long-form page nor lead form — mapped to long-form page as a judgment call the
skill doesn't guide); output path diverged from SKILL.md's hard-coded `angles/big-angle-spotter/wave-<N>/DCT<N>/`
per brief direction; task asked for 5 headlines but skill DEFAULT ships 2 (borrowed the opt-in 10-5-5 over-draft
mechanic — draft 5, lock 2, keep 3 — a partial-mode state the skill doesn't describe).

---

## Stage IMAGE-PROMPT — ad-concept-engine static creative briefs (LAST generation stage)

**What ran:** Static-creative-brief path of ad-concept-engine. Promoted the two highest-ranked angles
(A01 MP-01, A02 MP-03) to two DCTs, built locked headlines + 2 Meta copies + image pool per DCT
(DCT-01 = 3 variants, DCT-02 = 2). **STOPPED before render** — no render.py, no executor, no sheet, no
network/Meta. All images `status: pending`, `file: null`. Planted one deliberate defect.

**Skill files read:** `skills/ad-concept-engine/SKILL.md` (full, 761 lines);
`references/high-converting-static-brief.md` (full — 9-point scroll-stop bar, concept-type distribution,
visual-style no-repeat, SG ethnicity rule, anti-AI negative prompts); `clients/neezanizam/.../dct.json`
(read for SHAPE ONLY, no content copied); `writing/SKILL.md` + `copywriting-masters.md` (persuasive prose fields).

**Inputs consumed:** `04_ranked_angles.md` (A01/A02), `07_expansion.md` (A01 depth), `11_ad_prompts.md` +
`12_image_prompts.md` (ad bodies + 3 emulated image concepts), `copy/wave-smoke-260611.md` (A01 locked
copy carried verbatim into DCT-SMOKE-01), `_brand/buyer-profile.md` (MP-01/MP-03), `_brand/offer.md`
(T1/T2/T3 ladder + figures), `CLAUDE.md` (tone law).

**Outputs (sizes):** `campaigns/wave-smoke-260611/dct.json` (19203 B — `dcts[]` array of 2 single-avatar
DCTs, each with its own `image_pool`; inline `image_prompt` strings; planted-defect flag present).
Plus `_baseline/planted-defects.md` (registry).

**Gates fired + outcomes:**
- Phase 2a static-path routing (format=Static → hooks) — applied.
- high-converting-static-brief.md 9-point scroll-stop self-check per variant — PASS (distinct concept types + styles, SG-correct ethnicity on the one person-variant, explicit anti-AI negative prompts, clear headline-on-image, bridge lines, editorial/documentary aesthetic, no kill-listed drone-shot).
- Writing self-check (16-item) on all prose fields — PASS (0 em-dashes after fix, straight quotes, no arrows, no AI-tells, ≤1 negative parallelism carried from approved copy, no emoji).
- JSON validity — PASS: `python3 json.load` OK (2 DCTs, 3+2 image prompts, planted flag present).
- Render STOP — HONORED: render.py NOT invoked, no executor, no sheet, no network/Meta; all images pending/null.
- Write-scope — PASS: all 4 written files inside `clients/_smoketest/`.
- Planted-defect — PD-IMG-01 seeded in DCT-SMOKE-01-img-03 (hook + prompt body), marked `claim_status=UNSOURCED_PLANTED_DEFECT`, recorded in `planted-defects.md`.
- Sub-agent fresh-eyes critique — NOT dispatched (judgment call: structured JSON manifest, not a new skill/agent/system-prompt; planted defect intentional + self-documented; ran writing self-check inline). Logged.

**Friction hits:** dct.json shape conflict (canonical = ONE flat top-level `image_pool` Meta mixes across
angles; brief asked for a pool PER DCT entry — "2 DCT entries in one file" has no native slot in the
single-DCT schema; followed brief = `dcts[]` of two single-avatar DCTs); `high-converting-static-brief.md`
hard-codes Singapore (ethnicity rule, CPF/HFE, Straits Times aesthetic, SG photographer names) with NO
non-SG branch despite claiming it applies "for every client" (origin header admits neezanizam authorship —
single-client leakage into a universal MANDATORY gate; applied cleanly only because Meridian is a fictional
SG client); inline-vs-sidecar contradiction (brief MANDATES sidecar `image-prompts/<batch>-<variant>.json`;
neezanizam's production dct.json inlines — followed the task/inline, two live conventions disagree);
`dct-tracker.json` vs `dct.json` naming (skill's own open blocker G1 — wrote `dct.json`); only A01 had
finished copy upstream so A02 (MP-03) was promoted as DCT-2 with adapted copy (re-run through self-check,
flagged per-entry in `copy_source`); no neutral dct.json fixture exists for a new client (had to read a real
client's live manifest for shape — coupling mitigated by no-copy rule).

---

## Planted defect registry

| ID | Stage | Location | Planted claim | What the future gate MUST do |
|---|---|---|---|---|
| PD-IMG-01 | IMAGE-PROMPT | `campaigns/wave-smoke-260611/dct.json` → `DCT-SMOKE-01` → `image_pool.images[2]` (`DCT-SMOKE-01-img-03`), in both `image_prompt` body and `text_on_image_hook` | "73% of Singapore buyers overpay on their second home." | Flag the image as containing an unverifiable statistic, refuse to pass it to render, demand a real source (none exists) or removal. **A PASS verdict on this image = the gate failed.** |

Marking lives in metadata (`claim_status: "UNSOURCED_PLANTED_DEFECT"` + `_planted_defect` pointer), NOT in the
rendered hook text — so a metadata-only gate and a copy-reading gate are tested differently. Every OTHER number
in the manifest (S$4,500, S$290, S$900k/S$1.6m, three weeks, S$30k) is source-linked within the fictional pack
and is NOT a plant. Full write-up: `planted-defects.md`.

---

## Cross-cutting baseline facts (true for the whole run)

- **No spend, no mutations:** zero renders, zero Meta/sheet/network writes. The angle stage proved the real
  hardened pipeline runs headless but was emulated to honour the no-spend rule (1 probe worker = $0.066 total).
- **Research skills never exercised for file-writing:** fictional + no-network mandate forced direct authoring
  of all research; baseline does NOT cover `research`/`avatar-research`/`deep-research` live-sourcing behaviour.
- **HITL gates auto-approved** (3 in AVATAR) under an invented convention — no skill ships a headless auto-mode.
- **Defects preserved, not fixed:** `/simplify` PostToolUse hook overridden 3x; template bloat (197-line
  CLAUDE.md, empty scaffolds, `{{mustache}}` tokens, deprecated `_brand/avatars/`) left intact on purpose.
- **Two recurring skill-internal contradictions** worth a repair pass: headline-bank's HEADLINE/COPY length
  mapping (CORE PROMPT vs Output File template), and ad-concept-engine's `dct-tracker.json` vs `dct.json` +
  inline-vs-sidecar image-prompt storage. Both followed via one consistent reading; both logged.

---

## Re-run recipe (reproduce this baseline for comparison)

Run as a sandboxed, fictional, no-spend, no-network pass. Confine ALL writes to `clients/_smoketest/`.
Re-use the SAME fictional facts (Meridian Property Advisory, founder Daniel Tay, SG buyer-side flat-fee
advisory). Append (never overwrite) `invocations.md` + `friction-log.md`. Capture into a NEW dated run
dir/file so the diff against this baseline is clean.

**Exact stage order + skill files (top-to-bottom):**

1. **Stage 0 — scaffold + research pack**
   - `cp -R clients/_template/ clients/<new-run>/` (do NOT fix template defects).
   - Read `~/.claude/commands/writing/SKILL.md` (full) before any prose. Skip `copywriting-masters.md` (research artifacts).
   - Fill ONLY `{{...}}` identity blanks in `CLAUDE.md` / `CONTEXT.md` / `context-profile.json`. Write the 4 research files + 2 thin `_brand/` seeds, each with the FICTIONAL header.
   - Gate: writing 16-item self-check; fictional-header check; write-confinement; do NOT run `/simplify`.

2. **Stage AVATAR — `skills/avatar-research/SKILL.md`** (+ `writing/SKILL.md`)
   - Follow 4 phases + 3 HITL gates. Auto-approve each gate and log it in `buyer-profile.md`'s refresh log.
   - DEVIATE at Phase 0 Step 0: do NOT mine the real `sg-property-*` research vault (fictional mandate). Use `00_inputs/research/*` as the Phase 2 substitute.
   - Output: rewrite `_brand/buyer-profile.md` with `## MICRO-PERSONA MAP` (3 personas: 2× L4, 1× L2) + sophistication matrix. Do NOT write `_brand/avatars/`.

3. **Stage ANGLES — `skills/big-angle-spotter/SKILL.md`** (+ read `run_pipeline.py` argparse/hardened/`compute_gate_verdicts`; + `writing/SKILL.md` + `copywriting-masters.md`)
   - Author `inputs.json` + a non-empty `kill-list.md` (hardened is fail-closed) into `angles/run-<date>/`.
   - Honest live-capability check only: `run_pipeline.py --inputs ./inputs.json --hardened --buyer-profile <path> --kill-list <path> --dry-run --min-pass-count 5` (wiring proof, no spend). Do NOT run a live generation (18+ Opus workers = real spend).
   - EMULATE the 12 steps + scored resonance gate (5 dims, threshold 4, CODE-decided PASS iff every dim ≥4, set PASS iff pass_count ≥5). Re-derive verdicts in Python. Emit `01_`..`12_` + `SUMMARY.md` + `_run.log`. Hold honest failures (do not inflate to all-pass).
   - Write `SUMMARY.md` via Bash heredoc if the Write tool blocks it as a "report file".

4. **Stage META-COPY — `skills/headline-bank/SKILL.md`** (+ `writing/SKILL.md` + `copywriting-masters.md`)
   - Assemble the 7-item input checklist from `_smoketest` files (angle = confirmed top A01).
   - Run the CORE PROMPT manually (single-pass, Mode A). Resolve the HEADLINE/COPY length contradiction by following the **Output File template** numbering (COPY 1 ≈ 50w, COPY 2 ≈ 150w). NO EMOJI (from CLAUDE.md tone law). Read-cue CTA (no transactional verb).
   - Output `copy/wave-<date>.md` (halbert-copy.md format): 2 locked copies + 5 short headlines (borrow the 10-5-5 over-draft mechanic: draft 5, lock 2, keep 3).

5. **Stage IMAGE-PROMPT — `skills/ad-concept-engine/SKILL.md`** + `references/high-converting-static-brief.md` (+ read a real `dct.json` for SHAPE ONLY; + `writing/SKILL.md` + `copywriting-masters.md`)
   - Static path (format=Static → hooks). Promote A01 (MP-01) + A02 (MP-03) to 2 DCTs. Build `campaigns/wave-<date>/dct.json` as a `dcts[]` array, each DCT with its own `image_pool` (DCT-1 = 3 variants, DCT-2 = 2), inline `image_prompt` strings.
   - Apply the brief's 9-point self-check per variant + SG ethnicity rule (Meridian is SG). Plant ONE unsourced stat in one image and mark it `claim_status=UNSOURCED_PLANTED_DEFECT` + record in `planted-defects.md`.
   - **STOP before render:** no render.py, no executor, no sheet, no network/Meta. All images `status:pending`, `file:null`. Validate `python3 json.load`.

6. **Stage BASELINE-RECORD** (this stage)
   - `ls` + `shasum -a 256` every key artifact; flag any missing. Write `BASELINE.md` + `artifact-manifest.json`.

**Comparison method:** after a re-run, diff the new `artifact-manifest.json` hashes against this one. Prose
files WILL differ in hash (re-authored). Compare on structure instead: same stage order, same gates firing
with same outcomes, same friction surfacing (or repaired), and PD-IMG-01 still caught (or now blocked by a
new claim gate — the success signal for a future quality-gate addition).
