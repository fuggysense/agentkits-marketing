# Offer Definition — VitalKit Labs

> **FICTIONAL SMOKE-TEST DATA — VitalKit Labs is not a real client.** Thin seed, as a brand-new
> client would have before offer-builder / source-of-truth runs. Scoring matrices left for later.

## Product Classification
- **product_type:** ecom (DTC physical product)
- **business_model:** hybrid — one-off starter kit + recurring subscription

> Both fields are REQUIRED. They drive downstream skill behaviour:
> - `product_type` routes synthesis decisions in `source-of-truth` (KPI defaults, proof types, CTA grammar, format weighting, urgency triggers, angle pool) per `skills/source-of-truth/references/section-synthesis-frameworks.md` Product-Type Branching matrix.
> - `business_model` adjusts pricing/proof framing (e.g., recurring → trial-to-paid proof; performance-based → outcome-conditional pricing copy).
> - If unset, all downstream skills default to property/service patterns and break for ecom/SaaS/info clients.

## Core Offer (T2 — the entry point)
- **Name:** Sleep / Stress / Energy Starter Kit (single-category)
- **One-Line Description:** A curated 30-day supplement kit for one specific problem — sleep, stress, or energy — with ingredient forms and doses selected for that category, plus a plain-language explanation of why each one is in there.
- **Price:** $49 one-time (credits toward first subscription month)
- **Delivery Method:** physical product, shipped DTC
- **Timeline:** 30-day supply

## Offer Ladder (full)
- **T1 (free):** Sleep Stack Guide — 7 mistakes that kill supplement ROI (planned, not built)
- **T2 ($49):** Single-category Starter Kit — 30-day sampler in sleep, stress, or energy
- **T3 ($129/mo):** Foundation Stack subscription — all three kits bundled, cancel anytime

## Viability Scores

### OV Gate
| Dimension | Score |
|-----------|-------|
| Demand | /5 |
| Clarity | /5 |
| Ownership | /5 |
| Proof | /5 |
| **Average** | **/5** |

### Vending Machine Score
| Dimension | Score |
|-----------|-------|
| Demand | /10 |
| Clarity | /10 |
| Offer | /10 |
| Proof | /10 |
| **Average** | **/10** |

## Identity Map

### Offer House
- **Land (Market):**
- **Foundation (Identity):**
- **Walls (Mechanism):**
- **Roof (Promise):**

### 11PM Thought
- **The thought:**
- **Category:**
- **How we address it:**

## Micro Offer
- **What:**
- **Price:**
- **Promise:**
- **Timeline:**
- **Purpose:**

## Value Proposition
- **Primary Benefit:** Stop guessing which supplements to try. Get a kit built for your specific problem, with the right forms and doses, explained in plain language.
- **Supporting Benefits:**
  1. Category-specific: not a generic multi, not an all-in-one — formulated for one problem
  2. Mechanism explained: every ingredient, form, dose, and timing rationale included
  3. Low-commitment entry: $49 trial before any subscription
- **Unique Mechanism:** "Category-first formulation" — each kit is optimized for one physiological pathway (sleep onset vs cortisol vs cellular energy), not a broad-spectrum scatter approach
- **Transformation:** From "I've tried everything and nothing works" to "I finally understand what I'm taking and why, and it's working"

## Proof Elements

### Case Studies
-

### Testimonials
-

### Data Points
-

### Carrier Trust Signals
| Signal | Score (0-3) | Evidence |
|--------|-------------|----------|
| Results Proof | | |
| Social Proof | | |
| Authority Proof | | |
| Mechanism Proof | | |
| Risk Reversal | | |
| Specificity | | |
| Demonstration | | |
| **Total** | **/21** | |

## Guarantee / Risk Reversal
- **Type:** Starter Kit satisfaction guarantee
- **Terms:** If the kit doesn't match what was described — wrong contents, damaged, missing — full replacement or refund. Outcome guarantee not offered (supplement results vary; FTC compliance).
- **Duration:** 30 days from delivery

## Proof (seed — verify before use in copy)
- Founder origin: Priya burned out at 32, spent a year self-researching supplements for recovery. "I did the research so you don't have to." (Fictional — provable with personal narrative; not a clinical claim.)
- Customer story: "Jordan" — tried melatonin for 2 years, never understood timing/form/dose. The sleep kit explanation was the first time she understood what she was taking. (Fictional example.)
- Market stats in `00_inputs/research/market-stats-260611.md` — all FICTIONAL. Fail claim gate as-is.

## TODO (later passes)
- Run offer-builder for OV Gate / Vending Machine / Carrier Trust scoring.
- Verify or replace every proof point through claim gate before any live copy.

## Urgency / Scarcity
- **Type:**
- **Mechanism:**
- **How to communicate:**
