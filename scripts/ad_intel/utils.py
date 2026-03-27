"""Utilities for Singapore Ad Intelligence Pipeline."""

import re
from urllib.parse import urlparse
from thefuzz import fuzz


# ── Domain Normalization ─────────────────────────────────────────────────────

def normalize_domain(url_or_domain: str, strip_subdomains: bool = True) -> str:
    """Extract and normalize root domain from a URL or domain string.

    With strip_subdomains=True (default), reduces to the registrable domain:
        chinatown.compasschiropractic.sg → compasschiropractic.sg
        obt.zenyum.com → zenyum.com
        www.abcdental.com.sg → abcdental.com.sg

    Handles two-part TLDs (.com.sg, .com.au, .co.uk, etc.).
    """
    s = url_or_domain.strip()
    if not s:
        return ""
    # Add scheme if missing so urlparse works
    if not s.startswith(("http://", "https://")):
        s = "https://" + s
    try:
        host = urlparse(s).hostname or ""
    except Exception:
        return s.lower().strip("/")
    # Strip www prefix
    host = host.lower()
    if host.startswith("www."):
        host = host[4:]

    if not strip_subdomains:
        return host

    # Strip subdomains → keep only registrable domain
    # Two-part TLDs that are common in SG/APAC context
    two_part_tlds = {
        "com.sg", "org.sg", "edu.sg", "gov.sg", "net.sg",
        "com.au", "co.uk", "com.my", "co.id", "com.ph",
        "co.th", "co.in", "co.jp", "co.kr", "com.cn",
        "com.hk", "com.tw", "com.br", "co.nz",
    }
    parts = host.split(".")
    if len(parts) <= 2:
        return host  # already root (e.g., example.com)

    # Check if last two parts form a two-part TLD
    last_two = ".".join(parts[-2:])
    if last_two in two_part_tlds:
        # Root = name + two-part TLD (e.g., abcdental.com.sg)
        return ".".join(parts[-3:]) if len(parts) >= 3 else host
    else:
        # Root = name + single TLD (e.g., zenyum.com)
        return ".".join(parts[-2:])



def domains_match(d1: str, d2: str) -> bool:
    """Check if two domains are the same after normalization."""
    return normalize_domain(d1) == normalize_domain(d2)


# ── Phone / Postal Extraction ────────────────────────────────────────────────

# Singapore phone: 8 digits starting with 6/8/9, optionally +65 prefix
SG_PHONE_RE = re.compile(
    r"(?:\+65[\s-]?)?([689]\d{3}[\s-]?\d{4})"
)

# Singapore postal code: exactly 6 digits
SG_POSTAL_RE = re.compile(r"\b(\d{6})\b")

# Email
EMAIL_RE = re.compile(
    r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}"
)

# WhatsApp link: wa.me/<number> or api.whatsapp.com/send?phone=<number>
WHATSAPP_RE = re.compile(
    r"(?:wa\.me/|api\.whatsapp\.com/send\?phone=)(\+?\d{8,15})"
)


def extract_sg_phones(text: str) -> list[str]:
    """Extract Singapore phone numbers from text."""
    matches = SG_PHONE_RE.findall(text)
    # Normalize: remove spaces and dashes
    return list({re.sub(r"[\s\-]", "", m) for m in matches})


def extract_sg_postals(text: str) -> list[str]:
    """Extract 6-digit Singapore postal codes from text.
    Filters out obviously non-postal numbers (years, etc.).
    """
    candidates = SG_POSTAL_RE.findall(text)
    postals = []
    for c in candidates:
        n = int(c)
        # SG postal codes range roughly 01-83 for first two digits
        if 10000 <= n <= 839999:
            postals.append(c)
    return list(set(postals))


def extract_emails(text: str) -> list[str]:
    """Extract email addresses from text."""
    matches = EMAIL_RE.findall(text)
    # Filter out common false positives
    excluded = {"example.com", "email.com", "domain.com", "yoursite.com"}
    return [m for m in set(matches) if not any(ex in m for ex in excluded)]


