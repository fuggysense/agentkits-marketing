#!/usr/bin/env python3
"""
ScrapeCreators CLI — Universal Social Intelligence Tool
=======================================================
Command-line interface for the ScrapeCreators API.

Usage:
    python scrape.py tiktok profile <username>
    python scrape.py instagram posts <username>
    python scrape.py youtube search "ai marketing" --type video
    python scrape.py facebook ads-search "saas" --country US
    python scrape.py credits

Run `python scrape.py --help` for full command list.
"""

import argparse
import json
import sys
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parent))
from api import ScrapeCreatorsClient, ScrapeCreatorsError


def format_json(data):
    """Pretty-print JSON."""
    return json.dumps(data, indent=2, ensure_ascii=False, default=str)


def format_markdown_profile(data, platform):
    """Format a profile as markdown."""
    if not isinstance(data, dict):
        return format_json(data)

    # Try common profile field names
    d = data.get("data", data)
    if isinstance(d, dict):
        name = d.get("nickname", d.get("full_name", d.get("name", d.get("title", "Unknown"))))
        username = d.get("uniqueId", d.get("username", d.get("handle", "")))
        bio = d.get("signature", d.get("biography", d.get("bio", d.get("description", ""))))
        followers = d.get("followerCount", d.get("followers", d.get("follower_count", "?")))
        following = d.get("followingCount", d.get("following", d.get("following_count", "?")))
        likes = d.get("heartCount", d.get("likes", d.get("like_count", "")))
        posts = d.get("videoCount", d.get("posts", d.get("media_count", "")))
        verified = d.get("verified", d.get("is_verified", False))

        lines = [
            f"# {name} {'(verified)' if verified else ''}",
            f"**@{username}** on {platform}",
            "",
        ]
        if bio:
            lines.extend([f"> {bio}", ""])
        lines.append("| Metric | Value |")
        lines.append("|--------|-------|")
        lines.append(f"| Followers | {followers:,}" if isinstance(followers, int) else f"| Followers | {followers}")
        lines.append(f"| Following | {following:,}" if isinstance(following, int) else f"| Following | {following}")
        if likes:
            lines.append(f"| Likes | {likes:,}" if isinstance(likes, int) else f"| Likes | {likes}")
        if posts:
            lines.append(f"| Posts | {posts:,}" if isinstance(posts, int) else f"| Posts | {posts}")
        lines.append("")
        return "\n".join(lines)

    return format_json(data)


def format_markdown_list(data, item_type="item"):
    """Format a list of items as markdown."""
    if not isinstance(data, (dict, list)):
        return format_json(data)

    items = data
    if isinstance(data, dict):
        # Try common wrapper keys
        for key in ["videos", "data", "posts", "tweets", "results", "items",
                     "ads", "comments", "reels", "shorts", "hashtags", "songs",
                     "users", "companies", "followers", "following"]:
            if key in data:
                items = data[key]
                break

    if not isinstance(items, list):
        return format_json(data)

    if not items:
        return f"No {item_type}s found."

    lines = [f"# {len(items)} {item_type}(s) found", ""]

    for i, item in enumerate(items[:30], 1):  # Cap at 30 items
        if isinstance(item, dict):
            # Try to extract common fields
            title = item.get("desc", item.get("description", item.get("title",
                    item.get("text", item.get("caption", item.get("name", ""))))))
            if isinstance(title, str) and len(title) > 100:
                title = title[:100] + "..."

            author = item.get("author", {})
            if isinstance(author, dict):
                author = author.get("uniqueId", author.get("username", ""))

            # Stats
            stats = item.get("statistics", item.get("stats", {}))
            views = stats.get("playCount", stats.get("views", item.get("views", "")))
            likes = stats.get("diggCount", stats.get("likes", item.get("likes", "")))

            lines.append(f"### {i}. {title or '(no title)'}")
            if author:
                lines.append(f"- **Author:** @{author}")
            if views:
                lines.append(f"- **Views:** {views:,}" if isinstance(views, int) else f"- **Views:** {views}")
            if likes:
                lines.append(f"- **Likes:** {likes:,}" if isinstance(likes, int) else f"- **Likes:** {likes}")

            # Show ID if available
            item_id = item.get("id", item.get("video_id", item.get("shortcode", "")))
            if item_id:
                lines.append(f"- **ID:** {item_id}")
            lines.append("")
        else:
            lines.append(f"{i}. {item}")

    return "\n".join(lines)


