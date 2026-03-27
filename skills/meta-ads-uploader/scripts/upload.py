#!/usr/bin/env python3
"""
Meta Ads Creative Uploader — CLI
=================================
Validate, preview, and upload creative bundles to Meta Ads.

Usage:
    python upload.py validate <bundle.json>      # Check bundle (no API calls)
    python upload.py preview <bundle.json>       # Dry run — show what would happen
    python upload.py upload-media <bundle.json>  # Upload images/videos only
    python upload.py full <bundle.json>          # Full pipeline: media → creatives → ads (PAUSED)
    python upload.py status <bundle.json>        # Check status of previously uploaded bundle

Global flags:
    --quiet       Suppress progress messages
    --dry-run     Show what would happen without making API calls
"""

import argparse
import json
import sys
import time
from pathlib import Path

# Allow importing meta_api from same directory
sys.path.insert(0, str(Path(__file__).parent))

from meta_api import (
    MetaAdsClient, MetaAdsError, AuthError, CreativeError,
    CHAR_LIMITS, VALID_CTA_TYPES, VALID_FORMATS,
)


def load_bundle(bundle_path):
    """Load and return bundle JSON."""
    path = Path(bundle_path)
    if not path.exists():
        print(f"ERROR: Bundle not found: {path}", file=sys.stderr)
        sys.exit(1)
    with open(path) as f:
        return json.load(f), path


def results_path(bundle_path):
    """Return path for results sidecar file."""
    p = Path(bundle_path)
    return p.parent / f"{p.stem}_results.json"


def load_results(bundle_path):
    """Load existing results if available (for resume)."""
    rp = results_path(bundle_path)
    if rp.exists():
        with open(rp) as f:
            return json.load(f)
    return {}


def save_results(bundle_path, results):
    """Save results sidecar."""
    rp = results_path(bundle_path)
    with open(rp, "w") as f:
        json.dump(results, f, indent=2)
    return rp


def resolve_path(base_dir, relative_path):
    """Resolve a relative path from bundle's directory."""
    p = Path(relative_path)
    if p.is_absolute():
        return p
    return (base_dir / p).resolve()


# --- Commands ---

def cmd_validate(bundle, bundle_path, quiet=False):
    """Validate bundle structure and content (no API calls)."""
    errors = []
    warnings = []
    bundle_dir = bundle_path.parent

    # Required top-level fields
    for field in ["page_id", "ad_set_id", "creatives"]:
        if not bundle.get(field):
            errors.append(f"Missing required field: {field}")

    creatives = bundle.get("creatives", [])
    if not creatives:
        errors.append("No creatives defined")

    for i, c in enumerate(creatives):
        prefix = f"creative[{i}] ({c.get('name', 'unnamed')})"

        # Format check
        fmt = c.get("format", "")
        if fmt not in VALID_FORMATS:
            errors.append(f"{prefix}: invalid format '{fmt}'. Valid: {', '.join(VALID_FORMATS)}")

        # CTA check
        cta = c.get("cta_type", "LEARN_MORE")
        if cta not in VALID_CTA_TYPES:
            errors.append(f"{prefix}: invalid cta_type '{cta}'")

        # URL check
        if not c.get("link_url"):
            errors.append(f"{prefix}: missing link_url")

        # Asset path check
        if fmt == "single_image":
            img = c.get("image_path", "")
            if not img:
                errors.append(f"{prefix}: missing image_path")
            elif not resolve_path(bundle_dir, img).exists():
                errors.append(f"{prefix}: image not found: {img}")
        elif fmt == "single_video":
            vid = c.get("video_path", "")
            if not vid:
                errors.append(f"{prefix}: missing video_path")
            elif not resolve_path(bundle_dir, vid).exists():
                errors.append(f"{prefix}: video not found: {vid}")

        # Text presence
        if not c.get("primary_texts"):
            errors.append(f"{prefix}: missing primary_texts")
        if not c.get("headlines"):
            errors.append(f"{prefix}: missing headlines")

        # Character limit warnings
        for text in c.get("primary_texts", []):
            if len(text) > CHAR_LIMITS["primary_text"]:
                warnings.append(
                    f"{prefix}: primary_text exceeds {CHAR_LIMITS['primary_text']} chars "
                    f"({len(text)}): \"{text[:50]}...\""
                )
        for text in c.get("headlines", []):
            if len(text) > CHAR_LIMITS["headline"]:
                warnings.append(
                    f"{prefix}: headline exceeds {CHAR_LIMITS['headline']} chars "
                    f"({len(text)}): \"{text[:30]}...\""
                )
        for text in c.get("descriptions", []):
            if len(text) > CHAR_LIMITS["description"]:
                warnings.append(
                    f"{prefix}: description exceeds {CHAR_LIMITS['description']} chars "
                    f"({len(text)}): \"{text[:20]}...\""
                )

        # Dynamic vs static detection
        n_texts = len(c.get("primary_texts", []))
        n_heads = len(c.get("headlines", []))
        is_dynamic = n_texts > 1 or n_heads > 1
        if is_dynamic and not quiet:
            print(f"  {prefix}: dynamic creative ({n_texts} texts, {n_heads} headlines)")

    # Output
    if errors:
        print(f"\nVALIDATION FAILED — {len(errors)} error(s):")
        for e in errors:
            print(f"  ERROR: {e}")
    if warnings:
        print(f"\n{len(warnings)} warning(s):")
        for w in warnings:
            print(f"  WARN: {w}")
    if not errors:
        print(f"\nVALIDATION PASSED — {len(creatives)} creative(s), {len(warnings)} warning(s)")

    return len(errors) == 0


