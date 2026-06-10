# A2 — Infra Skills & Scripts Crawl

Repo: `/Users/jerel/Documents/Jerel's brain/jerel's brain/Marketing` (paths below relative to repo root unless `~`).
Date: 2026-06-10. Method: read SKILL.md files in full or targeted chunks, verified every referenced script/agent/path on disk, diffed script key-expectations against the newest real pipeline artifacts, test-ran read-only scripts. FACT = verified by reading/running; JUDGMENT = interpretation.

---

## 1. The headline drift, verified end-to-end (render.py + sheet writers vs dct.json)

The pipeline migrated its canonical per-DCT data file from `dct-tracker.json` (legacy, one big `creatives[]` array) to `dct.json` (new shape) on 2026-06-08, but three of the four scripts that consume it still read the old shape. The migration is **known and tracked** by the owning skill — it is not silent rot.

### 1.1 What the data actually looks like now

Newest tracker workspace: `clients/neezanizam/campaigns/buyer-funnel/dcts/dct-10-5-5-proof-260603/` (dct.json mtime 8 Jun 20:53, with `dct.json.pre-migrate-260608.bak` + `dct.migration-report.json` siblings).

- FACT — Legacy `dct-tracker.json` top keys: `creatives[]`, `dct_structure`, `kill_rules`, `sheet_write_plan`, etc. Each creative has `batch`, `copy_1/copy_2`, `headline_1/headline_2`, `variations[]`; each variation has `variant_id`, `image_prompt`, `visual_style`, `canva_link` (verified via jq).
- FACT — Current `dct.json` top keys: `angles[]`, `image_pool`, `avatar`, `constant`, `meta_adset`, `offer`, `tracking`, `dct_method`, … **No `creatives` or `ads` key.** Copy lives at `angles[].primary_text` + `angles[].headline`; image prompts live at `image_pool.images[].image_prompt` (operator decision 2026-06-08, documented in `scripts/migrate_tracker_to_dct.py:1-37`).

### 1.2 render.py — tracker mode is dead against the current shape

- FACT — `scripts/ad-images/render.py:80` does `data.get("creatives") or data.get("ads") or []`, then matches `c.get("batch")` (line 82), then `variations[].variant_id/variant` (line 85), then `image_prompt` / `image_prompt_file` (lines 89-97). This is byte-for-byte the LEGACY tracker shape. Against a current `dct.json` it returns an empty list → exits "batch not found" for every batch.
- FACT — The bypass is real and in use: render sidecars at `.../dct-10-5-5-proof-260603/image-prompts/renders/` show `DCT010-A01-v1.png.meta.json` rendered `--from-tracker` (pre-migration, 8 Jun 15:31) while `DCT010-A01-v1-chumbox.png.meta.json` shows `"source": "inline-prompt"` — the `--prompt` bypass.
- FACT — Three stale path references: render.py docstring line 22, `scripts/ad-images/README.md` ("Run it from a real pipeline output" section), and the v1 sidecar's recorded `source` all cite `clients/neezanizam/campaigns/dct-10-5-5-proof-260603/dct-tracker.json` — that path no longer exists (`ls` → No such file). Real path gained `buyer-funnel/dcts/` segments.
- FACT — `scripts/ad-images/styles/_registry.json` is healthy: 2 styles (`dr-clean-static` default, `chumbox-native`), both `.md` files present. Engine table has only `gpt-image-2` live; nano-banana/higgsfield are commented stubs (render.py:59-63).
- JUDGMENT — Fix is small: teach `prompt_from_tracker()` a third branch reading `image_pool.images[]` keyed by `id`/`source`, or point it at `dct.json`. Until then every 10-5-5 render is hand-pasted prompts, which defeats the "stop the manual grind" purpose stated in the README.

### 1.3 The drift is documented by its owner

