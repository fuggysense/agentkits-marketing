## Graph Links
- **Parent skill:** [[image-generation]]
- **Sibling references:** [[nano-banana-examples]]
- **Related skills:** [[video-director]], [[tiktok-slideshows]]

# Nano Banana 2 — Complete Image Generation Guide

> Source: AI Topia / fearless-offer-231.notion.site
> Model: gemini-3.1-flash-image-preview (Google DeepMind)
> Cost: ~$0.07/image | Resolution: up to 4K native | 14 aspect ratios

## Model Capabilities

| Capability | What It Means |
|---|---|
| Native 4K | Real 4096x4096, not upscaled |
| Text rendering | Character-validated, legible labels/headlines |
| Subject consistency | Same character across 5+ images |
| Mask-free editing | "Change background to kitchen" — no Photoshop needed |
| Web grounding | Pulls from Google Search for real landmarks/products |
| Thinking mode | Reasons about complex prompts before generating |
| JSON prompting | 92% precision vs 68% plain text |

## Comparison

| | Nano Banana 2 | Midjourney v7 | DALL-E 3 | Flux 2 Pro |
|---|---|---|---|---|
| Text on images | Excellent | Poor (~71%) | Good | Very Good |
| Max resolution | 4K native | 2K | 1K | 2K |
| JSON prompting | Native | No | No | No |
| Edit existing | Mask-free | Region variation | Inpainting | Kontext |
| Cost/image | ~$0.07 | ~$0.02-0.10 | ChatGPT sub | Varies |
| Best at | Precision + control | Artistic style | Accessibility | Photorealism |

## Access Points

| Provider | Model ID | Cost (1K) |
|---|---|---|
| Google AI Studio | gemini-3.1-flash-image-preview | ~$0.067 |
| fal.ai | fal-ai/nano-banana-2 | ~$0.08 |
| OpenRouter | google/gemini-3.1-flash-image-preview | ~$0.07 |

## Why JSON > Plain Text

| Metric | Plain Text | JSON |
|---|---|---|
| Color accuracy | 68% | 92% |
| Composition precision | ~70% | ~92% |
| Batch processing | Standard | 40% faster |
| Prompt reusability | Low | High (swap one field) |
| Brand consistency | Inconsistent | Locked in |

---

## Complete JSON Schema

```json
{
  "meta": {
    "aspect_ratio": "4:5",
    "resolution": "2K",
    "quality_mode": "high",
    "thinking_level": "high",
    "seed": 42,
    "guidance_scale": 7.5,
    "web_grounding": true
  },
  "subject": [{
    "type": "person | product | object | environment",
    "appearance": {},
    "clothing": [],
    "accessories": [],
    "action": "",
    "position": ""
  }],
  "scene": {
    "location": "",
    "details": "",
    "time_of_day": "",
    "lighting": {
      "type": "",
      "direction": "",
      "quality": "",
      "secondary": ""
    },
    "background_blur": ""
  },
  "camera": {
    "model": "",
    "lens": "",
    "aperture": "",
    "angle": "",
    "framing": "",
    "depth_of_field": "",
    "focus": "",
    "film_stock": ""
  },
  "style": {
    "aesthetic": "",
    "color_grading": "",
    "mood": "",
    "post_processing": ""
  },
  "text_rendering": {
    "elements": [{
      "text": "",
      "placement": "",
      "font_style": "",
      "color": "",
      "size": ""
    }]
  },
  "negative_prompt": ""
}
```

### Meta Settings

| Field | Options | When to Use |
|---|---|---|
| aspect_ratio | 1:1, 4:5, 9:16, 16:9, 21:9, 3:2, 2:3, 3:4, 4:3 | Always set. Match platform. |
| resolution | 1K, 2K, 4K | 1K drafts, 2K production, 4K print |
| thinking_level | minimal, high | high for complex multi-element, minimal for simple |
| seed | Any integer | Lock to reproduce same composition |
| guidance_scale | 1.0-20.0 | 7-8 ideal. Higher = stricter adherence |
| web_grounding | true/false | Real landmarks, logos, products |

### Lens Quick Reference

| Lens | Character | Best For |
|---|---|---|
| 16-24mm | Wide, dramatic, edge distortion | Interiors, establishing shots |
| 35mm | Environmental, natural | UGC selfies, lifestyle |
| 50mm | Neutral, "what eye sees" | General purpose |
| 85mm | Portrait compression, beautiful bokeh | Headshots, beauty |
| 105mm | Tight detail, macro | Texture, labels, ingredients |
| 200mm | Extreme compression, isolation | Product floating on blurred bg |

### Camera Angle Reference

