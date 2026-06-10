# Quote-Provenance Flag — neezanizam "mental burden off my shoulders"

> Written 260611 by the M1.2 persona-provenance task. neezanizam is a LIVE client and READ-ONLY for this run — nothing in `clients/neezanizam/` was edited. This is a flag-and-options note for the operator. No file was changed.

## The problem

`clients/neezanizam/_brand/avatars/avatar-1.md` presents this line as a verbatim buyer quote:

> **"I want this mental burden off my shoulders."**

It sits in two spots in that file:

- Line 11 — Quick Reference table, "Primary Emotion" cell.
- Line 272 — the "Buying Emotion" section, bolded as what the buyer says ("Not: 'We want to upgrade' / But: ...").

It reads as voice-of-customer. But it has **no source**. I grepped the whole client tree for the exact phrase `mental burden off my shoulders` and the looser `burden off my shoulders`:

- Zero hits in any research input, swipe file, scrape, or transcript.
- `clients/neezanizam/_swipe/research/raw/` (the actual Reddit/Grok dumps) does not contain it.
- avatar-1.md's own "Research Sources" block only names platforms ("Perplexity / Grok / ChatGPT", compiled 2026-04-07) — no quote, no line, nothing openable.

So the phrase looks like a real buyer line but is almost certainly a synthesis artifact — invented during compilation and never said by a customer. That is the exact failure mode the new `avatar-research` Quote Provenance rule (M1.2 task 1) is built to stop.

## Where it propagated (every live artifact, grep'd read-only)

Source file:

| File | Line(s) | How it appears |
|------|---------|----------------|
| `_brand/avatars/avatar-1.md` | 11, 272 | ORIGIN — stated as the buyer's verbatim emotion |

Downstream artifacts that inherited it:

| File | Line | How it appears | Buyer-facing? |
|------|------|----------------|---------------|
| `campaigns/dashboard.html` | 222 | "Primary emotion" row, quoted verbatim in the rendered avatar card | Yes — published dashboard surface |
| `campaigns/thomson-reserve/02_creatives/gpt-image-2-260531/_pitch-source-brief.md` | 96 | "Core desire: Ease — *'I want this mental burden off my shoulders'*" — feeds image-gen pitch | Indirect — brief that drives creative |
| `campaigns/buyer-funnel/dcts/dct-10-5-5-proof-260603/dct.json` | 23 | inside `angle_rationale`, quoted as the buying emotion the angle leads with | Indirect — DCT strategy, not the ad text itself |
| `campaigns/buyer-funnel/dcts/dct-10-5-5-proof-260603/dct-tracker.json` | 32 | same `angle_rationale` text, tracker copy | Indirect |
| `campaigns/_sheet-snapshots/260603-1746-post-ad-concept-write-dct-10-5-5-proof-260603.json` | 42 | snapshot of that same rationale | No — historical snapshot |
| `campaigns/buyer-funnel/angles/_spotter-runs/wave-1/DCT1/system_prompt.txt` | 19, 280 | avatar-1.md embedded verbatim into the spotter's system prompt | Indirect — shapes generated angles |
| `campaigns/buyer-funnel/angles/_spotter-runs/wave-1/DCT3/system_prompt.txt` | 19, 280 | same, second spotter run | Indirect |
| `campaigns/buyer-funnel/angles/_spotter-runs/wave-1/DCT1/inputs.json` | 4 | avatar-1.md serialized as spotter input | Indirect |
| `campaigns/buyer-funnel/angles/_spotter-runs/wave-1/DCT3/inputs.json` | 4 | same | Indirect |
| `campaigns/buyer-funnel/_drafts/dct-260408/chatgpt-talking-head-scripts-prompt.md` | 45 | quoted in a talking-head script-generation prompt | Indirect — shapes script copy |

That is 11 files total (1 origin + 10 derived). Spread: one published dashboard, one image-gen pitch brief, four DCT/tracker/snapshot records, four spotter inputs/prompts, one script prompt.

The spotter `inputs.json` and `system_prompt.txt` matches are the avatar file copied wholesale into the run — they are not independent confirmations, they are the same unsourced line traveling downstream. Whatever angles and scripts those runs produced were seeded with an invented buyer quote.

## What I did NOT check (out of scope / not reachable read-only)

- Whether any of those spotter runs or the talking-head prompt actually produced ad copy that put the quote in front of a buyer. The rendered creatives (if any) would need a separate pass through the campaign's output/review folders.
- Whether the line is "close enough" to a real buyer sentiment to source retroactively. There ARE adjacent real quotes about decision fatigue in the raw dumps (the "Characteristic Quote" in avatar-1.md line ~295 is a different, longer line) — but none match "mental burden off my shoulders", and I did not hunt for a paraphrase that could be cited in its place. That is an operator call.

## Operator's two options

**Option A — capture a real source.** Find a genuine buyer line in `_swipe/research/raw/` (or commission a fresh VOC pull) that carries the same decision-fatigue meaning, then rewrite avatar-1.md lines 11 and 272 to use the real quote with a pointer (`path:line`). Re-propagation is optional if the meaning is unchanged, but the dashboard (line 222) and pitch brief (line 96) should be updated to match so the published surfaces quote a real buyer. Cheapest if a close real quote exists.

**Option B — reword + re-render affected assets.** Treat the line as a hypothesis. Either tag it `[HYPOTHESIS - not customer language]` in avatar-1.md (per the new avatar-research rule) and strip the quotation marks everywhere it is presented as buyer voice, or replace it with a sourced line. Then re-render the buyer-facing assets: `dashboard.html` (line 222) and the `thomson-reserve` pitch brief (line 96) at minimum. The DCT rationale, spotter prompts, and script prompt would only need re-running if the operator wants downstream copy re-derived from clean inputs — most carry the line as internal strategy notes, not as ad text, so the urgency there is lower.

Recommendation (not a decision): Option A if a real quote is within reach, because it preserves the angle that is already live in the proof wave. Option B if no real quote says this — then the line should never have been a quote, and every buyer-facing surface that quotes it is unsupported.

## Cross-reference

This flag is the real-world case that justifies the M1.2 task-1 edit to `skills/avatar-research/SKILL.md` (Quote Provenance hard rule + Phase 4 provenance gate). The rule, had it been in force at avatar-1.md compile time (2026-04-07), would have blocked the write of this line until it was sourced or tagged.
