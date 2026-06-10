# Session Handoff — Thomson Reserve sheet + metrics-config readjust (260608)

**Status:** PAUSED mid-task. Resume here next session.
**Immediate next job:** rebuild the Thomson Reserve sheet's `CREATIVES` + `COPY` tabs to Jerel's *actual* desired format (below), then update `clients/neezanizam/_brand/metrics-config.json` gids to match.

---

## 1. THE CORRECTION — read this first

The Thomson Reserve sheet currently has `CREATIVES` + `COPY` tabs in the **10-5-5 "BATCH-keyed, one-row-per-angle"** layout. **Jerel says this is wrong.** His verbatim ask:

> "i want the previous one format, but extend it to 5 copy and 5 headline in one row for copy and for creatives its 5 angles 1 row, and tbh i dont know about the rest."
> "this part about the capitalized creatives and creatives, ten five five is absolutely wrong. This isn't the way where I want the sheets to look like."

So the desired layout is **WIDE single-row, not one-row-per-angle**:

- **COPY tab** — previous (standard) format, but widened to **5 copies + 5 headlines on ONE row per DCT**.
  Proposed columns: `BATCH | STATUS | COPY 1 | COPY 2 | COPY 3 | COPY 4 | COPY 5 | HEADLINE 1 | HEADLINE 2 | HEADLINE 3 | HEADLINE 4 | HEADLINE 5` (12 cols). One DCT = one row.
- **CREATIVES tab** — previous format, **"5 angles, 1 row."** EXACT columns NOT yet confirmed — see Open Question Q1.
- **The other 7 tabs** — Jerel said "i dont know about the rest." Needs his input — see Q3.

### ⚠️ This CONTRADICTS the written spec — resolve explicitly
`docs/methods/10-5-5/SPEC.md` §3 deliberately chose the OPPOSITE: *"we do NOT widen the COPY tab to 5+5 columns crammed on one row. We add rows."* Jerel now wants the wide format. The operator's preference wins, but next session must decide: (a) Thomson uses a wide layout that diverges from the SPEC, and/or (b) update SPEC.md §3 / D1 to reflect the new decision. Do NOT silently let the sheet and the spec disagree.

---

## 2. Open questions for Jerel (ask at start of next session)

- **Q1 — CREATIVES "5 angles 1 row":** what does each row hold? Likely the standard CREATIVES columns with the single `ANGLE` column expanded to `ANGLE 1…ANGLE 5` (5 angle slots on one DCT row). Confirm the exact columns, and where the metric columns (CTR/CVR/CPA/CALLS/SPEND/DURATION) sit — per-DCT (one set) or per-angle (5 sets)? Propose a column list and get a yes.
- **Q2 — COPY:** confirm the 12-col wide layout above (5 copies + 5 headlines, one DCT per row). Is `STATUS` still wanted? Any `PERSONA`/`AD` column?
- **Q3 — the 7 operational tabs** (DAILY CALLS, WEEKLY CALLS, MONTHLY CALLS, KPIs, APPT, AVATARS, OBF DATA): keep all? Drop any? They're currently cloned from buyer-funnel, empty. Jerel unsure.
- **Q4 — naming:** tabs should be plain `CREATIVES` / `COPY` (the whole workbook is the campaign), correct?

---

## 3. Thomson Reserve sheet — current state (facts)

- **Sheet ID:** `1KqWJP08h8BPr8ygH1ADnmrDPuGaH3p7v4O3WS6WoAtM`
- **URL:** https://docs.google.com/spreadsheets/d/1KqWJP08h8BPr8ygH1ADnmrDPuGaH3p7v4O3WS6WoAtM/edit
- **Owner:** jerel@genflos.com · **shared editor:** SA `neezanizam@neezanizam-492212.iam.gserviceaccount.com` + `ops@1upsalesai.com`
- **Current tabs + gids:**

| Tab | gid | State |
|---|---|---|
| DAILY CALLS | 416409408 | cloned from buyer-funnel, empty — keep? (Q3) |
| WEEKLY CALLS | 1148083398 | cloned, empty — keep? |
| MONTHLY CALLS | 925087880 | cloned, empty — keep? |
| KPIs | 599386541 | cloned (1 mock `$6000` row left), empty otherwise |
| APPT | 1509631817 | cloned, empty |
| AVATARS | 2014868411 | cloned, empty |
| OBF DATA | 1076289255 | cloned, only `Email Address(es)` label kept |
| **CREATIVES** | **517682187** | **WRONG (10-5-5 angle-row). REBUILD per Q1.** |
| **COPY** | **1419950717** | **WRONG (10-5-5 angle-row). REBUILD per Q2.** |

- **Config block:** `clients/neezanizam/_brand/metrics-config.json` → `campaigns[]` → `campaign_slug: "thomson-reserve-buyers"`. Currently `meta.enabled: false` (no Thomson Meta campaign exists yet — confirmed none in `act_837789749619954`). Its `tabs{}` maps all 9 gids above. **After rebuilding CREATIVES/COPY, the creatives+copy gids in this block must be updated.**
- Thomson is correctly OUT of the daily auto-pull (only `buyer-funnel` + `asset-progression` pull).

