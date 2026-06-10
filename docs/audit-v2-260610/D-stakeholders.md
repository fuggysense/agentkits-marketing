# Phase 1-D — Stakeholder & Dependency Inventory
_Audit agent D · 2026-06-10 (SGT) · Repo: /Users/jerel/Documents/Jerel's brain/jerel's brain/Marketing_
_All paths relative to repo root. FACT = read from file. JUDGMENT = interpretation. Plain-marketer translations inline._

---

## 1. Executive summary

The repo is a single-operator (Jerel) direct-response agency system. One client — **neezanizam** — has full
end-to-end live wiring (Meta ad account, 4 Google Sheets, a cloud cron that writes metrics daily). One client —
**eugene-chieng** — is in active build with a Meta upload pending behind operator/client gates. Everything else is
idle, paused, or pre-campaign. The two most fragile external dependencies found:

1. **Meta access token expiry ~2026-06-15** (5 days from audit date) — `docs/handoffs/metrics-automation-handoff.md:21`
   says the long-lived token saved as `META_ADS_ACCESS_TOKEN` expires ~2026-06-15. If true and unrenewed, the Modal
   metrics cron and all `meta` CLI work stop. (The repo `.env` was re-saved 7 Jun — token may have been rotated;
   unverified, no network calls allowed.)
2. **The "generic" sheet-writer scripts are hard-wired to neezanizam's service account** —
   `scripts/ad_concept_sheet_writer.py:87` and `scripts/source_of_truth_sheet_writer.py:59` both point at
   `scripts/modal/credentials.json`, whose `client_email` is `neezanizam@neezanizam-492212.iam.gserviceaccount.com`
   (verified by reading the JSON key name only). Multi-client tooling rides on one client's GCP identity.

---

## 2. External integrations census

### 2.1 Google Sheets (via `gws` CLI + gspread service accounts)

**Identity model** (FACT, `clients/_template/_brand/metrics-config.json:15-24`): human OAuth `jerel@genflos.com`
via `gws` *creates + shares* sheets; a per-client *service account* writes rows at runtime (cron). A bare service
account cannot create Sheets.

| Sheet ID | Client / purpose | Evidence |
|---|---|---|
| `14bh8k6S-krbg0I69JgO2e7eP-YkS6_NMC7XN2NTNKSE` | neezanizam buyer-funnel workbook (also hosts 10-5-5 TEST tabs) | `clients/neezanizam/_brand/metrics-config.json:18,680` |
| `1D-HrqZHUzvQVmnYO4hR3f9rnznnIprz0CZu8hmUO610` | neezanizam asset-progression workbook | `clients/neezanizam/_brand/metrics-config.json:343` |
| `1KqWJP08h8BPr8ygH1ADnmrDPuGaH3p7v4O3WS6WoAtM` | neezanizam thomson-reserve-buyers (CREATIVES gid 517682187, COPY gid 1419950717) | `metrics-config.json:709`; `clients/neezanizam/SESSION-HANDOFF-260609.md:11` |
| `1SDLzn4ceWoLUoWEagrmPFtWA7ZlTZAV_ShRqrD557mw` | eugene-chieng upgrader-ads campaign sheet | `clients/eugene-chieng/_brand/metrics-config.json:220` |

- **Reads:** Modal cron (`scripts/modal/marketing_metrics.py`) reads each client's `metrics-config.json` to know
  which sheet/tabs to update; sheets-updater skill; operator + client humans read the dashboards.
- **Writes:** Modal cron functions `daily_metrics` / `weekly_aggregation` / `monthly_aggregation`
  (`scripts/modal/marketing_metrics.py:1-12`); repo writers `scripts/tr_10_5_5_sheet_writer.py`,
  `scripts/ad_concept_sheet_writer.py`, `scripts/source_of_truth_sheet_writer.py` (all via
  `scripts/modal/credentials.json` SA — see §1 item 2).
- **Client dependency:** neezanizam (4 live workbooks), eugene-chieng (1). harmony-wellness/takekine configs are
  all `{{placeholder}}`/null (FACT — their `metrics-config.json` files).
- **If disconnected (marketer terms):** the client-facing performance dashboards stop updating. Founders looking at
  "DAILY CALLS" see stale rows; appointment/revenue tracking goes manual.

### 2.2 Meta Ads (via `meta` CLI — explicitly NOT an MCP)