def cmd_preview(bundle, bundle_path, quiet=False):
    """Show what would be created (dry run, no API calls)."""
    if not cmd_validate(bundle, bundle_path, quiet=True):
        print("\nFix validation errors before previewing.")
        return False

    print(f"\n{'='*60}")
    print(f"BUNDLE: {bundle.get('bundle_name', bundle_path.stem)}")
    print(f"{'='*60}")
    print(f"  Page ID:       {bundle.get('page_id', 'N/A')}")
    print(f"  Instagram ID:  {bundle.get('instagram_actor_id', 'N/A')}")
    print(f"  Ad Set ID:     {bundle.get('ad_set_id', 'N/A')}")
    print(f"  URL Tags:      {bundle.get('url_tags', 'none')}")
    print(f"  Creatives:     {len(bundle.get('creatives', []))}")
    print()

    for i, c in enumerate(bundle.get("creatives", [])):
        n_texts = len(c.get("primary_texts", []))
        n_heads = len(c.get("headlines", []))
        mode = "DYNAMIC" if (n_texts > 1 or n_heads > 1) else "SINGLE"
        combos = n_texts * n_heads if mode == "DYNAMIC" else 1

        print(f"  [{i+1}] {c.get('name', 'unnamed')}")
        print(f"      Format:     {c.get('format', 'N/A')}")
        print(f"      Mode:       {mode} ({combos} combination{'s' if combos > 1 else ''})")
        print(f"      CTA:        {c.get('cta_type', 'LEARN_MORE')}")
        print(f"      URL:        {c.get('link_url', 'N/A')}")

        if c.get("format") == "single_image":
            print(f"      Image:      {c.get('image_path', 'N/A')}")
        elif c.get("format") == "single_video":
            print(f"      Video:      {c.get('video_path', 'N/A')}")
            if c.get("thumbnail_path"):
                print(f"      Thumbnail:  {c['thumbnail_path']}")

        for j, t in enumerate(c.get("primary_texts", [])):
            print(f"      Text [{j+1}]:    \"{t}\"")
        for j, h in enumerate(c.get("headlines", [])):
            print(f"      Head [{j+1}]:    \"{h}\"")
        for j, d in enumerate(c.get("descriptions", [])):
            print(f"      Desc [{j+1}]:    \"{d}\"")
        print()

    print(f"ACTIONS (would execute):")
    print(f"  1. Upload media assets")
    print(f"  2. Create {len(bundle.get('creatives', []))} creative(s)")
    print(f"  3. Create {len(bundle.get('creatives', []))} ad(s) — all PAUSED")
    print(f"  4. Save results to {results_path(bundle_path).name}")
    return True


