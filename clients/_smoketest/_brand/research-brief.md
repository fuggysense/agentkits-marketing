# Research Brief — Meridian Property Advisory (smoke-test)

> **FICTIONAL SMOKE-TEST DATA** — Meridian is not a real client. This brief tunes the
> research-completeness gate for the buyer-side property-advisory niche so the smoke-test
> research pack PASSES honestly. Defaults below are the Ferres floor, adapted for SG property.

The machine reads ONLY the YAML block. Prose under the template's version
(`clients/_template/_brand/research-brief.md`) explains each knob. Builder-interview answers
for this niche are recorded after the YAML.

```yaml
# --- research-completeness contract (read by scripts/research_gate.py) ---
research_brief:
  niche: "SG buyer-side flat-fee property advisory"
  floor_profile: ferres-default

  required_sources:
    - id: voice_of_customer
      match: ["voc", "reddit", "review", "forum", "comment", "quote"]
    - id: competitor_intel
      match: ["competitor", "competitor-notes", "competitive-landscape", "swipe"]
    - id: market_context
      match: ["market", "market-stats", "trend", "category"]
    - id: client_assets
      match: ["offer", "onboarding", "winning-ad", "landing", "vsl", "transcript"]

  min_verbatim_phrases: 20

  required_artifacts:
    - id: icp_equivalent
      what: "Buyer-language dossier — the ICP-equivalent for SG property buyers"
      resolves_to:
        - "00_inputs/research/voc-*.md"
        - "00_inputs/market/buyer-language.md"
        - "_brand/buyer-profile.md"
        - "research-vault: language-map.md|fears.md|frustrations.md|desired-outcomes.md"
    - id: competitor_doc
      what: "Competitor analysis — commissioned-agent default + direct-model rivals"
      resolves_to:
        - "00_inputs/research/competitor-*.md"
        - "00_inputs/market/competitors/competitor-index.md"
        - "research-vault: competitive-landscape.md"
    - id: market_doc
      what: "Market research — SG buyer behaviour, fair-value gap, timing"
      resolves_to:
        - "00_inputs/research/market-*.md"
        - "00_inputs/market/awareness-sophistication.md"
        - "research-vault: sophistication-schwartz.md|awareness-schwartz.md"
    - id: gap_analysis
      what: "Gap analysis — what buyers say vs what the flat-fee offer answers"
      resolves_to:
        - "00_inputs/research/*gap*.md"
        - "00_inputs/market/awareness-sophistication.md"
        - "_brand/buyer-profile.md"

  compliance_constraints:
    - id: claims_have_sources
      note: "Every stat traces to a source; enforced by scripts/claim_gate.py --gate."
    - id: platform_policy
      note: "No CEA-agent implication, no guaranteed-appreciation claims, no fear-baiting the market."

  thin_data_fallback:
    - step: reuse_existing_research    # research-vault sg-property-* dossiers substitute first
    - step: lean_on_competitors
    - step: quick_brief_shortcut
    - step: rerun_with_more_context
    - step: operator_override

  human_read_through:
    required: true
    record_in: "00_inputs/research/README.md (operator notes read-through date + verdict)"
```

## Builder interview — answers for this niche

1. **Niche.** Meridian Property Advisory, a flat-fee buyer-side property advisor in Singapore;
   sells a S$4,500 end-to-end advisory, a S$290 shortlist teardown, and a free overpaying
   checklist. Buyers are fee-allergic and skeptical of anyone selling property advice.
2. **Good-enough research.** Enough VOC to show the real wound is trust ("whose side is the
   advice on"), not the fee — and competitor intel that names the commissioned-agent default
   as the true rival. Without those two, copy guesses.
3. **Where buyers talk.** Reddit (r/singaporefi, r/HDB, r/askSingapore) carries the honest
   voice; PropertyGuru reviews and Telegram groups are secondary. VOC source type stays.
4. **Verbatim floor.** 20 holds. The VOC dump already runs 27 numbered quotes, so the floor is
   comfortably met without padding.
5. **Competitors.** Three direct-model rivals plus the free commissioned agent. They run public
   IG ads and reviewable funnels, so `lean_on_competitors` is a viable fallback.
6. **Existing research.** The research-vault carries `sg-property-*` dossiers; reuse them first
   when a real campaign needs more depth than the smoke pack.
7. **Compliance landmines.** Never imply Meridian is a licensed CEA agent; never promise resale
   gains or "guaranteed" appreciation; never fear-bait the property market.
8. **Hard claims.** Market-stats numbers are fictional-but-sourced for the smoke test; the
   claim gate enforces source attribution downstream.
9. **Sign-off.** Operator records the read-through in `00_inputs/research/README.md`.
10. **Thin-data recovery.** Reuse the vault dossiers first; only then lean on competitors.
