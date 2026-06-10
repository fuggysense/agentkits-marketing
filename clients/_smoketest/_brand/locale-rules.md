# Locale Rules — Meridian Property Advisory (smoke-test, filled SG copy)

> **FICTIONAL SMOKE-TEST DATA — not a real client.** Filled copy of `clients/_template/_brand/locale-rules.md`, tied to Meridian's Singapore property-buyer market. The client-agnostic image method (`skills/ad-concept-engine/references/static-image-method.md`) and the copy pre-launch rubric load this file IF PRESENT and apply it as hard constraints. Built 260611 (rebuild M2.4).

---

## 1. Market + language

- **Primary market:** Singapore (residential property buyers — HDB upgraders + cautious resale first-timers; `_brand/buyer-profile.md`).
- **Register:** Singapore English; plain, direct, numbers-comfortable. The personas are "numbers-comfortable but not property-fluent" (`_brand/buyer-profile.md`), so lead with clean math, not jargon. Colloquial only where the persona VOC is colloquial.
- **Spelling:** UK (analyse, colour, centre) — matches the ACE language standard.

## 2. Casting (people in the image)

- **Primary-variant ethnicity:** match the target avatar's ethnicity for the lead variant.
- **Cross-variant reach:** Singapore's main groups are Chinese, Malay, Indian, and Eurasian — spread the non-primary variants across these to broaden reach without adding a test variable.
- **Realism (always on):** reference a real SG documentary/editorial photographer (Geraldine Kang, Sean Lee) in the `style` field; *Straits Times* feature / *Kinfolk* editorial look, never FB-marketplace stock. Negative prompt blocks: AI skin sheen, warped/extra fingers, over-symmetry, plastic texture, watermark, glossy stock-photo look.

## 3. Regulated / real documents + terms

| Term / document | What it is | Render rule |
|-----------------|-----------|-------------|
| **CPF** | Central Provident Fund — Singapore's mandatory savings scheme; the Ordinary Account funds property purchases. | If a CPF statement/figure appears, render as the real CPF document; any balance/usage figure must fit the persona's income band (household ~S$8k-S$18k/month, `_brand/buyer-profile.md`) — never invented. |
| **HFE** | HDB Flat Eligibility letter — confirms eligibility, grants, loan limits before an HDB buyer can act. | Render as the real HFE letter format; eligibility/grant figures plausible for the persona, never fabricated. |
| **OTP** | Option To Purchase — the document a buyer signs to commit; Meridian's advisory runs "from shortlist through to signing the OTP" (`_brand/offer.md`). | If shown, render as a real SG OTP form; no invented terms or figures. |

- **No invented stats** on any CPF/HFE/OTP/price document. The smoke research pack (`00_inputs/research/market-stats-260611.md`) is FICTIONAL and fails the claim gate as-is — every number routes through `scripts/claim_gate.py`.

## 4. Currency + income bands

- **Currency:** S$ with comma thousands separator (offer price S$4,500 flat, `_brand/offer.md`; "S$30k+" lead-magnet figure; the "S$71k gap" founder-origin number is illustrative, not a guaranteed result).
- **Income sanity:** match the persona's household income range (~S$8k-S$18k/month). A price band outside this reads as fake to a numbers-comfortable buyer.

## 5. Compliance

- **Platform (Meta):** no graphic before/after; no personal-attribute call-outs; no income/money-amount claims that breach policy.
- **Local (property/financial promotion):** avoid guaranteed-return or guaranteed-price language — Meridian explicitly does NOT outcome-guarantee the advisory ("Daniel won't promise a price he doesn't control", `_brand/offer.md`). CPF/HDB references must stay factually accurate to current scheme rules.
- **Kill-list cross-check:** reconcile against `_brand/brand-voice.md` before finalising. The personas reject drone-shot aspiration, "decide this weekend" urgency, and outrage/founder-rant marketing (`_brand/buyer-profile.md`) — the gut-punch must come from recognition and the clean-incentive contrast, not hype.