def output_result(data, args, item_type="result"):
    """Format and output the result based on args."""
    if args.format == "json":
        text = format_json(data)
    elif item_type == "profile":
        text = format_markdown_profile(data, args.platform if hasattr(args, 'platform') else "")
    else:
        text = format_markdown_list(data, item_type)

    if args.output:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        Path(args.output).write_text(text)
        if not args.quiet:
            print(f"Written to: {args.output}", file=sys.stderr)
    else:
        print(text)


def detect_format(args):
    """Auto-detect format: json if piped, markdown if TTY."""
    if hasattr(args, 'format') and args.format:
        return args.format
    return "markdown" if sys.stdout.isatty() else "json"


# ==========================================
# Subcommand handlers
# ==========================================

def cmd_tiktok(args, client):
    args.platform = "TikTok"
    cmd = args.tiktok_cmd

    if cmd == "profile":
        output_result(client.tiktok_profile(args.username), args, "profile")
    elif cmd == "audience":
        output_result(client.tiktok_audience(args.username), args, "audience")
    elif cmd == "videos":
        if args.pages and args.pages > 1:
            data = client.tiktok_videos_all(args.username, max_pages=args.pages)
        else:
            data = client.tiktok_videos(args.username)
        output_result(data if isinstance(data, dict) else {"videos": data}, args, "video")
    elif cmd == "video":
        output_result(client.tiktok_video(args.video_id), args, "video")
    elif cmd == "transcript":
        output_result(client.tiktok_transcript(args.video_id), args, "transcript")
    elif cmd == "comments":
        output_result(client.tiktok_comments(args.video_id), args, "comment")
    elif cmd == "search":
        if args.type == "top":
            output_result(client.tiktok_search_top(args.query), args, "result")
        elif args.type == "hashtag":
            output_result(client.tiktok_search_hashtag(args.query), args, "result")
        elif args.type == "users":
            output_result(client.tiktok_search_users(args.query), args, "user")
        else:
            output_result(client.tiktok_search_keyword(args.query), args, "video")
    elif cmd == "trending":
        if args.hashtags:
            output_result(client.tiktok_popular_hashtags(), args, "hashtag")
        elif args.sounds:
            output_result(client.tiktok_popular_songs(), args, "song")
        elif args.creators:
            output_result(client.tiktok_popular_creators(), args, "creator")
        elif args.feed:
            output_result(client.tiktok_trending_feed(), args, "video")
        else:
            output_result(client.tiktok_popular_videos(), args, "video")
    elif cmd == "shop":
        output_result(client.tiktok_shop_search(args.query), args, "product")
    elif cmd == "song":
        if args.videos:
            output_result(client.tiktok_song_videos(args.song_id), args, "video")
        else:
            output_result(client.tiktok_song(args.song_id), args, "song")
    elif cmd == "following":
        output_result(client.tiktok_following(args.username), args, "user")
    elif cmd == "followers":
        output_result(client.tiktok_followers(args.username), args, "user")
    elif cmd == "live":
        output_result(client.tiktok_live(args.username), args, "live")


