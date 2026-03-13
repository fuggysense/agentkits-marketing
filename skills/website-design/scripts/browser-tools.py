#!/usr/bin/env python3
"""
browser-tools.py — Autonomous browser automation for website-design skill v2.0

Subcommands:
  screenshot <url> <output_path> [--width N] [--full-page] [--mobile]
  gallery <gallery_url> [--limit N] [--category CAT]
  compare <reference> <build> <output>
  serve <html_dir> [--port N]
  browse-components <category> [--source 21st]
  design-analyze <screenshot> [--output json|markdown] [--focus full|layout|colors|typography|sections] [--model MODEL]

All commands return JSON to stdout. Exit code 0 = success, 1 = error.
"""

import argparse
import json
import sys
import os
import subprocess
import signal
import http.server
import threading
import time
from pathlib import Path

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def emit(data):
    """Print JSON to stdout and exit 0."""
    print(json.dumps(data, indent=2))
    sys.exit(0)

def fail(msg):
    """Print error JSON to stdout and exit 1."""
    print(json.dumps({"error": str(msg)}))
    sys.exit(1)

def ensure_playwright():
    """Install Chromium if not already installed."""
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            # Check if chromium is available
            try:
                browser = p.chromium.launch(headless=True)
                browser.close()
            except Exception:
                print("Installing Chromium...", file=sys.stderr)
                subprocess.run(
                    [sys.executable, "-m", "playwright", "install", "chromium"],
                    check=True, capture_output=True
                )
    except ImportError:
        fail("playwright not installed. Run: pip install playwright")

def resize_image(path, max_bytes=5 * 1024 * 1024):
    """Resize image if larger than max_bytes (~5MB for Claude vision)."""
    from PIL import Image
    file_size = os.path.getsize(path)
    if file_size <= max_bytes:
        return
    img = Image.open(path)
    quality = 85
    while file_size > max_bytes and quality > 20:
        quality -= 10
        img.save(path, optimize=True, quality=quality)
        file_size = os.path.getsize(path)
    # If still too large, scale down
    if file_size > max_bytes:
        scale = (max_bytes / file_size) ** 0.5
        new_w = int(img.width * scale)
        new_h = int(img.height * scale)
        img = img.resize((new_w, new_h), Image.LANCZOS)
        img.save(path, optimize=True, quality=75)

# ---------------------------------------------------------------------------
# screenshot
# ---------------------------------------------------------------------------

