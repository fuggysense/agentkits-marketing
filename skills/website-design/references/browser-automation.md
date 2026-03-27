## Graph Links
- **Parent skill:** [[website-design]]
- **Sibling references:** [[aesthetic-guidelines]], [[cinematic-presets]], [[component-sources]], [[gallery-sources]], [[scroll-driven-design]]
- **Related skills:** [[page-cro]], [[brand-building]]

# Browser Automation Reference

## Playwright Stealth Setup

All browser automation uses `playwright` with stealth techniques to avoid bot detection.

### Core Pattern
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        viewport={"width": 1440, "height": 900},
        user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        device_scale_factor=2,
    )
    page = context.new_page()
    page.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
        window.chrome = { runtime: {} };
    """)
```

### Auto-Install Chromium
```bash
python3 -m playwright install chromium
```
The `browser-tools.py` script handles this automatically on first run.

---

## Extract Functions (HTML, CSS, JS)

### Full Page Extraction
```bash
python3 scripts/browser-tools.py extract https://example.com /tmp/extracted
```

Outputs to the directory:
- `page.html` — full rendered HTML
- `styles.css` — all inline + linked CSS rules (cross-origin noted but unreadable)
- `scripts.js` — all inline JS + external script URLs listed
- `computed-styles.json` — computed styles for key elements (body, h1-h3, p, a, button, nav, header, footer, section)
- `screenshot.png` — full-page screenshot

### Mobile Extraction
```bash
python3 scripts/browser-tools.py extract https://example.com /tmp/extracted-mobile --mobile
```

---

## Screenshot Functions

### Desktop Full-Page
```bash
python3 scripts/browser-tools.py screenshot https://example.com /tmp/output.png --full-page
```

### Mobile Screenshot
```bash
python3 scripts/browser-tools.py screenshot https://example.com /tmp/mobile.png --mobile --full-page
```

### Custom Width
```bash
python3 scripts/browser-tools.py screenshot https://example.com /tmp/tablet.png --width 768 --full-page
```

### Local Build Screenshot
```bash
# Start local server first
python3 scripts/browser-tools.py serve ./build --port 8765
# Then screenshot
python3 scripts/browser-tools.py screenshot http://127.0.0.1:8765 /tmp/build.png --full-page
```

---

## Image Size Management

Claude vision has a practical limit of ~5MB per image. The script auto-resizes:

1. First pass: reduce JPEG quality (85 → 75 → 65...)
2. If still >5MB: scale down dimensions proportionally
3. Target: under 5MB while maintaining readable detail

Manual resize with Pillow:
```python
from PIL import Image
img = Image.open("large.png")
img = img.resize((1440, int(img.height * 1440 / img.width)), Image.LANCZOS)
img.save("resized.png", quality=80)
```

---

## Gallery-Specific CSS Selectors

| Gallery | Item Selector | Strengths |
|---------|---------------|-----------|
| godly.website | `a[href*='/website/']` | Modern SaaS, curated |
| landingfolio.com | `.inspiration-card, a[href*='/inspiration/']` | Landing pages specifically |
| lapa.ninja | `.grid-item a, a[href*='/post/']` | Volume, variety |
| onepagelove.com | `.post-entry a` | Single-page designs |

### Scrolling for Lazy-Loaded Content
Most galleries lazy-load images. The script scrolls 3 times before extracting:
```python
for _ in range(3):
    page.evaluate("window.scrollBy(0, window.innerHeight)")
    page.wait_for_timeout(1000)
```

---

## Cookie/Popup Dismissal

The script auto-dismisses common overlays before screenshotting:
```python
dismiss_selectors = [
    "button:has-text('Accept')",
    "button:has-text('Got it')",
    "button:has-text('Close')",
    "[aria-label='Close']",
    ".cookie-banner button",
]
```

---

## Local Server Pattern

For screenshotting local HTML builds:

1. `python3 scripts/browser-tools.py serve ./build` → starts on port 8765
2. Returns PID for cleanup
3. Screenshot from `http://127.0.0.1:8765`
4. Kill with `kill <PID>` when done

**Why a server?** Playwright handles `http://` URLs better than `file://` — proper font loading, relative paths, CORS for JS modules.

---

## Comparison Images

```bash
python3 scripts/browser-tools.py compare reference.png build.png comparison.png
```

Output: side-by-side image labeled "Reference" (white) and "Build" (green), on dark background. Heights normalized. Auto-resized to <5MB.

---

## Design Analysis (Gemini Vision)

Sends a screenshot to Gemini for structured design token extraction. Returns JSON with colors, typography, layout, sections, and style.

### Full Analysis (default)
```bash
python3 scripts/browser-tools.py design-analyze /tmp/inspiration.png
```
Returns complete design tokens: colors, typography, layout, style, and per-section detail.

### Focused Analysis
```bash
# Colors only
python3 scripts/browser-tools.py design-analyze /tmp/inspiration.png --focus colors

# Layout structure only
python3 scripts/browser-tools.py design-analyze /tmp/inspiration.png --focus layout

# Typography only
python3 scripts/browser-tools.py design-analyze /tmp/inspiration.png --focus typography

# Section-by-section breakdown
python3 scripts/browser-tools.py design-analyze /tmp/inspiration.png --focus sections
```

### Custom Model
```bash
python3 scripts/browser-tools.py design-analyze /tmp/inspiration.png --model gemini-2.5-pro
```

### Typical Workflow (Phase A2)
```bash
# 1. Screenshot the inspiration site
python3 scripts/browser-tools.py screenshot https://example.com /tmp/inspo.png --full-page

# 2. Extract design tokens with Gemini
python3 scripts/browser-tools.py design-analyze /tmp/inspo.png

# 3. Use the returned JSON to write design-rules.md
```

### API Key Setup
Requires `GEMINI_API_KEY`. Uses the same 5-step lookup as other Gemini skills (env var → project .env → .claude/.env → .claude/skills/.env → skill .env).

Get a key at: https://aistudio.google.com/apikey

### Fallback Behavior
If no API key is configured, returns:
```json
{"error": "GEMINI_API_KEY not configured", "fallback": "manual", "setup": "..."}
```
Exit code is still 0 — Claude falls back to analyzing the screenshot visually itself.

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `chromium not found` | Run: `python3 -m playwright install chromium` |
| Bot detection / blank page | Script uses stealth by default; try `--width 1280` |
| Image too large | Auto-handled; if still big, use `--width 1024` |
| Gallery returns 0 results | Site may have changed DOM; falls back to generic scraper |
| Server port in use | Use `--port 8766` or kill existing process |
| Cookie banner blocking content | Auto-dismissed; if persistent, screenshot will include it |

### Fallback Chain
If `browser-tools.py` fails for any reason:
1. **Firecrawl MCP** — `mcp__firecrawl__scrape` or `mcp__firecrawl__screenshot`
2. **WebFetch** — built-in tool for HTML content
3. **crawl4ai** — Python package at `/Library/Frameworks/Python.framework/Versions/3.14/lib/python3.14/site-packages/crawl4ai/`

Claude should try the next fallback automatically without asking the user.
