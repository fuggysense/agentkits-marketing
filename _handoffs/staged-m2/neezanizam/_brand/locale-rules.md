# Locale Rules — NeezaNizam (STAGED — not yet applied)

> **STAGED for operator apply.** NeezaNizam is a LIVE client (read-only to the rebuild). This file is the proposed `clients/neezanizam/_brand/locale-rules.md`. The new static image method loads it IF PRESENT. See the sibling `APPLY-NOTE.md` for what/where/why.

---

## 1. Market + language

- **Primary market:** Singapore (mid-career professionals 32–45 in a well-kept HDB flat at MOP; `_brand/buyer-profile.md:7`).
- **Register:** Singapore English; confident but never pushy — positions as "Solution Architects," not salespeople (`_brand/brand-voice.md`). Canonical CTA word is **consult** (not consultation/call/chat — locked 2026-04-25, `_brand/offer.md`).
- **Spelling:** UK.

## 2. Casting

- **Primary-variant ethnicity:** match the target avatar's ethnicity for the lead variant.
- **Cross-variant reach:** Singapore's main groups are Chinese, Malay, Indian, Eurasian — spread non-primary variants across these to broaden reach without adding a test variable.
- **Realism:** real, imperfect SG faces; reference an SG documentary/editorial photographer in `style`; negative prompt blocks AI skin sheen, warped/extra fingers, over-symmetry, plastic texture, watermark, stock-photo look.

## 3. Regulated / real documents + terms

| Term / document | What it is | Render rule |
|-----------------|-----------|-------------|
| **CPF** | Central Provident Fund; OA funds property. | Real CPF document format; figures fit the persona; never invented. |
| **HFE** | HDB Flat Eligibility letter. | Real HFE format; eligibility/grant figures plausible, never fabricated. |
| **MOP** | Minimum Occupation Period — the core trigger ("MOP has arrived or is approaching", `_brand/buyer-profile.md:11`). Urgency triggers include MOP timing (`_brand/offer.md`). | Keep MOP timing factually accurate on any image referencing it. |

- No invented stats on any document/data overlay — route numbers through `scripts/claim_gate.py`. (Note: the M1 ledger flagged a composite testimonial + an unsourced quote for this client — see `_handoffs/neezanizam-quote-flag-260611.md`; image proof cues inherit that scrutiny.)

## 4. Currency + income bands

- **Currency:** S$ with comma thousands separator.
- **Income sanity:** financially responsible HDB-at-MOP professionals; any price/equity band shown must fit that profile, not aspirational private-property pricing they'd reject as "break the bank" (`_brand/buyer-profile.md:11`).

## 5. Compliance

- **Platform (Meta):** no graphic before/after; no personal-attribute call-outs; no income/money-amount claims that breach policy.
- **Local:** property/CPF references factually accurate to current scheme rules. No fake urgency — the brand explicitly positions against pressure tactics (`_brand/brand-voice.md:16`).
- **Kill-list (HARD — from `_brand/brand-voice.md`):** never hard-sell; no generic agent language ("Let me find you your dream home", `:52`); per project memory the brand also kills smiles / upbeat-celebratory tone / "investment" / "dream home" / "break-the-bank" framing. The gut-punch must come from recognition / fear-of-regret / radical honesty, never hype.
