---
name: sheets-provisioner
description: "Provision Google Sheet + LP funnel tabs per campaign. Scaffolds new client folders or appends to existing metrics-config.json. Triggers: new campaign, new LP sheet, add campaign, provision sheet, onboard client."
---

# Sheets Provisioner — One Command Per Campaign

Provisions the infrastructure for a new landing-page-funnel campaign:

1. **Google Sheet** — fresh, LP-only (3 tabs: `LP-<Label>`, `LP-<Label>-Weekly`, `LP-<Label>-Monthly`)
2. **Modal config** — auto-merges into `clients/<slug>/metrics-config.json` using the `campaigns[]` array format (migrates legacy flat configs on first run)
3. **Client folder** — created from scratch if the client is new

Scoped to **1 sheet per campaign**. A client with 3 campaigns = 3 sheets.

## When to trigger

Auto-load this skill when user says:
- "new campaign for [client]"
- "provision new sheet"
- "add campaign"
- "new LP sheet"
- "onboard new client with LP funnel"
- "set up tracking for [campaign]"

## Prerequisites

- Google service account creds at `scripts/modal/credentials.json` (or `GOOGLE_SHEETS_CREDS_PATH` env) — for **writing** existing sheets
- For **creating/cloning** a sheet: a gcloud user token with Drive scope (`gcloud auth print-access-token`) — the service account **cannot create sheets**
- `.env` with `META_ADS_ACCESS_TOKEN` if you'll test the pull after
- Meta campaign already launched (you need the `campaign_id` to filter to) — or set `meta.enabled: false` until it is

> **READ FIRST — auth gotcha:** a bare service account CANNOT create Google Sheets (no Drive of its own → `403`). Creation runs under the gcloud **user** token; the service account is added as an **editor** so the cron can write. Full model + commands: [`references/sheet-auth.md`](references/sheet-auth.md). This is the #1 wall this skill hits.

## The single command

```bash
python3 scripts/modal/setup/provision_campaign.py \
  --client-slug <slug> \
  --campaign-slug <campaign-slug> \
  --label <Label> \
  --ad-account-id act_XXXXXXXXXXXXXXXX \
  --meta-campaign-id <META_CAMPAIGN_ID> \
  --share-email <jerel@email>
```

**Find-or-create shortcut (gws-native, no Python):** to reuse a campaign's registered sheet or create one if none exists, use `scripts/find_or_create_sheet.sh --client <slug> --campaign <slug>` — it reads `metrics-config.json`, reuses the `sheet_id` if present, else creates + shares + registers via the `gws` CLI. `--dry-run` is safe. Use this instead of `provision_from_template.py` when you don't need to clone a template's tab structure.

**Flags:**
- `--sheet-id <id>` — use existing sheet instead of creating new one
- `--share-email <email>` — share new sheet as editor
- `--force` — overwrite existing campaign block with same slug

**Behaviour:**
- New client folder? → creates it
- Existing flat `metrics-config.json`? → migrates to `campaigns[]` format (preserves existing data as `campaign_slug: "default"`)
- Existing `campaigns[]`? → appends the new campaign
- Tabs already exist on sheet? → skips re-creation (idempotent)

## Workflow for Claude

### 1. Gather inputs — ask user for each that's missing

| Input | Example | Purpose |
|---|---|---|
| Client slug | `neezanizam` | Folder under `clients/` |
| Campaign slug | `buyer-funnel` | Unique per client |
| Label | `BuyerFunnel` | Used in sheet title + tab names |
| Meta ad account id | `act_837789749619954` | From Meta Ads Manager account settings |
| Meta campaign id | `4048596882097890` | From the specific campaign you want tracked |
| Share email (optional) | `jerel@...` | Will share the new sheet as editor |

### 2. HITL confirmation

Present:
```
About to provision:
  Client: <slug> (existing folder? yes/no)
  Campaign: <slug> — "<Label>"
  Meta filter: campaign_id <id>
  New sheet: "<client_slug> — <Label>"
  Share with: <email>

Proceed? (yes / edit / cancel)
```

