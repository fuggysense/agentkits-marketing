---
name: meta-ads-uploader
version: "1.0.0"
category: paid-media
description: "End-to-end Meta (Facebook/Instagram) ad creative uploader. Bridges copy generation to live ads. Triggers: upload ads, create meta ads, bulk upload, publish, launch ads, deploy, upload creatives, push ads."
triggers:
  - upload ads
  - create meta ads
  - bulk upload ads
  - publish ads to meta
  - facebook ads upload
  - instagram ads upload
  - ad creative upload
  - launch ads
  - deploy ads to meta
  - upload creatives
  - push ads to meta
related_skills:
  - paid-advertising
  - copywriting
  - image-generation
  - video-director
  - campaign-runner
  - paid-media-audit
agents:
  - copywriter
  - researcher
---

# Meta Ads Creative Uploader

End-to-end pipeline for uploading ad creatives to Meta (Facebook/Instagram). Bridges the gap between copy generation and live ads.

**Before:** Copy → markdown → manual copy-paste → manual image upload → manual campaign setup
**After:** Copy → bundle JSON → one command → ads live (paused) in Meta

---

## When to Use

- After generating ad copy with `copywriting` or `/content:ads`
- After creating ad images with `image-generation`
- After creating ad videos with `video-director`
- When you have a creative bundle ready to publish to Meta Ads
- When running ad campaigns via `campaign-runner`

**Not for:** Campaign/ad-set creation with budgets (use Meta Ads MCP), audience targeting, or analytics (use `paid-media-audit`).

---

## Quick Start

### 1. Generate Creative Bundle

After running `/content:ads` and `image-generation`, structure output as a creative bundle:

```bash
# Validate (no API calls)
python3 skills/meta-ads-uploader/scripts/upload.py validate bundle.json

# Preview what will happen
python3 skills/meta-ads-uploader/scripts/upload.py preview bundle.json

# Upload everything — ads created PAUSED
python3 skills/meta-ads-uploader/scripts/upload.py full bundle.json
```

### 2. Review in Ads Manager

All ads are created **PAUSED**. Review previews in Ads Manager, then activate manually.

---

## Creative Bundle Format

The bundle JSON is the bridge between copy/images and the Meta API. See `templates/creative-bundle.json` for a full example.

```json
{
  "bundle_name": "campaign-name",
  "page_id": "YOUR_PAGE_ID",
  "instagram_actor_id": "YOUR_INSTAGRAM_ID",
  "ad_set_id": "TARGET_AD_SET_ID",
  "url_tags": "utm_source=meta&utm_medium=paid&utm_campaign=...",
  "creatives": [
    {
      "name": "Descriptive-Name",
      "format": "single_image",
      "image_path": "relative/path/to/image.png",
      "primary_texts": ["Text variation 1", "Text variation 2"],
      "headlines": ["Headline 1", "Headline 2"],
      "descriptions": ["Short description"],
      "link_url": "https://example.com/landing",
      "cta_type": "LEARN_MORE"
    }
  ]
}
```

### Format Rules

| Field | Rule |
|-------|------|
| `format` | `single_image` or `single_video` |
| `primary_texts` | Multiple → dynamic creative (Meta auto-rotates) |
| `headlines` | Multiple → dynamic creative |
| `descriptions` | Optional, multiple supported |
| `image_path` | Relative to bundle file location |
| `cta_type` | See CTA Types below |

### Character Limits

| Field | Max | Recommended |
|-------|-----|-------------|
| Primary text | 125 chars | < 100 |
| Headline | 40 chars | < 30 |
| Description | 25 chars | < 20 |

---

## CLI Commands

```bash
# Validate bundle structure (no API calls)
upload.py validate <bundle.json>

# Dry run — show what would be created
upload.py preview <bundle.json>

# Upload images/videos only, print hashes
upload.py upload-media <bundle.json>

# Full pipeline: upload → create creatives → create ads (PAUSED)
upload.py full <bundle.json>

# Check status of previously uploaded bundle
upload.py status <bundle.json>
```

**Flags:** `--quiet` (suppress progress), `--dry-run` (no API calls)

**Resumable:** If a run fails partway through, re-running skips already-completed items. Results saved to `<bundle>_results.json`.

