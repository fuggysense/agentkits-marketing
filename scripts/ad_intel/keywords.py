"""Phase 1: Keyword Engine — generate 1,000-2,000 search keywords across 8 verticals."""

import json
from itertools import product
from pathlib import Path
from config import DATA_DIR, VERTICALS

# ── Singapore Locations ──────────────────────────────────────────────────────

LOCATIONS = [
    # Central
    "orchard", "bugis", "tanjong pagar", "raffles place", "marina bay",
    "city hall", "dhoby ghaut", "somerset", "river valley", "novena",
    "newton", "tiong bahru", "chinatown", "little india", "kampong glam",
    "robertson quay", "clarke quay",
    # North
    "woodlands", "yishun", "sembawang", "ang mo kio", "bishan",
    "toa payoh", "thomson", "lentor", "springleaf",
    # East
    "tampines", "bedok", "pasir ris", "simei", "changi",
    "marine parade", "katong", "east coast", "geylang", "eunos",
    "kembangan", "paya lebar",
    # West
    "jurong east", "jurong west", "clementi", "bukit batok",
    "bukit panjang", "choa chu kang", "west coast", "dover",
    "buona vista", "one-north", "holland village",
    # North-East
    "hougang", "sengkang", "punggol", "serangoon", "kovan",
    "upper serangoon", "buangkok",
    # South
    "bukit merah", "harbourfront", "sentosa", "telok blangah",
    # Premium areas
    "bukit timah", "tanglin", "nassim", "sixth avenue",
    "holland road", "dempsey",
]

INTENT_MODIFIERS = [
    "best", "top", "near me", "cheap", "affordable", "cost",
    "review", "recommended", "trusted", "professional",
]

# ── Vertical Definitions ─────────────────────────────────────────────────────

