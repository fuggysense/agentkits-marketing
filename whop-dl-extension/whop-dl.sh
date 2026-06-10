#!/usr/bin/env bash
set -euo pipefail

URL="${1:?Usage: whop-dl.sh <m3u8-url> [output-name]}"
OUTPUT_BASE="${2:-video}"
VIDEO_FILE="${OUTPUT_BASE}.mp4"

for cmd in yt-dlp faster-whisper; do
  if ! command -v "$cmd" &>/dev/null; then
    echo "Error: $cmd not found. Install it first." >&2
    exit 1
  fi
done

echo "[1/2] Downloading stream → ${VIDEO_FILE}"
yt-dlp \
  --no-playlist \
  --concurrent-fragments 16 \
  -f "bv*+ba/b" \
  --merge-output-format mp4 \
  --postprocessor-args "ffmpeg:-movflags +faststart" \
  -o "$VIDEO_FILE" \
  "$URL"

echo "[2/2] Transcribing with faster-whisper..."
faster-whisper "$VIDEO_FILE" \
  --model large-v3 \
  --language en \
  --output_format txt \
  --output_dir .

echo "Done. Video: ${VIDEO_FILE} | Transcript: ${OUTPUT_BASE}.txt"