| Angle | Effect | Use Case |
|---|---|---|
| Eye-level | Neutral, relatable | Portraits, UGC, most shots |
| Low-angle | Power, authority | Leadership, product hero |
| High-angle | Approachable, overview | Flat lays, desk, food |
| Overhead | Clean, organized | Product arrangements |
| Dutch angle | Dynamic, edgy | Creative/editorial only |

### Style Presets

| Style | Best For |
|---|---|
| ugc-selfie | Social proof, DTC, relatable |
| lifestyle-in-context | Instagram, lifestyle brands |
| studio-product-hero | Catalog, e-commerce, hero |
| flat-lay | Carousel slides, ingredients |
| editorial-beauty | Premium/luxury |
| editorial-lifestyle | LinkedIn, brand photography |
| unboxing-moment | DTC subscription, reveals |
| documentary | Behind-the-scenes, authenticity |
| cinematic | Video thumbnails, hero banners |
| minimalist | Text-heavy, quotes |
| before-after | Testimonials, transformations |
| clean-bold-cover | Carousel covers, social hooks |

### Lighting Reference

| Lighting | Best For |
|---|---|
| Ring light | UGC selfies, beauty |
| Natural window | Lifestyle, product-in-context |
| Golden hour | Outdoor lifestyle, aspirational |
| Studio softbox | Product hero, headshots |
| Dramatic rim | Premium/editorial, authority |
| Overhead natural | Flat lays, food |
| Neon/colored | Creative, night scenes |

### Color Grading Reference

| Grading | Feel | Brands |
|---|---|---|
| Warm | Inviting, personal | Lifestyle, wellness, food |
| Cool | Professional, tech | SaaS, finance, healthcare |
| Neutral | Balanced | Corporate, any |
| Muted | Sophisticated | Premium, fashion |
| Vibrant | Energetic, bold | DTC, fitness |
| Cinematic | Dramatic | Media, high-end |

### Default Negative Prompt

```
blurry, low quality, distorted, extra fingers, extra limbs, watermark, cartoon, illustration, anime, 3d render, oversaturated, plastic skin, airbrushed, stock photo feel, generic, cluttered
```

Add context-specific:
- **People:** cross-eyed, deformed face, bad anatomy, unnatural pose
- **Products:** wrong proportions, floating objects, misspelled text
- **UGC style:** studio lighting, overly polished, professional model
- **Minimalist:** busy background, too many elements

---

## Platform Dimensions

| Platform | Format | Ratio | Size |
|---|---|---|---|
| Instagram Feed | Post | 4:5 | 1080x1350 |
| Instagram Stories | Story | 9:16 | 1080x1920 |
| Instagram Carousel | Slide | 1:1 | 1080x1080 |
| Facebook Feed | Post | 4:5 | 1080x1350 |
| Facebook Cover | Banner | 16:9 | 1640x924 |
| LinkedIn Feed | Post | 1:1/4:5 | 1080x1080/1350 |
| LinkedIn Banner | Banner | 4:1 | 1584x396 |
| Twitter/X | Post | 16:9 | 1200x675 |
| YouTube Thumb | Thumb | 16:9 | 1280x720 |
| Email Header | Banner | 3:1 | 600x200 |
| Pinterest | Pin | 2:3 | 1000x1500 |

## Cost Calculator

| Need | Res | Cost |
|---|---|---|
| 10 social posts | 1K | $0.67 |
| 50 ad creatives | 2K | $5.05 |
| 100 product shots | 2K | $10.10 |
| 500 brand library | Mixed | $35-50 |

---

## Generation Script (Python)

Supports key rotation for batch generation. Set `GEMINI_API_KEY`, `GEMINI_API_KEY_2`, `GEMINI_API_KEY_3` in `.env` for 3x throughput.

```python
import json, sys, os, requests, base64
from datetime import datetime

def get_api_keys():
    """Load all available Gemini API keys for round-robin rotation."""
    keys = [os.environ.get("GEMINI_API_KEY")]
    for i in range(2, 10):
        k = os.environ.get(f"GEMINI_API_KEY_{i}")
        if k:
            keys.append(k)
    return [k for k in keys if k]

def generate(prompt_path, output_dir="images", index=0):
    keys = get_api_keys()
    key = keys[index % len(keys)]
    with open(prompt_path) as f:
        data = json.load(f)
    prompt_text = json.dumps(data, indent=2)
    response = requests.post(
        "https://generativelanguage.googleapis.com/v1beta/models/"
        "gemini-3.1-flash-image-preview:generateContent",
        params={"key": key},
        json={
            "contents": [{"parts": [{"text": prompt_text}]}],
            "generationConfig": {
                "responseModalities": ["TEXT", "IMAGE"],
                "imageConfig": {
                    "aspectRatio": data.get("meta", {}).get("aspect_ratio", "1:1"),
                    "imageSize": data.get("meta", {}).get("resolution", "1K")
                }
            }
        }
    )
    result = response.json()
    for part in result["candidates"][0]["content"]["parts"]:
        if "inlineData" in part:
            img_data = base64.b64decode(part["inlineData"]["data"])
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            os.makedirs(output_dir, exist_ok=True)
            path = f"{output_dir}/{ts}.png"
            with open(path, "wb") as f:
                f.write(img_data)
            print(f"Saved: {path} (key {index % len(keys) + 1}/{len(keys)})")
            return path

if __name__ == "__main__":
    generate(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "images")
```

