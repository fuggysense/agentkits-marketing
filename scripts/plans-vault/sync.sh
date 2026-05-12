#!/usr/bin/env bash
#
# plans-vault sync — publishes a client's local vault folder to here.now
# and mounts it at plans.genflos.com/<client>.
#
# Usage:
#   ./sync.sh <client>              publish + mount/update
#   ./sync.sh --list                show all clients + their current mount
#   ./sync.sh --new <client>        scaffold a new client vault from _template/
#   ./sync.sh --unmount <client>    remove the mount (site stays)
#   ./sync.sh --delete <client>     unmount + delete the underlying site
#   ./sync.sh --refresh-admin       just regenerate the admin manifest + republish
#
# Architecture: this script lives in the Marketing repo at
# scripts/plans-vault/sync.sh. The working directory ($PLANS_VAULT_HOME,
# defaults to ~/plans-vault) holds per-client content + state. Run
# bootstrap.sh once on a new machine to symlink things up.

set -euo pipefail

# Resolve script's real location (chases through nested symlinks).
# Matters because publish.sh's `find $dir` doesn't traverse symlinks
# unless given the resolved target path.
SCRIPT_FILE="${BASH_SOURCE[0]}"
while [ -L "$SCRIPT_FILE" ]; do
  LINK_TARGET="$(readlink "$SCRIPT_FILE")"
  case "$LINK_TARGET" in
    /*) SCRIPT_FILE="$LINK_TARGET" ;;
    *)  SCRIPT_FILE="$(cd -P "$(dirname "$SCRIPT_FILE")" && pwd)/$LINK_TARGET" ;;
  esac
done
SCRIPT_DIR="$(cd -P "$(dirname "$SCRIPT_FILE")" && pwd)"

TEMPLATE_DIR="$SCRIPT_DIR/_template"
ADMIN_SRC_DIR="$SCRIPT_DIR/_admin"

# Working directory — where per-client content + state live
VAULT_HOME="${PLANS_VAULT_HOME:-$HOME/plans-vault}"
STATE="$VAULT_HOME/_state.json"

# here.now + auth
PUBLISH="$HOME/.claude/skills/here-now/scripts/publish.sh"
CRED="$HOME/.herenow/credentials"
DOMAIN="${PLANS_VAULT_DOMAIN:-plans.genflos.com}"
NOINDEX='<meta name="robots" content="noindex,nofollow,nosnippet,noarchive,noimageindex" />'

# Pre-flight
[ -d "$VAULT_HOME" ] || { echo "Missing $VAULT_HOME — run bootstrap.sh first."; exit 1; }
[ -d "$TEMPLATE_DIR" ] || { echo "Missing template at $TEMPLATE_DIR"; exit 1; }
[ -d "$ADMIN_SRC_DIR" ] || { echo "Missing admin source at $ADMIN_SRC_DIR"; exit 1; }
[ -f "$CRED" ] || { echo "Missing $CRED — run here.now signup first."; exit 1; }
[ -x "$PUBLISH" ] || { echo "Missing $PUBLISH"; exit 1; }
command -v jq >/dev/null || { echo "jq required"; exit 1; }
command -v curl >/dev/null || { echo "curl required"; exit 1; }

KEY=$(cat "$CRED")

# Init state if missing
if [ ! -f "$STATE" ]; then
  cat > "$STATE" <<EOF
{
  "domain": "$DOMAIN",
  "clients": {}
}
EOF
fi

inject_noindex() {
  local file="$1"
  if ! grep -q 'noindex' "$file" 2>/dev/null; then
    local tmp
    tmp=$(mktemp)
    sed "s|<head>|<head>\n${NOINDEX}|" "$file" > "$tmp"
    mv "$tmp" "$file"
  fi
}

extract_slug() {
  grep -oE 'https://[a-z0-9-]+\.here\.now/?' | head -1 \
    | sed -E 's|https://||; s|\.here\.now/?$||'
}

# publish.sh has a cosmetic bug where re-publishing unchanged content
# triggers "null upload" warnings + non-zero exit. Filter + tolerate.
run_publish() {
  local dir="$1"
  local maybe_slug="${2:-}"
  local args=("$dir" --client claude-code/plans-vault-sync)
  [ -n "$maybe_slug" ] && args+=(--slug "$maybe_slug")

  local out
  out=$("$PUBLISH" "${args[@]}" 2>&1 || true)
  echo "$out" | grep -v "missing local file for null" >&2

  if echo "$out" | grep -qE "error: [0-9]+ file\(s\) failed to upload" \
     && ! echo "$out" | grep -q "unchanged, skipped"; then
    echo "$out" >&2
    return 1
  fi

  echo "$out" | extract_slug
}

refresh_admin_manifest() {
  echo "==> Refreshing admin manifest..."

  local dom_json
  dom_json=$(curl -sS "https://here.now/api/v1/domains/$DOMAIN" \
    -H "Authorization: Bearer $KEY")

  local pubs_json
  pubs_json=$(curl -sS "https://here.now/api/v1/publishes" \
    -H "Authorization: Bearer $KEY")

  local clients_json="[]"
  for raw_dir in "$VAULT_HOME"/*/; do
    [ -d "$raw_dir" ] || continue
    local dir="${raw_dir%/}"
    local name
    name=$(basename "$dir")
    [ "${name:0:1}" = "_" ] && continue

    local slug
    slug=$(jq -r ".clients[\"$name\"].slug // \"\"" "$STATE")
    [ -z "$slug" ] && continue

    local subpaths="[]"
    local landing_path="$dir/index.html"
    if [ -f "$landing_path" ]; then
      subpaths=$(jq -n --arg p "/$name/" --arg url "https://$DOMAIN/$name/" --arg local "$landing_path" \
        '[{path: $p, url: $url, local_path: $local}]')
    fi

    while IFS= read -r idx; do
      local rel
      rel=$(echo "$idx" | sed "s|^$dir/||; s|/index\.html$||")
      [ -z "$rel" ] && continue
      subpaths=$(echo "$subpaths" | jq \
        --arg p "/$name/$rel/" \
        --arg url "https://$DOMAIN/$name/$rel/" \
        --arg local "$idx" \
        '. + [{path: $p, url: $url, local_path: $local}]')
    done < <(find "$dir" -mindepth 2 -type f -name "index.html" | sort)

    clients_json=$(echo "$clients_json" | jq \
      --arg name "$name" --arg slug "$slug" --arg dir "$dir" --argjson subs "$subpaths" \
      '. + [{mount_path: $name, slug: $slug, local_dir: $dir, subpaths: $subs}]')
  done

  local now
  now=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
  jq -n \
    --arg generated_at "$now" --arg domain "$DOMAIN" \
    --argjson clients "$clients_json" \
    --argjson all_mounts "$(echo "$dom_json" | jq '.mounts // []')" \
    --argjson all_publishes "$(echo "$pubs_json" | jq '.publishes // []')" \
    '{generated_at: $generated_at, domain: $domain, clients: $clients, all_mounts: $all_mounts, all_publishes: $all_publishes}' \
    > "$ADMIN_SRC_DIR/manifest.json"

  echo "    manifest written: $ADMIN_SRC_DIR/manifest.json"

  local admin_slug
  admin_slug=$(jq -r '.admin_slug // ""' "$STATE")
  if [ -z "$admin_slug" ]; then
    admin_slug=$(echo "$dom_json" | jq -r '.mounts[] | select(.mount_path == "admin") | .slug' | head -1)
    if [ -n "$admin_slug" ]; then
      jq --arg s "$admin_slug" '.admin_slug = $s' "$STATE" > "$STATE.tmp" && mv "$STATE.tmp" "$STATE"
    fi
  fi

  if [ -z "$admin_slug" ]; then
    echo "    WARN: no admin mount at /admin — skipping admin republish"
    echo "    To set up: run ./bootstrap.sh, or manually publish $ADMIN_SRC_DIR + mount at /admin"
    return 0
  fi

  echo "==> Republishing admin site ($admin_slug)..."
  run_publish "$ADMIN_SRC_DIR" "$admin_slug" > /dev/null
  echo "    admin updated: https://$DOMAIN/admin"
}

