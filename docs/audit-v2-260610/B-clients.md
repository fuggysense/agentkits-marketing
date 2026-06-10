# Phase 1 — Client Crawler Report (eugene-chieng, takekine, neezanizam)

Crawled 2026-06-10 (SGT). Repo root: `/Users/jerel/Documents/Jerel's brain/jerel's brain/Marketing`. All paths relative to repo root unless noted. Read-only audit; no repo files touched. Excluded: `node_modules/`, `.git/`, `.claude/worktrees/`, `clients/_template.old/` (exists, not entered), `clients/_archive/` (exists, contains 1 entry, not entered).

Jargon key: **DCT** = "dynamic creative test," one Meta ad-set batch of images+texts+headlines. **10-5-5** = up to 10 images, 5 primary texts, 5 headlines per ad set. **AG1/AG2** = human approval gates in the video pipeline. **VoC** = voice of customer (real buyer quotes). **ICM** = the repo's folder/context layering convention.

---

## 1. EUGENE CHIENG (`clients/eugene-chieng/`) — richest, LIVE campaign

### 1.1 Tree (3 levels, summarized)

```
eugene-chieng/
├── CLAUDE.md (197 lines)  CONTEXT.md  context-profile.json  DESIGN.md
├── _brand/        (13 files + avatars/ big-ideas/ brand-assets/ visual-characters/)
├── _config/       (client-brief, engagement-terms, scope, WA questions)
├── _references/   (README only)
├── _swipe/        (research/: 3 real files; competitor-reels/: .gitkeep only)
├── _templates/    (concept-pack template, concept-phases/, video-concept-workspace/ + .bak)
├── 00_inputs/     (input-manifest.json, market/, product/, research/, decks/)
├── 01_research/ … 06_measure/   (six numbered stage folders)
├── angles/big-angle-spotter/eugene-hardened-260606/   (gate-hardening R&D run)
├── campaigns/
│   ├── _campaigns-index.json
│   ├── _example-campaign/  (template demo)
│   ├── mp1-upgrader-letter-260603/  (sales letter + funnel page)
│   └── upgrader-ads/dcts/dct-001-cash-anxious + dct-002-math-blind  (10-5-5 wave)
└── output/deliverables/ (.gitkeep only)
```

### 1.2 Numbered stage folders: real vs scaffolding

- FACT: `01_research/` through `06_measure/` each contain ONLY a `CONTEXT.md` plus an empty `output/` (`.gitkeep`) — verified by file listing. All six are **empty scaffolding**; zero work product has ever landed in them.
- FACT: `00_inputs/` is mixed. `00_inputs/research/` holds real inputs (`260601-positioning-call-transcript.md` ≈9,854 words; `onboarding-form-260528.md` ≈947 words). But `00_inputs/product/` and `00_inputs/market/` are near-empty stubs: `product-faq.md` 14 words, `product-features.md` 16 words, `claims-and-proof.md` 20 words, `buyer-language.md` 22 words, `awareness-sophistication.md` 88 words (wc -w).
- JUDGMENT: the actual working dirs are `_brand/`, `_swipe/research/`, `campaigns/`, and `angles/` — the Jake numbered-stage layer is dead weight here.

### 1.3 _brand/ inventory (last-modified via ls -lT)

| File | Modified | Words | Real? |
|---|---|---|---|
| offer.md | 1 Jun | 992 | Real — TREE Method offer, viability scores (offer.md:1-25) |
| buyer-profile.md | 1 Jun | 1,792 | Real but now a **pointer shell** — see 1.5 |
| brand-voice.md | 28 May | 910 | Real, includes 4 verbatim voice quotes |
| icp.md | 28 May | 385 | Real, thin |
| story-bank.md | 1 Jun | 851 | Real |
| idea-bank.md | 5 Jun | 986 | Real, actively appended |
| learnings.md | 28 May | 36 | Stub |
| video-style.md | 28 May | 254 | Thin |
| metrics-config.json | 9 Jun | — | Real, recently touched (live campaign) |
| avatars/avatar-1 + avatar-2 | 9 Jun 23:07 | 38KB/36KB files | Real, deep, refreshed the night before the DCT runs |