VERTICAL_KEYWORDS: dict[str, dict] = {
    "real_estate": {
        "base": [
            "property agent", "real estate agent", "condo for sale",
            "hdb resale", "property listing", "real estate agency",
            "buy condo", "sell hdb", "property valuation", "property consultant",
            "rental agent", "landed property", "ec launch", "new condo launch",
            "property investment", "bto resale", "hdb upgrade",
            "private property", "freehold condo", "leasehold condo",
        ],
        "services": [
            "home loan advisor", "mortgage broker", "property viewing",
            "hdb 4-room resale", "hdb 5-room resale", "executive condo",
            "penthouse for sale", "shophouse for sale", "commercial property",
            "industrial property", "office space for rent", "co-working space",
            "property management", "strata management", "hdb valuation",
            "stamp duty calculator", "property tax", "rental yield",
            "sub-sale condo", "new launch condo 2026", "property auction",
            "district 9 condo", "district 10 condo", "district 15 condo",
            "cbd office space", "shop for rent", "warehouse for rent",
            "serviced apartment", "student accommodation", "expat housing",
            "hdb flat upgrade", "opposite sex scheme hdb", "singles hdb",
            "hdb loan eligibility", "cpf housing", "bank loan property",
            "resale levy", "mop hdb", "top hdb towns",
        ],
        "local": [
            "property agent sg", "propnex", "era realty", "huttons",
            "orangetee", "sg property", "singapore condo",
        ],
    },
    "aesthetic_clinics": {
        "base": [
            "aesthetic clinic", "beauty clinic", "skin clinic",
            "medical aesthetics", "cosmetic clinic", "dermatologist",
            "aesthetic doctor", "skin specialist", "beauty treatment",
            "anti-aging clinic", "laser clinic", "medi-spa",
            "aesthetic treatment", "skin care clinic", "beauty spa",
        ],
        "services": [
            "botox", "filler", "acne scar treatment", "laser treatment",
            "hair removal", "pico laser", "ultherapy", "thermage",
            "hifu treatment", "skin tightening", "fat freezing",
            "coolsculpting", "liposuction", "nose thread lift",
            "chin filler", "lip filler", "dark eye circles treatment",
            "pigmentation treatment", "hydrafacial", "chemical peel",
            "microneedling", "prp treatment", "rejuran",
            "profhilo", "skinbooster", "double chin removal",
            "eye bag removal", "facelift", "neck lift",
            "body contouring", "cellulite treatment", "stretch marks",
            "tattoo removal", "mole removal", "skin tag removal",
            "iv drip therapy", "whitening treatment", "glow facial",
            "co2 laser", "fractional laser", "vaser liposuction",
            "breast augmentation", "rhinoplasty", "blepharoplasty",
            "eyelid surgery", "jaw reduction", "cheek filler",
        ],
        "local": [
            "aesthetic clinic sg", "beauty clinic singapore",
            "skin doctor singapore", "botox singapore",
        ],
    },
    "dental": {
        "base": [
            "dental clinic", "dentist", "dental surgery",
            "dental care", "family dentist", "dental centre",
            "dental specialist", "oral health", "dental practice",
            "dental group", "dental studio", "dental office",
            "pediatric dentist", "emergency dentist", "dental hospital",
        ],
        "services": [
            "teeth whitening", "braces", "invisalign", "root canal",
            "dental implant", "wisdom tooth extraction", "crown",
            "dental bridge", "veneer", "tooth filling", "scaling polishing",
            "gum treatment", "orthodontist", "oral surgery",
            "teeth cleaning", "dental x-ray", "night guard",
            "retainer", "ceramic braces", "lingual braces",
            "dental bonding", "tooth extraction", "dentures",
            "endodontist", "periodontist", "prosthodontist",
            "tmj treatment", "sleep apnea dental", "kids dentist",
            "baby teeth", "zirconia crown",
        ],
        "local": [
            "dentist sg", "dental clinic singapore",
            "cheap dentist singapore", "polyclinic dental",
        ],
    },
    "renovation": {
        "base": [
            "renovation contractor", "interior design", "home renovation",
            "hdb renovation", "condo renovation", "kitchen renovation",
            "bathroom renovation", "renovation company", "id firm",
            "interior designer", "home makeover", "house renovation",
            "landed renovation", "shop renovation", "office renovation",
        ],
        "services": [
            "hdb 4-room renovation", "hdb 5-room renovation",
            "bto renovation package", "resale renovation",
            "kitchen cabinet", "wardrobe design", "false ceiling",
            "vinyl flooring", "toilet renovation", "feature wall",
            "built-in wardrobe", "shoe cabinet", "tv console",
            "carpentry work", "plumbing", "electrical work",
            "painting services", "waterproofing", "tiling",
            "aircon installation", "smart home", "lighting design",
            "open kitchen concept", "walk-in wardrobe",
            "laundry room design", "bomb shelter conversion",
            "balcony renovation", "window grille", "roller blind",
            "curtain", "wallpaper installation",
        ],
        "local": [
            "renovation sg", "reno contractor", "id firm singapore",
            "hdb reno", "bto reno", "singapore renovation",
        ],
    },
    "tuition": {
        "base": [
            "tuition centre", "tuition teacher", "private tutor",
            "tuition agency", "home tuition", "group tuition",
            "enrichment centre", "learning centre", "education centre",
            "academic tuition", "exam preparation", "study skills",
            "tuition class", "coaching centre", "tutorial centre",
        ],
        "services": [
            "primary school tuition", "secondary school tuition",
            "jc tuition", "a level tuition", "o level tuition",
            "psle tuition", "math tuition", "science tuition",
            "english tuition", "chinese tuition", "malay tuition",
            "tamil tuition", "physics tuition", "chemistry tuition",
            "biology tuition", "additional math tuition",
            "gp tuition", "economics tuition", "geography tuition",
            "history tuition", "literature tuition",
            "ip tuition", "ib tuition", "igcse tuition",
            "sat prep singapore", "gmat prep", "ielts prep",
            "coding class kids", "robotics class", "abacus class",
            "phonics class", "creative writing class",
            "nursery enrichment", "kindergarten enrichment",
            "speech drama", "public speaking kids",
            "preschool enrichment", "music lesson", "art class",
            "ballet class", "swimming lesson",
        ],
        "local": [
            "tuition sg", "tuition teacher singapore",
            "tuition centre singapore", "home tutor sg",
        ],
    },
    "wedding": {
        "base": [
            "wedding planner", "bridal shop", "wedding venue",
            "wedding photographer", "wedding videographer",
            "bridal boutique", "wedding dress", "wedding package",
            "rom venue", "wedding coordinator", "bridal studio",
            "pre-wedding photoshoot", "actual day photography",
            "wedding florist", "wedding caterer",
        ],
        "services": [
            "bridal makeup", "wedding gown rental", "groom suit rental",
            "wedding invitation", "wedding decoration",
            "solemnization venue", "banquet venue", "wedding dinner",
            "church wedding", "garden wedding", "beach wedding",
            "hotel wedding", "rom ceremony", "tea ceremony",
            "wedding cake", "wedding band music", "emcee wedding",
            "photo booth rental", "wedding car rental",
            "overseas pre-wedding", "wedding ring", "engagement ring",
            "wedding favour", "wedding door gift",
            "bridal hair", "bridal gown alteration",
        ],
        "local": [
            "wedding sg", "bridal singapore", "rom singapore",
            "wedding package singapore",
        ],
    },
    "legal_accounting": {
        "base": [
            "lawyer", "law firm", "legal services", "solicitor",
            "accountant", "accounting firm", "tax advisor",
            "corporate secretary", "company registration",
            "audit firm", "bookkeeping service", "tax filing",
            "legal counsel", "attorney", "advocate",
        ],
        "services": [
            "divorce lawyer", "criminal lawyer", "personal injury lawyer",
            "employment lawyer", "property lawyer", "conveyancing lawyer",
            "family lawyer", "litigation lawyer", "corporate lawyer",
            "ip lawyer", "trademark registration", "patent filing",
            "will writing", "estate planning", "probate lawyer",
            "debt recovery", "bankruptcy lawyer", "mediation",
            "company incorporation", "gst registration",
            "annual return filing", "xero accounting",
            "payroll service", "tax planning", "iras tax filing",
            "audit service", "financial advisory", "cfo service",
            "virtual cfo", "company strike off", "nominee director",
            "work visa", "employment pass", "dependent pass",
        ],
        "local": [
            "lawyer sg", "law firm singapore", "accountant singapore",
            "acra registration", "singapore company setup",
        ],
    },
    "fitness_wellness": {
        "base": [
            "gym", "fitness centre", "personal trainer",
            "yoga studio", "pilates studio", "crossfit",
            "martial arts", "boxing gym", "swimming class",
            "wellness centre", "spa", "massage",
            "physiotherapy", "chiropractic", "tcm clinic",
        ],
        "services": [
            "personal training", "group fitness class", "weight loss program",
            "body transformation", "strength training", "hiit class",
            "spin class", "barre class", "aerial yoga",
            "prenatal yoga", "postnatal recovery", "muay thai",
            "brazilian jiu-jitsu", "karate", "taekwondo",
            "kids swimming", "adult swimming lesson",
            "sports massage", "deep tissue massage", "thai massage",
            "reflexology", "acupuncture", "cupping",
            "tcm treatment", "slimming treatment",
            "physiotherapy sports", "rehabilitation",
            "osteopathy", "posture correction",
            "corporate wellness", "meditation class",
            "sound healing", "breathwork",
        ],
        "local": [
            "gym sg", "personal trainer singapore",
            "yoga singapore", "pilates singapore",
            "tcm singapore", "physiotherapy singapore",
        ],
    },
}


