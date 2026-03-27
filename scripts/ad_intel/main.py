"""Singapore Ad Intelligence Pipeline — CLI Orchestrator.

Usage:
    python main.py --per-vertical           # Run full pipeline per vertical (recommended)
    python main.py --per-vertical --sample 3  # Test mode: 3 keywords/vertical
    python main.py --per-vertical -v dental,real_estate  # Specific verticals only
    python main.py --per-vertical --no-review  # Skip HITL review gate
    python main.py --phase all              # Run full pipeline (all phases, all verticals at once)
    python main.py --phase keywords         # Phase 1 only
    python main.py --phase google           # Phase 2a only
    python main.py --phase meta             # Phase 2b only
    python main.py --phase score            # Phase 3 only
    python main.py --phase evaluate         # Phase 3.5 only
    python main.py --phase deep-dive        # Phase 3.6: Meta deep-dive top companies
    python main.py --phase review           # Phase 3.7: HITL review gate
    python main.py --phase contacts         # Phase 4 only
    python main.py --phase dedup            # Phase 4.5 only
    python main.py --phase export           # Phase 5 only
    python main.py --verticals real_estate,dental   # Specific verticals
    python main.py --output csv             # CSV instead of Sheets
    python main.py --sample 3               # Test mode: 3 keywords/vertical
    python main.py --no-review              # Skip HITL review gate
    python main.py --check                  # Check API credentials
"""

import argparse
import asyncio
import json
import sys
from datetime import datetime
from pathlib import Path

from config import (
    DATA_DIR, OUTPUT_DIR, VERTICALS, VERTICAL_DISPLAY_NAMES,
    check_credentials,
)


def _print_header(text: str):
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")


def _check_creds():
    """Check and display API credential status."""
    creds = check_credentials()
    print("API Credential Status:")
    for name, ok in creds.items():
        status = "✓ Ready" if ok else "✗ Missing"
        print(f"  {name:20s} {status}")
    return creds


