# A1 — Generation-Skill Crawl (money-path skills)

Repo root: `/Users/jerel/Documents/Jerel's brain/jerel's brain/Marketing` (paths below relative to root unless `~`-prefixed).
Scope: 18 skills + copywriting-os skim. Every claim tagged FACT (read/verified) or JUDGMENT (interpretation).

---

## 0. Executive picture

- FACT — The pipeline's gating does NOT stop after angles at the instruction level: `ad-concept-engine` documents 5 HITL gates (persona, angle, copy, creative, tracker — skills/ad-concept-engine/SKILL.md:234,276,356,570,618,660), `image-generation` has a mandatory pre-spend prompt-review gate (skills/image-generation/SKILL.md:143-151), `sales-letter-method` has 4 gates incl. a FAIL-stops-ship pre-ship checklist (skills/sales-letter-method/SKILL.md:69-91), and video has AG1/AG2 + an eval-buyer-fit HARD GATE (skills/vid-director/SKILL.md:48).
- JUDGMENT — The operator's belief that "gating stops after angles" is accurate for ONE specific path: a standalone `big-angle-spotter` run, which generates angles → headlines → image prompts inside a single script where quality gates are "logged, not auto-retried" (big-angle-spotter/SKILL.md:146) and no human approval fires between steps. If most waves run through that script, the lived experience matches the belief even though the documented system refutes it.
- FACT — Context grounding is wildly uneven: from fail-closed (`headline-bank`, `video-concept-lab`, `feedback-router`) to zero-file-required (`big-angle-spotter` default mode, `copywriting` one-off mode, all five "copywriting-foundation" skeletons).

---

## 1. Skill-by-skill

### 1.1 avatar-research (SKILL.md, 539 lines, v1.0.0)
- CLAIMS vs ACTUAL: FACT — description promises 3-7 micro-personas feeding downstream workspaces; body delivers a 4-phase + 2-HITL process that does exactly that (SKILL.md:114, 168, 413). Honest skill.
- GROUNDING: FACT — "Required: `_brand/buyer-profile.md`, `_brand/icp.md`, `_brand/offer.md`" (SKILL.md:54-57). Fallback ladder: migrate psychology from a rich icp.md (59-68); "If NEITHER buyer-profile.md NOR a rich icp.md exists, route to `persona-builder` agent first" (69) — a genuine refusal/redirect. BUT Phase 3: "Flag any section where external research was thin — offer to fill from buyer-profile.md" (407) — thin external research is back-filled from the client's own prior file, never blocked. No quantified minimum research bar anywhere.
- FACT — Phase 2 research is MANUAL: the skill generates Perplexity/Grok/ChatGPT prompts and "User runs prompts externally, then pastes results back" (254). This conflicts with `.claude/rules/routing-overrides.md` §Combos, which says avatar-research chains the `buyer-language-researcher` agent + `persona-builder` as sub-steps. Two different processes for the same skill depending on which doc you read.
- OUTPUTS: FACT — binary-ish: `## MICRO-PERSONA MAP` block in buyer-profile.md with a fixed field table + refresh log (364-445). Distinctness checks are judgment calls (410-411).
- GATES: FACT — HITL Gate 1 (persona selection, 168), optional Gate 2.5 (sophistication, 352), Gate 2 (final approval, 413). Strongest human-in-loop of the research stage.
- LEAKAGE: FACT — generic Grok prompt template hardcodes "Search r/singaporefi, r/askSingapore, HardwareZone EDMW for '{product_category} ad', 'agent marketing', 'property seminar', 'this is why I don't trust agents'" (SKILL.md:309) and "posts making fun of property ads, agent marketing, or upgrade promises" (299). Also references/grok-prompt-template.md:46,53 and chatgpt-prompt-template.md:34 ("they check their CPF balance every Sunday night") use SG examples (the templates label them as e.g. values — milder).
- PATHS: FACT — Phase 0 step 0 depends on `~/AI workflows/research-vault/markets/` (120) — outside-repo dependency, breaks on any other machine.

