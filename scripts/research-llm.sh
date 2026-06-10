#!/usr/bin/env bash
# Research LLM Router — delegates research/synthesis to cheaper LLMs (Kilo Gateway, Gemini CLI, Ollama local)
# Usage: research-llm.sh <provider> "prompt" [options]
# Requires: curl, jq. Optional: gemini CLI, KILO_API_KEY env var, Ollama running locally.

set -euo pipefail

# ============================================
# Default Models (easy to change)
# ============================================
KILO_DEFAULT_MODEL="minimax/minimax-m2.5"
KILO_ALT_MODEL="nvidia/nemotron-3-super-120b-a12b:free"
GEMINI_DEFAULT_MODEL="gemini-2.5-flash"
OLLAMA_DEFAULT_MODEL="qwen3:latest"

# ============================================
# Config
# ============================================
KILO_API_URL="https://api.kilo.ai/api/gateway/chat/completions"
OLLAMA_API_URL="${OLLAMA_HOST:-http://localhost:11434}"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Load .env from project root if KILO_API_KEY not already set
if [[ -z "${KILO_API_KEY:-}" && -f "$PROJECT_ROOT/.env" ]]; then
  KILO_API_KEY=$(grep -E '^KILO_API_KEY=' "$PROJECT_ROOT/.env" 2>/dev/null | cut -d'=' -f2- | tr -d '"' || true)
  export KILO_API_KEY
fi

# ============================================
# Usage
# ============================================
usage() {
  cat <<'EOF'
Usage: research-llm.sh <provider> "prompt" [options]

Providers:
  kilo     Route through Kilo Gateway (cheapest cloud)
  gemini   Route through Gemini CLI
  ollama   Route through local Ollama (free, private, offline)
  local    Alias for ollama
  auto     Try Kilo → Gemini → Ollama fallback chain
  list     List available Ollama models

Options:
  --model "model-id"     Override default model
  --system "prompt"      System prompt (default: research assistant)
  --max-tokens N         Max response tokens (default: 4096)
  --no-think             Disable thinking mode for Qwen3 (faster, shorter)

Default models:
  Kilo:   minimax/minimax-m2.5 (alt: nvidia/nemotron-3-super)
  Gemini: gemini-2.5-flash
  Ollama: qwen3:latest

Examples:
  research-llm.sh kilo "what are top B2B content formats in 2026"
  research-llm.sh kilo "summarize competitor strategies" --model "nvidia/nemotron-3-super"
  research-llm.sh gemini "summarize top 5 viral TikTok formats"
  research-llm.sh ollama "analyze this landing page copy"
  research-llm.sh ollama "quick summary" --model "qwen3:latest" --no-think
  research-llm.sh local "research prompt here"
  research-llm.sh list
  research-llm.sh auto "research prompt here"
EOF
  exit 0
}

# ============================================
# Output helper — consistent JSON format
# ============================================
output_json() {
  local provider="$1"
  local model="$2"
  local success="$3"
  local result="$4"
  local error="$5"
  local tokens="${6:-0}"

  jq -n -c \
    --arg p "$provider" \
    --arg m "$model" \
    --argjson s "$success" \
    --arg r "$result" \
    --arg e "$error" \
    --argjson t "$tokens" \
    '{provider:$p, model:$m, success:$s, result:$r, error:$e, tokens_used:$t}'
}

