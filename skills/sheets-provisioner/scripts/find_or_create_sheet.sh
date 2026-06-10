#!/usr/bin/env bash
# find_or_create_sheet.sh — registry-keyed find-or-create for client metrics sheets.
#
# Reads clients/<client>/_brand/metrics-config.json, looks up a campaign by slug:
#   - sheet already registered  -> prints its id (REUSE, no API call, no spend)
#   - not registered            -> creates via `gws` (human OAuth = jerel@genflos.com),
#                                  shares with the client's service account + ops,
#                                  writes the new block back into metrics-config.json
#
# Creation uses the gws CLI (Google Workspace CLI), NOT a service account — a bare
# service account cannot create Sheets (no Drive of its own). See the skill's
# references/sheet-auth.md for the two-identity model.
#
# Usage:
#   find_or_create_sheet.sh --client neezanizam --campaign buyer-funnel
#   find_or_create_sheet.sh --client neezanizam --campaign new-thing --title "NeezaNizam — New Thing"
#   find_or_create_sheet.sh --client neezanizam --campaign new-thing --copy-from 14bh8k6S... --title "..."
#   find_or_create_sheet.sh --client neezanizam --campaign new-thing --share "foo@bar.com=writer"
#   ... add --dry-run to print what it WOULD do without touching the API or the file.
#
# Output (stdout, last line, machine-parseable):  <status>\t<sheet_id>\t<sheet_url>
#   status = reused | created
set -euo pipefail

# --- repo root (this script lives at skills/sheets-provisioner/scripts/) ---
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"

CLIENT="" CAMPAIGN="" TITLE="" COPY_FROM="" SHARE_OVERRIDE="" DRY_RUN=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    --client)    CLIENT="$2"; shift 2 ;;
    --campaign)  CAMPAIGN="$2"; shift 2 ;;
    --title)     TITLE="$2"; shift 2 ;;
    --copy-from) COPY_FROM="$2"; shift 2 ;;
    --share)     SHARE_OVERRIDE="$2"; shift 2 ;;
    --dry-run)   DRY_RUN=1; shift ;;
    -h|--help)   sed -n '2,30p' "${BASH_SOURCE[0]}"; exit 0 ;;
    *) echo "unknown flag: $1" >&2; exit 2 ;;
  esac
done

[[ -z "$CLIENT"   ]] && { echo "ERROR: --client required" >&2; exit 2; }
[[ -z "$CAMPAIGN" ]] && { echo "ERROR: --campaign required" >&2; exit 2; }

CONFIG="$REPO_ROOT/clients/$CLIENT/_brand/metrics-config.json"
[[ -f "$CONFIG" ]] || { echo "ERROR: no metrics-config.json at $CONFIG" >&2; exit 1; }

# --- 1. REGISTRY LOOKUP (find) ---------------------------------------------
EXISTING_ID="$(jq -r --arg s "$CAMPAIGN" \
  '.campaigns[]? | select(.campaign_slug==$s) | .sheet_id // empty' "$CONFIG" | head -1)"

if [[ -n "$EXISTING_ID" ]]; then
  EXISTING_URL="$(jq -r --arg s "$CAMPAIGN" \
    '.campaigns[]? | select(.campaign_slug==$s) | .sheet_url // empty' "$CONFIG" | head -1)"
  [[ -z "$EXISTING_URL" ]] && EXISTING_URL="https://docs.google.com/spreadsheets/d/$EXISTING_ID/edit"
  echo "✓ '$CAMPAIGN' already has a sheet — reusing (no API call)." >&2
  printf 'reused\t%s\t%s\n' "$EXISTING_ID" "$EXISTING_URL"
  exit 0
fi

# --- 2. CREATE PATH --------------------------------------------------------
echo "→ '$CAMPAIGN' not in registry. Will create a new sheet." >&2
[[ -z "$TITLE" ]] && TITLE="$CLIENT — $CAMPAIGN"

