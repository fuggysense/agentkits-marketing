# Copy Routing Map — "which one do I use?"

The single answer to "I want to write X — what do I run?" One canonical owner per deliverable. Everything else redirects here.

**The short version: launch `ccc` and say what you want in plain English.** It reads this map, grounds on the client offer if a client is active, and dispatches to the right skill. You don't pick commands. This page is the source of truth `ccc` and `routing-overrides.md` both point at — and a reference for when you want to run something directly.

---

## The map

| You want to… | Canonical owner | Run directly | Notes |
|---|---|---|---|
| **Long-form sales letter** (cold paid traffic, 800–2000w) | `sales-letter-method` skill | `/copy:sales-letter <client>` | `ccc` finds the Big Idea / spine first, then hands to the method. |
| **Landing / pricing / homepage / product / about page copy** | `copywriting` skill | `/copy:landing <client>` | For *pages*. Not for letters, not for email. |
| **Meta ad text** (primary text + headlines) | `headline-bank` skill | `/ads:headlines` | Halbert-style 50w/150w copies + short headlines. |
| **Ad angles** (the strategic hooks behind the ad) | `big-angle-spotter` skill | `/copy:ad <client>` (full gated ad copy) · or `big-angle-spotter` directly (trigger: "spot angles") for raw angle + headline + image-prompt artifacts — no `/ads:big-angle-spotter` command exists | Angles ≠ headlines. Angle = the idea; headline = the line. |
| **Full DCT ad batch** (3×2×2 = 12 combinations) | `ad-concept-engine` skill | trigger: "DCT" / "ad concepts" (no standalone `/ads:concepts` command exists yet) | Downstream of `avatar-research`. Delegates angle work to `big-angle-spotter`. |
| **Email / sequence** (welcome, nurture, sales, re-engage) | `email-sequence` (copy) + `email-marketing` (strategy) | `/content:email <client>` | The ONE place `/content:*` is still the live engine. `email-sequence` = per-flow copy; `email-marketing` = deliverability/strategy. |
| **Edit / polish / de-AI existing copy** | `copy-editing` skill | — | Uses the single shared kill-list (`forbidden-content-audit.md`). Don't hand-route to unslop / brand-voice-guardian separately. |
| **Build / score an offer** | `offer-builder` skill | trigger: "build offer" (no `/offer:*` command exists yet) | Sole writer of `_brand/offer.md`. `client-onboarding` + `brand-scaffolder` write the same shape. |
| **Buyer research** | `avatar-research` (profile) + `buyer-language-researcher` (voice-of-customer dossier) | `/research:market` | `avatar-research` owns `buyer-profile.md` and chains the dossier as a sub-step. |
| **Big Idea / spine / stylize a line / kill-the-babies pass** | `copy-coach` (the `ccc` persona) | `ccc` | The interactive coaching layer. Names the principle behind every fix. |

## Hooks — disambiguated by context

"Write me a hook" routes by *where the hook lives*:

| Hook for… | Use |
|---|---|
| A **paid video ad** (multi-clip) | `video-hook-variants` skill |
| **Organic short-form** (Reels, TikTok, general social) | `viral-hooks-content-creator` skill |
| An **Instagram Reel** specifically | `ig-reel-script-writer` skill |
| A **YouTube / long video** | `yt-scriptwriter` / `script-skill` |
| The **opening line of a letter / email / ad** | That's the *lead* — handled inside `sales-letter-method` / `email-sequence` / `headline-bank`, not a separate hook skill. |

## Writing that isn't copy (future-friendly via `ccc`)

`ccc` is a copy-*and-writing* brain. For non-selling prose it defers to the matching skill plus the global `/writing` anti-slop floor:

| You want… | Use |
|---|---|
| **LinkedIn post / profile** | `linkedin-content` / `linkedin-optimization` |
| **Any general prose a human reads** (blog, caption, DM, newsletter) | global `/writing` skill (the shared floor) |

---

## The two rules that resolve the old contradictions

1. **Readability:** register is **audience-relative**. Third-grade Singapore-English for ESL/consumer; professional or technical for insider/B2B. This **overrides** the global `/writing` skill's fixed grade-4–6 target whenever the reader is an insider or B2B. (Grade 4–6 applies to consumer short-form only.)
2. **Language:** always reply in **English**, regardless of any skill's "respond in the user's language" boilerplate.

## What's deprecated (don't start here)

- `/content:sales-letter`, `/content:ads` → use `/copy:sales-letter`, `/ads:*`. (`/content:email` is the exception — still the live email engine.)
- `/copy:headline` as a standalone → folded into `/ads:headlines` + `headline-bank`.
- Routing the same task through both a `/copy:*` wrapper *and* a `/content:*` command — pick the canonical owner above.

*Machine-side precedence lives in `.claude/rules/routing-overrides.md` → "Copy deliverable → canonical owner". This page is the human-readable mirror.*
