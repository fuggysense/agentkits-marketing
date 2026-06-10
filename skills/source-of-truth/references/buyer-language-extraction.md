# Buyer Language Extraction Rules

How to handle verbatim buyer quotes from the research dossier. The core principle: preserve exact wording, always attribute source, never paraphrase.

**Why this matters:** the entire point of running `buyer-language-researcher` is to inject real buyer voice into the source-of-truth. If we paraphrase into copywriter voice, we've destroyed the research value. Hooks that quote a real Reddit thread outperform hooks written in brand voice — every time.

---

## Quote Preservation Rules

### Rule 1 — Verbatim only

Preserve exact buyer wording including:
- Typos and grammatical errors (shows authenticity)
- Slang, Singlish, regional language (don't translate)
- All-caps emphasis, exclamation marks, profanity (censor only what platform policy forbids in ads)
- Incomplete sentences, fragments

**Bad:** "Many upgraders feel uncertain about affordability." (paraphrased into brand voice)
**Good:** "confirm need to break the bank one lah" (verbatim, Singlish, fragment)

### Rule 2 — Source attribution is mandatory

Every quote needs:
- **Source type** (Reddit / Instagram / TikTok / review / forum / survey / interview)
- **Source location** (subreddit, competitor handle, product page, etc.)
- **Approximate date** (month/year precision minimum)

Format: `"quote text" — r/singaporefi, 2025-12-08` or `"quote text" — IG comment on @damien.tan, 2026-02`

**Missing attribution = rejected quote.** If buyer-language-researcher returned quotes without attribution, push back and request source metadata.

### Rule 3 — Context snippet for ambiguous quotes

If a quote by itself is ambiguous, include 1 line of context in parens before the quote:

`(responding to a post about spouse disagreement) "lah you think i haven't done the math?? 3 months already my wife still says cannot"`

### Rule 4 — Minimum 2 quotes per §5 dimension

For each of the 14 §5 Buyer Profile dimensions, aim for 2-5 verbatim quotes. If fewer than 2, mark:
`⚠️ THIN DATA — only 1 verbatim example available. Consider re-running buyer-language-researcher with expanded sources.`

### Rule 5 — Never synthesise quotes

If the dossier has no quote matching a dimension, DO NOT generate a "plausible" quote. Mark that dimension as NOT AVAILABLE and move on. A fabricated quote is worse than silence — it poisons the entire doc's credibility.

---

## Quote Categorisation for Buyer Language Bank (§5)

Organise quotes into 6 buckets:

1. **Problem language** — how they describe the problem in their own words
2. **Solution attempts** — what they've tried and why it failed
3. **Frustration / tired-of language** — expressed fatigue with the status quo
4. **Desire language** — what they want instead
5. **Hesitation language** — why they delay / don't act
6. **Trigger language** — what would convince them to act

Each bucket has 3-5 verbatim quotes. These 6 buckets map directly to the Buyer Language Bank subsections in §5.

---

## Privacy & Anonymisation

### When to preserve user handle
- Public posts on public subreddits / forums → preserve (it's public data)
- Public Instagram / TikTok comments → preserve handle if public
- Public review platforms (Google reviews, Trustpilot) → preserve attribution

### When to anonymise
- Private Slack / Discord / DMs → anonymise fully, cite only as `private community member, 2026-03`
- Interview transcripts (1:1) → anonymise to `Interview #N, 2026-03`
- Customer support tickets → anonymise to `Support ticket, [category], 2026-03`
- NotebookLM corpora built from private documents → cite as `NotebookLM:corpus-name`

### Never preserve
- Full names in private contexts
- Phone numbers, email addresses
- Financial specifics that could identify an individual (e.g. "John, who earns $12K/mo at DBS")

---

## Quote Density Quality Bar

After §5 synthesis, count total verbatim quotes used in the doc. Quality tiers:

| Tier | Verbatim Quote Count | Action |
|---|---|---|
| Strong | 60+ quotes across §4-7 | ✓ proceed to Phase 4 HITL |
| Acceptable | 30-59 | ✓ proceed, flag in §26 appendix: "Research density: acceptable" |
| Thin | 10-29 | ⚠️ surface to user: "Research was thin — recommend extending buyer-language-researcher run OR manually add customer interview transcripts" |
| Unacceptable | <10 | STOP. Abort Phase 3 synthesis. Re-run buyer-language-researcher with broader source list before proceeding. |

---

## Quote Formatting in the Doc

**In §4 Audience Reality Notes:**
Use blockquote:
```markdown
> "my wife still says cannot afford but we earn 15k combined. no idea what she thinks need"
> — r/singapore, 2025-11-23
```

**In §5 Buyer Language Bank:**
Use bullet list:
```markdown
- **How they describe the problem:**
  - "[verbatim quote 1]" ([source 1])
  - "[verbatim quote 2]" ([source 2 + date])
  - "[verbatim quote 3]" ([source 3 + date])
```

**In §7 Objections:**
Put verbatim objection as first line of each objection row:
```markdown
- **Price:**
  - "2M condo you crazy ah" — r/singapore, 2026-01
  - (root cause) buyer is filtering by visible price, not TDSR-corrected affordability
  - (best answer) show the 3-number test that reveals $10K income CAN upgrade
  - (placement) hook + body
```

---

## Verbatim-to-Hook Conversion (for §11 Hook Library)

When turning a buyer quote into a hook, minimise edits:

**Buyer quote:** `"still stuck lah. 3 months already spreadsheet lists every combination already still cannot decide"`

**Hook variants:**
- ✓ Direct quote: `"Still stuck after 3 months of spreadsheets?"`
- ✓ Mirrored frame: `"When spreadsheets stop giving you an answer."`
- ✗ Rewritten in brand voice: `"Many upgraders find themselves in analysis paralysis after extended research phases."` — AI slop, zero buyer resonance

**Rule:** if you can't trace the hook back to a specific buyer quote, ask yourself "am I writing from the dossier or from my imagination?" If imagination, scrap it and try again.

---

## Language Bank Growth Over Time

The Buyer Language Bank is a LIVING asset:
- Initial version: populated from Phase 2 research only
- Over time: append new verbatim quotes from:
  - Sales call transcripts
  - Customer support tickets (with anonymisation)
  - Post-ad comment sections (Meta / TikTok)
  - Post-purchase survey responses

During `/ops:monthly`, `knowledge-hygiene` skill should flag when buyer-language-dossier is older than 60 days — recommend a refresh run of `buyer-language-researcher`.

---

## Anti-AI Slop Filter Integration

Every hook generated from buyer quotes still gets a slop-check via `skills/copy-editing/references/overused-ai-patterns.md` and (if exists) `skills/unslop/profiles/paid-ads.md`.

Common AI slop patterns that sneak in even from verbatim quotes:
- "Picture this..." (never in real buyer language)
- "Imagine if..." (usually AI-synthesised framing)
- Colon-driven structures: "X: The Y You Need" (copywriter meme, not buyer voice)
- Rhetorical triplets with no source quote to back them up

If a hook fails slop check, but WAS derived from a verbatim quote, the slop is in YOUR framing — rewrite to stay closer to the quote.

---

## Audit Trail

Every quote used in the final source-of-truth.md should be traceable back to its source file. During Phase 5 write, append a `quote-audit.json` to the research manifest:

```json
{
  "total_verbatim_quotes_used": 73,
  "by_source": {
    "reddit:r/<sub-1>": 28,
    "reddit:r/<sub-2>": 19,
    "notebooklm:<project-corpus>": 15,
    "instagram:@<competitor> comments": 8,
    "internal:buyer-profile.md": 3
  },
  "by_dimension": {
    "§4 Audience Reality": 12,
    "§5.2 Core Problem": 9,
    "§5.4 Fears": 11,
    "§5.6 Past Solutions": 8,
    "§5.14 Objections": 14,
    "§6 Pain Points": 10,
    "§7 Objections (verbatim)": 9
  },
  "flagged_thin_dimensions": [
    "§5.5 Relationship Impacts — only 2 quotes",
    "§5.12 Must Give Up — 0 quotes (marked NOT AVAILABLE)"
  ]
}
```
