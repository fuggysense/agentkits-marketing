#!/usr/bin/env bash
# Mirror client-scoped session handoffs into the central _handoffs/mirror/ index.
#
# Why: handoffs get written next to the client they belong to (clients/<client>/SESSION-HANDOFF*.md
# and campaign _audit/session-handoff*). That keeps them with their context but scatters them.
# This copies the latest of each into _handoffs/mirror/ so a fresh session can find every client's
# last handoff in one place, without walking the whole tree.
#
# Idempotent: copies only when the source differs from the mirror (content compare). Running it
# twice in a row produces no second change. It NEVER deletes — orphaned mirror files (whose source
# moved or got archived, e.g. CODEX-HANDOFF-video-pipeline.md) are preserved on purpose.
#
# Read-only toward client folders. The only writes are into _handoffs/mirror/.
#
# Naming convention (matches the established mirror state):
#   clients/<client>/SESSION-HANDOFF*.md            -> mirror/<basename>
#   clients/<client>/**/_audit/session-handoff*.md  -> mirror/<client>-<basename>
#
# Usage: bash scripts/mirror_handoffs.sh

set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CLIENTS="$REPO/clients"
MIRROR="$REPO/_handoffs/mirror"

mkdir -p "$MIRROR"

copied=0
skipped=0

# copy_if_changed <src> <dst-basename>
copy_if_changed() {
  local src="$1" name="$2" dst
  dst="$MIRROR/$name"
  if [ -f "$dst" ] && cmp -s "$src" "$dst"; then
    skipped=$((skipped + 1))
    return
  fi
  cp "$src" "$dst"
  copied=$((copied + 1))
  echo "  mirrored: ${src#$REPO/} -> _handoffs/mirror/$name"
}

# 1) Top-level client SESSION-HANDOFF files (exclude _archive / _template*).
while IFS= read -r -d '' src; do
  copy_if_changed "$src" "$(basename "$src")"
done < <(find "$CLIENTS" \
  -path '*/_archive/*' -prune -o \
  -path '*/_template*' -prune -o \
  -mindepth 2 -maxdepth 2 -iname 'SESSION-HANDOFF*.md' -type f -print0)

# 2) Campaign _audit session-handoff files, prefixed with the client slug.
while IFS= read -r -d '' src; do
  rel="${src#$CLIENTS/}"
  client="${rel%%/*}"
  copy_if_changed "$src" "${client}-$(basename "$src")"
done < <(find "$CLIENTS" \
  -path '*/_archive/*' -prune -o \
  -path '*/_audit/*' -iname 'session-handoff*.md' -type f -print0)

echo "mirror_handoffs: $copied copied, $skipped unchanged. (orphaned mirror files preserved.)"
