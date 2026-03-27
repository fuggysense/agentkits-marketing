## Graph Links
- **Parent skill:** [[meta-ads-uploader]]
- **Related:** [[paid-advertising]], [[paid-media-audit]]

# Meta Marketing API — Creative Operations Reference

API reference for Meta Marketing API v22.0 creative endpoints used by `meta-ads-uploader`.

---

## Authentication

### Token Requirements

| Permission | Required For |
|------------|-------------|
| `ads_management` | Creating creatives, ads, uploading media |
| `ads_read` | Reading ad previews, checking status |
| `pages_show_list` | Accessing page info for `object_story_spec` |

### LIVE Mode Requirement (Critical)

Your Meta App **must be in LIVE mode**, not development mode. This is the #1 cause of `AuthError`.

**Check:** App Dashboard → App Review → toggle "Live"

Development mode restricts API access to app admins only and blocks creative creation for real ad accounts.

### Token Types

| Type | Lifespan | Recommended For |
|------|----------|-----------------|
| System User Token | Never expires | Production automation |
| User Access Token | 60 days | Testing |
| Page Access Token | Never expires (if extended) | Page-specific operations |

---

## Image Upload

### Endpoint

```
POST /{ad_account_id}/adimages
```

### Request

Multipart form upload:

| Parameter | Type | Description |
|-----------|------|-------------|
| `filename` | file | Image file (JPG, PNG, GIF, BMP) |
| `access_token` | string | Required |

### Response

```json
{
  "images": {
    "filename": {
      "hash": "abc123def456...",
      "url": "https://scontent.xx.fbcdn.net/..."
    }
  }
}
```

### Image Specs

| Spec | Requirement |
|------|-------------|
| Formats | JPG, PNG, GIF, BMP (we auto-convert WebP/TIFF/HEIC) |
| Max file size | 30 MB |
| Min resolution | 600x600 px |
| Recommended | 1080x1080 (square), 1080x1920 (story/reel) |
| Aspect ratios | 1:1, 4:5 (feed), 9:16 (story), 1.91:1 (link) |

---

## Video Upload

### Endpoint

```
POST /{ad_account_id}/advideos
```

### Request

Multipart form upload:

| Parameter | Type | Description |
|-----------|------|-------------|
| `source` | file | Video file |
| `title` | string | Optional title |
| `access_token` | string | Required |

### Response

```json
{
  "id": "123456789"
}
```

### Processing Status

After upload, poll until processing completes:

```
GET /{video_id}?fields=status
```

Response:
```json
{
  "status": {
    "processing_phase": {
      "status": "complete"
    }
  }
}
```

### Video Specs

| Spec | Requirement |
|------|-------------|
| Formats | MP4, MOV (MP4 recommended) |
| Max file size | 4 GB |
| Max duration | 240 minutes |
| Min resolution | 720p |
| Recommended | 1080x1080 (feed), 1080x1920 (story/reel) |
| Codec | H.264 |

---

## Creative Creation

### Endpoint

```
POST /{ad_account_id}/adcreatives
```

### Single Creative (object_story_spec)

For one image/video with one set of text. Uses `object_story_spec`.

#### Image Creative

```json
{
  "name": "My Creative",
  "object_story_spec": {
    "page_id": "PAGE_ID",
    "instagram_actor_id": "IG_ID",
    "link_data": {
      "message": "Primary text (body copy)",
      "link": "https://example.com",
      "name": "Headline text",
      "description": "Description text",
      "image_hash": "abc123...",
      "call_to_action": {
        "type": "LEARN_MORE",
        "value": {"link": "https://example.com"}
      }
    }
  },
  "url_tags": "utm_source=meta&utm_medium=paid"
}
```

#### Video Creative

```json
{
  "name": "My Video Creative",
  "object_story_spec": {
    "page_id": "PAGE_ID",
    "video_data": {
      "message": "Primary text",
      "video_id": "123456789",
      "title": "Headline text",
      "link_description": "Description",
      "call_to_action": {
        "type": "SIGN_UP",
        "value": {"link": "https://example.com"}
      },
      "link_url": "https://example.com"
    }
  }
}
```

### Dynamic Creative (asset_feed_spec)

For multiple text/asset variations. Meta auto-rotates best combinations.