- **Rule:** `.claude/rules/mcp-integrations.md:29` — all Meta work through `~/.local/bin/meta`; read verbs safe,
  create/update/delete are live + billable and need confirmation.
- **Known ad accounts** (FACT, same line): NND@Propnex `act_837789749619954` (biz `837781629620766`) → neezanizam;
  Fuggy's Media #1 `act_936198302709669` (biz `2334231630425342`) → the agency's own account. Only
  `act_837789749619954` appears in client configs/trackers (40+ hits, e.g. `clients/neezanizam/CLAUDE.md:14`,
  every `dct-tracker.json`). Eugene's Meta account is still `{{META_AD_ACCOUNT_ID}}` placeholder
  (`clients/eugene-chieng/_brand/metrics-config.json:22`) — his BM ID is "not yet delivered"
  (`metrics-config.json:12` service_account note).
- **Reads:** Modal cron `meta_puller.py` (insights → sheets); ad-library scrapes (`scripts/ingest-advertiser.py`,
  `/ads:scrape-library`).
- **Writes:** `skills/meta-ads-uploader/scripts/upload.py` creates campaigns/ad sets/ads (PAUSED) — runbook at
  `clients/neezanizam/campaigns/thomson-reserve/dcts/_UPLOAD-RUNBOOK.md:27-35`.
- **Token:** `META_ADS_ACCESS_TOKEN` + `META_APP_ID`/`META_APP_SECRET` in repo `.env` (names verified, values not
  read). Expiry risk in §1.
- **If disconnected:** no live spend data (dashboards freeze), no ad uploads, no competitor ad-library refreshes.
  Neezanizam's active spend continues unmonitored by this system — Meta itself keeps running the ads.

### 2.3 Modal.com (cloud cron host)

- FACT: deployed app `marketing-metrics` in workspace `fuggysense`, 4 functions, deploy URL
  modal.com/apps/fuggysense/... (`docs/handoffs/metrics-automation-handoff.md:46-50`). Secrets `meta-ads` and
  `google-sheets` stored *in Modal*, mirrored from `.env` + `scripts/modal/credentials.json`.
- **If disconnected:** daily/weekly/monthly metric rows stop appearing in client sheets. Silent failure mode —
  nothing in the repo alerts on a missed cron run (JUDGMENT; no alerting config found).

### 2.4 Azure GPT-Image-2 render pool

- FACT: the executor lives OUTSIDE the repo at `~/.claude/scripts/gpt-image-2`; the repo's
  `scripts/ad-images/render.py:37` shells out to it (`GPT_IMAGE_2 = Path.home()/".claude"/"scripts"/"gpt-image-2"`).
  Engine registry `ENGINES` at `render.py:59` has `gpt-image-2` as default; `higgsfield` engine is a commented-out
  stub (`render.py:62`). `AZURE_*` keys live in `~/.claude/.env`, not in this repo (FACT — no AZURE_ vars in repo
  `.env` name list).
- **Reads/writes:** big-angle-spotter / ad-concept pipelines call render.py to produce static ad images (e.g.
  eugene DCT002 `images/` folder).
- **Client dependency:** eugene-chieng (DCT images rendered 260609-10), neezanizam (Thomson Reserve 44 images).
- **If disconnected:** no new static ad creatives — copy can still be written but image batches stall, so DCT waves
  can't ship.

### 2.5 Ghost Postgres (swipe-file / ad-intel database)

- FACT: `scripts/ghost-sync.py` pushes `swipe-files/<industry>/ads-db.sqlite` → Ghost Postgres
  (`GHOST_DATABASE_URL` in `.env`); `scripts/sync-ghost-to-swipefiles.py` mirrors Postgres → `swipe-files/`
  filesystem ("One-way pull", header lines 1-16).
- FACT: **no `ads-db.sqlite` exists anywhere under `swipe-files/`** (find returned nothing) while
  `swipe-files/property-sg/pages/` holds 25 mirrored page folders. JUDGMENT: Ghost Postgres is now the only
  canonical copy of the property-sg competitor-ad intelligence (transcripts, OCR, classifications, embeddings);
  losing that DB loses the swipe research that grounds angle generation for property clients.
- **Client dependency:** neezanizam, eugene-chieng, propwise-sg (all property-sg industry).

### 2.6 Canva (via `one` CLI / api.withone.ai)

