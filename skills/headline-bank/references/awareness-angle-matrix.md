# Awareness × Angle Matrix — which angle banks fit which awareness levels

> Eugene Schwartz's 5 awareness levels × the 10 angle banks from the headline-bank skill. The grid tells you which angles hit hardest at which awareness level, and which combinations to AVOID.

## The matrix

| Angle ↓ / Awareness → | Most Aware | Product Aware | Solution Aware | Problem Aware | Completely Unaware |
|---|---|---|---|---|---|
| 1. Problem → Agitation → Relief | — | — | ◐ | ★★★ | ★ |
| 2. Identity-Based | ◐ | ★ | ★★ | ★★ | ★★ |
| 3. Contrarian / Against the Grain | — | ◐ | ★★★ | ★★ | ★★ |
| 4. Shortcut / How to X Without Y | — | ★ | ★★ | ★★★ | ★ |
| 5. Social Proof / Bandwagon | ★★★ | ★★ | ★ | — | — |
| 6. Comparison / Us vs Them | ★★ | ★★★ | ★★ | — | — |
| 7. Transformation / Before & After | ★ | ★ | ★★ | ★★★ | ★ |
| 8. Urgency / Scarcity / FOMO | ★★★ | ★★ | ★ | — | — |
| 9. Authority / Proof-Driven | ★★★ | ★★★ | ★★ | ★ | — |
| 10. Lifestyle / Aspiration | ★ | ★ | ★★ | ★ | ★★★ |

Legend: `★★★` = primary (generate many here) · `★★` = strong · `★` = viable with care · `◐` = only if an excellent angle idea lands · `—` = avoid, the mismatch costs CPA

---

## Why each combination works (or doesn't)

### Most Aware — buyer already wants this brand/product, needs closing pressure

**Best angles:**
- **Social Proof / Bandwagon** — "12,000+ customers already trust X" — herd logic closes the final gap
- **Authority / Proof-Driven** — specific credentials, recognisable names, hard numbers
- **Urgency / Scarcity / FOMO** — expiring stock, expiring bonus, price rising

**Avoid:**
- Problem → Agitation (they're past the problem stage; this sounds remedial)
- Shortcut (they already know the path)
- Contrarian (they're already converted; contrarian creates unnecessary doubt)

### Product Aware — buyer knows the brand/category exists, needs differentiation

**Best angles:**
- **Comparison / Us vs Them** — explicit side-by-side logic against category alternatives
- **Authority / Proof-Driven** — credentials and data
- **Social Proof / Bandwagon** — specific named customers, testimonials

**Avoid:**
- Problem → Agitation (they already accept the problem exists)
- Completely-unaware curiosity framings (too upstream)

### Solution Aware — buyer knows the category solution exists, needs proof yours is different

**Best angles:**
- **Contrarian** — "Not all X are created equal" — repositions the category
- **Shortcut / How to X Without Y** — removes objection that category = hassle
- **Transformation** — "From X to Y" — shows the outcome path
- **Identity-Based** — "For the X who Y" — tribal framing

### Problem Aware — buyer knows they have a problem, doesn't know solution exists yet

**Best angles (★★★):**
- **Problem → Agitation → Relief** — name the pain exactly, then promise relief
- **Transformation** — "From X to Y" — shows them the bridge
- **Shortcut / How to X Without Y** — removes the friction they assume is mandatory

**Strong angles (★★):**
- **Identity-Based** — peer framing ("If you're the one who…")
- **Contrarian** — contradicts the belief keeping them stuck

**Avoid:** Social Proof, Urgency (they don't yet believe a solution exists — proof feels premature)

### Completely Unaware — buyer doesn't know they have the problem OR that a solution exists

**Best angles:**
- **Lifestyle / Aspiration** — paint the desired state and let them recognise the gap
- **Identity-Based (with curiosity framing)** — "If you're the one who X, you'll want to know Y"
- **Contrarian** — intrigue + pattern-interrupt

**Avoid:** Social Proof, Authority, Urgency, Comparison (all require baseline awareness that doesn't exist yet)

---

## How the headline-bank skill uses this matrix

For each of the 5 awareness levels, generate **3 angle clusters** (the top 3 `★★★` + `★★` cells per row above). Within each cluster generate 5+ headlines (total ≥15 per awareness level, ≥75 across the bank).

### Example allocation for Problem Aware:
- Cluster 1 — **Problem → Agitation → Relief** (★★★): 7-9 headlines
- Cluster 2 — **Transformation** (★★★): 5-7 headlines
- Cluster 3 — **Shortcut** (★★★): 5-7 headlines
- Optional cluster — **Identity-Based** (★★): 3-5 headlines
- Optional cluster — **Contrarian** (★★): 3-5 headlines

### Example allocation for Most Aware:
- Cluster 1 — **Social Proof / Bandwagon** (★★★): 5-7 headlines
- Cluster 2 — **Urgency / Scarcity / FOMO** (★★★): 5-7 headlines
- Cluster 3 — **Authority / Proof-Driven** (★★★): 5-7 headlines
- Optional cluster — **Comparison** (★★): 3-5 headlines

---

## How ad-concept-engine reads this matrix

When Phase 2a selects the 2 Meta headlines for a batch:
1. Check the batch's `market_awareness` field
2. Go to the bank's corresponding awareness-level section
3. Prefer headlines from the `★★★` angle clusters first
4. Filter by the batch's specific `angle` field (e.g. "The 3-Number Test" = Contrarian + Specificity; "Had a Bad Agent" = Identity-Based + Contrarian)
5. Pick the top 2 that pass anti-slop + brand-voice
6. If no match exists in the bank for the batch's awareness level, fall back to the hooks in `clients/<project>/angles/wave-<N>.md`