# ============================================
# Kilo Gateway
# ============================================
cmd_kilo() {
  local prompt="$1"
  local model="${2:-$KILO_DEFAULT_MODEL}"
  local system_prompt="${3:-You are a research assistant. Provide comprehensive, well-structured findings with specific details, numbers, and examples. Be exhaustive and cite sources when possible.}"
  local max_tokens="${4:-4096}"

  if [[ -z "${KILO_API_KEY:-}" ]]; then
    output_json "kilo" "$model" false "" "KILO_API_KEY not set. Export it or add to .env file."
    return 1
  fi

  local payload
  payload=$(jq -n -c \
    --arg m "$model" \
    --arg sys "$system_prompt" \
    --arg usr "$prompt" \
    --argjson mt "$max_tokens" \
    '{
      model: $m,
      messages: [
        {role: "system", content: $sys},
        {role: "user", content: $usr}
      ],
      max_tokens: $mt,
      temperature: 0.3
    }')

  local response
  response=$(curl -s -w "\n%{http_code}" -X POST "$KILO_API_URL" \
    -H "Authorization: Bearer $KILO_API_KEY" \
    -H "Content-Type: application/json" \
    -d "$payload" 2>&1) || true

  # Split response body and HTTP status code
  local http_code body
  http_code=$(echo "$response" | tail -1)
  body=$(echo "$response" | sed '$d')

  if [[ "$http_code" -ge 200 && "$http_code" -lt 300 ]]; then
    local content tokens
    content=$(echo "$body" | jq -r '.choices[0].message.content // empty' 2>/dev/null || true)
    tokens=$(echo "$body" | jq -r '.usage.total_tokens // 0' 2>/dev/null || echo "0")

    if [[ -n "$content" ]]; then
      output_json "kilo" "$model" true "$content" "null" "$tokens"
    else
      output_json "kilo" "$model" false "" "Empty response from Kilo Gateway. Raw: $(echo "$body" | head -c 200)"
      return 1
    fi
  else
    local err_msg
    err_msg=$(echo "$body" | jq -r '.error.message // .error // .message // empty' 2>/dev/null || echo "$body" | head -c 200)
    output_json "kilo" "$model" false "" "HTTP $http_code: $err_msg"
    return 1
  fi
}

# ============================================
# Gemini CLI
# ============================================
cmd_gemini() {
  local prompt="$1"
  local model="${2:-$GEMINI_DEFAULT_MODEL}"

  # Check if gemini CLI is available
  if ! command -v gemini &>/dev/null; then
    output_json "gemini" "$model" false "" "gemini CLI not found. Install: npm install -g @anthropic-ai/gemini-cli or see https://github.com/google-gemini/gemini-cli"
    return 1
  fi

  local result
  result=$(echo "$prompt" | gemini -y -m "$model" 2>&1) || {
    output_json "gemini" "$model" false "" "Gemini CLI error: $(echo "$result" | head -c 200)"
    return 1
  }

  if [[ -n "$result" ]]; then
    output_json "gemini" "$model" true "$result" "null" "0"
  else
    output_json "gemini" "$model" false "" "Empty response from Gemini CLI"
    return 1
  fi
}

# ============================================
# Ollama (local models — free, private, offline)
# ============================================
cmd_ollama() {
  local prompt="$1"
  local model="${2:-$OLLAMA_DEFAULT_MODEL}"
  local system_prompt="${3:-You are a research assistant. Provide comprehensive, well-structured findings with specific details, numbers, and examples. Be exhaustive and cite sources when possible.}"
  local max_tokens="${4:-4096}"
  local no_think="${5:-false}"

  # Check if Ollama is reachable
  if ! curl -s --max-time 2 "$OLLAMA_API_URL/api/tags" &>/dev/null; then
    output_json "ollama" "$model" false "" "Ollama not running. Start with: ollama serve"
    return 1
  fi

  # Build payload — Qwen3 thinking mode controlled via top-level "think" field
  local think_flag="true"
  if [[ "$no_think" == "true" ]]; then
    think_flag="false"
  fi

  local payload
  payload=$(jq -n -c \
    --arg m "$model" \
    --arg sys "$system_prompt" \
    --arg usr "$prompt" \
    --argjson mt "$max_tokens" \
    --argjson think "$think_flag" \
    '{
      model: $m,
      messages: [
        {role: "system", content: $sys},
        {role: "user", content: $usr}
      ],
      stream: false,
      think: $think,
      options: {
        num_predict: $mt
      }
    }')

  local response
  response=$(curl -s --max-time 300 -X POST "$OLLAMA_API_URL/api/chat" \
    -H "Content-Type: application/json" \
    -d "$payload" 2>&1) || {
    output_json "ollama" "$model" false "" "Ollama request failed: $(echo "$response" | head -c 200)"
    return 1
  }

  local content tokens
  content=$(echo "$response" | jq -r '.message.content // empty' 2>/dev/null || true)
  tokens=$(echo "$response" | jq -r '(.prompt_eval_count // 0) + (.eval_count // 0)' 2>/dev/null || echo "0")

  if [[ -n "$content" ]]; then
    output_json "ollama" "$model" true "$content" "null" "$tokens"
  else
    local err_msg
    err_msg=$(echo "$response" | jq -r '.error // empty' 2>/dev/null || echo "$response" | head -c 200)
    output_json "ollama" "$model" false "" "Empty response from Ollama. ${err_msg:+Error: $err_msg}"
    return 1
  fi
}