def cmd_instagram(args, client):
    args.platform = "Instagram"
    cmd = args.instagram_cmd

    if cmd == "profile":
        output_result(client.instagram_profile(args.username), args, "profile")
    elif cmd == "posts":
        output_result(client.instagram_posts(args.username), args, "post")
    elif cmd == "post":
        output_result(client.instagram_post(args.shortcode), args, "post")
    elif cmd == "transcript":
        output_result(client.instagram_transcript(args.shortcode), args, "transcript")
    elif cmd == "comments":
        output_result(client.instagram_comments(args.shortcode), args, "comment")
    elif cmd == "reels":
        output_result(client.instagram_reels(args.username), args, "reel")
    elif cmd == "search-reels":
        output_result(client.instagram_search_reels(args.query), args, "reel")
    elif cmd == "highlights":
        output_result(client.instagram_highlights(args.username), args, "highlight")


def cmd_youtube(args, client):
    args.platform = "YouTube"
    cmd = args.youtube_cmd

    if cmd == "channel":
        output_result(client.youtube_channel(args.channel_id), args, "profile")
    elif cmd == "videos":
        output_result(client.youtube_channel_videos(args.channel_id), args, "video")
    elif cmd == "shorts":
        output_result(client.youtube_channel_shorts(args.channel_id), args, "short")
    elif cmd == "video":
        output_result(client.youtube_video(args.video_id), args, "video")
    elif cmd == "transcript":
        output_result(client.youtube_transcript(args.video_id), args, "transcript")
    elif cmd == "search":
        output_result(client.youtube_search(args.query, args.type), args, "result")
    elif cmd == "comments":
        output_result(client.youtube_comments(args.video_id), args, "comment")
    elif cmd == "trending-shorts":
        output_result(client.youtube_trending_shorts(), args, "short")
    elif cmd == "playlist":
        output_result(client.youtube_playlist(args.playlist_id), args, "video")


def cmd_twitter(args, client):
    args.platform = "Twitter/X"
    cmd = args.twitter_cmd

    if cmd == "profile":
        output_result(client.twitter_profile(args.username), args, "profile")
    elif cmd == "tweets":
        output_result(client.twitter_tweets(args.username), args, "tweet")
    elif cmd == "tweet":
        output_result(client.twitter_tweet(args.tweet_id), args, "tweet")
    elif cmd == "transcript":
        output_result(client.twitter_transcript(args.tweet_id), args, "transcript")


def cmd_facebook(args, client):
    args.platform = "Facebook"
    cmd = args.facebook_cmd

    if cmd == "profile":
        output_result(client.facebook_profile(args.username), args, "profile")
    elif cmd == "posts":
        output_result(client.facebook_posts(args.username), args, "post")
    elif cmd == "reels":
        output_result(client.facebook_reels(args.username), args, "reel")
    elif cmd == "ads-search":
        output_result(client.facebook_ads_search(args.query, args.country), args, "ad")
    elif cmd == "company-ads":
        output_result(client.facebook_company_ads(args.company), args, "ad")
    elif cmd == "group":
        output_result(client.facebook_group_posts(args.group_id), args, "post")


def cmd_linkedin(args, client):
    args.platform = "LinkedIn"
    cmd = args.linkedin_cmd

    if cmd == "profile":
        output_result(client.linkedin_profile(args.url), args, "profile")
    elif cmd == "company":
        output_result(client.linkedin_company(args.url), args, "profile")
    elif cmd == "company-posts":
        output_result(client.linkedin_company_posts(args.url), args, "post")
    elif cmd == "post":
        output_result(client.linkedin_post(args.url), args, "post")
    elif cmd == "ads":
        output_result(client.linkedin_ads_search(args.query), args, "ad")


def cmd_reddit(args, client):
    args.platform = "Reddit"
    cmd = args.reddit_cmd

    if cmd == "subreddit":
        output_result(client.reddit_subreddit_posts(args.name), args, "post")
    elif cmd == "subreddit-details":
        output_result(client.reddit_subreddit_details(args.name), args, "profile")
    elif cmd == "search":
        output_result(client.reddit_search(args.query), args, "post")
    elif cmd == "subreddit-search":
        output_result(client.reddit_subreddit_search(args.name, args.query), args, "post")
    elif cmd == "comments":
        output_result(client.reddit_post_comments(args.post_id), args, "comment")


