#!/usr/bin/env python3
"""
ScrapeCreators API Client
=========================
Universal Python client for the ScrapeCreators social intelligence API.
Covers 25+ platforms: TikTok, Instagram, YouTube, LinkedIn, Facebook,
Twitter/X, Reddit, Threads, Pinterest, Bluesky, and more.

Usage as module:
    from api import ScrapeCreatorsClient
    client = ScrapeCreatorsClient()
    profile = client.tiktok_profile("charlidamelio")

Usage as CLI:
    See scrape.py for the command-line interface.

API docs: https://docs.scrapecreators.com
Dashboard: https://app.scrapecreators.com
Cost: 1 credit/request (except audience demographics = 26 credits)
"""

import json
import os
import sys
import time
from pathlib import Path

try:
    import requests
except ImportError:
    print("ERROR: 'requests' package required. Install with: pip install requests")
    sys.exit(1)


API_BASE = "https://api.scrapecreators.com"


# --- Exceptions ---

class ScrapeCreatorsError(Exception):
    """Base exception for ScrapeCreators API errors."""
    pass

class AuthError(ScrapeCreatorsError):
    """Invalid or missing API key (401/403)."""
    pass

class NotFoundError(ScrapeCreatorsError):
    """Resource not found (404)."""
    pass

class RateLimitError(ScrapeCreatorsError):
    """Rate limit exceeded (429)."""
    pass

class ServerError(ScrapeCreatorsError):
    """Server-side error (5xx)."""
    pass


# --- Utility functions (shared with other scripts) ---

def find_project_root():
    """Walk up from script location looking for CLAUDE.md (repo convention)."""
    current = Path(__file__).resolve().parent
    for _ in range(10):
        if (current / "CLAUDE.md").exists():
            return current
        current = current.parent
    # Fallback: try CWD
    cwd = Path.cwd()
    for _ in range(10):
        if (cwd / "CLAUDE.md").exists():
            return cwd
        cwd = cwd.parent
    return None


def load_env(root=None):
    """Load .env file from project root."""
    if root is None:
        root = find_project_root()
    if root is None:
        return
    env_path = root / ".env"
    if not env_path.exists():
        return
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, _, value = line.partition("=")
                key = key.strip()
                value = value.strip().strip("'\"")
                os.environ.setdefault(key, value)


# --- Client ---

