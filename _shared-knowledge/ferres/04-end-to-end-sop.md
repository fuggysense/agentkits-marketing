# Ferres End-to-End SOP — Blank Page to Live Ad Set

What this is: Sean Ferres' operational pipeline for the $300 Control Challenge — every step from signed client to four live ads, with tools, timings, and what he checks at each stage.
Primary lectures: Part 5 full demo (transcript 06, 1:44:33), Control Challenge Checklist (text/17).
Last distilled: 2026-06-10.

---

## The shape of the offer (why these steps exist)

The whole pipeline produces ONE deliverable: three new video ads that race the client's existing winner head-to-head. Three ads = (1) the client's exact hook re-shot with an AI avatar, plus (2) two brand-new AI-avatar hooks. Run all four ads (the original plus your three) for 7 days; whoever wins, you keep. (06 [01:08:50], [01:27:23])

## Tool stack (⚠️DATED, pinned to early Nov 2025; "changes day to day")

- **ChatGPT Plus, $20/mo** is the only paid cost. Scripting plus deep research. Perplexity not needed. (06 [00:01:33], [00:01:50]) ⚠️PLATFORM
- **Sora 2** for video gen: free with ChatGPT Plus (watermarked) OR via fal.ai at $0.10/sec, no watermark. Sora over VEO3 because it's roughly half the cost at similar quality. (06 [00:02:01], [00:07:01]) ⚠️DATED
- **CapCut free plan** for editing. **TurboScribe.ai** transcribes the client's winning ad (3 free/day). **GoFullPage** captures sales pages as PDF. **Loom** records VSLs and competitor ads at 2x. **removesorawatermark.online** strips the watermark. (text/17; 06 [00:09:38], [00:11:13], [01:07:09])

---

## STAGE 1 — Onboard + collect assets (10–20 min)

Trigger: client signs. Send $300 Stripe invoice, get signed agreement back, send onboarding form. (06 [00:08:33]) The form asks for: business URL, the winning ad video file, the landing page it points to, what they sell and who buys, and their top 2–3 competitors. Specifically competitors **spending heavily** on ads, because those are the best ads to swipe. (06 [00:09:00])

Then build the research package on your desktop: download the winning ad and transcribe it (TurboScribe), save the landing page as a PDF (GoFullPage), record any VSL with Loom at 2x. Always name files clearly so the AI knows what each upload is. (06 [00:09:38], [00:11:11], [00:17:55])

## STAGE 2 — Research (≈1 hr 20 min — the longest stage on purpose)

This is the stage you don't rush: "give me six hours to cut down a tree and I'll spend four sharpening my axe." No avatar saves bad messaging. As he puts it, "you will never out-visual a bad hook." (06 [00:16:17], [00:16:35])

**Collect competitor assets (~60 min):** for each top competitor, capture their sales page (GoFullPage) and VSL (Loom), then record **10 of their ads** from Meta Ads Library, split as 3 most-recent (current hooks/angles), 3 a-few-months-old (proven), 4 longest-running (timeless winners that are probably still profitable). Pick 10 genuinely *different* ads, not the same ad with hook swaps. Pause each recording fast so it doesn't loop and double up the transcript. (text/17; 06 [00:13:11], [00:15:35])

**Generate 3 deep-research docs (20–30 min):** run Master Prompt List prompts 1–3 in ChatGPT **Deep Research mode**, one per browser tab, in parallel: (1) ICP Deep Dive, (2) Competitor Analysis, (3) Market Research. Each scans Reddit, reviews, social, and takes 15–30 min. Feed it the client's offer doc, sales page, and ad scripts; if a competitor is missing, tell it. If ChatGPT can't extract a PDF, paste the raw text into a Google Doc, export to PDF, re-upload. (06 [00:17:01], [00:18:08], [00:20:55]) He skim-reads the docs for accuracy but recommends reading them fully, since that's where the positioning gaps live. (06 [00:23:15], [00:23:50])

