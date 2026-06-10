#!/bin/bash
# Long-lived file watcher → runs scripts/link-skills.py when skills/ or agents/ change.
# Invoked by the com.jerel.marketing.link-skills LaunchAgent.
#
# fswatch:
#   -r             recursive
#   -l 2           2-second batching latency (debounce — many saves within 2s = one fire)
#   --event        only trigger on content changes (ignore touch/chmod)
#   -e             exclude regex (skip the auto-generated JSON + git internals)

set -u

MARKETING="/Users/jerel/Documents/Jerel's brain/jerel's brain/Marketing"
LINKER="$MARKETING/scripts/link-skills.py"
LOG_DIR="$HOME/Library/Logs/marketing-link-skills"
LOG="$LOG_DIR/watch.log"

mkdir -p "$LOG_DIR"

log() {
  printf '[%s] %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$*" >> "$LOG"
}

log "watcher starting (pid $$)"

FSWATCH="/opt/homebrew/bin/fswatch"
if [ ! -x "$FSWATCH" ]; then
  log "ERROR: fswatch not found at $FSWATCH"
  exit 1
fi

STAMP="$LOG_DIR/last-run.stamp"
COOLDOWN=8  # seconds after a run during which further events are ignored (kills the self-loop)

"$FSWATCH" \
  -r \
  -l 2 \
  --event Updated --event Created --event Removed --event Renamed \
  -e '\.claude/skill-graph\.json$' \
  -e '/\.git/' \
  -e '/\.obsidian/' \
  -e '/node_modules/' \
  "$MARKETING/skills" \
  "$MARKETING/agents" \
| while read -r changed; do
    case "$changed" in
      *"/SKILL.md"|*"/agents/"*.md) ;;
      *) continue ;;
    esac

    # Cooldown guard — skip events that land within N seconds of the last run.
    # This prevents the linker's own writes from retriggering itself.
    now=$(date +%s)
    if [ -f "$STAMP" ]; then
      last=$(cat "$STAMP" 2>/dev/null || echo 0)
      if [ $((now - last)) -lt $COOLDOWN ]; then
        continue
      fi
    fi

    log "change detected: $changed"
    date +%s > "$STAMP"
    if /Library/Frameworks/Python.framework/Versions/3.14/bin/python3 "$LINKER" >> "$LOG" 2>&1; then
      log "relink OK"
    else
      log "relink FAILED (exit $?)"
    fi
    date +%s > "$STAMP"
  done