---

## HITL Gates (Non-Negotiable)

| Gate | When | What |
|------|------|------|
| **Bundle Review** | Before any API call | Claude presents bundle summary. Jerel approves. |
| **Media Upload Confirm** | After `upload-media` | Show uploaded asset confirmations. |
| **Creative Preview** | After creatives created | Provide Ads Manager preview links. |
| **Go-Live** | Always | Ads created PAUSED. Jerel activates manually. |
| **Spend** | Never automated | This skill never sets budgets or activates spend. |

---

## Integration with Other Skills

### Typical Flow

```
1. /content:ads → copywriter generates ad variants
2. Claude structures output as creative-bundle.json
3. image-generation → produces ad images
4. Claude fills image_path references in bundle
5. HITL: Claude presents bundle for review
6. python upload.py full bundle.json
   → Images uploaded → Creatives created → Ads created (PAUSED)
7. HITL: Review ad previews in Ads Manager
8. Activate when ready
9. Analytics via Meta Ads MCP insights
```

### With campaign-runner

When `campaign-runner` reaches the "Ad launch" task, it routes to this skill instead of "Manual."

### With video-director

Video ads follow the same flow — set `format: "single_video"` and provide `video_path` + optional `thumbnail_path`.

---

## CTA Types Reference

| CTA | Best For |
|-----|----------|
| `LEARN_MORE` | Awareness, education content |
| `SHOP_NOW` | E-commerce, product pages |
| `SIGN_UP` | SaaS trials, newsletters |
| `SUBSCRIBE` | Subscriptions, memberships |
| `DOWNLOAD` | Lead magnets, apps |
| `BOOK_TRAVEL` | Travel, hospitality |
| `GET_OFFER` | Promotions, discounts |
| `GET_QUOTE` | Services, B2B |
| `APPLY_NOW` | Jobs, applications |
| `CONTACT_US` | Services, support |
| `WATCH_MORE` | Video content |
| `NO_BUTTON` | Brand awareness (no CTA) |

---

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| `AuthError` | Invalid token or dev mode app | Regenerate token with `ads_management` permission. App must be in LIVE mode. |
| `RateLimitError` | Too many API calls | Wait and retry. Standard limit: 200 calls/hour/account. |
| `CreativeError` | Invalid image hash, missing fields | Check bundle validation output. Ensure images uploaded first. |
| `ServerError` | Meta API issues | Auto-retries once. If persistent, check Meta API status. |

---

## Setup Guide

### 1. Environment Variables

Add to `.env`:

```bash
META_ADS_ACCESS_TOKEN=your_token_here
META_AD_ACCOUNT_ID=act_123456789
META_PAGE_ID=your_page_id   # Optional — can also set in bundle
```

### 2. Token Requirements

- **Permissions:** `ads_management`, `ads_read`, `pages_show_list`
- **App mode:** Must be **LIVE** (not development) — #1 gotcha
- **Token type:** System User token (long-lived) recommended over personal token

### 3. Get Your Token

1. Go to [Meta Business Suite](https://business.facebook.com)
2. Business Settings → System Users
3. Create System User with `ads_management` permission
4. Generate access token
5. Set app to LIVE mode in App Dashboard

### 4. Dependencies

```bash
pip install requests
pip install Pillow  # Optional — for WebP/HEIC auto-conversion
```

---

## Safety Rules

1. **Ads always PAUSED** — the `create_ad` method forces PAUSED regardless of input
2. **No budget control** — this skill never creates campaigns or ad sets with budgets
3. **All mutations logged** — every API call that changes state logs to stderr
4. **Resumable** — results sidecar file enables safe re-runs
5. **Image conversion** — WebP/TIFF/HEIC auto-converted to PNG before upload

<!-- skill-graph:start -->

## Related
<!-- auto-generated by scripts/link-skills.py — do not edit by hand -->

- [[ad-library-scraper]] (skill, 0.19)
- [[scrapecreators]] (skill, 0.19)
- [[ad-concept-engine]] (skill, 0.18)
- [[headline-bank]] (skill, 0.18)
- [[sheets-updater]] (skill, 0.16)

<!-- skill-graph:end -->