# auth precheck — fail loud with the fix, not a cryptic 401 (skipped for --dry-run)
if [[ $DRY_RUN -eq 0 ]]; then
  AUTH_JSON="$(gws auth status 2>/dev/null | sed -n '/^{/,$p' || true)"
  TOKEN_VALID="$(echo "$AUTH_JSON" | jq -r '.token_valid // false' 2>/dev/null || echo false)"
  if [[ "$TOKEN_VALID" != "true" ]]; then
    echo "ERROR: gws token is not valid (token_valid=$TOKEN_VALID)." >&2
    echo "       Re-auth first:  gws auth login -s drive,sheets   (opens browser, approve as jerel@genflos.com)" >&2
    exit 1
  fi
fi

# resolve share targets: --share override wins, else .provisioning.share_editors[] from config
declare -a SHARE_PAIRS=()
if [[ -n "$SHARE_OVERRIDE" ]]; then
  IFS=',' read -ra SHARE_PAIRS <<< "$SHARE_OVERRIDE"   # "email=role,email=role"
else
  while IFS= read -r line; do SHARE_PAIRS+=("$line"); done < <(
    jq -r '.provisioning.share_editors[]? | "\(.email)=\(.role // "writer")"' "$CONFIG"
  )
fi
if [[ ${#SHARE_PAIRS[@]} -eq 0 ]]; then
  echo "WARN: no share targets (no --share and no .provisioning.share_editors in config)." >&2
  echo "      The metrics service account won't be able to write until you share manually." >&2
fi

if [[ $DRY_RUN -eq 1 ]]; then
  echo "[dry-run] would create '$TITLE'${COPY_FROM:+ (copy of $COPY_FROM)}" >&2
  echo "[dry-run] would share with: ${SHARE_PAIRS[*]:-<none>}" >&2
  echo "[dry-run] would append campaign '$CAMPAIGN' to $CONFIG" >&2
  printf 'created\t<dry-run-id>\t<dry-run-url>\n'
  exit 0
fi

# create: copy a template (preserves tabs) OR a blank workbook
if [[ -n "$COPY_FROM" ]]; then
  RESP="$(gws drive files copy \
    --params "$(jq -nc --arg f "$COPY_FROM" '{fileId:$f}')" \
    --json   "$(jq -nc --arg n "$TITLE" '{name:$n}')" --format json)"
  SHEET_ID="$(echo "$RESP" | jq -r '.id')"
else
  RESP="$(gws sheets spreadsheets create \
    --json "$(jq -nc --arg t "$TITLE" '{properties:{title:$t}}')" --format json)"
  SHEET_ID="$(echo "$RESP" | jq -r '.spreadsheetId')"
fi
[[ -z "$SHEET_ID" || "$SHEET_ID" == "null" ]] && { echo "ERROR: create returned no id. Raw: $RESP" >&2; exit 1; }
SHEET_URL="https://docs.google.com/spreadsheets/d/$SHEET_ID/edit"
echo "  created sheet $SHEET_ID" >&2

# share
for pair in "${SHARE_PAIRS[@]}"; do
  email="${pair%%=*}"; role="${pair#*=}"; [[ "$role" == "$email" ]] && role="writer"
  gws drive permissions create \
    --params "$(jq -nc --arg f "$SHEET_ID" '{fileId:$f,sendNotificationEmail:false}')" \
    --json   "$(jq -nc --arg r "$role" --arg e "$email" '{role:$r,type:"user",emailAddress:$e}')" \
    >/dev/null
  echo "  shared with $email ($role)" >&2
done

# --- 3. REGISTER (write back) ----------------------------------------------
TMP="$(mktemp)"
jq --arg slug "$CAMPAIGN" --arg id "$SHEET_ID" --arg url "$SHEET_URL" --arg label "$TITLE" \
  '.campaigns += [{campaign_slug:$slug, label:$label, sheet_id:$id, sheet_url:$url, tabs:{}}]' \
  "$CONFIG" > "$TMP" && mv "$TMP" "$CONFIG"
echo "  registered '$CAMPAIGN' in $CONFIG" >&2

printf 'created\t%s\t%s\n' "$SHEET_ID" "$SHEET_URL"
