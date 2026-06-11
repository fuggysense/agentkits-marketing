# Locale Rules — TEMPLATE

> **What this is.** Per-client locale rules for ad creative: who to cast, which documents/terms are real and must render correctly, currency/income bands, and platform/regulatory compliance specific to this client's market. The client-agnostic skills (`static-image-method.md`, `copy-prelaunch-rubric.md`) carry ZERO locale content — they load THIS file IF PRESENT at `clients/<slug>/_brand/locale-rules.md` and apply it as hard constraints.
>
> **How to use the template.** Replace every `<…>` with this client's reality. The Singapore block below is a worked EXAMPLE — keep it if the client is SG, delete and rewrite if not. If a client has no locale specifics (rare for image ads with people or regulated claims), still write the file and say so explicitly under each heading, so the loader knows the silence is deliberate.
>
> **Source the specifics.** Every regulated term, document, and income band should trace to a real source (a government site, the client's `_brand/offer.md`, or a research file). The claim gate and the image QA gate read this file's compliance block.

---

## 1. Market + language

- **Primary market:** `<country / city / region>`
- **Audience language register:** `<e.g. Singapore English / Bahasa / formal vs colloquial; spelling convention UK vs US>`
- **Spelling:** `<UK or US — match the client's existing copy>`

## 2. Casting (people in the image)

> Any person rendered in an ad must be demographically correct for THIS market. Off-market casting reads as a stock-photo ad and tanks the native feel.

- **Primary-variant ethnicity:** match the target avatar's ethnicity. `<which group, per the active persona>`
- **Cross-variant reach rule:** use the other variants to broaden across the market's main demographic groups WITHOUT adding a test variable. `<list the market's main groups>`
- **Realism (always on):** real, imperfect faces — natural skin texture, asymmetry, available light. Reference a real local photographer by name in the `style` field. Block in the negative prompt: AI skin sheen, warped/extra fingers, over-symmetry, plastic texture, watermark, glossy stock-photo look.

## 3. Regulated / real documents + terms

> If the image shows a document, an official term, or a system unique to this market, it must look like the real thing and be factually correct. Garbled or invented official documents break trust and can trip platform review.

| Term / document | What it is | Render rule |
|-----------------|-----------|-------------|
| `<official term>` | `<one-line definition + source>` | `<must look like the real doc; correct fields; no invented stats>` |

- **No invented stats** on any document or data overlay. Numbers route through the claim gate (`scripts/claim_gate.py`).

## 4. Currency + income bands

- **Currency + format:** `<symbol, separator, e.g. S$1,234.56>`
- **Income / price-band sanity:** any price band or income figure shown must match the persona's actual range from `_brand/buyer-profile.md` + `_brand/offer.md`. Don't show a band the persona would never see.

## 5. Compliance (platform + local regulator)

> The image QA gate and the copy pre-launch rubric read this block. List every hard "do not."

- **Platform (Meta) — hard blocks:** no graphic before/after transformation photos (imply or animate); no personal-attribute call-outs; no income/money-amount claims that breach policy.
- **Local regulator:** `<body + the specific rules — e.g. advertising standards, financial-promotion rules, healthcare-claim rules>`
- **Client kill-list cross-check:** reconcile against `clients/<slug>/_brand/brand-voice.md` kill-list before finalising (the gut-punch must come from emotion the brand permits).

---

## Worked EXAMPLE — Singapore (delete or rewrite if not SG)

### 1. Market + language
- **Primary market:** Singapore.
- **Register:** Singapore English; plain, direct, numbers-comfortable. Colloquial only where the persona's verbatim VOC is colloquial.
- **Spelling:** UK (analyse, colour, centre).

### 2. Casting
- **Primary-variant ethnicity:** match the target avatar's ethnicity.
- **Cross-variant reach:** Singapore's main groups are Chinese, Malay, Indian, and Eurasian — spread the non-primary variants across these to broaden reach without adding a test variable.
- **Realism:** reference a real SG documentary/editorial photographer (e.g. Geraldine Kang, Sean Lee) in the `style` field. Aim for a *Straits Times* feature or *Kinfolk* editorial look, not an FB-marketplace ad.

### 3. Regulated / real documents + terms

| Term / document | What it is | Render rule |
|-----------------|-----------|-------------|
| **CPF** | Central Provident Fund — Singapore's mandatory savings/retirement scheme; CPF balances and the Ordinary Account fund property purchases. | If a CPF statement or figure appears, it must look like the real CPF document and use a balance/usage figure consistent with the persona's income band — no invented numbers. |
| **HFE** | HDB Flat Eligibility letter — confirms eligibility, grants, and loan limits before an HDB buyer can act. | If shown, render as the real HFE letter format; eligibility/grant figures must be plausible for the persona and never fabricated. |

- No invented stats on any CPF/HFE/price document — route every number through the claim gate.

### 4. Currency + income bands
- **Currency:** S$ with comma thousands separator (S$4,500; S$214,300).
- **Income sanity:** match the persona's stated household income range in `_brand/buyer-profile.md`. A band the persona would never see reads as fake.

### 5. Compliance
- **Platform (Meta):** no graphic before/after; no personal-attribute call-outs; no income/money-amount claims that breach policy.
- **Local:** financial/property promotions should avoid guaranteed-return or guaranteed-price language; property advice that touches CPF/HDB rules must stay factually accurate to current scheme rules.
- **Kill-list cross-check:** reconcile against the client's brand-voice kill-list before finalising.

### 6. Cultural sensitivity (SG-specific — was `sg-cultural-guidelines.md`, relocated 260611)

> Only relevant for clients whose audience is SG and ethnicity/religion-sensitive (e.g. a Malay-Muslim property audience). Skip if the client's audience is mixed/general and the brand voice already covers tone.

- **Malay-Muslim audience — do:** family/legacy framing (providing for parents + children); "we decide together" couple framing; acknowledge community touchpoints (void decks, estate identity); show households, not lone individuals.
- **Malay-Muslim audience — don't:** mock or trivialise HDB living; imply not-upgrading = failure; "keep up with the Joneses" framing; alcohol/gambling/non-halal imagery; debt-shaming ("stuck in debt", "throwing money away").
- **Islamic finance:** riba (interest) is a genuine concern — use "monthly commitment" or "financing", not "mortgage", for devout-Muslim audiences (see this client's ad-concept-engine `corrections.md` 260406). Reference Shariah-compliant options (Musharakah Mutanaqisah; Maybank/OCBC Islamic financing) only when relevant. Never label a service "halal" unless the client genuinely offers Shariah-compliant products. Treat "Is this halal?" as a values question, never a gimmick.
- **Sensitive periods:** Ramadan / Hari Raya Aidilfitri and National Day — acknowledge respectfully or stay neutral; never use a religious occasion as an urgency trigger ("Hari Raya special — upgrade now!").
- **Property-specific:** HDB is national pride, not something to "escape" — frame upgrading as progression; never name an estate negatively; avoid PDPA-triggering language ("We know your MOP is ending"); no implied returns (MAS compliance).
- **Language register:** Meta ad copy = standard English with natural SG phrasing. Singlish ("lah", "lor", "can") is fine in casual organic content only, used sparingly and authentically — never forced to seem relatable.
