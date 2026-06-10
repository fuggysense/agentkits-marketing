# Client Metrics Onboarding — Skill Plan (DRAFT, not built)

> Status: PLAN ONLY. Awaiting Jerel's go-ahead before any code is written.
> Date: 2026-06-07. Author: Claude session.

## Goal

Turn new-client onboarding for the Modal marketing-metrics cron into one guided
command, with guardrails that catch the common silent-failure modes (wrong ad
account, ungranted system user, campaign typo, sheet not shared) *before* a
client is told their dashboard is live.

## Honest framing — it is NOT truly "one-click"

Two steps cannot be eliminated by local code, confirmed by testing:

1. **Google sheet creation is blocked.** The service account
   (`neezanizam@neezanizam-492212.iam.gserviceaccount.com`) has zero Drive
   storage quota — `client.create()` returns `403 storageQuotaExceeded` (tested
   2026-06-07). Fixing this needs a paid Google Workspace + Shared Drive, which
   repo signals suggest you don't have. So a human must create a blank sheet and
   share it with the service-account email as Editor. One click in Drive.
2. **Meta access grant is external.** The shared system user must be able to read
   the client's ad account; that grant happens in Meta Business Manager. The
   `meta` CLI can *verify* it but cannot grant ad-account-level access.

So the realistic target is **"two clicks + one guided command,"** not zero-touch.
That is still a large reliability win over the current ad-hoc flow.

## Current state (Phase 0 — what already works)

- **Cron is multi-tenant.** One deployed Modal app, three schedules, loops every
  client in `clients/*/metrics-config.json` each run. No per-client cron.
  (`marketing_metrics.py:519-552`, schedules at :558/:573/:587.)
- **Provisioning is one command** that styles a sheet + builds 3 LP tabs + writes
  config: `provision_campaign.py`. Already supports `--sheet-id` to use an
  existing sheet (`:22, :255-258`) — this is the path that dodges the quota wall.
- **Sheet styling is already ~90% "branded"** in code: near-black headers,
  color-tinted columns, currency/percent/date formats, frozen rows, column
  widths (`provision_lp_tabs.py:_create_one_tab`, batch at :246).
- **Two shared Modal secrets**: `meta-ads` → `META_ADS_ACCESS_TOKEN`,
  `google-sheets` → `GOOGLE_CREDS_JSON`. Shared across all clients.
- Redeploy required after each new config (clients/ is baked into the image at
  build time, `marketing_metrics.py:42`).

## The guided flow (what the skill orchestrates)

Inputs the skill collects from Jerel (the judgment calls stay human):
- client-slug, campaign-slug, label
- ad-account-id (`act_…`)
- meta-campaign-id (optional filter) OR "account-level totals"
- the blank sheet ID (human-created + shared) — or skip styling if reusing one

Steps:
1. **Pre-flight (NEW, uses the `meta` CLI):**
   - `meta auth status` — token live?
   - `meta ads adaccount get <act_id>` — system user can actually see it? (fail
     fast with "grant access in Business Manager" if not)
   - if a campaign-id was given: `meta ads campaign get <id>` — exists + belongs
     to that account?
   - confirm the sheet is reachable by the service account (read its title).
2. **Provision:** run `provision_campaign.py … --sheet-id <id>`.
3. **Deploy:** `cd scripts/modal && modal deploy marketing_metrics.py`.
4. **Verify:** `modal run …::run_for_client --client-slug … --campaign-slug … --dry-run`,
   confirm Meta rows populate, return the sheet URL.
5. **Report:** what was created, the sheet link, and any manual step still owed.

## Branding extension (Path A — chosen over Shared Drive)

Build richer branding INTO `provision_lp_tabs.py` rather than fixing the broken
template-copy path. The master template adds almost nothing visual the code
can't reproduce; its only real extra (KPIs/CREATIVES/COPY/AVATARS tabs) was
already dropped from the active LP flow.

Scope, by effort:
- **Small:** tab color (`updateSheetProperties.tabColor`); brand font
  (`textFormat.fontFamily` on existing style requests).
- **Small:** conditional formatting (e.g. red CPFS over threshold) via
  `addConditionalFormatRule`.
- **Medium (optional):** a summary/cover tab with cross-sheet formulas, and/or a
  chart via `addChart`.
- **Medium (only if wanted):** `addProtectedRange` / `addNamedRange` for the
  agency-diagnostic columns.

Not doing: floating positioned logos (Sheets v4 API doesn't expose over-grid
images cleanly) and pivot tables (painful, not needed).

## Phased build plan (when greenlit)

- **Phase 1 — Pre-flight + wrapper.** Build the meta-CLI verification checks and
  the guided command that chains provision → deploy → dry-run. No styling
  changes. Decision gate: confirm the pre-flight catches a deliberately-wrong
  ad-account id. ≤5 files.
- **Phase 2 — Branding.** Extend `provision_lp_tabs.py` with the Small-tier items
  (tab color, font, conditional formatting). Test on a throwaway shared sheet.
  Decision gate: Jerel eyeballs the output before we add Medium-tier extras.
- **Phase 3 (optional) — Summary tab / charts.** Only if Phase 2 output warrants
  it.

Each phase verified before the next. No phase touches >5 files.

## Reality check / risks

- **Quota wall is permanent** without Workspace. The skill must treat
  "human-made shared sheet" as a required input, and fail loudly if the sheet
  isn't shared with the service account. Don't pretend auto-create works.
- **Redeploy is unavoidable** in the current image-mount model. Alternative
  (read clients/ from a live Modal Volume so no redeploy is needed) is a bigger
  refactor — out of scope for v1, note as a future option.
- **One shared Meta token for all clients** means every client's ad account must
  be added to a business the system user is on. Scaling past a handful of
  clients may warrant per-client tokens later — not now.
- **Effort:** Phase 1 small-medium, Phase 2 small. Total realistic: a focused
  session, not a project.

## Open questions for Jerel

1. Is there an existing per-client "blank sheet" creation SOP (a template you
   duplicate by hand), or should the skill output exact click-by-click
   instructions + the service-account email to share with?
2. Brand font/colors — do you have a defined palette/font, or use the current
   near-black/grey + tints?
3. Do you want the KPIs/CREATIVES/COPY/AVATARS tabs back as part of branding, or
   keep the lean LP-funnel-only sheet?