class ScrapeCreatorsClient:
    """Universal client for the ScrapeCreators API.

    Args:
        api_key: API key. If None, loads from SCRAPECREATORS_API_KEY env var.
        quiet: Suppress progress messages.
    """

    def __init__(self, api_key=None, quiet=False):
        if api_key is None:
            load_env()
            api_key = os.environ.get("SCRAPECREATORS_API_KEY")
        if not api_key:
            raise AuthError(
                "SCRAPECREATORS_API_KEY not set. "
                "Get your key at: https://app.scrapecreators.com"
            )
        self._api_key = api_key
        self._quiet = quiet
        self.credits_used = 0
        self.calls_made = 0

    def _log(self, msg):
        if not self._quiet:
            print(msg, file=sys.stderr)

    def request(self, endpoint, params=None, credits=1, retries=1):
        """Make an API request with retry on 5xx.

        Args:
            endpoint: API path (e.g., "/v1/tiktok/profile")
            params: Query parameters dict
            credits: Expected credit cost (for tracking)
            retries: Number of retries on server errors

        Returns:
            Parsed JSON response dict

        Raises:
            AuthError: On 401/403
            NotFoundError: On 404
            RateLimitError: On 429
            ServerError: On 5xx after retries exhausted
            ScrapeCreatorsError: On other errors
        """
        url = f"{API_BASE}{endpoint}"
        headers = {"x-api-key": self._api_key}
        last_error = None

        for attempt in range(1 + retries):
            try:
                resp = requests.get(
                    url, headers=headers, params=params or {}, timeout=30
                )

                if resp.status_code == 401 or resp.status_code == 403:
                    raise AuthError(f"Authentication failed ({resp.status_code})")
                if resp.status_code == 404:
                    raise NotFoundError(f"Not found: {endpoint}")
                if resp.status_code == 429:
                    raise RateLimitError("Rate limit exceeded")
                if resp.status_code >= 500:
                    last_error = ServerError(
                        f"Server error {resp.status_code}: {endpoint}"
                    )
                    if attempt < retries:
                        time.sleep(2 ** attempt)
                        continue
                    raise last_error

                resp.raise_for_status()
                self.credits_used += credits
                self.calls_made += 1
                return resp.json()

            except requests.exceptions.ConnectionError as e:
                last_error = ScrapeCreatorsError(f"Connection failed: {e}")
                if attempt < retries:
                    time.sleep(2 ** attempt)
                    continue
                raise last_error
            except requests.exceptions.Timeout:
                last_error = ScrapeCreatorsError(f"Request timed out: {endpoint}")
                if attempt < retries:
                    time.sleep(2 ** attempt)
                    continue
                raise last_error
            except (AuthError, NotFoundError, RateLimitError):
                raise
            except requests.exceptions.HTTPError as e:
                raise ScrapeCreatorsError(f"HTTP error: {e}")

        raise last_error

    def _extract(self, data, *keys):
        """Extract nested data, trying multiple key paths."""
        if data is None:
            return data
        for key in keys:
            if isinstance(data, dict) and key in data:
                return data[key]
        return data

    def _paginate(self, endpoint, params, data_key="videos", max_pages=5, credits_per_page=1):
        """Auto-paginate cursor-based endpoints.

        Yields items from each page. Stops at max_pages or when no more cursor.
        """
        params = dict(params) if params else {}
        for page in range(max_pages):
            data = self.request(endpoint, params, credits=credits_per_page)
            if data is None:
                break

            items = self._extract(data, data_key, "data")
            if isinstance(items, dict):
                items = items.get(data_key, items.get("data", []))
            if isinstance(items, list):
                yield from items
            elif items is not None:
                yield items

            # Check for cursor/pagination
            cursor = None
            if isinstance(data, dict):
                cursor = data.get("cursor", data.get("nextCursor", data.get("next_cursor")))
            if not cursor:
                break
            params["cursor"] = cursor

    # ==========================================
    # TikTok (20 endpoints)
    # ==========================================

    def tiktok_profile(self, username):
        """Get TikTok user profile info."""
        username = username.lstrip("@")
        return self.request("/v1/tiktok/profile", {"username": username})

    def tiktok_audience(self, username):
        """Get TikTok user audience demographics. Costs 26 credits."""
        username = username.lstrip("@")
        return self.request("/v1/tiktok/user/audience", {"username": username}, credits=26)

    def tiktok_videos(self, username, cursor=None):
        """Get videos from a TikTok profile (single page)."""
        username = username.lstrip("@")
        params = {"username": username}
        if cursor:
            params["cursor"] = cursor
        data = self.request("/v3/tiktok/profile/videos", params)
        videos = self._extract(data, "videos", "data")
        if isinstance(videos, dict):
            videos = videos.get("videos", [])
        return videos if isinstance(videos, list) else []

    def tiktok_videos_all(self, username, max_pages=5):
        """Get all videos from a TikTok profile (auto-paginate)."""
        username = username.lstrip("@")
        return list(self._paginate(
            "/v3/tiktok/profile/videos",
            {"username": username},
            data_key="videos",
            max_pages=max_pages
        ))

    def tiktok_video(self, video_id):
        """Get detailed info for a single TikTok video."""
        return self.request("/v2/tiktok/video", {"video_id": str(video_id)})

    def tiktok_transcript(self, video_id):
        """Get transcript for a TikTok video."""
        return self.request("/v1/tiktok/video/transcript", {"video_id": str(video_id)})

    def tiktok_comments(self, video_id):
        """Get comments on a TikTok video."""
        return self.request("/v1/tiktok/video/comments", {"video_id": str(video_id)})

    def tiktok_live(self, username):
        """Check if a TikTok user is live."""
        username = username.lstrip("@")
        return self.request("/v1/tiktok/user/live", {"username": username})

    def tiktok_following(self, username):
        """Get accounts a TikTok user follows."""
        username = username.lstrip("@")
        return self.request("/v1/tiktok/user/following", {"username": username})

    def tiktok_followers(self, username):
        """Get a TikTok user's followers."""
        username = username.lstrip("@")
        return self.request("/v1/tiktok/user/followers", {"username": username})

    def tiktok_search_users(self, keyword):
        """Search TikTok users by keyword."""
        return self.request("/v1/tiktok/search/users", {"keyword": keyword})

    def tiktok_search_hashtag(self, hashtag):
        """Search TikTok videos by hashtag."""
        hashtag = hashtag.lstrip("#")
        return self.request("/v1/tiktok/search/hashtag", {"hashtag": hashtag})

    def tiktok_search_keyword(self, keyword):
        """Search TikTok videos by keyword."""
        return self.request("/v1/tiktok/search/keyword", {"keyword": keyword})

    def tiktok_search_top(self, keyword):
        """Top search results on TikTok (includes carousels)."""
        return self.request("/v1/tiktok/search/top", {"keyword": keyword})

    def tiktok_popular_songs(self):
        """Get currently popular TikTok songs."""
        return self.request("/v1/tiktok/songs/popular")

    def tiktok_popular_creators(self):
        """Get currently popular TikTok creators."""
        return self.request("/v1/tiktok/creators/popular")

    def tiktok_popular_videos(self):
        """Get currently popular TikTok videos."""
        return self.request("/v1/tiktok/videos/popular")

    def tiktok_popular_hashtags(self):
        """Get currently popular TikTok hashtags."""
        return self.request("/v1/tiktok/hashtags/popular")

    def tiktok_song(self, song_id):
        """Get details for a specific TikTok song."""
        return self.request("/v1/tiktok/song", {"song_id": str(song_id)})

    def tiktok_song_videos(self, song_id):
        """Get TikTok videos using a specific song."""
        return self.request("/v1/tiktok/song/videos", {"song_id": str(song_id)})

    def tiktok_trending_feed(self):
        """Get the TikTok trending feed."""
        return self.request("/v1/tiktok/get-trending-feed")

    # ==========================================
    # TikTok Shop (4 endpoints)
    # ==========================================

    def tiktok_shop_search(self, keyword):
        """Search TikTok Shop."""
        return self.request("/v1/tiktok/shop/search", {"keyword": keyword})

    def tiktok_shop_products(self, username):
        """Get products from a TikTok Shop."""
        username = username.lstrip("@")
        return self.request("/v1/tiktok/shop/products", {"username": username})

    def tiktok_product(self, product_id):
        """Get TikTok product details."""
        return self.request("/v1/tiktok/product", {"product_id": str(product_id)})

    def tiktok_product_reviews(self, product_id):
        """Get reviews for a TikTok Shop product."""
        return self.request("/v1/tiktok/shop/product/reviews", {"product_id": str(product_id)})

    # ==========================================
    # Instagram (12 endpoints)
    # ==========================================

    def instagram_profile(self, username):
        """Get Instagram user profile."""
        username = username.lstrip("@")
        return self.request("/v1/instagram/profile", {"username": username})

    def instagram_basic_profile(self, username):
        """Get basic Instagram profile info."""
        username = username.lstrip("@")
        return self.request("/v1/instagram/basic-profile", {"username": username})

    def instagram_posts(self, username):
        """Get posts from an Instagram user."""
        username = username.lstrip("@")
        return self.request("/v2/instagram/user/posts", {"username": username})

    def instagram_post(self, shortcode):
        """Get details for a specific Instagram post or reel."""
        return self.request("/v1/instagram/post", {"shortcode": shortcode})

    def instagram_transcript(self, shortcode):
        """Get transcript for an Instagram reel."""
        return self.request("/v2/instagram/media/transcript", {"shortcode": shortcode})

    def instagram_search_reels(self, keyword):
        """Search Instagram reels by keyword."""
        return self.request("/v2/instagram/reels/search", {"keyword": keyword})

    def instagram_comments(self, shortcode):
        """Get comments on an Instagram post."""
        return self.request("/v2/instagram/post/comments", {"shortcode": shortcode})

    def instagram_reels(self, username):
        """Get reels from an Instagram user."""
        username = username.lstrip("@")
        return self.request("/v1/instagram/user/reels", {"username": username})

    def instagram_highlights(self, username):
        """Get story highlights from an Instagram user."""
        username = username.lstrip("@")
        return self.request("/v1/instagram/user/highlights", {"username": username})

    def instagram_highlight_detail(self, highlight_id):
        """Get details for a specific Instagram story highlight."""
        return self.request("/v1/instagram/user/highlight/detail", {"highlight_id": str(highlight_id)})

    def instagram_embed(self, username):
        """Get embed HTML for an Instagram user."""
        username = username.lstrip("@")
        return self.request("/v1/instagram/user/embed", {"username": username})

    # ==========================================
    # YouTube (11 endpoints)
    # ==========================================

    def youtube_channel(self, channel_id):
        """Get YouTube channel details."""
        return self.request("/v1/youtube/channel", {"channel_id": channel_id})

    def youtube_channel_videos(self, channel_id):
        """Get videos from a YouTube channel."""
        return self.request("/v1/youtube/channel-videos", {"channel_id": channel_id})

    def youtube_channel_shorts(self, channel_id):
        """Get shorts from a YouTube channel."""
        return self.request("/v1/youtube/channel/shorts", {"channel_id": channel_id})

    def youtube_video(self, video_id):
        """Get details for a YouTube video or short."""
        return self.request("/v1/youtube/video", {"video_id": video_id})

    def youtube_transcript(self, video_id):
        """Get transcript for a YouTube video."""
        return self.request("/v1/youtube/video/transcript", {"video_id": video_id})

    def youtube_search(self, query, search_type="video"):
        """Search YouTube. Types: video, channel, shorts."""
        return self.request("/v1/youtube/search", {"query": query, "type": search_type})

    def youtube_search_hashtag(self, hashtag):
        """Search YouTube by hashtag."""
        hashtag = hashtag.lstrip("#")
        return self.request("/v1/youtube/search/hashtag", {"hashtag": hashtag})

    def youtube_comments(self, video_id):
        """Get comments on a YouTube video."""
        return self.request("/v1/youtube/video/comments", {"video_id": video_id})

    def youtube_trending_shorts(self):
        """Get trending YouTube shorts."""
        return self.request("/v1/youtube/shorts/trending")

    def youtube_playlist(self, playlist_id):
        """Get videos from a YouTube playlist."""
        return self.request("/v1/youtube/playlist", {"playlist_id": playlist_id})

    def youtube_community_post(self, post_id):
        """Get a YouTube community post."""
        return self.request("/v1/youtube/community-post", {"post_id": post_id})

    # ==========================================
    # LinkedIn (4 + 2 ad library endpoints)
    # ==========================================

    def linkedin_profile(self, url):
        """Get LinkedIn person's profile. Pass full LinkedIn URL or username."""
        return self.request("/v1/linkedin/profile", {"url": url})

    def linkedin_company(self, url):
        """Get LinkedIn company page. Pass full LinkedIn URL or company name."""
        return self.request("/v1/linkedin/company", {"url": url})

    def linkedin_company_posts(self, url):
        """Get posts from a LinkedIn company page."""
        return self.request("/v1/linkedin/company/posts", {"url": url})

    def linkedin_post(self, url):
        """Get a specific LinkedIn post."""
        return self.request("/v1/linkedin/post", {"url": url})

    def linkedin_ads_search(self, query):
        """Search LinkedIn Ad Library."""
        return self.request("/v1/linkedin/ads/search", {"query": query})

    def linkedin_ad(self, ad_id):
        """Get LinkedIn ad details."""
        return self.request("/v1/linkedin/ad", {"ad_id": str(ad_id)})

    # ==========================================
    # Facebook (8 + 4 ad library endpoints)
    # ==========================================

    def facebook_profile(self, username):
        """Get Facebook profile."""
        return self.request("/v1/facebook/profile", {"username": username})

    def facebook_reels(self, username):
        """Get reels from a Facebook profile."""
        return self.request("/v1/facebook/profile/reels", {"username": username})

    def facebook_photos(self, username):
        """Get photos from a Facebook profile."""
        return self.request("/v1/facebook/profile/photos", {"username": username})

    def facebook_posts(self, username):
        """Get posts from a Facebook profile."""
        return self.request("/v1/facebook/profile/posts", {"username": username})

    def facebook_group_posts(self, group_id):
        """Get posts from a Facebook group."""
        return self.request("/v1/facebook/group/posts", {"group_id": group_id})

    def facebook_post(self, post_id):
        """Get a specific Facebook post."""
        return self.request("/v1/facebook/post", {"post_id": str(post_id)})

    def facebook_transcript(self, post_id):
        """Get transcript for a Facebook video."""
        return self.request("/v1/facebook/post/transcript", {"post_id": str(post_id)})

    def facebook_comments(self, post_id):
        """Get comments on a Facebook post."""
        return self.request("/v1/facebook/post/comments", {"post_id": str(post_id)})

    def facebook_ad(self, ad_id):
        """Get Facebook Ad Library ad details."""
        return self.request("/v1/facebook/adLibrary/ad", {"ad_id": str(ad_id)})

    def facebook_ads_search(self, query, country=None):
        """Search Facebook Ad Library."""
        params = {"query": query}
        if country:
            params["country"] = country
        return self.request("/v1/facebook/adLibrary/search/ads", params)

    def facebook_company_ads(self, company):
        """Get ads from a specific company in Facebook Ad Library."""
        return self.request("/v1/facebook/adLibrary/company/ads", {"company": company})

    def facebook_ads_companies(self, query):
        """Search for companies in Facebook Ad Library."""
        return self.request("/v1/facebook/adLibrary/search/companies", {"query": query})

    # ==========================================
    # Google Ad Library (3 endpoints)
    # ==========================================

    def google_company_ads(self, company):
        """Get ads from a company in Google Ad Library."""
        return self.request("/v1/google/company/ads", {"company": company})

    def google_ad(self, ad_id):
        """Get Google ad details."""
        return self.request("/v1/google/ad", {"ad_id": str(ad_id)})

    def google_advertisers_search(self, query):
        """Search for advertisers in Google Ad Library."""
        return self.request("/v1/google/adLibrary/advertisers/search", {"query": query})

    # ==========================================
    # Twitter/X (6 endpoints)
    # ==========================================

    def twitter_profile(self, username):
        """Get Twitter/X profile."""
        username = username.lstrip("@")
        return self.request("/v1/twitter/profile", {"username": username})

    def twitter_tweets(self, username):
        """Get tweets from a Twitter/X user."""
        username = username.lstrip("@")
        return self.request("/v1/twitter/user-tweets", {"username": username})

    def twitter_tweet(self, tweet_id):
        """Get a specific tweet."""
        return self.request("/v1/twitter/tweet", {"tweet_id": str(tweet_id)})

    def twitter_transcript(self, tweet_id):
        """Get transcript for a Twitter/X video."""
        return self.request("/v1/twitter/tweet/transcript", {"tweet_id": str(tweet_id)})

    def twitter_community(self, community_id):
        """Get a Twitter/X community."""
        return self.request("/v1/twitter/community", {"community_id": str(community_id)})

    def twitter_community_tweets(self, community_id):
        """Get tweets from a Twitter/X community."""
        return self.request("/v1/twitter/community/tweets", {"community_id": str(community_id)})

    # ==========================================
    # Reddit (7 endpoints)
    # ==========================================

    def reddit_subreddit_details(self, name):
        """Get subreddit details."""
        return self.request("/v1/reddit/subreddit/details", {"subreddit": name})

    def reddit_subreddit_posts(self, name):
        """Get posts from a subreddit."""
        return self.request("/v1/reddit/subreddit", {"subreddit": name})

    def reddit_subreddit_search(self, name, query):
        """Search within a subreddit."""
        return self.request("/v1/reddit/subreddit/search", {"subreddit": name, "query": query})

    def reddit_post_comments(self, post_id):
        """Get comments on a Reddit post."""
        return self.request("/v1/reddit/post/comments", {"post_id": post_id})

    def reddit_search(self, query):
        """Search Reddit globally."""
        return self.request("/v1/reddit/search", {"query": query})

    def reddit_ads_search(self, query):
        """Search Reddit Ad Library."""
        return self.request("/v1/reddit/ads/search", {"query": query})

    def reddit_ad(self, ad_id):
        """Get Reddit ad details."""
        return self.request("/v1/reddit/ad", {"ad_id": str(ad_id)})

    # ==========================================
    # Threads (4 endpoints)
    # ==========================================

    def threads_profile(self, username):
        """Get Threads profile."""
        username = username.lstrip("@")
        return self.request("/v1/threads/profile", {"username": username})

    def threads_posts(self, username):
        """Get posts from a Threads user."""
        username = username.lstrip("@")
        return self.request("/v1/threads/user/posts", {"username": username})

    def threads_post(self, post_id):
        """Get a specific Threads post."""
        return self.request("/v1/threads/post", {"post_id": str(post_id)})

    def threads_search_users(self, query):
        """Search Threads users."""
        return self.request("/v1/threads/search/users", {"query": query})

    # ==========================================
    # Bluesky (3 endpoints)
    # ==========================================

    def bluesky_profile(self, handle):
        """Get Bluesky profile."""
        return self.request("/bluesky/profile", {"handle": handle})

    def bluesky_posts(self, handle):
        """Get posts from a Bluesky user."""
        return self.request("/bluesky/user/posts", {"handle": handle})

    def bluesky_post(self, uri):
        """Get a specific Bluesky post."""
        return self.request("/bluesky/post", {"uri": uri})

    # ==========================================
    # Pinterest (4 endpoints)
    # ==========================================

    def pinterest_search(self, query):
        """Search Pinterest."""
        return self.request("/v1/pinterest/search", {"query": query})

    def pinterest_pin(self, pin_id):
        """Get a Pinterest pin."""
        return self.request("/v1/pinterest/pin", {"pin_id": str(pin_id)})

    def pinterest_boards(self, username):
        """Get boards from a Pinterest user."""
        return self.request("/v1/pinterest/user/boards", {"username": username})

    def pinterest_board(self, board_id):
        """Get a Pinterest board."""
        return self.request("/v1/pinterest/board", {"board_id": str(board_id)})

    # ==========================================
    # Truth Social (3 endpoints)
    # ==========================================

    def truthsocial_profile(self, username):
        """Get Truth Social profile."""
        return self.request("/v1/truthsocial/profile", {"username": username})

    def truthsocial_posts(self, username):
        """Get posts from a Truth Social user."""
        return self.request("/v1/truthsocial/user/posts", {"username": username})

    def truthsocial_post(self, post_id):
        """Get a specific Truth Social post."""
        return self.request("/v1/truthsocial/post", {"post_id": str(post_id)})

    # ==========================================
    # Other platforms
    # ==========================================

    def google_search(self, query):
        """Run a Google search."""
        return self.request("/v1/google/search", {"query": query})

    def twitch_profile(self, username):
        """Get Twitch profile."""
        return self.request("/v1/twitch/profile", {"username": username})

    def twitch_clip(self, clip_id):
        """Get a Twitch clip."""
        return self.request("/v1/twitch/clip", {"clip_id": clip_id})

    def kick_clip(self, clip_id):
        """Get a Kick clip."""
        return self.request("/v1/kick/clip", {"clip_id": clip_id})

    def snapchat_profile(self, username):
        """Get Snapchat profile."""
        return self.request("/v1/snapchat/profile", {"username": username})

    def linktree(self, username):
        """Get a Linktree page."""
        return self.request("/v1/linktree", {"username": username})

    def komi(self, username):
        """Get a Komi page."""
        return self.request("/v1/komi", {"username": username})

    def pillar(self, username):
        """Get a Pillar page."""
        return self.request("/v1/pillar", {"username": username})

    def linkbio(self, username):
        """Get a Linkbio page."""
        return self.request("/v1/linkbio", {"username": username})

    def linkme(self, username):
        """Get a Linkme page."""
        return self.request("/v1/linkme", {"username": username})

    def amazon_shop(self, url):
        """Get an Amazon Shop page."""
        return self.request("/v1/amazon/shop", {"url": url})

    def detect_age_gender(self, image_url):
        """Detect age and gender from an image URL."""
        return self.request("/v1/detect-age-gender", {"image_url": image_url})

    def credit_balance(self):
        """Get current credit balance."""
        return self.request("/v1/credit-balance", credits=0)

    # ==========================================
    # Summary
    # ==========================================

    def summary(self):
        """Return usage summary."""
        return {
            "credits_used": self.credits_used,
            "calls_made": self.calls_made,
        }
