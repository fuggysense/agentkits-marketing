# Benchmarks Registry — Per-Vertical Industry Benchmarks

Consumed by the scoring rubric (`page-layouts.md`) and the Calculator Close math in `generate_pdf.py`. This is the **only** place per-vertical numbers should live. The Python script itself is vertical-agnostic.

**How to use:** The orchestrator reads `clients/<project>/context-profile.json → business_context.vertical` and looks up the matching entry below. If no match → use `default` and flag the Calculator Close as "estimated — precise benchmark pending".

**How to extend:** When onboarding a client in a new vertical, append a new YAML entry to this file. Zero Python changes required. Update the `notes` field with your source.

---

```yaml
verticals:

  sg_property:
    display_name: "Singapore Property (HDB + private)"
    ctr_benchmark_percent: 1.8
    cpl_benchmark_usd: 45
    lp_conversion_benchmark_percent: 4.0
    monthly_budget_floor_usd: 3000
    net_margin_assumption: 0.40
    notes: |
      Source: internal observation from Meta Ad Library scans of SG property
      ads (260406 NeezaNizam swipe file scan). Benchmark based on top-quartile
      SG property ads that have been running 3+ months. Update quarterly from
      Ad Library data.

  sg_property_malay_muslim:
    display_name: "Singapore Property — Malay-Muslim segment"
    ctr_benchmark_percent: 2.1
    cpl_benchmark_usd: 42
    lp_conversion_benchmark_percent: 4.5
    monthly_budget_floor_usd: 3000
    net_margin_assumption: 0.42
    notes: |
      Sub-vertical of sg_property. Slightly higher benchmarks because the
      segment has less ad saturation (blue ocean for Islamic-financing-friendly
      angles). Derived from NeezaNizam campaign observations 260406-260411.

  saas_b2b:
    display_name: "SaaS (B2B)"
    ctr_benchmark_percent: 0.9
    cpl_benchmark_usd: 120
    lp_conversion_benchmark_percent: 2.5
    monthly_budget_floor_usd: 5000
    net_margin_assumption: 0.75
    notes: |
      Sourced from WordStream 2026 B2B SaaS benchmarks. Higher CPL reflects
      longer sales cycles. Net margin is high because software delivery cost
      is low. Update when WordStream publishes next annual report.

  saas_b2c:
    display_name: "SaaS (B2C / consumer subscription)"
    ctr_benchmark_percent: 1.4
    cpl_benchmark_usd: 35
    lp_conversion_benchmark_percent: 3.2
    monthly_budget_floor_usd: 3000
    net_margin_assumption: 0.65
    notes: |
      Consumer SaaS — lower CPL, shorter decision cycle than B2B. Benchmarks
      from Triple Whale + Databox 2026 reports.

  ecommerce_dtc:
    display_name: "E-commerce (DTC)"
    ctr_benchmark_percent: 1.2
    roas_benchmark: 2.8
    lp_conversion_benchmark_percent: 3.5
    monthly_budget_floor_usd: 2000
    net_margin_assumption: 0.35
    notes: |
      Sourced from Triple Whale 2026 DTC benchmarks. ROAS is the primary
      metric (not CPL). Net margin is lower due to physical product costs.

  local_service:
    display_name: "Local Service (home services, trades, healthcare clinics)"
    ctr_benchmark_percent: 2.2
    cpl_benchmark_usd: 35
    lp_conversion_benchmark_percent: 5.5
    monthly_budget_floor_usd: 1500
    net_margin_assumption: 0.50
    notes: |
      Local service ads tend to have higher CTR due to specific geo intent.
      Source: WordStream local services benchmarks.

  info_products:
    display_name: "Info Products / Courses / Coaching"
    ctr_benchmark_percent: 1.5
    cpl_benchmark_usd: 25
    lp_conversion_benchmark_percent: 4.8
    monthly_budget_floor_usd: 2000
    net_margin_assumption: 0.80
    notes: |
      High net margin because digital delivery. Benchmarks from Ramit Sethi's
      IWT transparency reports and Hormozi's $100M Leads data.

  real_estate_us:
    display_name: "Real Estate (US agents + brokers)"
    ctr_benchmark_percent: 1.6
    cpl_benchmark_usd: 55
    lp_conversion_benchmark_percent: 3.8
    monthly_budget_floor_usd: 2500
    net_margin_assumption: 0.45
    notes: |
      US real estate agent benchmarks. Different from sg_property due to
      commission structure and market dynamics.

  healthcare:
    display_name: "Healthcare (clinics, dental, elective)"
    ctr_benchmark_percent: 1.9
    cpl_benchmark_usd: 48
    lp_conversion_benchmark_percent: 4.2
    monthly_budget_floor_usd: 2500
    net_margin_assumption: 0.55
    notes: |
      Healthcare ads have regulatory constraints (HIPAA in US, PDPA in SG).
      Benchmarks exclude pharma (different category entirely).

  agency:
    display_name: "Marketing / Consulting Agency"
    ctr_benchmark_percent: 1.1
    cpl_benchmark_usd: 85
    lp_conversion_benchmark_percent: 2.8
    monthly_budget_floor_usd: 2000
    net_margin_assumption: 0.60
    notes: |
      Agency-to-agency marketing — longer sales cycle, relationship-driven.

  default:
    display_name: "Default (vertical unknown)"
    ctr_benchmark_percent: 1.0
    cpl_benchmark_usd: 75
    lp_conversion_benchmark_percent: 2.5
    monthly_budget_floor_usd: 2500
    net_margin_assumption: 0.40
    notes: |
      Conservative defaults for clients in verticals not yet in the registry.
      When used, the orchestrator MUST flag the Calculator Close as "estimated
      — precise benchmark pending" in the PDF. Add a new vertical entry as
      soon as the client's actual industry data is known.
```

---

## Calculator Close Formula

```
monthly_cost_of_constraint = current_monthly_spend
                           × (benchmark_metric / current_metric - 1)
                           × net_margin_assumption

annual_ignorance_tax = monthly_cost_of_constraint × 12
```

**When `current_metric` is unknown:** Use `monthly_budget_floor_usd` as the implied floor and compute opportunity cost of not hitting benchmark.

**When `benchmark_metric` is unknown:** Don't render the Calculator Close on page 1. Replace with a qualitative constraint rationale. Flag this as a limitation in the PDF.

## Adding a new vertical

1. Append a new YAML entry at the top of the `verticals:` block (keep `default` last)
2. Fill in all 5 numeric fields + `display_name` + `notes` with source
3. Add a `-YYMMDD` date stamp to `notes` so freshness is traceable
4. Commit the change with a descriptive message (`feat(benchmarks): add <vertical>`)
5. Test by running `generate_pdf.py` against a sample JSON using the new vertical

## Update cadence

- Quarterly review of existing verticals (check if WordStream / Triple Whale / Databox have published newer benchmarks)
- Ad-hoc updates when internal client data proves a benchmark is materially wrong
- Never edit `default` without updating every "flag as estimated" note in the code