async def run_pipeline(
    phases: list[str],
    verticals: list[str] | None = None,
    output_format: str = "sheets",
    sample_size: int | None = None,
    no_review: bool = False,
):
    """Run the specified pipeline phases."""
    target_verticals = verticals or VERTICALS
    run_all = "all" in phases

    # ── Phase 1: Keywords ──
    if run_all or "keywords" in phases:
        _print_header("Phase 1: Keyword Generation")
        from keywords import generate_keywords, save_keywords

        max_per = sample_size * 10 if sample_size else 300
        keywords = generate_keywords(
            verticals=target_verticals,
            max_per_vertical=max_per,
        )
        save_keywords(keywords)
        total = sum(len(v) for v in keywords.values())
        print(f"Generated {total} keywords across {len(keywords)} verticals")
        for v, kws in keywords.items():
            print(f"  {VERTICAL_DISPLAY_NAMES.get(v, v)}: {len(kws)}")

    # ── Phase 2a: Google Ads Scan ──
    if run_all or "google" in phases:
        _print_header("Phase 2a: Google Ads Scan (DataForSEO)")
        from keywords import load_keywords
        from google_scan import scan_google_ads, save_google_results

        keywords = load_keywords()
        # Trim if sample mode
        if sample_size:
            keywords = {v: kws[:sample_size] for v, kws in keywords.items() if v in target_verticals}

        results = await scan_google_ads(keywords)
        save_google_results(results)
        total = sum(len(v) for v in results.values())
        print(f"Found {total} paid ads")

    # ── Phase 2b: Meta Ad Library Scan ──
    if run_all or "meta" in phases:
        _print_header("Phase 2b: Meta Ad Library Scan (ScrapeCreators)")
        from keywords import load_keywords
        from meta_scan import scan_meta_ads, save_meta_results

        keywords = load_keywords()
        if sample_size:
            keywords = {v: kws[:sample_size] for v, kws in keywords.items() if v in target_verticals}

        max_kw = sample_size or 50
        results = await scan_meta_ads(keywords, max_keywords_per_vertical=max_kw)

        # Resolve missing domains from FB pages
        from meta_scan import resolve_missing_domains
        results = await resolve_missing_domains(results)

        save_meta_results(results)
        total = sum(len(v) for v in results.values())
        with_domain = sum(1 for ads in results.values() for a in ads if a.get("domain"))
        print(f"Found {total} Meta ads ({with_domain} with website domains)")

    # ── Phase 3: Score ──
    if run_all or "score" in phases:
        _print_header("Phase 3: Merge & Score")
        from google_scan import load_google_results
        from meta_scan import load_meta_results
        from scorer import score_businesses, save_scored

        google = load_google_results()
        meta = load_meta_results()
        scored = score_businesses(google, meta)
        save_scored(scored)

        from collections import Counter
        tiers = Counter(b["tier"] for b in scored)
        print(f"Scored {len(scored)} businesses")
        print(f"  Hot: {tiers['hot']} | Warm: {tiers['warm']} | Cold: {tiers['cold']}")

    # ── Phase 3.5: Evaluator Gate ──
    if run_all or "evaluate" in phases:
        _print_header("Phase 3.5: Evaluator Gate")
        from scorer import load_scored
        from evaluator import evaluate_batch, save_evaluation

        scored = load_scored()
        report = await evaluate_batch(scored)
        save_evaluation(report)

        decision = report["gate_decision"]
        rate = report["pass_rate"]
        print(f"Gate decision: {decision} (pass rate: {rate:.1%})")

        if decision == "FAIL":
            print("\n⚠️  Evaluator gate FAILED. Review evaluation_report.json")
            print("   Adjust keywords/scoring before proceeding to mass scrape.")
            if "all" in phases:
                print("   Stopping pipeline. Fix issues and re-run.")
                return

    # ── Phase 3.6: Meta Deep-Dive (top companies) ──
    if run_all or "deep-dive" in phases:
        _print_header("Phase 3.6: Meta Deep-Dive (Top Companies)")
        from scorer import load_scored, save_scored
        from meta_scan import deep_dive_top_companies

        scored = load_scored()
        deep_results = await deep_dive_top_companies(scored, min_score=4)

        # Enrich scored businesses with deep-dive ad counts
        for biz in scored:
            name = biz.get("business_name", "")
            if name in deep_results and not deep_results[name].get("error"):
                dd = deep_results[name]
                biz["meta_deep_dive_count"] = dd["ad_count"]
                # Update sample ad copy if we got better data
                if dd["ads"] and not biz.get("sample_ad_copy"):
                    first_ad = dd["ads"][0]
                    snapshot = first_ad.get("snapshot", first_ad)
                    body = snapshot.get("body", {})
                    biz["sample_ad_copy"] = (
                        body.get("text", "") if isinstance(body, dict) else str(body)
                    )[:200]

        save_scored(scored)
        print(f"Deep-dived {len(deep_results)} companies")

    # ── Phase 3.7: HITL Review Gate ──
    if (run_all or "review" in phases) and not no_review:
        _print_header("Phase 3.7: HITL Review Gate")
        from scorer import load_scored, save_scored
        from review import review_batches

        scored = load_scored()
        approved = review_batches(scored, batch_size=20)

        if len(approved) < len(scored):
            # Save only approved businesses back
            save_scored(approved)
            print(f"Proceeding with {len(approved)}/{len(scored)} approved businesses")

    # ── Phase 4: Contact Extraction ──
    if run_all or "contacts" in phases:
        _print_header("Phase 4: Contact + Location + Metadata Extraction")
        from scorer import load_scored
        from contact_scraper import extract_contacts, save_contacts

        scored = load_scored()
        contacts = await extract_contacts(scored)
        save_contacts(contacts)

        total = len(contacts)
        phones = sum(1 for c in contacts if c.get("phone"))
        emails = sum(1 for c in contacts if c.get("email"))
        dm = sum(1 for c in contacts if c.get("decision_maker_full_name"))
        meta_ok = sum(1 for c in contacts if c.get("page_title"))
        print(f"Extracted contacts for {total} businesses")
        print(f"  Phone: {phones} | Email: {emails} | Decision Maker: {dm} | Metadata: {meta_ok}")

    # ── Phase 4.5: Dedup ──
    if run_all or "dedup" in phases:
        _print_header("Phase 4.5: Deduplication + HQ Resolution")
        from contact_scraper import load_contacts
        from dedup import deduplicate, save_deduped

        contacts = load_contacts()
        before = len(contacts)
        deduped = deduplicate(contacts)
        save_deduped(deduped)

        chains = sum(1 for b in deduped if b.get("is_chain"))
        print(f"Before: {before} → After: {len(deduped)} (removed {before - len(deduped)} dupes)")
        print(f"  Chains flagged: {chains}")

    # ── Phase 5: Export ──
    if run_all or "export" in phases:
        _print_header("Phase 5: Export")
        from dedup import load_deduped
        from sheets_export import export_to_sheets, export_to_csv

        deduped = load_deduped()

        if output_format == "csv":
            csv_path = export_to_csv(deduped)
            print(f"CSV exported: {csv_path}")
        else:
            try:
                url = export_to_sheets(deduped)
                print(f"Google Sheet: {url}")
            except Exception as e:
                print(f"Sheets failed ({e}), falling back to CSV...")
                csv_path = export_to_csv(deduped)
                print(f"CSV exported: {csv_path}")

    _print_header("Pipeline Complete")
    print(f"Data files in: {DATA_DIR}")
    print(f"Output files in: {OUTPUT_DIR}")