# ============================================
# List available Ollama models
# ============================================
cmd_list() {
  if ! curl -s --max-time 2 "$OLLAMA_API_URL/api/tags" &>/dev/null; then
    echo "Ollama not running. Start with: ollama serve" >&2
    return 1
  fi

  echo "Available Ollama models:"
  curl -s "$OLLAMA_API_URL/api/tags" | jq -r '.models[] | "  \(.name)\t\(.details.parameter_size // "?")\t\(.details.quantization_level // "")"' 2>/dev/null | column -t -s $'\t'
}

# ============================================
# Auto mode — try Kilo first, fall back to Gemini, then Ollama
# ============================================
cmd_auto() {
  local prompt="$1"
  local model="${2:-}"
  local system_prompt="${3:-}"
  local max_tokens="${4:-4096}"
  local no_think="${5:-false}"

  # Try Kilo first (cheapest cloud)
  if [[ -n "${KILO_API_KEY:-}" ]]; then
    local kilo_model="${model:-$KILO_DEFAULT_MODEL}"
    if cmd_kilo "$prompt" "$kilo_model" "$system_prompt" "$max_tokens" 2>/dev/null; then
      return 0
    fi
    echo "# Kilo failed, falling back to Gemini..." >&2
  else
    echo "# KILO_API_KEY not set, trying Gemini..." >&2
  fi

  # Fall back to Gemini
  local gemini_model="${model:-$GEMINI_DEFAULT_MODEL}"
  if cmd_gemini "$prompt" "$gemini_model" 2>/dev/null; then
    return 0
  fi
  echo "# Gemini failed, falling back to Ollama local..." >&2

  # Last resort — Ollama local
  local ollama_model="${model:-$OLLAMA_DEFAULT_MODEL}"
  cmd_ollama "$prompt" "$ollama_model" "$system_prompt" "$max_tokens" "$no_think"
}

# ============================================
# Main dispatch
# ============================================
if [[ $# -lt 1 ]]; then
  usage
fi

provider="$1"; shift

# Handle help and no-prompt commands before requiring prompt
case "$provider" in
  help|--help|-h) usage ;;
  list) cmd_list; exit $? ;;
esac

if [[ $# -lt 1 ]]; then
  echo "ERROR: prompt argument required" >&2
  usage
fi

prompt="$1"; shift

# Parse optional flags
model=""
system_prompt=""
max_tokens="4096"
no_think="false"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --model) model="$2"; shift 2 ;;
    --system) system_prompt="$2"; shift 2 ;;
    --max-tokens) max_tokens="$2"; shift 2 ;;
    --no-think) no_think="true"; shift ;;
    help|--help|-h) usage ;;
    *) echo "Unknown option: $1" >&2; exit 1 ;;
  esac
done

case "$provider" in
  kilo) cmd_kilo "$prompt" "${model:-$KILO_DEFAULT_MODEL}" "$system_prompt" "$max_tokens" ;;
  gemini) cmd_gemini "$prompt" "${model:-$GEMINI_DEFAULT_MODEL}" ;;
  ollama|local) cmd_ollama "$prompt" "${model:-$OLLAMA_DEFAULT_MODEL}" "$system_prompt" "$max_tokens" "$no_think" ;;
  auto) cmd_auto "$prompt" "$model" "$system_prompt" "$max_tokens" "$no_think" ;;
  list) cmd_list ;;
  *) echo "Unknown provider: $provider (use: kilo, gemini, ollama, local, auto, list)" >&2; exit 1 ;;
esac
