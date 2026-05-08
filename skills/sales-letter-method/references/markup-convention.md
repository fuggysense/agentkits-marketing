# Markup Convention

Inline bracket markup lets the copy stay render-agnostic — same file pastes into Google Docs, Notion, landing-page builders, or gets converted to HTML by a future Phase 5 layout renderer.

---

## The Markers

| Marker | Meaning | Render target (future HTML) | Semantics |
|--------|---------|---------------------------|-----------|
| `(h)word(h)` | Highlight — desire anchor | `<span class="highlight-intent">` (Gold #FFD700 bg) | Reserved for outcome/desire words only |
| `(b)word(b)` | Bold — skimmer anchor | `<strong>` | Every 2-3 sentences, catches skimmers |
| `(u)word(u)` | Underline — expert markup | `<u>` | ONLY for transactional results ("Closed in 14 Days") |
| `*word*` | Italics — aside or concession | `<em>` (native markdown) | Personal aside, concession, quiet emphasis |

**Stacking:** Use `(h,b)word(h,b)` when a phrase needs both highlight and bold. Order doesn't matter — renderer parses both.

---

## Usage Rules

### Highlight `(h)`
- **Purpose:** Anchor one word of **massive desire** per headline or major section
- **Frequency:** Maximum 1 per 200 words. Overuse kills impact
- **Target words:** Outcome nouns ("appointments," "closings," "freedom"), not verbs or adjectives
- **Anti-pattern:** Highlighting entire phrases, using for emphasis on generic words

### Bold `(b)`
- **Purpose:** Anchor skimmer attention, surface core benefits
- **Frequency:** Every 2-3 sentences in body copy, or 1-2 per short paragraph
- **Target phrases:** Numbers, outcomes, differentiators, specific claims
- **Anti-pattern:** Bolding transitions, common phrases, or random sentences

### Underline `(u)`
- **Purpose:** Mimic an expert marking up a document for the reader
- **Frequency:** Very sparingly — 3-5 per letter max
- **Target phrases:** Transactional terms only (*Approved*, *Closed in 14 Days*, *Direct Access*)
- **Anti-pattern:** Underlining for generic emphasis (bold or highlight does this better)

### Italics `*word*`
- **Purpose:** Aside, concession, quiet authority
- **Frequency:** As needed — fits naturally
- **Target phrases:** *"I've never shared this publicly before…"*, *"most won't follow through on this"*
- Uses native markdown `*word*` syntax (not bracket)

---

## Output Rules for Drafters

Both Phase 1 drafters (Hook Half + Commit Half) **must** apply markup inline as they write. Do not deliver plain text.

Example drafter output (good):

```
For (h)serious SG property agents(h) who've closed 3+ transactions this year:

You're about to see a system that books (b)8-12 qualified appointments every month(b) — (u)without cold calling, prospecting, or buying Zillow leads(u).

*I've spent 4 years building this. Most agents will never be shown it.*
```

Example output (bad — no markup):

```
For serious SG property agents who've closed 3+ transactions this year:

You're about to see a system that books 8-12 qualified appointments every month — without cold calling, prospecting, or buying Zillow leads.

I've spent 4 years building this. Most agents will never be shown it.
```

---

## Stitcher Responsibilities

Phase 2 Stitcher must:
- Preserve all markup from both drafters
- Rebalance if one half is markup-dense and the other is sparse
- Enforce frequency caps (≤ 1 highlight per 200 words, ≤ 1 bold per 2-3 sentences)
- Flag over-markup (reader sees a rainbow) as a failure mode

---

## Conversion Gate Checks

Lens B (Contract Validation) should verify:

- [ ] At least 1 `(h)` highlight in the headline
- [ ] Bold anchor frequency matches target (1 per 2-3 sentences in body)
- [ ] Underlines used only on transactional terms, not generic emphasis
- [ ] No entire sentences or paragraphs wrapped in `(b)` or `(h)`
- [ ] Italics used for asides, not shouting

---

## Future: HTML Render (Phase 5)

When/if Phase 5 is added, the renderer maps:

```
(h)word(h)    → <span class="highlight-intent">word</span>
(b)word(b)    → <strong>word</strong>
(u)word(u)    → <u>word</u>
(h,b)word(h,b) → <strong class="highlight-intent">word</strong>
*word*        → <em>word</em> (via standard markdown parser)
```

CSS shipped in `templates/sales-letter.html` (Phase 2 work, not yet in scope).

---

## Why Inline Brackets

- **Render-agnostic:** Same file works in any editor
- **Diff-friendly:** Version control sees clean text changes, not HTML churn
- **Reviewer-friendly:** Human reviewers read markup without HTML noise
- **Future-proof:** Any renderer (HTML, PDF, print) can parse brackets

Trade-off: brackets appear as visible text in plain-view modes. That's acceptable — production always runs through the renderer.