- FACT: template `_brand/` has `booking.json` and `tracking.json` (clients/_template/_brand/); eugene's `_brand/` has neither, and adds `big-ideas/` + root `DESIGN.md` which the template lacks.

### 1.4 Persona → research traceability (sampled 3 claims — ALL PASS)

- FACT: avatar-1 cites Derek's ad-fatigue quote "we have seen so many webinars" at `[v01-2nd-couple.txt:60-61]` (_brand/avatars/avatar-1-cash-anxious-upgrader.md:38). Verified: the phrase appears at `_brand/brand-assets/testimonials/transcripts/raw/v01-2nd-couple.txt:60`.
- FACT: Cheryl's "typical middle income Singaporean" quote (avatar-1...md:39) verified at `raw/v01-2nd-couple.txt:42`.
- FACT: fear claim "Lack of confidence to proceed due to fear of financial burden" (avatar-1...md:40, cited to onboarding-form-260528.md:60-61) verified at `00_inputs/research/onboarding-form-260528.md:61`.
- JUDGMENT: Eugene's avatars are the best-evidenced artifacts in the repo — quotes carry file:line anchors to raw transcripts that actually exist on disk. This is the standard the other two clients don't reach.

### 1.5 CLAUDE.md (197 lines, read fully) — the two stale lines, verified

**Line 76 — STALE, contradicts live practice.** Quote (CLAUDE.md:76): "Do not use `_brand/avatars/` as buyer targeting. Use `_brand/visual-characters/` for generated presenters… `_brand/avatars/` is legacy/tooling only."
- Folder reality: `_brand/avatars/` holds the two ACTIVE buyer-targeting avatars (avatar-1-cash-anxious, avatar-2-math-blind, both refreshed 9 Jun), and `_brand/buyer-profile.md:125` states the opposite: "Source of truth for buyer targeting is now the per-avatar files under `avatars/`" (restructured 2026-06-01). The live DCT workspaces are literally named after these avatars (`campaigns/upgrader-ads/dcts/dct-001-cash-anxious/`, `dct-002-math-blind/`). Meanwhile `_brand/visual-characters/` contains only a 399-byte README. Line 76 describes the pre-2026-06-01 world.

**Line 185 — STALE count.** Quote (CLAUDE.md:185): "| Buyer psychology + 4 micro-personas | `_brand/buyer-profile.md` |"
- Folder reality: buyer-profile.md no longer carries 4 micro-personas. Per buyer-profile.md:125+145, "Verbatim micro-persona detail blocks (MP1 / MP2 / MP3 / MP4) were superseded by per-avatar files on 2026-06-01"; MP1 was promoted to avatars, MP2/MP3/MP4 demoted to backlog. Active roster = **2 avatars** (avatar-3 retired by operator 2026-06-01, documented at `_brand/avatars/_index.md:5,20,105`). The "4 micro-personas" label points a cold agent at a count and a file role that no longer exist.

### 1.6 Broken / aspirational pointers in CLAUDE.md

- FACT: `01_strategy/creative-diversity-map.json` (CLAUDE.md:152) — exists NOWHERE under the client (find across whole client: zero hits). The "Simple Concept Generation Route" (CLAUDE.md:146-164) requires it; the route has never been runnable here.
- FACT: `02_ag1-options/concepts-draft.json` (CLAUDE.md:158) — zero hits anywhere.
- FACT: `videos/` (folder-map row, CLAUDE.md:59 "Video Studio … created by /video:new") — directory does not exist (`ls -d videos` → no such dir).
- FACT: `00_inputs/input-manifest.json` (CLAUDE.md:52) — EXISTS at client root, so the validator's `_inputs/input-manifest.json` flag is true only at the *concept-workspace* level: the only concept workspace on disk, `campaigns/_example-campaign/video-concepts/_example-concept/`, has NO `00_inputs/` and NO `eval/` folder (listing shows 01_strategy…07_review only), i.e., it predates the current `_templates/video-concept-workspace/` which has both.
- FACT: eugene has zero real video-concept workspaces — every `video-concepts` pointer in CLAUDE.md (lines 60, 92, 101-164) routes to machinery that has produced nothing for this client. JUDGMENT: ~60 of 197 CLAUDE.md lines are video-pipeline spec for a client whose entire live output is a sales letter + static-image DCT wave.