## STAGE 3 — Hooks: generate, then select (≈10 min)

Run Prompt 1 (Hook Generator) with the winning ad script plus the 3 research docs (and the AI Ads Lab slides, so it uses *your* proven framework, not whatever it invents). Default is 10 hooks across 5 types (shock, curiosity-gap, social-proof, fear/urgency, benefit), but for real client work bump it to 25. (06 [00:25:36], [00:29:35])

Run Prompt 2 (Hook Selector) to score all hooks /60 across scroll-stop, emotional trigger, audience fit, conversion, algorithm, and **differentiation from the original**. (06 [00:29:01]) Then override the AI with judgment: this is collaborative, not copy-paste. Checks he applies: clear beats clever ("confused prospect never buys"); does the hook attach cleanly to the existing ad body; does the hook attract the RIGHT avatar. He rejected "work 1 hour a day" because it pulls lazy people, reworking it to "you already work 8 hours, what if you owned the same in 1?" Final sanity prompt: "act as a world-class viral ad copywriter and copy chief these hooks." (06 [00:31:08], [00:32:39], [00:34:05])

## STAGE 4 — Scenes + video (10–15 min PER hook; do one hook fully, then repeat)

Per hook, run Prompt 3 (Scene Generator) for 5 scene concepts, then Prompt 4 (Scene Selector) to rank them. Avatars must be **aspirational, credible, or relatable** to the target, not random spectacle. (06 [00:36:09], [00:37:50]) Once the formal prompts are done, drop the rigid prompting and talk to ChatGPT like a thought-partner. He scrapped all 5 "boring" scenes and asked for "crazy unhinged" robot-boss concepts to match a punchy line, because you're competing with memes for attention. (06 [00:39:17], [00:40:00])

Run Prompt 5 (Sora Scene Builder) to compile the chosen scene into a Sora 2 prompt, **50–100 words** per OpenAI's guide. The balance is load-bearing: enough detail to control mood/lighting/action, not so much it breaks ("you don't want to control it frame by frame"). (06 [00:46:17], [00:46:32])

Generate: vertical **9:16**, ~**8 seconds** for a hook. He runs Sora.com AND fal.ai simultaneously across multiple tabs (2–3 max in the Sora app before it gets funky; unlimited on fal.ai). It's a **volume game**: generate many, expect duds, keep the "happy accidents." Stick to standard Sora 2 (720p), not Pro (3–5x credits), since you upscale free in CapCut later. (06 [00:47:46], [00:48:28], [00:54:35])

Iteration loop he actually runs. Dialogue cut off: tell ChatGPT "make sure all dialogue fits the 8-second window" and regenerate. Wrong background: screenshot a good frame, feed it back as a visual reference, or try image-to-video. Compliance worry (violence, bikini, body): he reworks the prompt OR test-launches on his OWN Meta account at $5/day (no spend, just see if it gets approved), never risking a client account. (06 [00:52:39], [00:53:06], [01:00:46])

Accept/reject criteria, in his words: prompt adherence, delivery/tonality, framing (both characters in frame), comedic timing. He picks the robot-therapist winner on humor, relatability, and viral feel, then plans to splice the *better audio take* over the *better visual take*. (06 [01:05:08], [01:06:32])

## STAGE 5 — Edit + deliver (≈40 min for all 3)

Remove watermark first (removesorawatermark.online: paste the published Sora link, instant and free). (06 [01:07:09]) In CapCut: set **9:16**; place the new AI hook at the front, trim the first beat so it jumps to the action; stitch the new hook onto the original ad body so it reads as one seamless clip (he sync-matches the audio waveform and cuts at the exact frame the avatar starts talking). (06 [01:09:53], [01:11:45])

Polish pass: upscale to **HD**, not UHD (too AI-looking; free in CapCut); auto-adjust color ~30% so it pops in-feed; even out volume, peak around −6 dB, never clip into red. Generate captions on the HOOK only (the original body already has them); fix wording and timing; ~4–5 words/line; style native-to-platform; keep them mid-to-lower-third. (06 [01:13:25], [01:17:00], [01:18:11])

