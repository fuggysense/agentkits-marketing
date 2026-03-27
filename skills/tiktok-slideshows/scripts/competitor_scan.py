#!/usr/bin/env python3
"""
TikTok Competitor Scanner (ScrapeCreators API)
================================================
Scans competitor TikTok profiles, searches keywords, and finds trending
hashtags/sounds. Extracts outlier hooks for the hooks database.

Usage:
    python competitor_scan.py <project> --profiles @handle1 @handle2 --keywords "keyword1" "keyword2" [--scan-trending]
    python competitor_scan.py <project> --profiles @handle1 --keywords "keyword" --scan-trending
    python competitor_scan.py --help

Environment:
    SCRAPECREATORS_API_KEY  - API key from app.scrapecreators.com (required)

Outputs:
    - Scan report: clients/<project>/campaigns/tiktok-slideshows/competitor-scan-YYMMDD.md
    - Hooks-db append: clients/<project>/assets/video/hooks-db.md (deduped by video ID)

Get API key at: https://app.scrapecreators.com
Docs: https://docs.scrapecreators.com
Cost: 1 credit per API request
"""

import argparse
import json
import os
import re
import sys
import subprocess
from datetime import datetime
from pathlib import Path

# Import shared ScrapeCreators client
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scrapecreators" / "scripts"))
from api import ScrapeCreatorsClient, find_project_root, load_env, ScrapeCreatorsError


def get_date_stamp():
    """Get YYMMDD date stamp using shell date command for consistency."""
    try:
        result = subprocess.run(
            ["bash", "-c", "date +%y%m%d"],
            capture_output=True, text=True, timeout=5
        )
        return result.stdout.strip()
    except Exception:
        return datetime.now().strftime("%y%m%d")


def fetch_profile_videos(client, handle):
    """Fetch recent videos from a TikTok profile."""
    clean_handle = handle.lstrip("@")
    print(f"  Fetching videos for @{clean_handle}...")
    try:
        return client.tiktok_videos(clean_handle)
    except ScrapeCreatorsError as e:
        print(f"  API error: {e}")
        return []


def fetch_keyword_search(client, keyword):
    """Search TikTok videos by keyword."""
    print(f"  Searching keyword: '{keyword}'...")
    try:
        data = client.tiktok_search_keyword(keyword)
        if not data:
            return []
        return data.get("videos", data.get("data", []))
    except ScrapeCreatorsError as e:
        print(f"  API error: {e}")
        return []


def fetch_trending_hashtags(client):
    """Fetch popular TikTok hashtags."""
    print("  Fetching trending hashtags...")
    try:
        data = client.tiktok_popular_hashtags()
        if not data:
            return []
        return data.get("hashtags", data.get("data", []))
    except ScrapeCreatorsError as e:
        print(f"  API error: {e}")
        return []


def fetch_trending_sounds(client):
    """Fetch popular TikTok sounds."""
    print("  Fetching trending sounds...")
    try:
        data = client.tiktok_popular_songs()
        if not data:
            return []
        return data.get("songs", data.get("data", []))
    except ScrapeCreatorsError as e:
        print(f"  API error: {e}")
        return []


def extract_hook(caption):
    """Extract hook = first line of caption."""
    if not caption:
        return ""
    first_line = caption.split("\n")[0].strip()
    # Remove hashtags from hook
    first_line = re.sub(r"#\S+", "", first_line).strip()
    return first_line[:200]  # Cap at 200 chars


def calc_engagement(video):
    """Calculate engagement rate for a video."""
    stats = video.get("statistics", video.get("stats", {}))
    views = stats.get("playCount", stats.get("views", 0)) or 0
    likes = stats.get("diggCount", stats.get("likes", 0)) or 0
    shares = stats.get("shareCount", stats.get("shares", 0)) or 0
    comments = stats.get("commentCount", stats.get("comments", 0)) or 0

    if views == 0:
        return 0, views, likes, shares, comments

    eng_rate = (likes + shares + comments) / views * 100
    return eng_rate, views, likes, shares, comments


def extract_hashtags(video):
    """Extract hashtags from video."""
    text_extra = video.get("textExtra", video.get("text_extra", []))
    if isinstance(text_extra, list):
        return [t.get("hashtagName", t.get("hashtag", "")) for t in text_extra if t]
    desc = video.get("desc", video.get("description", ""))
    return re.findall(r"#(\S+)", desc)


def get_video_id(video):
    """Extract video ID."""
    return str(video.get("id", video.get("video_id", video.get("aweme_id", ""))))


def get_author(video):
    """Extract author handle."""
    author = video.get("author", {})
    if isinstance(author, dict):
        return author.get("uniqueId", author.get("username", "unknown"))
    return str(author) if author else "unknown"


