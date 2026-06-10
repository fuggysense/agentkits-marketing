# Specificity Audit — Post-Write Reviewer (sub-agent)

**Source:** Phase B anti-hallucination layer. Complements cai #38 Specificity proof type (proof-density-audit.md) — this reviewer focuses narrowly on weasel-word → concrete-number substitutions.

**Core principle:** Weasel words are specificity leaks. If the client's grounding files contain a concrete number that applies, the draft MUST use it. "Most couples consider upgrading" fails when research says "67% of HDB upgraders aged 32–42 begin researching within 6 months of their first child." Round numbers ("10x", "2x", "thousands") are equally suspect — push to exact. Precision implies measurement. Measurement implies truth.

**Agent model:** Sub-agent. Receives the draft + any available combination of: `clients/<slug>/context-profile.json`, `clients/<slug>/source-of-truth.md` (§5, §7.5), `clients/<slug>/research/*.md`.

---

## Weasel-Word Reference List (40+ terms)

The following terms are automatically flagged in Step 2. Any match triggers a cross-reference against the number index built in Step 1.

**Quantifier weasels:** most, many, some, several, numerous, a handful of, a number of, a lot of, lots of, plenty of, countless, various, multiple, a few, a couple of, a range of, a variety of, a host of

**Frequency weasels:** often, usually, typically, frequently, regularly, generally, commonly, sometimes, occasionally, largely, broadly, mostly

**Magnitude weasels:** significantly, considerably, substantially, dramatically, massively, hugely, greatly, markedly, noticeably, vastly

**Vague cost/value weasels:** affordable, cheap, inexpensive, a fraction of, way less than, much cheaper, cost-effective, budget-friendly, reasonably priced

**Vague outcome weasels:** better results, improved performance, significant improvement, real difference, huge difference, meaningful change, noticeable impact, positive outcome

**Vague time weasels:** quickly, soon, fast, rapidly, in no time, before long, in a short time, almost immediately, within a reasonable timeframe

**Superlative weasels:** best-in-class, top-tier, leading, world-class, industry-leading, premier, superior, unmatched

---

## What Counts as a Specificity Leak

- Weasel quantifiers from the list above used inside factual or outcome claims
- Round multipliers ("10x faster", "2x more") with no anchor number anywhere nearby
- Vague timelines ("quickly", "soon") in process or outcome claims
- Vague costs ("affordable", "a fraction of") where pricing data exists in context-profile.json
- Vague outcomes ("better results") where research holds a percentage, count, or dollar figure
- Generic superlatives ("industry-leading") without a number, rank, or benchmark
- Plural social references masking count ("clients tell us", "buyers often say") — how many, exactly?

## What Does NOT Count

- **Emotional intensifiers with no factual claim attached** — "incredibly frustrating", "deeply exhausting". No number applies. Leave alone.
- **Deliberately hedged legal-sensitive copy** — where the operator has explicitly requested non-committal language ("may help support", "results may vary"). Flag LOW only; do not block.
- **Rhetorical flourishes in closing sentences** — "the best decision you'll make this year" is a persuasive closer, not a factual claim. Leave alone unless a number genuinely strengthens the line.

---

## Severity Rules

| Severity | Condition | Action |
|----------|-----------|--------|
| **CRITICAL** | Vague claim in a headline, hero sentence, or CTA — and grounding files contain the exact number | Auto-block. Draft cannot proceed. |
| **HIGH** | Vague claim in body copy — and grounding files contain the exact number | Block. Demand specific rewrite before passing. |
| **MEDIUM** | Round multiplier without anchor — grounding files support a more specific figure | Flag. Recommend rewrite. Does not auto-block if isolated. |
| **LOW** | Weasel word used where research genuinely lacks a supporting number | Note only. May allow. |

---

## Procedure

### Step 1 — Build the number index

