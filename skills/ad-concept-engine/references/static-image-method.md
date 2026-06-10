# Static Image Method (Ferres-grounded)

> **Active method for static + carousel image prompts.** Load this in Phase 2a whenever a batch's `format ∈ {Static, Carousel}`. It replaces the retired `high-converting-static-brief.md` (now in `_archive/references-pre-ferres/`, switchable on operator request).
>
> **Grounding:** Sean Ferres "AI Ads Lab" — distilled and citation-verified in `_shared-knowledge/ferres/06-statics-playbook.md`, `_shared-knowledge/ferres/patterns/statics-pattern-library.md`, and `_shared-knowledge/ferres/05-quality-bar-critique-rubric.md`. When a claim here is thin, open those files for the primary-source line cites.
>
> **Client-agnostic.** This file holds zero locale content. Locale rules (ethnicity casting, regulated documents, currency/income bands, compliance bodies) live per-client in `clients/<slug>/_brand/locale-rules.md` — load it IF PRESENT before writing any prompt. Template + SG example: `clients/_template/_brand/locale-rules.md`.

---

## What this method does

For each static/carousel batch, it produces image-gen prompts that are grounded, not guessed. The flow is four moves:

1. **Choose the format or pattern** — pick a lane (1 of 5) or a named sub-pattern (1 of 11).
2. **3-pass teardown-rebuild** — why-it-wins → how-we-rebuild → the prompt. Either teardown a swipe winner or build from scratch on the same three passes.
3. **Inject the client's offer + VOC** — every specific (price, mechanism, the on-image hook) carries a source pointer, and the prompt text runs the M1 claim gate.
4. **Post-render image QA gate** — text legible + spelled, on-brand, product correct, compliance scanned. Then label by format + hook.

The operating creed from the playbook: you don't need perfect, you need a volume of good-enough images that sell the click; the dashboard picks the winner (`06-statics-playbook.md` §6).

---

## Move 1 — Choose the format OR a pattern

### The operating axis first (decides which lane you even reach for)

Map directness to the persona's Schwartz awareness. The hotter/more-aware, the more direct; the colder/more-unaware, the more disguised it must be (`06-statics-playbook.md` §2).

- **Direct** (product shot, social proof) → links straight to product page/checkout. Speaks to the ~3% ready to buy. Highest ROAS, small ceiling.
- **Indirect** (infographic, native, tabloid) → links to an advertorial that does the selling. Speaks to the other 97%. Scales on cold traffic. The less it looks like an ad, the better it performs.

Two facts to bake into every batch (`06-statics-playbook.md` §1):

- **Statics fatigue faster than video** — one glance gives away the whole message. Keep feeding fresh ones; hold frequency under 3 (Meta metric).
- **Long run-time is the "this works" stamp** — when you swipe, model the long-runners first.

### The 5 canonical formats (lane labels for tagging)

Pick ONE lane per creative; vary lanes across the batch. Full anatomy: `06-statics-playbook.md` §3.

