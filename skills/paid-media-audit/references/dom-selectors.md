## Graph Links
- **Parent skill:** [[paid-media-audit]]
- **Sibling references:** [[audit-checklist]], [[creative-analysis-prompts]]
- **Related skills:** [[paid-advertising]], [[analytics-attribution]]

# DOM Selectors & URL Patterns Reference

Meta Ad Library page ID extraction, media download selectors, and URL patterns for competitive ad intelligence.

## Page ID Extraction

### delegate_page ID (preferred — used by Ad Library)

```javascript
// Run on https://www.facebook.com/<page-username>/
const html = document.documentElement.innerHTML;
const delegateMatch = html.match(/"delegate_page":\{[^}]*"id":"(\d+)"/);
const profileMatch = html.match(/fb:\/\/profile\/(\d+)/);
const adLibraryId = delegateMatch ? delegateMatch[1] : (profileMatch ? profileMatch[1] : null);
```

**Why this matters:** Facebook pages have TWO IDs:
- **Profile ID** (from `al:android:url` meta tag) — e.g. `100063910068612`
- **Delegate Page ID** (from page JSON data) — e.g. `103237888271515`

The Ad Library's `view_all_page_id` parameter uses the **delegate_page ID**. Using the profile ID returns zero results or wrong results.

## Ad Library URL Template

```
https://www.facebook.com/ads/library/?active_status={STATUS}&ad_type=all&country={COUNTRY}&is_targeted_country=false&media_type={MEDIA}&search_type=page&view_all_page_id={PAGE_ID}
```

| Parameter | Values | Notes |
|-----------|--------|-------|
| active_status | `active`, `inactive`, `all` | `all` shows full history |
| country | `ALL`, `US`, `DE`, etc. | `ALL` = worldwide |
| media_type | `image_and_meme`, `video`, omit for all | Filter by asset type |
| view_all_page_id | numeric ID | The delegate_page ID |

## Media Extraction JavaScript

### Full extraction script (run via browser evaluate)

```javascript
(() => {
  const results = { images: [], videos: [] };
  const seen = new Set();

  // Extract ad images (600x600 thumbnails)
  document.querySelectorAll('img').forEach(img => {
    const src = img.src || '';
    if (src.includes('fbcdn.net') && src.includes('s600x600') && !seen.has(src)) {
      seen.add(src);
      const adContainer = img.closest('[class*="x1"]');
      results.images.push({
        url: src,
        width: img.naturalWidth || 600,
        height: img.naturalHeight || 600
      });
    }
  });

  // Extract ad videos (direct .mp4 URLs)
  document.querySelectorAll('video').forEach(video => {
    const src = video.src || video.querySelector('source')?.src || '';
    if (src.includes('fbcdn.net') && !seen.has(src)) {
      seen.add(src);
      results.videos.push({
        url: src,
        poster: video.poster || null,
        duration: video.duration || null
      });
    }
  });

  return JSON.stringify(results);
})()
```

### Simpler extraction (just URLs)

```javascript
(() => {
  const imgs = [...document.querySelectorAll('img')]
    .map(i => i.src)
    .filter(s => s.includes('fbcdn.net') && s.includes('s600x600'));
  const vids = [...document.querySelectorAll('video')]
    .map(v => v.src || v.querySelector('source')?.src)
    .filter(Boolean)
    .filter(s => s.includes('fbcdn.net'));
  const posters = [...document.querySelectorAll('video[poster]')]
    .map(v => v.poster)
    .filter(s => s.includes('fbcdn.net'));
  return JSON.stringify({
    images: [...new Set(imgs)],
    videos: [...new Set(vids)],
    posters: [...new Set(posters)]
  });
})()
```

## CDN URL Patterns

### Images
```
https://scontent-{region}.xx.fbcdn.net/v/t39.35426-6/{id}?stp=dst-jpg_s600x600_tt6&...
```
- `s600x600` = resolution (server-enforced max for Ad Library)

### Videos
```
https://video-{region}.xx.fbcdn.net/v/t42.1790-2/{id}?...
```
- Full quality, no resolution cap
- Progressive download, not streaming

### Video Posters (Thumbnails)
```
https://scontent-{region}.xx.fbcdn.net/v/t39.35426-6/{id}?...
```

## Download Commands

```bash
# Single image
curl -sL -o "advertiser-image-01.jpg" "URL"

# Single video
curl -sL -o "advertiser-video-01.mp4" "URL"

# Batch download from extracted JSON
echo "$JSON" | jq -r '.images[].url' | while read -r url; do
  n=$((n+1))
  curl -sL -o "advertiser-image-$(printf '%02d' $n).jpg" "$url"
  sleep 1
done
```

## Scrolling for More Results

The Ad Library lazy-loads ~20 ads initially. To load more:

```javascript
window.scrollTo(0, document.body.scrollHeight);
// Wait 2-3 seconds, then re-run extraction (dedup handles overlap)
```

Repeat until no new URLs appear.

## Filtering Tips

- Use `active_status=active` for current competitive intel
- Use `active_status=all` for creative evolution study
- Use `media_type=image_and_meme` for image-only swipe files