def cmd_upload_media(bundle, bundle_path, client, dry_run=False):
    """Upload images/videos only. Returns results dict."""
    bundle_dir = bundle_path.parent
    results = load_results(bundle_path)
    media_results = results.get("media", {})

    for i, c in enumerate(bundle.get("creatives", [])):
        name = c.get("name", f"creative-{i}")

        # Skip if already uploaded
        if name in media_results and media_results[name].get("hash" if c.get("format") == "single_image" else "video_id"):
            print(f"  [{i+1}] {name}: already uploaded, skipping")
            continue

        if dry_run:
            print(f"  [{i+1}] {name}: would upload {c.get('format', 'unknown')}")
            continue

        try:
            if c.get("format") == "single_image":
                img_path = resolve_path(bundle_dir, c["image_path"])
                result = client.upload_image(img_path)
                media_results[name] = {"hash": result["hash"], "url": result.get("url", "")}
                print(f"  [{i+1}] {name}: image uploaded — hash: {result['hash']}")

            elif c.get("format") == "single_video":
                vid_path = resolve_path(bundle_dir, c["video_path"])
                result = client.upload_video(vid_path, title=name)
                media_results[name] = {"video_id": result["video_id"]}
                print(f"  [{i+1}] {name}: video uploaded — id: {result['video_id']}")

                # Upload thumbnail if provided
                if c.get("thumbnail_path"):
                    thumb_path = resolve_path(bundle_dir, c["thumbnail_path"])
                    thumb_result = client.upload_image(thumb_path)
                    media_results[name]["thumbnail_hash"] = thumb_result["hash"]
                    print(f"       thumbnail uploaded — hash: {thumb_result['hash']}")

        except MetaAdsError as e:
            media_results[name] = {"error": str(e)}
            print(f"  [{i+1}] {name}: FAILED — {e}")

    results["media"] = media_results
    if not dry_run:
        rp = save_results(bundle_path, results)
        print(f"\nMedia results saved to: {rp}")

    return results


def cmd_full(bundle, bundle_path, client, dry_run=False):
    """Full pipeline: upload media → create creatives → create ads (PAUSED)."""
    if not cmd_validate(bundle, bundle_path, quiet=True):
        print("Fix validation errors before running full pipeline.")
        return False

    page_id = bundle["page_id"]
    ad_set_id = bundle["ad_set_id"]
    instagram_actor_id = bundle.get("instagram_actor_id")
    url_tags = bundle.get("url_tags", "")

    print(f"\n--- Step 1/3: Upload Media ---")
    results = cmd_upload_media(bundle, bundle_path, client, dry_run=dry_run)

    print(f"\n--- Step 2/3: Create Creatives ---")
    creative_results = results.get("creatives", {})

    for i, c in enumerate(bundle.get("creatives", [])):
        name = c.get("name", f"creative-{i}")

        # Skip if already created
        if name in creative_results and creative_results[name].get("creative_id"):
            print(f"  [{i+1}] {name}: already created, skipping")
            continue

        # Check media was uploaded
        media = results.get("media", {}).get(name, {})
        if media.get("error"):
            creative_results[name] = {"error": f"Media upload failed: {media['error']}"}
            print(f"  [{i+1}] {name}: SKIPPED — media upload failed")
            continue

        if dry_run:
            print(f"  [{i+1}] {name}: would create creative")
            continue

        try:
            primary_texts = c.get("primary_texts", [])
            headlines = c.get("headlines", [])
            descriptions = c.get("descriptions", [])
            is_dynamic = len(primary_texts) > 1 or len(headlines) > 1

            if is_dynamic:
                # Dynamic creative with multiple variations
                result = client.create_creative_dynamic(
                    page_id=page_id,
                    image_hashes=[media["hash"]] if media.get("hash") else None,
                    video_ids=[media["video_id"]] if media.get("video_id") else None,
                    primary_texts=primary_texts,
                    headlines=headlines,
                    descriptions=descriptions,
                    link_url=c["link_url"],
                    cta_type=c.get("cta_type", "LEARN_MORE"),
                    name=name,
                    instagram_actor_id=instagram_actor_id,
                    url_tags=url_tags,
                )
            else:
                # Single creative
                result = client.create_creative_single(
                    page_id=page_id,
                    image_hash=media.get("hash"),
                    video_id=media.get("video_id"),
                    primary_text=primary_texts[0] if primary_texts else "",
                    headline=headlines[0] if headlines else "",
                    description=descriptions[0] if descriptions else "",
                    link_url=c["link_url"],
                    cta_type=c.get("cta_type", "LEARN_MORE"),
                    name=name,
                    instagram_actor_id=instagram_actor_id,
                    url_tags=url_tags,
                )

            creative_results[name] = {"creative_id": result["creative_id"]}
            print(f"  [{i+1}] {name}: creative created — id: {result['creative_id']}")

        except MetaAdsError as e:
            creative_results[name] = {"error": str(e)}
            print(f"  [{i+1}] {name}: FAILED — {e}")

    results["creatives"] = creative_results
    if not dry_run:
        save_results(bundle_path, results)

    print(f"\n--- Step 3/3: Create Ads (PAUSED) ---")
    ad_results = results.get("ads", {})

    for i, c in enumerate(bundle.get("creatives", [])):
        name = c.get("name", f"creative-{i}")

        # Skip if already created
        if name in ad_results and ad_results[name].get("ad_id"):
            print(f"  [{i+1}] {name}: ad already created, skipping")
            continue

        creative_data = creative_results.get(name, {})
        if not creative_data.get("creative_id"):
            ad_results[name] = {"error": "No creative ID — creative creation failed"}
            print(f"  [{i+1}] {name}: SKIPPED — no creative")
            continue

        if dry_run:
            print(f"  [{i+1}] {name}: would create ad (PAUSED)")
            continue

        try:
            result = client.create_ad(
                ad_set_id=ad_set_id,
                creative_id=creative_data["creative_id"],
                name=name,
                status="PAUSED",
            )
            ad_results[name] = {"ad_id": result["ad_id"]}
            print(f"  [{i+1}] {name}: ad created (PAUSED) — id: {result['ad_id']}")

        except MetaAdsError as e:
            ad_results[name] = {"error": str(e)}
            print(f"  [{i+1}] {name}: FAILED — {e}")

    results["ads"] = ad_results
    results["completed_at"] = time.strftime("%Y-%m-%d %H:%M:%S")

    if not dry_run:
        rp = save_results(bundle_path, results)
        print(f"\nAll results saved to: {rp}")

    # Summary
    total = len(bundle.get("creatives", []))
    ok_media = sum(1 for v in results.get("media", {}).values() if not v.get("error"))
    ok_creative = sum(1 for v in creative_results.values() if v.get("creative_id"))
    ok_ads = sum(1 for v in ad_results.values() if v.get("ad_id"))

    print(f"\n{'='*60}")
    print(f"SUMMARY: {ok_media}/{total} media, {ok_creative}/{total} creatives, {ok_ads}/{total} ads")
    if ok_ads == total:
        print("All ads created PAUSED. Review in Ads Manager, then activate.")
    elif ok_ads > 0:
        print("Some ads failed. Check results file, fix issues, and re-run (resumable).")
    else:
        print("No ads created. Check errors above.")
    print(f"{'='*60}")

    return ok_ads > 0


