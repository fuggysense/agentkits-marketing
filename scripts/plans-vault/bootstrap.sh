#!/usr/bin/env bash
#
# bootstrap.sh — set up plans-vault working directory on this machine.
# Idempotent: safe to re-run after a repo pull.
#
# Creates ~/plans-vault/ and symlinks sync.sh + _admin from the repo.
# Working data (client folders + state) stays local, NOT in git.

set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HOME_DIR="${PLANS_VAULT_HOME:-$HOME/plans-vault}"

echo "==> Bootstrap plans-vault"
echo "    Repo:    $REPO_DIR"
echo "    Working: $HOME_DIR"

# Make working dir
mkdir -p "$HOME_DIR"

# Symlink sync.sh + _admin (force-replace existing symlinks; leave existing files alone)
if [ -L "$HOME_DIR/sync.sh" ] || [ ! -e "$HOME_DIR/sync.sh" ]; then
  ln -sf "$REPO_DIR/sync.sh" "$HOME_DIR/sync.sh"
  echo "    ✓ Symlinked sync.sh"
else
  echo "    ⚠ $HOME_DIR/sync.sh exists and is not a symlink — leaving alone."
  echo "      Move/delete it first if you want to replace with the repo version."
fi

if [ -L "$HOME_DIR/_admin" ] || [ ! -e "$HOME_DIR/_admin" ]; then
  ln -sf "$REPO_DIR/_admin" "$HOME_DIR/_admin"
  echo "    ✓ Symlinked _admin"
else
  echo "    ⚠ $HOME_DIR/_admin exists and is not a symlink — leaving alone."
fi

# Initialize state if missing
if [ ! -f "$HOME_DIR/_state.json" ]; then
  cat > "$HOME_DIR/_state.json" <<EOF
{
  "domain": "${PLANS_VAULT_DOMAIN:-plans.genflos.com}",
  "clients": {}
}
EOF
  echo "    ✓ Initialized _state.json"
else
  echo "    ✓ _state.json already present (left alone)"
fi

# Permissions
chmod +x "$REPO_DIR/sync.sh"
chmod +x "$REPO_DIR/bootstrap.sh"

echo ""
echo "✓ Bootstrap complete."
echo ""
echo "Next steps:"
echo "  1. Get a here.now API key (one-time):"
echo "       curl -sS https://here.now/api/auth/agent/request-code \\"
echo "         -H 'content-type: application/json' \\"
echo "         -d '{\"email\":\"YOUR_EMAIL\"}'"
echo "     Then verify with the code:"
echo "       curl -sS https://here.now/api/auth/agent/verify-code \\"
echo "         -H 'content-type: application/json' \\"
echo "         -d '{\"email\":\"YOUR_EMAIL\",\"code\":\"XXXX-XXXX\"}'"
echo "     Save the apiKey to ~/.herenow/credentials (chmod 600)."
echo ""
echo "  2. Register your custom domain (one-time):"
echo "       curl -sS https://here.now/api/v1/domains \\"
echo "         -H \"Authorization: Bearer \$(cat ~/.herenow/credentials)\" \\"
echo "         -H 'Content-Type: application/json' \\"
echo "         -d '{\"domain\":\"plans.YOUR-DOMAIN.com\"}'"
echo "     Add the CNAME (plans → fallback.here.now) at your DNS provider."
echo ""
echo "  3. Scaffold + publish your first client vault:"
echo "       $HOME_DIR/sync.sh --new acme-corp"
echo "       # edit ~/plans-vault/acme-corp/{plan,onb}/index.html"
echo "       $HOME_DIR/sync.sh acme-corp"
echo ""
echo "  4. (Optional) publish the admin UI manually for the first time:"
echo "       ~/.claude/skills/here-now/scripts/publish.sh \\"
echo "         $REPO_DIR/_admin --client claude-code/plans-vault-sync"
echo "       # then mount at /admin via the links API."
