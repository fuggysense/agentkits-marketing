# ScrapeCreators Integration Patterns

> How each consuming skill should use the scrapecreators skill.

---

## Skill Integration Map

| Consuming Skill | Use Case | Method |
|-----------------|----------|--------|
| **tiktok-slideshows** | Competitor hook scraping, outlier detection | Python import: `ScrapeCreatorsClient` |
| **linkedin-content** | Profile research, post analysis, company intel | CLI: `scrape.py linkedin profile/company-posts` |
| **youtube-content** | Channel analysis, video metadata, transcripts | CLI: `scrape.py youtube channel/transcript` |
| **paid-media-audit** | Ad library research (Meta, Google, LinkedIn, Reddit) | CLI: `scrape.py facebook ads-search` |
| **competitor-alternatives** | Multi-platform competitor intel gathering | CLI: multiple platform commands |
| **content-moat** | Trend research for originality scoring | CLI: `scrape.py tiktok trending` |
| **social-media** | Cross-platform audience research | CLI: profile commands across platforms |
| **script-skill** | Hook scraping, outlier video identification | Python import for batch processing |
| **campaign-runner** | Performance data for active campaigns | Python import for scheduled checks |

---

## Python Import Pattern

For skills that need programmatic access (batch processing, data pipelines):

```python
import sys
from pathlib import Path

# Resolve path relative to any skill's scripts/ directory
scrapecreators_path = Path(__file__).resolve().parents[2] / "scrapecreators" / "scripts"
sys.path.insert(0, str(scrapecreators_path))
from api import ScrapeCreatorsClient, find_project_root, load_env

# Initialize
client = ScrapeCreatorsClient(quiet=True)

# Use
videos = client.tiktok_videos_all("competitor", max_pages=3)
for v in videos:
    print(v.get("desc", "")[:100])

# Track costs
print(f"Credits used: {client.summary()['credits_used']}")
```

---

## CLI Pattern

For ad-hoc research and agent-driven workflows:

```bash
# Agent calls CLI, captures output
python3 skills/scrapecreators/scripts/scrape.py tiktok profile @competitor --format json

# Pipe to file for downstream processing
python3 skills/scrapecreators/scripts/scrape.py youtube videos UCxyz --format json -o /tmp/videos.json

# Quick markdown view in terminal
python3 skills/scrapecreators/scripts/scrape.py instagram profile @brand
```

---

## Common Integration Scenarios

### 1. Competitor Scan (tiktok-slideshows)

The `competitor_scan.py` script imports `ScrapeCreatorsClient` to:
- Fetch profile videos for multiple competitors
- Search keywords for content discovery
- Get trending hashtags and sounds
- Feed data into outlier detection and hooks-db

### 2. Ad Research (paid-media-audit)

```bash
# Research what competitors are running
scrape.py facebook ads-search "competitor name" --country US --format json
scrape.py google company-ads "competitor name" --format json
scrape.py linkedin ads "competitor product" --format json
scrape.py reddit ads-search "industry keyword" --format json
```

### 3. Content Inspiration (content-moat)

```bash
# What's trending right now
scrape.py tiktok trending --feed
scrape.py youtube trending-shorts
scrape.py tiktok trending --hashtags

# What's working for competitors
scrape.py instagram reels @competitor
scrape.py tiktok videos @competitor --pages 3
```

### 4. Audience Research (linkedin-content, social-media)

```bash
# LinkedIn company research
scrape.py linkedin company "company-url"
scrape.py linkedin company-posts "company-url"

# Reddit audience insights
scrape.py reddit subreddit "targetaudience"
scrape.py reddit subreddit-search "marketing" "pain point keyword"
```

### 5. Transcript Research (youtube-content, script-skill)

```bash
# Get video transcripts for analysis
scrape.py youtube transcript dQw4w9WgXcQ
scrape.py tiktok transcript 7123456789
scrape.py instagram transcript CxYz123
```

---

## Cost-Conscious Patterns

1. **Start with profiles** (1 credit) before deep dives
2. **Cap pagination** with `--pages N` to control costs
3. **Avoid audience demographics** (26 credits) unless specifically needed
4. **Use `scrape.py credits`** to monitor balance
5. **Batch wisely:** A full competitor scan = ~7 credits, not 50