def cmd_threads(args, client):
    args.platform = "Threads"
    cmd = args.threads_cmd

    if cmd == "profile":
        output_result(client.threads_profile(args.username), args, "profile")
    elif cmd == "posts":
        output_result(client.threads_posts(args.username), args, "post")
    elif cmd == "search":
        output_result(client.threads_search_users(args.query), args, "user")


def cmd_bluesky(args, client):
    args.platform = "Bluesky"
    cmd = args.bluesky_cmd

    if cmd == "profile":
        output_result(client.bluesky_profile(args.handle), args, "profile")
    elif cmd == "posts":
        output_result(client.bluesky_posts(args.handle), args, "post")


def cmd_pinterest(args, client):
    args.platform = "Pinterest"
    cmd = args.pinterest_cmd

    if cmd == "search":
        output_result(client.pinterest_search(args.query), args, "pin")
    elif cmd == "boards":
        output_result(client.pinterest_boards(args.username), args, "board")


def cmd_google(args, client):
    args.platform = "Google"
    cmd = args.google_cmd

    if cmd == "search":
        output_result(client.google_search(args.query), args, "result")
    elif cmd == "company-ads":
        output_result(client.google_company_ads(args.company), args, "ad")
    elif cmd == "advertisers":
        output_result(client.google_advertisers_search(args.query), args, "advertiser")


def cmd_credits(args, client):
    data = client.credit_balance()
    if args.format == "json":
        print(format_json(data))
    else:
        balance = data.get("credits", data.get("balance", data.get("data", data)))
        print(f"Credit balance: {balance}")


# ==========================================
# Argument parser
# ==========================================

