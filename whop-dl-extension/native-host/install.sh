#!/usr/bin/env bash
set -euo pipefail

# Install the native messaging host for Whop Stream Grabber.

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
HOST_NAME="com.whop_grabber.native"
HOST_SCRIPT="$SCRIPT_DIR/whop_grabber.py"

echo "Whop Stream Grabber — Native Host Installer"
echo ""

# Get the extension ID from the user
echo "To find your extension ID:"
echo "  1. Go to opera://extensions"
echo "  2. Enable Developer mode"
echo "  3. Find 'Whop Stream Grabber'"
echo "  4. Copy the ID (e.g., abcdefghijklmnopqrstuvwxyz)"
echo ""
read -p "Paste your extension ID: " EXT_ID

if [[ -z "$EXT_ID" ]]; then
  echo "Error: No extension ID provided"
  exit 1
fi

MANIFEST=$(cat <<EOF
{
  "name": "com.whop_grabber.native",
  "description": "Whop Stream Grabber - downloads and transcribes Whop course videos",
  "path": "$HOST_SCRIPT",
  "type": "stdio",
  "allowed_origins": ["chrome-extension://$EXT_ID/"]
}
EOF
)

# macOS install locations
if [[ "$OSTYPE" == "darwin"* ]]; then
  DIRS=(
    "$HOME/Library/Application Support/Google/Chrome/NativeMessagingHosts"
    "$HOME/Library/Application Support/Chromium/NativeMessagingHosts"
    "$HOME/Library/Application Support/com.operasoftware.Opera/NativeMessagingHosts"
  )
else
  DIRS=(
    "$HOME/.config/google-chrome/NativeMessagingHosts"
    "$HOME/.config/chromium/NativeMessagingHosts"
    "$HOME/.config/opera/NativeMessagingHosts"
  )
fi

for dir in "${DIRS[@]}"; do
  mkdir -p "$dir"
  echo "$MANIFEST" > "$dir/$HOST_NAME.json"
  echo "✓ Installed to: $dir/$HOST_NAME.json"
done

# Verify dependencies
echo ""
echo "Checking dependencies..."
for cmd in python3 yt-dlp; do
  if command -v "$cmd" &>/dev/null; then
    echo "  ✓ $cmd"
  else
    echo "  ✗ $cmd NOT FOUND"
  fi
done

# Check faster-whisper as Python library (not CLI)
if python3 -c "import faster_whisper" 2>/dev/null; then
  echo "  ✓ faster-whisper (Python library)"
else
  echo "  ✗ faster-whisper NOT FOUND — run: pip3 install faster-whisper"
fi

echo ""
echo "Done! Restart Opera and reload the extension."
