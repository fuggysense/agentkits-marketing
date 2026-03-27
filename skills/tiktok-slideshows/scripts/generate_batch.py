#!/usr/bin/env python3
"""
TikTok Slideshow Batch Generator
=================================
Generates 3:4 images for TikTok Photo Mode carousels using Gemini API.
Reads prompts from a JSON manifest, supports key rotation for 3x throughput.

Usage:
    python generate_batch.py <manifest.json> [--output-dir DIR] [--dry-run] [--retry-failed] [--pause SECONDS]

Manifest format (JSON):
    {
        "batch_name": "batch-01",
        "model": "gemini-3.1-flash-image-preview",
        "aspect_ratio": "3:4",
        "prompt_prefix": "Generate a high-quality marketing image for a TikTok Photo Mode carousel slide at 3:4 aspect ratio: ",
        "slides": [
            {"filename": "post01_slide1.png", "prompt": "..."},
            {"filename": "post01_slide2.png", "prompt": "..."}
        ]
    }

Environment:
    GEMINI_API_KEY    - Primary key (required)
    GEMINI_API_KEY_2  - Second key (optional, enables rotation)
    GEMINI_API_KEY_3  - Third key (optional, 3x throughput)
    ...up to GEMINI_API_KEY_9

Get keys at: https://aistudio.google.com/apikey
Each Google AI Studio project gets a free key. More keys = faster batches.
"""

import argparse
import base64
import json
import os
import sys
import time

try:
    import requests
except ImportError:
    print("ERROR: 'requests' package required. Install with: pip install requests")
    sys.exit(1)


API_BASE = "https://generativelanguage.googleapis.com/v1beta/models"


def load_env_file():
    """Load .env file from project root if it exists."""
    # Walk up from CWD looking for .env
    path = os.getcwd()
    for _ in range(10):
        env_path = os.path.join(path, ".env")
        if os.path.exists(env_path):
            with open(env_path) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, _, value = line.partition("=")
                        key, value = key.strip(), value.strip()
                        if key and key not in os.environ:
                            os.environ[key] = value
            return
        parent = os.path.dirname(path)
        if parent == path:
            break
        path = parent


def get_api_keys():
    """Load all available Gemini API keys for round-robin rotation."""
    load_env_file()
    keys = []
    primary = os.environ.get("GEMINI_API_KEY")
    if primary:
        keys.append(primary)
    for i in range(2, 10):
        k = os.environ.get(f"GEMINI_API_KEY_{i}")
        if k:
            keys.append(k)
    if not keys:
        print("ERROR: No GEMINI_API_KEY found in environment or .env file.")
        print("Set GEMINI_API_KEY in your .env or export it.")
        sys.exit(1)
    return keys