- FACT — `skills/ad-concept-engine/SKILL.md:116` explicitly tracks the open blockers: "(G1) the Phase 2 emitter still writes legacy dct-tracker.json, (G3) allocate/phase_3b is unbuilt, (G4) ad_concept_sheet_writer.py still reads the old format… a 10-5-5 run yields … a dct.json (via migrate_tracker_to_dct.py), while the live sheet/upload steps still touch the legacy artifact." render.py is NOT on that blocker list (no SKILL.md references render.py at all — grep returned zero) — the render-side drift is untracked.

### 1.4 Sheet writers — split-brain, plus two sibling bugs

- FACT — `scripts/ad_concept_sheet_writer.py` (770 lines, owner: ad-concept-engine per its docstring) reads legacy shape only: `tracker["creatives"]` (line 321/328), `copy_1/copy_2/headline_1/headline_2` (lines 461-464), 3-2-2 COPY header. Cannot write a 10-5-5 `dct.json`.
- FACT — `scripts/tr_10_5_5_sheet_writer.py` is the new-shape writer (reads `angles[].primary_text/headline`, `image_pool.images`) but is hardcoded to one client/campaign: `SHEET_ID = "1KqWJP08h8B…"` (line 38), `DCT_IDS = ["DCT101"…"DCT105"]` (line 37), defaults `--client neezanizam --campaign thomson-reserve` (lines 153-154). Good gates though: dry-run default, aborts live write unless all 5 DCTs have 5/5 copy (lines 130-131).
- FACT — Sibling drift #1: `scripts/source_of_truth_sheet_writer.py:79` looks ONLY at `clients/<slug>/metrics-config.json` (client root). But the two active sheet clients keep it at `clients/neezanizam/_brand/metrics-config.json` and `clients/eugene-chieng/_brand/metrics-config.json` (verified by find; only hazecraft + templates still have root-level). The AVATARS writer raises FileNotFoundError for exactly the clients it was built for. `ad_concept_sheet_writer.py:272-273` handles both locations — the fix exists in a sibling and was never back-ported.
- FACT — Sibling drift #2: `scripts/patch_angle_cell.py:40` has the same root-only `metrics-config.json` path, and reads legacy `creatives[]` (line 92-95). Its docstring example tracker paths (lines 14-15) omit the now-required `/dcts/` segment. `scripts/backfill_angle_rationale.py` likewise targets `creatives[0].angle_rationale` (line 18) — legacy-only.
- JUDGMENT — Net: for any new 10-5-5 wave outside Thomson Reserve there is currently NO working sheet writer; for AVATARS writes on neezanizam/eugene there is NO working writer at all until the `_brand/` path lands in `source_of_truth_sheet_writer.py`.

---

## 2. Infra skill audits (12 skills)

### 2.1 client-onboarding (`skills/client-onboarding/SKILL.md`, 512 lines)
- FACT — Claims match machinery: `scripts/scaffold-client.sh` exists; `clients/_template/` exists; ICM linter path `~/.claude/skills/icm/marketing-scaffold/scripts/validate-icm.sh` is invoked at Phase 4 (line 265). Gates are explicit: checkpoint protocol (lines 300-339), readiness score + ICM verdict shown separately (lines 281-284). Done-condition is crisp: "onboarding ends when the client has a paste-ready strategy prompt" (line 58).
- FACT — Broken ref: `references/scraper-prompts.md` cited at line 179 and listed at line 498 with "(TODO if missing)" — it IS missing; only `discovery-questions.md` exists in `references/`.
- FACT — Dead agent ref: Graph Links "Used by agents: [[project-manager]]" (line 39) — project-manager.md deleted.
- JUDGMENT — Otherwise the strongest-specified skill in the set; the 14-CONTEXT.md / 9-phase-template scaffold contract (lines 125-130) is detailed enough to audit a scaffold against.

