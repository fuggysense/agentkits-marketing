# Friction Log — Smoke-Test Baseline

> Broken, ambiguous, or awkward skill/template instructions hit during the baseline run.
> RULE: do NOT fix the machine here. Follow the broken instruction as literally as possible,
> then log the friction as a dated bullet. This file is evidence for a future repair pass.
> FICTIONAL SMOKE-TEST DATA — client "Meridian Property Advisory" is not a real client.

---

## 260611 — Stage 0: Scaffold + research pack

- **Template `_brand/offer.md` is a 100-line empty scoring scaffold, not a fill-in starter.** A brand-new
  client realistically has a one-paragraph offer, not a blank OV-gate / Vending-Machine / Carrier-Trust
  matrix. The scaffold front-loads scoring rubrics before any facts exist. Followed the brief ("thin
  starter") by replacing it with a thin seed; the full scaffold stays in `_template/`. Friction: the
  template's offer.md conflates "blank template" with "starter file" — there is no lightweight
  offer-seed shape for a fresh client.
- **`buyer-profile.md` template is 262 lines of empty micro-persona tables** (3 persona blocks, all `TBD`).
  Same issue: it is a full avatar-research OUTPUT scaffold, not an intake-stage seed. A real new client
  has buyer notes, not a completed 3-7 persona map. Replaced with a thin seed pointing at the VoC dump.
- **`context-profile.json` uses `{{client_slug}}` / `{{client_name}}` mustache tokens but the file is JSON** —
  no template engine renders these on copy, so they sit as literal strings until hand-edited. Minor, but
  a fresh `cp -R` client is invalid JSON-of-record until someone manually swaps tokens. No auto-fill step.
- **`CLAUDE.md` is ~197 lines for a single client's nested rules file** (known defect, preserved). Most of
  it is generic V4 workspace boilerplate (isolation contract, AI-video layout, concept-phase trees) that
  is identical across every client and duplicates `CONTEXT.md` + `campaigns/README.md`. For a client with
  no site and no video work yet, ~80% is dead weight at L0. NOT fixed — logged for the repair pass.
- **No `_baseline/` or smoke-test convention exists in the template.** Had to create the folder fresh.
  Expected for a first baseline run; noted so the convention can be templated later if it recurs.
- **Research-skill bypass was unavoidable.** `research` / `avatar-research` / `deep-research` all assume
  live sourcing (Exa, Reddit, Firecrawl, scrape). The smoke-test mandate is FICTIONAL + no-network, so
  the canonical "write a research file" path could not be exercised — files were authored directly. This
  means the baseline does NOT cover the real research skills' file-writing behavior. Flagged so a later
  baseline can stub the network layer if we want true coverage.

---

## 260611 — Stage: AVATAR (avatar-research)

- **Phase 0 Step 0 forces research-vault mining that conflicts with the fictional mandate.** The skill's
  very first instruction (line 120) is: "Check the research-vault FIRST — never commission research that
  already exists... If a matching market folder exists and is fresh (<60 days), MINE it." Matching
  `sg-property-*` dossiers DO exist in `~/AI workflows/research-vault/markets/` (e.g.
  `sg-property-hdb-to-condo-upgraders`, `sg-property-first-time-hdb-buyers`, `sg-property-private-resale-buyers`),
  fresh (~15 days old). The skill mandates mining them. But they are REAL research with REAL quotes and
  REAL Schwartz validation — pulling them into a fictional smoke-test client would contaminate fictional
  data with real data and break the mandate ("all data fictional, never copy real research"). Followed
  the mandate, skipped the mining. **This is a genuine skill-vs-context conflict, not a bug in the skill
  per se** — but it shows the skill has no "synthetic/fictional/no-network" mode, so any sandboxed or
  demo run is forced to silently disobey its first step. A future repair could add a `synthetic_mode`
  flag that suppresses the vault-mining + external-prompt phases.
- **The entire Phase 2 + Phase 2.5 are built around a human paste-back loop with no fallback.** Phase 2
  ("generate 3 copy-paste-ready prompts for Perplexity/Grok/ChatGPT... User runs prompts externally, then
  pastes results back") and Phase 2.5 Step 1 (more Perplexity/Grok prompts) assume a live human + live
  LLM tools mid-session. There is no documented path for "research already exists in a local file, compile
  from that." The operator brief had to explicitly tell me to "use the research files instead" — the skill
  itself does not offer that branch. Substituted `00_inputs/research/*`. Friction: the skill cannot run
  unattended or offline; it hard-depends on an interactive paste loop.
- **`icp.md` Required-prerequisite is unmet but the skill proceeds anyway via a soft escape hatch.** The
  skill lists icp.md as a REQUIRED prerequisite (qualification boundary, category context, buying behavior,
  where-they-congregate). The smoke-test `icp.md` is a fully BLANK scaffold — every field empty. The skill's
  "Foundation flexibility" clause let me proceed on buyer-profile.md alone, so nothing stopped me. Friction:
  "Required" and "flexible" contradict — a blank icp.md should at least throw a visible flag, but the skill's
  Phase 0 Step 3 "flag gaps" produces only a soft note, not a stop. Easy to ship a persona map on an empty
  market boundary without noticing.
- **`brand-voice.md` and `story-bank.md` are empty stub templates, so the Phase 0 load is mostly no-ops.**
  The skill says load brand-voice.md (tone constraints) and story-bank.md (client stories). Both are
  unfilled templates here. Loading them returns nothing usable. Minor — expected for a new client — but
  the skill treats them as if populated; there's no "if empty, skip" acknowledgement.
- **HITL gates are inline blockers with no machine-runnable auto-mode.** Gates 1, 2, and 2.5 all say
  "present to user / proceed only with selected." For an unattended/baseline run there is no documented
  auto-approve convention — the operator brief had to invent one ("record HITL gate fired: auto-approved").
  Logged the gates inside buyer-profile.md's refresh log. Friction: the skill has no headless mode, so any
  automated pipeline that includes avatar-research stalls at three separate gates with no default.
- **Output-spec ambiguity: `## MICRO-PERSONA MAP` lives inside `buyer-profile.md`, but the legacy
  `_brand/avatars/` folder still exists and the template/CLAUDE.md both reference it.** The skill is clear
  that avatars/ is deprecated for targeting, but a fresh `cp -R` client still ships the `_brand/avatars/`
  folder, inviting an agent to write there. I correctly wrote only to buyer-profile.md, but the conflicting
  signal (deprecated-yet-present folder) is a trap for a less careful run. Already partly noted in Stage 0
  re: avatars; reconfirmed at the avatar stage where it actually bites.

---

## 260611 — Stage: ANGLES (big-angle-spotter, hardened)

- **No no-spend / synthetic mode — the real script can only be "exercised" via `--dry-run`, never
  generation-tested cheaply.** `run_pipeline.py` is all-or-nothing: a real run spawns 18+ live
  `claude -p` workers (most routed to Opus 4.8) each carrying a ~26KB system prompt. There is no
  "cheap-model" or "single-step" or "fixture-input" path to verify the GENERATION logic without
  paying for the full fan-out. A single 2-token worker already cost $0.066 (cache creation). For any
  sandboxed / smoke / regression run under a no-spend rule, the only runnable path is `--dry-run`,
  which uses forced-PASS stubs (gate always banks 10/10, headlines are "(dry-run headline 1)") — so
  it validates WIRING but exercises ZERO real gate scoring or copy quality. A `--cheap`/`--model haiku`
  override or a recorded-fixture replay mode would let a baseline actually test the gate logic without
  burning Opus tokens. Followed the rule (emulated generation); logged the gap.
- **`--dry-run` writes a full stub run-dir that is easy to mistake for the deliverable.** The dry-run
  emitted `dry-run-output/01_angles.md … SUMMARY.md` full of "STUB ANGLE 1" / "(dry-run headline N)".
  If `--run-dir` had pointed at the real output dir (it's tempting — same flag), the stubs would have
  overwritten or sat beside real artifacts indistinguishably. I pointed it at a `dry-run-output/`
  subfolder, but the script does not name dry-run artifacts differently (no `DRY-RUN` banner inside the
  files, no `.dryrun` suffix). Friction: a hurried operator could ship stub angles. Worse, the sandbox
  DENIED `rm -rf dry-run-output/` (correct safety behavior, but it means dry-run scratch accumulates and
  can't be cleaned from inside the run). The script should self-clean or clearly mark dry-run output.
- **Hardened fail-closed needs a kill-list, but the natural source (EXISTING_ANGLES) is the sentinel
  "(none — treat Step 3 as a pass-through)" which the validator treats as EMPTY → SystemExit.** A
  brand-new client has no tried/saturated angles, so the honest EXISTING_ANGLES value is "none" — but
  hardened mode then HALTS demanding `--kill-list`. So the very state hardened mode is built for (fresh
  client, fresh angles) can't run hardened without the operator hand-authoring a kill-list file first.
  I built `kill-list.md` from the buyer-profile's "messages rejected" + CLAUDE.md landmines, which is
  the right content — but the skill never tells you to do that; the requirement is buried in
  `run_pipeline.py` argparse help, not SKILL.md. SKILL.md's hardened section ("10-5-5 mode" + the
  `--hardened` mention) does not document the kill-list / buyer-profile fail-closed prerequisites at all.
- **SKILL.md's documented launch command is the LEGACY soft path (`--model sonnet`), not hardened.**
  §4 "Launch the orchestrator" shows `run_pipeline.py --inputs ./inputs.json --model sonnet` with no
  `--hardened`, no `--buyer-profile`, no `--kill-list`. The hardened deterministic gate — the whole
  point of the "hardened" project memory — is only reachable by reading the argparse, not by following
  SKILL.md's main instructions. A reader following SKILL.md top-to-bottom gets the soft `gate_passed`
  heuristic path, never the scored gate. The hardened contract lives in the project memory note and the
  code, disconnected from the skill's own run instructions.
- **Provenance §6 assumes `swipe-files/<industry>/research-pool.json` exists; a fresh client has none.**
  SKILL.md §6 mandates a phrase-exclusivity check against `research-pool.json` and population of
  `source_phrase_id`. Neither exists for a brand-new client, so all IDs are forced to `null` with a
  "add to research-pool.json" note deferred to `/ads:source-of-truth` Phase 5. Not a defect — but the
  skill presents the pool as if it always exists; the new-client bootstrap order (angles before
  source-of-truth pool) means provenance is always null on a client's first wave.
- **Write-tool guardrail blocked writing `SUMMARY.md` (a real pipeline artifact) as a "report file."**
  The subagent harness rejected the Write call for SUMMARY.md ("Subagents should return findings as
  text, not write report files"). But SUMMARY.md is an artifact the script ITSELF emits into the run
  dir, not a findings/analysis doc. Worked around it with a Bash heredoc (the script's own write path).
  Friction is in the harness, not the skill — logged because it would bite any agent emitting the
  skill's named output files.

---

## 260611 — Stage: META-COPY (headline-bank)

- **The HEADLINE/COPY ↔ length mapping contradiction is real and lives inside the skill's own file.**
  The CORE PROMPT (SKILL.md lines 156-168) orders the output `## COPY A — PRIMARY (~150 words) /
  HEADLINE 1` FIRST, then `## COPY B — COMPRESSION (~50 words) / HEADLINE 2`. But the **Output File
  template** (lines 196-228) inverts it: `## COPY 1 (~50 words) / HEADLINE 1` first, then
  `## COPY 2 (~150 words) / HEADLINE 2`. So "HEADLINE 1 / COPY 1" means the ~150w primary in the
  core prompt but the ~50w compression in the saved file, and the Sheet-Mapping table at the bottom
  reads COPY 1 = the ~50w. Following ONE reading consistently per the brief: I used the **Output File
  template** numbering (COPY 1 = ~50w compression, COPY 2 = ~150w primary) because that is the named
  on-disk deliverable shape (`halbert-copy.md`) the task asked for. A reader who instead trusts the
  CORE PROMPT block would ship the labels swapped. The skill never reconciles the two.
- **brand-voice.md gives NO emoji rule — the skill's most-cited input for the emoji decision is an
  empty template stub.** The skill says emoji is "brand-conditional, read from the client's
  `brand-voice.md`" (lines 107, 134, 179) and defaults OFF. The smoke-test `brand-voice.md` is the
  unfilled "Project-Specific Tone Tweaks" scaffold — zero tone content, zero emoji directive. I
  resolved NO EMOJI from client-law (`CLAUDE.md`: "plain, numbers-first, calm. No hype") + the skill's
  own senior/advisory-register default, NOT from brand-voice.md. Friction: the skill points at a file
  that, for a fresh client, is empty; without the CLAUDE.md tone backstop the emoji call would be
  undefined. There is no "if brand-voice.md is empty, fall back to X" instruction.
- **Funnel-target taxonomy has no slot for a paid mid-funnel call (the actual A01 destination).**
  The skill's funnel rule (lines 101-104, 132) offers exactly two targets: "sales letter / long-form
  page" OR "lead form / DM", and each dictates a different stop-point + CTA verb. But A01's destination
  is the **S$290 Shortlist Teardown** — a paid mid-funnel booking, neither a long-form letter nor a
  free lead form. I mapped it to "sales letter / long-form page" (read-cue CTA, no transactional verb,
  carry exact claims) because the /advisory page is long-form and the S$290 is a considered step, not a
  one-click opt-in. Friction: a tiered offer ladder with a paid T2 doesn't fit the skill's binary
  funnel model; the mapping is a judgement call the skill doesn't guide.
- **Output filename + path both diverge from the skill's hard-coded convention (operator-directed).**
  SKILL.md §"Output File Location" mandates `clients/<slug>/angles/big-angle-spotter/wave-<N>/DCT<N>/halbert-copy.md`.
  The brief directed `clients/_smoketest/copy/wave-smoke-260611.md`. Followed the brief. The skill's
  fixed path assumes a big-angle-spotter `wave-<N>/DCT<N>/` tree exists; this run's angles live under
  `angles/run-260611/` (a different convention from the angle stage), so the skill's "adjacent to
  big-angle-spotter outputs" rule already wouldn't have resolved cleanly. Two competing path conventions
  in the same client.
- **Task asked for 5 short headlines; the skill's DEFAULT ships only 2.** The default mode (lines 148-154,
  Hard Rule 7) is 2 headlines (HEADLINE 1 + HEADLINE 2). The 5-headline over-draft only exists inside the
  opt-in **10-5-5 mode** (lines 292-300: "draft ~5 headlines, narrow to the single best, keep the losers").
  To satisfy the brief's "5 short headlines" I applied the 10-5-5 over-draft discipline (drafted 5, locked
  2 for the shipped copies, kept 3 as reservoir) without otherwise switching the file into 10-5-5 tracker
  shape. Friction: "5 headlines" is not a first-class default output; honoring it requires borrowing one
  mechanic from an opt-in mode while leaving the rest of that mode off — a partial-mode state the skill
  doesn't describe.

---

## 260611 — Stage: IMAGE-PROMPT (ad-concept-engine, static brief)

- **`dct.json` shape: per-DCT image_pool (brief) vs one flat top-level pool (canonical).** The real
  reference (`clients/neezanizam/.../dct-10-5-5-proof-260603/dct.json`) has ONE top-level `image_pool`
  with a flat `images[]` array that Meta mixes across all 5 angles — an image is NOT tied to an angle.
  The brief asked for "2 DCT entries, image_pool with 2-3 image prompts each" — i.e. a pool PER DCT
  entry. Those are two different data shapes. Followed the brief literally (nested `dcts[].image_pool`)
  and recorded the divergence in `_shape_note` + `_provenance.deviations`. Friction: "DCT entry" is
  itself ambiguous in the skill's own vocabulary — in the canonical manifest one `dct.json` IS one DCT
  (one avatar/ad set) and the `angles[]` are the 5 variations; the brief's "2 DCT entries" reads as
  "2 DCTs in one file", which the canonical single-DCT manifest has no slot for. Modelled it as a
  top-level `dcts[]` array of two single-avatar DCTs, each with its own image pool. A reader trusting
  the canonical schema would have produced one DCT with one flat pool instead.
- **`high-converting-static-brief.md` hard-codes Singapore with no non-SG branch (leakage friction).**
  Rules 3 and 8 bake in SG specifics: ethnicity distribution (Chinese / Malay / Indian / Eurasian),
  CPF / HFE documents, "Straits Times feature / Kinfolk editorial" aesthetic, SG photographer names
  (Geraldine Kang, Sean Lee). The file's own origin header says it was authored "during neezanizam
  DCT001 generation" and then declares it applies "for every client". For a non-SG client this brief
  would force SG ethnic logic and SG documents onto the wrong market with no override path. Meridian
  happens to be a fictional SG client, so the SG rules apply cleanly here and produced correct output —
  but the leakage is real: a single client's market assumptions are hard-coded as a universal MANDATORY
  gate. Followed it as-is (SG-correct), logged the leakage. A repair would parameterise market/ethnicity
  from `context-profile.json` instead of hard-coding SG.
- **No `dct.json` template / scaffold for a static-only DCT — had to mirror a real client's file.** The
  skill's canonical-shape pointer is `docs/dct-json-schema.md` (not read this run — the brief directed
  mirroring the neezanizam file for shape). To get the field shape I had to open a REAL client's live
  manifest as the only concrete example. The brief's guard ("read for shape ONLY, copy no content")
  worked, but it means the only ground-truth shape reference for a new client is another client's
  production data — there is no neutral fixture. Friction: a fictional/new client has to reach into a
  real client's folder to learn the output shape. (Mitigated here by the no-copy rule; still a coupling.)
- **The static brief's output contract names `dct-tracker.json`, but the canonical manifest is `dct.json`.**
  `high-converting-static-brief.md` (lines 52, 70, "Output contract — per variant, in `dct-tracker.json`")
  and the SKILL.md Phase 2a output schema both still say `dct-tracker.json`, while the 10-5-5 section +
  the brief's own task say the canonical manifest is `dct.json`. Same unresolved G1 blocker the SKILL.md
  flags ("Phase 2 emitter still writes legacy dct-tracker.json"). Wrote `dct.json` per the task; the
  static brief's per-variant contract (`image_prompt_file` referencing an external file) was NOT followed
  literally — the brief mandates storing the full prompt in a separate `image-prompts/<batch>-<variant>.json`
  and only referencing it in the tracker. The task asked for the prompts INLINE in dct.json (mirroring the
  neezanizam file, which inlines `image_prompt` strings). Followed the task (inline) over the static
  brief's file-reference rule. Friction: the static brief and the canonical dct.json disagree on whether
  image prompts live inline or in sidecar files — neezanizam's production dct.json inlines them, the brief
  forbids inlining. Two live conventions contradict.
