"""Reddit CLI — public .json endpoints, no API key.

Sub-commands
------------
    scrape      Deep post + comment tree with 'more' stub resolution
    search      Reddit-wide or per-subreddit search
    user        User profile + comment/post history
    subreddit   Subreddit about + top posts
    trending    Popular subreddits list
    submission  Single post metadata by id or URL

Examples
--------
    # Scrape (existing behavior — same flags as v1)
    python3 scripts/reddit.py scrape --url https://www.reddit.com/r/singaporefi/comments/1abcdef/title/
    python3 scripts/reddit.py scrape --subreddit singaporefi --post-id 1abcdef,1xyz \\
        --output-dir clients/neezanizam/research/raw \\
        --keywords "halal,riba,bto" --resolve-stubs

    # Search
    python3 scripts/reddit.py search "halal mortgage" --limit 25
    python3 scripts/reddit.py search "bto upgrade" --subreddit singaporefi \\
        --sort top --time year --limit 50 --output-dir clients/fuggysmedia/research/raw

    # User
    python3 scripts/reddit.py user spez
    python3 scripts/reddit.py user spez --comments --posts --sort top --time year --limit 25

    # Subreddit
    python3 scripts/reddit.py subreddit singaporefi                   # about only
    python3 scripts/reddit.py subreddit singaporefi --top --time week --limit 25

    # Trending
    python3 scripts/reddit.py trending --limit 25

    # Single submission (no comment tree)
    python3 scripts/reddit.py submission 1abcdef
    python3 scripts/reddit.py submission https://www.reddit.com/r/sub/comments/1abcdef/title/

Rate limit
----------
Reddit anonymous ~60 req/min. Script sleeps 1.1s between requests and retries
429/503 with exponential backoff. User-Agent is required (Reddit blocks missing UA).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlparse
from urllib.request import Request, urlopen

USER_AGENT = "gumclaw-research/2.0 (by /u/neezanizam-research)"
RATE_LIMIT_SLEEP = 1.1
MAX_RETRIES = 4
RETRY_BACKOFF_BASE = 2.0
BASE = "https://www.reddit.com"


# ---------------------------------------------------------------------------
# HTTP
# ---------------------------------------------------------------------------

def _request(url: str) -> Any:
    for attempt in range(MAX_RETRIES):
        try:
            req = Request(url, headers={"User-Agent": USER_AGENT})
            with urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except HTTPError as exc:
            if exc.code in (429, 503) and attempt < MAX_RETRIES - 1:
                wait = RETRY_BACKOFF_BASE * (2**attempt)
                print(
                    f"  [rate-limit] {exc.code} — sleeping {wait:.1f}s (retry {attempt + 1}/{MAX_RETRIES})",
                    file=sys.stderr,
                )
                time.sleep(wait)
                continue
            raise
        except URLError as exc:
            if attempt < MAX_RETRIES - 1:
                wait = RETRY_BACKOFF_BASE * (2**attempt)
                print(
                    f"  [network] {exc} — sleeping {wait:.1f}s (retry {attempt + 1}/{MAX_RETRIES})",
                    file=sys.stderr,
                )
                time.sleep(wait)
                continue
            raise
    raise RuntimeError(f"Failed after {MAX_RETRIES} retries: {url}")


def _get(url: str) -> Any:
    time.sleep(RATE_LIMIT_SLEEP)
    return _request(url)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def parse_post_url(url: str) -> tuple[str, str]:
    path = urlparse(url).path
    m = re.search(r"/r/([^/]+)/comments/([^/]+)", path)
    if not m:
        raise ValueError(f"Could not parse subreddit/post_id from URL: {url}")
    return m.group(1), m.group(2)


def ts_to_iso(ts: float) -> str:
    return datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def write_outputs(output_dir: Path | None, stem: str, raw: Any, markdown: str) -> None:
    if output_dir is None:
        print(markdown)
        return
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / f"{stem}-raw.json").write_text(
        json.dumps(raw, indent=2, ensure_ascii=False)
    )
    (output_dir / f"{stem}-flat.md").write_text(markdown)
    print(f"  [done] → {output_dir}/{stem}-flat.md", file=sys.stderr)


def listing_children(data: Any) -> list[dict]:
    """Extract children from a Reddit listing response."""
    if isinstance(data, dict) and data.get("kind") == "Listing":
        return data.get("data", {}).get("children", [])
    return []


# ---------------------------------------------------------------------------
# Sub-command: scrape  (v1 behavior, preserved)
# ---------------------------------------------------------------------------

def fetch_post(subreddit: str, post_id: str) -> tuple[dict, list[dict]]:
    url = f"{BASE}/r/{subreddit}/comments/{post_id}.json?limit=500&depth=100&sort=top"
    data = _get(url)
    if not isinstance(data, list) or len(data) != 2:
        raise RuntimeError(f"Unexpected response shape for {post_id}")
    post = data[0]["data"]["children"][0]["data"]
    comments = list(data[1]["data"]["children"])
    return post, comments


def fetch_more_subtree(subreddit: str, post_id: str, comment_id: str) -> list[dict]:
    url = (
        f"{BASE}/r/{subreddit}/comments/{post_id}/_/{comment_id}.json"
        "?limit=500&depth=100"
    )
    try:
        data = _get(url)
    except HTTPError as exc:
        print(f"  [stub-skip] {comment_id}: {exc}", file=sys.stderr)
        return []
    if not isinstance(data, list) or len(data) != 2:
        return []
    return list(data[1]["data"]["children"])


def resolve_stubs(
    subreddit: str, post_id: str, comments: list[dict], max_stubs: int = 200
) -> list[dict]:
    stub_count = [0]

    def walk(items: list[dict]) -> list[dict]:
        resolved = []
        for item in items:
            if item.get("kind") == "more":
                for cid in item.get("data", {}).get("children", []):
                    if stub_count[0] >= max_stubs:
                        print(
                            f"  [stub-cap] hit max_stubs={max_stubs}, stopping",
                            file=sys.stderr,
                        )
                        return resolved
                    stub_count[0] += 1
                    resolved.extend(walk(fetch_more_subtree(subreddit, post_id, cid)))
                continue
            replies = item.get("data", {}).get("replies")
            if isinstance(replies, dict):
                children = replies.get("data", {}).get("children", [])
                item["data"]["replies"] = {"data": {"children": walk(children)}}
            resolved.append(item)
        return resolved

    out = walk(comments)
    print(f"  [stubs-resolved] {stub_count[0]}", file=sys.stderr)
    return out


def flatten_comments(comments: list[dict], depth: int = 0):
    for item in comments:
        if item.get("kind") == "more":
            continue
        data = item.get("data", {})
        yield depth, data
        replies = data.get("replies")
        if isinstance(replies, dict):
            yield from flatten_comments(
                replies.get("data", {}).get("children", []), depth + 1
            )


def keyword_match(body: str, keywords: list[str]) -> bool:
    if not keywords:
        return True
    low = body.lower()
    return any(kw.lower() in low for kw in keywords)


def render_post_markdown(
    post: dict, comments: list[dict], keywords: list[str] | None = None
) -> str:
    keywords = keywords or []
    lines = [
        f"# {post.get('title', '(untitled)')}",
        "",
        f"- **Subreddit:** r/{post.get('subreddit')}",
        f"- **Author:** u/{post.get('author')}",
        f"- **Posted:** {ts_to_iso(post.get('created_utc', 0))}",
        f"- **Score:** {post.get('score', 0)} · **Comments:** {post.get('num_comments', 0)}",
        f"- **URL:** {BASE}{post.get('permalink', '')}",
        "",
        "## Post Body",
        "",
        post.get("selftext", "") or "_(link post, no body)_",
        "",
        "## Comments",
        "",
    ]
    kept = total = 0
    for depth, c in flatten_comments(comments):
        total += 1
        body = c.get("body", "")
        if not body or body in ("[deleted]", "[removed]"):
            continue
        if not keyword_match(body, keywords):
            continue
        kept += 1
        indent = "  " * depth
        lines.append(
            f"{indent}- **u/{c.get('author', '?')}** · score {c.get('score', 0)} · {ts_to_iso(c.get('created_utc', 0))}"
        )
        for line in body.splitlines():
            lines.append(f"{indent}  > {line}")
        lines.append("")
    lines.append(f"\n---\n_Comments in output: {kept} / {total} total_")
    if keywords:
        lines.append(f"_Keyword filter: {', '.join(keywords)}_")
    return "\n".join(lines)


def cmd_scrape(args) -> int:
    if args.url:
        subreddit, pid = parse_post_url(args.url)
        post_ids = [pid]
    else:
        if not args.subreddit:
            print("error: --post-id requires --subreddit", file=sys.stderr)
            return 2
        subreddit = args.subreddit
        post_ids = [p.strip() for p in args.post_id.split(",") if p.strip()]

    keywords = [k.strip() for k in (args.keywords or "").split(",") if k.strip()]
    output_dir = Path(args.output_dir) if args.output_dir else None
    total = 0
    for pid in post_ids:
        try:
            print(f"[scrape] r/{subreddit}/{pid}", file=sys.stderr)
            post, comments = fetch_post(subreddit, pid)
            if args.resolve_stubs:
                comments = resolve_stubs(
                    subreddit, pid, comments, max_stubs=args.max_stubs
                )
            md = render_post_markdown(post, comments, keywords)
            write_outputs(output_dir, pid, {"post": post, "comments": comments}, md)
            total += sum(1 for _ in flatten_comments(comments))
        except Exception as exc:
            print(f"[error] {subreddit}/{pid}: {exc}", file=sys.stderr)
    print(f"\n[summary] {len(post_ids)} post(s), {total} comments", file=sys.stderr)
    return 0


# ---------------------------------------------------------------------------
# Sub-command: search
# ---------------------------------------------------------------------------

def render_search_markdown(query: str, subreddit: str | None, children: list[dict]) -> str:
    scope = f"r/{subreddit}" if subreddit else "all of Reddit"
    lines = [
        f"# Reddit search: {query}",
        "",
        f"- **Scope:** {scope}",
        f"- **Results:** {len(children)}",
        f"- **Fetched:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
        "",
    ]
    for ch in children:
        d = ch.get("data", {})
        lines.extend([
            f"## {d.get('title', '(untitled)')}",
            "",
            f"- **r/{d.get('subreddit')}** · u/{d.get('author')} · score {d.get('score', 0)} · comments {d.get('num_comments', 0)}",
            f"- **Posted:** {ts_to_iso(d.get('created_utc', 0))}",
            f"- **URL:** {BASE}{d.get('permalink', '')}",
            "",
        ])
        body = d.get("selftext", "").strip()
        if body:
            for line in body.splitlines()[:20]:
                lines.append(f"  > {line}")
            if len(body.splitlines()) > 20:
                lines.append("  > _(truncated)_")
            lines.append("")
    return "\n".join(lines)


def cmd_search(args) -> int:
    q = quote(args.query)
    params = [
        f"q={q}",
        f"sort={args.sort}",
        f"t={args.time}",
        f"limit={args.limit}",
        "raw_json=1",
    ]
    if args.subreddit:
        params.append("restrict_sr=1")
        url = f"{BASE}/r/{args.subreddit}/search.json?{'&'.join(params)}"
        stem = f"search-{args.subreddit}-{re.sub(r'[^a-z0-9]+', '-', args.query.lower())[:40]}"
    else:
        url = f"{BASE}/search.json?{'&'.join(params)}"
        stem = f"search-all-{re.sub(r'[^a-z0-9]+', '-', args.query.lower())[:40]}"

    print(f"[search] {args.query!r} in {args.subreddit or 'all'} (sort={args.sort} time={args.time})", file=sys.stderr)
    data = _get(url)
    children = listing_children(data)
    md = render_search_markdown(args.query, args.subreddit, children)
    output_dir = Path(args.output_dir) if args.output_dir else None
    write_outputs(output_dir, stem, data, md)
    print(f"  [results] {len(children)}", file=sys.stderr)
    return 0


# ---------------------------------------------------------------------------
# Sub-command: user
# ---------------------------------------------------------------------------

def render_user_markdown(username: str, about: dict, comments: list[dict], posts: list[dict]) -> str:
    ad = about.get("data", {}) if isinstance(about, dict) else {}
    lines = [
        f"# u/{username}",
        "",
        f"- **Created:** {ts_to_iso(ad.get('created_utc', 0))}",
        f"- **Comment karma:** {ad.get('comment_karma', 0)}",
        f"- **Link karma:** {ad.get('link_karma', 0)}",
        f"- **Verified email:** {ad.get('has_verified_email', False)}",
        f"- **URL:** {BASE}/user/{username}",
        "",
    ]
    if comments:
        lines.append(f"## Recent Comments ({len(comments)})")
        lines.append("")
        for ch in comments:
            d = ch.get("data", {})
            lines.append(
                f"- **r/{d.get('subreddit')}** · score {d.get('score', 0)} · {ts_to_iso(d.get('created_utc', 0))}"
            )
            body = d.get("body", "").strip()
            for line in body.splitlines()[:10]:
                lines.append(f"  > {line}")
            if len(body.splitlines()) > 10:
                lines.append("  > _(truncated)_")
            lines.append(f"  [link]({BASE}{d.get('permalink', '')})")
            lines.append("")
    if posts:
        lines.append(f"## Recent Posts ({len(posts)})")
        lines.append("")
        for ch in posts:
            d = ch.get("data", {})
            lines.extend([
                f"### {d.get('title', '(untitled)')}",
                "",
                f"- **r/{d.get('subreddit')}** · score {d.get('score', 0)} · comments {d.get('num_comments', 0)} · {ts_to_iso(d.get('created_utc', 0))}",
                f"- **URL:** {BASE}{d.get('permalink', '')}",
                "",
            ])
    return "\n".join(lines)


def cmd_user(args) -> int:
    username = args.username
    print(f"[user] u/{username}", file=sys.stderr)
    about = _get(f"{BASE}/user/{username}/about.json?raw_json=1")
    comments: list[dict] = []
    posts: list[dict] = []
    raw: dict[str, Any] = {"about": about}

    want_comments = args.comments or not (args.comments or args.posts)
    want_posts = args.posts

    if want_comments:
        url = f"{BASE}/user/{username}/comments.json?sort={args.sort}&t={args.time}&limit={args.limit}&raw_json=1"
        c_data = _get(url)
        comments = listing_children(c_data)
        raw["comments"] = c_data
    if want_posts:
        url = f"{BASE}/user/{username}/submitted.json?sort={args.sort}&t={args.time}&limit={args.limit}&raw_json=1"
        p_data = _get(url)
        posts = listing_children(p_data)
        raw["posts"] = p_data

    md = render_user_markdown(username, about, comments, posts)
    output_dir = Path(args.output_dir) if args.output_dir else None
    write_outputs(output_dir, f"user-{username}", raw, md)
    print(f"  [fetched] comments={len(comments)} posts={len(posts)}", file=sys.stderr)
    return 0


# ---------------------------------------------------------------------------
# Sub-command: subreddit
# ---------------------------------------------------------------------------

def render_subreddit_markdown(name: str, about: dict, top: list[dict]) -> str:
    ad = about.get("data", {}) if isinstance(about, dict) else {}
    lines = [
        f"# r/{name}",
        "",
        f"- **Title:** {ad.get('title', '')}",
        f"- **Subscribers:** {ad.get('subscribers', 0):,}",
        f"- **Active users:** {ad.get('active_user_count', 0):,}",
        f"- **Created:** {ts_to_iso(ad.get('created_utc', 0))}",
        f"- **Over 18:** {ad.get('over18', False)}",
        f"- **URL:** {BASE}/r/{name}",
        "",
        "## Description",
        "",
        ad.get("public_description", "").strip() or "_(none)_",
        "",
    ]
    if top:
        lines.append(f"## Top Posts ({len(top)})")
        lines.append("")
        for ch in top:
            d = ch.get("data", {})
            lines.extend([
                f"### {d.get('title', '(untitled)')}",
                "",
                f"- u/{d.get('author')} · score {d.get('score', 0)} · comments {d.get('num_comments', 0)} · {ts_to_iso(d.get('created_utc', 0))}",
                f"- {BASE}{d.get('permalink', '')}",
                "",
            ])
    return "\n".join(lines)


def cmd_subreddit(args) -> int:
    name = args.name
    print(f"[subreddit] r/{name}", file=sys.stderr)
    about = _get(f"{BASE}/r/{name}/about.json?raw_json=1")
    top: list[dict] = []
    raw: dict[str, Any] = {"about": about}
    if args.top:
        url = f"{BASE}/r/{name}/top.json?t={args.time}&limit={args.limit}&raw_json=1"
        t_data = _get(url)
        top = listing_children(t_data)
        raw["top"] = t_data
    md = render_subreddit_markdown(name, about, top)
    output_dir = Path(args.output_dir) if args.output_dir else None
    write_outputs(output_dir, f"subreddit-{name}", raw, md)
    print(f"  [fetched] top_posts={len(top)}", file=sys.stderr)
    return 0


# ---------------------------------------------------------------------------
# Sub-command: trending
# ---------------------------------------------------------------------------

def render_trending_markdown(children: list[dict]) -> str:
    lines = [
        f"# Trending subreddits ({len(children)})",
        "",
        f"- **Fetched:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
        "",
    ]
    for ch in children:
        d = ch.get("data", {})
        lines.append(
            f"- **r/{d.get('display_name')}** · {d.get('subscribers', 0):,} subs · {d.get('public_description', '').strip()[:100]}"
        )
    return "\n".join(lines)


def cmd_trending(args) -> int:
    print("[trending] popular subreddits", file=sys.stderr)
    url = f"{BASE}/subreddits/popular.json?limit={args.limit}&raw_json=1"
    data = _get(url)
    children = listing_children(data)
    md = render_trending_markdown(children)
    output_dir = Path(args.output_dir) if args.output_dir else None
    write_outputs(output_dir, "trending-subreddits", data, md)
    print(f"  [fetched] {len(children)} subreddits", file=sys.stderr)
    return 0


# ---------------------------------------------------------------------------
# Sub-command: submission (single post metadata, no comment tree)
# ---------------------------------------------------------------------------

def cmd_submission(args) -> int:
    ref = args.post_ref
    if ref.startswith("http"):
        subreddit, pid = parse_post_url(ref)
    else:
        subreddit = "unknown"
        pid = ref
    print(f"[submission] {pid}", file=sys.stderr)
    url = f"{BASE}/comments/{pid}.json?limit=1&depth=0&raw_json=1"
    data = _get(url)
    if not isinstance(data, list) or not data:
        print(f"error: bad response for {pid}", file=sys.stderr)
        return 1
    post = data[0]["data"]["children"][0]["data"]
    md = render_post_markdown(post, [], [])
    output_dir = Path(args.output_dir) if args.output_dir else None
    write_outputs(output_dir, f"submission-{pid}", {"post": post}, md)
    return 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _add_output_dir(p: argparse.ArgumentParser) -> None:
    p.add_argument(
        "--output-dir",
        default=None,
        help="Write outputs here; if omitted, markdown prints to stdout",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="reddit",
        description=__doc__.splitlines()[0],
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    # scrape
    s = sub.add_parser("scrape", help="Deep post + comment tree extraction")
    g = s.add_mutually_exclusive_group(required=True)
    g.add_argument("--url", help="Full Reddit post URL")
    g.add_argument("--post-id", help="Post id (requires --subreddit; comma-separated for batch)")
    s.add_argument("--subreddit", help="Subreddit without r/ prefix (required with --post-id)")
    s.add_argument("--keywords", default="", help="Comma-separated keywords to filter markdown (case-insensitive)")
    s.add_argument("--resolve-stubs", action="store_true", help="Recursively resolve 'more' stubs (97-100%% coverage)")
    s.add_argument("--max-stubs", type=int, default=200, help="Max 'more' stubs to resolve (default 200)")
    _add_output_dir(s)
    s.set_defaults(func=cmd_scrape)

    # search
    s = sub.add_parser("search", help="Search Reddit or a subreddit")
    s.add_argument("query", help="Search query")
    s.add_argument("--subreddit", help="Restrict to one subreddit (optional)")
    s.add_argument("--sort", default="relevance", choices=["relevance", "hot", "top", "new", "comments"])
    s.add_argument("--time", default="all", choices=["hour", "day", "week", "month", "year", "all"])
    s.add_argument("--limit", type=int, default=25, help="1-100 (default 25)")
    _add_output_dir(s)
    s.set_defaults(func=cmd_search)

    # user
    s = sub.add_parser("user", help="User profile + activity")
    s.add_argument("username", help="Reddit username without u/")
    s.add_argument("--comments", action="store_true", help="Include recent comments")
    s.add_argument("--posts", action="store_true", help="Include recent posts")
    s.add_argument("--sort", default="new", choices=["new", "top", "hot", "controversial"])
    s.add_argument("--time", default="all", choices=["hour", "day", "week", "month", "year", "all"])
    s.add_argument("--limit", type=int, default=25)
    _add_output_dir(s)
    s.set_defaults(func=cmd_user)

    # subreddit
    s = sub.add_parser("subreddit", help="Subreddit about + top posts")
    s.add_argument("name", help="Subreddit name without r/")
    s.add_argument("--top", action="store_true", help="Also fetch top posts")
    s.add_argument("--time", default="week", choices=["hour", "day", "week", "month", "year", "all"])
    s.add_argument("--limit", type=int, default=25)
    _add_output_dir(s)
    s.set_defaults(func=cmd_subreddit)

    # trending
    s = sub.add_parser("trending", help="Popular subreddits")
    s.add_argument("--limit", type=int, default=25)
    _add_output_dir(s)
    s.set_defaults(func=cmd_trending)

    # submission
    s = sub.add_parser("submission", help="Single post metadata (no comment tree)")
    s.add_argument("post_ref", help="Post id OR full post URL")
    _add_output_dir(s)
    s.set_defaults(func=cmd_submission)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