### 3. Execute the command

Run `provision_campaign.py` with the gathered args. Stream output to user.

### 4. Smoke-test the cron path

```bash
modal run scripts/modal/marketing_metrics.py::run_for_client \
  --client-slug <slug> \
  --campaign-slug <campaign-slug> \
  --dry-run
```

Confirms Meta API can pull with the new filter + config loads cleanly.

### 5. Summary to user

```
✓ Provisioned: <client>/<campaign-slug>
  Sheet: <URL>
  Tabs: LP-<Label>, LP-<Label>-Weekly, LP-<Label>-Monthly
  Config: clients/<slug>/metrics-config.json (campaigns[] updated)

Next daily cron (9am SGT) writes the first row automatically.
```

## What it creates on the sheet

3 tabs with identical 19-column structure. Rows 1-3 frozen:

- **Row 1** — column headers (black bg)
- **Row 2** — auto SUMMARY totals (dark grey bg, `=IFERROR(SUM/SUM,"")` formulas)
- **Row 3** — descriptions explaining why each metric matters (light grey, italic)

### Column order (same across daily/weekly/monthly)

**Front — client-facing reporting (uncoloured):**
`DATE | SPEND | FORM SUBMITS | CPFS | LP→FORM CVR | APPT | CAPPT | CPA | REVENUE`

**Back — agency diagnostic (coloured):**
`IMPRESSIONS | REACH | LINK CLICKS | LP VIEWS | CTR | CPC | CPM | CPLV | CLICK→FORM CVR | NOTES`

Color convention:
- **Yellow tint** = volume metrics (IMPRESSIONS, REACH, LINK CLICKS, LP VIEWS)
- **Pink tint** = cost metrics (CPC, CPM, CPLV)
- **Blue tint** = rate metrics (CTR, CLICK→FORM CVR)

### Blank-cell rule

When Meta reports 0 form submits for a period:
- `FORM SUBMITS` → blank (not `0`)
- `CPFS`, `LP→FORM CVR`, `CLICK→FORM CVR` → blank (not `$0.00` or `—`)

Keeps the sheet honest: blank = no conversion, not "we measured zero efficiency."

### Manual columns

`APPT`, `CAPPT`, `REVENUE`, `NOTES` — filled by you/client post-call, not by the cron.

## What Meta needs for this to work

The LP must fire a Meta Pixel `Lead` event on form submit. Without it, `FORM SUBMITS` stays 0 forever.

To verify: open the LP → submit a test form → check Meta Events Manager → Test Events → confirm `Lead` event appears.

If the pixel only fires `PageView`, install a ClickFunnels/Webflow form-submit trigger that calls `fbq('track', 'Lead')` on success.

## Error handling

| Error | Response |
|---|---|
| `credentials.json` missing | Guide user through Google Cloud service account setup |
| Client folder doesn't exist | Auto-creates (expected for new clients) |
| Campaign slug already in config | Requires `--force` flag — ask user to confirm overwrite |
| Sheet creation fails with `403 "caller does not have permission"` | The **service account can't create sheets** (no Drive). Create under the gcloud user token instead — see `references/sheet-auth.md` + `scripts/provision_from_template.py`. NOT a quota issue. |
| LP tab provisioning fails mid-way | Tabs are idempotent — re-run the same command to finish |
| `load_client_config` validates fails | Print the ValueError and ask user to fix the config manually |

## Rules

1. **Always HITL before creating** — sheet + config writes are non-trivial
2. **Never overwrite a campaign block** without `--force`
3. **Never share externally** unless `--share-email` explicitly provided
4. **One campaign = one sheet** — don't merge multiple campaigns into one sheet
5. **Log the run outcome** by checking the script's printed summary

## Clone the full operational structure from a template (DAILY CALLS … OBF DATA)