- FACT: Thomson Reserve created 5 multi-image Canva designs through One CLI connection
  `live::canva::default::a7dda6c...` — design IDs DAHMC34tcUE etc.; edit URLs expire ~mid-2026; binary import
  needed a raw curl workaround because `one` lacks a file-upload flag
  (`clients/neezanizam/SESSION-HANDOFF-260609.md:12`).
- **If disconnected:** the client's creative-review links (sheet column J "CANVA LINK") die; ads themselves are
  unaffected once uploaded.

### 2.7 Tally forms

- FACT: a Tally form feeds eugene's sheet — tab `TALLY FORM`, source `tally_form_responses`
  (`clients/eugene-chieng/_brand/metrics-config.json:259-263`). FACT: neezanizam Thomson Reserve Instant Form is
  **blocked waiting on operator pasting Tally questions** into `campaigns/thomson-reserve/instant-form-questions.md`
  (`SESSION-HANDOFF-260609.md:23,37`).
- **If disconnected:** lead capture for embedded-form funnels stops; form-response tab in the sheet stops filling.

### 2.8 here.now / plans-vault (plans.genflos.com)

- FACT: `.herenow/state.json` registers published sites (happy-sequin-9k6t.here.now etc.). Client review surfaces
  publish to `plans.genflos.com/<client>/...` with HazeCraft as visible publisher — eugene
  (`clients/eugene-chieng/CLAUDE.md:10,72`), takekine live AG1 review
  (`clients/takekine/CLAUDE.md:47` — plans.genflos.com/takekine/ag1/dr-foundation-pilot-260519/).
- **If disconnected:** client approval galleries / concept-review pages go dark; AG1/AG2 sign-off reverts to
  emailing files.

### 2.9 Postiz (self-hosted social scheduler)

- FACT: integration spec at `skills/integrations/postiz/config.json` (env `POSTIZ_API_KEY`/`POSTIZ_API_URL`, both
  present in repo `.env` name list). Instance on Contabo VPS postiz.genflos.com (memory; repo evidence is the
  `vps-guide.md` in the same folder). Consumed by `campaign-runner`, `tiktok-slideshows`, `linkedin-optimization`
  skills (grep hits).
- **Client dependency:** none currently live (no client campaign references Postiz scheduling in active state).
  JUDGMENT: dormant capability.

### 2.10 Telegram bot

- FACT: `CHANNELS.md:1-13` — always-on Claude Code Telegram bot `@fuggycompany_bot` via official Anthropic plugin;
  `cron-registry.json` prompts fire through it when running `--channels`. Operator-facing only.
- **If disconnected:** Jerel loses mobile ops channel (morning dashboard, weekly/monthly reviews); no client impact.

### 2.11 cron-registry.json (FACT, root file)

| id | schedule | enabled |
|---|---|---|
| upstream-sync (check aitytech/agentkits-marketing) | every 3 days 09:00 | true |
| ops-weekly (/ops:weekly) | Mon 10:00 | true |
| ops-monthly (/ops:monthly) | 1st 10:00 | true |
| campaign-check (daily health scan) | daily 09:00 | **false** |
| session-start (morning dashboard) | daily 08:00 | true |

JUDGMENT: the one cron that would catch stalled live campaigns (campaign-check) is the one switched off.

### 2.12 Others (one-liners)

- **Mux** — per-client video host; template-only so far (`clients/_template/CLAUDE.md:88,97-98`); no live client keys in repo. Breaks: landing-page video embeds.
- **Higgsfield** — routed via global CLI skill only (memory + `clients/takekine/CLAUDE.md:24` reference-routing); fuels takekine/neezanizam video creative. Breaks: AI video renders.
- **NotebookLM** — `clients/neezanizam/_brand/notebooklm.json` (source config; keys `general_notebook, notebooks`). Research convenience only.
- **Google Drive** — eugene DCT002 creatives reviewable at a Drive folder URL (`...upgrader-ads/dcts/dct-002-math-blind/pipeline-state.json` `next_action`). Breaks: client creative review.
- **MCP servers** — `.claude/.mcp.json.example` lists 20+ (semrush, dataforseo, hubspot, ahrefs, postiz, notion, slack...); example file only, actual `.mcp.json` gitignored. Mostly aspirational (JUDGMENT).
- **Client-owned hosts** — `thomson.swopyourhome.com/landing` (neezanizam LP, ad destination — `SESSION-HANDOFF-260609.md:17`), `takekine.com` product/sales-letter pages, `eugenechieng.sg`. Not operated from this repo; if they go down, live ads click to dead pages.
- **Whisper/Groq, ElevenLabs, ScrapeCreators, Firecrawl, Linkup, Kilo, Gemini keys** — research/transcription utilities, env names in `.env`; loss degrades research speed, not live campaigns.