async def run_per_vertical(
    verticals: list[str] | None = None,
    output_format: str = "sheets",
    sample_size: int | None = None,
    no_review: bool = False,
    sheet_url: str | None = None,
):
    """Run the full pipeline one vertical at a time.

    Each vertical goes through all phases end-to-end, then its results
    are exported as a tab to one shared Google Sheet before moving
    to the next vertical.
    """
    from collections import Counter
    from keywords import generate_keywords, save_keywords, load_keywords
    from google_scan import scan_google_ads, save_google_results, load_google_results
    from meta_scan import (
        scan_meta_ads, save_meta_results, load_meta_results,
        resolve_missing_domains,
    )
    from scorer import score_businesses, save_scored, load_scored
    from contact_scraper import extract_contacts, save_contacts
    from dedup import deduplicate, save_deduped
    from sheets_export import (
        create_spreadsheet, add_vertical_tab, export_to_csv,
        open_spreadsheet,
    )

    target_verticals = verticals or VERTICALS

    # Reuse existing sheet or create one
    # Persist sheet URL so subsequent runs auto-reuse it
    sheet_url_file = DATA_DIR / "sheet_url.txt"
    spreadsheet = None
    if output_format == "sheets":
        try:
            # Priority: CLI arg > saved URL > create new
            if not sheet_url and sheet_url_file.exists():
                sheet_url = sheet_url_file.read_text().strip()

            if sheet_url:
                spreadsheet = open_spreadsheet(sheet_url)
                print(f"Using existing sheet: {sheet_url}")
            else:
                spreadsheet, sheet_url = create_spreadsheet()
                sheet_url_file.write_text(sheet_url)
                print(f"Google Sheet created: {sheet_url}")
        except Exception as e:
            print(f"Sheets failed ({e}), will fall back to CSV per vertical.")
            output_format = "csv"

    for v_idx, vertical in enumerate(target_verticals):
        display = VERTICAL_DISPLAY_NAMES.get(vertical, vertical)
        _print_header(f"[{v_idx + 1}/{len(target_verticals)}] {display}")

        # ── Phase 1: Keywords ──
        print(f"  Phase 1: Keywords...")
        max_per = sample_size * 10 if sample_size else 300
        kw_all = generate_keywords(verticals=[vertical], max_per_vertical=max_per)
        save_keywords(kw_all)
        kw_count = sum(len(v) for v in kw_all.values())

        # Filter out previously searched keywords
        used_kw_file = DATA_DIR / "used_keywords.json"
        used_kws = json.loads(used_kw_file.read_text()) if used_kw_file.exists() else {}
        used_set = set(used_kws.get(vertical, []))
        for v_key in kw_all:
            before = len(kw_all[v_key])
            kw_all[v_key] = [kw for kw in kw_all[v_key] if kw not in used_set]
            skipped = before - len(kw_all[v_key])
            if skipped:
                print(f"    {kw_count} generated, {skipped} already searched → {len(kw_all[v_key])} new")
            else:
                print(f"    {kw_count} keywords (all new)")

        # Trim for sample mode
        if sample_size:
            kw_all = {v: kws[:sample_size] for v, kws in kw_all.items()}

        # ── Phase 2a: Google ──
        print(f"  Phase 2a: Google Ads scan...")
        google_failed = False
        try:
            google_results = await scan_google_ads(kw_all, progress=False)
            save_google_results(google_results)
            g_total = sum(len(ads) for ads in google_results.values())
            if g_total == 0:
                print(f"    WARNING: 0 results — DataForSEO may have failed")
                google_failed = True
            else:
                print(f"    {g_total} paid ads")
        except Exception as e:
            print(f"    ERROR: Google scan failed — {e}")
            google_results = {vertical: []}
            google_failed = True

        # ── Phase 2b: Meta ──
        print(f"  Phase 2b: Meta Ad Library scan...")
        max_kw = sample_size or 50
        meta_results = await scan_meta_ads(kw_all, progress=False, max_keywords_per_vertical=max_kw)
        meta_results = await resolve_missing_domains(meta_results, progress=False)
        save_meta_results(meta_results)
        m_total = sum(len(ads) for ads in meta_results.values())
        print(f"    {m_total} Meta ads")

        # Save used keywords so future runs skip them
        used_kws = json.loads(used_kw_file.read_text()) if used_kw_file.exists() else {}
        for v_key, kws in kw_all.items():
            existing = set(used_kws.get(v_key, []))
            existing.update(kws)
            used_kws[v_key] = sorted(existing)
        used_kw_file.write_text(json.dumps(used_kws, indent=2))

        # ── Phase 3: Score ──
        print(f"  Phase 3: Merge & Score...")
        scored = score_businesses(google_results, meta_results)
        save_scored(scored)
        tiers = Counter(b["tier"] for b in scored)
        print(f"    {len(scored)} businesses (Hot: {tiers['hot']} | Warm: {tiers['warm']} | Cold: {tiers['cold']})")

        # ── Phase 3.7: HITL Review (optional) ──
        if not no_review and scored:
            from review import review_batches
            print(f"  Phase 3.7: HITL Review...")
            approved = review_batches(scored, batch_size=20)
            if len(approved) < len(scored):
                scored = approved
                save_scored(scored)
                print(f"    Proceeding with {len(scored)} approved")

        # ── Phase 4: Contacts ──
        print(f"  Phase 4: Contact extraction...")
        contacts = await extract_contacts(scored, progress=False)
        save_contacts(contacts)
        phones = sum(1 for c in contacts if c.get("phone"))
        emails = sum(1 for c in contacts if c.get("email"))
        dm = sum(1 for c in contacts if c.get("decision_maker_full_name"))
        print(f"    Phone: {phones} | Email: {emails} | DM: {dm}")

        # ── Phase 4.5: Dedup ──
        print(f"  Phase 4.5: Dedup...")
        deduped = deduplicate(contacts)
        # Add note if Google data was missing
        if google_failed:
            for b in deduped:
                b["notes"] = (b.get("notes", "") + " [Google scan failed — Meta only]").strip()
        save_deduped(deduped)
        print(f"    {len(contacts)} → {len(deduped)}")

        # ── Phase 5: Export tab ──
        if output_format == "sheets" and spreadsheet:
            print(f"  Phase 5: Exporting to Sheets tab '{display}'...")
            try:
                # Re-open to avoid stale auth
                spreadsheet = open_spreadsheet(sheet_url)
                add_vertical_tab(spreadsheet, vertical, deduped)
                print(f"    Tab added: {display} ({len(deduped)} rows)")
            except Exception as e:
                print(f"    Sheets tab failed ({e}), saving CSV instead...")
                csv_path = export_to_csv(deduped, OUTPUT_DIR / f"sg_ad_intel_{vertical}.csv")
                print(f"    CSV: {csv_path}")
        else:
            csv_path = export_to_csv(deduped, OUTPUT_DIR / f"sg_ad_intel_{vertical}.csv")
            print(f"  Phase 5: CSV exported: {csv_path}")

        print(f"  {display} complete.\n")

    _print_header("All Verticals Complete")
    if sheet_url:
        print(f"Google Sheet: {sheet_url}")
    print(f"Data files in: {DATA_DIR}")
    print(f"Output files in: {OUTPUT_DIR}")