def cmd_status(bundle, bundle_path):
    """Show status of previously uploaded bundle."""
    results = load_results(bundle_path)
    if not results:
        print("No results file found. Run 'full' or 'upload-media' first.")
        return

    print(f"\nBundle: {bundle.get('bundle_name', bundle_path.stem)}")
    print(f"Completed: {results.get('completed_at', 'in progress')}")

    for section in ["media", "creatives", "ads"]:
        data = results.get(section, {})
        if not data:
            continue
        ok = sum(1 for v in data.values() if not v.get("error"))
        fail = sum(1 for v in data.values() if v.get("error"))
        print(f"\n{section.upper()}: {ok} OK, {fail} failed")
        for name, v in data.items():
            if v.get("error"):
                print(f"  {name}: ERROR — {v['error']}")
            elif v.get("hash"):
                print(f"  {name}: hash={v['hash']}")
            elif v.get("video_id"):
                print(f"  {name}: video_id={v['video_id']}")
            elif v.get("creative_id"):
                print(f"  {name}: creative_id={v['creative_id']}")
            elif v.get("ad_id"):
                print(f"  {name}: ad_id={v['ad_id']}")


# --- Main ---

def main():
    parser = argparse.ArgumentParser(
        description="Meta Ads Creative Uploader",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("command", choices=["validate", "preview", "upload-media", "full", "status"],
                        help="Command to run")
    parser.add_argument("bundle", help="Path to creative-bundle.json")
    parser.add_argument("--quiet", action="store_true", help="Suppress progress messages")
    parser.add_argument("--dry-run", action="store_true", help="Show what would happen")
    args = parser.parse_args()

    bundle, bundle_path = load_bundle(args.bundle)

    # Commands that don't need API
    if args.command == "validate":
        ok = cmd_validate(bundle, bundle_path, quiet=args.quiet)
        sys.exit(0 if ok else 1)

    if args.command == "preview":
        cmd_preview(bundle, bundle_path, quiet=args.quiet)
        sys.exit(0)

    if args.command == "status":
        cmd_status(bundle, bundle_path)
        sys.exit(0)

    # Commands that need API
    try:
        client = MetaAdsClient(quiet=args.quiet)
    except AuthError as e:
        print(f"AUTH ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    if args.command == "upload-media":
        cmd_upload_media(bundle, bundle_path, client, dry_run=args.dry_run)

    elif args.command == "full":
        ok = cmd_full(bundle, bundle_path, client, dry_run=args.dry_run)
        sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
