#!/usr/bin/env python3
"""
verify-research-citations.py
-----------------------------
Reads a markdown file, extracts citations, fetches each URL, and checks
whether the quoted phrase (or an 85%+ fuzzy match) appears in the page text.

Supported citation patterns:
  1. Block-quote style:  > "quote" — source: URL
  2. Inline markdown:    [quote](URL)

Usage:
  python3 scripts/verify-research-citations.py <markdown_file> [--out results.csv]

Output CSV columns:
  citation_id, quote, url, http_status, phrase_found, similarity_pct, error
"""

import sys
import re
import csv
import argparse
from pathlib import Path

# Dependency check — fail gracefully with install instructions
missing = []
try:
    import requests
except ImportError:
    missing.append("requests")
try:
    from bs4 import BeautifulSoup
except ImportError:
    missing.append("beautifulsoup4")
try:
    from rapidfuzz import fuzz
except ImportError:
    missing.append("rapidfuzz")

if missing:
    print(f"ERROR: Missing dependencies: {', '.join(missing)}")
    print("Install with:")
    print(f"  pip3 install {' '.join(missing)}")
    sys.exit(1)


# ── Citation extraction ────────────────────────────────────────────────────────

PATTERN_BLOCKQUOTE = re.compile(
    r'>\s*["“](.+?)["”]\s*[—–-]+\s*source:\s*(https?://\S+)',
    re.IGNORECASE
)
PATTERN_INLINE = re.compile(
    r'\[([^\]]{10,})\]\((https?://[^\)]+)\)'
)


def extract_citations(md_text: str) -> list[dict]:
    citations = []
    seen = set()

    for i, m in enumerate(PATTERN_BLOCKQUOTE.finditer(md_text), start=1):
        key = (m.group(1).strip(), m.group(2).strip())
        if key not in seen:
            seen.add(key)
            citations.append({"id": f"bq-{i:03d}", "quote": key[0], "url": key[1]})

    for i, m in enumerate(PATTERN_INLINE.finditer(md_text), start=1):
        key = (m.group(1).strip(), m.group(2).strip())
        if key not in seen:
            seen.add(key)
            citations.append({"id": f"il-{i:03d}", "quote": key[0], "url": key[1]})

    return citations


# ── URL fetching ───────────────────────────────────────────────────────────────

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0 Safari/537.36"
    )
}


def fetch_text(url: str, timeout: int = 10) -> tuple[int, str, str]:
    """Returns (http_status, page_text, error_str)."""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=timeout, allow_redirects=True)
        status = resp.status_code
        if status in (403, 429):
            return status, "", f"HTTP {status} — cannot verify (bot protection)"
        if status != 200:
            return status, "", f"HTTP {status}"
        soup = BeautifulSoup(resp.text, "html.parser")
        # Remove script/style noise
        for tag in soup(["script", "style", "nav", "header", "footer"]):
            tag.decompose()
        text = soup.get_text(separator=" ", strip=True)
        return status, text, ""
    except requests.exceptions.Timeout:
        return 0, "", "Timeout after 10s"
    except requests.exceptions.ConnectionError as e:
        return 0, "", f"ConnectionError: {str(e)[:80]}"
    except Exception as e:
        return 0, "", f"Unexpected error: {str(e)[:80]}"


# ── Phrase matching ────────────────────────────────────────────────────────────

SIMILARITY_THRESHOLD = 85


def check_phrase(quote: str, page_text: str) -> tuple[bool, int]:
    """
    Returns (found: bool, best_similarity_pct: int).
    Scans the page text in sliding windows ~2× the quote length for best partial match.
    """
    if not page_text:
        return False, 0

    quote_clean = quote.strip().lower()
    page_lower = page_text.lower()

    # Fast exact check first
    if quote_clean in page_lower:
        return True, 100

    # Sliding window fuzzy match — window = 1.5x quote length, step = 20 chars
    q_len = len(quote_clean)
    window = min(int(q_len * 1.5) + 30, 500)
    step = max(20, q_len // 4)
    best = 0

    for start in range(0, max(1, len(page_lower) - window), step):
        chunk = page_lower[start : start + window]
        score = fuzz.partial_ratio(quote_clean, chunk)
        if score > best:
            best = score
        if best == 100:
            break

    found = best >= SIMILARITY_THRESHOLD
    return found, best


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Verify research citations in a markdown file"
    )
    parser.add_argument("markdown_file", help="Path to the markdown file to check")
    parser.add_argument(
        "--out", default="results.csv", help="Output CSV path (default: results.csv)"
    )
    parser.add_argument(
        "--timeout", type=int, default=10, help="HTTP timeout per URL in seconds (default: 10)"
    )
    args = parser.parse_args()

    md_path = Path(args.markdown_file)
    if not md_path.exists():
        print(f"ERROR: File not found: {md_path}")
        sys.exit(1)

    md_text = md_path.read_text(encoding="utf-8")
    citations = extract_citations(md_text)

    if not citations:
        print(f"No citations found in {md_path}")
        print("Supported patterns:")
        print('  > "quote" — source: https://...')
        print("  [quote text](https://...)")
        sys.exit(0)

    print(f"Found {len(citations)} citation(s) in {md_path.name}")
    print(f"Verifying... (timeout: {args.timeout}s per URL)\n")

    rows = []
    pass_count = 0
    fail_count = 0
    skip_count = 0

    for c in citations:
        cid = c["id"]
        quote = c["quote"]
        url = c["url"]

        print(f"[{cid}] {url[:70]}...")
        status, page_text, error = fetch_text(url, timeout=args.timeout)

        if error and not page_text:
            phrase_found = "SKIP"
            similarity_pct = 0
            result_icon = "⚠️ "
            skip_count += 1
        else:
            found, sim = check_phrase(quote, page_text)
            phrase_found = "YES" if found else "NO"
            similarity_pct = sim
            if found:
                result_icon = "✓  "
                pass_count += 1
            else:
                result_icon = "✗  "
                fail_count += 1

        print(f"  {result_icon} status={status}  phrase_found={phrase_found}  similarity={similarity_pct}%  error={error or 'none'}")

        rows.append({
            "citation_id": cid,
            "quote": quote[:120],
            "url": url,
            "http_status": status,
            "phrase_found": phrase_found,
            "similarity_pct": similarity_pct,
            "error": error
        })

    # Write CSV
    out_path = Path(args.out)
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["citation_id", "quote", "url", "http_status", "phrase_found", "similarity_pct", "error"]
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"\n{'─'*60}")
    print(f"Results: {pass_count} passed · {fail_count} failed · {skip_count} skipped (bot-protected)")
    print(f"CSV written to: {out_path}")

    if fail_count > 0:
        print(f"\n⚠️  HITL GATE: {fail_count} citation(s) could not be verified.")
        print("Review the CSV and either fix the source URLs or flag the quotes as unverifiable before approving this doc.")
        sys.exit(2)  # Non-zero exit lets CI/pre-approve scripts detect failures


if __name__ == "__main__":
    main()