### 1.2 big-angle-spotter (symlink, SKILL.md 206 lines)
- FACT — `skills/big-angle-spotter` is a symlink to `/Users/jerel/AI workflows/big-angle-spotter` (verified `ls -la`). The skill source of truth lives outside the repo.
- FACT — BROKEN LAUNCH PATH: SKILL.md:63 instructs `python3 ~/.claude/skills/big-angle-spotter/scripts/run_pipeline.py` — `~/.claude/skills/big-angle-spotter` does not exist (verified). The real script is at `~/AI workflows/big-angle-spotter/scripts/run_pipeline.py` (named only later, at line 188). A cold agent following step 4 fails.
- GROUNDING: FACT — default-mode inputs are 6 free-text slots typed/pasted by the operator: OFFER, COMPANY, PERSONA, INDUSTRY (+optional EXISTING_ANGLES, PRODUCT_IMAGE_REFS) (SKILL.md:22-32). No file is required; "PERSONA — demographic *and* psychographic (not just 'SG home-buyer')" is the only quality nudge. JUDGMENT — this skill will happily produce angles, headlines, and image prompts from a one-line persona with zero research on disk. This is the thinnest grounding on the money path.
- FACT — A hard gate EXISTS but is hidden: `run_pipeline.py` has an opt-in `--hardened` mode that is fail-closed ("hardened mode: OFFER is required (fail-closed)", "--buyer-profile is required (fail-closed)" — run_pipeline.py:1197-1205; scored JSON gate per memory) — but SKILL.md never mentions `--hardened` (grep: zero hits). The deterministic quality gate only fires if the operator remembers a flag the instructions don't document.
- GATES: FACT — "Gates (steps 2, 5, 6, 10) are logged, not auto-retried in v1... The orchestrator flags gate failures in SUMMARY.md with ⚠️; the operator decides" (146). Soft. No HITL between angle → headline → image-prompt steps inside a run.
- OUTPUTS: FACT — binary done condition: script exits "✅ Run complete.", agent reads SUMMARY.md + gate log (72-74). Provenance block required per headline but `source_phrase_id: null` is permitted (85-94) — provenance is aspirational, not enforced.
- LEAKAGE: FACT — line 10: methodology doc is "a bundled copy of the Neeza Nizam / 1up-marketing reference doc"; line 32 example "run big-angle-spotter for Neeza's property advisory offer". Mild (examples, not rules).

### 1.3 headline-bank (329 lines, v2.1.0)
- GROUNDING: FACT — hardest input gate of the copy skills: 7-item checklist (brand, angle, awareness, sophistication, persona, LP URL, angle spine) with "MUST all be present before running... If any are missing, halt and request them. No improvisation on inputs." (SKILL.md:74-86). Sources point at `_brand/buyer-profile.md` + big-angle-spotter artifacts.
- FACT — INTERNAL CONTRADICTION: the core prompt outputs "COPY A — PRIMARY (~150 words) / HEADLINE 1" then "COPY B — COMPRESSION (~50 words) / HEADLINE 2" (158-168), but the output-file template says "## COPY 1 (~50 words) / HEADLINE 1" then "## COPY 2 (~150 words) / HEADLINE 2" (206-216). The headline↔copy↔length mapping is inverted between the two templates; whichever the sheet writer assumes, half the runs will mislabel the lock.
- GATES: FACT — no HITL inside the skill; output feeds the COPY tab and is reviewed at ad-concept-engine Gate 2. JUDGMENT — acceptable since it's a sub-step, but a standalone `/ads:headlines` run ships copy with no documented review.
- LEAKAGE: FACT — "NeezaNizam (Propnex Realty SG)" as the example input (78); the GENERIC core prompt contains the read-cue example "see the number on your flat" (138) — an HDB-flavoured line that a naive agent will replicate for non-SG clients; Hard Rule 2 bakes a client avatar's tonal contract into the generic rules: "for Avatar 2 life-transition: no 'investment,' 'dream home,' 'build wealth'..." (176).
- CLAIMS vs ACTUAL: FACT — description matches body (curiosity-led ~150w + ~50w + 3-5w headlines, funnel-aware stop rules at 101-103). 10-5-5 over-draft→narrow craft is operational and concrete (294-302).