Extract every quantifiable data point from:
- `clients/<slug>/context-profile.json` — MRR, customer count, pricing tiers, retention rate, founding year, team size
- `clients/<slug>/source-of-truth.md` §5 (market stats) and §7.5 (misconceptions)
- `clients/<slug>/research/*.md` — any percentage, count, dollar figure, timeframe, ranking

Store as a flat list: `number | unit | context / source`. This becomes the lookup table for Steps 2–4.

### Step 2 — Scan draft for weasel-word matches

Run the full 40+ term list (Weasel-Word Reference List, above) against the draft line by line. For each hit record: line number, matched term, surrounding sentence, copy zone (headline / hero / body / CTA).

### Step 3 — Cross-reference each hit against the number index

For each weasel hit: does the index contain a number applicable to this claim? If yes → severity HIGH or CRITICAL (determined by copy zone). If no → severity LOW.

### Step 4 — Flag round-multiplier patterns separately

Search the draft for these patterns: `\d+x`, "double", "triple", "half", "twice as", "ten times". For each match: is there an anchor number in the surrounding two sentences? If not, check the index for a specific multiplier. Flag MEDIUM if the index has a better number; LOW if not.

### Step 5 — Emit per-hit records

For every flagged term produce a single line:
```
Line N | [SEVERITY] | vague phrase | available specific | recommended rewrite
```

### Step 6 — Compute density metric

Count total weasel-word hits (exclude LOW / unspecifiable). Divide by draft word count. Multiply by 1,000. This is the weasel density score used in the verdict.

---

## Output Schema

```
## SPECIFICITY AUDIT
Draft word count: N
Weasel-word density: X.X per 1000 words (threshold: < 4)

CRITICAL leaks (headline / hero / CTA zone + number available):
1. Line N | "[vague phrase in context]" | Available: [number + source] | Rewrite: "[proposed copy]"
...

HIGH leaks (body copy + number available):
1. Line N | "[vague phrase]" | Available: [number + source] | Rewrite: "[proposed copy]"
...

MEDIUM leaks (round multipliers without anchor):
1. Line N | "[e.g. '10x faster']" | Available: [specific from index, or none] | Rewrite: "[proposed copy]"
...

LOW / unspecifiable hedges (no source number — may allow):
1. Line N | "[phrase]" | No number in research — genuinely unquantifiable | Status: ALLOW / REVIEW
...

Verdict: PASS (zero CRITICAL, ≤1 HIGH, density < 4/1000) / FAIL

Reason (if FAIL): [CRITICAL present | >1 HIGH | density ≥ 4/1000 — state which triggered]
```

---

## Failure Thresholds

- **Any CRITICAL** → auto-FAIL regardless of all other scores
- **More than 1 HIGH** → FAIL
- **Weasel density ≥ 4 per 1,000 words** → FAIL

All three thresholds must clear simultaneously for a PASS.

---

## The Four Cheap Wins to Check First

1. **Grep "most" and "many"** — highest-frequency weasels in sales copy. Typically 3–5 hits per letter. Start here before touching anything else.
2. **Grep "often", "usually", "typically"** — frequency weasels. Swap to "X in Y clients" or "N% of buyers" wherever the number index has a figure.
3. **Check headlines and CTAs first** — CRITICAL severity zone. One vague headline with a better number sitting in research = auto-FAIL. Clear these before touching body copy.
4. **Grep "a lot of"** — almost never defensible. Research nearly always yields a count, percentage, or dollar figure. Replace every instance without exception.

---

## Logging

Append to `clients/<slug>/copy-system/quality-gates/specificity-log.md`:

`| YYMMDD-HHMM | output file | word count N | density X/1000 | CRITICAL N | HIGH N | MEDIUM N | LOW N | verdict |`

---

**File path:** `.claude/references/copywriting-os/reviewers/specificity-audit.md`
**Line count:** ~175 lines — within the 130–180 target.

> ⚠️ `Write` and `Bash` are not available in this session. Paste the block above into the file manually, or re-run in a standard Claude Code session where `Write` is enabled.
