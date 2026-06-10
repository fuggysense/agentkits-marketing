# Sheet creation auth — the two-identity model (hard-won gotcha)

**The wall:** a bare Google **service account cannot create Google Sheets.** Service accounts have no personal Drive to create files in, so `spreadsheets.create` (and `drive.files.create`/`copy`) returns `403 "The caller does not have permission"`. The SA can only **read/write sheets already shared with it.**

This bit us 2026-06-08 (THOMSON RESERVE | Buyers). The `sheets-provisioner` skill referenced only `credentials.json` (the SA) and silently assumed it could create — it can't. Don't rediscover this.

## The model: two identities, split by job

| Identity | Can it create? | Job | When it runs |
|---|---|---|---|
| **gcloud user token** (`jerel@genflos.com`, Drive scope) | ✅ yes | **create + own** the workbook, clone tabs, share | setup time — a human is present |
| **Service account** (`neezanizam@neezanizam-492212.iam.gserviceaccount.com`) | ❌ no | **write rows** into an existing sheet | runtime — the Modal cron |

Creation is inherently a setup-time, human-present act. The cron never creates sheets, only writes — so this split is clean, not a workaround.

## How creation is authorized

**Preferred (fewer steps): the `gws` CLI.** `gws auth login -s drive,sheets` gives a native Drive+Sheets OAuth token (same human, `jerel@genflos.com`), then create + share are pure CLI — no Python `google` libs (not installed here), no brittle `--enable-gdrive-access` flag:

```bash
gws auth status        # token_valid? if false: gws auth login -s drive,sheets
ID=$(gws sheets spreadsheets create --json '{"properties":{"title":"X"}}' --format json | jq -r .spreadsheetId)
gws drive permissions create --params "{\"fileId\":\"$ID\",\"sendNotificationEmail\":false}" \
  --json '{"role":"writer","type":"user","emailAddress":"neezanizam@neezanizam-492212.iam.gserviceaccount.com"}'
```

Or just run `scripts/find_or_create_sheet.sh --client <slug> --campaign <slug>` — it does find-or-create + share + register via `gws`.

**Fallback: the gcloud user token** (use only if `gws` is unavailable). The gcloud login was granted Drive scope once:

```bash
gcloud auth login --enable-gdrive-access     # one-time; persists in ~/.config/gcloud
gcloud auth print-access-token                # now returns a Drive-scoped token
```

Verify the token actually carries Drive scope before using it:

```bash
curl -s "https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=$(gcloud auth print-access-token)" \
  | jq -r '.scope' | tr ' ' '\n' | grep drive
```

The active gcloud account here is `jerel@genflos.com` — the **same** account that owns the existing client metrics sheets (buyer-funnel `14bh8k6S…`, asset-progression `1D-Hrq…`). So sheets created this way match the existing ownership pattern: **human owns, SA is shared editor.**

## After creating, always

1. Share the new sheet with the **service account** as **editor** (`neezanizam@neezanizam-492212.iam.gserviceaccount.com`) — otherwise the metrics pipeline can't write to it.
2. Share with whoever needs human access (e.g. `ops@1upsalesai.com`) as editor.
3. Register it in `clients/<client>/_brand/metrics-config.json` (a `campaigns[]` block with `sheet_id` + `tabs`).

## Fragility + the bulletproof option

- **Fragility:** if anyone runs `gcloud auth login` again *without* `--enable-gdrive-access`, the Drive scope drops and creation breaks until re-enabled. Headless/cron contexts have no user token at all — but they never create, only write, so that's fine.
- **Bulletproof (optional):** configure **domain-wide delegation** on the service account so it can impersonate a `genflos.com` Workspace user and create sheets itself — zero human token. Needs Workspace-admin sign-off once. Only worth it if sheet creation becomes frequent/automated.

## Use the script, don't hand-roll

`scripts/provision_from_template.py` encapsulates all of the above: gcloud token → clone tab structure from a template workbook → clear data → share. See its `--help`.