def build_parser():
    parser = argparse.ArgumentParser(
        description="ScrapeCreators CLI — Universal Social Intelligence Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--format", choices=["json", "markdown"], default=None,
                        help="Output format (default: markdown for TTY, json when piped)")
    parser.add_argument("--output", "-o", help="Write output to file")
    parser.add_argument("--quiet", "-q", action="store_true", help="Suppress progress messages")

    subs = parser.add_subparsers(dest="platform_cmd", help="Platform")

    # --- TikTok ---
    tt = subs.add_parser("tiktok", help="TikTok commands")
    tt_subs = tt.add_subparsers(dest="tiktok_cmd")

    p = tt_subs.add_parser("profile", help="Get user profile")
    p.add_argument("username")

    p = tt_subs.add_parser("audience", help="Get audience demographics (26 credits)")
    p.add_argument("username")

    p = tt_subs.add_parser("videos", help="Get profile videos")
    p.add_argument("username")
    p.add_argument("--pages", type=int, default=1, help="Pages to fetch (default: 1)")

    p = tt_subs.add_parser("video", help="Get video details")
    p.add_argument("video_id")

    p = tt_subs.add_parser("transcript", help="Get video transcript")
    p.add_argument("video_id")

    p = tt_subs.add_parser("comments", help="Get video comments")
    p.add_argument("video_id")

    p = tt_subs.add_parser("search", help="Search TikTok")
    p.add_argument("query")
    p.add_argument("--type", choices=["keyword", "top", "hashtag", "users"], default="keyword")

    p = tt_subs.add_parser("trending", help="Get trending content")
    p.add_argument("--hashtags", action="store_true")
    p.add_argument("--sounds", action="store_true")
    p.add_argument("--creators", action="store_true")
    p.add_argument("--feed", action="store_true")

    p = tt_subs.add_parser("shop", help="Search TikTok Shop")
    p.add_argument("query")

    p = tt_subs.add_parser("song", help="Get song details")
    p.add_argument("song_id")
    p.add_argument("--videos", action="store_true", help="Get videos using this song")

    p = tt_subs.add_parser("following", help="Get user's following list")
    p.add_argument("username")

    p = tt_subs.add_parser("followers", help="Get user's followers")
    p.add_argument("username")

    p = tt_subs.add_parser("live", help="Check if user is live")
    p.add_argument("username")

    # --- Instagram ---
    ig = subs.add_parser("instagram", help="Instagram commands")
    ig_subs = ig.add_subparsers(dest="instagram_cmd")

    p = ig_subs.add_parser("profile", help="Get user profile")
    p.add_argument("username")

    p = ig_subs.add_parser("posts", help="Get user posts")
    p.add_argument("username")

    p = ig_subs.add_parser("post", help="Get post/reel details")
    p.add_argument("shortcode")

    p = ig_subs.add_parser("transcript", help="Get reel transcript")
    p.add_argument("shortcode")

    p = ig_subs.add_parser("comments", help="Get post comments")
    p.add_argument("shortcode")

    p = ig_subs.add_parser("reels", help="Get user reels")
    p.add_argument("username")

    p = ig_subs.add_parser("search-reels", help="Search reels by keyword")
    p.add_argument("query")

    p = ig_subs.add_parser("highlights", help="Get user story highlights")
    p.add_argument("username")

    # --- YouTube ---
    yt = subs.add_parser("youtube", help="YouTube commands")
    yt_subs = yt.add_subparsers(dest="youtube_cmd")

    p = yt_subs.add_parser("channel", help="Get channel details")
    p.add_argument("channel_id")

    p = yt_subs.add_parser("videos", help="Get channel videos")
    p.add_argument("channel_id")

    p = yt_subs.add_parser("shorts", help="Get channel shorts")
    p.add_argument("channel_id")

    p = yt_subs.add_parser("video", help="Get video details")
    p.add_argument("video_id")

    p = yt_subs.add_parser("transcript", help="Get video transcript")
    p.add_argument("video_id")

    p = yt_subs.add_parser("search", help="Search YouTube")
    p.add_argument("query")
    p.add_argument("--type", choices=["video", "channel", "shorts"], default="video")

    p = yt_subs.add_parser("comments", help="Get video comments")
    p.add_argument("video_id")

    yt_subs.add_parser("trending-shorts", help="Get trending shorts")

    p = yt_subs.add_parser("playlist", help="Get playlist videos")
    p.add_argument("playlist_id")

    # --- Twitter ---
    tw = subs.add_parser("twitter", help="Twitter/X commands")
    tw_subs = tw.add_subparsers(dest="twitter_cmd")

    p = tw_subs.add_parser("profile", help="Get user profile")
    p.add_argument("username")

    p = tw_subs.add_parser("tweets", help="Get user tweets")
    p.add_argument("username")

    p = tw_subs.add_parser("tweet", help="Get tweet details")
    p.add_argument("tweet_id")

    p = tw_subs.add_parser("transcript", help="Get video transcript")
    p.add_argument("tweet_id")

    # --- Facebook ---
    fb = subs.add_parser("facebook", help="Facebook commands")
    fb_subs = fb.add_subparsers(dest="facebook_cmd")

    p = fb_subs.add_parser("profile", help="Get user profile")
    p.add_argument("username")

    p = fb_subs.add_parser("posts", help="Get profile posts")
    p.add_argument("username")

    p = fb_subs.add_parser("reels", help="Get profile reels")
    p.add_argument("username")

    p = fb_subs.add_parser("ads-search", help="Search Meta Ad Library")
    p.add_argument("query")
    p.add_argument("--country", default=None, help="Country code (e.g., US)")

    p = fb_subs.add_parser("company-ads", help="Get company's ads from Ad Library")
    p.add_argument("company")

    p = fb_subs.add_parser("group", help="Get group posts")
    p.add_argument("group_id")

    # --- LinkedIn ---
    li = subs.add_parser("linkedin", help="LinkedIn commands")
    li_subs = li.add_subparsers(dest="linkedin_cmd")

    p = li_subs.add_parser("profile", help="Get person's profile")
    p.add_argument("url", help="LinkedIn URL or username")

    p = li_subs.add_parser("company", help="Get company page")
    p.add_argument("url", help="LinkedIn URL or company name")

    p = li_subs.add_parser("company-posts", help="Get company posts")
    p.add_argument("url")

    p = li_subs.add_parser("post", help="Get a post")
    p.add_argument("url")

    p = li_subs.add_parser("ads", help="Search LinkedIn Ad Library")
    p.add_argument("query")

    # --- Reddit ---
    rd = subs.add_parser("reddit", help="Reddit commands")
    rd_subs = rd.add_subparsers(dest="reddit_cmd")

    p = rd_subs.add_parser("subreddit", help="Get subreddit posts")
    p.add_argument("name")

    p = rd_subs.add_parser("subreddit-details", help="Get subreddit details")
    p.add_argument("name")

    p = rd_subs.add_parser("search", help="Search Reddit")
    p.add_argument("query")

    p = rd_subs.add_parser("subreddit-search", help="Search within subreddit")
    p.add_argument("name")
    p.add_argument("query")

    p = rd_subs.add_parser("comments", help="Get post comments")
    p.add_argument("post_id")

    # --- Threads ---
    th = subs.add_parser("threads", help="Threads commands")
    th_subs = th.add_subparsers(dest="threads_cmd")

    p = th_subs.add_parser("profile", help="Get user profile")
    p.add_argument("username")

    p = th_subs.add_parser("posts", help="Get user posts")
    p.add_argument("username")

    p = th_subs.add_parser("search", help="Search users")
    p.add_argument("query")

    # --- Bluesky ---
    bs = subs.add_parser("bluesky", help="Bluesky commands")
    bs_subs = bs.add_subparsers(dest="bluesky_cmd")

    p = bs_subs.add_parser("profile", help="Get user profile")
    p.add_argument("handle")

    p = bs_subs.add_parser("posts", help="Get user posts")
    p.add_argument("handle")

    # --- Pinterest ---
    pi = subs.add_parser("pinterest", help="Pinterest commands")
    pi_subs = pi.add_subparsers(dest="pinterest_cmd")

    p = pi_subs.add_parser("search", help="Search Pinterest")
    p.add_argument("query")

    p = pi_subs.add_parser("boards", help="Get user boards")
    p.add_argument("username")

    # --- Google ---
    go = subs.add_parser("google", help="Google commands")
    go_subs = go.add_subparsers(dest="google_cmd")

    p = go_subs.add_parser("search", help="Google search")
    p.add_argument("query")

    p = go_subs.add_parser("company-ads", help="Get company ads from Google Ad Library")
    p.add_argument("company")

    p = go_subs.add_parser("advertisers", help="Search Google Ad Library advertisers")
    p.add_argument("query")

    # --- Credits ---
    subs.add_parser("credits", help="Check credit balance")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if not args.platform_cmd:
        parser.print_help()
        sys.exit(1)

    # Auto-detect format
    if args.format is None:
        args.format = detect_format(args)

    try:
        client = ScrapeCreatorsClient(quiet=args.quiet)
    except ScrapeCreatorsError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    # Route to handler
    handlers = {
        "tiktok": cmd_tiktok,
        "instagram": cmd_instagram,
        "youtube": cmd_youtube,
        "twitter": cmd_twitter,
        "facebook": cmd_facebook,
        "linkedin": cmd_linkedin,
        "reddit": cmd_reddit,
        "threads": cmd_threads,
        "bluesky": cmd_bluesky,
        "pinterest": cmd_pinterest,
        "google": cmd_google,
        "credits": cmd_credits,
    }

    handler = handlers.get(args.platform_cmd)
    if handler:
        try:
            handler(args, client)
            # Show credit usage
            s = client.summary()
            if s["calls_made"] > 0 and not args.quiet:
                print(f"\n---\nCredits used: {s['credits_used']} | API calls: {s['calls_made']}",
                      file=sys.stderr)
        except ScrapeCreatorsError as e:
            print(f"ERROR: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