def main():
    parser = argparse.ArgumentParser(description="Singapore Ad Intelligence Pipeline")
    parser.add_argument(
        "--phase", "-p",
        default="all",
        help="Phase(s) to run: all, keywords, google, meta, score, evaluate, deep-dive, review, contacts, dedup, export",
    )
    parser.add_argument(
        "--verticals", "-v",
        default=None,
        help="Comma-separated verticals to process (default: all)",
    )
    parser.add_argument(
        "--output", "-o",
        default="sheets",
        choices=["sheets", "csv"],
        help="Output format (default: sheets)",
    )
    parser.add_argument(
        "--sample", "-s",
        type=int, default=None,
        help="Test mode: limit keywords per vertical (e.g., --sample 3)",
    )
    parser.add_argument(
        "--per-vertical",
        action="store_true",
        help="Run full pipeline per vertical (finish each industry end-to-end before next)",
    )
    parser.add_argument(
        "--sheet",
        default=None,
        help="Google Sheet URL to add tabs to (reuse existing sheet instead of creating new)",
    )
    parser.add_argument(
        "--no-review",
        action="store_true",
        help="Skip HITL review gate (for automated/scheduled runs)",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check API credential status and exit",
    )

    args = parser.parse_args()

    if args.check:
        _check_creds()
        return

    verticals = [v.strip() for v in args.verticals.split(",")] if args.verticals else None

    # Validate verticals
    if verticals:
        invalid = [v for v in verticals if v not in VERTICALS]
        if invalid:
            print(f"Unknown verticals: {invalid}")
            print(f"Valid: {VERTICALS}")
            sys.exit(1)

    _check_creds()

    if args.per_vertical:
        print(f"Singapore Ad Intelligence Pipeline (per-vertical mode)")
        print(f"Verticals: {verticals or 'all'}")
        print(f"Output: {args.output}")
        if args.sample:
            print(f"Sample mode: {args.sample} keywords/vertical")
        asyncio.run(run_per_vertical(verticals, args.output, args.sample, args.no_review, args.sheet))
    else:
        phases = [p.strip() for p in args.phase.split(",")]
        print(f"Singapore Ad Intelligence Pipeline")
        print(f"Phases: {phases}")
        print(f"Verticals: {verticals or 'all'}")
        print(f"Output: {args.output}")
        if args.sample:
            print(f"Sample mode: {args.sample} keywords/vertical")
        asyncio.run(run_pipeline(phases, verticals, args.output, args.sample, args.no_review))


if __name__ == "__main__":
    main()
