"""Phase 3.5: Evaluator Gate — quality check before mass scrape."""

import asyncio
import json
from pathlib import Path

from config import (
    GROQ_API_KEY, GROQ_MODEL, GROQ_RPM,
    EVAL_PASS_THRESHOLD, EVAL_PASS_RATE_REQUIRED,
    DATA_DIR,
)

EVAL_PROMPT = """You are evaluating a business found through ad scanning for cold outreach suitability.

Business data:
- Name: {name}
- Domain: {domain}
- Vertical: {verticals}
- Score: {score}/10
- Google keyword appearances: {google_kw_count}
- Meta ad count: {meta_ad_count}
- Meta spend range: ${meta_spend_min}-${meta_spend_max}
- Sample ad copy: {ad_copy}
- Landing pages: {landing_pages}

Answer each question with PASS (2 points) or FAIL (1 point) and a one-line reason.

1. Is this a real business running its own ads? (Not an aggregator, directory, marketplace, or platform)
2. Does this business fit the 1UP ICP? (High-ticket service, likely 2-15 employees, Singapore-based, appointment/lead-dependent)
3. Is there enough data to personalize outreach? (Ad copy captured, landing page available, vertical identified)
4. Is the business contactable? (Has a website domain that would have contact info)
5. Is this likely a decision-maker-accessible SMB? (Not a large corp/MNC where reaching the owner is impossible)

Respond in JSON format:
{{
  "q1": {{"verdict": "PASS"|"FAIL", "reason": "..."}},
  "q2": {{"verdict": "PASS"|"FAIL", "reason": "..."}},
  "q3": {{"verdict": "PASS"|"FAIL", "reason": "..."}},
  "q4": {{"verdict": "PASS"|"FAIL", "reason": "..."}},
  "q5": {{"verdict": "PASS"|"FAIL", "reason": "..."}},
  "total_score": <number 5-10>,
  "overall": "PASS"|"MARGINAL"|"FAIL"
}}"""


async def _evaluate_single(client, business: dict) -> dict:
    """Evaluate a single business through the 5-question prompt contract."""
    prompt = EVAL_PROMPT.format(
        name=business.get("business_name", "Unknown"),
        domain=business.get("domain", ""),
        verticals=", ".join(business.get("verticals", [])),
        score=business.get("score", 0),
        google_kw_count=business.get("google_keyword_count", 0),
        meta_ad_count=business.get("meta_ad_count", 0),
        meta_spend_min=business.get("meta_spend_min", 0),
        meta_spend_max=business.get("meta_spend_max", 0),
        ad_copy=business.get("sample_ad_copy", "N/A")[:300],
        landing_pages=", ".join(business.get("landing_pages", [])[:3]),
    )

    try:
        response = await asyncio.to_thread(
            client.chat.completions.create,
            model=GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            max_tokens=500,
            response_format={"type": "json_object"},
        )

        result = json.loads(response.choices[0].message.content)
        result["business_name"] = business["business_name"]
        result["domain"] = business["domain"]
        result["verticals"] = business["verticals"]
        result["ad_score"] = business["score"]
        return result

    except Exception as e:
        return {
            "business_name": business["business_name"],
            "domain": business["domain"],
            "error": str(e),
            "total_score": 0,
            "overall": "ERROR",
        }


async def evaluate_batch(
    businesses: list[dict],
    top_n_per_vertical: int = 10,
) -> dict:
    """Run evaluator gate on top N businesses per vertical.

    Returns evaluation report with pass/fail decision.
    """
    if not GROQ_API_KEY:
        raise RuntimeError("Groq API key not set. Add GROQ_API_KEY to .env")

    from groq import Groq
    client = Groq(api_key=GROQ_API_KEY)

    # Group by vertical, take top N per vertical
    by_vertical: dict[str, list[dict]] = {}
    for b in businesses:
        for v in b.get("verticals", []):
            if v not in by_vertical:
                by_vertical[v] = []
            if len(by_vertical[v]) < top_n_per_vertical:
                by_vertical[v].append(b)

    # Evaluate all
    evaluations = []
    for vertical, vb_list in by_vertical.items():
        for biz in vb_list:
            result = await _evaluate_single(client, biz)
            result["evaluated_vertical"] = vertical
            evaluations.append(result)
            # Rate limit for Groq free tier
            await asyncio.sleep(60 / GROQ_RPM)

    # Calculate pass rates
    total = len(evaluations)
    passed = sum(1 for e in evaluations if e.get("overall") == "PASS")
    marginal = sum(1 for e in evaluations if e.get("overall") == "MARGINAL")
    failed = sum(1 for e in evaluations if e.get("overall") == "FAIL")
    errors = sum(1 for e in evaluations if e.get("overall") == "ERROR")

    pass_rate = passed / total if total > 0 else 0
    gate_passed = pass_rate >= EVAL_PASS_RATE_REQUIRED

    # Per-vertical breakdown
    vertical_stats = {}
    for v in by_vertical:
        v_evals = [e for e in evaluations if e.get("evaluated_vertical") == v]
        v_passed = sum(1 for e in v_evals if e.get("overall") == "PASS")
        vertical_stats[v] = {
            "total": len(v_evals),
            "passed": v_passed,
            "pass_rate": v_passed / len(v_evals) if v_evals else 0,
        }

    # Collect failed domains for blocklist consideration
    failed_domains = [
        e["domain"]
        for e in evaluations
        if e.get("overall") == "FAIL" and e.get("domain")
    ]

    report = {
        "gate_decision": "PASS" if gate_passed else "FAIL",
        "pass_rate": round(pass_rate, 3),
        "required_rate": EVAL_PASS_RATE_REQUIRED,
        "summary": {
            "total_evaluated": total,
            "passed": passed,
            "marginal": marginal,
            "failed": failed,
            "errors": errors,
        },
        "vertical_breakdown": vertical_stats,
        "suggested_blocklist_additions": failed_domains,
        "evaluations": evaluations,
    }

    return report


def save_evaluation(report: dict, path: Path | None = None) -> Path:
    """Save evaluation report to JSON."""
    out = path or (DATA_DIR / "evaluation_report.json")
    out.write_text(json.dumps(report, indent=2))
    return out


# ── CLI ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    from scorer import load_scored

    businesses = load_scored()
    report = asyncio.run(evaluate_batch(businesses))
    out = save_evaluation(report)

    decision = report["gate_decision"]
    rate = report["pass_rate"]
    summary = report["summary"]

    print(f"\nEvaluator Gate: {decision}")
    print(f"Pass rate: {rate:.1%} (required: {EVAL_PASS_RATE_REQUIRED:.0%})")
    print(f"  Passed: {summary['passed']}")
    print(f"  Marginal: {summary['marginal']}")
    print(f"  Failed: {summary['failed']}")
    print(f"  Errors: {summary['errors']}")

    print("\nPer vertical:")
    for v, stats in report["vertical_breakdown"].items():
        print(f"  {v}: {stats['passed']}/{stats['total']} ({stats['pass_rate']:.0%})")

    if report["suggested_blocklist_additions"]:
        print(f"\nSuggested blocklist additions: {report['suggested_blocklist_additions']}")

    print(f"\nSaved to {out}")
