# Session Handoff — Thomson Reserve DCTs built → ready to upload (PAUSED)

_Date: 2026-06-09 (SGT). Client: neezanizam. Campaign: thomson-reserve. Branch: main._

## One-line resume
Thomson Reserve is built end-to-end (images→DCTs, copy, sheet, Canva) and **approved to upload all 5 ads PAUSED**. Next session: paste the Tally questions, then run the upload. Start at `campaigns/thomson-reserve/dcts/pipeline-state.json` + `dcts/_UPLOAD-RUNBOOK.md`.

## What shipped this session
- **5 DCTs (10-5-5)** at `campaigns/thomson-reserve/dcts/DCT101–105/` — `dct.json` + `copy.md` + `images/`. 44 images allocated image-first (moved + renamed `DCT1NN-img-NN`), ledger reconciled (`_assets/_assets.json`: 38 allocated, 6 bench available, 17 retired). Source-of-truth map: `dcts/../allocation-map.json`.
- **Copy:** scraped FB Ad Library (58 active competitor ads → `_swipe/fb-ad-library/tr-scrape-260609/`), wrote the inverse-of-saturated voice: 25 primary texts + 25 headlines (5×5 per DCT), committed to every `dct.json` + `copy.md`. Lean register, real proximity claims, no anti-sell padding.
- **Google Sheet** (`1KqWJP08h8BPr8ygH1ADnmrDPuGaH3p7v4O3WS6WoAtM`): live tabs are plain **CREATIVES** (gid 517682187) + **COPY** (gid 1419950717); the `_10x5x5` names in old config never existed. COPY widened to 10-5-5. 5+5 rows, copy verbatim, CANVA LINK = column J.
- **Canva** (via `one` CLI, connection `live::canva::default::a7dda6c201db4e75bde87c2493dc017f`): one multi-image design per DCT (page_count = image count, verified). Links in sheet col J + each `dct.json.canva`. Design IDs: 101 `DAHMC34tcUE` · 102 `DAHMC5fP5aQ` · 103 `DAHMC1Oflw0` · 104 `DAHMC8Vhioo` · 105 `DAHMCzZVQqQ`. NOTE: edit_urls carry a ~mid-2026 token expiry + open only in a logged-in Canva session; design IDs are the durable handle. (Binary import couldn't go through `one actions execute` — agent posted PDFs to the same `api.withone.ai/v1/passthrough/imports` endpoint via curl using the stored One credential. Real `one` CLI gap: no `--data-binary`/`--file` flag.)

## Upload decisions LOCKED (operator, 260609) — build all 5 PAUSED
- **Objective:** Leads. **Optimise:** Leads for now (appointment-optimisation deferred — needs pixel + offline event).
- **Budget:** $20/day per ad set (nominal placeholder, paused).
- **Destinations:** DCT101 + DCT102 → WEBSITE `https://thomson.swopyourhome.com/landing` · DCT103/104/105 → Instant Form.
- **Pixel:** OPERATOR-MANUAL — Jerel sets up pixel + appointment event himself. Do NOT block upload on it.
- **Account:** `act_837789749619954` (NND@Propnex), business `837781629620766`. Auth: `source ~/.claude/.env && export ACCESS_TOKEN="$META_ACCESS_TOKEN"`.
- **Naming:** campaign `Thomson Reserve | VVIP Preview | Lead-Gen` (must contain "Thomson Reserve") · ad sets `TR_<DCTID>_Flex_5angles` · ads `TR_<DCTID>_FlexAd_10x5x5`.

## Pick up here (next session)
1. **Paste the Tally questions** into `campaigns/thomson-reserve/instant-form-questions.md` (currently PENDING) — needed to build the Instant Form for DCT103/104/105.
2. Run the upload per `dcts/_UPLOAD-RUNBOOK.md`: `meta` CLI → 1 Leads campaign + 5 ad sets (PAUSED, $20/day) → build 5 bundles from dct.json → `skills/meta-ads-uploader/scripts/upload.py full` → 5 PAUSED Flexible Ads.
3. **Verify first:** does `upload.py create_creative_dynamic` pack all ≤10 images into one asset_feed_spec Flexible Ad? If not, build the creative via `meta ads creative create` directly (runbook §0).
4. After create: flip `metrics-config.json` thomson-reserve-buyers `meta.enabled=true` + add campaign_id; set pipeline-state phase → `UPLOADED_PAUSED`. Founder reviews in Ads Manager → enables. NEVER enable from here.

## Open / honest caveats (do not lose)
- **3 provisional avatars** (DCT102 Area-Loyalist, DCT103 School-belt Parent, DCT105 Right-sizer) — founder sign-off pending (CONTEXT). Copy built on them; fine while PAUSED.
- **Proximity claims** (1km Ai Tong, 5-min MRT) are competitor-sourced + UNVERIFIED — fact-check before enabling.
- **DCT104 thin** (1 image, text-led). Bench top-up available: `tr_37_lifestyle_nature_sofa`, `tr_65_interior_reserveview_family` (+ 4 pool: tr_13/14/15/61). Decide before or after upload.
- `thomson.swopyourhome.com/landing` — confirm the page is live before enabling DCT101/102.

## Key files
- `campaigns/thomson-reserve/dcts/pipeline-state.json` — machine state (READ FIRST) + upload_plan
- `campaigns/thomson-reserve/dcts/_UPLOAD-RUNBOOK.md` — CLI upload steps + naming
- `campaigns/thomson-reserve/instant-form-questions.md` — PENDING Tally paste
- `campaigns/thomson-reserve/CONTEXT.md` — Status/next updated to point here
- `campaigns/thomson-reserve/dcts/DCT101–105/{dct.json,copy.md}` — the creative
- `skills/meta-ads-uploader/` — uploader (bundle → paused ads)
