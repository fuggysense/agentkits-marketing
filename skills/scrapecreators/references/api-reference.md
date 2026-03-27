# ScrapeCreators API Reference

> Full endpoint catalog. Base URL: `https://api.scrapecreators.com`
> Auth: `x-api-key` header. Cost: 1 credit/request unless noted.
> Docs: https://docs.scrapecreators.com

---

## TikTok (20 endpoints)

| # | Name | Method | Path | Key Params | Credits |
|---|------|--------|------|------------|---------|
| 1 | Profile | GET | `/v1/tiktok/profile` | `username` | 1 |
| 2 | Audience Demographics | GET | `/v1/tiktok/user/audience` | `username` | **26** |
| 3 | Profile Videos | GET | `/v3/tiktok/profile/videos` | `username`, `cursor` | 1 |
| 4 | Video Info | GET | `/v2/tiktok/video` | `video_id` | 1 |
| 5 | Transcript | GET | `/v1/tiktok/video/transcript` | `video_id` | 1 |
| 6 | TikTok Live | GET | `/v1/tiktok/user/live` | `username` | 1 |
| 7 | Comments | GET | `/v1/tiktok/video/comments` | `video_id` | 1 |
| 8 | Following | GET | `/v1/tiktok/user/following` | `username` | 1 |
| 9 | Followers | GET | `/v1/tiktok/user/followers` | `username` | 1 |
| 10 | Search Users | GET | `/v1/tiktok/search/users` | `keyword` | 1 |
| 11 | Search by Hashtag | GET | `/v1/tiktok/search/hashtag` | `hashtag` | 1 |
| 12 | Search by Keyword | GET | `/v1/tiktok/search/keyword` | `keyword` | 1 |
| 13 | Top Search | GET | `/v1/tiktok/search/top` | `keyword` | 1 |
| 14 | Popular Songs | GET | `/v1/tiktok/songs/popular` | — | 1 |
| 15 | Popular Creators | GET | `/v1/tiktok/creators/popular` | — | 1 |
| 16 | Popular Videos | GET | `/v1/tiktok/videos/popular` | — | 1 |
| 17 | Popular Hashtags | GET | `/v1/tiktok/hashtags/popular` | — | 1 |
| 18 | Song Details | GET | `/v1/tiktok/song` | `song_id` | 1 |
| 19 | TikToks using Song | GET | `/v1/tiktok/song/videos` | `song_id` | 1 |
| 20 | Trending Feed | GET | `/v1/tiktok/get-trending-feed` | — | 1 |