def extract_whatsapp(text: str) -> list[str]:
    """Extract WhatsApp numbers from text."""
    return list(set(WHATSAPP_RE.findall(text)))


# ── Fuzzy Matching ───────────────────────────────────────────────────────────

def fuzzy_business_match(name1: str, name2: str, threshold: int = 80) -> bool:
    """Check if two business names are likely the same entity.

    Uses token_sort_ratio to handle word order differences:
        "ABC Dental" vs "ABC Dental Clinic Pte Ltd" → high score
    """
    if not name1 or not name2:
        return False
    score = fuzz.token_sort_ratio(name1.lower(), name2.lower())
    return score >= threshold


def clean_business_name(name: str) -> str:
    """Remove common suffixes for cleaner matching."""
    suffixes = [
        r"\bpte\.?\s*ltd\.?\b",
        r"\bprivate\s+limited\b",
        r"\blimited\b",
        r"\bltd\.?\b",
        r"\bllp\b",
        r"\binc\.?\b",
        r"\bsingapore\b",
        r"\bsg\b",
    ]
    cleaned = name
    for pattern in suffixes:
        cleaned = re.sub(pattern, "", cleaned, flags=re.IGNORECASE)
    return cleaned.strip().strip("- ,.")


# ── Country Detection ────────────────────────────────────────────────────────

# Phone prefix → country mapping (focus on APAC + common)
PHONE_COUNTRY_MAP = {
    "+65": "SG", "+60": "MY", "+62": "ID", "+63": "PH", "+66": "TH",
    "+84": "VN", "+91": "IN", "+81": "JP", "+82": "KR", "+86": "CN",
    "+852": "HK", "+853": "MO", "+886": "TW", "+61": "AU", "+64": "NZ",
    "+1": "US/CA", "+44": "UK", "+49": "DE", "+33": "FR",
}

# SG domain TLDs
SG_TLDS = {".sg", ".com.sg", ".org.sg", ".edu.sg", ".gov.sg", ".net.sg"}


def detect_country(phone: str = "", domain: str = "", address: str = "") -> str:
    """Detect country from phone prefix, domain TLD, or address keywords.

    Returns 2-letter country code or "" if unknown.
    Priority: phone > domain > address.
    """
    # Phone prefix check
    if phone:
        clean = phone.strip().replace(" ", "").replace("-", "")
        if not clean.startswith("+"):
            # 8-digit number starting with 6/8/9 = likely SG
            if re.match(r"^[689]\d{7}$", clean):
                return "SG"
        else:
            for prefix, country in sorted(PHONE_COUNTRY_MAP.items(), key=lambda x: -len(x[0])):
                if clean.startswith(prefix):
                    return country

    # Domain TLD check
    if domain:
        d = domain.lower()
        for tld in SG_TLDS:
            if d.endswith(tld):
                return "SG"
        # Other country TLDs
        country_tlds = {
            ".com.au": "AU", ".co.uk": "UK", ".com.my": "MY",
            ".co.id": "ID", ".com.ph": "PH", ".co.th": "TH",
            ".co.in": "IN", ".co.jp": "JP", ".co.kr": "KR",
            ".com.cn": "CN", ".com.hk": "HK", ".com.tw": "TW",
        }
        for tld, country in country_tlds.items():
            if d.endswith(tld):
                return country

    # Address keywords
    if address:
        addr_lower = address.lower()
        if "singapore" in addr_lower or re.search(r"\bsg\b", addr_lower):
            return "SG"

    return ""


# ── Data Helpers ─────────────────────────────────────────────────────────────

def chunk_list(lst: list, size: int) -> list[list]:
    """Split a list into chunks of given size."""
    return [lst[i : i + size] for i in range(0, len(lst), size)]