### 1.7 campaigns/ — state vs folder truth

**`mp1-upgrader-letter-260603` — pipeline-state STALE.**
- Recorded: `sales-letters/main-letter/pipeline-state.json` → `current_phase: phase_3_body_draft`, `last_updated: 2026-06-03`, phase_5_assembly `not_started`, phase_6_ship `blocked`.
- Folder truth: assembled letters exist (`sales-letters/main-letter/_archive/assembled-lead1-v4-clean-260603.md`, `…TRIMMED-260603.md`), a full funnel page was built and reviewed (`funnel-pages/mp1-letter-page/index.html`, `BUILD-REPORT-260604.md`, v2/v3 EDITOR HTMLs), and the page is PUBLISHED — `funnel-pages/mp1-letter-page/.herenow/state.json` lists two live here.now sites (russet-ravine-f6ss, silver-zephyr-83pf). The DCT002 launch gate even says "swap [LETTER_URL] … to the live mp1-letter-page URL" (dct-002 pipeline-state next_action). The state file froze at body-draft 7 days before the crawl while the deliverable shipped around it.

**`upgrader-ads` — no campaign-index.json.** FACT: `campaigns/upgrader-ads/` contains only `dcts/` (ls shows dcts + .DS_Store). CLAUDE.md:79 mandates "Read campaigns/_campaigns-index.json, then campaigns/<campaign>/campaign-index.json" — and `_campaigns-index.json` lists ONLY mp1-upgrader-letter-260603; the live ad campaign `upgrader-ads` is absent from the client's own campaign registry. A cold agent following the prescribed discovery chain cannot find the live wave.

**`dct-001-cash-anxious` — state COHERENT (parked).** pipeline-state.json: `current_phase: PARKED`, angles banked (school/P1-deadline lane shelved — no matching funnel page), A10 angle promoted into DCT002. Folder truth matches: `angle-run-260609/` complete (24 files, 01_angles → 12_image_prompt_rank1-3), no dct.json/images — consistent with parked-after-phase-1.

**`dct-002-math-blind` — state mostly coherent, one internal contradiction + one count gap.**
- FACT: phases 0-4 all `complete/approved`; `current_phase: phase_5_upload` with next_action listing 5 launch gates (URL swap, Derek+Cheryl quote permission, v10 scope confirmation, stat upgrade, Meta Flex limit check). Folder truth supports it: `dct.json` (5 angles A02/A01/A06/A07/A10), `wave-1-copy-260610.md` + `-v2.md`, 10 rendered images `images/DCT002-img-01..10.png` with meta.json sidecars, Canva verify screenshot.
- FACT (internal drift): `phases.phase_5_upload.status` still reads `blocked_until_phase_4` even though phase_4_sheet is `complete` — the per-phase status was not advanced when phase 4 closed.
- FACT (both sides): `images/` holds **10** renders; `dct.json.image_pool` has **len=4**. Unverified whether 4-of-10 selection was a deliberate creative-gate cut or an unfinished allocation.

### 1.8 10-5-5 wave artifact inventory (for the Pipeline Tracer — inventory only)

