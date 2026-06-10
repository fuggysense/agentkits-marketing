# Audit: unslop profiles vs anti-ai-patterns.md

Date: 260507 | Scope: 4-layer de-AI stack architecture review

---

## What was read

1. `skills/unslop/SKILL.md` — full
2. `skills/unslop/profiles/linkedin-posts.md` — full (generated 260319, 50 samples)
3. `skills/unslop/profiles/email-sequences.md` — full (generated 260319, 50 samples)
4. `context/writing/anti-ai-patterns.md` — full (Wikipedia field guide, 19 categories)
5. `skills/copy-editing/references/overused-ai-patterns.md` — full (5 rhetorical constructions + ~120 prohibited words + structural anti-patterns)

---

## Overlap analysis

### anti-ai-patterns.md vs overused-ai-patterns.md

These two static files have meaningful overlap but are not duplicates:

- `overused-ai-patterns.md` targets rhetorical constructions specific to marketing/sales copy (Revelation Hook, Big Contrast, Philosophical Reduction) and business jargon. Draws from observed copy failure modes.
- `anti-ai-patterns.md` targets universal statistical regression patterns (elegant variation, false ranges, copulative substitution, superficial "-ing" analysis). Draws from the Wikipedia field guide on AI tells.

The overlap zone: both flag em-dash overuse (L.272 in overused-ai-patterns.md; pattern 14 in anti-ai-patterns.md), promotional vocabulary (vibrant, tapestry, underscores appear in both), and "It's not X/it's Y" constructions. Rough estimate: ~20-25% content overlap between these two static files.

These two serve different threat models: overused-ai-patterns.md targets copy-specific slop; anti-ai-patterns.md targets encyclopedic/analytical register slop. Merging them would muddy both.

### unslop profiles vs the two static files

The linkedin-posts.md profile explicitly notes it was deduped (6 patterns removed). The email-sequences.md profile notes 4 patterns removed. What remains after dedup is genuinely domain-specific content the static lists don't have:

**linkedin-posts.md adds:**
- Meta-commentary that arrives *around* the post (bracket placeholders, word count reports, "Here's the post:" hand-offs, "here's why this works" post-hoc sections) — none of this exists in the static files
- Format fingerprints specific to LinkedIn output behavior (uniform short paragraphs, zero-emoji tell, zero-hashtag tell)
- Opening/closing line archetypes tied to LinkedIn's specific cliche ecosystem ("Unpopular opinion:", "Onward.", "DMs open.")
- The "calculated vulnerability" tonal pattern — not flagged anywhere in the static lists

**email-sequences.md adds:**
- Structural sequence patterns (mandatory 5-beat arc, breakup email default, P.S. as structural load-bearing element) — not in any static file
- Anti-marketing-performance as a distinct tonal error ("I'm not like other marketers" pose)
- Specific email phrases tied to deliverability/reply theatrics ("Reply to this email, a real person reads these")
- Meta-commentary specific to sequence output (copywriting masters citations, sequence logic sections, CTA annotation)

These are real additions. The static lists couldn't generate them because they're not universal patterns — they're domain defaults that surface only when you prompt the model for that specific content type at scale.

---

## Architectural evaluation

### Does the 4-layer structure pay its maintenance cost?

The 4 layers are:
- Layer 1: Unslop profiles (domain-specific, soft, empirical, refresh every 90 days)
- Layer 2: overused-ai-patterns.md (universal to copy, hard, static)
- Layer 3: corrections.md (user-accumulated, hard)
- Layer 4: V.O.I.C.E. (positive target)

The maintenance cost is real but not symmetric:
- Layers 2-4 are static or self-appending — near-zero maintenance
- Layer 1 is the only one that requires active work (re-run Python tooling quarterly per domain)

The cognitive load on consumer skills is also real — each skill has to load 2-3 files before drafting. But this is already handled by the consumer skill wiring table in SKILL.md, not by the consuming human.

The key question is whether Layer 1 actually earns its existence vs collapsing into Layer 2. The profiles show it does — but only because the dedup step is enforced. Without the dedup step (SKILL.md Step 4), profiles would accumulate redundant copies of Layer 2 content and the architecture would collapse into noise. The dedup step is the load-bearing mechanism that justifies the separation.

### Is the static/Wikipedia file (anti-ai-patterns.md) earning its position?

This is the weakest link. It lives at `context/writing/anti-ai-patterns.md`, not alongside the copy-editing skill, and it isn't referenced in the consumer skill wiring table in SKILL.md. The routing-overrides.md and unslop SKILL.md both reference `overused-ai-patterns.md` as the dedup target — `anti-ai-patterns.md` is not mentioned in either. This suggests it may be orphaned: loaded by `writing:references:anti-ai-patterns` but not wired into the de-AI stack that actually runs.

If `anti-ai-patterns.md` is loaded separately by general writing contexts, that's fine. If it was intended as Layer 2 but was superseded by `overused-ai-patterns.md`, it's redundant scaffolding.

---

## Verdict: KEEP SEPARATE — with one tightening fix

The 4-layer architecture is justified. The unslop profiles contain real domain-specific signal (meta-commentary patterns, format fingerprints, tonal archetypes) that the static lists cannot and should not contain. Combining them would require either making the static list domain-conditional (defeating its purpose) or stripping the domain-specific content (losing the value).

**What's gained by keeping separate:** crisp constraint hierarchy (soft domain defaults vs hard universal prohibitions vs accumulated corrections), refresh cadence stays isolated to Layer 1, and consumer skills can load only what they need.

**What's lost:** two files to maintain instead of one at the static layer, slight consumer skill loading complexity.

**The one fix:** Clarify whether `anti-ai-patterns.md` is part of the de-AI stack or a parallel general-writing reference. If it's parallel, document that it targets a different register (encyclopedic/analytical) than `overused-ai-patterns.md` (copy-specific). If it was meant to be Layer 2, consolidate into `overused-ai-patterns.md` and delete the separate file. Currently it's ambiguous — that ambiguity is the only real problem in the architecture.

---

**One-line verdict:** The two-layer static architecture (anti-ai-patterns + overused-ai-patterns) has ~20% redundancy but serves distinct registers; unslop profiles are non-redundant after dedup and justify their own layer — keep the stack, clarify which static file owns which register.
