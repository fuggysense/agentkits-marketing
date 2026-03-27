---
name: scrapecreators
version: "1.0.0"
brand: AgentKits Marketing by AityTech
category: utility
difficulty: beginner
description: "Universal social intelligence API client for 25+ platforms. Use when any skill or agent needs social media data — profiles, videos, posts, comments, transcripts, trending content, ad library research, or competitor scanning. Covers TikTok, Instagram, YouTube, LinkedIn, Facebook, Twitter/X, Reddit, Threads, Pinterest, Bluesky, Google, and more. Replaces direct API calls scattered across skills."
triggers:
  - scrape profile
  - social intelligence
  - competitor scan
  - ad library
  - trending content
  - tiktok data
  - instagram data
  - youtube data
  - linkedin data
  - facebook data
  - twitter data
  - reddit data
  - competitor videos
  - audience demographics
  - social media data
  - scrape creator
  - meta ad library
  - google ad library
prerequisites: []
related_skills:
  - tiktok-slideshows
  - linkedin-content
  - youtube-content
  - competitor-alternatives
  - paid-media-audit
  - content-moat
  - social-media
agents:
  - researcher
  - attraction-specialist
mcp_integrations:
  optional: []
success_metrics:
  - api_calls_successful
  - credits_efficiency
  - data_freshness
---

## Graph Links
- **Feeds into:** [[tiktok-slideshows]], [[linkedin-content]], [[youtube-content]], [[competitor-alternatives]], [[paid-media-audit]], [[content-moat]]
- **Foundation for:** Any skill needing real social media data

---

## When to Use

| Intent | Command |
|--------|---------|
| Research a competitor's TikTok | `scrape.py tiktok videos @competitor` |
| Find trending TikTok hooks | `scrape.py tiktok trending --feed` |
| Get Instagram profile stats | `scrape.py instagram profile @username` |
| Research YouTube channel | `scrape.py youtube videos <channel_id>` |
| Search Meta Ad Library | `scrape.py facebook ads-search "keyword"` |
| Get LinkedIn company posts | `scrape.py linkedin company-posts <url>` |
| Research Reddit discussions | `scrape.py reddit subreddit <name>` |
| Check API credit balance | `scrape.py credits` |

---

## Quick Start

```bash
# 1. Set your API key in .env
echo 'SCRAPECREATORS_API_KEY=your_key' >> .env

# 2. Get a TikTok profile
python3 skills/scrapecreators/scripts/scrape.py tiktok profile @charlidamelio

# 3. Search for competitor content
python3 skills/scrapecreators/scripts/scrape.py tiktok search "ai marketing" --type top

# 4. Get trending hashtags
python3 skills/scrapecreators/scripts/scrape.py tiktok trending --hashtags

# 5. Research Meta ads
python3 skills/scrapecreators/scripts/scrape.py facebook ads-search "saas tools" --country US

# 6. Check remaining credits
python3 skills/scrapecreators/scripts/scrape.py credits
```

---

## Platform Reference

### TikTok (20 endpoints + 4 TikTok Shop)
| Command | Endpoint | Credits |
|---------|----------|---------|
| `tiktok profile <user>` | `/v1/tiktok/profile` | 1 |
| `tiktok audience <user>` | `/v1/tiktok/user/audience` | **26** |
| `tiktok videos <user> [--pages N]` | `/v3/tiktok/profile/videos` | 1/page |
| `tiktok video <id>` | `/v2/tiktok/video` | 1 |
| `tiktok transcript <id>` | `/v1/tiktok/video/transcript` | 1 |
| `tiktok comments <id>` | `/v1/tiktok/video/comments` | 1 |
| `tiktok search <query> [--type]` | `/v1/tiktok/search/*` | 1 |
| `tiktok trending [--hashtags\|--sounds\|--creators\|--feed]` | `/v1/tiktok/*/popular` | 1 |
| `tiktok shop <query>` | `/v1/tiktok/shop/search` | 1 |
| `tiktok song <id> [--videos]` | `/v1/tiktok/song[/videos]` | 1 |
| `tiktok following <user>` | `/v1/tiktok/user/following` | 1 |
| `tiktok followers <user>` | `/v1/tiktok/user/followers` | 1 |
| `tiktok live <user>` | `/v1/tiktok/user/live` | 1 |

### Instagram (12 endpoints)
| Command | Endpoint | Credits |
|---------|----------|---------|
| `instagram profile <user>` | `/v1/instagram/profile` | 1 |
| `instagram posts <user>` | `/v2/instagram/user/posts` | 1 |
| `instagram post <shortcode>` | `/v1/instagram/post` | 1 |
| `instagram transcript <shortcode>` | `/v2/instagram/media/transcript` | 1 |
| `instagram comments <shortcode>` | `/v2/instagram/post/comments` | 1 |
| `instagram reels <user>` | `/v1/instagram/user/reels` | 1 |
| `instagram search-reels <query>` | `/v2/instagram/reels/search` | 1 |
| `instagram highlights <user>` | `/v1/instagram/user/highlights` | 1 |

### YouTube (11 endpoints)
| Command | Endpoint | Credits |
|---------|----------|---------|
| `youtube channel <id>` | `/v1/youtube/channel` | 1 |
| `youtube videos <channel_id>` | `/v1/youtube/channel-videos` | 1 |
| `youtube shorts <channel_id>` | `/v1/youtube/channel/shorts` | 1 |
| `youtube video <id>` | `/v1/youtube/video` | 1 |
| `youtube transcript <id>` | `/v1/youtube/video/transcript` | 1 |
| `youtube search <query> [--type]` | `/v1/youtube/search` | 1 |
| `youtube comments <id>` | `/v1/youtube/video/comments` | 1 |
| `youtube trending-shorts` | `/v1/youtube/shorts/trending` | 1 |
| `youtube playlist <id>` | `/v1/youtube/playlist` | 1 |