Per DCT under `campaigns/upgrader-ads/dcts/<dct>/`:
- `angle-run-260609/`: `system_prompt.txt`, `inputs.json`, `_run.log`, `01_angles.{json,md}`, `02_gate_resonance_loop1.json` (dct-002 also loop2), `03_pruned.md`, `04_ranked_angles.md`, `05_gate_top_angle.md`, `06_gate_novelty.md`, `07_expansion.md`, `07b_angle_rationale.md`, `08_headlines.md`, `09_ranked_headlines.md`, `10_gate_four_check.md`, `10b_top_3.json`, `11_ad_prompt_rank1-3.md`, `12_image_prompt_rank1-3.md`, `SUMMARY.md`.
- DCT root: `inputs.json`, `pipeline-state.json`; dct-002 adds `dct.json`, `images/` (10 PNG + meta), `wave-1-copy-260610{,-v2}.md`, `canva-uploads-verify.png`; dct-001 has none of those (parked).
- Hardening R&D (separate from production wave): `angles/big-angle-spotter/eugene-hardened-260606/` — 6 gate JSONs (fresh_loop1-3, ideabank_loop1, killlist_catch, RERUN_loop1), `inputs_used.json`, `THRESHOLD-FINDING.md`, `council-transcript-260607-1935.md`, `FLOWCHART.html`, `verdict-lock-review-260608.html`, `_source.md`, `README.md`. `_source.md:1-9` explicitly labels it "a gate-hardening R&D test, not a production creative run" against DRAFT avatar-1.

### 1.9 Duplicate artifacts: client tree vs ~/AI workflows (ls-only check, as permitted)

- FACT: `~/AI workflows/big-angle-spotter/runs/` contains exactly two runs: `eugene-hardened-260606` and `neezanizam_DCT3_260421-1748`.
- FACT (duplicate pair 1): `clients/eugene-chieng/angles/big-angle-spotter/eugene-hardened-260606/` ↔ `~/AI workflows/big-angle-spotter/runs/eugene-hardened-260606/`. `diff -rq` shows shared files byte-identical; only deltas are `RELOCATED.md` (AI-workflows side) and `_source.md` (client side). RELOCATED.md:1-10 declares the client copy canonical and says the originals "can be deleted … whenever you're ready — left in place because the automated delete needs your OK." Duplication is documented and awaiting operator deletion.
- FACT (duplicate pair 2): `~/AI workflows/big-angle-spotter/runs/neezanizam_DCT3_260421-1748/` mirrors the spotter-step file pattern of `clients/neezanizam/campaigns/buyer-funnel/angles/_spotter-runs/wave-1/DCT3/` (DCT3 system_prompt.txt/inputs.json confirmed present in the client tree). Byte-level diff NOT run for this pair (inventory only) — no RELOCATED.md marker exists on the neezanizam run, so unlike eugene's it is an **unmanaged** duplicate. Unverified which copy is canonical.

---

## 2. TAKEKINE (`clients/takekine/`) — canonical ICM reference

### 2.1 Tree (3 levels, summarized)

```
takekine/
├── CLAUDE.md (71 lines) + CLAUDE.md.bak.20260521-165912  CONTEXT.md  context-profile.json
├── _archive/2026-05-18 (dr-foundation pilot AG1), 2026-05-21 (dormant-campaigns, legacy-phases)
├── _brand/   (14 files + avatars/ big-ideas/ brand-assets/ funnel-research/ visual-characters/; CONTEXT.md in every subfolder)
├── _config/  (+ claude-md-drift-log.md, refresh-claude-map.sh — unique to this client)
├── _swipe/   (winning-ads/: 9 scraped FB ads × {json, md, marketing.v1/v2} + 2 mp4; research/: 3 seed notes)
├── _templates/ (concept-phases/ contracts)
├── analysis.md  analysis2.md   (loose root files)
├── campaigns/test_2/  (state.yaml, STATUS.md, campaign-index/selection, video-concepts/ ×6, video-runs/, _audit/, metrics/)
├── output/{deliverables, publish/takekine}
└── videos/
```

- FACT: NO numbered stage folders (00_inputs..06_measure) at client root. They were archived: `_archive/2026-05-21/legacy-phases/` contains `01_research 02_script 03_production 04_review 05_handoff campaigns migration-log.md`. Takekine migrated off the Jake-stage layout that eugene still carries (empty) — two template generations coexist across clients.
- FACT: every major folder carries a `CONTEXT.md` (ICM L1) — `_brand/`, `_brand/avatars/`, `_swipe/`, `campaigns/`, etc. This matches its "canonical ICM reference" billing.
- FACT: `_config/refresh-claude-map.sh` + `_config/claude-md-drift-log.md` implement an auto-refresh + append-only diff audit for CLAUDE.md (drift-log.md:1-8). No other crawled client has this.

