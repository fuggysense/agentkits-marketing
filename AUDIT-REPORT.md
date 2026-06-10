# AUDIT-REPORT — Marketing Machine v2

Date: 2026-06-10 · Auditor: Claude (Fable 5 orchestrator, Opus 4.8 finder/verifier agents) · Scope: full repo, read-only
Evidence discipline: every finding cites file:line and survived an independent adversarial verification pass (one finding was refuted and dropped). Supporting deep-dive reports: `docs/audit-v2-260610/`.
Ferres corpus: `~/corpora/sean-ferres` (read-only library). Distilled references: `_shared-knowledge/ferres/`.

---

## 1. Executive Summary

**Health grade: C.** The machine ships real client work and has pockets of genuinely strong engineering. But it checks structure, not truth, and the factory template stamps its defects into every new client. The operator is the only claim-checker in the system.

**Top 3 risks (plain terms):**

1. **Invented numbers can reach paid ads.** A $214,300 loan balance that exists in no research file was rendered into two approved Eugene creatives. Nothing in the pipeline compares a number in copy or an image prompt against a source. The one citation check that exists is advisory: it flagged a problem and shipped anyway.
2. **The money-path automation is broken, so every wave detours through hand-paste.** The image renderer and the sheet writer both read a data format the pipeline stopped producing. Renders now go prompt-by-prompt by hand and sheet rows are written manually, which silently drops the preview/snapshot safety steps those scripts had.
3. **Operational single points of failure.** A live Google service-account private key sits unencrypted in the synced Obsidian vault. The Meta access token is documented to expire ~2026-06-15. A month of system work is uncommitted, and the four most recent high-stakes handoff notes exist as single copies in gitignored folders. Any one of these going wrong costs days.

**Top 3 opportunities:**

1. **You already invented the fix; it's just not deployed.** The hardened angle gate (code scores against a threshold and refuses to pass weak work) is the strongest pattern in the repo. It guards one stage, as an opt-in nobody documented. Extending "code decides, model judges" to copy claims, image-prompt numerals, and persona quotes closes the biggest risk with a pattern you have already proven.
2. **The Ferres swipe vault can ground your weakest stage.** Image prompts are currently generated from adjectives. The distilled pattern library (49 statics with verbatim copy, layout anatomy, and replication recipes) gives the image stage real winners to model instead.
3. **Fix the template once, fix every future client.** `clients/_template` fails 4 of 7 of its own compliance rules, so each onboarding clones the defects. A compliant template plus a research-completeness gate makes client #12 cheaper than client #11 instead of equally manual.

**Why your ads come out generic or need so much manual catching (one paragraph, no jargon):**
The machine checks structure, not truth. Your research is often rich, but nothing forces a generation step to actually read it: the angle engine's default mode runs on six typed lines, the gated headlines from the angle run get thrown away and regenerated downstream with no gate, and image prompts can invent a loan balance no research file contains. The one hard gate you built is opt-in and undocumented, so on most runs the only gate is you. Meanwhile the render and sheet scripts no longer understand the current data files, so each wave detours through manual steps that drop the few safety checks the scripts had. Generic output is not a model problem. Specificity lives in your research files, and the pipeline does not make anyone use them.

---

## 2. What This Machine Is + Repo Map

A multi-client direct-response marketing factory inside an Obsidian-vault git repo. Flow: onboarding interview → client ICM workspace (`_brand/` holds offer, buyer profile, voice) → avatar research → campaign workspaces → angle generation (big-angle-spotter) → headlines/copy (headline-bank, copywriting OS) → DCT assembly (ad-concept-engine, 10-5-5 method) → image prompts → render (Azure GPT-Image via render.py) → Google Sheet tracking (gws) → paused Meta upload → metrics cron → feedback routing. A sibling video lane (vid-director, AG0/1/2 gates) has the strongest gating architecture in the repo.

Repo top level: `clients/` (11 real clients + `_template`), `skills/` (74 project skills), `commands/` (129 slash commands), `agents/` (8 remaining of 25), `scripts/` (render + sheet writers + hooks), `.claude/` (rules, workflows, references incl. copywriting-os), `docs/`, `learnings/`, `swipe-files/`, plus oddities flagged in findings (root `credentials/`, duplicate `propwise-sg/`, accidental `brain/` chain).

Client compliance scoreboard (validate-icm.sh, 7 rules): harmony-wellness 7/7 · takekine 6/7 · michelle-koh 6/7 · hazecraft 5/7 · neezanizam 5/7 · five un-onboarded folders 4/7 · eugene-chieng 3/7 · `_template` itself 3/7. Caveat: the score rewards empty folders (finding A-02), so read it as a structure check, not a quality ranking.

**What the course covers (from the lecture map):** Sean Ferres' "AI Ads Lab" (25 lectures: 11 video transcripts ~163K words + 18 documents) teaches freelancers to produce winning Meta ads with AI end to end: winning-ad anatomy, research and creation process, a 104-minute live end-to-end demo, statics production at volume, media buying and testing, an 82-creative swipe vault, his master prompt list, plus client acquisition (the "$300 challenge" offer, outreach, objections, contracts) and ad-critique calls that reveal his quality bar in practice.

---

## 3. Audit Report — verified findings, ugly parts first

62 findings kept after adversarial verification (1 refuted, dropped). Sorted within each dimension by severity. FACT = verifier re-read the cited lines; JUDGMENT = interpretation of verified facts.

### Dimension B — Context grounding (can output be traced to research?)

**B-02 · Critical · FACT** — An invented loan balance ($214,300) was rendered into two approved Eugene creatives; one (img-04) presents it as a labeled chart figure with no fiction marker, and the number appears nowhere in any research file.
  - Where: clients/eugene-chieng/campaigns/upgrader-ads/dcts/dct-002-math-blind/dct.json:160; clients/eugene-chieng/campaigns/upgrader-ads/dcts/dct-002-math-blind/dct.json:173; clients/eugene-chieng/campaigns/upgrader-ads/dcts/dct-002-math-blind/images/DCT002-img-04.png.meta.json
  - Consequence: A made-up dollar figure passed the creative gate (all 10 KEEP) and is sitting in finished ad images for a trust-positioned financial advisor. A viewer reads it as a real number. Same fabrication class as the 4,580 stat that WAS caught — but this one shipped uncaught.

**B-03 · Critical · JUDGMENT** — No machine gate anywhere compares a number or claim in copy/image-prompts against a source manifest — claims enter the pipeline at four ungated stages (inputs.json authoring, copy drafting, image-prompt numerals, sheet write).
  - Where: clients/eugene-chieng/campaigns/upgrader-ads/dcts/dct-002-math-blind/wave-1-copy-260610.md:318; clients/eugene-chieng/campaigns/upgrader-ads/dcts/dct-002-math-blind/dct.json:160; skills/image-generation/SKILL.md:143
  - Consequence: This is the mechanism behind B-01 and B-02. The only thing standing between an invented claim and a live ad is whether the drafting agent happens to self-flag and the operator happens to enforce it. The 4,580 catch was luck, not a system.