def cmd_screenshot(args):
    ensure_playwright()
    from playwright.sync_api import sync_playwright

    url = args.url
    output = args.output
    width = args.width or 1440
    mobile = args.mobile

    if mobile:
        width = 390  # iPhone 14 Pro

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": width, "height": 900},
            user_agent=(
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            device_scale_factor=2 if not mobile else 3,
        )
        page = context.new_page()

        # Stealth: remove webdriver flag
        page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            window.chrome = { runtime: {} };
        """)

        try:
            page.goto(url, wait_until="networkidle", timeout=30000)
        except Exception:
            # Fallback: just wait for load
            try:
                page.goto(url, wait_until="load", timeout=30000)
            except Exception as e:
                browser.close()
                fail(f"Failed to load {url}: {e}")

        # Wait for images/fonts
        page.wait_for_timeout(2000)

        # Dismiss common popups/cookie banners
        for selector in [
            "button:has-text('Accept')", "button:has-text('Got it')",
            "button:has-text('Close')", "[aria-label='Close']",
            "button:has-text('Dismiss')", ".cookie-banner button",
        ]:
            try:
                el = page.query_selector(selector)
                if el and el.is_visible():
                    el.click()
                    page.wait_for_timeout(500)
            except Exception:
                pass

        # Take screenshot
        os.makedirs(os.path.dirname(os.path.abspath(output)), exist_ok=True)
        page.screenshot(path=output, full_page=args.full_page)
        browser.close()

    resize_image(output)
    size_kb = os.path.getsize(output) / 1024
    emit({
        "status": "ok",
        "path": os.path.abspath(output),
        "width": width,
        "mobile": mobile,
        "full_page": args.full_page,
        "size_kb": round(size_kb, 1),
    })

# ---------------------------------------------------------------------------
# gallery
# ---------------------------------------------------------------------------

GALLERY_SCRAPERS = {
    "godly.website": {
        "item_selector": "a[href*='/website/']",
        "title_selector": "h3, span, p",
        "img_selector": "img",
        "base_url": "https://godly.website",
    },
    "landingfolio.com": {
        "item_selector": ".inspiration-card, a[href*='/inspiration/']",
        "title_selector": "h3, .card-title, span",
        "img_selector": "img",
        "base_url": "https://www.landingfolio.com",
    },
    "lapa.ninja": {
        "item_selector": ".grid-item a, a[href*='/post/']",
        "title_selector": "h3, .title, span",
        "img_selector": "img",
        "base_url": "https://www.lapa.ninja",
    },
    "onepagelove.com": {
        "item_selector": ".post-entry a, a[href*='/one-page-website/']",
        "title_selector": "h2, .entry-title, span",
        "img_selector": "img",
        "base_url": "https://onepagelove.com",
    },
}

def detect_gallery(url):
    for key in GALLERY_SCRAPERS:
        if key in url:
            return key
    return None

def cmd_gallery(args):
    ensure_playwright()
    from playwright.sync_api import sync_playwright
    from urllib.parse import urljoin

    url = args.url
    limit = args.limit or 20
    gallery_key = detect_gallery(url)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1440, "height": 900},
            user_agent=(
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
        )
        page = context.new_page()
        page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
        """)

        try:
            page.goto(url, wait_until="networkidle", timeout=30000)
        except Exception:
            try:
                page.goto(url, wait_until="load", timeout=30000)
            except Exception as e:
                browser.close()
                fail(f"Failed to load gallery {url}: {e}")

        page.wait_for_timeout(3000)

        # Scroll to load lazy content
        for _ in range(3):
            page.evaluate("window.scrollBy(0, window.innerHeight)")
            page.wait_for_timeout(1000)
        page.evaluate("window.scrollTo(0, 0)")
        page.wait_for_timeout(500)

        results = []

        if gallery_key and gallery_key in GALLERY_SCRAPERS:
            config = GALLERY_SCRAPERS[gallery_key]
            items = page.query_selector_all(config["item_selector"])
            for item in items[:limit]:
                try:
                    title_el = item.query_selector(config["title_selector"])
                    img_el = item.query_selector(config["img_selector"])
                    href = item.get_attribute("href") or ""
                    title = title_el.inner_text().strip() if title_el else ""
                    thumbnail = ""
                    if img_el:
                        thumbnail = img_el.get_attribute("src") or img_el.get_attribute("data-src") or ""
                    if href and not href.startswith("http"):
                        href = urljoin(config["base_url"], href)
                    if thumbnail and not thumbnail.startswith("http"):
                        thumbnail = urljoin(config["base_url"], thumbnail)
                    if href:
                        results.append({
                            "title": title[:100],
                            "url": href,
                            "thumbnail_url": thumbnail,
                            "category": args.category or "",
                        })
                except Exception:
                    continue
        else:
            # Generic scraper: find all links with images
            links = page.query_selector_all("a")
            for link in links[:limit * 2]:
                try:
                    href = link.get_attribute("href") or ""
                    img = link.query_selector("img")
                    title_el = link.query_selector("h2, h3, h4, span, p")
                    if not href or href in ("#", "/"):
                        continue
                    title = title_el.inner_text().strip() if title_el else ""
                    thumbnail = ""
                    if img:
                        thumbnail = img.get_attribute("src") or img.get_attribute("data-src") or ""
                    if not href.startswith("http"):
                        href = urljoin(url, href)
                    if thumbnail and not thumbnail.startswith("http"):
                        thumbnail = urljoin(url, thumbnail)
                    results.append({
                        "title": title[:100],
                        "url": href,
                        "thumbnail_url": thumbnail,
                        "category": args.category or "",
                    })
                except Exception:
                    continue

        browser.close()

    # Deduplicate by URL
    seen = set()
    unique = []
    for r in results:
        if r["url"] not in seen:
            seen.add(r["url"])
            unique.append(r)

    emit({
        "status": "ok",
        "gallery": gallery_key or "generic",
        "count": len(unique[:limit]),
        "results": unique[:limit],
    })

# ---------------------------------------------------------------------------
# compare
# ---------------------------------------------------------------------------