### 2.2 _brand/ inventory

| File | Modified | Words | Real? |
|---|---|---|---|
| funnel.md | 19 May | 2,026 | Real — biggest brand file |
| buyer-profile.md | 21 May | 594 | Thin |
| offer.md | 18 May | 288 | Thin |
| icp.md | 13 May | 312 | Thin |
| brand-voice.md | 28 May | 107 | Stub-grade |
| story-bank.md | 13 May | 251 | Thin |
| learnings.md | 14 May | 78 | Stub |
| funnel-research/ | 15-18 May | ≈630K words total (mostly raw reddit JSON) | Real, huge |

- JUDGMENT: takekine is research-heavy / brand-thin — the inverse of eugene. The structured brand layer (~5.4K words across all .md) is dwarfed ~100:1 by raw VoC.

### 2.3 Persona → research traceability (sampled)

- FACT: `_brand/avatars/avatar-normal-labs-depleted-woman.md` frontmatter declares `status: draft_from_winning_facebook_ad` with `source_seed: ../../_swipe/winning-ads/2026-05-14-ferritin-normal-range-gap-facebook.md` (avatar file lines 1-13) — that seed file exists. Provenance is declared, not line-anchored.
- FACT: the avatar's Primary Fear, "Maybe this is all in my head" (line 28), traces to real VoC: the phrase "all in my head" appears verbatim in `_brand/funnel-research/voc/raw-reddit/1sjepet-flat.md` and `search-all-low-ferritin-normal-hemoglobin-symptoms-flat.md` (grep-verified, e.g., "maybe it wasn't all in my head").
- JUDGMENT: traceable but loosely — no file:line anchors like eugene's avatars; the link is thematic plus a declared seed.

### 2.4 Research richness vs generation output

- FACT inputs: 28 raw reddit files (`_brand/funnel-research/voc/raw-reddit/`, flat-md + raw-json pairs; single largest raw JSON ≈26.5K words), VoC syntheses (`260515-audience-insights-synthesis.md`, `reddit-community-research.md`), sales-letter extract (md+json, 18 May), 9 fully scraped Facebook ads in `_swipe/winning-ads/` (≈29.5K words of swipe analysis incl. marketing.v1/v2 breakdowns), 3 seed notes in `_swipe/research/`.
- FACT generation: one campaign (`test_2`) with SIX video-concept workspaces (dr-foundation-pilot, -singing, -v2, -v2-singing, ferritin-in-range-spoken-260528, three-anchor-slate-260522), each a full 00_inputs..07_review + eval workspace; plus `explorations/`, `render-requests/`, `spine-lift-analysis-260521.md`. Zero shipped ad on disk; everything is pre-AG1/AG2 ideation.

### 2.5 campaigns/test_2 — recorded state vs folder truth (STALE)