def find_outliers(videos, multiplier=3.0):
    """Find videos with engagement rate >= multiplier * account average."""
    if not videos:
        return []

    # Group by author
    by_author = {}
    for v in videos:
        author = get_author(v)
        if author not in by_author:
            by_author[author] = []
        by_author[author].append(v)

    outliers = []
    for author, author_videos in by_author.items():
        rates = [calc_engagement(v)[0] for v in author_videos]
        avg_rate = sum(rates) / len(rates) if rates else 0

        for v in author_videos:
            eng_rate = calc_engagement(v)[0]
            if avg_rate > 0 and eng_rate >= avg_rate * multiplier:
                outliers.append((v, eng_rate, avg_rate))

    # Sort by engagement rate descending
    outliers.sort(key=lambda x: x[1], reverse=True)
    return outliers


def load_existing_hooks(hooks_path):
    """Load existing video IDs from hooks-db to prevent duplicates."""
    existing_ids = set()
    if hooks_path.exists():
        content = hooks_path.read_text()
        # Extract video IDs from "Video ID: xxxxx" pattern
        for match in re.finditer(r"Video ID:\s*(\S+)", content):
            existing_ids.add(match.group(1))
    return existing_ids


def generate_scan_report(all_videos, outliers, trending_hashtags, trending_sounds,
                         profiles, keywords, date_stamp):
    """Generate markdown scan report."""
    lines = [
        f"# Competitor Scan — {date_stamp}",
        "",
        f"> Profiles scanned: {', '.join(profiles) if profiles else 'none'}",
        f"> Keywords searched: {', '.join(keywords) if keywords else 'none'}",
        f"> Total videos analyzed: {len(all_videos)}",
        f"> Outliers found (3x+ avg engagement): {len(outliers)}",
        "",
        "---",
        "",
    ]

    # Top videos by engagement
    lines.append("## Top Videos by Engagement")
    lines.append("")
    lines.append("| # | Author | Hook | Views | Eng% | Likes | Shares |")
    lines.append("|---|--------|------|-------|------|-------|--------|")

    sorted_videos = sorted(all_videos, key=lambda v: calc_engagement(v)[0], reverse=True)
    for i, v in enumerate(sorted_videos[:20], 1):
        eng_rate, views, likes, shares, comments = calc_engagement(v)
        hook = extract_hook(v.get("desc", v.get("description", "")))
        author = get_author(v)
        lines.append(f"| {i} | @{author} | {hook[:60]}{'...' if len(hook) > 60 else ''} | {views:,} | {eng_rate:.1f}% | {likes:,} | {shares:,} |")

    lines.append("")
    lines.append("---")
    lines.append("")

    # Outlier hooks
    if outliers:
        lines.append("## Outlier Hooks (3x+ Account Average)")
        lines.append("")
        for v, eng_rate, avg_rate in outliers[:10]:
            hook = extract_hook(v.get("desc", v.get("description", "")))
            author = get_author(v)
            vid_id = get_video_id(v)
            _, views, likes, shares, comments = calc_engagement(v)
            hashtags = extract_hashtags(v)

            lines.append(f"### {hook or '(no caption)'}")
            lines.append(f"- **Author:** @{author} | **Video ID:** {vid_id}")
            lines.append(f"- **Views:** {views:,} | **Eng rate:** {eng_rate:.1f}% (account avg: {avg_rate:.1f}%)")
            lines.append(f"- **Likes:** {likes:,} | **Shares:** {shares:,} | **Comments:** {comments:,}")
            if hashtags:
                lines.append(f"- **Hashtags:** {', '.join('#' + h for h in hashtags[:10])}")
            lines.append("")

        lines.append("---")
        lines.append("")

    # Trending hashtags
    if trending_hashtags:
        lines.append("## Trending Hashtags")
        lines.append("")
        for h in trending_hashtags[:15]:
            name = h.get("name", h.get("hashtag", str(h)))
            views = h.get("views", h.get("viewCount", "?"))
            lines.append(f"- #{name} ({views} views)")
        lines.append("")
        lines.append("---")
        lines.append("")

    # Trending sounds
    if trending_sounds:
        lines.append("## Trending Sounds")
        lines.append("")
        for s in trending_sounds[:10]:
            title = s.get("title", s.get("name", str(s)))
            author = s.get("author", s.get("artist", "unknown"))
            lines.append(f"- **{title}** by {author}")
        lines.append("")

    return "\n".join(lines)


def generate_hooks_entries(outliers, existing_ids, date_stamp):
    """Generate hooks-db markdown entries for new outlier hooks."""
    entries = []
    for v, eng_rate, avg_rate in outliers:
        vid_id = get_video_id(v)
        if vid_id in existing_ids or not vid_id:
            continue

        hook = extract_hook(v.get("desc", v.get("description", "")))
        if not hook:
            continue

        author = get_author(v)
        _, views, likes, shares, comments = calc_engagement(v)

        entry = [
            f"### {hook}",
            f"- **Source:** @{author} | Video ID: {vid_id} (scraped {date_stamp})",
            f"- **Type:** TBD | **Power:** TBD",
            f"- **Views:** {views:,} | **Eng rate:** {eng_rate:.1f}%",
            f"- **Why it works:** [Claude fills post-scan]",
            f"- **Adapted for project:** [Claude fills post-scan]",
            f"- **Status:** Available",
            "",
        ]
        entries.append("\n".join(entry))
        existing_ids.add(vid_id)

    return entries