---

## 3. Client census (11 real clients)

| Client | Status (JUDGMENT) | Evidence (FACT) |
|---|---|---|
| **neezanizam** | **LIVE** — real Meta spend, metrics cron, 3 funnels; Thomson Reserve upload imminent | act_837789749619954 wired in `_brand/metrics-config.json` with campaign IDs 52569405524110 + 6665612766106 enabled; "15 active PropNex/NeezaNizam Meta ads" (`_swipe/research/buyer-language-dossier.md:182`); handoff dated 260609; newest file 2026-06-09 |
| **eugene-chieng** | **ACTIVE BUILD / upload-gated** — paid client, upgrader-ads DCT002 at `phase_5_upload`, `blocked_until_launch_gates`; DCT001 PARKED (banked angles) | `campaigns/upgrader-ads/dcts/dct-002-math-blind/pipeline-state.json` (`current_phase: phase_5_upload`, last_updated 2026-06-10); dct-001 `pipeline-state.json` = `PARKED`; "Status: Paid client. Intake 28 May 2026" (`CLAUDE.md:24`) |
| **takekine** | **ACTIVE (creative R&D, no paid spend wired)** | `campaigns/_campaigns-index.json`: test_2 active, trial_test_1 archived; live AG1 review URL (`CLAUDE.md:47`); `metrics-config.json` all placeholders; newest file 2026-06-10 |
| **harmony-wellness** | **PAUSED / pre-scope** — website project "pending-scope" | `campaigns/_campaigns-index.json`: `website | pending-scope`; metrics-config sheet_id null; root `active/harmony-wellness/` + `build/harmony-wellness*/` hold site drafts; newest client file 2026-06-02 |
| **stackworks** | **IDLE (research-only; audit test bed)** — avatars + buyer profile + research raw, no campaigns/ | folder = `avatars/ buyer-profile.md research/` only; newest 2026-05-08; V4 audit pilot artifacts kept in `scratch/stackworks` (commit c7d1108); positioning risk flagged in memory |
| **fuggysmedia** | **IDLE (agency's own brand)** — flat legacy structure, empty campaigns/ | `clients/fuggysmedia/campaigns/` empty; newest file 2026-05-14 (video dry-run stills); own Meta account act_936198302709669 known from `.claude/rules/mcp-integrations.md:29` |
| **hazecraft** | **INTERNAL (the agency identity, not a revenue client)** — owns DESIGN.md every published surface must read | `routing-overrides.md` §Design system; `campaigns/` empty; newest 2026-06-02 (DESIGN.md backup) |
| **michelle-koh** | **IDLE** — one published output page, empty campaigns/ | `output/publish/michelle-koh/index.html` (2026-05-16 newest); campaigns/ empty |
| **aura** | **IDLE since mid-March** | 3 campaign folders (brand-outreach, reddit-seeding, tiktok-slideshows); newest file 2026-03-16 |
| **1up-sales-ai** | **IDLE since early April** — Jerel's own SaaS, flat legacy structure | campaigns/ empty; newest 2026-04-08 (swipe-file.md); Paper-design sync pending per memory |
| **propwise-sg** | **IDLE / split-brain** — `clients/propwise-sg/` is a thin flat profile (avatars, icp, offer, brand-voice — exactly the structure `clients/README.md` forbids); the real project lives at ROOT `propwise-sg/` | `ls clients/propwise-sg` = 7 flat files; root `propwise-sg/` = CLAUDE.md, docs, gtm, marketing, tech, shared (last mtime 11 Apr); find on clients/propwise-sg returned no datable file |

**Registry drift (FACT):** `clients/eugene-chieng/campaigns/_campaigns-index.json` lists ONLY
`mp1-upgrader-letter-260603` — the upgrader-ads campaign (the one nearest live spend, edited today) is absent.
Anyone trusting the index per the AGENT ENTRY CONTRACT would miss the hottest workspace.

**Memory-hint verification:** the "DCT008 composite testimonial LIVE" hint is supported:
`clients/neezanizam/output/sales-letters/firsttime-buyers/foundation-packet/claim-evidence-ledger.md:51` calls
DCT008 "a live-creative problem flagged for pause/replace per 0.1-N"; `_brand/source-of-truth.md:549,947,964`
lists the real-testimonial shoot as the DCT008 blocker. Whether the composite ad is still running on Meta is
unverifiable from files alone.
**Eugene "known LIVE (protected)" hint:** files do NOT show live ads — DCT002 explicitly says upload is the only
step left and ads will be created PAUSED. JUDGMENT: "live" likely means "active protected workspace," not live spend.

---

## 4. Operator-dependency map (where Jerel is personally required)

Source docs: `docs/system-rules/hitl-gates.md` (26 lines, read in full), `.claude/workflows/creative-pipeline.md`
HITL gate map (lines 25-35, 128-137), `CLAUDE.md` operating model ("Jerel does 20%: taste, approvals"),
`.claude/rules/routing-overrides.md` AG1/AG2 eval gate.

**Hard BLOCK+ASK (hitl-gates.md:3-11):** any spend · publishing to live platforms · creative direction & brand
voice · strategy pivots · client-facing deliverables before send · schema/data migrations · bulk deletes ·
anything touching production systems.

Per-stage map (creative pipeline — the revenue path):

| Stage | Jerel's personal action | Evidence |
|---|---|---|
| Research / source-of-truth Phase 4 | pick KPI, core message, top 3 angles, first test variable | creative-pipeline.md:131 |
| Angle selection (ad-concept-engine P1) | pick top 2 angles per avatar | creative-pipeline.md:133 |
| Brief/hooks (P2) | per-batch approval, edit headlines/visuals | creative-pipeline.md:134 |
| Asset creation (P3) | per-image / per-video approval | creative-pipeline.md:135 |
| **Meta upload** | ads created PAUSED; only a human un-pauses in Ads Manager ("Founder reviews → enables. NEVER enable from here" — neezanizam handoff §4) | creative-pipeline.md:136; SESSION-HANDOFF-260609.md:30 |
| Feedback routing | approve NEW/BETTER/MORE route | creative-pipeline.md:137 |
| Video AG0/AG1/AG2 | operator approval at each gate; AG1/AG2 HTML publish hard-blocked unless eval-buyer-fit PASS or operator override | routing-overrides.md §Brand-alignment evaluator gate |
| Pixel / offline events (neezanizam) | "OPERATOR-MANUAL — Jerel sets up pixel + appointment event himself" | SESSION-HANDOFF-260609.md:18 |
| Tally form questions | operator must paste questions before Instant Form build | SESSION-HANDOFF-260609.md:23 |
| Client-side dependencies | Eugene: quote permission, case scope confirm, BM ID delivery; NeezaNizam: real testimonial shoot (DCT008), avatar sign-offs | dct-002 pipeline-state `next_action`; source-of-truth.md:549 |

JUDGMENT: the system is genuinely 80/20 — agents draft everything, but **no money moves and nothing goes public
without Jerel clicking**. The single-human bottleneck is also the single point of failure: five separate
workstreams (Thomson upload, eugene gates, pixel setup, Tally paste, testimonial chase) are all queued on the
same person, and three of those additionally wait on the *client*.

---

## 5. Root oddities

| Item | Purpose | Last activity | Notes |
|---|---|---|---|
| `credentials/` | Google API identities for the ad-intel sheets pipeline: `gsheets-service-account.json` (SA `ad-intel-sheets@ad-intel-pipeline-27983...`, full private key), `oauth_client.json`, `oauth_token.json` (refresh token) | 27 Mar | **SECURITY: real secrets on disk but NOT in git** — `git check-ignore` matches all three + `.env` (gitignore line `credentials/`), `git ls-files credentials/` empty. Sibling risk: `scripts/modal/credentials.json` (neezanizam SA key) also on disk, also gitignored. `.env.bak-260607-171106` is an extra secrets copy at root (gitignored via `.env*`). |
| `propwise-sg/` (root) | Full product/GTM project (CLAUDE.md, docs, gtm, marketing, tech, shared) — predates/parallels the thin `clients/propwise-sg/` profile | 11 Apr | JUDGMENT: should be merged into `clients/propwise-sg/` or explicitly marked external; currently two sources of truth. |
| `_swipe/` (root) | Single folder `winning-ads/` with 3 files (one Ferrovia ad mp4 + analyses) | 21 May | Personal "winning ads" stash; naming collides with per-client `_swipe/` convention. |
| `swipe-files/` (root) | Industry-level ad-intel mirror (`property-sg/`: 25 pages, avatar-registry.json, research-pool.json) — the filesystem face of Ghost Postgres | 21 Apr dir mtime | Canonical data is in Ghost; the SQLite source named by ghost-sync.py is absent locally (see §2.5). |
| `active/` | Working scratch: chatroom/consensus reports, harmony-wellness index.html, pdf-extraction report | 1 May | JUDGMENT: stale session debris, not a pipeline stage. |
| `brain/` | `brain/jerels brain/Marketing/clients` — an EMPTY nested directory chain (zero files) | 8 May | JUDGMENT: accidental path creation (likely a mis-resolved absolute path during a write); safe to flag for deletion by owner. |
| `build/` | HTML site builds: harmony-wellness v1/v3 section files, 1up-index.html, screenshots | 17 Mar dirs | Website-design skill output; gitignored (`build`). |
| `exports/` | Two zips: 1up-sales-ai data + agentkit marketing system (both 260312) | 12 Mar | Generated by `scripts/export.py`; gitignored. |
| Root strays | `findings.md` (83KB), `task_plan.md`, `progress.md`, `tcm-clinic-sitemap-sg.md`, `Nadia_Marketing_Pitch_Calculator.xlsx` (in scripts/), `whop-dl-extension/`, `youtube-thumbnails/` | Mar-Jun | JUDGMENT: planning/one-off artifacts living at root against the repo's own ICM hygiene rules. |

---

## 6. Stage map (what this agent observed of the pipeline)

1. **Swipe/intel ingest** — inputs: Meta Ad Library scrapes; gate: none; outputs: Ghost Postgres + `swipe-files/` mirror; owner: `scripts/ghost-sync.py`, `scripts/sync-ghost-to-swipefiles.py`, `/ads:scrape-library`.
2. **Research → source-of-truth** — inputs: dossiers, scrapes; gate: Phase 4 strategic picks (Jerel) + citation verification; owner: `source-of-truth` skill + `scripts/verify-research-citations.py`.
3. **Angles → copy → images (DCT build)** — inputs: avatars + source-of-truth; gates: HITL at every phase (angles, briefs, per-image); owners: big-angle-spotter / ad-concept-engine / headline-bank / `scripts/ad-images/render.py` (Azure executor).
4. **Sheet write + Canva review pack** — inputs: dct.json; gate: none (mechanical); owners: `scripts/tr_10_5_5_sheet_writer.py` et al. (neezanizam SA), `one` CLI → Canva.
5. **Meta upload** — inputs: dct bundles; gate: operator-locked decisions, ads created PAUSED, founder enables in Ads Manager; owner: `skills/meta-ads-uploader/scripts/upload.py` + `meta` CLI.
6. **Metrics loop** — inputs: Meta insights; gate: none (automated cron); outputs: client sheet rows + `clients/<slug>/metrics/` snapshots; owner: Modal app `marketing-metrics` (workspace fuggysense).
7. **Feedback routing** — inputs: performance rows; gate: Jerel approves NEW/BETTER/MORE; owner: `feedback-router` skill.

---

## 7. Open questions for the orchestrator / operator

1. Was the Meta long-lived token (exp ~2026-06-15 per the Apr-16 handoff) rotated when `.env` was re-saved on
   7 Jun? If not, the metrics cron dies this week.
2. Is the DCT008 composite-testimonial ad still spending on act_837789749619954? Files flag it for pause/replace;
   only an Ads Manager read can confirm.
3. What does "eugene upgrader-ads LIVE (protected)" mean operationally? On-disk state says pre-upload, blocked on
   client permissions — no live-ads evidence found.
4. Should the multi-client sheet writers keep using neezanizam's GCP service account, or does each client get its
   own (template says per-client; practice says shared)?
5. Root `propwise-sg/` vs `clients/propwise-sg/` — which is canonical, and is propwise a client or an internal
   product?
6. Where does the canonical property-sg ads SQLite live now? ghost-sync.py's documented input file doesn't exist
   locally; if Ghost is the only copy, is it backed up?
7. Why is the daily `campaign-check` cron disabled while two clients have money-adjacent pipelines in flight?