Two judgment moves worth copying. **On-screen text hook** in the first ~1.8 seconds to create curiosity for the RIGHT person: he chose "POV: your boss replaced HR with ChatGPT" over a generic therapist line, to filter for office workers, not "random depressed fucks." (06 [01:19:54], [01:20:20]) **Emotional aftertaste**: he picked humor over the savage robot-CEO cut because viewers should *feel good* about your brand (Coca-Cola logic); laughter lowers the guard and lets the message in. (06 [01:10:13])

Final gate before handoff: export 1080p, mp4, 30fps, H.264 (CapCut auto-settings are fine), then **watch the whole thing start to finish on a big screen with fresh eyes, always, before any client sees it.** (06 [01:24:11], [01:24:49]) Package into a Google Drive folder: the 3 video files (named clearly), optional text file of the new hook scripts, and the ad setup guide. Set sharing to "anyone with link can view"; getting this wrong is the named mistake. (06 [01:24:18]; text/17; 05 [00:40:25])

## STAGE 6 — Test setup (the Control Challenge gate)

Client runs it; you must know the exact setup so it's a fair, single-variable test. Duplicate the existing winning campaign ("duplicate original setup," skip Meta's suggested changes). In the duplicate, keep ONLY the best-performing ad set with the winning ad and delete everything else (verify it's all GREEN = paused, never touch the live original). Switch from campaign budget to **ad-set budget at $25/day**, because campaign budget lets Meta pick an early winner and starve the rest; you need each ad isolated. Duplicate that ad set 3x and swap in each of your 3 videos. Leave primary text and headlines unchanged (video viewers barely read them); only the creative changes. **Turn OFF every Advantage+ "enhancement"**: they rewrite copy, translate, and swap CTA links. Result: one campaign, 4 ad sets, $25 each = $100/day, 7 days. Publish. (06 [01:30:33], [01:31:51], [01:33:07], [01:36:38])

## STAGE 7 — Result + upsell (after 7 days)

Lose (≈1-in-4): honor the refund, or offer to keep testing hooks free if the client prefers. Win: book the results review call, show the winning ads and the psychology/avatar that made them win, stretch the gap with Meta's "25–35 unique ads" requirement, pitch the $3k package. (06 [01:38:04]) That package is the **5×5**: 5 talking-head, 5 talking-head with AI hooks, 5 full-AI ads, 5 B-roll, 5 testimonial/UGC. Offer the 3 deep-research docs as a sign-up bonus. (text/17; 06 [01:39:46], [01:43:47])

---

## Stage map

| STAGE | inputs | gate | outputs | tool |
|---|---|---|---|---|
| 1 Onboard+assets | signed client | form complete, files named | research package | Stripe, onboarding form, TurboScribe, GoFullPage, Loom |
| 2 Research | package + competitors | 3 docs skim-checked for accuracy | ICP / competitor / market docs | ChatGPT Deep Research, Meta Ads Library, Loom, GoFullPage |
| 3 Hooks | winning script + 3 docs + slides | 2 hooks chosen, clear + right-avatar + flows | 2 new hooks (+ original = 3) | ChatGPT (Prompts 1–2) |
| 4 Scenes+video | chosen hook | accepts on adherence/delivery/framing/timing; compliant | 8s vertical hook clips | ChatGPT (Prompts 3–5), Sora 2 / fal.ai |
| 5 Edit+deliver | raw clips + original ad | full watch-through, fresh eyes, no clipping | 3 final 1080p ads in shared Drive | removesorawatermark, CapCut |
| 6 Test setup | 4 ads | all green, $25/ad-set, enhancements OFF | 1 campaign / 4 ad sets live 7 days | Meta Ads Manager |
| 7 Result+upsell | 7-day data | winner determined | refund OR $3k 5×5 close | Stripe, results call |