Requires: `GEMINI_API_KEY` env var (+ optional `GEMINI_API_KEY_2`, `GEMINI_API_KEY_3` for rotation), `requests` package.

---

## Advanced Techniques

### Feedback Loop
After every batch, tell Claude what worked/didn't. Claude updates preferences. After a few rounds, it knows your visual style.

### Batch Generation
Plan all campaign assets at once. Lock visual settings, swap only content per image. One session = 13+ consistent assets.

### Seed Locking
`"seed": 42` — same composition, change one variable (product, background). Variations without re-rolling everything.

### Thinking Mode
`"thinking_level": "high"` for multi-element scenes. Model reasons through placement before generating. Use "minimal" for simple shots.

### Web Grounding
`"web_grounding": true` for real locations, products, landmarks. Model searches Google for reference.

---

## Nano Banana Pro Advanced Features

### Style Prompt Saving
Lock a complete style configuration and reuse across batches:
```json
{
  "meta": { "style_preset": "saved:my-brand-style" },
  "subject": [{ "description": "[new subject each time]" }]
}
```
- Save lighting, color grading, lens, angle, and mood as a preset
- Swap only the subject/content per generation
- Ensures brand consistency across 50+ images in a campaign

### Annotation Workflow
After generating an image, annotate it for downstream use:
1. **Mark motion zones** — Circle areas that should move in video (e.g., "steam rises here", "hand enters from right")
2. **Mark static zones** — X areas that should stay fixed (product label, background)
3. **Add notes** — Text labels for video model context ("this is the hero product", "camera pushes in here")

This annotation feeds into the video-director's image-first pipeline: annotated reference images give video models clearer direction about what to animate.

### Seedream 4 Character Alternative
For projects needing extreme character consistency:
- **Seedream 4** generates consistent characters from a single reference image
- Better facial feature preservation than Nano Banana across 10+ images
- Use when building character image libraries for video campaigns or character-based social accounts
- Workflow: Seedream 4 (character images) → Nano Banana (scene/product images) → Video model

---

## 8 Prompt Categories (100+ Templates)

1. **Professional Portraits** (15): LinkedIn Authority, Approachable Founder, Conference Speaker, Creative Professional, Outdoor Authority, Podcast Host, Workshop Facilitator, Remote Worker, Team Leader, Brand Builder + 5 headshot style variations
2. **Product Photography** (15): Clean Hero, Lifestyle-in-Context, Flat Lay, Unboxing, Before/After, Ingredient Showcase, Scale Reference, Texture Close-Up, Product Family, Action Shot
3. **Social Graphics** (20): Bold Statement, Data Card, Carousel Cover, Framework Slide, Testimonial Card, Comparison Chart, Checklist, Process Flow, Quote Over Photo, This vs That, Calendar, Tip of Day, Poll, Cheat Sheet, CTA Slide, Framework Diagram, Myth vs Reality, Timeline, Behind-Scenes, Numbered List
4. **Ad Creative** (15): UGC-Style Product Ad, Hero Banner, Carousel Ad Series, Video Thumbnail, Story/Reel Ad, Social Proof Ad, Comparison Ad, Seasonal Ad, Limited Offer, Bundle Ad
5. **Brand Assets** (15): Email Header, Presentation Title, Blog Hero, Podcast Cover, Event Banner, Lead Magnet Cover, Social Profile Banner, Course Thumbnail, Slide Divider, Thank You
6. **Infographics** (10): Process, Comparison Table, Pie Chart, Timeline, Funnel, Matrix, Dashboard, Flowchart, Bar Chart, Icon Grid
7. **Image Editing** (15): Background Swap, Brand Color Overlay, Profile Polish, Text Addition, Device Mockup, Color Regrade, Object Removal, Style Transfer, Aspect Ratio Change, Seasonal Update, Branded Frame, Before/After Split, Multiple Variations, Watermark, Social Optimization
8. **Advanced** (10): Consistent Character Series, Web-Grounded Location, Multi-Product Story, Seasonal Campaign Set, A/B Test Variants, Platform Adaptation, Mood Board to Image, Abstract Brand, Neon Sign, Magazine Cover

See `nano-banana-examples.md` for the 5 detailed starter templates with full JSON.