- Recorded: `state.yaml` → `phase: ag1_review`, `last_session: "260519"`, `active_output: video-concepts/dr-foundation-pilot`, blockers: "Do not create prompt packs … until AG1 approval" (state.yaml:1-35). `STATUS.md:3` agrees: "Last updated: 2026-05-19".
- Folder truth: TWO later workspaces exist that state.yaml never mentions (grep count of "ferritin-in-range|dr-foundation-pilot-v2" in state.yaml = **0**): `dr-foundation-pilot-v2` (pipeline-state `current_phase: preflight_complete_awaiting_ag0`) and `ferritin-in-range-spoken-260528` (pipeline-state `current_phase: prompts-pending-review` — i.e., prompt packs WERE created despite the standing "do not create prompt packs" blocker recorded at campaign level). The campaign-level state machine stopped updating on 19 May while workspace-level work continued through at least 28 May.
- FACT: takekine also uses a different state stack than eugene (`state.yaml` + `STATUS.md` at campaign level vs eugene/neezanizam's `pipeline-state.json`) — three clients, two-plus state conventions.

### 2.6 Broken pointer in takekine CLAUDE.md

- FACT: CLAUDE.md routing table row "Generate AG1 concepts → `/Users/jerel/.claude/prompts/orchestrators/vid-director.md` § Phase 0" (CLAUDE.md:~19) — that file does NOT exist (ls: missing). It was replaced by the `vid-director` skill at `.claude/skills/vid-director/` (per `.claude/rules/routing-overrides.md` §"vid-director skill auto-load … replaces the legacy ccv system-prompt-file"). The drift-log mechanism guards campaigns-index lines, but this routing row rotted anyway.

---

## 3. NEEZANIZAM (`clients/neezanizam/`) — 10-5-5 DCT conductor client

### 3.1 Tree (3 levels, summarized)

```
neezanizam/
├── CLAUDE.md (114 lines)  CONTEXT.md  context-profile.json
├── _brand/  (14 files + avatars/ ×4 active, brand-assets/, funnel-setup/, source-of-truth.md 83KB)
├── _swipe/  (competitor-ads ×3 raw, headline-banks, hook-library, research/ dossiers + raw/, swipe-files ×3)
├── _salvaged-from-worktree/letter-critic/   (orphaned skill copy)
├── _reorg-dataflow.html  _reorg-spec.md  _research-meta-flex-tracking.md  (loose root files)
├── SESSION-HANDOFF-260608.md / -260609.md / -thomson-sheet-260608.md      (loose root files)
├── campaigns/
│   ├── _campaigns-index.json   _sheet-snapshots/ (24 pre/post-write JSONs)   _TEMPLATE/
│   ├── buyer-funnel/   (dcts ×4 incl. dct-10-5-5-proof-260603; angles/_spotter-runs; landing-pages)
│   ├── asset-progression/ (dcts ×1)
│   └── thomson-reserve/ (DCT101-105 + dcts/pipeline-state.json, 01_reference, 02_creatives, instant-form-questions)
├── meetings/ (thomson kickoff 260530 + transcript)
├── output/{deliverables (onboarding PDF), sales-letters (v1, v1.6, v1.7 + reviews + renders)}
└── website/propnex-listings-widget/ (Cloudflare worker, wrangler.toml)
```

- FACT: no `_config/`, no `_templates/`, no 00_inputs..06_measure anywhere (never had them — no archive of them either; diff vs `_template` confirms). Campaign folders use a DCT-native layout (`_TEMPLATE/{_assets,_drafts,_inbox,angles,avatars,dcts,landing-pages}`) that exists in NO other crawled client and not in `clients/_template/`.

### 3.2 _brand/ inventory

| File | Modified | Size/Words | Real? |
|---|---|---|---|
| source-of-truth.md | 18 Apr | 83KB / 12,556 words | Real — the 26-section master doc |
| buyer-profile.md | 29 May | 21.8KB / 3,264 words | Real |
| offer.md | 12 May | 6KB | Real |
| learnings.md | 28 Apr | 14.8KB | Real, substantial |
| brand-voice.md | 31 May | 2.7KB | Real |
| metrics-config.json | 9 Jun | 20.7KB | Real, live (sheet wiring) |
| avatars/avatar-1..4.md + coverage/sophistication maps | Apr-May | — | Real, 4 active avatars |
| icp.md / channels.json / asset-map.md | 6 Apr | small | Original onboarding vintage, not refreshed |

### 3.3 Persona → research traceability (sampled 2 — ONE FAILS)

- PASS: avatar-1 behavior quote "my own calc but still scared lah" traces upstream to `_brand/source-of-truth.md` (grep hit) and is listed in `_swipe/swipe-file.md:203` under "Language to Borrow (Audience's Own Words)". Second-hand (source-of-truth is itself a synthesis) but a research-side origin exists.
- **FAIL:** avatar-1's Primary Emotion quote — "I want this mental burden off my shoulders" (`_brand/avatars/avatar-1.md:11`) — appears NOWHERE in any research input. Case-insensitive grep for "mental burden" across `_swipe/research/` (incl. raw reddit JSONs) and `source-of-truth.md`: zero hits. It appears ONLY in the avatar file and its DOWNSTREAM generated artifacts: `campaigns/buyer-funnel/dcts/dct-10-5-5-proof-260603/dct.json`, `dct-tracker.json`, `campaigns/buyer-funnel/angles/_spotter-runs/wave-1/DCT1/system_prompt.txt` + `inputs.json`, `campaigns/dashboard.html`. JUDGMENT: an invented VoC phrase was minted at avatar-generation time and has propagated through the live ad pipeline as if it were buyer language — exactly the fabrication-laundering pattern the repo's DATA RELIABILITY rule exists to prevent.

### 3.4 Research richness vs generation output

- FACT inputs: `_swipe/research/` dossiers ≈12.2K words (buyer-language 2,835; malay-first-buyer 3,694; life-transition 5,701) + `raw/` reddit comment JSONs (10+ files, 260417-18) + 3 competitor-ad raw scrapes + source-of-truth.md 12.5K words.
- FACT generation: 83 files under `campaigns/*/angles/` (spotter runs), 83 files under `campaigns/*/dcts/`, sales letters v1→v1.7 (≈8.4K words incl. reviews/plan), headline banks, hook library, landing pages, thomson 02_creatives (gpt-image-2 + sales-letter mockups), 24 sheet snapshots. JUDGMENT: generation output comfortably exceeds research input in file count and is fed largely through the source-of-truth synthesis rather than raw VoC.

### 3.5 campaigns/ — state vs folder truth

- **`_campaigns-index.json` STALE/incomplete.** FACT: created 2026-06-03, self-described as "Generated 260603 from on-disk dct-tracker.json scan (was MISSING before)" (file line 6). It lists 6 entries — all buyer-funnel/asset-progression DCTs. `thomson-reserve` (kickoff meeting 260530, DCTs built per `dcts/pipeline-state.json` key `built_260609`) is ABSENT (grep "thomson" in index = 0). Likely cause: thomson uses `pipeline-state.json`/`dct.json`, not the `dct-tracker.json` the scan keyed on. Both sides: index purpose says "Discover campaign trackers here instead of guessing paths" — but the newest, most active campaign is undiscoverable through it.
- **`dct-10-5-5-proof-260603` COHERENT.** pipeline-state: `current_phase: phase_3_render, in_progress, last_updated 2026-06-08`. Folder truth matches partial render: `images/DCT010-img-01.png` (1 of pool), `image-prompts/renders/DCT010-A01-v1{,-chumbox}.png` + meta. Also present: `dct.json` (migrated; `dct.json.pre-migrate-260608.bak` + `dct.migration-report.json` document the tracker→dct migration), `review-findings.md`, `_preview.html`. Note tension: MEMORY says "proof wave LIVE in NeezaNizam test tabs" — sheet write happened to TEST tabs (index note), but pipeline-state still shows phase_4_sheet blocked; sheet snapshots `260603-1746-{pre,post}-ad-concept-write-dct-10-5-5-proof-260603.json` prove a sheet write DID occur 260603 before the state file's phase model says so. Unverified which is authoritative.
- **`thomson-reserve` BLOCKED, state coherent.** `dcts/pipeline-state.json` next_action: "HARD BLOCKER (operator-only): complete Singapore advertiser verification in Meta Business Settings … error_subcode 3858548". DCT101-105 each hold `copy.md`, `dct.json`, `images/`. Uses yet another state schema (keys: phase, upload_plan, meta, naming_conventions, dcts, done — no `phases{}` map, no last_updated).
- FACT: `campaigns/_sheet-snapshots/` (24 pre/post JSONs, Apr-Jun) is a write-audit trail unique to this client.

---

## 4. Cross-client structural comparison

| Dimension | eugene-chieng | takekine | neezanizam | _template (current) |
|---|---|---|---|---|
| Numbered stages 00-06 | Present, ALL EMPTY | Archived 2026-05-21 | Never existed | Present |
| CLAUDE.md lines | 197 (matches template's 197-line skeleton; ~150 diff lines of customization) | 71 ("Layer 0 Map" style) + auto-refresh script | 114 | 197 |
| Campaign state file | pipeline-state.json (per workspace/DCT) | state.yaml + STATUS.md (campaign) + pipeline-state.json (workspace) | pipeline-state.json, 2 schemas (DCT vs thomson) + dct-tracker legacy | pipeline-state.json |
| Campaign layout | `<campaign>/<artifact-family>/<slug>` + `dcts/` | `test_2/video-concepts/<slug>` | `_TEMPLATE/{_assets,_drafts,_inbox,angles,avatars,dcts,landing-pages}` | `_example-campaign/video-concepts` |
| _brand extras vs template | +big-ideas/, +DESIGN.md; −booking.json, −tracking.json | +funnel.md, +funnel-research/, +CONTEXT.md per folder; −idea-bank.md | +source-of-truth.md, +funnel-setup/, +notebooklm.json; −idea-bank, −video-style…; | booking.json + tracking.json exist ONLY in template |
| Avatar evidence style | file:line anchors to raw transcripts (best) | declared seed + thematic VoC link | mixed; 1 sampled quote unsourced (worst) | template stub |
| schema_version stamps | "1.0" everywhere sampled | n/a (yaml) | "1.0" | "1.0" (6 files) |

- JUDGMENT: these are three different template generations living side by side. Eugene = current `_template` vintage (May 28) with dead Jake stages; takekine = ICM-migrated (May 21 migration, archived stages, CONTEXT.md everywhere, drift-log tooling); neezanizam = oldest (Apr 6 onboarding), fully custom DCT-native layout that the shared `_template` has never absorbed. Per-client conventions (sheet-snapshots, drift-log, `_TEMPLATE` campaign scaffold, `angles/` client-root folder) have NOT been back-ported to `clients/_template/` — each client is a fork, not an instance.
- FACT: schema_version is frozen at "1.0" across all three clients and the template — version stamps don't distinguish the generations; only folder shape does.

## 5. Consolidated stale-state ledger (recorded vs real)

1. eugene mp1 letter: state says `phase_3_body_draft` (2026-06-03) — disk shows assembled v4 letter, BUILD-REPORT-260604, 2 published here.now URLs.
2. eugene CLAUDE.md:76 "avatars/ is legacy/tooling only" — avatars/ is the declared source of truth for targeting (buyer-profile.md:125) and powers the live wave.
3. eugene CLAUDE.md:185 "4 micro-personas" — actual: 2 active avatars, MP-blocks superseded 2026-06-01.
4. eugene `campaigns/_campaigns-index.json` omits live `upgrader-ads`; `upgrader-ads/` lacks campaign-index.json entirely.
5. eugene dct-002: `current_phase: phase_5_upload` while `phases.phase_5_upload.status = blocked_until_phase_4` though phase 4 is complete.
6. takekine test_2 state.yaml frozen at 260519/AG1-pending — ferritin workspace reached `prompts-pending-review` (28 May) violating the recorded "no prompt packs until AG1" blocker; v2 workspaces unreferenced.
7. takekine CLAUDE.md routes AG1 generation to deleted `~/.claude/prompts/orchestrators/vid-director.md`.
8. neezanizam `_campaigns-index.json` (260603) missing thomson-reserve (built 260609; kickoff 260530).
9. neezanizam dct-10-5-5-proof: sheet write to TEST tabs evidenced by 260603 snapshots while phase model still shows phase_4_sheet blocked.

## 6. Open questions

1. dct-002 image_pool len=4 vs 10 renders on disk — deliberate creative-gate selection or unfinished allocation? (operator knows)
2. Is the neezanizam "mental burden off my shoulders" phrase from an un-captured call/meeting (i.e., real but undocumented), or invented? If invented, does it survive in the LIVE proof-wave copy?
3. Who owns deleting the `~/AI workflows/big-angle-spotter/runs/eugene-hardened-260606` duplicate (RELOCATED.md says delete needs operator OK), and should `neezanizam_DCT3_260421-1748` get the same relocation treatment?
4. Should eugene's empty 01_research..06_measure stages be archived takekine-style, or does some automation still expect them?
5. Which state schema is canonical going forward — eugene's phased pipeline-state.json, takekine's state.yaml, or thomson's flat plan-state? Three conventions guarantee future stale-state findings.
6. Why does `clients/_template/_brand/` carry booking.json/tracking.json that no real client has — dead template features?