| # | Format | Direct/Indirect | Use when | Routes to |
|---|--------|-----------------|----------|-----------|
| 1 | **Product Shot** | Direct | Product-/most-aware, retargeting | Product page |
| 2 | **Social Proof / Testimonial** | Direct | Doubt is "does it work for someone like me" | Product page |
| 3 | **Educational / Infographic** | Mostly indirect | Problem-/solution-aware who want the mechanism | Advertorial |
| 4 | **Native** | Indirect (blend-in) | Cold/unaware — copy does 100% of the work | Advertorial |
| 5 | **Breaking News / Tabloid** | Indirect (stand-out) | Cold/unaware at scale (Ferres' favourite) | Advertorial |

### The 11 named patterns (the specific layout the generator needs)

When a lane is too coarse, **load `_shared-knowledge/ferres/patterns/statics-pattern-library.md` at generation time and cite the chosen pattern by name** (e.g. "Pattern 08 — Breaking-News / Tabloid"). The library carries 49 winning creatives clustered into 11 patterns, each with anatomy + a prompt-ready replication recipe. Each pattern already maps to one of the 5 lanes, so tagging stays consistent.

| Pattern | Lane |
|---------|------|
| 01 Product-Shot + Big Promise | PRODUCT-SHOT |
| 02 Hard Offer / Red-Hot-Deal | PRODUCT-SHOT |
| 03 Social-Proof Quote + Face | SOCIAL-PROOF |
| 04 Verified Review / Comment Card | SOCIAL-PROOF |
| 05 Educational / Annotated Infographic | INFOGRAPHIC |
| 06 Us-vs-Them Comparison | INFOGRAPHIC |
| 07 Native Article-Thumbnail Advertorial | NATIVE |
| 08 Breaking-News / Tabloid | TABLOID |
| 09 Native-Organic: Notes / Handwritten / UI-Mimic | NATIVE |
| 10 Before / After Transformation | SOCIAL-PROOF / INFOGRAPHIC |
| 11 Pattern-Interrupt Oddballs (Wanted Poster, Ugly Pain, Surreal-AI, Meme, Apology, Listicle cover, Spokesperson, UGC-selfie, Podcast-clip, Quiz, Countdown) | mixed |

Cite the pattern in the prompt's `_meta.pattern` field. Don't paraphrase the recipe from memory — read the live pattern block so the layout is right.

### Batch spread rule

No two creatives in a batch share a pattern, and the lanes spread across the direct/indirect axis. For a cold-traffic wave, weight the 3 indirect lanes (infographic, native, tabloid); for warm/retargeting, weight product-shot + testimonial (`06-statics-playbook.md` §6 — the 5-Ad Sprint allocation).

---

## Move 2 — 3-pass teardown-rebuild

Every prompt is built on three passes, whether you swipe a winner (80% of tests) or build from scratch (20%) (`06-statics-playbook.md` §5, `statics-pattern-library.md` "build stack").

### Pass 1 — Why it wins

For a swipe: front-load the client brand docs + brief, paste the winner, and name the eye-path, the hook/promise/action, the awareness level it serves, and the emotional button it presses. For a from-scratch concept: name the same four things about the concept you're about to build, so you're not flying blind.

### Pass 2 — How we rebuild

Keep the converting structure and psychology; swap the product, offer, voice, and colours for this client. The structure is the winner — the words and the casting are yours. This is where the offer + VOC injection (Move 3) happens.

### Pass 3 — The prompt

Write one copy-paste image-gen prompt that specifies:

- **Format/pattern lane** + what the image should "pass as" (an article, a friend's post, a polished ad).
- **Scene** — subject, setting, props.
- **Top-to-bottom layout** + product placement (for a product shot, composite the real background-stripped PNG).
- **Brand colours** (from the client brand kit).
- **Framing / lighting** + a real photographer reference where realism matters.
- **Exact on-image words in quotes**, rewritten for this offer — plus 2 alternate test headlines.
- **Aspect ratio 4:5 portrait**, text inside a centre-safe area so a square crop survives, `--ar 4:5`. (Feeds went vertical; 1:1 is outdated — `06-statics-playbook.md` §5.)
- **Anti-AI negative prompt** — block AI skin sheen, warped/extra fingers, over-symmetry, plastic texture, watermark, glossy stock-photo look.

For face-locked composites across a set, open the prompt with a non-negotiable face-fidelity block (pixel-level likeness, no smoothing, treat as background-replacement around an untouched subject) and lock the reference — see `image-generation/SKILL.md` § Character Consistency.

---

## Move 3 — Inject offer + VOC (every specific carries a source pointer)

The image text is where an unsourced claim is most dangerous: it ships inside a pixel where no reviewer re-reads the body copy. So every concrete thing on the image traces back to a file.

### Fixed-slot discipline (same as headline-bank)

Each prompt fills these slots, and each slot that carries a claim or a VOC line names its source — same discipline `headline-bank` uses for its headline/copy slots (verbatim avatar voice, no paraphrase into marketer-speak). Put the pointer in the prompt's `_meta`, not on the rendered image:

| Slot | What goes in it | Source pointer (required) |
|------|-----------------|---------------------------|
| `on_image_hook` | The exact on-image words (2-8 words preferred) | If it mirrors the buyer, cite the VOC line: `_brand/buyer-profile.md:<line>` |
| `bridge_line` | Optional — only if the hook alone confuses | VOC or offer line if it carries a specific |
| `offer_specific` | Price, guarantee, mechanism name, timeline shown on image | `_brand/offer.md:<line>` |
| `proof_cue` | Rating, badge, review count, named result | A research file path + line/anchor |
| `claims_ledger` | Any number on the image | `dct.json` `claims:` ledger entry (path + line) |

### VOC sourcing rule

Pull the on-image hook and any mirror line from the persona's own words in `_brand/buyer-profile.md` (Language rows, Raw inner dialogue, buyer-truth line). Do not invent a quote and do not paraphrase their words into category language. If the persona file has no usable verbatim for the angle, the hook drops to a benefit/curiosity line — it does not fabricate a quote. (This mirrors the M1 Quote Provenance rule that avatar-research enforces upstream.)

### The M1 claim gate runs on the prompt text

Every number a creative asserts is a liability if no source backs it. After the prompts are assembled into `dct.json`, run the claim gate as a hard precondition — it reads `text_on_image_hook`, `bridge_line`, `image_prompt`, and the copy fields, extracts checkable claims (currency, percentages, ratios, quantified superlatives), and resolves each against the `claims:` ledger → `_brand/offer.md` prices → an auto-trace through client research + the research vault.

```bash
python3 scripts/claim_gate.py --gate clients/<project>/campaigns/<campaign>/dcts/<dct-slug>/dct.json
```

Exit 0 = every claim sourced. Exit 1 = at least one unsourced; fix each by (a) adding a source to the `claims:` ledger, (b) rewording without the number, or (c) cutting the claim. Never wave a failing gate through silently. Full spec: ACE `SKILL.md` § Claim Gate.

---

## Move 4 — Post-render image QA gate

This runs after the image renders, before the human creative gate (HITL Gate 3). It is the playbook's launch QA (`06-statics-playbook.md` §5) plus a compliance scan. Fail any line → regenerate; do not ship.

```
[ ] TEXT LEGIBLE + SPELLED  — on-image text reads clearly in the feed thumbnail and is spelled
                              correctly (AI still fumbles text). If a text-heavy variant renders
                              messy, render a clean text-free plate and set copy in Canva.
[ ] ON-BRAND               — colours, type, tone match the client brand kit + kill-list.
[ ] PRODUCT CORRECT        — the product renders accurately (founders notice). Composited from the
                              real background-stripped PNG for product shots.
[ ] COMPLIANCE SCAN        — no literal before/after transformation photos (Meta disapproves and can
                              kill the account — imply or animate instead). Apply the client's
                              `locale-rules.md` compliance block if present (regulated claims,
                              personal-attribute call-outs, income/money-amount rules).
[ ] CLAIM GATE GREEN       — claim_gate.py returned exit 0 (or a recorded operator override).
```

Then **label by format + hook** so the dashboard and the feedback loop can read it back — e.g. `NEWS-3_FixTheIncentive`, `INFOGRAPHIC-1_HiddenCommission` (`06-statics-playbook.md` §6).

---

## Output contract (per creative, in the dct.json image_pool)

The full image prompt lives in a file; the manifest references it. Never inline the whole prompt in the tracker (corrections 260418).

```json
{
  "id": "<dct>-img-<NN>",
  "pattern": "Pattern 08 — Breaking-News / Tabloid",
  "lane": "TABLOID",
  "direct_indirect": "indirect-standout",
  "routes_to": "advertorial",
  "text_on_image_hook": "<exact on-image words>",
  "bridge_line": "<optional>",
  "image_prompt_file": "campaigns/<campaign>/image-prompts/<dct>-img-<NN>.json",
  "label": "NEWS-3_<HookShort>",
  "_meta": {
    "voc_source": "_brand/buyer-profile.md:<line>",
    "offer_source": "_brand/offer.md:<line>",
    "claim_sources": ["dct.json#claims/<id>"]
  }
}
```

---

## Worked smoke example (pattern-cited, source-pointed)

Client: `clients/_smoketest/` — Meridian Property Advisory (fictional smoke data). Persona: **MP-03 Fee-Allergic Convertible** (`_brand/buyer-profile.md:132`), the ROI-driven skeptic who scoffs at paying for "free" advice until the hidden commission cost is made visible. Awareness L4 (`_brand/buyer-profile.md:176`). Cold-traffic, so an indirect lane.

**Move 1 — pattern.** L4 + "make the hidden cost visible, contrast the model not the people" (`_brand/buyer-profile.md:176`) → **Pattern 09 — Native-Organic: Notes / Handwritten / UI-Mimic** (NATIVE lane, indirect blend-in). A fake note that mirrors the buyer's own realisation reads as found content, not an ad; routes to an advertorial, never straight to the product page.

**Move 2 — 3 passes.**
- *Pass 1 (why a note wins for this persona):* eye-path lands on a single human-feeling line; the hook is the buyer's own inner monologue, so it pre-empts the "this is an ad" reflex; serves L4 by mirroring not claiming; emotional button = the relief of finally seeing the rigged math.
- *Pass 2 (rebuild for Meridian):* surface = a phone Notes-app screenshot. Copy = the persona's own words. Product (the advisory) stays out of the image; selling is deferred to the advertorial.
- *Pass 3 (the prompt):* see below.

**Move 3 — slots + sources.**
- `on_image_hook`: "Fix the incentive and I'm in." → verbatim VOC, `_brand/buyer-profile.md:156` (Raw inner dialogue) and `:41` (buyer-truth line). Not paraphrased.
- `bridge_line`: "The 'free' agent's fee is baked into the price." → mirrors `_brand/buyer-profile.md:154` (Beliefs to overcome, MP-03).
- `offer_specific`: none shown on this native variant (keeps it un-ad-like).
- No numbers on the image → claim gate has nothing to flag for this creative. (A sibling product-shot variant that prints "S$4,500 flat, no commission" would source it to `_brand/offer.md` line for the S$4,500 price via the ledger.)

**Pass 3 prompt (stored at `campaigns/wave-smoke-260611/image-prompts/DCT-SMOKE-img-09.json`):**

```json
{
  "meta": { "aspect_ratio": "4:5", "resolution": "2K", "thinking_level": "high",
            "pattern": "Pattern 09 — Native-Organic: Notes / UI-Mimic", "lane": "NATIVE" },
  "scene": "A close, slightly-off-angle phone photo of an iOS Notes-app screen, held in one hand at a kitchen table, available evening light, faint warm bokeh behind. Reads as a real screenshot a person took, not a designed graphic.",
  "on_image_text": "Note title: \"Fix the incentive and I'm in.\"  Body line, smaller: \"The 'free' agent's fee is baked into the price.\"",
  "layout": "Note text fills the centre-safe area; phone bezel and hand at the edges; nothing branded on screen.",
  "style": "Candid documentary realism, real phone-camera look, natural skin texture on the hand, slight asymmetry. No graphic-design polish, no banner, no logo.",
  "negative_prompt": "AI skin sheen, plastic texture, warped or extra fingers, over-symmetry, watermark, glossy stock-photo look, designed ad banner, brand logo on screen",
  "_meta": {
    "voc_source": "_brand/buyer-profile.md:156, :41",
    "bridge_source": "_brand/buyer-profile.md:154",
    "offer_source": "n/a (no offer specific on this native variant)",
    "claim_sources": []
  }
}
```

**Move 4 — QA.** Text legible + spelled (two short lines, low garble risk); on-brand (un-branded by design — native lane); product correct (product intentionally absent); compliance (no before/after, no income claim, locale-rules SG compliance block applies if present); claim gate green (no numbers). Label: `NATIVE-9_FixTheIncentive`. Routes to the "hidden commission" advertorial.
