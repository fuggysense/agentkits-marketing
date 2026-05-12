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

# Reserved client names — would collide with admin UI or other mount paths.
RESERVED_NAMES=(admin api _admin _template index root)

# Validate a client name against shell-/URL-/jq-safe regex and reserved list.
# Exits non-zero with a clear message if invalid.
validate_client_name() {
  local name="$1"
  if ! [[ "$name" =~ ^[a-z0-9](-?[a-z0-9])*$ ]]; then
    echo "Invalid client name: '$name'"
    echo "  Allowed: lowercase a-z, 0-9, internal hyphens. No leading/trailing/double hyphens."
    exit 1
  fi
  for r in "${RESERVED_NAMES[@]}"; do
    if [ "$name" = "$r" ]; then
      echo "Reserved client name: '$name' would shadow the $r mount."
      echo "  Pick a different slug (e.g. ${name}-co, ${name}-team)."
      exit 1
    fi
  done
}

# URL-encode a single path segment (keeps regex-safe but defends against future drift).
urlenc() {
  jq -nr --arg s "$1" '$s | @uri'
}

# Atomic state writer with single-flight guard.
# macOS lacks flock; we use a PID-bearing lockfile + staleness check (10 min).
LOCKFILE="$VAULT_HOME/.sync.lock"
acquire_lock() {
  if [ -f "$LOCKFILE" ]; then
    local pid mtime now age
    pid=$(cat "$LOCKFILE" 2>/dev/null || echo "")
    mtime=$(stat -f %m "$LOCKFILE" 2>/dev/null || stat -c %Y "$LOCKFILE" 2>/dev/null || echo 0)
    now=$(date +%s)
    age=$((now - mtime))
    if [ -n "$pid" ] && kill -0 "$pid" 2>/dev/null && [ "$age" -lt 600 ]; then
      echo "Another sync.sh is running (pid=$pid, age=${age}s). Aborting."
      echo "  If you're sure no other process is active, rm $LOCKFILE and retry."
      exit 1
    fi
  fi
  echo $$ > "$LOCKFILE"
  trap 'rm -f "$LOCKFILE"' EXIT INT TERM
}

# Init state if missing
if [ ! -f "$STATE" ]; then
  cat > "$STATE" <<EOF
{
  "domain": "$DOMAIN",
  "clients": {}
}
EOF
fi

# Validate state JSON before any operation reads it.
if ! jq empty "$STATE" >/dev/null 2>&1; then
  echo "ERROR: $STATE is corrupt (not valid JSON)."
  echo "  Recovery: inspect the file, fix manually, or restore from backup."
  echo "  Live mounts on here.now remain unaffected and can be listed via:"
  echo "    curl -sS https://here.now/api/v1/domains/$DOMAIN -H 'Authorization: Bearer \$KEY' | jq"
  exit 1
fi

# Atomic state writer — call via: write_state '<jq filter>'
write_state() {
  local filter="$1"
  shift
  local tmp
  tmp=$(mktemp "$STATE.XXXXXX")
  if jq "$@" "$filter" "$STATE" > "$tmp"; then
    mv "$tmp" "$STATE"
  else
    rm -f "$tmp"
    echo "ERROR: state write failed for filter: $filter"
    return 1
  fi
}

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

api_get() {
  # Wrapper that fails loudly on non-2xx instead of silently returning error JSON.
  local url="$1"
  local body
  local http_code
  body=$(curl -sS -w "\n%{http_code}" "$url" -H "Authorization: Bearer $KEY" || true)
  http_code=$(echo "$body" | tail -n1)
  body=$(echo "$body" | sed '$d')
  if [ "$http_code" != "200" ]; then
    echo "ERROR: GET $url returned HTTP $http_code" >&2
    echo "  Body: $body" >&2
    return 1
  fi
  echo "$body"
}

