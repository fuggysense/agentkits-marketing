#!/usr/bin/env bash
# Linkup API wrapper — sourced answers, citations, date/domain filtering, async research
# Usage: linkup.sh <command> [args]
# Requires: LINKUP_API_KEY env var, curl, jq

set -euo pipefail

# Load .env from project root if LINKUP_API_KEY not already set
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
if [[ -z "${LINKUP_API_KEY:-}" && -f "$PROJECT_ROOT/.env" ]]; then
  LINKUP_API_KEY=$(grep -E '^LINKUP_API_KEY=' "$PROJECT_ROOT/.env" 2>/dev/null | cut -d'=' -f2- | tr -d '"' || true)
  export LINKUP_API_KEY
fi

BASE_URL="https://api.linkup.so"
CONTENT_TYPE="Content-Type: application/json"

usage() {
  cat <<'EOF'
Usage: linkup.sh <command> [options]

Commands:
  search "query"           Web search with sourced answers
  research "query"         Start async deep research task
  research-status <id>     Poll async research task status
  fetch "url"              Fetch single URL content
  balance                  Check remaining API credits

Search options:
  --depth fast|standard|deep       Search depth (default: standard)
  --output searchResults|sourcedAnswer  Output type (default: sourcedAnswer)
  --citations                      Include inline citations
  --from YYYY-MM-DD                Filter results from date
  --to YYYY-MM-DD                  Filter results to date
  --include-domains "d1.com,d2.com"  Only search these domains
  --exclude-domains "d1.com,d2.com"  Exclude these domains
  --max-results N                  Max results (default: 5)

Research options:
  --citations              Include inline citations
  --from YYYY-MM-DD        Filter from date
  --to YYYY-MM-DD          Filter to date

Fetch options:
  --js                     Enable JavaScript rendering
EOF
  exit 0
}

require_api_key() {
  if [[ -z "${LINKUP_API_KEY:-}" ]]; then
    echo "ERROR: LINKUP_API_KEY not set. Export it in your shell profile." >&2
    exit 1
  fi
  AUTH_HEADER="Authorization: Bearer $LINKUP_API_KEY"
}

cmd_search() {
  require_api_key
  local query=""
  local depth="standard"
  local output_type="sourcedAnswer"
  local include_citations="false"
  local from_date=""
  local to_date=""
  local include_domains=""
  local exclude_domains=""
  local max_results=5

  if [[ $# -lt 1 ]]; then
    echo "ERROR: search requires a query argument" >&2
    exit 1
  fi
  query="$1"; shift

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --depth) depth="$2"; shift 2 ;;
      --output) output_type="$2"; shift 2 ;;
      --citations) include_citations="true"; shift ;;
      --from) from_date="$2"; shift 2 ;;
      --to) to_date="$2"; shift 2 ;;
      --include-domains) include_domains="$2"; shift 2 ;;
      --exclude-domains) exclude_domains="$2"; shift 2 ;;
      --max-results) max_results="$2"; shift 2 ;;
      *) echo "Unknown option: $1" >&2; exit 1 ;;
    esac
  done

  # Build JSON payload
  local json
  json=$(jq -n \
    --arg q "$query" \
    --arg d "$depth" \
    --arg ot "$output_type" \
    --argjson ic "$include_citations" \
    --argjson mr "$max_results" \
    '{q: $q, depth: $d, outputType: $ot, includeCitations: $ic, maxResults: $mr}')

  # Add optional date filters
  if [[ -n "$from_date" ]]; then
    json=$(echo "$json" | jq --arg f "$from_date" '. + {from: $f}')
  fi
  if [[ -n "$to_date" ]]; then
    json=$(echo "$json" | jq --arg t "$to_date" '. + {to: $t}')
  fi

  # Add optional domain filters
  if [[ -n "$include_domains" ]]; then
    json=$(echo "$json" | jq --arg d "$include_domains" '. + {includeDomains: ($d | split(","))}')
  fi
  if [[ -n "$exclude_domains" ]]; then
    json=$(echo "$json" | jq --arg d "$exclude_domains" '. + {excludeDomains: ($d | split(","))}')
  fi

  curl -s -X POST "$BASE_URL/v1/search" \
    -H "$AUTH_HEADER" \
    -H "$CONTENT_TYPE" \
    -d "$json"
}

cmd_research() {
  require_api_key
  local query=""
  local include_citations="false"
  local from_date=""
  local to_date=""

  if [[ $# -lt 1 ]]; then
    echo "ERROR: research requires a query argument" >&2
    exit 1
  fi
  query="$1"; shift

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --citations) include_citations="true"; shift ;;
      --from) from_date="$2"; shift 2 ;;
      --to) to_date="$2"; shift 2 ;;
      *) echo "Unknown option: $1" >&2; exit 1 ;;
    esac
  done

  local json
  json=$(jq -n \
    --arg q "$query" \
    --argjson ic "$include_citations" \
    --arg ot "sourcedAnswer" \
    '{q: $q, outputType: $ot, includeCitations: $ic}')

  if [[ -n "$from_date" ]]; then
    json=$(echo "$json" | jq --arg f "$from_date" '. + {from: $f}')
  fi
  if [[ -n "$to_date" ]]; then
    json=$(echo "$json" | jq --arg t "$to_date" '. + {to: $t}')
  fi

  curl -s -X POST "$BASE_URL/v1/research" \
    -H "$AUTH_HEADER" \
    -H "$CONTENT_TYPE" \
    -d "$json"
}

cmd_research_status() {
  require_api_key
  if [[ $# -lt 1 ]]; then
    echo "ERROR: research-status requires a task ID" >&2
    exit 1
  fi
  local task_id="$1"

  curl -s -X GET "$BASE_URL/v1/research/$task_id" \
    -H "$AUTH_HEADER"
}

cmd_fetch() {
  require_api_key
  local url=""
  local js_rendering="false"

  if [[ $# -lt 1 ]]; then
    echo "ERROR: fetch requires a URL argument" >&2
    exit 1
  fi
  url="$1"; shift

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --js) js_rendering="true"; shift ;;
      *) echo "Unknown option: $1" >&2; exit 1 ;;
    esac
  done

  local json
  json=$(jq -n \
    --arg u "$url" \
    --argjson js "$js_rendering" \
    '{url: $u, jsRendering: $js}')

  curl -s -X POST "$BASE_URL/v1/fetch" \
    -H "$AUTH_HEADER" \
    -H "$CONTENT_TYPE" \
    -d "$json"
}

cmd_balance() {
  require_api_key
  curl -s -X GET "$BASE_URL/v1/credits/balance" \
    -H "$AUTH_HEADER"
}

# Main dispatch
if [[ $# -lt 1 ]]; then
  usage
fi

command="$1"; shift

case "$command" in
  search) cmd_search "$@" ;;
  research) cmd_research "$@" ;;
  research-status) cmd_research_status "$@" ;;
  fetch) cmd_fetch "$@" ;;
  balance) cmd_balance ;;
  help|--help|-h) usage ;;
  *) echo "Unknown command: $command" >&2; usage ;;
esac