### 1.4 ad-concept-engine (761 lines, v2.0.0)
- CLAIMS vs ACTUAL: FACT — description says "3 creatives × 2 headlines × 2 copies = 12 combinations"; body delivers that plus a full conductor/resume protocol, format-split Phase 2a/2b, and 10-5-5 opt-in mode. Description undersells (it's also the wave conductor).
- GATES: FACT — "Process: 5 Phases + 5 HITL Gates" (234): Gate 0 micro-persona selection (276), Gate 1 angle approval (356), Gate 2 batch approval = headlines + copy + creative concepts per card (570-590), Gate 3 creative approval = rendered images/video (618-620), Gate 4 tracker sign-off before uploader (660-662). 10-5-5 keeps all five (743-752). This is the strongest documented refutation of "gating stops after angles."
- GROUNDING: FACT — Phase 0 loads `_brand/{buyer-profile,offer,brand-voice,icp,story-bank}.md` (240-245); BUT if no micro-persona map exists: "offer to run `/ads:avatars` first, or proceed in Legacy mode" (250) — an escape hatch that lets the whole DCT engine run without avatar research. Swipe-file absence is only "suggest running /ads:scrape-library" (288). JUDGMENT — soft gates; thin research produces output with a suggestion, not a stop.
- FACT — dead command: `/ads:avatars` (250) has no command file (`.claude/commands/ads/` contains only feedback, headlines, scrape-advertiser, scrape-library, source-of-truth — verified).
- LEAKAGE: FACT — Conductor Mode hardcodes client names in a generic skill: "10-5-5 opt-in clients (neezanizam, eugene)" (72, 712) with neezanizam workspace paths as canonical examples (87-89). references/high-converting-static-brief.md — loaded as "MANDATORY on every static batch" (689) and "for every client" (its line 4) — hardcodes "Singapore = Chinese / Malay / Indian / Eurasian" (rule 3), real-SG-document fidelity "CPF, HFE" (rule 8), and *Straits Times*/SG photographers (rules 4,7). A US client run inherits SG ethnicity rules unless the agent self-corrects.
- FACT — corrections.md is the healthiest in the repo (12+ dated entries incl. the 260420 one-row-per-DCT rule); learnings.md opens with an explicit "N=1 WARNING... priors, not laws" (learnings.md:3). Good epistemics.
- PATHS: FACT — NotebookLM notebook id `1644f7b5` hardcoded as 2nd-pass validator for ALL clients (255, 705), with "PropWise SG campaign scripts" as its content — SG-trained validation layer applied client-agnostically (JUDGMENT: subtle leakage vector).

### 1.5–1.9 The five "copywriting-foundation" skeletons
(persuasive-premise 129L, problem-promise 130L, unique-mechanism-problem 106L, unique-mechanism-solution 105L, usp-generator 108L)
- FACT — All five are `version: "0.1.0-skeleton"`, `status: skeleton-pending-calibration`. All five have "Worked Examples — TODO" and "Calibration Set — TODO" (e.g. persuasive-premise/SKILL.md:104-112). All five cite `references/canonical-sources.md (TODO)` — and none of the five folders contains a references/ directory at all (verified ls: SKILL.md is the only file).
- GROUNDING: FACT — each lists "Required Inputs" with REQUIRED labels (e.g. problem-promise/SKILL.md:65-68) but there is NO halt/refuse language anywhere — REQUIRED is a label, not a gate. "REQUIRED if exists" (persuasive-premise:67, UMP:48, UMS:48, usp:47) is an oxymoron that operationalizes as optional. JUDGMENT — any of these will emit a premise/mechanism/USP from a thin or absent dossier without complaining.
- FACT — PATH CONVENTION CONFLICT: all five require `clients/<project>/offer.md` and `clients/<project>/research/buyer-language-dossier.md` (flat root), while the repo canon (CLAUDE.md AGENT ENTRY CONTRACT, sales-letter-method/SKILL.md:97-105, avatar-research:54-57) is `_brand/offer.md`. The required files point at the legacy layout, so even a compliant agent looks in the wrong place.
- OUTPUTS: FACT — strong typed YAML schemas with binary test_questions (must-be-yes) — the best output contracts in the set; but with zero few-shot examples the disagreeability/uniqueness tests have no calibration anchor (JUDGMENT).
- FACT — Downstream handoff claims "Cross-reference in headline-bank, ad-concept-engine, sales-letter-method system prompts as required input" (persuasive-premise:118) — not wired: headline-bank's input checklist (74-86) does not include persuasive-premise.md or any mechanism file. Aspirational integration.
- GATES: none. No HITL, no reviewer.

### 1.10 source-of-truth (300 lines)
- CLAIMS vs ACTUAL: FACT — matches: triage (slug/URL/idea) → parallel research → 26-section synthesis → 1 HITL gate → write + derivatives (SKILL.md:72-258).
- GROUNDING: FACT — Mode C runs from a free-text idea + 5-7 intake questions (90-95, 126-135) — by design it can build the full strategy doc from near-zero, but it SPAWNS research first and carries the repo's best anti-fabrication rails: "if any single research source fails... Mark missing sections '⚠️ NOT AVAILABLE'... NEVER hallucinate buyer quotes — if buyer-language-researcher returns thin results, flag the section" (168) and the same at 266. Phase 0 step 3 forces an onboarding-artifact ask BEFORE research, with the honest admission "without them, the skill fabricates what the founder could have told us directly" (113).
- JUDGMENT — minimum research bar is qualitative ("thin → flag"), never quantified (no min quote count / source count). A doc can ship with many ⚠️ sections.
- GATES: FACT — Phase 4 HITL: exactly 4 strategic decisions (KPI, core message, 3 priority angles, first test variable) (204-215). Binary-ish done: file written + derivative files + manifest (221-242).
- FACT — dead commands in the hand-off message: "1. /ads:avatars <project> ... 2. /ads:concepts <project>" (255-256) — neither command file exists.
- LEAKAGE: FACT — neezanizam as example slug (77), neezanizam lesson baked in (109), r/singaporefi as the canonical quote-format example (263); references/research-pipeline.md:115-133 is an SG-property subreddit table; references/sheet-integration.md:74 neezanizam example. JUDGMENT — examples more than rules; tolerable but steers pattern-matching toward SG property.

### 1.11 copywriting (520 lines, v1.0.0)
- CLAIMS vs ACTUAL: FACT — generic page-copy craft skill (principles, style rules, page-structure frameworks, CTA guidance). Description accurate.
- GROUNDING: FACT — "If a client context is active, READ the client folder first — do not interview for what's already on disk" (`_brand/offer.md`, `_brand/buyer-profile.md`, context-profile.json) (54) — read-first, but no STOP if absent. With no client context it interviews 4 question groups and writes (52-80). JUDGMENT — one-off mode = a full landing page from a chat interview with zero research files; the hard stop ("copy session... must STOP and load it") lives in CLAUDE.md's AGENT ENTRY CONTRACT, not in this skill — a session that loads the skill without the contract has no gate.
- GATES: FACT — none internal. Quality enforcement is deferred: unslop profiles as soft constraints at draft (43-50), copy-editing as the hard pass, and the `/copy:landing` wrapper adds copywriting-OS gates — whose own input gate is soft: "If any of the 3 is missing from the client files, ask the operator ONCE before writing (don't overwhelm). Then write." (.claude/commands/copy/landing.md:24).
- OUTPUTS: FACT — copy + annotations + 2-3 headline/CTA alternatives (407-431). No score, no binary done-condition.
- FACT — corrections.md is empty boilerplate (header only).

### 1.12 sales-letter-method (122-line SKILL.md + the deepest reference tree)
- CLAIMS vs ACTUAL: FACT — matches and over-delivers: 5-phase pipeline with parallel drafters, stitcher, 5-reviewer conversion gate, polish + pre-ship gate (SKILL.md:67-91). The 5 reviewer files exist (reviewers/: buyer-lens, coherence, copy-chief, pre-ship-checklist, self-contained — verified).
- GROUNDING: FACT — 8 ordered required inputs (95-103); `_brand/` declared canonical with legacy-root fallback + migration flag (105); "If any critical input is missing, surface to the user before drafting. Do not fabricate." (107). JUDGMENT — "critical" is undefined, so the stop is discretionary; still the strongest stated input discipline among generators.
- GATES: FACT — Phase 0 HITL (component matrix confirm), Phase 0.5 claim audit (CAN/CANNOT/NEEDS WORDING before drafting, 72-73), Phase 0.7 mechanism HITL — "Drafters running without the Phase 0.7 document is a hard error" (82), Phase 3 "mandatory... Skip any one and the review is broken" (87-88), Phase 4 isolated fresh-eyes auditor + "Any FAIL stops the ship" (91; references/phase-4-preship.md:13 "Any FAIL on the pre-ship lenses stops the ship", isolated-context requirement at :22-24). Binary and testable.
- FACT — FABRICATION-ADJACENT INSTRUCTION: prompt-template.md context block: "MECHANISM NAME: {{if the client has named their system... If none, invent one that fits.}}" — direct instruction to invent a mechanism label, sitting in the same skill as the Phase 0.5 claim audit (JUDGMENT: naming a real method is legitimate positioning, but "invent" with no guardrail invites mechanism-washing on thin offers).
- FACT — prompt-template.md:5 routes through deprecated `/content:sales-letter` while SKILL.md frontmatter says `/copy:sales-letter` — stale.
- PATHS: FACT — evals/evals.json hardcodes absolute paths incl. `/Users/jerel/.../clients/neezanizam/_brand/` (evals.json:3,11-12,91). Eval fixtures, so tolerable, but non-portable.

### 1.13 copy-editing (564 lines)
- CLAIMS vs ACTUAL: FACT — 8-sweep editing framework as described. Input = an existing draft; "Before You Start" asks goal/audience/action (396-401) — soft.
- GATES/DONE: FACT — quantified: "Quality gate scored >= 35/50" in the De-AI checklist (414) plus per-sweep binary checklists (404-463). Best binary done-conditions of the copy skills.
- OWNERSHIP: FACT — routing-overrides.md declares `forbidden-content-audit.md` the canonical kill-list and says copy-editing Sweep 8 "defers" to it — the deference is asserted in routing-overrides, not visible in copy-editing's own text (unverified in skill body). JUDGMENT — two kill-lists (references/overused-ai-patterns.md + copywriting-os forbidden-content-audit) risk drift without an explicit pointer inside the skill.
- FACT — corrections.md empty.

### 1.14 image-generation (535 lines)
- CLAIMS vs ACTUAL: FACT — Tier-1 router + Vertex/NB2 backend + HITL + carousel + video ref frames, as described (40-48).
- GATES: FACT — three real ones: routing gate (50-63), MANDATORY backend ask — "Never silently pick a backend" (77-115), and the HITL Prompt Review Gate: "Before generating any image... Only after approval, proceed to generation" (143-151), plus batch-review in video-ref mode (169) and a post-render dimension gate (283). This directly refutes "no gating at image prompts."
- GROUNDING: FACT — no requirement to read buyer research; the quality bar assumes "angle + headlines are approved" upstream (references/gut-wrenching-ad-format.md:27-28). JUDGMENT — correct division of labor, but a standalone invocation generates from chat description alone.
- FACT — CONFLICT: "CRITICAL: Respond in the same language the user is using" (119) contradicts the repo-level "Always reply in English" override (routing-overrides.md §Copy principle overrides explicitly kills this AgentKits boilerplate — but the line is still live in the skill).
- FACT — DUPLICATE STANDARD: references/gut-wrenching-ad-format.md is a genericized copy of ad-concept-engine/references/high-converting-static-brief.md — same 9 rules, same "physically ill if they scroll past" bar, two files, two owners. Drift risk: the ACE version still hardcodes SG ethnicity/documents as universal rules; the image-gen version half-fixes it ("for SG clients: Singaporean" — gut-wrenching:rule 3) while SKILL.md:133 still says "real-not-AI Singaporean/locale casting".

### 1.15 video-concept-lab (315 lines, v0.2.0)
- CLAIMS vs ACTUAL: FACT — honest about its own demotion: "this skill is the rubric/reference the seeder reads — not a second runtime concept generator" (33, 43).
- GROUNDING: FACT — tightest contract in the repo: Brief Type Gate "mandatory pre-load" with ask-don't-default on ambiguity (112-118); "Halt-and-ask: if `awareness_stage` is missing/empty in concept-brief.json, halt and request operator input. Do NOT default" (130); "Seeder refuses to emit concepts otherwise" for L3+ briefs missing big_idea/credibility_stack (132); product-reference gate script before any product image (250); evaluators must verify the methodology receipt or "reject and force re-dispatch" (84).
- GATES: FACT — AG1 hard stop: "Save approval-1.json with status: pending. Nothing proceeds... until operator approves" (242).
- PATHS: FACT — scripts/validate_reference_graph.py hardcodes `/Users/jerel/.claude/agents/...` and `/Users/jerel/.claude/prompts/orchestrators/...` absolute paths (lines 76-78, 114-119) — validator breaks off-machine.
- OUTPUTS: FACT — binary: concepts-draft.json + inputs-used.json with required receipt schema (66-82); validator exits 0/non-zero (288-295).

### 1.16 video-hook-variants (117 lines, v1.0.0)
- FACT — rubric for a dispatched agent; "Single-clip flows are refused" (frontmatter + 111 `multi_clip_flow: true` (refuse if false)). Dispatch contract enumerates required context incl. `_brand/*.md` files (104-112). Output contract with methodology_receipt (113-115). Six-Question Checklist gives a scoring rubric (74-83). Clean boundaries (34-38). References tree exists (frameworks/, checks/, examples/ — verified). JUDGMENT — no findings of concern; best-shaped small skill in the set.

### 1.17 vid-director (100 lines)
- FACT — pure router: "You route, dispatch, and gate... Don't write scripts... Don't generate concepts" (12-21). eval-buyer-fit is a "Brand-alignment HARD GATE on AG1, AG2, and any html-publisher dispatch" with a 3-cycle cap (48); the render-layer enforcement also lives in routing-overrides.md §Brand-alignment evaluator gate (refuse-to-render unless PASS or recorded override).
- FACT — corrections.md exists but is 0 bytes; the SKILL.md tells agents to "always read after skill loads" (91) — harmless but empty loop.
- PATHS: FACT — references/EDITING.md is a map of ~20 absolute `/Users/jerel/...` paths spanning `~/.claude/` and `~/AI workflows/` (EDITING.md:9-45). By design (cross-workspace edit map) but the skill is unusable as documentation anywhere else.

### 1.18 feedback-router (216 lines, v1.0.0)
- GATES: FACT — most fail-closed skill in the set: Phase 0 "If any check fails → surface the gap, stop. Don't route on thin data" (90); references/routing-criteria.md pre-routing gates table (min S$200/creative, S$600/batch, 7 days, 5,000 impressions, populated tracker) with "If any pre-routing gate fails → output: INSUFFICIENT_DATA. Do not route." (routing-criteria.md:9-19). Binary thresholds per route. Anti-patterns include "Don't fabricate metrics" (180).
- FACT — STALE DEPENDENCY: frontmatter requires `mcp_integrations.required: meta-ads` (29-31) — but `.claude/rules/mcp-integrations.md` states "Meta / Facebook Ads = CLI, not MCP... there is no meta-ads MCP server." A compliant agent hits a dependency that cannot exist.
- FACT — DEAD ROUTES: all three routes resolve to `/ads:concepts <slug>` (with `--refine`/`--expand` flags) or `/ads:avatars` (125-130, 187-192) — `/ads:concepts` was retired 260609 (routing-overrides.md: "replaces the dead /ads:concepts command reference") and no command file exists (verified). The feedback loop's output is a recommendation the operator cannot run verbatim.
- LEAKAGE: FACT — S$ (Singapore dollars) baked into generic defaults (75-77, 88, routing-criteria gates) and a fully neezanizam-flavoured example output (149-169). JUDGMENT — thresholds belong in client config (the file does allow `feedback_router_thresholds` override — routing-criteria.md:3 — so this is default-leakage, not hard-coding).

---

## 2. copywriting-os skim (.claude/references/copywriting-os/)
- FACT — Structure: `_index.md`, `_newsletter-index.md`, gates/ (3), builders/ (2), reviewers/ (9 across Phase B anti-hallucination + Phase C quality), frameworks/ (12, all populated, 134-338 lines each — verified wc), case-studies/, raw-newsletters/ (48 files).
- FACT — Reviewer thresholds are binary and quantified: claim-verification "Coverage ≥ 95%, zero CRITICAL unsourced"; specificity "< 4 per 1000 words"; proof-density "≥80% density, ≥4/6 types"; emotional-sequence "no skips, no reversals" (_index.md reviewer tables). Frameworks carry verbatim primary-source quotes (five-headline-mechanisms.md:20-23; six-emotional-states.md:17-21). JUDGMENT — copy generation routed through `/copy:*` wrappers is genuinely well-grounded; copy generated by invoking the raw skills directly bypasses all of it.
- FACT — stale note: `_newsletter-index.md:10` still says "12 stub framework files in frameworks/ are still empty" — contradicted by the populated files and `_index.md`'s "POPULATED 2026-04-25".

---

## 3. Cross-cutting findings

1. FACT — GROUNDING SPECTRUM. Fail-closed: headline-bank (halt on missing inputs), video-concept-lab (halt/refuse), feedback-router (INSUFFICIENT_DATA), sales-letter-method (surface-before-drafting + phase hard errors). Soft/flag-only: avatar-research, source-of-truth, ad-concept-engine (Legacy-mode escape hatch). None: big-angle-spotter default, copywriting one-off, all 5 skeletons. JUDGMENT — the two skills that originate ANGLES AND COPY FROM SCRATCH (big-angle-spotter, copywriting) are the two with the weakest grounding requirements; the skills that refuse are mostly downstream packagers.
2. FACT — TWO CLIENT-FILE CONVENTIONS COEXIST: `_brand/offer.md` canon (CLAUDE.md, sales-letter-method:97-105, avatar-research, ad-concept-engine, headline-bank) vs flat `clients/<project>/offer.md` + `research/` (all 5 skeletons, source-of-truth Mode A load list at :79, feedback-router learnings paths). Only sales-letter-method documents the fallback explicitly.
3. FACT — DEAD/DEPRECATED COMMAND REFERENCES in live skills: `/ads:avatars` (avatar-research:50,449; ad-concept-engine:250; source-of-truth:255), `/ads:concepts` (source-of-truth:256; feedback-router:125-130,188-192; headline-bank:56), `/content:sales-letter` (sales-letter-method/prompt-template.md:5), `/test:ab-setup` (source-of-truth:257, unverified). The intent-routing replacement exists only for the DCT conductor (routing-overrides 260609); avatar entry has no documented replacement.
4. FACT — CORRECTIONS LOOP MOSTLY DORMANT: corrections.md empty/boilerplate in copywriting, copy-editing, image-generation, feedback-router, avatar-research, sales-letter-method, vid-director (0 bytes). Active only in ad-concept-engine (12+ entries), headline-bank (2), source-of-truth (4.5KB). JUDGMENT — the "compounding loop" the repo's skill-activation rule depends on is real for the DCT pipeline and fiction elsewhere.
5. FACT — DUPLICATED 9-RULE STATIC STANDARD: ad-concept-engine/references/high-converting-static-brief.md (SG rules declared universal) vs image-generation/references/gut-wrenching-ad-format.md (genericized). Same bar, two owners, already diverged on locale handling.
6. FACT — SG/CLIENT LEAKAGE RANKING (worst first): (a) high-converting-static-brief.md — SG ethnicity/CPF/Straits Times as rules "for every client"; (b) avatar-research:309 — SG-property subreddits + search strings inside the generic Grok prompt; (c) headline-bank:138,176 — HDB read-cue + client-avatar banned words in generic rules; (d) feedback-router — S$ thresholds as defaults; (e) ad-concept-engine conductor — neezanizam/eugene named (legitimate per-client config, wrong layer: client opt-ins living inside a generic skill); (f) source-of-truth / sophistication-creative-map — SG examples (examples only; sophistication map was explicitly multi-product-ified per corrections 260418).
7. FACT — ABSOLUTE-PATH HOTSPOTS: big-angle-spotter SKILL.md:63 (dead `~/.claude/skills/...` path), video-concept-lab/scripts/validate_reference_graph.py:76-119, vid-director/references/EDITING.md:9-45, sales-letter-method/evals/evals.json:3-91, avatar-research:120 (`~/AI workflows/research-vault`), vid-director:59-63 (`~/AI workflows/higgsfield-prompts`). Plus the big-angle-spotter symlink itself: the repo's most-used angle pipeline is versioned OUTSIDE the repo.
8. JUDGMENT — VAGUE vs OPERATIONAL: most operational = video-concept-lab, feedback-router, headline-bank core prompt, copy-editing checklists, sales-letter reviewer stack. Most vague = the 5 skeletons (no examples by their own admission), copywriting principles ("clarity over cleverness" with no test), avatar-research distinctness checks. Missing few-shot examples are self-declared TODOs in 5 skills.
9. JUDGMENT — OWNERSHIP SEAMS THAT COULD BITE: headline-bank vs big-angle-spotter overlay-headline split is well documented (58-62) — fine. copywriting vs copy-coach vs copy-editing — resolved only at routing-overrides layer, invisible inside the skills. Kill-list ownership (forbidden-content-audit vs overused-ai-patterns vs unslop) — declared at routing layer, not inside copy-editing. avatar-research manual-paste research vs routing-overrides' agent-chain — unresolved contradiction.

---

## 4. The operator's gating question, answered precisely
- Angles: gated (ACE Gate 1; big-angle-spotter soft-logged only).
- Copy: gated at ACE Gate 2 (cards with headlines+copy), headline-bank input halt, sales-letter Phases 0.7/3/4, copywriting-OS reviewers via /copy:* — FACT, documented.
- Image prompts: gated — image-generation Prompt Review Gate (143-151) + gut-wrenching step 5 "Run through the Prompt Review Gate (HITL) before any spend".
- Rendered creatives: gated — ACE Gate 3 (618).
- Tracker/upload: gated — ACE Gate 4 (660); uploads created PAUSED (feedback-router:191).
- THE ACTUAL HOLE (JUDGMENT): inside a single big-angle-spotter run, angle→headline→image-prompt flows with zero HITL and soft gates; and any skill invoked directly (not via /copy:* or conductor) bypasses the OS reviewers entirely. The belief "gating stops after angles" is wrong on paper, right for the standalone-script path.

---

## 5. Top fixes by leverage (JUDGMENT)
1. Fix big-angle-spotter SKILL.md:63 dead path; document `--hardened` and make it default-on for client work.
2. Resolve headline-bank COPY 1/2 ↔ HEADLINE 1/2 ↔ length inversion (158-168 vs 206-216) before the next sheet write.
3. Repoint the 5 skeleton skills' Required Inputs to `_brand/` paths and add a one-line halt clause; or mark them not-for-production until calibration lands.
4. Merge the two 9-rule static standards into one file with a locale parameter; strip "Singapore = ..." from the universal rules.
5. Sweep dead `/ads:avatars`, `/ads:concepts` references; give avatar-research an intent-routing entry like the DCT conductor.
6. feedback-router: replace `meta-ads` MCP requirement with the `meta` CLI per mcp-integrations.md.