def ensure_hooks_db(hooks_path, template_path):
    """Create hooks-db from template if it doesn't exist."""
    if hooks_path.exists():
        return
    # Create parent dirs
    hooks_path.parent.mkdir(parents=True, exist_ok=True)
    if template_path.exists():
        import shutil
        shutil.copy2(template_path, hooks_path)
        print(f"  Created hooks-db from template: {hooks_path}")
    else:
        # Minimal scaffold
        hooks_path.write_text(
            "# Hooks Database\n\n"
            "## Manually Curated Hooks\n\n"
            "## Scraped Hooks\n\n"
            "## Used Hooks\n\n"
            "## Resting Hooks\n"
        )
        print(f"  Created empty hooks-db: {hooks_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Scan TikTok competitors via ScrapeCreators API"
    )
    parser.add_argument("project", help="Client project name (e.g., aura)")
    parser.add_argument(
        "--profiles", nargs="*", default=[],
        help="TikTok handles to scan (e.g., @lovebonito @charleskeith)"
    )
    parser.add_argument(
        "--keywords", nargs="*", default=[],
        help="Keywords to search (e.g., 'curated fashion singapore')"
    )
    parser.add_argument(
        "--scan-trending", action="store_true",
        help="Also fetch trending hashtags and sounds"
    )
    parser.add_argument(
        "--outlier-multiplier", type=float, default=3.0,
        help="Engagement multiplier for outlier detection (default: 3.0)"
    )

    args = parser.parse_args()

    # Setup
    root = find_project_root()
    if root is None:
        print("ERROR: Could not find project root (no CLAUDE.md found)")
        sys.exit(1)
    load_env(root)

    try:
        client = ScrapeCreatorsClient()
    except ScrapeCreatorsError as e:
        print(f"ERROR: {e}")
        sys.exit(1)

    date_stamp = get_date_stamp()
    client_path = root / "clients" / args.project
    campaign_path = client_path / "campaigns" / "tiktok-slideshows"
    hooks_path = client_path / "assets" / "video" / "hooks-db.md"
    template_path = root / "skills" / "tiktok-slideshows" / "templates" / "hooks-db-template.md"

    if not client_path.exists():
        print(f"ERROR: Client project not found: {client_path}")
        sys.exit(1)

    campaign_path.mkdir(parents=True, exist_ok=True)

    print(f"Competitor scan for: {args.project}")
    print(f"Date: {date_stamp}")
    print()

    # Collect all videos
    all_videos = []

    # Scan profiles
    for profile in args.profiles:
        videos = fetch_profile_videos(client, profile)
        print(f"    Found {len(videos)} videos")
        all_videos.extend(videos)

    # Search keywords
    for keyword in args.keywords:
        videos = fetch_keyword_search(client, keyword)
        print(f"    Found {len(videos)} results")
        all_videos.extend(videos)

    # Trending
    trending_hashtags = []
    trending_sounds = []
    if args.scan_trending:
        trending_hashtags = fetch_trending_hashtags(client) or []
        trending_sounds = fetch_trending_sounds(client) or []

    if not all_videos and not trending_hashtags and not trending_sounds:
        print("\nNo data retrieved. Check API key and handles.")
        sys.exit(1)

    # Find outliers
    outliers = find_outliers(all_videos, args.outlier_multiplier)
    print(f"\nFound {len(outliers)} outlier videos (>={args.outlier_multiplier}x avg engagement)")

    # Generate scan report
    report = generate_scan_report(
        all_videos, outliers, trending_hashtags, trending_sounds,
        args.profiles, args.keywords, date_stamp
    )
    report_path = campaign_path / f"competitor-scan-{date_stamp}.md"
    report_path.write_text(report)
    print(f"\nScan report: {report_path}")

    # Update hooks-db
    ensure_hooks_db(hooks_path, template_path)
    existing_ids = load_existing_hooks(hooks_path)
    new_entries = generate_hooks_entries(outliers, existing_ids, date_stamp)

    if new_entries:
        content = hooks_path.read_text()
        # Append under "## Scraped Hooks" section
        marker = "## Scraped Hooks"
        if marker in content:
            idx = content.index(marker) + len(marker)
            # Find next section or end
            next_section = content.find("\n## ", idx)
            if next_section == -1:
                insert_at = len(content)
            else:
                insert_at = next_section
            new_content = (
                content[:insert_at].rstrip()
                + "\n\n"
                + "\n".join(new_entries)
                + "\n"
                + content[insert_at:]
            )
        else:
            new_content = content + "\n\n## Scraped Hooks\n\n" + "\n".join(new_entries)

        hooks_path.write_text(new_content)
        print(f"Added {len(new_entries)} new hooks to: {hooks_path}")
    else:
        print("No new hooks to add (all already in database or no outliers)")

    print("\nDone. Next: Claude reads the scan report + hooks-db to categorize, explain, and adapt hooks.")


if __name__ == "__main__":
    main()