### Pagination
Profile Videos (endpoint #3) supports cursor-based pagination. Response includes a `cursor` field — pass it back to get the next page. Each page = 1 credit.

---

## TikTok Shop (4 endpoints)

| # | Name | Method | Path | Key Params | Credits |
|---|------|--------|------|------------|---------|
| 1 | Shop Search | GET | `/v1/tiktok/shop/search` | `keyword` | 1 |
| 2 | Shop Products | GET | `/v1/tiktok/shop/products` | `username` | 1 |
| 3 | Product Details | GET | `/v1/tiktok/product` | `product_id` | 1 |
| 4 | Product Reviews | GET | `/v1/tiktok/shop/product/reviews` | `product_id` | 1 |

---

## Instagram (12 endpoints)

| # | Name | Method | Path | Key Params | Credits |
|---|------|--------|------|------------|---------|
| 1 | Profile | GET | `/v1/instagram/profile` | `username` | 1 |
| 2 | Basic Profile | GET | `/v1/instagram/basic-profile` | `username` | 1 |
| 3 | Posts | GET | `/v2/instagram/user/posts` | `username` | 1 |
| 4 | Post/Reel Info | GET | `/v1/instagram/post` | `shortcode` | 1 |
| 5 | Transcript | GET | `/v2/instagram/media/transcript` | `shortcode` | 1 |
| 6 | Search Reels | GET | `/v2/instagram/reels/search` | `keyword` | 1 |
| 7 | Comments | GET | `/v2/instagram/post/comments` | `shortcode` | 1 |
| 8 | Reels | GET | `/v1/instagram/user/reels` | `username` | 1 |
| 9 | Story Highlights | GET | `/v1/instagram/user/highlights` | `username` | 1 |
| 10 | Highlight Details | GET | `/v1/instagram/user/highlight/detail` | `highlight_id` | 1 |
| 11 | Reels using Song | GET | `/v1/instagram/song/reels` | `song_id` | 1 (deprecated) |
| 12 | Embed HTML | GET | `/v1/instagram/user/embed` | `username` | 1 |

---

## YouTube (11 endpoints)

| # | Name | Method | Path | Key Params | Credits |
|---|------|--------|------|------------|---------|
| 1 | Channel Details | GET | `/v1/youtube/channel` | `channel_id` | 1 |
| 2 | Channel Videos | GET | `/v1/youtube/channel-videos` | `channel_id` | 1 |
| 3 | Channel Shorts | GET | `/v1/youtube/channel/shorts` | `channel_id` | 1 |
| 4 | Video/Short Details | GET | `/v1/youtube/video` | `video_id` | 1 |
| 5 | Transcript | GET | `/v1/youtube/video/transcript` | `video_id` | 1 |
| 6 | Search | GET | `/v1/youtube/search` | `query`, `type` | 1 |
| 7 | Search by Hashtag | GET | `/v1/youtube/search/hashtag` | `hashtag` | 1 |
| 8 | Comments | GET | `/v1/youtube/video/comments` | `video_id` | 1 |
| 9 | Trending Shorts | GET | `/v1/youtube/shorts/trending` | — | 1 |
| 10 | Playlist | GET | `/v1/youtube/playlist` | `playlist_id` | 1 |
| 11 | Community Post | GET | `/v1/youtube/community-post` | `post_id` | 1 |

---

## LinkedIn (4 + 2 Ad Library endpoints)

| # | Name | Method | Path | Key Params | Credits |
|---|------|--------|------|------------|---------|
| 1 | Person's Profile | GET | `/v1/linkedin/profile` | `url` | 1 |
| 2 | Company Page | GET | `/v1/linkedin/company` | `url` | 1 |
| 3 | Company Posts | GET | `/v1/linkedin/company/posts` | `url` | 1 |
| 4 | Post | GET | `/v1/linkedin/post` | `url` | 1 |
| 5 | Search Ads | GET | `/v1/linkedin/ads/search` | `query` | 1 |
| 6 | Ad Details | GET | `/v1/linkedin/ad` | `ad_id` | 1 |

---

## Facebook (8 + 4 Ad Library endpoints)

| # | Name | Method | Path | Key Params | Credits |
|---|------|--------|------|------------|---------|
| 1 | Profile | GET | `/v1/facebook/profile` | `username` | 1 |
| 2 | Profile Reels | GET | `/v1/facebook/profile/reels` | `username` | 1 |
| 3 | Profile Photos | GET | `/v1/facebook/profile/photos` | `username` | 1 |
| 4 | Profile Posts | GET | `/v1/facebook/profile/posts` | `username` | 1 |
| 5 | Group Posts | GET | `/v1/facebook/group/posts` | `group_id` | 1 |
| 6 | Post | GET | `/v1/facebook/post` | `post_id` | 1 |
| 7 | Transcript | GET | `/v1/facebook/post/transcript` | `post_id` | 1 |
| 8 | Comments | GET | `/v1/facebook/post/comments` | `post_id` | 1 |

### Facebook Ad Library
| # | Name | Method | Path | Key Params | Credits |
|---|------|--------|------|------------|---------|
| 1 | Ad Details | GET | `/v1/facebook/adLibrary/ad` | `ad_id` | 1 |
| 2 | Search Ads | GET | `/v1/facebook/adLibrary/search/ads` | `query`, `country` | 1 |
| 3 | Company Ads | GET | `/v1/facebook/adLibrary/company/ads` | `company` | 1 |
| 4 | Search Companies | GET | `/v1/facebook/adLibrary/search/companies` | `query` | 1 |

---

## Google Ad Library (3 endpoints)

| # | Name | Method | Path | Key Params | Credits |
|---|------|--------|------|------------|---------|
| 1 | Company Ads | GET | `/v1/google/company/ads` | `company` | 1 |
| 2 | Ad Details | GET | `/v1/google/ad` | `ad_id` | 1 |
| 3 | Advertiser Search | GET | `/v1/google/adLibrary/advertisers/search` | `query` | 1 |

---

## Twitter/X (6 endpoints)

| # | Name | Method | Path | Key Params | Credits |
|---|------|--------|------|------------|---------|
| 1 | Profile | GET | `/v1/twitter/profile` | `username` | 1 |
| 2 | User Tweets | GET | `/v1/twitter/user-tweets` | `username` | 1 |
| 3 | Tweet Details | GET | `/v1/twitter/tweet` | `tweet_id` | 1 |
| 4 | Transcript | GET | `/v1/twitter/tweet/transcript` | `tweet_id` | 1 |
| 5 | Community | GET | `/v1/twitter/community` | `community_id` | 1 |
| 6 | Community Tweets | GET | `/v1/twitter/community/tweets` | `community_id` | 1 |

---

## Reddit (7 endpoints)

| # | Name | Method | Path | Key Params | Credits |
|---|------|--------|------|------------|---------|
| 1 | Subreddit Details | GET | `/v1/reddit/subreddit/details` | `subreddit` | 1 |
| 2 | Subreddit Posts | GET | `/v1/reddit/subreddit` | `subreddit` | 1 |
| 3 | Subreddit Search | GET | `/v1/reddit/subreddit/search` | `subreddit`, `query` | 1 |
| 4 | Post Comments | GET | `/v1/reddit/post/comments` | `post_id` | 1 |
| 5 | Search | GET | `/v1/reddit/search` | `query` | 1 |
| 6 | Search Ads | GET | `/v1/reddit/ads/search` | `query` | 1 |
| 7 | Get Ad | GET | `/v1/reddit/ad` | `ad_id` | 1 |

---

## Threads (4 endpoints)

| # | Name | Method | Path | Key Params | Credits |
|---|------|--------|------|------------|---------|
| 1 | Profile | GET | `/v1/threads/profile` | `username` | 1 |
| 2 | Posts | GET | `/v1/threads/user/posts` | `username` | 1 |
| 3 | Post | GET | `/v1/threads/post` | `post_id` | 1 |
| 4 | Search Users | GET | `/v1/threads/search/users` | `query` | 1 |

---

## Bluesky (3 endpoints)

| # | Name | Method | Path | Key Params | Credits |
|---|------|--------|------|------------|---------|
| 1 | Profile | GET | `/bluesky/profile` | `handle` | 1 |
| 2 | Posts | GET | `/bluesky/user/posts` | `handle` | 1 |
| 3 | Post | GET | `/bluesky/post` | `uri` | 1 |

---

## Truth Social (3 endpoints)

| # | Name | Method | Path | Key Params | Credits |
|---|------|--------|------|------------|---------|
| 1 | Profile | GET | `/v1/truthsocial/profile` | `username` | 1 |
| 2 | User Posts | GET | `/v1/truthsocial/user/posts` | `username` | 1 |
| 3 | Post | GET | `/v1/truthsocial/post` | `post_id` | 1 |

---

## Pinterest (4 endpoints)

| # | Name | Method | Path | Key Params | Credits |
|---|------|--------|------|------------|---------|
| 1 | Search | GET | `/v1/pinterest/search` | `query` | 1 |
| 2 | Pin | GET | `/v1/pinterest/pin` | `pin_id` | 1 |
| 3 | User Boards | GET | `/v1/pinterest/user/boards` | `username` | 1 |
| 4 | Board | GET | `/v1/pinterest/board` | `board_id` | 1 |

---

## Other Platforms

| Platform | Endpoint | Path | Key Params |
|----------|----------|------|------------|
| Google Search | Search | `/v1/google/search` | `query` |
| Twitch | Profile | `/v1/twitch/profile` | `username` |
| Twitch | Clip | `/v1/twitch/clip` | `clip_id` |
| Kick | Clip | `/v1/kick/clip` | `clip_id` |
| Snapchat | Profile | `/v1/snapchat/profile` | `username` |
| Linktree | Page | `/v1/linktree` | `username` |
| Komi | Page | `/v1/komi` | `username` |
| Pillar | Page | `/v1/pillar` | `username` |
| Linkbio | Page | `/v1/linkbio` | `username` |
| Linkme | Page | `/v1/linkme` | `username` |
| Amazon Shop | Page | `/v1/amazon/shop` | `url` |
| Age/Gender | Detect | `/v1/detect-age-gender` | `image_url` |

---

## Utility

| Endpoint | Path | Credits |
|----------|------|---------|
| Credit Balance | `/v1/credit-balance` | 0 |

---

## Authentication

All requests require the `x-api-key` header:
```
x-api-key: your_api_key_here
```

Get your key at: https://app.scrapecreators.com

---

## Response Format

All endpoints return JSON. Common patterns:
- Profile data usually in `data` or root object
- Video lists in `videos`, `data`, or `data.videos`
- Pagination via `cursor` / `nextCursor` field
- Stats in `statistics` or `stats` sub-object

The Python client normalizes these inconsistencies.

---

## Total: 100+ endpoints across 20+ platforms