def generate_keywords(
    verticals: list[str] | None = None,
    include_locations: bool = True,
    include_intent: bool = True,
    max_per_vertical: int = 300,
) -> dict[str, list[str]]:
    """Generate keyword list per vertical.

    Returns dict mapping vertical name → list of keyword strings.
    """
    target_verticals = verticals or VERTICALS
    all_keywords: dict[str, list[str]] = {}

    for vertical in target_verticals:
        if vertical not in VERTICAL_KEYWORDS:
            continue

        vk = VERTICAL_KEYWORDS[vertical]
        kw_set: set[str] = set()

        # 1. Base terms + "singapore"
        for base in vk["base"]:
            kw_set.add(f"{base} singapore")
            kw_set.add(base)

        # 2. Service-specific terms + "singapore"
        for svc in vk.get("services", []):
            kw_set.add(f"{svc} singapore")
            kw_set.add(svc)

        # 3. Local/Singlish terms
        for local in vk.get("local", []):
            kw_set.add(local)

        # 4. Location modifiers (base × location)
        if include_locations:
            # Use top 20 locations to avoid explosion
            top_locations = LOCATIONS[:30]
            for base in vk["base"][:8]:  # top 8 base terms only
                for loc in top_locations:
                    kw_set.add(f"{base} {loc}")

        # 5. Intent modifiers (top base terms × intent)
        if include_intent:
            for base in vk["base"][:6]:
                for intent in INTENT_MODIFIERS[:6]:
                    kw_set.add(f"{intent} {base} singapore")

        # Cap per vertical
        kw_list = sorted(kw_set)[:max_per_vertical]
        all_keywords[vertical] = kw_list

    return all_keywords


def save_keywords(keywords: dict[str, list[str]], path: Path | None = None) -> Path:
    """Save keywords to JSON file. Returns path."""
    out = path or (DATA_DIR / "keywords.json")
    total = sum(len(v) for v in keywords.values())

    payload = {
        "total_keywords": total,
        "verticals": {
            v: {"count": len(kws), "keywords": kws}
            for v, kws in keywords.items()
        },
    }
    out.write_text(json.dumps(payload, indent=2))
    return out


def load_keywords(path: Path | None = None) -> dict[str, list[str]]:
    """Load keywords from JSON file."""
    p = path or (DATA_DIR / "keywords.json")
    data = json.loads(p.read_text())
    return {v: info["keywords"] for v, info in data["verticals"].items()}


# ── CLI ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    keywords = generate_keywords()
    out = save_keywords(keywords)
    total = sum(len(v) for v in keywords.values())
    print(f"Generated {total} keywords across {len(keywords)} verticals")
    for v, kws in keywords.items():
        print(f"  {v}: {len(kws)} keywords")
    print(f"Saved to {out}")