### LinkedIn (6 endpoints)
| Command | Endpoint | Credits |
|---------|----------|---------|
| `linkedin profile <url>` | `/v1/linkedin/profile` | 1 |
| `linkedin company <url>` | `/v1/linkedin/company` | 1 |
| `linkedin company-posts <url>` | `/v1/linkedin/company/posts` | 1 |
| `linkedin post <url>` | `/v1/linkedin/post` | 1 |
| `linkedin ads <query>` | `/v1/linkedin/ads/search` | 1 |

### Facebook (8 + 4 Ad Library endpoints)
| Command | Endpoint | Credits |
|---------|----------|---------|
| `facebook profile <user>` | `/v1/facebook/profile` | 1 |
| `facebook posts <user>` | `/v1/facebook/profile/posts` | 1 |
| `facebook reels <user>` | `/v1/facebook/profile/reels` | 1 |
| `facebook ads-search <query> [--country]` | `/v1/facebook/adLibrary/search/ads` | 1 |
| `facebook company-ads <company>` | `/v1/facebook/adLibrary/company/ads` | 1 |
| `facebook group <group_id>` | `/v1/facebook/group/posts` | 1 |

### Twitter/X (6 endpoints)
| Command | Endpoint | Credits |
|---------|----------|---------|
| `twitter profile <user>` | `/v1/twitter/profile` | 1 |
| `twitter tweets <user>` | `/v1/twitter/user-tweets` | 1 |
| `twitter tweet <id>` | `/v1/twitter/tweet` | 1 |
| `twitter transcript <id>` | `/v1/twitter/tweet/transcript` | 1 |

### Reddit (7 endpoints)
| Command | Endpoint | Credits |
|---------|----------|---------|
| `reddit subreddit <name>` | `/v1/reddit/subreddit` | 1 |
| `reddit subreddit-details <name>` | `/v1/reddit/subreddit/details` | 1 |
| `reddit search <query>` | `/v1/reddit/search` | 1 |
| `reddit subreddit-search <name> <query>` | `/v1/reddit/subreddit/search` | 1 |
| `reddit comments <post_id>` | `/v1/reddit/post/comments` | 1 |

### Other Platforms
| Command | Credits |
|---------|---------|
| `threads profile/posts/search` | 1 |
| `bluesky profile/posts` | 1 |
| `pinterest search/boards` | 1 |
| `google search/company-ads/advertisers` | 1 |

---

## Credit Awareness

| Endpoint | Credits | Note |
|----------|---------|------|
| Most endpoints | 1 | Standard |
| TikTok audience demographics | **26** | Use sparingly |
| Multi-page pagination | 1/page | Cap with `--pages` |

**Budget rule:** A typical competitor scan (3 profiles + 2 keywords + trending) = ~7 credits.

---

## Python Import Guide

Other skills can import `ScrapeCreatorsClient` directly:

```python
import sys
from pathlib import Path

# Add scrapecreators to path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scrapecreators" / "scripts"))
from api import ScrapeCreatorsClient

# Initialize (auto-loads API key from .env)
client = ScrapeCreatorsClient(quiet=True)

# Use any platform method
videos = client.tiktok_videos("charlidamelio")
profile = client.instagram_profile("nike")
channel = client.youtube_channel("UC-lHJZR3Gqxm24_Vd_AJ5Yw")

# Check usage
print(client.summary())  # {'credits_used': 3, 'calls_made': 3}
```

For generic/new endpoints not yet wrapped:
```python
data = client.request("/v1/some/new/endpoint", {"param": "value"})
```

---

## Common Flows

### Competitor Analysis (5-7 credits)
```bash
# Profile overview
scrape.py tiktok profile @competitor
# Recent videos with engagement
scrape.py tiktok videos @competitor --pages 2
# What they're ranking for
scrape.py tiktok search "their niche keyword" --type top
```

### Trend Monitoring (3-4 credits)
```bash
# What's trending right now
scrape.py tiktok trending --hashtags
scrape.py tiktok trending --sounds
scrape.py tiktok trending --feed
```

### Ad Research (2-3 credits)
```bash
# Search competitor ads
scrape.py facebook ads-search "competitor name" --country US
# Google ads too
scrape.py google company-ads "competitor name"
```

### Content Research (3-5 credits)
```bash
# YouTube competitor deep dive
scrape.py youtube videos UC-channelid
scrape.py youtube transcript dQw4w9WgXcQ
# Reddit audience research
scrape.py reddit subreddit-search "marketing" "ai tools"
```

---

## Output Formats

- **Markdown** (default in terminal): Human-readable tables and sections
- **JSON** (default when piped): Machine-readable for other scripts

```bash
# Force JSON output
scrape.py tiktok profile @user --format json

# Pipe to file
scrape.py tiktok videos @user --format json -o data/competitor.json

# Pipe to jq
scrape.py tiktok profile @user --format json | jq '.data.followerCount'
```

---

## Error Handling

The client raises typed exceptions:
- `AuthError` — Invalid API key (check `.env`)
- `NotFoundError` — User/video/post not found
- `RateLimitError` — Too many requests
- `ServerError` — API server issue (auto-retries once)

---

## Setup

1. Get API key at https://app.scrapecreators.com
2. Add to `.env`: `SCRAPECREATORS_API_KEY=your_key_here`
3. Install `requests`: `pip install requests`
4. Run: `python3 skills/scrapecreators/scripts/scrape.py credits`