When a campaign needs the full operational workbook (the multi-tab DCT structure:
`DAILY CALLS, WEEKLY CALLS, MONTHLY CALLS, KPIs, APPT, CREATIVES, AVATARS, COPY, OBF DATA`)
rather than the LP-funnel-only sheet, clone the structure from an existing template
workbook with `scripts/provision_from_template.py`. It copies each tab's
formatting/formulas/frozen-rows/dimensions via the Sheets `copyTo` API, then **clears the
template client's data** so nothing leaks, and shares with the accounts you pass.

```bash
# create a new workbook from a template (e.g. buyer-funnel 14bh8k6S as the template)
python3 skills/sheets-provisioner/scripts/provision_from_template.py \
  --source 14bh8k6S-krbg0I69JgO2e7eP-YkS6_NMC7XN2NTNKSE \
  --title "THOMSON RESERVE | Buyers" \
  --tabs "DAILY CALLS,WEEKLY CALLS,MONTHLY CALLS,KPIs,APPT,CREATIVES,AVATARS,COPY,OBF DATA" \
  --keep "APPT=2" \
  --share "neezanizam@neezanizam-492212.iam.gserviceaccount.com=writer,ops@1upsalesai.com=writer"

# or reshape an EXISTING (already-shared) workbook in place: swap --title for --into <sheet_id>
```

Header depth kept per tab = `max(frozenRows, 1)`; override with `--keep "TAB=N"`. Everything
below is cleared. Auth model (gcloud user token creates; SA is editor): `references/sheet-auth.md`.

The old `scripts/modal/sheets_creator.py` path assumed the **service account** could create —
it can't (see the auth gotcha). Prefer `provision_from_template.py`.

## Canonical config template (source of truth for the tab set)

The canonical `metrics-config.json` shape lives at **`clients/_template/_brand/metrics-config.json`**.
A new client's config is a copy of it. It carries the `provisioning` block, an empty
`campaigns[]`, and the `tabs` schema library. The tab doctrine is encoded in its
`_tabs_doctrine` field:

- **CORE (every client):** `daily_calls, weekly_calls, monthly_calls, kpis, appt, creatives, avatars, copy, obf_data` — 9 tabs.
- **OPTIONAL (add only when relevant):** `lp_funnel` (+weekly/+monthly) for clients with a **landing page**; `creatives_test` + `copy_test` for clients running **10-5-5 test-wave** discipline; one **form-response tab** named for the client's own tool (e.g. `TALLY FORM`) for clients capturing leads via an embedded form. These live under `_optional_*` wrappers in the template — move them out and fill the gid only when the client needs them. Do NOT hardcode a form tool or ship LP tabs to a client with no landing page.

`CREATIVES` is 16-col (`Why am I testing this?` at index 7). `COPY` is 6-col by default; widen to the 12-col 10-5-5 shape (`BATCH, STATUS, COPY 1-5, HEADLINE 1-5`) before a 10-5-5 wave if you want one row per DCT.

**Full build sequence for a new client (assembled — no single command):**
1. `find_or_create_sheet.sh --client <slug> --campaign <slug>` → create + share + register the workbook (human OAuth; SA can't create).
2. `provision_from_template.py --source <template-sheet> --into <new-sheet> --tabs "<CORE 9, + any OPTIONAL the client needs>"` → clone tab structure, clear template data.
3. (LP clients only) `scripts/modal/setup/provision_lp_tabs.py --client-slug <slug> --label <Label>` → add the 3 LP tabs with their SUMMARY formulas.
4. Record the live gids into `campaigns[].tabs`.
5. `source_of_truth_sheet_writer.py` → AVATARS (narrative-per-row). `tr_10_5_5_sheet_writer.py` / `ad_concept_sheet_writer.py` → CREATIVES/COPY rows.

Note: the `provision_*.py` scripts need the google python libs (Modal env). In a gws-only
local shell, replicate the clone via `gws sheets spreadsheets sheets copyTo` (preserves
formatting/formulas/frozen rows) + rename + `values batchClear` below the frozen rows.

<!-- skill-graph:start -->

## Related
<!-- auto-generated by scripts/link-skills.py — do not edit by hand -->

- [[metrics-wire]] (skill, 0.26)
- [[sheets-updater]] (skill, 0.14)

<!-- skill-graph:end -->
