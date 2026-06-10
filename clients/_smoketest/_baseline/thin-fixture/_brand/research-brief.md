# Research Brief — THIN FIXTURE (deliberately under-researched)

> **TEST FIXTURE — not a client.** This root is built to FAIL the research gate. It carries a
> valid brief but almost no research behind it: 2 VOC quotes, an empty buyer-language template,
> no competitor doc, no market doc, no gap analysis. The niche is a non-property dummy so no
> research-vault dossier matches and the FAILs are deterministic. Used by the gate's regression
> test to prove FAIL produces an actionable scorecard. Do not fix it.

```yaml
research_brief:
  # Deliberately a niche with NO matching research-vault dossier, so the test isolates to this
  # thin client folder and the FAILs are deterministic regardless of the operator's vault.
  niche: "thinfixture widget demo"
  floor_profile: ferres-default

  required_sources:
    - id: voice_of_customer
      match: ["voc", "reddit", "review", "forum", "comment", "quote"]
    - id: competitor_intel
      match: ["competitor", "competitive-landscape", "swipe"]
    - id: market_context
      match: ["market-stats", "trend"]
    - id: client_assets
      match: ["offer", "onboarding", "landing"]

  min_verbatim_phrases: 20

  required_artifacts:
    - id: icp_equivalent
      what: "Buyer-language dossier"
      resolves_to:
        - "00_inputs/research/voc-*.md"
        - "00_inputs/market/buyer-language.md"
    - id: competitor_doc
      what: "Competitor analysis"
      resolves_to:
        - "00_inputs/research/competitor-*.md"
        - "00_inputs/market/competitors/competitor-index.md"
    - id: market_doc
      what: "Market research"
      resolves_to:
        - "00_inputs/research/market-*.md"
    - id: gap_analysis
      what: "Gap analysis"
      resolves_to:
        - "00_inputs/research/*gap*.md"

  compliance_constraints:
    - id: claims_have_sources
      note: "Enforced by scripts/claim_gate.py --gate."
    - id: platform_policy
      note: "No CEA-agent implication, no guaranteed-appreciation claims."

  thin_data_fallback:
    - step: reuse_existing_research
    - step: lean_on_competitors
    - step: quick_brief_shortcut
    - step: rerun_with_more_context
    - step: operator_override

  human_read_through:
    required: true
    record_in: "00_inputs/research/README.md"
```

Note the `research-vault:` resolution path is intentionally OMITTED from every artifact so the
fixture can't accidentally pass by borrowing the operator's sg-property dossiers. This isolates
the test to the (thin) client folder.