refresh_admin_manifest() {
  echo "==> Refreshing admin manifest..."

  local dom_json
  dom_json=$(api_get "https://here.now/api/v1/domains/$(urlenc "$DOMAIN")") || {
    echo "    Skipping manifest refresh — domain fetch failed."
    return 1
  }

  local pubs_json
  pubs_json=$(api_get "https://here.now/api/v1/publishes") || {
    echo "    Skipping manifest refresh — publishes fetch failed."
    return 1
  }

  local clients_json="[]"
  for raw_dir in "$VAULT_HOME"/*/; do
    [ -d "$raw_dir" ] || continue
    local dir="${raw_dir%/}"
    local name
    name=$(basename "$dir")
    [ "${name:0:1}" = "_" ] && continue

    local slug
    slug=$(jq -r --arg n "$name" '.clients[$n].slug // ""' "$STATE")
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
      write_state '.admin_slug = $s' --arg s "$admin_slug"
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
    slug=$(jq -r --arg n "$name" '.clients[$n].slug // "(not published)"' "$STATE")
    echo "  $name → https://$DOMAIN/$name  (slug: $slug)"
  done
  echo ""
  echo "Live mounts on here.now:"
  api_get "https://here.now/api/v1/domains/$(urlenc "$DOMAIN")" \
    | jq -r '.mounts[] | "  /\(.mount_path // "(root)") → \(.slug)"'
}

cmd_new() {
  local client="$1"
  validate_client_name "$client"
  local dir="$VAULT_HOME/$client"
  [ -d "$dir" ] && { echo "Already exists: $dir"; exit 1; }

  cp -R "$TEMPLATE_DIR" "$dir"
  # Use a sed delimiter that can't appear in a valid client name to defend
  # against future regex relaxation.
  find "$dir" -type f -name "*.html" -exec sed -i.bak "s|__CLIENT__|$client|g" {} \;
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
  validate_client_name "$client"
  acquire_lock
  echo "Unmounting /$client from $DOMAIN..."
  curl -sS --fail -X DELETE \
    "https://here.now/api/v1/links/$(urlenc "$client")?domain=$(urlenc "$DOMAIN")" \
    -H "Authorization: Bearer $KEY" | jq -c '.' || {
      echo "  WARN: DELETE failed (mount may already be gone — continuing)" >&2
    }
  write_state 'del(.clients[$n])' --arg n "$client"
  echo "Done. Underlying site still exists (use --delete to remove)."
  refresh_admin_manifest || true
}

cmd_delete() {
  local client="$1"
  validate_client_name "$client"
  acquire_lock
  local slug
  slug=$(jq -r --arg n "$client" '.clients[$n].slug // ""' "$STATE")
  echo "Unmounting /$client..."
  curl -sS -X DELETE \
    "https://here.now/api/v1/links/$(urlenc "$client")?domain=$(urlenc "$DOMAIN")" \
    -H "Authorization: Bearer $KEY" | jq -c '.' || true
  write_state 'del(.clients[$n])' --arg n "$client"
  if [ -n "$slug" ]; then
    echo "Deleting underlying site $slug..."
    curl -sS --fail -X DELETE \
      "https://here.now/api/v1/publish/$(urlenc "$slug")" \
      -H "Authorization: Bearer $KEY" | jq -c '.' || {
        echo "  WARN: site delete failed; orphan may remain at $slug.here.now" >&2
      }
  fi
  refresh_admin_manifest || true
}

cmd_sync() {
  local client="$1"
  validate_client_name "$client"
  acquire_lock
  local dir="$VAULT_HOME/$client"
  [ -d "$dir" ] || { echo "No vault folder: $dir"; echo "Hint: ./sync.sh --new $client"; exit 1; }

  echo "==> Injecting noindex meta into HTML files that don't have it..."
  while IFS= read -r f; do inject_noindex "$f"; done < <(find "$dir" -type f -name "*.html")
  find "$dir" -mindepth 1 -type d -empty -delete 2>/dev/null || true

  local existing_slug
  existing_slug=$(jq -r --arg n "$client" '.clients[$n].slug // ""' "$STATE")

  local slug
  echo ""
  if [ -n "$existing_slug" ]; then
    echo "==> Updating existing slug: $existing_slug"
    slug=$(run_publish "$dir" "$existing_slug") || { echo "Publish failed"; exit 1; }
    [ -z "$slug" ] && slug="$existing_slug"
  else
    echo "==> First publish for $client"
    slug=$(run_publish "$dir") || { echo "Publish failed"; exit 1; }
    if [ -z "$slug" ]; then
      echo "ERROR: publish.sh did not return a slug for first-time publish of '$client'."
      echo "  This usually means publish.sh stdout format changed (extract_slug returned empty)."
      echo "  Refusing to mount with an empty slug — state would loop on next sync."
      echo "  Inspect publish.sh output and update extract_slug() if its format drifted."
      exit 1
    fi
    echo "==> New slug: $slug"
    echo "==> Mounting at /$client on $DOMAIN..."
    local mount_payload
    mount_payload=$(jq -nc --arg loc "$client" --arg slug "$slug" --arg dom "$DOMAIN" \
      '{location: $loc, slug: $slug, domain: $dom}')
    curl -sS --fail -X POST "https://here.now/api/v1/links" \
      -H "Authorization: Bearer $KEY" \
      -H "Content-Type: application/json" \
      -H "X-HereNow-Client: claude-code/plans-vault-sync" \
      -d "$mount_payload" | jq -c '.' || {
        echo "ERROR: mount POST failed. Site published as $slug but not mounted." >&2
        exit 1
      }
  fi

  local now
  now=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
  write_state \
    '.clients[$n] = {slug: $slug, mounted_at: (.clients[$n].mounted_at // $now), last_published: $now}' \
    --arg n "$client" --arg slug "$slug" --arg now "$now"

  echo ""
  echo "==> Smoke test:"
  sleep 2
  local failures=0
  for sub in "" $(cd "$dir" && find . -mindepth 2 -name "index.html" -type f | sed -e 's|^\./||' -e 's|/index\.html$||' | sort); do
    local url="https://$DOMAIN/$client${sub:+/$sub}"
    local code
    code=$(curl -sSL -o /dev/null -w "%{http_code}" --max-time 10 "$url" || echo "---")
    printf "  %-60s  [%s]\n" "$url" "$code"
    case "$code" in
      2*) ;;
      *) failures=$((failures + 1)) ;;
    esac
  done

  refresh_admin_manifest || true

  echo ""
  if [ "$failures" -gt 0 ]; then
    echo "⚠ Sync finished with $failures non-2xx response(s)."
    echo "  here.now CDN propagation can take 5-30s — re-run smoke check in a minute."
  else
    echo "✓ Sync complete."
  fi
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
