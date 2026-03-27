"""Phase 3.5b: HITL Review Gate — manual batch review before contact extraction.

Presents scored businesses in batches of 20 for human review.
Catches bad data, non-SG businesses, and irrelevant results before
spending Groq tokens + crawl4ai time on contact extraction.
"""

import json
from datetime import datetime
from pathlib import Path

from config import DATA_DIR


def review_batches(
    businesses: list[dict],
    batch_size: int = 20,
) -> list[dict]:
    """Interactive CLI review of scored businesses in batches.

    Returns list of approved businesses only.
    Saves review decisions to data/review_log.json.
    """
    if not businesses:
        print("No businesses to review.")
        return []

    approved = []
    removed = []
    skipped = []
    total = len(businesses)
    num_batches = (total + batch_size - 1) // batch_size

    print(f"\nHITL Review Gate: {total} businesses in {num_batches} batches of {batch_size}")
    print("─" * 80)

    for batch_idx in range(num_batches):
        start = batch_idx * batch_size
        end = min(start + batch_size, total)
        batch = businesses[start:end]

        print(f"\nBatch {batch_idx + 1}/{num_batches} (businesses {start + 1}-{end} of {total}):\n")

        # Print header
        print(f"{'#':>3}  {'Score':>5}  {'Ctry':>4}  {'Business Name':<30}  {'Domain':<28}  {'Verticals':<15}  {'Meta Ads':>8}")
        print("─" * 100)

        for i, biz in enumerate(batch):
            idx = start + i + 1
            name = (biz.get("business_name") or "?")[:30]
            domain = (biz.get("domain") or "—")[:28]
            verticals = ", ".join(biz.get("verticals", []))[:15]
            country = biz.get("country") or "?"
            score = biz.get("score", 0)
            meta_ads = biz.get("meta_ad_count", 0)

            print(f"{idx:>3}  {score:>5}  {country:>4}  {name:<30}  {domain:<28}  {verticals:<15}  {meta_ads:>8}")

        print()
        print("Actions: [a]pprove all  |  [r]emove by # (e.g., r 3,7,15)  |  [s]kip batch  |  [q]uit")

        while True:
            try:
                action = input("> ").strip().lower()
            except (EOFError, KeyboardInterrupt):
                action = "q"

            if action == "a":
                approved.extend(batch)
                print(f"  Approved {len(batch)} businesses")
                break

            elif action.startswith("r"):
                # Parse removal numbers
                nums_str = action[1:].strip().lstrip(" ")
                try:
                    remove_indices = {int(n.strip()) for n in nums_str.split(",")}
                except ValueError:
                    print("  Invalid format. Use: r 3,7,15")
                    continue

                for i, biz in enumerate(batch):
                    abs_idx = start + i + 1
                    if abs_idx in remove_indices:
                        removed.append(biz)
                    else:
                        approved.append(biz)

                kept = len(batch) - len(remove_indices & set(range(start + 1, end + 1)))
                print(f"  Kept {kept}, removed {len(batch) - kept}")
                break

            elif action == "s":
                skipped.extend(batch)
                print(f"  Skipped batch ({len(batch)} businesses)")
                break

            elif action == "q":
                skipped.extend(businesses[end:])  # skip remaining
                print(f"\n  Quit. Approved {len(approved)} total, skipping {total - len(approved) - len(removed)}.")
                _save_review_log(approved, removed, skipped)
                return approved

            else:
                print("  Unknown action. Use: a, r <numbers>, s, or q")

    print(f"\nReview complete: {len(approved)} approved, {len(removed)} removed, {len(skipped)} skipped")
    _save_review_log(approved, removed, skipped)
    return approved


def _save_review_log(
    approved: list[dict],
    removed: list[dict],
    skipped: list[dict],
) -> Path:
    """Save review decisions to data/review_log.json."""
    out = DATA_DIR / "review_log.json"
    log = {
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "approved": len(approved),
            "removed": len(removed),
            "skipped": len(skipped),
        },
        "removed_businesses": [
            {"uid": b.get("uid", ""), "name": b.get("business_name", ""), "domain": b.get("domain", "")}
            for b in removed
        ],
        "skipped_businesses": [
            {"uid": b.get("uid", ""), "name": b.get("business_name", ""), "domain": b.get("domain", "")}
            for b in skipped
        ],
    }
    out.write_text(json.dumps(log, indent=2))
    return out


# ── CLI ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    from scorer import load_scored

    businesses = load_scored()
    approved = review_batches(businesses)
    print(f"\n{len(approved)} businesses approved for contact extraction.")