```json
{
  "name": "Dynamic Creative",
  "object_story_spec": {
    "page_id": "PAGE_ID",
    "instagram_actor_id": "IG_ID"
  },
  "asset_feed_spec": {
    "images": [
      {"hash": "hash1"},
      {"hash": "hash2"}
    ],
    "bodies": [
      {"text": "Primary text variation 1"},
      {"text": "Primary text variation 2"}
    ],
    "titles": [
      {"text": "Headline 1"},
      {"text": "Headline 2"}
    ],
    "descriptions": [
      {"text": "Description 1"}
    ],
    "link_urls": [
      {"website_url": "https://example.com"}
    ],
    "call_to_action_types": ["LEARN_MORE"],
    "ad_formats": ["SINGLE_IMAGE"]
  }
}
```

### Response

```json
{
  "id": "CREATIVE_ID"
}
```

---

## Ad Creation

### Endpoint

```
POST /{ad_account_id}/ads
```

### Request

```json
{
  "name": "Ad Name",
  "adset_id": "AD_SET_ID",
  "creative": {"creative_id": "CREATIVE_ID"},
  "status": "PAUSED"
}
```

### Response

```json
{
  "id": "AD_ID"
}
```

**Safety:** Always create with `status: "PAUSED"`. Never auto-activate.

---

## Ad Preview

### Endpoint

```
GET /{creative_id}/previews?ad_format=DESKTOP_FEED_STANDARD
```

### Ad Formats for Preview

| Format | Description |
|--------|-------------|
| `DESKTOP_FEED_STANDARD` | Facebook desktop feed |
| `MOBILE_FEED_STANDARD` | Facebook mobile feed |
| `INSTAGRAM_STANDARD` | Instagram feed |
| `INSTAGRAM_STORY` | Instagram story |
| `INSTAGRAM_REELS` | Instagram reel |
| `RIGHT_COLUMN_STANDARD` | Facebook right column |

---

## CTA Types (Full Enum)

| CTA Type | Typical Use |
|----------|-------------|
| `LEARN_MORE` | Default — awareness, education |
| `SHOP_NOW` | E-commerce, product pages |
| `SIGN_UP` | SaaS free trials, newsletters |
| `SUBSCRIBE` | Subscriptions, recurring services |
| `CONTACT_US` | B2B, service businesses |
| `GET_OFFER` | Promotions, discounts, deals |
| `GET_QUOTE` | Insurance, B2B services |
| `DOWNLOAD` | Apps, lead magnets, resources |
| `BOOK_TRAVEL` | Hotels, flights, experiences |
| `LISTEN_NOW` | Podcasts, music, audio |
| `WATCH_MORE` | Video content, streaming |
| `APPLY_NOW` | Jobs, programs, applications |
| `BUY_NOW` | Direct purchase, urgent offers |
| `GET_DIRECTIONS` | Local businesses, retail |
| `MESSAGE_PAGE` | Customer service, inquiries |
| `CALL_NOW` | Phone-based businesses |
| `OPEN_LINK` | Generic link click |
| `NO_BUTTON` | Pure brand awareness |

---

## Error Codes

| Code | Type | Meaning | Fix |
|------|------|---------|-----|
| 100 | `OAuthException` | Invalid parameter | Check field values, image hashes |
| 102 | `OAuthException` | Session expired | Regenerate access token |
| 104 | `OAuthException` | Access token invalid | Check token permissions |
| 190 | `OAuthException` | Token expired or revoked | Generate new token |
| 4 | `CodedException` | Too many calls | Reduce request rate |
| 17 | `CodedException` | User request limit reached | Wait and retry |
| 10 | `PermissionError` | App not authorized | Check app permissions |
| 200-299 | `PermissionError` | Insufficient permissions | Add required permissions |
| 1487851 | `OAuthException` | Ad account disabled | Check account status |

### Common Gotchas

1. **App in development mode** — most common auth failure. Switch to LIVE.
2. **Missing page permission** — creative creation needs page access.
3. **Invalid image hash** — hash from different ad account won't work.
4. **Character limits** — API accepts longer text but Meta truncates in display.
5. **Video still processing** — must wait for `processing_phase.status: "complete"`.

---

## Rate Limits

| Endpoint Type | Limit |
|---------------|-------|
| Standard API calls | 200/hour per ad account |
| Insights queries | 60/hour per ad account |
| Batch requests | 50 operations per batch |
| Image uploads | No specific limit (counts against standard) |
| Video uploads | 1000/day per ad account |

---

## Useful Graph API Explorer Links

- Test API calls: `https://developers.facebook.com/tools/explorer/`
- Access token debugger: `https://developers.facebook.com/tools/debug/accesstoken/`
- Ad account info: `GET /act_{ID}?fields=name,currency,timezone_name`