### 2.2 campaign-runner (`skills/campaign-runner/SKILL.md`, 399 lines)
- FACT — Frontmatter agents list (lines 32-39): of 7 named agents, 5 are deleted (email-wizard, attraction-specialist, planner, project-manager, tracking-specialist) and seo-specialist is deleted too — only `copywriter` survives. Prerequisite skill `social-media` (line 21) now lives in `skills/_archive/social-media/`.
- FACT — Machinery exists: `scripts/state_manager.py`, `templates/state-template.yaml`, 6 campaign-type YAMLs, `references/execution-playbook.md`, `skills/integrations/postiz/index.md` all on disk.
- FACT — Frontmatter lists `meta-ads` under mcp_integrations (line 45) and a `skills/integrations/meta-ads/` folder exists — contradicting `.claude/rules/mcp-integrations.md` ("Meta = CLI, not MCP… there is no meta-ads MCP server").
- FACT — Workspace contract here (lines 127-142) omits `00_inputs/`, `eval/`, and `CONTEXT.md` that client-onboarding's version of the same contract includes (client-onboarding lines 426-451). Two specs for one structure, drifting.
- JUDGMENT — This skill reads like the V3 generation: Postiz/HubSpot-centric lifecycle that the current DCT/vid-director pipelines largely route around. The agent roster is the most rotted in the repo.

### 2.3 brand-scaffolder (GLOBAL — `~/.claude/skills/brand-scaffolder/SKILL.md`, 117 lines; NOT in repo skills/)
- FACT — Clean: explicit missing-file diff (Step 1), grounding rule "never fabricate… insert [NEEDS USER INPUT]" (line 75), hard HITL gate "Do not write on silence" (line 103), exact done-state string (line 114). Writes only to `_brand/` (boundary stated twice).
- FACT — Minor path drift: Step 2 inventories `clients/<slug>/business-summary.md` at client root (line 41), but client-onboarding writes it to `_swipe/research/<slug>-business-summary.md` (client-onboarding line 369).

