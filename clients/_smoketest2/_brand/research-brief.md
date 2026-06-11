# Research Brief — VitalKit Labs (smoke-test 2)

> **FICTIONAL SMOKE-TEST DATA** — VitalKit Labs is not a real client. This brief tunes the
> research-completeness gate for the US DTC supplement niche so the smoke-test research pack
> PASSES honestly. Defaults are the Ferres floor, adapted for health/supplement DTC.

The definition of "research complete" for this client. It is the contract the
research-completeness gate checks before any avatar, angle, or ad work runs.

Defaults below are the **Ferres floor** — Sean Ferres treats research as Stage 1 of 6
and the phase the ad "lives or dies by" (four hours sharpening the axe out of six). His
done-bar: three named research docs (ICP, competitor, market), at least 20 verbatim
customer phrases in the ICP doc, a gap analysis of what customers say vs what the client
addresses, a human read-through before the docs get used, and a re-run if the output came
back thin. See `_shared-knowledge/ferres/02-research-flow.md`.

Keep the YAML block below in sync with reality. The machine reads ONLY the YAML; the prose
underneath explains each knob so a human can tune it per niche. To set the values for a new
client, answer the questions in `## Builder interview` and write the answers into the YAML.

```yaml
# --- research-completeness contract (read by scripts/research_gate.py) ---
research_brief:
  niche: "US DTC supplement starter kits — sleep/stress/energy, women 25-45"
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
      what: "Buyer-language dossier — supplement-fatigued US women, past-purchase graveyard language"
      resolves_to:
        - "00_inputs/research/voc-*.md"
        - "00_inputs/market/buyer-language.md"
        - "_brand/buyer-profile.md"
        - "research-vault: language-map.md|fears.md|frustrations.md|desired-outcomes.md"
    - id: competitor_doc
      what: "Competitor analysis — AG1/Athletic Greens model, Amazon top-sellers, Ritual/Seed subscription rivals"
      resolves_to:
        - "00_inputs/research/competitor-*.md"
        - "00_inputs/market/competitors/competitor-index.md"
        - "research-vault: competitive-landscape.md"
    - id: market_doc
      what: "Market research — supplement fatigue, subscription churn, US wellness trends, category trust gap"
      resolves_to:
        - "00_inputs/research/market-*.md"
        - "00_inputs/market/awareness-sophistication.md"
        - "research-vault: sophistication-schwartz.md|awareness-schwartz.md|trigger-events.md"
    - id: gap_analysis
      what: "Gap analysis — what buyers say about past failures vs what the starter-kit offer answers"
      resolves_to:
        - "00_inputs/research/*gap*.md"
        - "00_inputs/market/awareness-sophistication.md"
        - "_brand/buyer-profile.md"

  compliance_constraints:
    - id: claims_have_sources
      note: "Every stat traces to a source; enforced by scripts/claim_gate.py --gate."
    - id: platform_policy
      note: "No disease-treatment claims (FTC/FDA). No guaranteed outcomes. No before/after framing for supplements. No weight-loss percentages. Meta health-condition targeting prohibited — interest-only. Use 'supports' not 'treats/cures/prevents'."

  thin_data_fallback:
    - step: lean_on_competitors
    - step: reuse_existing_research
    - step: quick_brief_shortcut
    - step: rerun_with_more_context
    - step: operator_override

  human_read_through:
    required: true
    record_in: "00_inputs/research/README.md (operator notes read-through date + verdict)"
```

## Each knob, explained

**`niche` / `floor_profile`** — the niche label drives every other default. `ferres-default`
ships the values above. To start from the floor and tune one number, leave the profile name
and just edit the YAML in place; the gate reads the written values, never the profile name.

**`required_sources`** — the source *types* Ferres mines: voice-of-customer (he weights Reddit
highest — "where people are the most brutally honest"), competitor intel (read the OLDEST ads
first; still running 3-6 months later means profitable), market context (trends, stats, timing),
and the client's own assets (offer, winning ad, landing page, VSL). The `match` lists are the
filename/keyword hints the gate greps for. If a niche genuinely can't supply one source type,
delete that entry and write the reason in the source notes — don't leave it failing silently.

**`min_verbatim_phrases`** — the Ferres floor is 20 pointable customer quotes in the ICP doc.
The bar is "feel like you read their mind" — verbatim phrasing, not paraphrase. Consumer/ESL
niches usually want more raw quotes to find the register; a narrow B2B niche with few public
voices may justify a lower number, but record the justification.

**`required_artifacts`** — Ferres ships three named PDFs (ICP, competitor, market). Here they
map to the repo's real artifact names. Each artifact `resolves_to` a list of paths; the gate
passes the artifact if ANY path resolves (in the client folders OR the research-vault). The
`research-vault:` prefix means "any of these aspect files inside the matched market dossier."
`gap_analysis` is the fourth: Ferres bakes "what customers say vs what the client addresses"
into the ICP doc — here it's its own checkable artifact.

**`compliance_constraints`** — niche guardrails the research must surface (so copy honors them).
The gate checks these are NAMED here, not that they're enforced — claim enforcement is
`claim_gate.py`'s job. `platform_policy` is where you write the niche's ad-platform landmines
(no income claims for money niches, no personal-attribute call-outs for health/weight, etc.).

**`thin_data_fallback`** — the recovery ladder when the floor isn't met, in Ferres's order:
lean on competitors -> reuse existing fresh research -> quick-brief shortcut for cold/spec ->
re-run with more context -> operator override. The gate never auto-applies a fallback. It
surfaces the ladder so the operator picks the right rung instead of generating from thin air.

**`human_read_through`** — Ferres actually reads the research before using it, and re-ran the
deep-research prompts the time output came back thin. This is a human gate, recorded by the
operator (read-through date + verdict), not auto-detected by the machine.

## Builder interview — answers for this niche

1. **Niche.** VitalKit Labs, a US DTC brand selling curated supplement starter kits in three
   categories (sleep, stress, energy); core offer is a $49 single-category sampler and a
   $129/mo Foundation Stack subscription. Buyers are women 25-45 who have already tried multiple
   supplements with mixed results and are frustrated by decision fatigue and wasted money.
2. **Good-enough research.** Enough VOC to surface the "supplement graveyard" pattern — the
   specific language buyers use about past failures — plus competitor intel naming the
   AG1-style all-in-one vs the category-specific kit as the real choice architecture.
3. **Where buyers talk.** Reddit (r/supplements, r/sleep, r/nootropics, r/xxfitness). Amazon
   reviews for top-selling sleep/stress supplements. TikTok wellness skepticism discourse.
   VOC source type stays.
4. **Verbatim floor.** 20 holds. The VOC dump carries 25+ numbered quotes.
5. **Competitors.** AG1/Athletic Greens, Amazon private-label magnesium/ashwagandha, Ritual,
   Seed. All run public Meta/TikTok ads, so lean_on_competitors is viable.
6. **Existing research.** No research-vault dossier for this niche yet. Lean on competitors first.
7. **Compliance landmines.** FTC/FDA: never use "treats," "cures," "prevents" for any condition.
   No guaranteed outcomes. No weight-loss percentages. Meta health-condition targeting prohibited.
8. **Hard claims.** Market-stats numbers are fictional-but-sourced for this smoke test; claim
   gate enforces source attribution downstream.
9. **Sign-off.** Operator records read-through in `00_inputs/research/README.md`.
10. **Thin-data recovery.** Lean on competitors first (AG1/Ritual/Amazon reviews supply dense VOC);
    then reuse any research-vault wellness dossier if one exists.
