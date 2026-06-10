#!/bin/bash
# scaffold-client.sh — create a new client folder from _template/
# Usage: ./scripts/scaffold-client.sh <client-slug> "<Client Name>"
# Example: ./scripts/scaffold-client.sh michelle-koh "Michelle Koh"

set -euo pipefail

SLUG="${1:-}"
NAME="${2:-}"

if [[ -z "$SLUG" || -z "$NAME" ]]; then
  echo "Usage: $0 <client-slug> \"<Client Name>\""
  echo "  slug: lowercase, hyphens, no spaces (e.g. michelle-koh)"
  echo "  name: full display name (e.g. \"Michelle Koh\")"
  exit 1
fi

if [[ ! "$SLUG" =~ ^[a-z0-9][a-z0-9-]*$ ]]; then
  echo "ERROR: slug must be lowercase, hyphens only, no spaces. Got: $SLUG"
  exit 1
fi

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TEMPLATE="$REPO_ROOT/clients/_template"
TARGET="$REPO_ROOT/clients/$SLUG"

if [[ -d "$TARGET" ]]; then
  echo "ERROR: $TARGET already exists. Pick a different slug or rm the existing folder."
  exit 1
fi

if [[ ! -d "$TEMPLATE" ]]; then
  echo "ERROR: template not found at $TEMPLATE"
  exit 1
fi

# Guardrail: new clients must use the Jake-style marketing folder structure.
REQUIRED_DIRS=(
  "00_inputs"
  "00_inputs/product"
  "00_inputs/product/product-images"
  "00_inputs/market"
  "00_inputs/market/competitors"
  "00_inputs/market/competitors/ads"
  "00_inputs/research"
  "00_inputs/research/raw"
  "00_inputs/research/summaries"
  "00_inputs/research/winning-ads"
  "_brand"
  "_config"
  "_references"
  "_swipe/research"
  "_templates"
  "_templates/video-concept-workspace"
  "_templates/video-concept-workspace/01_strategy"
  "_templates/video-concept-workspace/02_ag1-options"
  "_templates/video-concept-workspace/03_scripts"
  "_templates/video-concept-workspace/04_input-images"
  "_templates/video-concept-workspace/05_prompt-packs"
  "_templates/video-concept-workspace/06_generation-runs"
  "_templates/video-concept-workspace/07_review"
  "campaigns/feedback"
  "output/deliverables"
)

REQUIRED_FILES=(
  "CLAUDE.md"
  "CONTEXT.md"
  "context-profile.json"
  "00_inputs/input-manifest.json"
  "_brand/buyer-profile.md"
  "campaigns/README.md"
  "campaigns/_campaigns-index.json"
  "_templates/video-concept-workspace/pipeline-state.json"
  "_templates/video-concept-workspace/artifact-manifest.json"
  "_templates/video-concept-workspace/concept-brief.json"
  "_templates/video-concept-workspace/event-log.jsonl"
  "_templates/video-concept-workspace/04_input-images/input-image-manifest.json"
)

for d in "${REQUIRED_DIRS[@]}"; do
  if [[ ! -d "$TEMPLATE/$d" ]]; then
    echo "ERROR: clients/_template is missing required Jake-style directory: $d"
    echo "Refusing to scaffold a new client from an incomplete template."
    exit 1
  fi
done

for f in "${REQUIRED_FILES[@]}"; do
  if [[ ! -f "$TEMPLATE/$f" ]]; then
    echo "ERROR: clients/_template is missing required Jake-style file: $f"
    echo "Refusing to scaffold a new client from an incomplete template."
    exit 1
  fi
done

echo "Scaffolding $SLUG ($NAME) from _template/..."
cp -r "$TEMPLATE" "$TARGET"

# Swap placeholders in all scaffold text contract files
TODAY=$(date +%Y-%m-%d)
find "$TARGET" -type f \( -name "*.md" -o -name "*.json" -o -name "*.jsonl" \) | while read -r f; do
  sed -i '' "s/{{client_slug}}/$SLUG/g" "$f"
  sed -i '' "s/{{client_name}}/$NAME/g" "$f"
  sed -i '' "s/{{today}}/$TODAY/g" "$f"
done

# Set _created date in context-profile.json
sed -i '' "s/\"_created\": \"\"/\"_created\": \"$TODAY\"/" "$TARGET/context-profile.json"

echo ""
echo "Done. Scaffold created at:"
echo "  $TARGET"
echo ""
echo "Next steps:"
echo "  1. Open clients/$SLUG/CLAUDE.md and fill in client-specific context"
echo "  2. Put raw client inputs in clients/$SLUG/00_inputs/"
echo "  3. Keep all buyer micro-personas in clients/$SLUG/_brand/buyer-profile.md"
echo "  4. Run /project:new $SLUG to start onboarding (Path A research-first or Path B interview-first)"
echo "  5. Or skip the skill and populate _brand/ + context-profile.json manually"
