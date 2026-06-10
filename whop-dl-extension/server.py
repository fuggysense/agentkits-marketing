#!/Library/Frameworks/Python.framework/Versions/3.14/bin/python3
"""Local transcription server for Whop Stream Grabber extension.
Start: python3 server.py
Stop:  Ctrl+C"""

import json
import subprocess
import tempfile
import os
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = 8765

os.environ["PATH"] = (
    "/usr/local/bin:/opt/homebrew/bin:/Library/Frameworks/Python.framework/Versions/3.14/bin:"
    + os.environ.get("PATH", "/usr/bin:/bin")
)

class Handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length))
        url = body.get("url", "")
        action = body.get("action", "transcribe")

        if not url:
            self.respond({"error": "No URL provided"})
            return

        print(f"\n→ {action}: {url[:80]}...")

        with tempfile.TemporaryDirectory() as tmpdir:
            video_path = os.path.join(tmpdir, "video.mp4")

            # Download
            print("  [1/2] Downloading...")
            try:
                result = subprocess.run(
                    ["yt-dlp", "--no-playlist", "--concurrent-fragments", "16",
                     "-f", "bv*+ba/b", "--merge-output-format", "mp4",
                     "--postprocessor-args", "ffmpeg:-movflags +faststart",
                     "-o", video_path, url],
                    capture_output=True, text=True, timeout=600,
                )
                if result.returncode != 0:
                    print(f"  ✗ yt-dlp error: {result.stderr[:200]}")
                    self.respond({"error": f"yt-dlp failed: {result.stderr[:500]}"})
                    return
            except FileNotFoundError:
                self.respond({"error": "yt-dlp not found"})
                return
            except subprocess.TimeoutExpired:
                self.respond({"error": "Download timed out"})
                return

            print("  ✓ Download complete")

            if action == "download":
                self.respond({"status": "done", "transcript": ""})
                return

            # Transcribe
            print("  [2/2] Transcribing...")
            try:
                from faster_whisper import WhisperModel
                model = WhisperModel("base", device="cpu", compute_type="int8")
                segments, info = model.transcribe(video_path, language="en")
                lines = [seg.text.strip() for seg in segments]
                transcript = "\n".join(lines)
            except ImportError:
                self.respond({"error": "faster-whisper not installed"})
                return
            except Exception as e:
                print(f"  ✗ Transcription error: {e}")
                self.respond({"error": f"Transcription failed: {str(e)[:500]}"})
                return

            # Always save to file as backup
            save_path = os.path.expanduser("~/Desktop/whop-transcript.txt")
            with open(save_path, "w") as f:
                f.write(transcript)
            # Auto-copy to clipboard
            subprocess.run(["pbcopy"], input=transcript.encode(), check=False)
            print(f"  ✓ Done — {len(transcript)} chars")
            print(f"  📄 Saved to {save_path}")
            print(f"  📋 Copied to clipboard")
            self.respond({"status": "done", "transcript": transcript})

    def respond(self, data):
        try:
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(data).encode())
        except BrokenPipeError:
            pass  # Browser closed connection — transcript already saved

    def log_message(self, format, *args):
        pass  # Suppress default request logging

if __name__ == "__main__":
    print(f"Whop Grabber server running on http://localhost:{PORT}")
    print("Press Ctrl+C to stop\n")
    try:
        HTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