### 2.4 business-profile (`skills/business-profile/SKILL.md`, 314 lines)
- FACT — Interview skill, 6 sections / ~21 questions, output strictly `clients/<project>/context-profile.json`; "Accept partial answers… never invent content" (line 55). `brand.vertical` must match keys in `skills/onboarding-strategy-pdf/references/benchmarks-registry.md` (verified the cross-ref text at line ~145).
- FACT — Branded "Fuggy's Media" in frontmatter + body — intentional (it IS the Fuggy's intake form), but it means a non-Fuggy client sees Fuggy's welcome copy verbatim (Section 1, line 82). JUDGMENT: client leakage by design; fine for the agency's own form, awkward if reused white-label.
- FACT — Mode detection checks `clients/<project>/icp.md` at client root (line 70) — the v2.x flat structure client-onboarding declares "forward-only deprecated" (its line 489). Works for legacy clients only.

### 2.5 sheets-provisioner (`skills/sheets-provisioner/SKILL.md`, 230 lines)
- FACT — Best gate-documentation in the set: the SA-cannot-create-Sheets auth gotcha is flagged "READ FIRST" (line 33) with full model in `references/sheet-auth.md` (exists). HITL confirm block before provisioning (lines 73-85). Idempotent tab creation documented. All referenced scripts exist: `scripts/modal/setup/provision_campaign.py`, `provision_lp_tabs.py`, `skills/sheets-provisioner/scripts/find_or_create_sheet.sh` + `provision_from_template.py`, canonical template at `clients/_template/_brand/metrics-config.json`.
- FACT — Explicitly deprecates its own old path: "The old scripts/modal/sheets_creator.py path assumed the service account could create — it can't" (lines 197-198); sheets_creator.py still on disk.
- FACT — Hardcoded example IDs leak into instructions: template sheet `14bh8k6S-…NTNKSE` (line 186), `neezanizam@neezanizam-492212.iam.gserviceaccount.com`, `ops@1upsalesai.com` (line 189), NeezaNizam ad-account ids in the input table (line 69-71). JUDGMENT: as worked examples they're useful; the risk is an agent copy-running them for a different client.
- FACT — "Next daily cron (9am SGT) writes the first row automatically" (line 110) — cron liveness unverified from the repo.

### 2.6 sheets-updater (`skills/sheets-updater/SKILL.md`, 161 lines)
- FACT — Reads `config["ad_platforms"]["meta"]["ad_account_id"]` flat shape (line 24) — the canonical template + live configs are now `campaigns[]`-keyed (`clients/neezanizam/_brand/metrics-config.json` top keys: `_comment, campaigns, client_slug, provisioning`). The skill's pseudocode shows the pre-260419 legacy shape; the actual Modal scripts (`scripts/modal/config_loader.py`) handle migration, but an agent following the SKILL.md literally would mis-read the config. Same family of drift as §1.4.
- FACT — Dangling refs: "immediate DM to Strategist via Pentagon MCP" (line 133) — no `pentagon` MCP in `.claude/rules/mcp-integrations.md`; Pentagon is a memory-file concept. Also expects config path at client root (line 14: `clients/<slug>/metrics-config.json`) — see §1.4 `_brand/` move.
- FACT — Good rules block: never fabricate, protected columns sacred, log every run, fail loudly (lines 146-152).

### 2.7 meta-ads-uploader (`skills/meta-ads-uploader/SKILL.md`, 269 lines)
- FACT — Strong safety story, verified in spec: ads forced PAUSED, no budget control, HITL table (lines 146-155), resumable results sidecar. Scripts exist (`scripts/upload.py`, `meta_api.py`, `templates/creative-bundle.json`).
- FACT — Tells the operator twice to use "Meta Ads MCP" (line 47 for campaign/ad-set creation, line 172 for insights) — contradicts the repo's auto-loaded rule that Meta work is `meta` CLI only and no such MCP exists.
- FACT — Env-var split: scripts require `META_ADS_ACCESS_TOKEN` + `META_AD_ACCOUNT_ID` (`scripts/meta_api.py:149-160`); the global `meta` CLI uses `META_ACCESS_TOKEN`. Two token conventions for one platform. JUDGMENT: a fresh session will set one and watch the other fail.
- FACT — Dead agent ref `tracking-specialist` (line 27); related_skill `video-director` (line 22) is now a redirect husk per its own description.
- FACT — Character-limit table (lines 113-117: primary text "max 125") states recommended display-truncation thresholds as hard maxes — Meta accepts far longer primary text. JUDGMENT: mislabeled, will cause agents to over-truncate ad copy.

### 2.8 ad-library-scraper (`skills/ad-library-scraper/SKILL.md`, 198 lines)
- FACT — Claims vs machinery check out: all 5 pipeline scripts exist in `scripts/ad_library/` (plus an undocumented `classify-unclassified.py`); `swipe-files/property-sg/` exists; schemas referenced. HITL gate on stage-analysis is concrete (approve by renaming `.draft.md`, line 139-140).
- FACT — Reads-table cites `skills/transcribe/` (line 169) — no such repo path; transcribe is a global skill. Dead agent ref `attraction-specialist` (line 34). Locked-decisions pointer goes to `~/.claude/plans/started-prancy-origami.md` (outside repo, unverified).
- JUDGMENT — One of the few skills where the "execution recipe" is literally runnable as written (lines 124-141); good pattern.

### 2.9 scrapecreators (`skills/scrapecreators/SKILL.md`, 310 lines)
- FACT — `scripts/scrape.py` + `api.py` exist; endpoint/credit tables are a CLI reference (accuracy vs live API unverified). Setup + typed error handling documented.
- FACT — Dead refs: agent `attraction-specialist` (line 38); related_skill `social-media` (line 35, archived). Its auto-generated Related footer still links `[[social-media]]` even though the freshly regenerated `.claude/skill-graph.json` (10 Jun) contains zero `social-media` entries — footer injection is stale relative to the graph (file mtime 27 May).

### 2.10 knowledge-hygiene (`skills/knowledge-hygiene/SKILL.md`, 169 lines)
- FACT — All 3 scripts exist AND run on default python3. Live output 2026-06-10: freshness → "8 docs overdue (analytics-setup 99d, campaign-playbooks 99d, content-style-guide 99d, usage-guide 99d, brand-guidelines 89d)"; registry drift → "51 issues (43 field mismatches, 8 missing SKILL.md)"; learnings → "16 skills with unintegrated entries (video-director: 20, sales-letter-method: 18, copywriting: 8…)". The anti-decay system works and is reporting heavy decay.
- FACT — Its own refs are decayed: agent `docs-manager` (line 20, deleted), related_skill `amplifier` (line 17, exists nowhere), suggested command `/amplify:skill` (line 137, no such command file).
- JUDGMENT — Irony noted: the hygiene skill flags everything except itself; its wiring into `/ops:weekly` Step 5 can't dispatch to a deleted docs-manager.

### 2.11 verification-loops (`skills/verification-loops/SKILL.md`, 287 lines)
- FACT — Sound pattern (Implement → Review → Resolve, fresh-context reviewer, `general-purpose`+sonnet default, lines 70-77). Scoped NOT-for list (line 53). Dead agent ref: `seo-specialist` (line 26).
- FACT — Carries AgentKits boilerplate "Respond in the same language the user is using" (line 43) — overridden by the repo's always-English rule in routing-overrides; the contradiction lives on in the file.

### 2.12 prompt-contracts (`skills/prompt-contracts/SKILL.md`, 402 lines)
- FACT — Frontmatter agents: `planner`, `project-manager` (lines 29-30) — both deleted. Routing-table maps trigger `high-stakes work` → this skill.
- FACT — Contract library is specified at `clients/<project>/contracts/` (lines 282, 310, 360) — zero clients have a `contracts/` directory (glob returned nothing). JUDGMENT: the library half of the skill (incl. Reverse-mode "save this contract") has never been exercised; spec without practice.

---

## 3. Commands census (`commands/` — `.claude/commands` is a symlink to it)

- FACT — 129 `.md` command files across 33 namespaces. Largest blocks: training/* 24 files (course content, not ops commands), content/* 11, campaign/* 10, seo/* 6, checklist/* 6.
- FACT — Deprecation is invisible in-file: per `.claude/rules/_index.md` "Content → /content:* (deprecated → use /copy:*; EXCEPT /content:email which is still the live email engine)", but NONE of the 11 `commands/content/*.md` files carry any deprecated/redirect marker (grep -i deprecat across content/ + copy/ matched only `commands/project/new.md`, which uses the word in another sense). An agent or user opening `/content:ads` cold sees a fully live-looking command. 10 of 11 are walking dead.
- FACT — Routing-overrides itself says the `/ads:concepts` command reference is dead, "entry is by intent, not a slash command" (260609 note) — consistent: no `commands/ads/concepts.md` exists.
- FACT — Commands referencing missing/archived skills: 8 files instruct activating the `social-media` skill (`commands/content/social.md`, `commands/social/{viral,schedule,engage}.md`, `commands/campaign/calendar.md`, `commands/ops/daily.md`, `commands/checklist/social-daily.md`, `commands/training/start-0-0.md`) — that skill now lives in `skills/_archive/social-media/` and is invisible to the loader.
- FACT — Commands referencing deleted agents: `commands/seo/programmatic.md` (seo-specialist ×3, attraction-specialist ×3), `commands/training/start-1-4.md` (lead-qualifier, email-wizard), `commands/training/start-1-5.md` (seo-specialist ×4).
- FACT — Boilerplate "Respond in the same language the user is using. If Vietnamese, respond in Vietnamese…" persists in command files (e.g. `commands/content/ads.md`), contradicting the standing English-only override (routing-overrides §Copy principle overrides acknowledges this inheritance).
- FACT — `commands/video/` has only `approve/new/resume/status`; `/video:new-concept` (cited by routing-overrides) resolves via the global `video-new-concept` skill, not a command file here. Works, but the override's slash-command phrasing implies a file that doesn't exist in this repo.
- JUDGMENT — Roughly 35-40 of 129 commands are live working surface (ads, campaign, copy, cro, ops, research, project, video); training/* is course material wearing the command namespace; content/* (-email) is deprecated; several checklist/* and crm/* reference the deleted-agent generation. The census number overstates the system by ~3x.

## 4. Agents census (`agents/`)

- FACT — Remaining (8 agent specs + attribution/learnings siblings): brand-voice-guardian, conversion-optimizer, copywriter, eval-halbert, eval-sales-letter, persona-builder, researcher, sales-letter-auditor (standalone, no siblings). Plus `agents/_archive/`.
- FACT — Deleted this cycle (17, per git status `D` entries): attraction-specialist, brainstormer, command-helper, continuity-specialist, docs-manager, email-wizard, lead-qualifier, mcp-manager, planner, project-manager, pseo-architect, sales-enabler, seo-specialist, solopreneur, startup-founder, tracking-specialist, upsell-maximizer.
- FACT — Dangling references to deleted agents remain across ~25 skill files + 3 command files (grep counts, top offenders): content-strategy (planner, attraction-specialist), email-marketing/email-sequence (email-wizard), campaign-runner (5 dead), seo-mastery/schema-markup/programmatic-seo/website-design (seo-specialist, attraction-specialist, tracking-specialist), brand-building/onboarding-strategy-pdf (docs-manager, project-manager), marketing-{psychology,ideas,fundamentals}/problem-solving/content-moat/avatar-research/ad-concept-engine/source-of-truth/linkedin-optimization (brainstormer/planner), analytics-attribution (project-manager).
- FACT — The auto-loaded rule file `.claude/rules/mcp-integrations.md:27` still says "delegate to `mcp-manager` agent" — deleted. This one loads every session.
- FACT — Video-pipeline agents the routing layer depends on (eval-buyer-fit, html-publisher, video-concept-seeder, video-prompt-pack-builder, video-hook-variant-generator, buyer-language-researcher, research-orchestrator) all exist GLOBALLY at `~/.claude/agents/` — the repo's routing-overrides references resolve.
- JUDGMENT — The agent cull was the right call but the reference sweep never happened. Per the repo's own No-Semantic-Search rule, a rename/delete requires grepping all reference classes; ~28 files still point at ghosts, and skill-activation.md tells agents to USE the agents that skills name — so the rot is load-bearing, not cosmetic.

## 5. Hooks, graph, registry run-ability

- FACT — `.claude/hooks/` contains `refresh-registry.js`, `skill-router.sh`, `smart-ctx-guard.sh`; all three wired in `.claude/settings.json` (lines 40, 57, 69). `refresh-registry.js` works — `.claude/rules/routing-table.md` header shows "Generated: 2026-06-10T06:58" (today).
- FACT — `link-skills.py` lives at `scripts/link-skills.py` (NOT `.claude/hooks/`). It hard-exits on missing sklearn (lines 30-35). Verified: `python3 -c "import sklearn"` → ModuleNotFoundError; `python3 scripts/link-skills.py --dry-run` → "Install sklearn: pip3 install scikit-learn" and dies. PATH python3 = homebrew (no sklearn); `/opt/homebrew/bin/python3.12` also lacks it; ONLY `/Library/Frameworks/Python.framework/Versions/3.14/bin/python3` has sklearn. So the documented invocation (`docs/system-rules/skill-graph-rule.md` mandates running it on every skill/agent edit; every SKILL.md footer cites it) fails under the default interpreter — it only runs if you happen to call the python.org 3.14 binary.
- FACT — Despite that, `.claude/skill-graph.json` is FRESH (mtime 10 Jun 01:00; zero SKILL.md files newer than it; deleted skills/agents absent from it; no `social-media` node). Someone/something ran it with the working interpreter. The graph is not stale — the *tooling path* is fragile and undocumented.
- FACT — But the in-file `## Related` footers are not all in sync with the fresh graph: `skills/scrapecreators/SKILL.md` footer still lists `[[social-media]]` (file mtime 27 May) while the 10 Jun graph has no such node — last run either skipped footer injection for unchanged-similarity files or ran `--dry-run` for some. (Mechanism unverified; mismatch verified.)
- FACT — `skills/skills-registry.json` drift is quantified by the repo's own tool: 51 issues, 43 field mismatches, 8 entries whose SKILL.md is missing (knowledge-hygiene `registry_drift.py` run 2026-06-10; the 8 likely map to archived/deleted skills — not enumerated).

## 6. Other scripts worth flagging (siblings hunt)

- FACT — `scripts/` top level is a 35-item mixed bag: live pipeline scripts (ad_concept_sheet_writer, tr_10_5_5_sheet_writer, source_of_truth_sheet_writer, migrate_tracker_to_dct, link-skills), one-off patches (patch_angle_cell, backfill_angle_rationale, backfill-ocr, backfill-transcripts, phase4_acceptance_test), platform pushes (canva_push, create_canva_design, ghost-sync, seed-netlify-blobs), and an `.xlsx` (`Nadia_Marketing_Pitch_Calculator.xlsx`) sitting beside `pitch_calculator.py`. No `scripts/README` or index distinguishes live vs one-shot. JUDGMENT: an agent told to "use the sheet writer" has 4 candidates and the correct one depends on data-shape vintage — this is the #1 navigability gap in scripts/.
- FACT — `scripts/modal/` (cron stack: marketing_metrics.py, meta_puller.py, sheets_writer.py, aggregator.py, config_loader.py) exists and `credentials.json` is present in-tree (service-account key on disk; gitignore status not checked from this seat). JUDGMENT: verify it never reaches the remote.
- FACT — gws/sheet-append surface: `find_or_create_sheet.sh` and `tr_10_5_5_sheet_writer.py` shell out to `gws` CLI; modal scripts use Python google libs; ad_concept/source_of_truth writers use the modal `SheetsWriter` (gspread-style). Three different write stacks for one workbook family. JUDGMENT: consistent with the documented two-identity auth model, but each stack fails differently — worth one reference doc.

## 7. Stage map (infra slice observed by this agent)

1. client-onboarding (scaffold→scrape/interview→validate→activate) — gates: path HITL, checkpoints, readiness+ICM dual verdict.
2. sheets-provisioner (sheet+config provisioning) — gates: HITL confirm, SA-can't-create auth model, idempotent tabs.
3. sheets-updater + scripts/modal (metrics cron) — gates: HITL preview interactive / auto-write cron, protected columns.
4. ad-concept-engine → dct.json assembly → sheet writers (SPLIT: legacy vs TR-hardcoded) — gates: copy 5/5 abort, dry-run default.
5. scripts/ad-images/render.py (image render) — gate: --dry-run approval; tracker mode broken vs dct.json.
6. meta-ads-uploader (publish) — gates: bundle HITL, forced PAUSED, no budgets.
7. ad-library-scraper (industry swipe DB) — gate: stage-analysis HITL rename.
8. knowledge-hygiene (meta) — surfaces in /ops:weekly//ops:monthly; currently reporting 8 stale docs / 51 registry issues / 16 unintegrated-learnings skills.

## 8. Open questions

1. What ran `link-skills.py` on 10 Jun 01:00 — which interpreter/wrapper? The working sklearn lives only in the python.org 3.14 framework install; nothing in-repo documents that dependency.
2. Is the Modal 9am-SGT daily cron actually live for neezanizam/eugene (sheets-provisioner line 110 claims it)? Not verifiable from the repo.
3. Should `tr_10_5_5_sheet_writer.py` be generalized (sheet_id/DCT list from `metrics-config.json`) before the next 10-5-5 wave, or is a per-client fork the intended pattern?
4. Which 8 registry entries point at missing SKILL.md files (registry_drift output) — archived skills or genuine losses?
5. Is `scripts/modal/credentials.json` (service-account key in-tree) gitignored? Not checked; high-priority if not.
6. Are the deleted-agent references scheduled for a sweep (the deletions are uncommitted in git status) — i.e., is this crawl observing mid-refactor state?
