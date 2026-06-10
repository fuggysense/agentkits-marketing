# Four Horsemen — Pre-flight Audit

Run this on EVERY hook before locking a variant. A hook that fails ANY check → redraft.

## The Four Failures

### 1. Delay

**Test:** Does the core topic appear within 1 second?

**Fail condition:** The first phrase is a generic warmup. No value delivered in first 1–2 seconds.

**Fix:** CUT the warmup. Start with the what. The hook's first word should create momentum.

**Common fail patterns:** "Have you ever wondered…" / "Welcome to…" / "Today we're going to talk about…" / "Hi I'm [name]" — see `references/frameworks/forbidden-openers.md`.

---

### 2. Confusion

**Test:** Would a 12-year-old understand the verbal layer?

**Fail condition:** Coded medical / financial / technical / industry language slips into the first sentence. Viewer spends cognitive effort parsing words instead of absorbing the hook.

**Fix:** Rephrase. Replace jargon with plain words. If the viewer has to work to decode the first sentence, they've already scrolled.

---

### 3. Irrelevance

**Test:** Does the hook use "you/your" (not "I/me")? Does the viewer immediately know "this is for someone like me"?

**Fail condition:** Hook is entirely about the creator's perspective. No anchor to the viewer's world.

**Fix:** Anchor with a specific avatar tell — a sensation, scenario, or identity the viewer recognizes. OR tag an emotion the viewer carries (loneliness, isolation, ambition, fear of wasting time, cost of the wrong circle). Emotion is the universal bridge: a 22-year-old can relate to a 34-year-old saying "I'm afraid I've wasted too much time" via the underlying fear — not the specific age.

---

### 4. Disinterest

**Test:** Is there contrast or tension within the first 2 seconds?

**Fail condition:** The hook is static, low-energy, or entirely expected. No Point A → Point B movement. No curiosity gap opened.

**Fix:** Inject contrast. Engineer the distance between what the avatar believes now (Point A) and your contrarian frame (Point B). The bigger the gap, the stronger the pull.

---

## Output Field

In `hook-variants-draft.json`, record per variant:
```json
"four_horsemen_check": {
  "delay": "<how you neutralized it — pass>",
  "confusion": "<how you neutralized it — pass>",
  "irrelevance": "<how you neutralized it — pass>",
  "disinterest": "<how you neutralized it — pass>"
}
```

Also record which Horseman was most at risk during drafting — surface for AG1 review if it passed only marginally.
