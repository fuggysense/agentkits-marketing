# Locale Rules — Eugene Chieng (STAGED — not yet applied)

> **STAGED for operator apply.** Eugene is a LIVE client (read-only to the rebuild). This file is the proposed `clients/eugene-chieng/_brand/locale-rules.md`. The new static image method loads it IF PRESENT. See the sibling `APPLY-NOTE.md` for what/where/why.

---

## 1. Market + language

- **Primary market:** Singapore (HDB owners / upgraders, 25–54, MOPed or 4+ years in current home; `_brand/buyer-profile.md:6`).
- **Register:** Singapore English; ~60% formal, contractions but never slang (`_brand/brand-voice.md`). Numbers-literate, decision-fatigued — lead with the long-arc framing, not urgency.
- **Spelling:** UK.

## 2. Casting

- **Primary-variant ethnicity:** match the target avatar's ethnicity for the lead variant.
- **Cross-variant reach:** Singapore's main groups are Chinese, Malay, Indian, Eurasian — spread non-primary variants across these to broaden reach without adding a test variable.
- **Realism:** real, imperfect SG faces; reference an SG documentary/editorial photographer in `style`; negative prompt blocks AI skin sheen, warped/extra fingers, over-symmetry, plastic texture, watermark, stock-photo look.

## 3. Regulated / real documents + terms

| Term / document | What it is | Render rule |
|-----------------|-----------|-------------|
| **CPF** | Central Provident Fund; OA funds property; equity often "locked in a flat" (`_brand/buyer-profile.md:12`). | Real CPF document format; figures fit the persona's profile; never invented. |
| **HFE** | HDB Flat Eligibility letter. | Real HFE format; eligibility/grant figures plausible, never fabricated. |
| **MOP** | Minimum Occupation Period — the upgrade trigger ("MOP just hit", `_brand/buyer-profile.md:12`). | If referenced on-image, keep timing factually accurate. |

- No invented stats on any document/data overlay — route numbers through `scripts/claim_gate.py`.

## 4. Currency + income bands

- **Currency:** S$ with comma thousands separator.
- **Income sanity:** "cash-light" upgraders (`_brand/buyer-profile.md:7`) — any price/equity band shown must fit that reality; don't show a band they'd never see.

## 5. Compliance

- **Platform (Meta):** no graphic before/after; no personal-attribute call-outs; no income/money-amount claims that breach policy.
- **Local:** long-arc framing; AVOID "buy now before prices go up" (`_brand/brand-voice.md:15`). Property/CPF references factually accurate to current scheme rules.
- **Kill-list (HARD — from `_brand/brand-voice.md:18`):** banned words — "dream home", "hot property", "must-buy", "once-in-a-lifetime", "limited units", "act now", "don't miss out", "game-changer", "synergy", "leverage", "unlock". First-person "I" (Eugene) + "you"; never third-person. The gut-punch must come from recognition + the right-move-for-your-situation frame, never hype.