def generate_image(filename, prompt, index, total, keys, model, aspect_ratio, output_dir, prompt_prefix):
    """Generate a single image via Gemini API with key rotation."""
    key = keys[index % len(keys)]
    key_num = (index % len(keys)) + 1
    url = f"{API_BASE}/{model}:generateContent?key={key}"

    full_prompt = prompt_prefix + prompt

    payload = {
        "contents": [{"parts": [{"text": full_prompt}]}],
        "generationConfig": {
            "responseModalities": ["TEXT", "IMAGE"],
            "imageConfig": {"aspectRatio": aspect_ratio},
        },
    }

    try:
        resp = requests.post(url, json=payload, timeout=120)

        # Handle rate limiting with auto-retry
        if resp.status_code == 429:
            print(f"  RATE LIMITED (key {key_num}) — waiting 10s and retrying...")
            time.sleep(10)
            # Try next key
            alt_key = keys[(index + 1) % len(keys)]
            alt_url = f"{API_BASE}/{model}:generateContent?key={alt_key}"
            resp = requests.post(alt_url, json=payload, timeout=120)

        resp.raise_for_status()
        data = resp.json()

        candidates = data.get("candidates", [])
        if not candidates:
            print(f"  ERROR {index + 1}/{total}: {filename} — no candidates in response")
            return False

        parts = candidates[0].get("content", {}).get("parts", [])
        image_data = None
        for part in parts:
            if "inlineData" in part:
                image_data = part["inlineData"]["data"]
                break

        if not image_data:
            print(f"  ERROR {index + 1}/{total}: {filename} — no image data")
            for part in parts:
                if "text" in part:
                    print(f"    API: {part['text'][:200]}")
            return False

        filepath = os.path.join(output_dir, filename)
        os.makedirs(os.path.dirname(filepath) or output_dir, exist_ok=True)
        with open(filepath, "wb") as f:
            f.write(base64.b64decode(image_data))

        fsize = os.path.getsize(filepath)
        print(f"  OK {index + 1}/{total}: {filename} ({fsize:,} bytes) [key {key_num}/{len(keys)}]")
        return True

    except requests.exceptions.HTTPError as e:
        print(f"  ERROR {index + 1}/{total}: {filename} — HTTP {e.response.status_code}")
        print(f"    {e.response.text[:300]}")
        return False
    except Exception as e:
        print(f"  ERROR {index + 1}/{total}: {filename} — {type(e).__name__}: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="TikTok Slideshow Batch Generator")
    parser.add_argument("manifest", help="Path to JSON manifest file")
    parser.add_argument("--output-dir", "-o", help="Output directory (default: same dir as manifest)")
    parser.add_argument("--dry-run", action="store_true", help="Print prompts without generating")
    parser.add_argument("--retry-failed", action="store_true", help="Only regenerate missing/failed images")
    parser.add_argument("--pause", type=float, default=2.0, help="Seconds between API calls (default: 2)")
    parser.add_argument("--only", help="Generate only specific slides (comma-separated filenames)")
    args = parser.parse_args()

    with open(args.manifest) as f:
        manifest = json.load(f)

    batch_name = manifest.get("batch_name", "unnamed")
    model = manifest.get("model", "gemini-3.1-flash-image-preview")
    aspect_ratio = manifest.get("aspect_ratio", "3:4")
    prompt_prefix = manifest.get("prompt_prefix", "Generate a high-quality marketing image for a TikTok Photo Mode carousel slide at 3:4 aspect ratio: ")
    slides = manifest.get("slides", [])

    output_dir = args.output_dir or os.path.dirname(os.path.abspath(args.manifest))

    # Filter slides if --only or --retry-failed
    if args.only:
        only_set = set(args.only.split(","))
        slides = [s for s in slides if s["filename"] in only_set]

    if args.retry_failed:
        slides = [s for s in slides if not os.path.exists(os.path.join(output_dir, s["filename"]))]

    if not slides:
        print("No slides to generate.")
        return

    keys = get_api_keys()

    print(f"Batch: {batch_name}")
    print(f"Model: {model} | Aspect: {aspect_ratio}")
    print(f"Keys: {len(keys)} (round-robin)")
    print(f"Slides: {len(slides)} | Pause: {args.pause}s")
    print(f"Output: {output_dir}")
    print()

    if args.dry_run:
        for i, slide in enumerate(slides):
            print(f"  [{i + 1}] {slide['filename']}")
            print(f"      {slide['prompt'][:120]}...")
            print()
        print("DRY RUN — no images generated.")
        return

    os.makedirs(output_dir, exist_ok=True)
    success = 0
    failed = []

    for i, slide in enumerate(slides):
        ok = generate_image(
            slide["filename"],
            slide["prompt"],
            i,
            len(slides),
            keys,
            model,
            aspect_ratio,
            output_dir,
            prompt_prefix,
        )
        if ok:
            success += 1
        else:
            failed.append(slide["filename"])

        if i < len(slides) - 1:
            time.sleep(args.pause)

    print()
    print(f"Done! {success}/{len(slides)} succeeded, {len(failed)} failed.")
    if failed:
        print(f"Failed: {', '.join(failed)}")
        print(f"Re-run with --retry-failed to regenerate only the failures.")


if __name__ == "__main__":
    main()