cmd_list() {
  echo "Domain: $DOMAIN"
  echo "Vault: $VAULT_HOME"
  echo "Script: $SCRIPT_DIR/sync.sh"
  echo ""
  echo "Local clients:"
  for d in "$VAULT_HOME"/*/; do
    [ -d "$d" ] || continue
    local name
    name=$(basename "$d")
    [ "${name:0:1}" = "_" ] && continue
    local slug
    slug=$(jq -r ".clients[\"$name\"].slug // \"(not published)\"" "$STATE")
    echo "  $name → https://$DOMAIN/$name  (slug: $slug)"
  done
  echo ""
  echo "Live mounts on here.now:"
  curl -sS "https://here.now/api/v1/domains/$DOMAIN" \
    -H "Authorization: Bearer $KEY" \
  | jq -r '.mounts[] | "  /\(.mount_path // "(root)") → \(.slug)"'
}

cmd_new() {
  local client="$1"
  local dir="$VAULT_HOME/$client"
  [ -d "$dir" ] && { echo "Already exists: $dir"; exit 1; }

  cp -R "$TEMPLATE_DIR" "$dir"
  find "$dir" -type f -name "*.html" -exec sed -i.bak "s/__CLIENT__/$client/g" {} \;
  find "$dir" -type f -name "*.bak" -delete

  echo "✓ Scaffolded $dir"
  echo ""
  echo "Files created:"
  find "$dir" -type f | sed "s|^|  |"
  echo ""
  echo "Next:"
  echo "  1. Replace $dir/plan/index.html with the real operator plan"
  echo "  2. Replace $dir/onb/index.html with the real client-facing onboarding"
  echo "  3. Edit $dir/index.html for custom landing"
  echo "  4. Run: $0 $client"
}

cmd_unmount() {
  local client="$1"
  echo "Unmounting /$client from $DOMAIN..."
  curl -sS -X DELETE "https://here.now/api/v1/links/$client?domain=$DOMAIN" \
    -H "Authorization: Bearer $KEY" | jq -c '.'
  jq "del(.clients[\"$client\"])" "$STATE" > "$STATE.tmp" && mv "$STATE.tmp" "$STATE"
  echo "Done. Underlying site still exists (use --delete to remove)."
  refresh_admin_manifest
}

cmd_delete() {
  local client="$1"
  local slug
  slug=$(jq -r ".clients[\"$client\"].slug // \"\"" "$STATE")
  echo "Unmounting /$client..."
  curl -sS -X DELETE "https://here.now/api/v1/links/$client?domain=$DOMAIN" \
    -H "Authorization: Bearer $KEY" | jq -c '.' || true
  jq "del(.clients[\"$client\"])" "$STATE" > "$STATE.tmp" && mv "$STATE.tmp" "$STATE"
  if [ -n "$slug" ]; then
    echo "Deleting underlying site $slug..."
    curl -sS -X DELETE "https://here.now/api/v1/publish/$slug" \
      -H "Authorization: Bearer $KEY" | jq -c '.'
  fi
  refresh_admin_manifest
}

cmd_sync() {
  local client="$1"
  local dir="$VAULT_HOME/$client"
  [ -d "$dir" ] || { echo "No vault folder: $dir"; echo "Hint: ./sync.sh --new $client"; exit 1; }

  echo "==> Injecting noindex meta into HTML files that don't have it..."
  while IFS= read -r f; do inject_noindex "$f"; done < <(find "$dir" -type f -name "*.html")
  find "$dir" -mindepth 1 -type d -empty -delete 2>/dev/null || true

  local existing_slug
  existing_slug=$(jq -r ".clients[\"$client\"].slug // \"\"" "$STATE")

  local slug
  echo ""
  if [ -n "$existing_slug" ]; then
    echo "==> Updating existing slug: $existing_slug"
    slug=$(run_publish "$dir" "$existing_slug") || { echo "Publish failed"; exit 1; }
    [ -z "$slug" ] && slug="$existing_slug"
  else
    echo "==> First publish for $client"
    slug=$(run_publish "$dir") || { echo "Publish failed"; exit 1; }
    echo "==> New slug: $slug"
    echo "==> Mounting at /$client on $DOMAIN..."
    curl -sS -X POST "https://here.now/api/v1/links" \
      -H "Authorization: Bearer $KEY" \
      -H "Content-Type: application/json" \
      -H "X-HereNow-Client: claude-code/plans-vault-sync" \
      -d "{\"location\":\"$client\",\"slug\":\"$slug\",\"domain\":\"$DOMAIN\"}" | jq -c '.'
  fi

  local now
  now=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
  jq ".clients[\"$client\"] = {slug: \"$slug\", mounted_at: (.clients[\"$client\"].mounted_at // \"$now\"), last_published: \"$now\"}" \
    "$STATE" > "$STATE.tmp" && mv "$STATE.tmp" "$STATE"

  echo ""
  echo "==> Smoke test:"
  sleep 2
  for sub in "" $(cd "$dir" && find . -mindepth 2 -name "index.html" -type f | sed -e 's|^\./||' -e 's|/index\.html$||' | sort); do
    local url="https://$DOMAIN/$client${sub:+/$sub}"
    local code
    code=$(curl -sSL -o /dev/null -w "%{http_code}" --max-time 10 "$url" || echo "---")
    printf "  %-60s  [%s]\n" "$url" "$code"
  done

  refresh_admin_manifest

  echo ""
  echo "✓ Sync complete."
  echo "  Live: https://$DOMAIN/$client"
  echo "  Admin: https://$DOMAIN/admin"
}

# Dispatch
case "${1:-}" in
  --list)            cmd_list ;;
  --new)             shift; cmd_new "${1:?usage: --new <client>}" ;;
  --unmount)         shift; cmd_unmount "${1:?usage: --unmount <client>}" ;;
  --delete)          shift; cmd_delete "${1:?usage: --delete <client>}" ;;
  --refresh-admin)   refresh_admin_manifest ;;
  -h|--help|"")      sed -n '2,/^set -euo pipefail$/p' "$0" | head -n 25 ;;
  *)                 cmd_sync "$1" ;;
esac
