# Research Brief — {{client_name}}

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
  niche: "{{niche}}"                  # e.g. "SG buyer-side property advisory", "DTC supplement"
  # Floor profile this brief inherits from. "ferres-default" = the values below as shipped.
  # Override any single knob in place; the gate uses what is written here, not the profile name.
  floor_profile: ferres-default

  # 1. REQUIRED SOURCES — the source TYPES research must draw from for this niche.
  #    The gate looks for at least one file/section matching each id across the client's
  #    research dirs and the research-vault. Drop a source the niche genuinely can't have
  #    (e.g. no public reviews for a brand-new category) and SAY WHY in source notes.
  required_sources:
    - id: voice_of_customer        # forums, reviews, comments in the buyer's own words (Reddit weighted highest)
      match: ["voc", "reddit", "review", "forum", "comment", "quote"]
    - id: competitor_intel         # competitor ads / funnels / reviews — who already paid to test
      match: ["competitor", "competitor-notes", "competitive-landscape", "swipe", "ad-library"]
    - id: market_context           # trends, stats, pain hierarchy, timing, macro
      match: ["market", "market-stats", "trend", "category"]
    - id: client_assets            # the client's own offer, winning ad, landing page, VSL transcript
      match: ["offer", "onboarding", "winning-ad", "landing", "vsl", "transcript"]

  # 2. VERBATIM PHRASE FLOOR — minimum count of pointable customer quotes.
  #    Ferres floor = 20. ESL/consumer niches usually need more raw quotes to find the
  #    register; tight B2B niches with few public voices may justify fewer (record why).
  min_verbatim_phrases: 20

  # 3. REQUIRED ARTIFACTS — the named outputs that must exist, mapped to THIS repo.
  #    Ferres ships three named docs; here they map to the repo's artifact names. The gate
  #    resolves each against the client folders AND ~/AI workflows/research-vault/markets/*.
  required_artifacts:
    - id: icp_equivalent           # Ferres "research doc 1 ICP"
      what: "Buyer-language dossier / buyer-profile psychology — the ICP-equivalent"
      # Any ONE of these satisfies it:
      resolves_to:
        - "00_inputs/research/voc-*.md"                       # client VOC dump
        - "00_inputs/market/buyer-language.md"                # filled buyer-language file
        - "_brand/buyer-profile.md"                           # built buyer profile
        - "research-vault: language-map.md|fears.md|frustrations.md|desired-outcomes.md"
    - id: competitor_doc           # Ferres "research doc 2 competitor analysis"
      what: "Competitor analysis — models, weaknesses, differentiation, language opportunities"
      resolves_to:
        - "00_inputs/research/competitor-*.md"
        - "00_inputs/market/competitors/competitor-index.md"
        - "research-vault: competitive-landscape.md"
    - id: market_doc               # Ferres "research doc 3 market"
      what: "Market research — trends, stats, pain hierarchy, urgency, timing"
      resolves_to:
        - "00_inputs/research/market-*.md"
        - "00_inputs/market/awareness-sophistication.md"
        - "research-vault: sophistication-schwartz.md|awareness-schwartz.md|trigger-events.md"
    - id: gap_analysis             # Ferres ICP-doc requirement: what customers say vs what client addresses
      what: "Gap analysis — researched buyer language vs what the offer currently answers"
      resolves_to:
        - "00_inputs/research/*gap*.md"
        - "00_inputs/market/awareness-sophistication.md"      # if it carries a gap section
        - "_brand/buyer-profile.md"                            # if it carries a gap/objection section

  # 4. COMPLIANCE CONSTRAINTS — niche guardrails the research must surface so copy honors them.
  #    These are checked as PRESENT-AND-NAMED, not enforced here (claim_gate.py enforces claims).
  compliance_constraints:
    - id: claims_have_sources      # every number a reviewer could be sued over must trace to a source
      note: "Enforced downstream by scripts/claim_gate.py --gate; named here so research carries the sources."
    - id: platform_policy          # niche-specific ad-platform landmines (income claims, health, personal attributes)
      note: "{{platform_compliance_note}}"

  # 5. THIN-DATA FALLBACK LADDER — what to do when the floor isn't met, in order.
  #    Ferres: lean on competitors, then run the quick-brief shortcut, then re-run with more
  #    context. The gate never auto-applies these — it surfaces the ladder to the operator.
  thin_data_fallback:
    - step: lean_on_competitors    # competitor old long-running ads + reviews + comments supply VOC the client lacks
    - step: reuse_existing_research # a fresh prior dossier (research-vault, <60 days) substitutes — drop it in, skip re-research
    - step: quick_brief_shortcut   # cold/spec/new-niche: paste offer/landing/notes -> quick brief, model proven winners 80/20
    - step: rerun_with_more_context # output thin -> add main-offer VSL + offer doc, re-run the deep-research prompts
    - step: operator_override      # last resort: operator records research_gate_override (with reason) in pipeline-state.json

  # 6. HUMAN SIGN-OFF — Ferres reads the docs before using them. Recorded, not auto-detected.
  human_read_through:
    required: true
    record_in: "00_inputs/research/README.md or _baseline — operator notes the read-through date + verdict"
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

## Builder interview

Answer these at onboarding to fill the YAML for a new niche. Defaults in parentheses are the
Ferres floor — keep them unless the niche gives you a reason to move them.

1. **Niche, one line.** Who is this client and what do they sell, to whom, where?
   (Sets `niche`.)
2. **What does "good-enough research" look like for THIS niche before you'd let copy ship?**
   The honest answer here is what tunes the whole floor. If you don't have one yet, keep
   `ferres-default` and revisit after the first campaign.
3. **Where do these buyers actually talk?** Reddit, Facebook groups, review sites, WhatsApp,
   in person only? (Tunes `required_sources` — drop `voice_of_customer` source types the niche
   can't supply, and say why.)
4. **How many verbatim quotes is enough to capture the register?** (Sets `min_verbatim_phrases`;
   floor 20. Raise for consumer/ESL, justify any drop for thin-voice B2B.)
5. **Who are the real competitors, and do they run public ads / leave reviewable funnels?**
   (Tunes the `competitor_doc` artifact and whether `lean_on_competitors` is a viable fallback.)
6. **Is there existing research we can reuse?** A research-vault market dossier, a prior
   week-one intel report? (Decides whether `reuse_existing_research` is the first fallback rung.)
7. **What ad-platform compliance landmines does this niche carry?** Income claims, health
   claims, personal-attribute call-outs, licensing/regulatory language? (Fills
   `platform_compliance_note` under `compliance_constraints`.)
8. **Are there hard claims (numbers, stats, prices) the ads will lean on?** Where do those
   sources live? (Confirms `claims_have_sources` is wired to `claim_gate.py`.)
9. **Who signs off on the research read-through, and where do they record it?**
   (Sets `human_read_through.record_in`.)
10. **When research comes back thin for this niche, what's the realistic recovery?** Reorder
    `thin_data_fallback` so the most viable rung for this niche is first.
