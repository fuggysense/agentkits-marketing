#!/Library/Frameworks/Python.framework/Versions/3.14/bin/python3
"""Native messaging host for Whop Stream Grabber extension."""

import json
import struct
import subprocess
import sys
import tempfile
import os
import traceback

# Log to file for debugging (Opera swallows stderr)
LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "debug.log")

def log(msg):
    with open(LOG_FILE, "a") as f:
        f.write(msg + "\n")

log("=== Native host started ===")
log(f"Python: {sys.executable}")
log(f"PATH: {os.environ.get('PATH', 'NOT SET')}")

# Ensure common tool paths are available (Opera doesn't load shell profile)
os.environ["PATH"] = (
    "/usr/local/bin:/opt/homebrew/bin:/Library/Frameworks/Python.framework/Versions/3.14/bin:"
    + os.environ.get("PATH", "/usr/bin:/bin")
)

def read_message():
    raw_length = sys.stdin.buffer.read(4)
    log(f"Read raw_length: {len(raw_length) if raw_length else 0} bytes")
    if not raw_length or len(raw_length) < 4:
        return None
    length = struct.unpack("=I", raw_length)[0]
    log(f"Message length: {length}")
    data = sys.stdin.buffer.read(length)
    log(f"Read data: {len(data)} bytes")
    decoded = json.loads(data.decode("utf-8"))
    log(f"Decoded message: {json.dumps(decoded)[:200]}")
    return decoded

def send_message(msg):
    log(f"Sending: {json.dumps(msg)[:200]}")
    encoded = json.dumps(msg).encode("utf-8")
    sys.stdout.buffer.write(struct.pack("=I", len(encoded)))
    sys.stdout.buffer.write(encoded)
    sys.stdout.buffer.flush()

def transcribe_video(video_path):
    from faster_whisper import WhisperModel
    model = WhisperModel("base", device="cpu", compute_type="int8")
    segments, info = model.transcribe(video_path, language="en")
    lines = []
    for segment in segments:
        lines.append(segment.text.strip())
    return "\n".join(lines)

def main():
    try:
        msg = read_message()
    except Exception as e:
        log(f"read_message error: {traceback.format_exc()}")
        send_message({"error": f"Failed to read message: {str(e)}"})
        return

    if not msg:
        log("No message received")
        send_message({"error": "No message received"})
        return

    url = msg.get("url", "")
    action = msg.get("action", "transcribe")

    if not url:
        send_message({"error": "No URL provided"})
        return

    with tempfile.TemporaryDirectory() as tmpdir:
        video_path = os.path.join(tmpdir, "video.mp4")

        # Step 1: Download
        log(f"Starting yt-dlp download...")
        try:
            result = subprocess.run(
                [
                    "yt-dlp",
                    "--no-playlist",
                    "--concurrent-fragments", "16",
                    "-f", "bv*+ba/b",
                    "--merge-output-format", "mp4",
                    "--postprocessor-args", "ffmpeg:-movflags +faststart",
                    "-o", video_path,
                    url,
                ],
                capture_output=True,
                text=True,
                timeout=600,
            )
            if result.returncode != 0:
                log(f"yt-dlp failed: {result.stderr[:300]}")
                send_message({"error": f"yt-dlp failed: {result.stderr[:500]}"})
                return
        except FileNotFoundError:
            log("yt-dlp not found")
            send_message({"error": "yt-dlp not found. Install: brew install yt-dlp"})
            return
        except subprocess.TimeoutExpired:
            send_message({"error": "Download timed out (10 min limit)"})
            return

        log("Download complete")

        if action == "download":
            send_message({"status": "done", "transcript": ""})
            return

        # Step 2: Transcribe
        log("Starting transcription...")
        try:
            transcript = transcribe_video(video_path)
        except ImportError:
            log("faster-whisper not installed")
            send_message({"error": "faster-whisper not installed. Run: pip3 install faster-whisper"})
            return
        except Exception as e:
            log(f"Transcription error: {traceback.format_exc()}")
            send_message({"error": f"Transcription failed: {str(e)[:500]}"})
            return

        log(f"Transcription done, {len(transcript)} chars")
        send_message({"status": "done", "transcript": transcript})

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log(f"FATAL: {traceback.format_exc()}")
        try:
            send_message({"error": f"Fatal error: {str(e)}"})
        except:
            pass
