"""Configuration for Singapore Ad Intelligence Pipeline."""

import os
import json
from pathlib import Path
from dotenv import load_dotenv

# Load .env from marketing root
_root = Path(__file__).resolve().parent.parent.parent
load_dotenv(_root / ".env")

# ── API Credentials ──────────────────────────────────────────────────────────

DATAFORSEO_LOGIN = os.getenv("DATAFORSEO_LOGIN", "")
DATAFORSEO_PASSWORD = os.getenv("DATAFORSEO_PASSWORD", "")
SCRAPECREATORS_API_KEY = os.getenv("SCRAPECREATORS_API_KEY", "")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY", "")

# Google Sheets — path to service account JSON
GSHEETS_CREDENTIALS_FILE = os.getenv(
    "GSHEETS_CREDENTIALS_FILE",
    str(_root / "credentials" / "gsheets-service-account.json"),
)
GSHEETS_SHARE_EMAIL = os.getenv("GSHEETS_SHARE_EMAIL", "")  # email to share sheet with

# ── Rate Limits & Concurrency ────────────────────────────────────────────────

DATAFORSEO_BATCH_SIZE = 100       # keywords per batch POST
DATAFORSEO_PARALLEL_BATCHES = 8   # concurrent batch requests
SCRAPECREATORS_RATE_LIMIT = 2     # seconds between requests
CRAWL4AI_CONCURRENCY = 50         # concurrent website scrapes
GROQ_MODEL = "llama-3.3-70b-versatile"
GROQ_RPM = 30                     # requests per minute (free tier)
FIRECRAWL_FALLBACK_BUDGET = 200   # max firecrawl credits to use

# ── Paths ────────────────────────────────────────────────────────────────────

DATA_DIR = Path(__file__).parent / "data"
OUTPUT_DIR = Path(__file__).parent / "output"
BLOCKLIST_FILE = DATA_DIR / "blocklist.json"

# ── Scoring Weights ──────────────────────────────────────────────────────────

SCORE_THRESHOLDS = {
    "hot": 8,   # 8-10
    "warm": 4,  # 4-7
    "cold": 1,  # 1-3
}

# ── Evaluator Settings ───────────────────────────────────────────────────────

EVAL_SAMPLE_KEYWORDS_PER_VERTICAL = 3
EVAL_TOP_RESULTS_PER_VERTICAL = 10
EVAL_PASS_THRESHOLD = 8    # out of 10
EVAL_PASS_RATE_REQUIRED = 0.70  # 70% must pass

# ── Verticals ────────────────────────────────────────────────────────────────

VERTICALS = [
    "real_estate",
    "aesthetic_clinics",
    "dental",
    "renovation",
    "tuition",
    "wedding",
    "legal_accounting",
    "fitness_wellness",
]

VERTICAL_DISPLAY_NAMES = {
    "real_estate": "Real Estate",
    "aesthetic_clinics": "Aesthetic Clinics",
    "dental": "Dental",
    "renovation": "Renovation",
    "tuition": "Tuition",
    "wedding": "Wedding",
    "legal_accounting": "Legal & Accounting",
    "fitness_wellness": "Fitness & Wellness",
}

# ── Helpers ──────────────────────────────────────────────────────────────────

def load_blocklist() -> set[str]:
    """Load blocked domains from blocklist.json."""
    if BLOCKLIST_FILE.exists():
        data = json.loads(BLOCKLIST_FILE.read_text())
        return set(data.get("domains", []))
    return set()


def check_credentials() -> dict[str, bool]:
    """Check which API credentials are configured."""
    return {
        "dataforseo": bool(DATAFORSEO_LOGIN and DATAFORSEO_PASSWORD),
        "scrapecreators": bool(SCRAPECREATORS_API_KEY),
        "groq": bool(GROQ_API_KEY),
        "firecrawl": bool(FIRECRAWL_API_KEY),
        "gsheets": Path(GSHEETS_CREDENTIALS_FILE).exists() if GSHEETS_CREDENTIALS_FILE else False,
    }