**B-04 · High · FACT** — No skill, stage, or contract defines 'research complete' — there is no minimum quote/source count below which a generation skill refuses to run; client research richness ranges ~100:1 (takekine 630K words VoC vs takekine's own 5.4K-word brand layer; neezanizam 12K) with the same absent floor for all.
  - Where: skills/source-of-truth/SKILL.md:94; skills/avatar-research/SKILL.md:405; clients/takekine/_brand/funnel-research
  - Consequence: A thin-research client and a research-heavy client flow through identical generation skills with identical (zero) grounding floors. Output quality silently tracks research depth nobody is required to check, so weak campaigns look identical to strong ones until they underperform on spend.

**B-05 · High · FACT** — big-angle-spotter's default mode requires no research files (6 free-text slots, the thinnest grounding on the money path); the fail-closed --hardened mode that enforces a scored grounding gate is never mentioned in the skill's own instructions (grep 'hardened' in SKILL.md = 0).
  - Where: skills/big-angle-spotter/SKILL.md:22; skills/big-angle-spotter/SKILL.md:63; skills/big-angle-spotter/SKILL.md:146
  - Consequence: The angle engine will happily produce ad angles, headlines and image prompts from a one-line persona with zero research on disk. The deterministic grounding gate only fires if the operator remembers an undocumented flag — and the documented launch path at line 63 points at a non-existent directory, so a cold run breaks.

**B-06 · High · FACT** — In the Eugene wave the gated angle-run headlines were all discarded and replaced by freshly generated headline-bank headlines that passed no scored or factual gate — headline-bank has no human review inside the skill.
  - Where: clients/eugene-chieng/campaigns/upgrader-ads/dcts/dct-002-math-blind/wave-1-copy-260610-v2.md:6; clients/eugene-chieng/campaigns/upgrader-ads/dcts/dct-002-math-blind/angle-run-260609; skills/headline-bank/SKILL.md:74
  - Consequence: The four-check factual gate certified headlines that were thrown away; the headlines that actually run reached the creative only via the copy file's self-QA and the operator's eyeball. The one factual checkpoint in the copy lane validates discarded work.

**B-01 · Medium · FACT** — An invented buyer quote ('I want this mental burden off my shoulders') was minted at avatar-creation for neezanizam and has propagated into the LIVE proof-wave ad copy as if it were a real customer's words — it exists in NO research file.
  - Where: clients/neezanizam/_brand/avatars/avatar-1.md:11; clients/neezanizam/campaigns/buyer-funnel/dcts/dct-10-5-5-proof-260603/dct.json:23; clients/neezanizam/campaigns/buyer-funnel/dcts/dct-10-5-5-proof-260603/pipeline-state.json:10
  - Consequence: A fabricated quote is the persuasive anchor of an approved, rendering Meta ad. If a prospect or PropNex compliance ever asks 'who said this,' there is no source — and the agency is running voice-of-customer copy it invented. Every angle built on this phrase is unsourced.
  - Verifier correction: Real but overstated; severity Critical->Medium and one citation wrong. CONFIRMED: 'I want this mental burden off my shoulders' is in avatar-1.md (lines 11 + 272) as Primary/Buying Emotion with NO Evidence:/Source: tag, while sibling claims in the same file (lines 181-182) DO carry r/singaporefi citations — so it is a synthesized, unsourced emotion line. It does not appear verbatim in any neezanizam research file (the only research 'off my shoulders' hit, r13-inherit2.json, is an unrelated aging-parent story). BUT the propagation/consequence claims are materially inflated: in dct-10-5-5-proof-260603/dct.json the quote appears ONLY in /angles[0]/angle_rationale (the strategist's internal reasoning), NOT in any primary_text, headline, or compression_text — verified 0 live-copy hits across all angles. The wave's status is 'draft' and pipeline-state shows phase_3_render in_progress, not live/uploaded. So 'propagated into the LIVE proof-wave ad copy as if it were a real customer's words' and 'persuasive anchor of an approved, rendering Meta ad' are not supported — no Meta viewer would ever see this string. The Critical rubric (unsourced claim reaching paid media) is not met because it never reaches viewer-facing copy. Third citation is wrong: pipeline-state.json:10 is a next_action render note and contains the quote nowhere in the file. Correct what/where: unsourced avatar emotion line that leaked into the angle_rationale (not the ad copy) of a draft wave; where = avatar-1.md:11 + dct.json:23 (angle_rationale). Severity Medium (misleading internal drift, not money-path).

**B-07 · Medium · FACT** — The hardened angle run's citation audit is advisory only — it flagged A01/A03 as citing evidence 'not found verbatim in profile' and did not block; A01 still shipped.
  - Where: clients/eugene-chieng/campaigns/upgrader-ads/dcts/dct-002-math-blind/angle-run-260609/_run.log:13
  - Consequence: The one piece of machinery that could catch ungrounded claims warns and waves it through. It also only checks angle evidence, not copy numerals, so it would never have caught the $214,300. Operators learn to ignore an alarm that never stops anything.

**B-08 · Medium · FACT** — avatar-research back-fills thin external research from the client's own prior buyer-profile.md rather than blocking, and ad-concept-engine offers a 'Legacy mode' escape that lets the whole DCT engine run with no avatar research at all.
  - Where: skills/avatar-research/SKILL.md:405; skills/ad-concept-engine/SKILL.md:250
  - Consequence: Two escape hatches let the pipeline manufacture persona depth from its own earlier output (a feedback loop with no fresh evidence) or skip avatar grounding entirely — both quietly degrade traceability while the pipeline reports success.

### Dimension D — Process, automation and handoffs

**D-01 · Critical · JUDGMENT** — Claims and numbers written into ad copy and creatives pass to the operator's creative-approval gate with no machine check against any source; an unsourced $214,300 reached a shipped Eugene creative.
  - Where: clients/eugene-chieng/campaigns/upgrader-ads/dcts/dct-002-math-blind/angle-run-260609/_run.log:13; clients/eugene-chieng/campaigns/upgrader-ads/dcts/dct-002-math-blind/dct.json:160; clients/eugene-chieng/campaigns/upgrader-ads/dcts/dct-002-math-blind/dct.json:173
  - Consequence: An invented number can ride into paid media on a trust-positioned client's ad; the only guardrail is the operator's eyeball, and the one automated citation check (_run.log:13) is advisory and did not block.
  - Verifier correction: Mechanism CONFIRMED: no machine gate blocks numbers from reaching the creative-approval gate, and _run.log:13 shows the citation audit is explicitly 'advisory' and did not block (it flagged A01/A03 but the wave still PASSed). $214,300 is real in dct.json:159/173 and absent from eugene _brand/. BUT two overstatements: (1) the $214,300 is explicitly framed in the visual_style/provenance as 'illustrative set dressing on an explicitly fictional generic statement' — a fictional bank-statement prop, not a deceptive factual claim about Eugene's results; the overlay headline carries no number. (2) It has NOT 'reached a shipped creative' — dct.json top-level status is 'draft', pipeline is at phase_5_upload with ads created PAUSED and 5 outstanding launch gates; it reached operator-APPROVED, not live paid media. Severity drops from Critical to High: the structural gap (no source-check, advisory-only audit) is real and money-adjacent, but the cited instance is a labeled-fictional prop that has not shipped, so the 'unsourced claim reaches live paid media' Critical bar is not met by this evidence.

**D-02 · High · FACT** — The image-render automation cannot read the current dct.json data shape, so every 10-5-5 ad image is now hand-pasted prompt-by-prompt.
  - Where: scripts/ad-images/render.py:79; scripts/ad-images/render.py:80; scripts/ad-images/render.py:82
  - Consequence: The tool built to end the manual image-prompting grind is dead against today's data; operators feed 10 prompts by hand per wave, which won't scale and reintroduces copy-paste error risk.

**D-03 · High · FACT** — The sheet-writer that pushes ad copy to the client dashboard refuses the new dct.json shape, so the live write is done by hand with no snapshot or preview artifact.
  - Where: scripts/ad_concept_sheet_writer.py:314; scripts/ad_concept_sheet_writer.py:321; clients/eugene-chieng/campaigns/upgrader-ads/dcts/dct-002-math-blind/pipeline-state.json:87
  - Consequence: The HITL snapshot safety designed into the sheet-write step is lost when operators route around it; what landed in the client's live dashboard is unverifiable from the repo.

**D-04 · High · FACT** — The only new-shape sheet writer is hardcoded to one client and campaign (Thomson Reserve), so any other 10-5-5 wave has no working sheet writer at all.
  - Where: scripts/tr_10_5_5_sheet_writer.py:37; scripts/tr_10_5_5_sheet_writer.py:38; scripts/tr_10_5_5_sheet_writer.py:153
  - Consequence: Scaling 10-5-5 to a second client requires either a per-client script fork or another manual write; the generic-looking script silently only serves Thomson.

**D-05 · High · FACT** — Two sheet scripts look for the client config at the old client-root path while every live client moved it to the _brand/ folder, so they error out for exactly the clients they serve.
  - Where: scripts/source_of_truth_sheet_writer.py:79; scripts/patch_angle_cell.py:40; clients/neezanizam/_brand/metrics-config.json
  - Consequence: The AVATARS / source-of-truth sheet writer throws file-not-found for neezanizam and eugene; the fix already exists in a sibling script and was never copied over.

**D-07 · High · FACT** — A month of system-level work is uncommitted (last commit 33 days old, ~520 uncommitted files), and the 4 most recent high-stakes handoff notes live only in gitignored client folders.
  - Where: clients/neezanizam/SESSION-HANDOFF-260609.md; docs/methods/10-5-5/SPEC.md; skills/sheets-provisioner/SKILL.md
  - Consequence: The 10-5-5 spec, the sheets-provisioner skill, the copywriting-OS, and every recent handoff have no git safety net; one bad cleanup loses irreplaceable single-copy work, a pattern that already caused a near-miss.

**D-13 · High · FACT** — The provisioner's --into flag collects every existing tab in the target workbook and queues a delete for all of them.
  - Where: skills/sheets-provisioner/scripts/provision_from_template.py:97; skills/sheets-provisioner/scripts/provision_from_template.py:121
  - Consequence: Pointing --into at an existing populated client workbook wipes all its tabs (including live metrics history) before copying the template in; a one-flag mistake destroys client data.

**D-06 · Medium · FACT** — Three generic multi-client sheet writers all hardcode one client's Google service-account key file.
  - Where: scripts/ad_concept_sheet_writer.py; scripts/source_of_truth_sheet_writer.py; scripts/patch_angle_cell.py
  - Consequence: All multi-client sheet automation rides on neezanizam's GCP identity (scripts/modal/credentials.json client_email = neezanizam@...); the template prescribes per-client accounts, so this is a cross-client data-access coupling waiting to bite.

**D-08 · Medium · FACT** — The allocate helper was fully specced and its guard contract locked, but never built; the next session hand-allocated 44 ad images.
  - Where: clients/neezanizam/SESSION-HANDOFF-260608.md:70; clients/neezanizam/SESSION-HANDOFF-260609.md:9; scripts/ad-images/README.md
  - Consequence: A locked-spec tool that would prevent image-to-test mis-assignment sits unbuilt while operators do its job by hand 44 images at a time, the exact error-prone grind the spec targeted.

**D-09 · Medium · FACT** — Live campaign indexes, the 10-5-5 spec, and the mandated session-memory files all drift because nothing auto-syncs them; eugene's index omits its hottest workspace and the spec contradicts both the migration log and the live sheet.
  - Where: clients/eugene-chieng/campaigns/_campaigns-index.json; docs/methods/10-5-5/SPEC.md:80; docs/methods/10-5-5/migration-log.md:7
  - Consequence: An agent trusting the campaigns index (per the entry contract) misses the near-live upgrader-ads work; the self-declared single-source-of-truth spec is wrong about both phase status and the live sheet layout.

**D-10 · Medium · FACT** — The session-end protocol's three mandated memory files are dead while real continuity travels through ad-hoc handoff files scattered across five locations.
  - Where: docs/system-rules/session-end-protocol.md:14; learnings/session-state.md; docs/changelog.md
  - Consequence: Cross-session memory is split and stale (living files frozen since early May; changelog since March) so a fresh agent gets a misleading picture of project state and may re-do or skip work.
  - Verifier correction: Core CONFIRMED: session-end-protocol mandates session-state.md (step 1), open-threads.md (step 5), changelog.md (step 6); session-state.md and open-threads.md both mtime 4 May (frozen ~early May — accurate). Real continuity travels through scattered SESSION-HANDOFF files in gitignored client folders. CORRECTION to one date: changelog's most recent SECTION header is '## 260424' (April 24, mtime April 24) — the '2026-06-15' string the earlier scan caught is body text (an Opus deprecation TODO), not an entry date. So changelog is stale since late April, NOT 'since March' as the consequence states. Substance (split, stale cross-session memory misleading a fresh agent) holds; Medium sane. Note corrects 'March' to 'late April'.

**D-11 · Medium · FACT** — 52 skill and auto-loaded rule files still name 17 deleted agents, including two rule files that load every single session.
  - Where: .claude/rules/mcp-integrations.md:27; .claude/rules/skill-activation.md:28; skills/campaign-runner/SKILL.md:32
  - Consequence: The skill-activation gate and MCP rule tell agents to dispatch work to agents that no longer exist (mcp-manager, attraction-specialist, planner, etc.), causing failed delegations on routine research/review tasks; knowledge-hygiene's /ops:weekly dispatch points at a deleted docs-manager.
  - Verifier correction: Core CONFIRMED: 17 agents deleted (git ^D: attraction-specialist, brainstormer, command-helper, continuity-specialist, docs-manager, email-wizard, lead-qualifier, mcp-manager, planner, project-manager, pseo-architect, sales-enabler, seo-specialist, solopreneur, startup-founder, tracking-specialist, upsell-maximizer). Cited lines verified: mcp-integrations.md:27 names 'mcp-manager' (auto-loaded rule), skill-activation.md:28 names 'attraction-specialist' (auto-loaded rule), campaign-runner SKILL.md:32 lists planner/email-wizard/attraction-specialist. knowledge-hygiene SKILL.md:20 names 'docs-manager' (sub-claim confirmed). CORRECTION to count: the '52 files' figure is unverified/likely understated-or-imprecise — a broad grep for the 17 names across *.md hit ~192 files, but that count includes prose false positives (e.g. generic 'planner'). The specific cited files are all real; the exact 52 is not reproducible as stated. Medium sane.

**D-12 · Medium · FACT** — The mandated skill-graph linker hard-exits under the default Python interpreter because it needs a library only one non-default interpreter has, and that dependency is undocumented.
  - Where: scripts/link-skills.py:30; scripts/link-skills.py:34; docs/system-rules/skill-graph-rule.md
  - Consequence: A fresh agent following the every-edit mandate runs the command, hits the error, and skips the graph update, so the skill routing graph silently rots on the next skill/agent change.

**D-14 · Low · FACT** — The one daily cron that scans for stalled money-adjacent campaigns is disabled while two clients have live-spend-adjacent pipelines mid-flight.
  - Where: cron-registry.json
  - Consequence: No automated sweep flags a Thomson upload or eugene gate that quietly stalls; detection depends entirely on the single operator remembering to look.

### Dimension A — ICM compliance (structure discipline)

**A-01 · Critical · JUDGMENT** — The only automated ICM check verifies files exist and counts lines, but never checks that factory files (the buyer/claim layer) avoid sourcing from per-run outputs — so it gave neezanizam a passing-grade verdict while an unsourced 'buyer quote' lives in the live ad file.
  - Where: ~/.claude/skills/icm/marketing-scaffold/scripts/validate-icm.sh:52-154; clients/neezanizam/campaigns/buyer-funnel/dcts/dct-10-5-5-proof-260603/dct.json; clients/neezanizam/_brand/source-of-truth.md
  - Consequence: An invented phrase ('I want this mental burden off my shoulders') absent from ALL research inputs but present in 10+ live pipeline artifacts including the proof-wave dct.json passes the compliance gate as if grounded; fabricated buyer language can reach paid Meta creative.

**A-02 · High · FACT** — The validator's pass/fail scale rewards absence: five flat un-onboarded folders with NO CLAUDE.md/CONTEXT.md/_brand score 4/7 'PARTIAL', ranking ABOVE eugene-chieng (a live-revenue client) at 3/7, because empty clients can't trip the broken-pointer or oversized-file rules.
  - Where: /Users/jerel/.claude/jobs/89b7b01b/tmp/phase0/validate-1up-sales-ai.json; /Users/jerel/.claude/jobs/89b7b01b/tmp/phase0/validate-eugene-chieng.json; ~/.claude/skills/icm/marketing-scaffold/scripts/validate-icm.sh:121
  - Consequence: Operator reading the scoreboard concludes un-onboarded skeletons are 'more compliant' than the working client, so remediation effort points at the wrong folders; the score actively misleads triage.
  - Verifier correction: Mechanism fully reproduced: un-onboarded skeletons (aura, propwise-sg, stackworks, fuggysmedia, 1up-sales-ai) score 4/7 PARTIAL while live client eugene-chieng scores 3/7, because empty folders fail only R1-R3 and pass R4/R6 (no oversized files, no broken pointers) whereas eugene's real content trips R4 and R6. Score genuinely inverts triage. Adjustment: 1up-sales-ai is not literally 'flat' — it carries root-level brand .md files (offer.md, icp.md, brand-voice.md) but no _brand/, CLAUDE.md or CONTEXT.md; the other four are flatter. The 'five folders at 4/7' count is correct. Severity High stands.

**A-03 · High · FACT** — The client template itself fails 4 of the 7 rules (CLAUDE.md 197 lines vs 100 cap, no _brand/CONTEXT.md, root CONTEXT.md 127 lines, broken pointers) and ships 7 empty Jake stage folders — every new client is stamped non-compliant and bloated at birth.
  - Where: clients/_template/CLAUDE.md; clients/_template/CONTEXT.md; clients/_template/_brand/
  - Consequence: client-onboarding copies _template, so the 197-line L0, missing _brand contract, and dead 00_inputs..06_measure stages reproduce in every client; the defect is manufactured, not drift, and compounds per onboarding.
  - Verifier correction: Reproduced: _template/CLAUDE.md is 197 lines (>100 cap), no _brand/CONTEXT.md, root CONTEXT.md 127 lines, broken pointers — _template scores 3/7 PARTIAL, and client-onboarding copies it so the defect reproduces per client. Overstatement to correct: the seven 00_inputs..06_measure stage folders are NOT empty/dead — they ship CONTEXT.md scaffold contracts and .gitkeep output dirs (00_inputs has 17 files incl. input-manifest.json + market/product/research subfolders). They are intentional scaffold templates, not dead stages. Drop 'ships 7 empty Jake stage folders / dead 00_inputs..06_measure stages' from the claim; the L0-bloat + missing-_brand-contract + broken-pointer reproduction is the real, confirmed defect. High severity holds.

**A-04 · High · FACT** — A factory (L3) file grounds its product-claim substantiation in per-run product (L4) outputs — the one-way-data-flow rule ICM exists to enforce is violated in the compliance-critical layer, and the validator has no rule to catch it.
  - Where: clients/takekine/_brand/funnel-research/voc/product-claim-context.md:35; clients/takekine/_brand/funnel-research/voc/product-claim-context.md:160; ~/.claude/skills/icm/SKILL.md:53
  - Consequence: The file that decides what medical/performance claims are allowed cites generated concept-input-packets (campaigns/test_2/.../concept-input-packet-*.json) instead of raw research, so an agent can treat a model-invented claim as substantiated when authoring ad copy for a wellness product.

**A-05 · High · FACT** — The 3-section L2 contract (Inputs / Process / Outputs) that ICM calls load-bearing is enforced by NO rule, and is violated by every client including the canonical reference — takekine's _brand/CONTEXT.md has 5 sections, eugene's testimonials CONTEXT.md has 9.
  - Where: ~/.claude/skills/icm/SKILL.md:31-47; clients/takekine/_brand/CONTEXT.md; clients/eugene-chieng/_brand/brand-assets/testimonials/CONTEXT.md
  - Consequence: Agents reading a room contract get an unbounded, free-form doc instead of the binary Inputs/Process/Outputs the spec promises, so 'what do I read, what do I produce, when am I done' is unreliable across the whole pipeline — and the validator reports it all clean.

**A-06 · Medium · FACT** — The validator scans dirs the ICM audit scope itself excludes (_archive/, _template.old/): takekine's sole rule-5 'fail' is a retired 2026-05-21 archive file, and the matched phrase is incidental prose, not a duplicated rule — a false positive dropping a clean client from 7/7 to 6/7.
  - Where: ~/.claude/skills/icm/marketing-scaffold/scripts/validate-icm.sh:91; ~/.claude/skills/icm/marketing-scaffold/scripts/validate-icm.sh:109; /Users/jerel/.claude/jobs/89b7b01b/tmp/phase0/validate-takekine.json
  - Consequence: Operator chases a phantom duplication in dead history; real compliance signal is diluted by noise from folders nobody reads.

**A-07 · Medium · FACT** — The broken-pointer rule mis-resolves layered paths: it strips the numeric prefix off 00_inputs/input-manifest.json (reporting it as _inputs/... 'not found' though the file exists) and flags workspace-relative refs as broken because it only resolves against the anchor file's own directory.
  - Where: ~/.claude/skills/icm/marketing-scaffold/scripts/validate-icm.sh:133; clients/_template/00_inputs/input-manifest.json; clients/_template/CLAUDE.md:44
  - Consequence: R6's broken-pointer list mixes regex artifacts, valid layer-relative refs, and genuine rot with no distinction, so operators can't trust it and learn to ignore the only rule that catches real dead links.

**A-09 · Medium · FACT** — Budgets are checked in lines (CONTEXT.md cap 100), but the ICM spec sets them in tokens (L2 = 200-500 tokens, ~30-70 lines) — the line cap is ~40% looser than the token spec for files loaded on every agent dispatch.
  - Where: ~/.claude/skills/icm/marketing-scaffold/scripts/validate-icm.sh:88; ~/.claude/skills/icm/SKILL.md:24; ~/.claude/skills/icm/SKILL.md:57
  - Consequence: A 100-line CONTEXT.md (~700-1000 tokens) passes while sitting 2x over the L2 token budget; cache bloat the spec is designed to prevent accumulates silently across every session and client.

**A-10 · Medium · FACT** — The template's own no-duplication rule (forbidding 00_inputs/ folders inside campaigns/concept workspaces) is already broken — all 6 takekine concept workspaces carry their own 00_inputs/ — and no rule can detect it.
  - Where: clients/_template/CLAUDE.md:61; clients/takekine/campaigns/test_2/video-concepts/dr-foundation-pilot/00_inputs; clients/takekine/campaigns/test_2/video-concepts/ferritin-in-range-spoken-260528/00_inputs
  - Consequence: Inputs are copied per-workspace instead of selected from one manifest, so the same source material drifts across six locations — the exact duplication-drift ICM is meant to kill, invisible to the gate.

**A-11 · Low · FACT** — Spec/practice/validator terminology diverged: the SKILL.md generic structure names the L3 factory '_shared-knowledge/' (zero clients use it) while the validator hardcodes '_brand/' — the published methodology no longer describes the system it validates.
  - Where: ~/.claude/skills/icm/SKILL.md:154-172; ~/.claude/skills/icm/marketing-scaffold/scripts/validate-icm.sh:73
  - Consequence: An operator or new agent reading the canonical ICM doc to learn the structure is taught a folder name that exists nowhere in the repo, eroding trust in the spec and slowing onboarding.

**A-12 · Low · FACT** — The ICM spec rests on a fabricated-looking academic citation — 'Van Clief & McDermott, In-Context Modeling for Agentic Software, arXiv:2603.16021v2' — with a future (March-2026) arXiv id and a title that differs from the methodology's own name.
  - Where: ~/.claude/skills/icm/SKILL.md:12; ~/.claude/skills/icm/SKILL.md:3
  - Consequence: The foundational doc cites a source that cannot be verified, which undermines the authority of the methodology operators are told to follow and is itself an anti-fabrication-rule violation in the system's own documentation.
  - Verifier correction: The citation exists verbatim (SKILL.md:3 and :12: 'Van Clief & McDermott, In-Context Modeling for Agentic Software, arXiv:2603.16021v2') and is unverifiable — that part stands. But the specific claim 'a future (March-2026) arXiv id' is factually wrong: arXiv YYMM 2603 = March 2026, and today is 2026-06-10, so the id is ~3 months in the PAST, not the future. The note that the paper title differs from the methodology name ('In-Context Modeling' vs 'Interpretable Context Methodology') is accurate. Corrected claim: unverifiable/likely-fabricated citation with a past-dated arXiv id and a title mismatch. Low severity holds.

_Refuted in verification (dropped): A-08 — Three clients sit on three different template generations (eugene = current with empty Jake stages, takekine = ICM-migra... (The load-bearing claim is false. schema_version is NOT 'frozen at 1.0 across all of them and the template' — grep across the four trees returns 0.1 (m)_

### Dimension C — Prompt quality and client leakage

**C-01 · Critical · FACT** — The 'MANDATORY on every static batch' image-quality brief hardcodes Singapore ethnicity (Chinese/Malay/Indian/Eurasian) and SG documents (CPF, HFE) as universal rules, while the operator's own correction note claims the file is client-agnostic.
  - Where: skills/ad-concept-engine/references/high-converting-static-brief.md:4; skills/ad-concept-engine/references/high-converting-static-brief.md:13; skills/ad-concept-engine/references/high-converting-static-brief.md:18
  - Consequence: A non-SG client's ad creatives inherit Singapore-only casting and CPF/HFE document props as hard rules, sending wrong-market imagery toward paid media without the agent or operator noticing.
  - Verifier correction: Evidence real: static-brief.md:4 ('for every client'), :13 (SG ethnicity hardcoded), :18 (CPF/HFE), and SKILL.md:689 marks it 'MANDATORY on every static batch' (cited 691 is within ±5). But two corrections needed. (1) Severity Critical -> High: this is wrong-MARKET casting/document props reaching paid media (a grounding/market-fit defect), not an unsourced/fabricated claim or data-loss, which is what the Critical band reserves. Mitigations exist in-file (line 13 also says 'Match the target avatar's ethnicity to the primary variant') and the sibling gut-wrenching file made the same rule conditional. (2) The 'operator's correction note claims the file is client-agnostic' framing is imprecise: corrections.md:24 says the quality BAR 'Applies globally, not neezanizam-only'; the 'Generic, client-agnostic' phrase is corrections.md:26 about the sheet-writer, not the brief. The contradiction (globally-mandated file with SG-hardcoded casting/doc rules) is genuine in spirit.

**C-02 · High · FACT** — The generic avatar-research web-search prompt hardcodes Singapore property forums (r/singaporefi, HardwareZone EDMW) and property/agent search strings for every persona.
  - Where: skills/avatar-research/SKILL.md:299; skills/avatar-research/SKILL.md:309
  - Consequence: Buyer-voice research for any non-SG, non-property client gets steered to Singapore property subreddits, poisoning the persona dossier that every downstream ad and page is built on.

**C-04 · High · FACT** — headline-bank inverts the headline-to-copy-length mapping between its core prompt and its output-file template: HEADLINE 1 attaches to the ~150-word copy in one place and the ~50-word copy in the other.
  - Where: skills/headline-bank/SKILL.md:158; skills/headline-bank/SKILL.md:168; skills/headline-bank/SKILL.md:206
  - Consequence: Roughly half of runs mislabel which headline locks to which copy length when written to the Meta COPY tab, so the wrong headline can ship paired with the wrong ad text.

**C-06 · High · FACT** — feedback-router declares a required 'meta-ads' MCP integration that does not exist; the repo standard is the meta CLI, not an MCP.
  - Where: skills/feedback-router/SKILL.md:7; skills/feedback-router/SKILL.md:28; skills/feedback-router/SKILL.md:30
  - Consequence: An agent honoring the required dependency halts before the only fail-closed performance-feedback skill can run, stalling the iterate-on-results loop.

**C-07 · High · FACT** — Every NEW/BETTER/MORE route in feedback-router and the next-step suggestions in avatar-research, source-of-truth, and headline-bank point at slash-commands that have no command file (/ads:concepts, /ads:avatars, /test:ab-setup).
  - Where: skills/feedback-router/SKILL.md:125; skills/feedback-router/SKILL.md:130; skills/feedback-router/SKILL.md:206
  - Consequence: The feedback loop and research handoffs end on instructions the operator literally cannot run, dead-ending the pipeline and forcing manual workarounds.
  - Verifier correction: Core finding real and well-evidenced: every cited line points at /ads:concepts or /ads:avatars, and NEITHER has a command file (.claude/commands/ads/ has only feedback, headlines, scrape-advertiser, scrape-library, source-of-truth). Cited feedback-router :125/:130/:206, avatar-research :50/:449, source-of-truth :255/:256, ad-concept-engine :250 all reference the two dead commands. routing-overrides.md itself notes /ads:concepts is a 'dead command reference.' BUT the 'what' wrongly lists /test:ab-setup as nonexistent — .claude/commands/test/ab-setup.md DOES exist, and no cited line references it. Drop /test:ab-setup from the finding; the dead commands are /ads:concepts and /ads:avatars only. Severity High stands for the feedback-loop dead-end.

**C-08 · High · FACT** — meta-ads-uploader reads the token from META_ADS_ACCESS_TOKEN, but the documented repo/global standard variable is META_ACCESS_TOKEN.
  - Where: skills/meta-ads-uploader/scripts/meta_api.py:149; skills/meta-ads-uploader/scripts/meta_api.py:152; skills/meta-ads-uploader/SKILL.md:222
  - Consequence: An operator who set up the documented token variable hits an auth failure at the live-money upload step and cannot publish ads without discovering the undocumented variable name.

**C-03 · Medium · FACT** — The generic Meta-copy generator bakes one client's HDB-flat read-cue ('see the number on your flat') and one client avatar's banned-word contract into its universal Hard Rules.
  - Where: skills/headline-bank/SKILL.md:138; skills/headline-bank/SKILL.md:176
  - Consequence: Ad copy for other clients picks up Singapore-flat phrasing and a different client's tonal restrictions as if they were house rules.

**C-05 · Medium · FACT** — The 9-rule static image standard exists in two files with two owners that have already diverged on the SG-vs-generic ethnicity rule.
  - Where: skills/ad-concept-engine/references/high-converting-static-brief.md:13; skills/image-generation/references/gut-wrenching-ad-format.md:9; skills/image-generation/SKILL.md:133
  - Consequence: A fix to the image standard only lands in one copy; the two creative-quality bars drift apart, and the image-generation SKILL summary still re-leaks 'Singaporean casting' even though its own reference file fixed it.

**C-09 · Medium · FACT** — All five copywriting-foundation skills are unfinished skeletons that cite a nonexistent source file, use legacy flat input paths, have no halt/refuse gate, and admit they contain zero worked examples.
  - Where: skills/persuasive-premise/SKILL.md:38; skills/persuasive-premise/SKILL.md:45; skills/persuasive-premise/SKILL.md:65
  - Consequence: If routed to, these skills generate foundational positioning beliefs from thin or absent research with a dead source citation and no example of good output, looking past wrong (legacy) file paths in the process.

**C-10 · Medium · JUDGMENT** — The most load-bearing angle-generation prompt on the statics path is adjective-driven ('god-tier... gut wrenching... emotion provoking') with structure but zero few-shot examples, and runs from free-text slots with no required research file.
  - Where: ~/AI workflows/big-angle-spotter/scripts/run_pipeline.py:122; ~/AI workflows/big-angle-spotter/scripts/run_pipeline.py:128; skills/ad-concept-engine/SKILL.md:120
  - Consequence: With a thin one-line persona the angle engine produces generic, vibes-based angles because nothing anchors what a winning angle looks like; quality depends entirely on persona richness the prompt never enforces.

**C-11 · Medium · FACT** — The Singapore cultural-sensitivity reference is loaded unconditionally in the ad-concept-engine conductor's standard skill-load set for both static and video batches, for every client.
  - Where: skills/ad-concept-engine/SKILL.md:465; skills/ad-concept-engine/SKILL.md:515; skills/ad-concept-engine/references/sg-cultural-guidelines.md:5
  - Consequence: Every client's DCT wave pulls in Singapore-multiracial guidance as a default context, biasing creative direction toward SG cultural framing regardless of the client's actual market.

**C-12 · Low · FACT** — feedback-router default spend/volume gates are denominated in Singapore dollars (S$200/creative, S$600/batch) and its worked example output is fully NeezaNizam-flavoured, though a per-client override field exists.
  - Where: skills/feedback-router/references/routing-criteria.md:9; skills/feedback-router/SKILL.md:149
  - Consequence: A non-SG client without an explicit threshold override is judged against Singapore-dollar spend gates, so the iterate-vs-wait decision uses the wrong currency and benchmark.

### Dimension E — Hygiene

**E-11 · Critical · FACT** — Root `credentials/` holds a live Google service-account RSA private key plus an OAuth refresh token and client secret, unencrypted on disk in a synced Obsidian vault.
  - Where: credentials/gsheets-service-account.json; credentials/oauth_token.json; .gitignore:113
  - Consequence: Gitignore is the only thing stopping these from being committed; any forced add, backup, or vault copy leaks credentials that mint Google access.

**E-01 · High · FACT** — eugene client law forbids using `_brand/avatars/` for targeting and points to an empty folder instead — but those avatars are the only approved, signed-off targeting avatars for a LIVE campaign.
  - Where: clients/eugene-chieng/CLAUDE.md:76; clients/eugene-chieng/_brand/avatars/avatar-1-cash-anxious-upgrader.md:2; clients/eugene-chieng/_brand/buyer-profile.md:125
  - Consequence: A fresh agent obeying client law refuses the only approved targeting avatars and searches an empty folder, on the money path of a live ad campaign.

**E-09 · High · FACT** — 94 hardcoded `/Users/jerel/...` paths across 31 files; several are executable scripts that crash on any other machine or if the vault folder is renamed.
  - Where: scripts/phase4_acceptance_test.py:22; scripts/build_copyos_reviewers.py:29; scripts/link-skills-watch.sh:13
  - Consequence: These scripts fail for anyone but Jerel and break the moment the vault path moves; the factory is not portable.
  - Verifier correction: All 5 cited script lines exist verbatim with hardcoded /Users/jerel/... paths. But counts are overstated/unreproducible: scripts-only (.py/.sh/.js, excl worktrees) = 6 files/16 occurrences; all file types (excl node_modules/.git/worktrees) = 69 files/172 occurrences. Neither matches '94 across 31 files.' Severity High also overstated for a hygiene dimension — these scripts run fine on Jerel's current machine and only fail on relocation/clone; this is portability hygiene, not currently-broken automation on a money path. Suggest Medium.

**E-13 · High · FACT** — ghost-sync.py declares `swipe-files/<industry>/ads-db.sqlite` as its canonical input, but that sqlite file does not exist anywhere in the repo.
  - Where: scripts/ghost-sync.py:7; scripts/ghost-sync.py:106
  - Consequence: The Ghost/swipe-vault sync is non-runnable as documented; its required input has never existed, so any attempt to populate the swipe encyclopedia errors immediately.

**E-02 · Medium · FACT** — eugene CLAUDE.md routing row advertises '4 micro-personas' in buyer-profile.md, but they were moved out to per-avatar files on 2026-06-01 (active roster is 2 avatars).
  - Where: clients/eugene-chieng/CLAUDE.md:185; clients/eugene-chieng/_brand/buyer-profile.md:125
  - Consequence: Cold agent loads the wrong file for a persona set that no longer lives there and may author against demoted personas.

**E-03 · Medium · FACT** — neezanizam client law says 'One workbook', but metrics-config.json registers three distinct Google Sheets across the client's campaigns.
  - Where: clients/neezanizam/CLAUDE.md:28; clients/neezanizam/_brand/metrics-config.json
  - Consequence: An agent obeying client law writes Thomson/asset-progression metrics against the wrong workbook — data lands in or overwrites the wrong sheet.

**E-04 · Medium · FACT** — All 11 `/content:*` command files carry zero deprecation markers, while the rules index says they are deprecated in favor of `/copy:*`.
  - Where: .claude/rules/_index.md:53; commands/content/social.md:1; commands/content/landing.md:1
  - Consequence: An agent opening the command file directly sees a live command and runs the deprecated path, splitting copy output across two competing engines.
  - Verifier correction: 11 content command files confirmed with zero deprecation markers. But _index.md:53 explicitly EXEMPTS /content:email ('still the live email engine'), so only 10 of the 11 are deprecated-but-unmarked; email.md correctly has no marker. Core issue (deprecated commands open as live) holds for the other 10. Medium fine.

**E-05 · Medium · FACT** — Root `propwise-sg/` and `clients/propwise-sg` are two unrelated trees sharing one name; the client copy is a symlink pointing OUTSIDE the repo entirely.
  - Where: clients/propwise-sg; propwise-sg/CLAUDE.md
  - Consequence: Name collision plus an external symlink that dies on clone/move/backup, silently emptying the client folder; nobody can trust which is canonical.

**E-10 · Medium · FACT** — The canonical ICM skill expands its own acronym two different ways and cites a paper whose title does not match the methodology name (likely a misattributed source).
  - Where: ~/.claude/skills/icm/SKILL.md:6; ~/.claude/skills/icm/SKILL.md:12; ~/.claude/skills/icm/SKILL.md:3
  - Consequence: The foundational architecture skill loaded for every scaffold decision cites a wrong/invented source and contradicts itself, eroding trust in the pattern.

**E-12 · Medium · FACT** — An accidental empty directory chain `brain/jerels brain/Marketing/...` (13 nested dirs, zero files) mirrors the real client tree and is NOT gitignored — created by a path bug that dropped the apostrophe from 'Jerel's brain'.
  - Where: brain/jerels brain/Marketing/clients/stackworks; brain/jerels brain/Marketing/clients/takekine/campaigns/test_2/02_script/output
  - Consequence: A ghost mirror of the client tree that can get committed and misleads anyone exploring the repo into thinking there is a second client tree.

**E-14 · Medium · FACT** — The social-media skill lives only in `skills/_archive/`, yet 9 command files still tell agents to activate it via a path (`.claude/skills/social-media/SKILL.md`) that does not exist.
  - Where: skills/_archive/social-media/SKILL.md; commands/social/engage.md:20; commands/content/social.md
  - Consequence: Nine social/content commands instruct agents to load a dead skill path, so they silently lose their framework or error out.
  - Verifier correction: social-media skill lives only in skills/_archive/; the cited path .claude/skills/social-media/SKILL.md and skills/social-media/ both MISSING — dead path confirmed (engage.md:20 references it). But only 4 command files reference the dead path (content/social.md, social/schedule.md, social/engage.md, checklist/social-daily.md), NOT 9. Count overstated; Medium still fine.

**E-15 · Medium · FACT** — Three copies of skills-registry.json exist; the one all docs tell agents to load is the 3-month-stale 51-skill copy with 8 dead SKILL.md pointers, while the fresh complete 132-skill registry is referenced by nothing.
  - Where: .claude/skills/skills-registry.json; skills/skills-registry.json; .claude/rules/skills-registry.json
  - Consequence: The orchestrator loads a stale catalog missing ~80 current skills and pointing at 7 non-existent ones; skill discovery is silently degraded while a correct registry sits unused.

**E-16 · Medium · FACT** — metrics-config.json sits at `_brand/` for every client except hazecraft, which keeps it at the client root, breaking the convention.
  - Where: clients/hazecraft/metrics-config.json; clients/neezanizam/_brand/metrics-config.json; clients/eugene-chieng/_brand/metrics-config.json
  - Consequence: A script resolving `<client>/_brand/metrics-config.json` finds nothing for hazecraft and either errors or falls back to the wrong sheet config.

**E-06 · Low · FACT** — Two near-identical handoff folders exist (singular `docs/handoff/` and plural `docs/handoffs/`), one file each, nothing reconciles them.
  - Where: docs/handoff/2026-04-24-copywriting-os-phase-1.md; docs/handoffs/metrics-automation-handoff.md
  - Consequence: Handoffs scatter; an agent looking in one folder misses the other.

**E-07 · Low · FACT** — Swipe-file material lives under three competing names: root `_swipe/`, root `swipe-files/`, and 6 per-client `_swipe/` — the sync script reads `swipe-files/` while client work writes `_swipe/`.
  - Where: _swipe/winning-ads; swipe-files/property-sg; scripts/ghost-sync.py:7
  - Consequence: Scripts and agents disagree on where swipe data lives; sync misses client-written swipe material.

**E-08 · Low · FACT** — A neezanizam_DCT3 angle run is duplicated between the client tree and ~/AI workflows with no marker, unlike the managed eugene-hardened duplicate that carries a RELOCATED.md.
  - Where: clients/neezanizam/campaigns/buyer-funnel/angles/_spotter-runs/wave-1/DCT3; clients/eugene-chieng/angles/big-angle-spotter/eugene-hardened-260606/_source.md:1
  - Consequence: Unmanaged duplicate; nobody knows which copy is authoritative or whether edits propagate.
  - Verifier correction: DCT3 duplicated in client tree and ~/AI workflows with no marker — confirmed. But the managed eugene duplicate carries '_source.md' (which states 'Relocated: 2026-06-09'), NOT a 'RELOCATED.md' — no file named RELOCATED.md exists anywhere in the repo. Substance (managed dup has provenance marker, DCT3 has none) is correct; the marker filename in the finding is wrong.

**E-17 · Low · FACT** — Campaign state uses two live file schemas (18 pipeline-state.json vs 1 state.yaml in takekine); the 'plan-state' schema named in docs is referenced nowhere and appears to be a phantom.
  - Where: clients/takekine/campaigns/test_2/state.yaml; clients/eugene-chieng/campaigns/upgrader-ads/dcts/dct-002-math-blind/pipeline-state.json
  - Consequence: takekine's lone state.yaml means any state-reader must handle two formats; agents told to read pipeline-state.json find nothing in takekine's campaign and may misjudge its phase.
  - Verifier correction: Two live schemas confirmed: 1 state.yaml (takekine test_2, phase ag1_review) vs pipeline-state.json elsewhere; eugene dct-002 pipeline-state.json exists; 'plan-state' schema referenced nowhere (phantom confirmed). But pipeline-state.json count is 13 in active trees (excl _archive/_template), not 18. Count overstated; Low correct.

### Strengths — what works and must be protected

**S-01** — CONFIRMED: the hardened angle gate scores angles 1-5 on 5 dimensions and lets CODE (not the model) decide pass/fail against a fixed threshold, fail-closed, with a monotonic regen loop until 5 winners bank.
  - Evidence: /Users/jerel/AI workflows/big-angle-spotter/scripts/run_pipeline.py:791; /Users/jerel/AI workflows/big-angle-spotter/scripts/run_pipeline.py:1197-1210; clients/eugene-chieng/campaigns/upgrader-ads/dcts/dct-002-math-blind/angle-run-260609/_run.log:2-18
  - Protect it by: Only weak ad angles get regenerated and only strong ones reach copy, so the operator stops wasting render and ad spend on angles that do not mirror buyer language. PROTECT: make --hardened the default for client work (it is currently opt-in and undocumented) and promote the advisory citation audit to blocking.

**S-07** — CONFIRMED: Meta ad uploads are forced PAUSED at the code level (not just a config default) - create_ad logs a warning and overrides any non-PAUSED status back to PAUSED, and only a human un-pauses in Ads Manager.
  - Evidence: skills/meta-ads-uploader/scripts/meta_api.py:500; skills/meta-ads-uploader/scripts/meta_api.py:513-515; docs/system-rules/hitl-gates.md:5-6
  - Protect it by: An agent cannot accidentally spend money - every uploaded ad lands paused and waits for a human to enable it. PROTECT: any rebuilt uploader must keep the force-PAUSED-in-the-create-call guarantee, not rely on a default argument.

**S-08** — CONFIRMED (re-verified): every real credential file (service-account keys, OAuth tokens, .env and its backup) is gitignored and untracked; only .example files are committed.
  - Evidence: .env.example; .claude/.env.example
  - Protect it by: Live private keys and tokens sit on disk for the tooling to use but have never leaked into version control. PROTECT: keep credentials/ and scripts/modal/credentials.json in .gitignore; if the rebuild adds CI, add a pre-commit secret scan.

**S-02** — CONFIRMED: the signed-off copy and image prompts land in dct.json byte-for-byte and into renders unchanged - hand-assembly does not corrupt approved text (A02 primary_text verbatim; 10/10 sidecar prompts match dct.json, re-checked programmatically this session).
  - Evidence: clients/eugene-chieng/campaigns/upgrader-ads/dcts/dct-002-math-blind/dct.json:18; clients/eugene-chieng/campaigns/upgrader-ads/dcts/dct-002-math-blind/wave-1-copy-260610-v2.md:38-52; clients/eugene-chieng/campaigns/upgrader-ads/dcts/dct-002-math-blind/images/DCT002-img-08.png.meta.json
  - Protect it by: What the operator approves is exactly what the customer sees in the ad - no silent rewording between sign-off and launch. PROTECT: add an approved-copy-vs-emitted-dct diff gate so a future automated emitter cannot break this fidelity.

**S-03** — CONFIRMED: Eugene persona claims trace verbatim to real client-testimonial transcripts on disk with timestamps - the headline quotes are grounded in what customers actually said, not invented.
  - Evidence: clients/eugene-chieng/_brand/avatars/avatar-2-math-blind-upgrader.md:51; clients/eugene-chieng/_brand/avatars/avatar-2-math-blind-upgrader.md:172; clients/eugene-chieng/_brand/brand-assets/testimonials/transcripts/raw/v10-square2.txt:5
  - Protect it by: Ad voice resonates because it echoes real buyer words, and claims are defensible if questioned. PROTECT: keep raw transcripts in _brand/ with inline timestamp citations, and add a script that verifies every VERBATIM tag resolves to a transcript line.

**S-04** — CONFIRMED: the video lane has a brand-alignment HARD GATE (eval-buyer-fit) that refuses to publish any AG1/AG2 review page unless a PASS verdict file exists, with operator-logged override - enforced at the render layer, defense-in-depth.
  - Evidence: skills/vid-director/SKILL.md:48; .claude/rules/routing-overrides.md:97-102; .claude/rules/routing-overrides.md:30
  - Protect it by: No off-brand or wrong-buyer video concept reaches a client without an explicit machine PASS or a logged human override. PROTECT: port this refuse-to-publish-without-PASS pattern into the statics lane, which currently has no equivalent buyer/claim gate before spend.

**S-05** — CONFIRMED: the sales-letter pipeline runs 5 isolated-context reviewers plus a fresh-eyes ship-gate auditor, with hard-error and FAIL-stops-ship rules - the strongest review stack in the repo and all reviewer files exist.
  - Evidence: skills/sales-letter-method/SKILL.md:82; skills/sales-letter-method/SKILL.md:88-91; skills/sales-letter-method/references/phase-4-preship.md:12
  - Protect it by: Weak or unsafe sales letters cannot ship - multiple independent lenses must clear them first. PROTECT: keep this as the template for every high-stakes deliverable gate. Watch the prompt-template.md 'invent a mechanism if none' line, which invites mechanism-washing thin offers.

**S-12** — DISCOVERED (not on list): the 'code decides, model judges' separation is the deepest reusable primitive - the gate code derives the verdict from numeric scores against a threshold and never trusts the model's self-declared verdict, failing closed on malformed scores.
  - Evidence: /Users/jerel/AI workflows/big-angle-spotter/scripts/run_pipeline.py:283; /Users/jerel/AI workflows/big-angle-spotter/scripts/run_pipeline.py:760-767; /Users/jerel/AI workflows/big-angle-spotter/scripts/run_pipeline.py:375
  - Protect it by: Prevents an LLM from talking itself into a PASS - the safety property the whole grounding story should be built on. PROTECT: apply this primitive to every LLM-grading gate in the rebuild (copy claims, image numerals, buyer-fit) - have code compute pass/fail from the scores, never read the model's verdict.

**S-06** — PARTIAL: the feedback-router's decision logic is genuinely fail-closed (refuses to route below S$200/creative, 7 days, 5000 impressions, returns INSUFFICIENT_DATA) but its plumbing is dead - it reads the retired dct-tracker.json shape and requires a meta-ads MCP that does not exist.
  - Evidence: skills/feedback-router/references/routing-criteria.md:9-19; skills/feedback-router/SKILL.md:28-29; skills/feedback-router/SKILL.md:7
  - Protect it by: The brain that stops the operator from scaling ads on statistical noise is sound, but today it cannot read live data or emit a runnable next step. PROTECT: keep the thresholds verbatim; repoint the data source to dct.json, swap the MCP requirement for the meta CLI, and give it a live route target.

**S-09** — CONFIRMED: every rendered ad image writes a .meta.json sidecar recording engine, style, size, source and the exact prompt - provenance is pervasive (52 sidecars across clients, not a one-off).
  - Evidence: scripts/ad-images/render.py:158-188; clients/neezanizam/campaigns/buyer-funnel/image-prompts/renders/BF11_view-first-vs-check-first_split_malay.png.meta.json; clients/eugene-chieng/campaigns/upgrader-ads/dcts/dct-002-math-blind/images/DCT002-img-06.png.meta.json
  - Protect it by: You can always reconstruct what prompt and engine produced any creative, which is what made the byte-fidelity audit possible. PROTECT: keep the every-render-writes-provenance invariant and extend the same pattern to the copy and sheet stages, which currently leave no record.

**S-10** — CONFIRMED: orchestration runs on explicit phase-state files with documented HITL gates (ad-concept-engine 5 gates, vid-director AG ceremony) and a live ICM structure validator that emits per-rule PASS/FAIL JSON and is honest about failures.
  - Evidence: skills/ad-concept-engine/SKILL.md:234; skills/ad-concept-engine/SKILL.md:276-618; /Users/jerel/.claude/skills/icm/marketing-scaffold/scripts/validate-icm.sh
  - Protect it by: A session can resume mid-pipeline without re-running paid steps, and folder structure conformance is checkable rather than vibes. PROTECT: make phase-gating the default not opt-out (close the ACE Legacy-mode escape hatch) and keep the ICM validator; revive the corrections.md loop repo-wide (only ad-concept-engine's is active).

**S-11** — CONFIRMED: the cold-context fresh-eyes review pattern is independently implemented at three layers - the sales-letter-auditor agent, the verification-loops skill, and the global CLAUDE.md self-review rule - all enforcing reviewer isolation to defeat anchoring bias.
  - Evidence: agents/sales-letter-auditor.md:11; skills/verification-loops/SKILL.md:72; /Users/jerel/.claude/CLAUDE.md:281-290
  - Protect it by: Reviews catch real defects (this pattern caught a wrong-gender testimonial in DCT002) because the reviewer never saw the generation history. PROTECT: keep cold-context review first-class and standardize one JSON return envelope (artifact path in, structured findings out) so every gate reuses it.

**S-14** — DISCOVERED (not on list): where a sheet-writer exists for the current data shape it is properly gated (dry-run default, aborts live write unless all 5 DCTs have 5/5 copy) - but coverage is the gap: the gated writer is hardcoded to one client, so other waves fall back to ungated manual gws writes.
  - Evidence: scripts/tr_10_5_5_sheet_writer.py:37-38; scripts/tr_10_5_5_sheet_writer.py:130-131; skills/meta-ads-uploader/SKILL.md:146-155
  - Protect it by: The safety pattern (refuse incomplete writes, preview before commit) is correct and worth keeping, but every non-thomson 10-5-5 wave today loses snapshot safety to raw manual writes. PROTECT: generalize the gated writer (sheet id and DCT list from metrics-config.json) so the dry-run/completeness gate covers all clients before the next wave.

**S-13** — DISCOVERED (not on list): the system honestly self-declares its own blockers and bypasses rather than silently rotting - open blockers are tracked in-skill, manual workarounds are logged in pipeline-state, and learnings carry an explicit N=1 humility warning.
  - Evidence: skills/ad-concept-engine/SKILL.md:116; clients/eugene-chieng/campaigns/upgrader-ads/dcts/dct-002-math-blind/dct.json:265; skills/ad-concept-engine/learnings.md:3
  - Protect it by: An auditor or fresh agent can trust the system's own notes about where it is broken, which is rare and accelerates safe handoffs. PROTECT: preserve this epistemic-honesty convention (declare blockers, log bypasses, mark priors as priors) as a cultural invariant in the rebuild.


---

## 4. The two pipelines side by side

- **Mine:** `docs/audit-v2-260610/MY-PIPELINE-STAGE-MAP.md` (18 stages, onboarding → session memory, gates marked, undocumented stages flagged)
- **Ferres:** `_shared-knowledge/ferres/ferres-pipeline-stage-map.md` (video path + statics path + media-buying close, "vibe check" marked where he has no gate)

Shape of the difference in one sentence each:
- **My machine is infrastructure-heavy and gate-poor where claims enter**: strong scaffolding, research tooling, state files and provenance, but generation steps don't have to read the research, and nothing machine-checks a claim before it reaches a creative.
- **His process is tooling-light and contract-tight**: three ChatGPT docs and a spreadsheet, but every stage has a named artifact, a "done" definition, and a human read-through before the next stage consumes it — plus a critique rubric built from years of roasting real ads.

## 5. Gap-Analysis Table — ✅ GATE 1 PASSED 2026-06-11 (all 17 rows decided)

Verdict legend: KEEP (mine wins) / ADOPT (his wins) / HYBRIDIZE (designed combination) / ADD (I lack the stage) / DROP (neither, or out of scope). DW = double-win (audit weakness + Ferres mechanism for it). Operator verdicts to be recorded in the rightmost column.

| # | Stage | Mine today | Ferres' version | Recommended | What I gain | What I give up | Conf | Operator verdict |
|---|-------|-----------|------------------|-------------|-------------|----------------|------|------------------|
| 1 | Client intake | 21-q interview → ICM workspace; no proven-assets requirement; template stamps defects (A-03) | Onboarding form REQUIRES winning ad, landing page, offer doc, top-3 competitors before work starts | HYBRIDIZE | Research raw material guaranteed at intake; thin-data detected day 0 | Slightly heavier client ask; needs an "never ran ads" variant | High | ✅ approved as recommended 260611 |
| 2 | Research **DW** | Stronger tooling (research orchestrator, reddit/scrapecreators, provenance dossiers) but NO done-definition; richness varies 100:1 (B-04) | Weaker tooling, stronger contract: 3 named docs, ≥20 verbatim phrases, gap analysis, human read-through, re-run-if-thin, timebox, thin-client fallback | HYBRIDIZE | A research-completeness gate that blocks generation; my channels keep the depth advantage | Nothing real; codifying "done" costs setup time per niche | High | ✅ NOTE 260611: research lives in `~/AI workflows/research-vault/` — completeness gate must read the vault cross-repo, not just client folders |
| 3 | Synthesis | source-of-truth 26 sections + HITL | 3 docs incl. competitor opportunity matrix + says-vs-addresses gap analysis | KEEP + absorb his 2 sections | Sharper differentiation inputs for angles | Minor file growth | Med | ✅ approved as recommended 260611 |
| 4 | Avatars **DW** | Micro-personas + Schwartz mapping + HITL; quotes traceable for eugene, MINTED for neezanizam (B-01) | One named person; every language pattern verbatim-from-source | KEEP + adopt his provenance rule | Fail-closed source pointer on every persona quote kills quote-laundering | Authoring personas gets slower | High | ✅ approved as recommended 260611 |
| 5 | Angles | Hardened scored gate (code decides, 5 dims) — but opt-in, undocumented; default mode ungrounded (B-05) | 50 angles → human top-25; diversity doctrine (mind-map 20-30 buy reasons; TAM-exhaustion diagnosis; 1% remixes don't scale) | KEEP gate + ADOPT his volume/diversity spec; hardened becomes default | More candidate breadth feeding a stronger gate than his | Default runs get slower/costlier (gate + regen loop) | High | ✅ APPROVED 260611 |
| 6 | Hooks **DW** | headline-bank emotional sequence; gated headlines discarded downstream, regen ungated (B-06) | Hook = 80% of effort; does 2 jobs (scroll-stop + algo steering); 25 hooks EACH TAGGED to a research insight; scored selector + human | HYBRIDIZE | Research-insight tag per hook = cheapest traceability win in the whole merge; scored hook gate | Headline-bank's current free-regen convenience | High | ✅ APPROVED 260611 + NOTE: global `script-skill` carries existing hook logic + hooks DB — fold in as input source; keep extension point for future hook sources |
| 7 | Copy body **DW** | copywriting-os deep theory; 5-reviewer chain for LETTERS only; Meta copy has no internal gate | 7-element skeleton; copyboarding (handle objection the moment it forms); proof-is-god; who-it's-NOT-for; even-if qualifiers | KEEP for letters/pages; ADD his rubric as scored pre-launch gate for Meta copy | Copy gate where the audit found none | Nothing — letters keep my stack | High | ✅ approved as recommended 260611 |
| 8 | Image prompts **DW** | Adjective-driven brief (C-10), SG rules leaked into generic (C-01), invented numeral shipped (B-02); strong render executor + sidecars | 5 static formats, teardown→rebuild 3-pass, 25-before-lunch, swipe-grounded; QA gate; route-the-click (native→advertorial) | ADOPT his creative method, KEEP my executor/provenance/HITL + add claim-source gate | Winner-grounded image prompts instead of adjectives; format taxonomy; the 11-pattern library | The "god-tier/gut-wrenching" brief retires; SG rules move to client L3 | High | ✅ APPROVED 260611 + CONDITION: archive current static brief + 9-rule standard as switchable reference, do not delete |
| 9 | Video ads | vid-director AG0/1/2 + eval-buyer-fit hard gate — institutionally stronger | Hook-swap on proven winning body (cheap control-challenge play) | KEEP + add his hook-swap as a cheap variant lane | Low-cost test lane for clients with a winning control | None | Med-High | ✅ approved as recommended 260611 |
| 10 | Pre-launch QA **ADD, DW** | Nothing for Meta ads (operator eyeball) | Critique rubric distilled from his roast calls (hook effort, call-out/disqualify, copyboarding, native feel, compliance) | ADD as scored reviewer gate (my "code decides" pattern × his rubric) | A pre-launch gate where claims currently pass unchecked | Each batch takes one more review cycle | High | ✅ approved as recommended 260611 |
| 11 | Media buying | Largely outside repo (operator/client-side); PAUSED-only upload; no test doctrine on file | Explicit playbook: $25/ad-set ×4, Advantage+ off, 3× TCPR kill, 20-30%/day scale, fatigue triggers, 80/20 batch mix | ADOPT as reference playbook (⚠️PLATFORM-tagged) feeding feedback-router | A written doctrine where there is none | Risk of treating his Meta-2026 numbers as gospel — needs your per-client judgment | **ASK** — who owns media buying per client? | ✅ RESOLVED 260611: Jerel owns media buying → ADOPT at full depth (⚠️PLATFORM-tagged) |
| 12 | Feedback loop | feedback-router fail-closed thresholds (strength) but plumbing dead (S-06) | Weekly vibe-check, 80/20 proven/fresh, comment mining as standing objection feed | KEEP mechanism, fix plumbing (audit), ADD comment-mining input + 80/20 rule | Live objection feed into next batch | None | High | ✅ approved as recommended 260611 |
| 13 | Tracking/metrics | Sheets infra + Modal cron (real automation; writers broken — audit fixes) | Manual Ads Manager checks | KEEP (his loses), fix writers | — | — | High | ✅ approved as recommended 260611 |
| 14 | Client acquisition / $300 challenge | Out of machine scope (advisors handle offers) | Productized foot-in-door challenge offer, outreach, objections, contract | DROP from rebuild; file 08 stays as reference. Optional business idea, your call | — | — | High | ✅ DROP confirmed 260611 |
| 15 | Swipe practice | ad-library-scraper (stronger tooling); sqlite canonical-copy lost (E-13) | Curation filters (30+ days running = proven), standing habit, 80% swipe / 20% original | HYBRIDIZE — my scraper + his curation filters + pattern-naming discipline | Proven-winner filter on what enters the swipe corpus | None | High | ✅ approved as recommended 260611 |
| 16 | Research→copy injection **DW** | Implicit, untraceable (B-03) | Fixed slots: problem section = exact comment language; objection+proof in-line; hooks tagged to insights | ADOPT as prompt-level requirement in headline-bank/ACE | Verbatim VOC with source pointers lands in every ad | Slightly longer prompts | High | ✅ approved as recommended 260611 |
| 17 | Session memory/handoffs | Exists, dead in practice (D-10); Ferres has nothing here | — | KEEP + fix per audit (no Ferres input) | — | — | High | ✅ approved as recommended 260611 |

## 6. Rebuild Plan — ✅ GATE 2 PASSED 2026-06-11 ("go"). Session A (M0+M1) executing.

Standing constraints for every task: external systems are READ-ONLY (sheet/Meta changes tested dry-run only; no live writes without operator); never delete research or client outputs (archive to `_archive/`); Eugene = content-only fixes with per-diff preview, structure frozen; one milestone at a time, git commit per milestone, stop-and-summarize between; smoke test must pass before a milestone counts as done (M2/M3 minimum). Effort: S <1h · M 1–3h · L half-day · XL day+. Blast radius names what the task can touch, from the stakeholder inventory (`docs/audit-v2-260610/D-stakeholders.md`).

### M0 — Safety net

**M0.1 Branch + commit + client snapshot** (M · low risk · deps: none)
Create branch `rebuild-v2`, commit the ~520 uncommitted files (33 days of work) as a baseline commit. Because `clients/*` is gitignored, also tar the full clients tree to `~/marketing-backups/260611-pre-rebuild.tar.gz` (outside repo). Files: git state, backup tarball. Blast: none (snapshot only). Accept: branch exists; `git status` clean; tarball restorable.

**M0.2 Baseline records** (S · low · deps: M0.1)
Re-run validate-icm.sh for all clients into `docs/audit-v2-260610/baseline/`; freeze current findings as the before-picture. Accept: 12 JSON files dated 260611.

**M0.3 Smoke-test client #1 + BASELINE run** (L · low · deps: M0.1)
Build `clients/_smoketest/` (property/finance-flavoured dummy research, realistic volume, zero real client data) and run the pipeline end-to-end: research brief → avatar → angles → copy → image prompts, stopping before any render spend or external write. Save outputs as BASELINE. Blast: none (new folder only). Accept: every stage completes; BASELINE outputs stored under `clients/_smoketest/_baseline/`; a re-run script documents the exact invocation order.

### M1 — Critical fixes (truth + money path)

**M1.1 Claim gate v1 — source-or-cut** (XL · medium · deps: M0.3) ★ top-3 sketch below
Machine gate that extracts every numeral and checkable claim from copy and image prompts in a dct.json and requires a source pointer (research file, client asset, or research-vault path); unsourced → blocks with a plain-language message naming the claim, the file, and what to do. Wires in as: ACE conductor gate precondition + render.py precondition. Files: new `scripts/claim_gate.py`, ad-concept-engine SKILL.md gate section, render.py. Blast: ad pipeline for all clients; no external systems. Accept: Eugene wave artifacts replayed through the gate catch $214,300 and pass the sourced A01 stat; smoke-test wave passes with sourced claims, fails with a planted unsourced number.

**M1.2 Persona-quote provenance** (M · low · deps: none)
Every quote/language-pattern in avatar files gets a `source:` pointer; avatar-research refuses to write quotes without one; validator-v2 rule added later (M3.2). Trace the neezanizam "mental burden" phrase: if no source exists, flag to operator for keep-with-marker or cut decision (it propagates into live pipeline artifacts). Files: avatar-research SKILL.md, neezanizam avatar-1.md (flag only). Blast: neezanizam (live client — flag, don't auto-edit). Accept: new avatars cannot carry unsourced quotes; neezanizam decision recorded.

**M1.3 render.py reads current dct.json** (M · medium · deps: M0.3)
Repoint `--from-tracker` to the `image_pool.images[].image_prompt` shape (keep legacy `creatives[]` fallback behind a flag), fix stale docstring/README paths. Restores scripted renders + their HITL snapshot instead of hand-pasted `--prompt`. Files: scripts/ad-images/render.py, README.md. Blast: render pipeline (Azure pool unchanged). Accept: dry-run against the real Eugene dct.json resolves all 10 prompts byte-identical to the shipped sidecars.

**M1.4 One generic gated sheet writer** (L · medium-high · deps: M0.1)
Generalize tr_10_5_5_sheet_writer.py: sheet_id, DCT list, and credentials read from the client's `_brand/metrics-config.json`; back-port the dual-path metrics-config lookup to source_of_truth_sheet_writer.py + patch_angle_cell.py; per-client service accounts honored (falls back to current SA with a logged warning). Keeps its dry-run default and 5/5-copy completeness gate (strength S-14). Files: 3 scripts. Blast: Google Sheets integration, neezanizam + eugene configs — DRY-RUN TESTING ONLY, no live writes. Accept: dry-run produces correct row preview for both a 10-5-5 and a 3-2-2 wave from the smoke client.

**M1.5 sheets-provisioner --into bug** (S · high if unfixed · deps: none) ⚡quick win
Remove the collect-and-delete-all-existing-tabs behavior; `--into` may only append its own tabs. Files: sheets-provisioner script. Blast: Google Sheets (dry-run test). Accept: `--into` against a fixture workbook leaves pre-existing tabs untouched.

**M1.6 Hardened mode becomes the documented default** (M · low · deps: none)
big-angle-spotter SKILL.md documents `--hardened` and declares it default for client work; fix the dead launch path (SKILL.md:63 points at a script that doesn't exist); citation-audit flag flips from advisory to blocking (B-07). Files: big-angle-spotter SKILL.md + run_pipeline.py (in ~/AI workflows — symlink target). Blast: angle stage, all clients; runs get slower/costlier by design. Accept: default invocation runs gated; ungated requires explicit `--fast` flag; citation-audit failures block.

**M1.7 Eugene content fixes (preview each)** (M · medium — protected client · deps: none) ⚡quick win
Fix CLAUDE.md:76 (avatars/ "legacy" contradiction) and :185 (4 micro-personas → 2 avatars); add upgrader-ads to campaigns/_campaigns-index.json; repair the verified broken pointers. Every diff shown before applying. Files: eugene CLAUDE.md, _campaigns-index.json. Blast: eugene (content only). Accept: validator broken-pointer count for eugene drops; the live wave is discoverable from the index.

**M1.8 Handoff mirror (data-loss stopgap)** (S · low · deps: none) ⚡quick win
Copy the 4 gitignored single-copy handoffs (3 neezanizam + takekine) into tracked `_handoffs/mirror/`; going forward rule lands in M3.6. Accept: `git ls-files` shows them.

**M1.9 Operator-action sheet** (S · — · deps: none)
One page listing what only Jerel can do: move credentials/ key to keychain/encrypted store (E-11), check DCT008 spend status, roster triage for the 5 skeleton clients (onboard/archive), locate shelved school/shame angles. Output: `_handoffs/operator-actions-260611.md`. Accept: file exists; items checked off as done.

### M2 — The merge (approved Gate 1 rows)

**M2.1 Niche-adaptive research-completeness brief** (XL · medium · deps: M1.1) ★ top-3 sketch below
Per-client `_brand/research-brief.md` + machine-readable checklist defining what "research complete" means for THIS client (sources, VOC pools, proof types, compliance constraints), built from the onboarding interview; template ships a builder. The gate script reads BOTH `~/AI workflows/research-vault/` (your storage location) and client folders, enforces a Ferres-style floor (named artifacts, ≥20 verbatim phrases, gap-analysis section, read-through sign-off, re-run-if-thin), and blocks generation skills until met. Includes a working session with you to codify "good enough" for your current niches (open question #6). Files: clients/_template/_brand/, new `scripts/research_gate.py`, generation SKILL.md preconditions. Blast: onboarding + all generation skills; research-vault read-only. Accept: smoke client blocks on thin research, passes on full; gates adapt when the brief differs per niche.

**M2.2 Hook system upgrade** (L · medium · deps: M2.1)
Research-insight tag required per generated hook; scored hook gate (code-decides, threshold like the angle gate); script-skill's hook logic + hooks DB folded in as an input source (per your note), extension point left for future hook sources; headline-bank HEADLINE/COPY mapping contradiction fixed. Files: headline-bank SKILL.md + templates, hook-gate script. Blast: hook/copy stage, all clients. Accept: every hook in output carries `insight:` pointer that resolves; contradiction gone; gate blocks untagged hooks.

**M2.3 Meta-copy pre-launch gate** (L · medium · deps: M2.1)
Ferres critique rubric (`05-quality-bar-critique-rubric.md`) converted to a scored reviewer gate (hook effort, call-out + who-it's-NOT-for, copyboarding objections, native feel, compliance scan) on every ad batch before creative approval; runs cold-context (your existing fresh-eyes pattern). Files: new reviewer reference + ACE gate wiring. Blast: copy stage. Accept: a deliberately weak smoke ad fails with named rubric items; signed-off Eugene copy passes.

**M2.4 Image-prompt stage rebuild** (XL · medium · deps: M1.1, M2.1) ★ top-3 sketch below
The 5-format taxonomy + pattern-library grounding replace the adjective brief: prompts are built by teardown→rebuild against a named pattern (`patterns/statics-pattern-library.md`) or a named format, claim gate runs on prompt text, Ferres QA gate (text legible, on-brand, compliance) added post-render. Current static brief + 9-rule standard move to `_archive/references-pre-ferres/` and stay switchable on request (your condition). SG/CPF rules relocate to `clients/<sg-client>/_brand/locale-rules.md`. Files: ad-concept-engine references, image-generation SKILL.md, client _brand files. Blast: image stage all clients; render executor untouched. Accept: smoke batch produces prompts citing pattern + source for every number; SG rules absent from generic skills (grep clean); old brief retrievable.

**M2.5 VOC injection requirements** (M · low · deps: M2.1)
Generation prompts in headline-bank/ACE require verbatim VOC at fixed slots (problem section = exact customer language, objection+proof in-line), each with source pointer. Files: 2 SKILL.md prompt sections. Accept: smoke outputs quote real dummy-research phrases traceably.

**M2.6 Angle volume/diversity spec** (M · low · deps: M1.6)
Hardened runs consume a diversity map (20–30 mind-mapped buy reasons, awareness/emotion spread) and produce more candidates before the gate; TAM-exhaustion diagnosis note added to feedback-router's BETTER route. Files: big-angle-spotter input spec, feedback-router reference. Accept: gated run banks 5 winners from a measurably wider candidate spread.

**M2.7 Feedback loop repair + media-buying doctrine** (L · medium · deps: M1.4)
feedback-router reads current dct.json + sheet shapes, meta CLI replaces the phantom MCP, dead `/ads:*` routes replaced with live intent-routing entries; comment-mining added as standing objection input; 80/20 proven/fresh batch mix; Ferres media-buying playbook (file 07) becomes the written doctrine (thresholds per-client configurable, ⚠️PLATFORM tags kept) — full depth since you own media buying. Files: feedback-router SKILL.md + references. Blast: feedback stage; Meta read-only. Accept: router runs end-to-end on smoke data and outputs a routing decision citing live commands.

**M2.8 Synthesis absorbs 2 Ferres sections** (S · low) — source-of-truth gains says-vs-addresses gap analysis + competitor opportunity matrix. Accept: sections appear in next smoke run.

**M2.9 Video hook-swap lane** (M · low) — video-concept-lab gains a "new hook on proven winning body" variant lane for clients with a control. Accept: lane documented + producible in smoke video workspace.

**M2.10 Swipe curation + canonical copy** (M · low) — ad-library-scraper adopts proven-winner filters (30+ days running, longest-running sort); resolve the lost ads-db.sqlite: either regenerate from Ghost Postgres or declare Ghost canonical and fix ghost-sync.py docs. Accept: scraper filter flags exist; one canonical store documented.

### M3 — Structure

**M3.1 Template rebuild** (L · medium · deps: M2.1)
`clients/_template/` passes its own validator: L0 ≤100 lines, `_brand/CONTEXT.md` added, root CONTEXT.md ≤100, pointers fixed, research-brief builder included, booking/tracking stubs justified or removed. Files: _template tree. Blast: future clients only. Accept: validator 7/7 on _template.

**M3.2 Validator v2** (L · medium · deps: M3.1)
Content-aware rules: L3-never-references-L4 check, 3-section L2 contract check, persona-quote source check, scoring that no longer rewards absence (un-onboarded ≠ compliant), _archive/_template.old excluded from scans, pointer resolution fixed (no more `00_` prefix stripping), token-denominated budgets. Files: validate-icm.sh (global skill). Blast: all clients' scores will change — re-baseline. Accept: known false positives (takekine R5) gone; known true negatives (takekine L3→L4 violation, neezanizam unsourced quote) now caught.

**M3.3 Canonical state schema** (L · medium · deps: M0.3)
JSON-schema for pipeline-state.json; validation at stage boundaries (fail loud, plain-language message: what's wrong, which file, what to do — never silent repair); takekine state.yaml migrated; edge cases handled per target model (missing files, half-completed stages, older template versions, state-vs-folder disagreement). Files: new schema file + validator hook, takekine campaign state. Accept: planted malformed state halts with helpful message; takekine migrated with zero data loss (yaml archived).

**M3.4 Index/state auto-sync** (M · medium · deps: M3.3)
Script regenerates campaigns-index.json from folder truth + drift report (state vs disk); wired into /ops:daily. Files: new script, ops command. Accept: eugene + thomson indexes regenerate complete; drift report flags the known stale states.

**M3.5 /status capability** (L · low · deps: M3.3, M3.4) 
`/status` reads every client's pipeline-state + folder truth: where each client is, next action, blocked on whom (operator/client/gate). Session-entry orientation line added to root CLAUDE.md (grow the AGENT ENTRY CONTRACT). Files: new command + skill, CLAUDE.md (net-zero line budget honored). Accept: output names eugene/takekine/neezanizam states correctly against disk truth.

**M3.6 Handoff system v2** (M · low · deps: M1.8)
One convention: `_handoffs/` tracked, dated, format from this project's handoffs; session-end protocol rewritten to point at it; docs/handoff + docs/handoffs merged; client SESSION-HANDOFFs mirrored automatically. Files: session-end-protocol.md, _handoffs/, root CLAUDE.md pointer. Accept: protocol names one location; old files migrated with redirects.

**M3.7 Dead-reference sweep** (L · low · deps: none)
52 files naming 17 deleted agents get repointed or cleaned; dead /ads:concepts + /ads:avatars references → live intent-routing entries; meta-ads-MCP mentions → meta CLI; social-media command activations → archive-aware. Grep-verified after (rename discipline: calls, types, strings, re-exports, docs). Files: ~60 across skills/commands/rules. Blast: wide but mechanical. Accept: grep for dead agent names + dead commands returns only _archive + audit docs.

**M3.8 Repeatability proof — smoke client #2** (L · low · deps: M3.1–M3.5)
Onboard a second test client in a deliberately different niche (e-commerce or health) from scratch through `clients/_template/` using only the system. Hard test: zero hand-edits outside its own L3. Then rerun smoke #1 against BASELINE. Accept: both smoke clients complete every stage, every gate fires, no manual patching outside L3 — else the milestone is NOT done.

### M4 — Polish

**M4.1** ICM citation + acronym fix (S) — correct title/source in icm SKILL.md per the actual methodology paper; consistent expansion. **M4.2** Hardcoded-path sweep (M) — ~94 `/Users/jerel` paths in 31 files → repo-relative/env; scripts get a ROOT resolver. **M4.3** Deprecation sweep (M) — in-file markers for 10 /content:* commands; skeleton copywriting-foundation skills: kill-or-finish decision with you; skills-registry.json single fresh source. **M4.4** link-skills.py dependency fix (S) — document/vendor the sklearn interpreter or drop the dependency; register ferres-corpus in the graph. **M4.5** Naming + orphans (M) — docs/handoff(s) merged (done in M3.6), _swipe vs swipe-files decision, propwise-sg canonical decision (with you), `brain/` accidental chain archived, duplicate run markers (neezanizam_DCT3 gets RELOCATED.md treatment; ~/AI workflows originals deleted only with your per-folder OK). **M4.6** metrics-config location convention (S) — hazecraft moves to _brand/, scripts read one path. **M4.7** Re-enable daily campaign-check cron (S) — with you confirming the cadence.

### Quick wins (can run inside M1 week)
M1.5 provisioner bug · M1.7 Eugene stale lines · M1.8 handoff mirror · M4.1 ICM citation · feedback-router dead-command repoint (part of M3.7, 30 min standalone).

### Top-3 implementation sketches

**1. Claim gate (M1.1).** A Python script walks a dct.json (and any copy file): regex + LLM pass extracts numerals, named stats, and checkable claims; each must match a `claims:` ledger entry (claim → source path:line) that the copy/prompt author maintains; the gate greps the source to confirm it exists. Output: PASS, or a table of unsourced claims with "add a source, reword without the number, or cut." Bolted into ACE's existing gate sequence (it already has 5 HITL gates — this becomes the machine precondition before the human creative gate) and into render.py as a refusal. Your "code decides, model judges" pattern, applied to truth.

**2. Research-completeness brief (M2.1).** Onboarding interview produces `_brand/research-brief.md` with a YAML checklist block: required sources (e.g. reddit pools, review sites, competitor list), minimum verbatim-phrase count, required artifacts (ICP/competitor/market or your dossier equivalents), compliance constraints for the niche. `research_gate.py` resolves each item against `~/AI workflows/research-vault/markets/<id>/` and client folders, emits a scorecard, and generation skills call it as a precondition. The Ferres floor is the default template; the per-niche brief overrides it — the gate itself adapts per client, which is the niche-adaptive requirement from the target model.

**3. Image-prompt rebuild (M2.4).** New flow per batch: pick format (from the 5) or pattern (from the 11) → teardown-rebuild 3-pass against the pattern's replication recipe → inject offer/VOC specifics (with sources, claim gate runs on the prompt text) → render via existing render.py + sidecars → Ferres QA gate post-render. The pattern library is the few-shot layer the audit found missing (C-10). Old brief archived switchable; SG rules become client L3 data, loaded only for SG clients.

### Session split proposal
This plan is ~2–3 working sessions of execution: Session A = M0+M1 (safety net + critical fixes + smoke baseline), Session B = M2 (the merge, biggest), Session C = M3+M4 (structure + polish + repeatability proof). Each ends with a milestone commit + handoff + your stop/go.

## 7. Open Questions for the operator

Decisions I cannot make from files. Grouped; answer in any order.

**Client roster**
1. Which of the 11 client folders are active engagements? Five (1up-sales-ai, aura, fuggysmedia, propwise-sg, stackworks) are un-onboarded skeletons — onboard or archive?
2. "Eugene upgrader-ads LIVE": files show pre-upload, blocked on launch gates (client quote permission, letter URL, BM id placeholder). What's the real status, and does the protected zone cover content fixes (stale CLAUDE.md lines) in M1? — ✅ PARTIALLY ANSWERED 260611: content-only fixes allowed in M1, each diff previewed; no moves/renames; campaigns/upgrader-ads/ structure untouched.
3. neezanizam DCT008 composite testimonial: flagged pause/replace in your own ledger — still spending?

**Truth & claims policy**
4. img-04's $214,300 chart figure: acceptable illustrative number, or violation needing a fiction-marker policy? This decision defines the claim-gate spec. — ✅ ANSWERED 260611: **source-or-cut.** Every number/claim traces to a research file or client asset, or it gets cut before render.
5. The "mental burden off my shoulders" persona quote: real-but-undocumented client language, or invented? Is it in live proof-wave copy?
6. What does "good enough research" look like per niche you serve? (Drives the niche-adaptive research-completeness brief — row 2.)

**Mechanics**
7. Should --hardened become big-angle-spotter's default for all client work (slower, costlier, gated)?
8. Which campaign-state schema is canonical: pipeline-state.json (18 uses) or takekine's state.yaml (1)? — ✅ ANSWERED 260611: pipeline-state.json; takekine migrates; schema validation at stage boundaries.
9. Sheet writers: generalize tr_10_5_5_sheet_writer.py to read metrics-config.json, or keep per-client forks?
10. Media buying ownership per client (you vs client) — decides row 11's depth. — ✅ ANSWERED 260611: Jerel owns media buying.
11. propwise-sg: root project vs clients/ symlink — which is canonical; client or internal product?
12. Meta token (expires ~6/15): rotated yet? — ✅ ANSWERED 260611: already replaced.

**Security & hygiene**
13. Root credentials/ holds a live RSA private key in the synced Obsidian vault — move to keychain/encrypted store? (Outside rebuild scope but shouldn't wait.)
14. Handoffs: exempt SESSION-HANDOFF files from clients/* gitignore, or mirror to a tracked path?
15. Deprecation sweep candidates: 10 /content:* commands, 9 commands activating the archived social-media skill, 5 skeleton copywriting-foundation skills — kill, finish, or leave?
16. Shelved school/shame angles (you flagged keep-or-kill in the brief): keep or kill? (Not located in this audit's crawl — point me at the folder if keep.)

---

*Supporting evidence: `docs/audit-v2-260610/` (6 discovery reports, 6 verified dimension reports, stage map). Ferres library: `_shared-knowledge/ferres/` + `skills/ferres-corpus/SKILL.md`. Corpus clone: `~/corpora/sean-ferres` (read-only). All 11 distilled files passed independent citation verification, zero violations.*
