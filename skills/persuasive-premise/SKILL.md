---
name: persuasive-premise
version: "0.1.0-skeleton"
brand: AgentKits Marketing by AityTech
category: copywriting-foundation
difficulty: advanced
description: "Generate the single belief that makes an offer inevitable (Schwartz framework). Outputs: core_belief + contrast + evidence + implication. Feeds: headline-bank, ad-concept-engine, sales-letter-method. NOT a benefit list — premises are disagreeable beliefs. Run after offer-builder."
triggers:
  - persuasive premise
  - core belief
  - one belief
  - "/copy:premise"
  - what should they believe
  - the premise
prerequisites:
  - buyer-language-researcher
  - offer-builder
related_skills:
  - marketing-psychology
  - source-of-truth
  - avatar-research
  - headline-bank
  - ad-concept-engine
  - sales-letter-method
  - unique-mechanism-problem
  - unique-mechanism-solution
agents:
  - copywriter
  - brainstormer
  - brand-voice-guardian
mcp_integrations: {}
success_metrics:
  - belief_disagreeability_check
  - evidence_specificity
  - offer_inevitability_logic
  - audience_language_match
output_schema: persuasive-premise-v1
status: skeleton-pending-calibration
---

# Persuasive Premise

You produce the **single belief** that, if the audience accepts it, makes the offer the obvious choice. You do NOT produce benefits, claims, or features. You produce a defensible belief that contradicts what the market currently holds.

**Source:** Eugene Schwartz, *Breakthrough Advertising* — "core mass desire" + the role of belief structures. See `references/canonical-sources.md` (TODO).

## Angle = problem + person + timing + proof

Keep it human. An angle is just:

`Angle = problem + person + timing + proof`

- **Problem (the barrier):** the real thing blocking them. Name it FIRST.
- **Person + awareness:** who they are, and how aware they already are of the problem and the options.
- **Timing:** what makes it matter *now* (the trigger).
- **Proof:** the evidence THIS person will actually believe.

**Example — speaking coach:** Barrier: they freeze on stage · Awareness: they know they need to speak better · Frame: "say less, land harder" · Proof: before/after clips, testimonials, speaking results.

**Example — iron supplement:** Barrier: they feel tired and foggy · Awareness: they know low energy is the problem · Frame: "steady energy without caffeine crashes" · Proof: ingredient credibility, reviews, results.

**The biggest mistake is starting with the frame before you understand the barrier.** Barrier first, frame last.

## Required Inputs
- `clients/<project>/research/buyer-language-dossier.md` — REQUIRED
- `clients/<project>/offer.md` — REQUIRED
- `clients/<project>/research/avatar.md` — REQUIRED if exists
- `voice/jerel/` or `clients/<project>/brand-voice.md` — for tone

## Hard Rules (non-negotiable)
1. A premise is a BELIEF, not a benefit, not a claim, not a feature.
2. **Disagreeability test:** can the audience reasonably disagree? If no, it's a benefit. Reject and rewrite.
3. The premise must contradict (or replace) a belief the market currently holds. State the contrast belief explicitly.
4. Must be defensible with at least 3 pieces of evidence (study, mechanism, story, data, expert authority).
5. The premise must logically lead to the offer being the obvious next step — not "an option among many."
6. One premise per output. Do not stack premises.
7. Use buyer-language verbatim where possible (pull from dossier).

## Anti-patterns (REJECT these)
- "X is the best way to Y" → claim, not belief.
- "Stop doing X" → command, not premise.
- Premise that sounds smart but doesn't connect logically to the offer.
- Premise requiring 3 sub-beliefs to be accepted first (load-bearing chain too long).
- Generic industry truisms ("most diets fail" — too vague).
- Premise the audience already holds (no work for the copy to do).

## Output Schema (`persuasive-premise-v1`)
```yaml
core_belief: <one sentence — the single belief>
contrast_belief: <what the market currently believes — explicit>
evidence:
  - <proof item 1: study/mechanism/story/data>
  - <proof item 2>
  - <proof item 3>
why_now: <urgency or relevance trigger>
implication: <what becomes true if they accept the premise — must lead to offer>
test_questions:
  disagreeable: <yes/no — must be yes>
  leads_to_offer: <yes/no — must be yes>
  has_evidence: <yes/no — must be yes>
buyer_language_used: [<list of verbatim phrases pulled from dossier>]
```

## Worked Examples
TODO — populate after Ghostwriter calibration runs land in `ghostwriteros-research/calibration/persuasive-premise/`.
Required: 3 good examples (one per market sophistication stage 2/3/4) + 2 bad examples with reasons.

## Calibration Set
TODO — 10 input/output pairs at `evals/persuasive-premise/calibration.jsonl`.
- 5 from Ghostwriter (gold benchmark to beat)
- 3 from `swipe-files/`
- 2 from `ad-library-scraper` winners

## Lock Criteria
Average ≥ 8/10 across calibration set. Beats Ghostwriter on ≥ 5/10 inputs.

## Downstream Handoff
Save output to `clients/<project>/research/persuasive-premise.md`. Cross-reference in `headline-bank`, `ad-concept-engine`, `sales-letter-method` system prompts as required input.

<!-- skill-graph:start -->

## Related
<!-- auto-generated by scripts/link-skills.py — do not edit by hand -->

- [[problem-promise]] (skill, 0.37)
- [[usp-generator]] (skill, 0.12)
- [[unique-mechanism-problem]] (skill, 0.12)

<!-- skill-graph:end -->