def cmd_compare(args):
    from PIL import Image, ImageDraw, ImageFont

    ref = Image.open(args.reference)
    build = Image.open(args.build)

    # Normalize heights
    target_h = max(ref.height, build.height)
    if ref.height != target_h:
        scale = target_h / ref.height
        ref = ref.resize((int(ref.width * scale), target_h), Image.LANCZOS)
    if build.height != target_h:
        scale = target_h / build.height
        build = build.resize((int(build.width * scale), target_h), Image.LANCZOS)

    label_h = 40
    gap = 20
    total_w = ref.width + gap + build.width
    total_h = target_h + label_h

    canvas = Image.new("RGB", (total_w, total_h), (30, 30, 30))

    # Draw labels
    draw = ImageDraw.Draw(canvas)
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 24)
    except Exception:
        font = ImageFont.load_default()

    draw.text((ref.width // 2 - 50, 8), "Reference", fill=(255, 255, 255), font=font)
    draw.text((ref.width + gap + build.width // 2 - 30, 8), "Build", fill=(100, 255, 100), font=font)

    # Paste images
    canvas.paste(ref, (0, label_h))
    canvas.paste(build, (ref.width + gap, label_h))

    canvas.save(args.output, quality=85)
    resize_image(args.output)

    size_kb = os.path.getsize(args.output) / 1024
    emit({
        "status": "ok",
        "path": os.path.abspath(args.output),
        "reference_size": f"{ref.width}x{ref.height}",
        "build_size": f"{build.width}x{build.height}",
        "size_kb": round(size_kb, 1),
    })

# ---------------------------------------------------------------------------
# serve
# ---------------------------------------------------------------------------

def cmd_serve(args):
    html_dir = os.path.abspath(args.html_dir)
    port = args.port or 8765

    if not os.path.isdir(html_dir):
        fail(f"Directory not found: {html_dir}")

    # Fork a background process
    pid = os.fork()
    if pid == 0:
        # Child process — run server
        os.chdir(html_dir)
        handler = http.server.SimpleHTTPRequestHandler
        with http.server.HTTPServer(("127.0.0.1", port), handler) as httpd:
            httpd.serve_forever()
    else:
        # Parent — wait briefly to confirm server started
        time.sleep(1)
        # Check if child is alive
        try:
            os.kill(pid, 0)
        except OSError:
            fail("Server process died immediately")

        emit({
            "status": "ok",
            "pid": pid,
            "port": port,
            "url": f"http://127.0.0.1:{port}",
            "directory": html_dir,
            "stop": f"kill {pid}",
        })

# ---------------------------------------------------------------------------
# browse-components
# ---------------------------------------------------------------------------

def cmd_browse_components(args):
    ensure_playwright()
    from playwright.sync_api import sync_playwright

    category = args.category or "all"
    source = args.source or "21st"

    if source == "21st":
        url = "https://21st.dev"
        if category != "all":
            url = f"https://21st.dev/components/{category}"
    else:
        fail(f"Unknown component source: {source}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1440, "height": 900},
            user_agent=(
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
        )
        page = context.new_page()
        page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
        """)

        try:
            page.goto(url, wait_until="networkidle", timeout=30000)
        except Exception:
            try:
                page.goto(url, wait_until="load", timeout=30000)
            except Exception as e:
                browser.close()
                fail(f"Failed to load {url}: {e}")

        page.wait_for_timeout(3000)

        # Scroll to load content
        for _ in range(3):
            page.evaluate("window.scrollBy(0, window.innerHeight)")
            page.wait_for_timeout(1000)

        # Extract components — 21st.dev uses cards with component names
        components = []
        # Try multiple selectors for 21st.dev's layout
        selectors = [
            "a[href*='/component/']",
            "a[href*='/components/']",
            ".component-card a",
            "[data-component] a",
            "a[href*='21st.dev']",
        ]

        for sel in selectors:
            items = page.query_selector_all(sel)
            if items:
                for item in items[:50]:
                    try:
                        href = item.get_attribute("href") or ""
                        text = item.inner_text().strip()
                        if href and text and len(text) < 200:
                            name = text.split("\n")[0].strip()
                            if name and len(name) > 1:
                                components.append({
                                    "name": name[:100],
                                    "url": href if href.startswith("http") else f"https://21st.dev{href}",
                                    "install": f"npx 21st@latest add {name.lower().replace(' ', '-')}",
                                })
                    except Exception:
                        continue
                if components:
                    break

        # Deduplicate
        seen = set()
        unique = []
        for c in components:
            if c["name"] not in seen:
                seen.add(c["name"])
                unique.append(c)

        browser.close()

    emit({
        "status": "ok",
        "source": source,
        "category": category,
        "count": len(unique),
        "components": unique,
    })

# ---------------------------------------------------------------------------
# design-analyze
# ---------------------------------------------------------------------------

DESIGN_ANALYSIS_PROMPTS = {
    "full": """Analyze this website screenshot and extract ALL design tokens as structured JSON.

Return ONLY valid JSON (no markdown fences, no explanation) with this exact structure:
{
  "colors": {
    "primary": "#hex",
    "secondary": "#hex",
    "accent": "#hex",
    "background": "#hex",
    "text": "#hex",
    "muted": "#hex"
  },
  "typography": {
    "heading_font": "Font Name (best guess from visual style)",
    "body_font": "Font Name (best guess)",
    "heading_sizes": ["text-5xl", "text-3xl", "text-xl"],
    "body_size": "text-base"
  },
  "layout": {
    "max_width": "max-w-7xl or similar Tailwind class",
    "sections": ["navbar", "hero", ...list all sections in order],
    "grid_pattern": "description of grid/column usage",
    "spacing_system": "8px | 4px | custom"
  },
  "style": {
    "border_radius": "rounded-none | rounded-lg | rounded-2xl",
    "shadow_style": "none | subtle | dramatic",
    "animation_style": "none | fade | slide | parallax",
    "overall_vibe": "2-3 word description"
  },
  "sections_detail": [
    {
      "name": "section name",
      "layout_description": "brief layout description",
      "suggested_component": "21st.dev component type or custom",
      "key_elements": ["element1", "element2"]
    }
  ]
}

Be precise with hex colors — sample actual colors from the screenshot.
Use Tailwind CSS equivalents for sizes, spacing, and border radius.
List ALL visible sections in order from top to bottom.""",

    "colors": """Analyze this website screenshot and extract the color palette.

Return ONLY valid JSON (no markdown fences):
{
  "colors": {
    "primary": "#hex",
    "secondary": "#hex",
    "accent": "#hex",
    "background": "#hex",
    "text": "#hex",
    "muted": "#hex",
    "additional": ["#hex", "#hex"]
  },
  "color_notes": "brief description of color usage patterns"
}

Be precise — sample actual colors visible in the screenshot.""",

    "typography": """Analyze this website screenshot and extract typography details.

Return ONLY valid JSON (no markdown fences):
{
  "typography": {
    "heading_font": "Font Name (best guess from visual style — suggest closest Google Font)",
    "body_font": "Font Name (best guess — suggest closest Google Font)",
    "heading_sizes": ["text-5xl", "text-3xl", "text-xl"],
    "body_size": "text-base or text-lg",
    "font_weights": {"heading": "font-bold or font-semibold", "body": "font-normal or font-light"},
    "line_height": "leading-tight | leading-normal | leading-relaxed",
    "letter_spacing": "tracking-tight | tracking-normal | tracking-wide"
  },
  "typography_notes": "brief description of typographic style"
}""",

    "layout": """Analyze this website screenshot and extract layout structure.

Return ONLY valid JSON (no markdown fences):
{
  "layout": {
    "max_width": "max-w-7xl or similar Tailwind class",
    "sections": ["list all sections top to bottom"],
    "grid_pattern": "description of grid/column usage",
    "spacing_system": "8px | 4px | custom",
    "container_padding": "px-4 | px-6 | px-8",
    "section_spacing": "py-16 | py-20 | py-24"
  },
  "layout_notes": "brief description of overall layout approach"
}""",

    "sections": """Analyze this website screenshot and describe each section in detail.

Return ONLY valid JSON (no markdown fences):
{
  "sections_detail": [
    {
      "name": "section name (e.g. hero, features, pricing)",
      "layout_description": "detailed layout description",
      "suggested_component": "21st.dev component type or custom build",
      "key_elements": ["element1", "element2", "element3"],
      "background": "bg color or gradient description",
      "estimated_height": "h-screen | h-auto | specific estimate"
    }
  ]
}

List ALL visible sections from top to bottom.""",
}


def cmd_design_analyze(args):
    """Send screenshot to Gemini for structured design analysis."""
    import base64

    screenshot_path = args.screenshot
    if not os.path.exists(screenshot_path):
        fail(f"Screenshot not found: {screenshot_path}")

    # Find API key using existing helper
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "common"))
    from api_key_helper import find_api_key

    skill_dir = Path(__file__).resolve().parent.parent
    api_key = find_api_key(skill_dir)
    if not api_key:
        # Graceful fallback — don't crash, let Claude do manual analysis
        print(json.dumps({
            "error": "GEMINI_API_KEY not configured",
            "fallback": "manual",
            "setup": "Add GEMINI_API_KEY to .env — get key at https://aistudio.google.com/apikey"
        }, indent=2))
        sys.exit(0)  # Exit 0 so Claude can fall back gracefully

    # Read and encode the image
    with open(screenshot_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode()

    # Determine mime type
    ext = Path(screenshot_path).suffix.lower()
    mime_map = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp"}
    mime_type = mime_map.get(ext, "image/png")

    # Select prompt based on --focus
    focus = args.focus or "full"
    prompt = DESIGN_ANALYSIS_PROMPTS.get(focus, DESIGN_ANALYSIS_PROMPTS["full"])

    # Call Gemini
    try:
        from google import genai
    except ImportError:
        fail("google-genai SDK not installed. Run: pip install google-genai")

    model_name = args.model or "gemini-2.5-flash"
    client = genai.Client(api_key=api_key)

    try:
        response = client.models.generate_content(
            model=model_name,
            contents=[
                {
                    "parts": [
                        {"inline_data": {"mime_type": mime_type, "data": image_data}},
                        {"text": prompt},
                    ]
                }
            ],
        )
    except Exception as e:
        fail(f"Gemini API error: {e}")

    # Extract text from response
    raw_text = response.text.strip()

    # Strip markdown code fences if present
    if raw_text.startswith("```"):
        lines = raw_text.split("\n")
        # Remove first line (```json or ```) and last line (```)
        lines = [l for l in lines if not l.strip().startswith("```")]
        raw_text = "\n".join(lines).strip()

    # Try to parse as JSON
    output_format = args.output_format or "json"
    try:
        parsed = json.loads(raw_text)
        if output_format == "json":
            emit({
                "status": "ok",
                "model": model_name,
                "focus": focus,
                "screenshot": os.path.abspath(screenshot_path),
                "design_tokens": parsed,
            })
        else:
            # Markdown output — emit JSON with a markdown summary
            emit({
                "status": "ok",
                "model": model_name,
                "focus": focus,
                "screenshot": os.path.abspath(screenshot_path),
                "design_tokens": parsed,
                "markdown": raw_text,
            })
    except json.JSONDecodeError:
        # Return raw text if Gemini didn't return valid JSON
        emit({
            "status": "ok",
            "model": model_name,
            "focus": focus,
            "screenshot": os.path.abspath(screenshot_path),
            "raw_analysis": raw_text,
            "parse_warning": "Response was not valid JSON — raw text included",
        })


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Browser automation tools for website-design skill")
    sub = parser.add_subparsers(dest="command")

    # screenshot
    p_ss = sub.add_parser("screenshot", help="Take a screenshot of a URL")
    p_ss.add_argument("url", help="URL to screenshot")
    p_ss.add_argument("output", help="Output file path (PNG)")
    p_ss.add_argument("--width", type=int, default=1440, help="Viewport width (default 1440)")
    p_ss.add_argument("--full-page", action="store_true", help="Capture full page")
    p_ss.add_argument("--mobile", action="store_true", help="Use mobile viewport (390px)")

    # gallery
    p_gal = sub.add_parser("gallery", help="Scrape a design gallery")
    p_gal.add_argument("url", help="Gallery URL")
    p_gal.add_argument("--limit", type=int, default=20, help="Max results")
    p_gal.add_argument("--category", help="Filter by category")

    # compare
    p_cmp = sub.add_parser("compare", help="Side-by-side comparison image")
    p_cmp.add_argument("reference", help="Reference screenshot path")
    p_cmp.add_argument("build", help="Build screenshot path")
    p_cmp.add_argument("output", help="Output comparison image path")

    # serve
    p_srv = sub.add_parser("serve", help="Local HTTP server for build screenshots")
    p_srv.add_argument("html_dir", help="Directory to serve")
    p_srv.add_argument("--port", type=int, default=8765, help="Port (default 8765)")

    # browse-components
    p_bc = sub.add_parser("browse-components", help="Browse component library")
    p_bc.add_argument("category", nargs="?", default="all", help="Component category")
    p_bc.add_argument("--source", default="21st", help="Source: 21st (default)")

    # design-analyze
    p_da = sub.add_parser("design-analyze", help="Analyze screenshot with Gemini vision")
    p_da.add_argument("screenshot", help="Path to screenshot (PNG/JPG)")
    p_da.add_argument("--output", dest="output_format", choices=["json", "markdown"], default="json", help="Output format (default: json)")
    p_da.add_argument("--focus", choices=["full", "layout", "colors", "typography", "sections"], default="full", help="Analysis focus (default: full)")
    p_da.add_argument("--model", default=None, help="Gemini model (default: gemini-2.5-flash)")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        if args.command == "screenshot":
            cmd_screenshot(args)
        elif args.command == "gallery":
            cmd_gallery(args)
        elif args.command == "compare":
            cmd_compare(args)
        elif args.command == "serve":
            cmd_serve(args)
        elif args.command == "browse-components":
            cmd_browse_components(args)
        elif args.command == "design-analyze":
            cmd_design_analyze(args)
    except Exception as e:
        fail(str(e))

if __name__ == "__main__":
    main()