### "Previous format" reference (what to widen FROM)
Standard tabs live in the buyer-funnel workbook `14bh8k6S-krbg0I69JgO2e7eP-YkS6_NMC7XN2NTNKSE`:
- standard **CREATIVES** gid `1164222857` — 16 cols: `(BATCH) | STATUS | FORMAT | AD | MARKET AWARENESS | MARKET SOPHISTICATION | ANGLE | Why am I testing this? | PERSONA | CANVA LINK | CTR | CVR | CPA | CALLS | SPEND | DURATION`
- standard **COPY** gid `1695031878` — 6 cols: `BATCH | STATUS | COPY 1 | COPY 2 | HEADLINE 1 | HEADLINE 2`
Start from these and WIDEN (COPY → 5+5; CREATIVES → 5 angles per Q1).

---

## 4. How to operate the sheet next session (auth + tooling)

**Auth gotcha (do not rediscover):** the service account CANNOT create/restructure-create sheets (no Drive → 403). It can only WRITE sheets shared with it. To create/clone/rename tabs, use the **gcloud user token** (jerel@genflos.com, has Drive scope). Full model: `skills/sheets-provisioner/references/sheet-auth.md`.

```bash
# Drive-scoped token (verify it carries drive scope):
gcloud auth print-access-token
curl -s "https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=$(gcloud auth print-access-token)" | jq -r .scope | tr ' ' '\n' | grep drive
```

**Sheets API client** (no global google libs installed — use a venv; /tmp one is ephemeral, recreate):
```bash
python3 -m venv /tmp/sheetsverify && /tmp/sheetsverify/bin/pip install -q google-api-python-client google-auth
# read/write existing tabs can also use the SA creds at scripts/modal/credentials.json
```

**Reusable provisioner** (built this session): `skills/sheets-provisioner/scripts/provision_from_template.py` — clones tab STRUCTURE from a template workbook, clears data, shares.
- ⚠️ **Footgun:** its `--into` mode deletes ALL pre-existing tabs in the destination. That's why the CREATIVES/COPY swap this session was done by hand, not via the script. **TODO: tighten `--into` to only replace name-collision tabs (not nuke all), + add a source→dest rename map.** Until then, do targeted tab swaps by hand (copyTo + delete old + rename + batchClear).
- For the rebuild, the WIDE layout is NOT a clone (no source tab has 5+5 cols) — it must be BUILT: create the tab with the desired header row, set dimensions, frozen row 1.

---

## 5. What else this session shipped (context — already done, working)

These are DONE and verified; listed so next session doesn't re-litigate them:

1. **Meta Ads MCP → `meta` CLI migration** (13 files): the repo no longer references a `meta-ads` MCP (it never existed live). Canonical: `.claude/rules/mcp-integrations.md` note + `data-reliability-rules.md` + 10 command files. Meta work = `meta` CLI (`~/.local/bin/meta`), `meta ads <object> <verb>`.
2. **NeezaNizam metrics pipeline — diagnosed + de-risked.** It's a **Modal cron app** (`scripts/modal/marketing_metrics.py`), pulls Meta via raw Graph v22.0, writes to Google Sheets via gspread/SA. It is **NOT broken** — it's been writing `asset-progression` daily (LP-AssetProgression tab, continuous 3 Apr → 6 Jun) via the old baked `default` config slug. Earlier "dead since April" diagnosis was WRONG (snapshots save to ephemeral Modal storage).
   - **Token swap DONE:** the Meta token expired ~15 Jun; replaced the Modal `meta-ads` secret + repo `.env` `META_ADS_ACCESS_TOKEN` with the never-expiring system token. Modal reads secrets at runtime, so the live cron is already protected — no redeploy required.
   - **Config-path bug FIXED:** `scripts/modal/config_loader.py` now resolves `metrics-config.json` from `_brand/` (with legacy root fallback) for every client — generic, no per-client hardcoding. Takes effect on next `modal deploy` (not yet deployed; cron still runs April image, which works).
   - **Ghost folder ARCHIVED:** `clients/neezanizam-260504-pre-reorg/` (a stale backup that the scanner treated as a 2nd live client → would double-write) moved to `clients/_archive/`. Scanner now sees only buyer-funnel + asset-progression.
   - **10-5-5 test campaign DISABLED:** `buyer-funnel-10-5-5-test` block set `enabled:false`.
3. **sheets-provisioner skill — capability added:** `references/sheet-auth.md` (the SA-can't-create gotcha + two-identity model), `scripts/provision_from_template.py` (the cloner), SKILL.md updated. NOTE: SKILL.md clone example still points at *standard* CREATIVES/COPY — should be revisited once Thomson's true format is locked (the 10-5-5 row-vs-column question is unresolved at the spec level).

### Deferred / not done (operator's call)
- `modal deploy` of the fixed config_loader + config (cron works on old image, so not urgent).
- Fixing the wrong "one sheet (`14bh8k6S`)" note in `clients/neezanizam/CLAUDE.md` (asset-progression is actually `1D-Hrq…`; two workbooks).
- Tighten the provisioner `--into` footgun (item 4 above).
- New skill files + config edits are SAVED but NOT committed to git.

---

## 6. First actions next session

1. Ask Jerel Q1–Q4 (§2). Lock the exact CREATIVES + COPY column layouts.
2. Decide the SPEC.md tension (§1) — diverge or update the spec.
3. Build the two tabs to the agreed wide layout (build, don't clone). Clear/empty.
4. Update `metrics-config.json` `thomson-reserve-buyers.tabs.creatives` + `.copy` gids.
5. Validate: `jq empty` the config; `load_client_config('neezanizam','thomson-reserve-buyers')`; confirm Thomson still out of auto-pull; leak-check the tabs.
