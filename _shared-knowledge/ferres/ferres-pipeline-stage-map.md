# Ferres Pipeline Stage Map — Client Intake to Launch, Iterate, Feedback

Sean Ferres' full ad-production process, A to Z, assembled from the distilled rulebooks. One row per stage. Where his process has no formal gate, the row says so honestly. Each row cites the distilled file it came from.

Two paths share the same spine. The **video path** (Stages 1-7) is the $300 Control Challenge SOP. The **statics path** (Brief, Path A/B, Generate, QA, Route) is the parallel image-ad track. Media buying (Test/Scale/Fatigue) closes both.

---

## Video path — the $300 Control Challenge

- **STAGE 1. Onboard + assets** | inputs: signed client | gate: form complete + files clearly named | outputs: research package (control_ad_script, business_details, landing_page.pdf, vsl_script) | owner/tool: Stripe, onboarding form, TurboScribe, GoFullPage, Loom — *[04-end-to-end-sop.md]*

- **STAGE 2. Research** | inputs: research package + named competitors | gate: 3 deep-research docs skim-checked for accuracy (re-run with more context if thin) | outputs: ICP / Competitor-Analysis / Market-Research docs | owner/tool: ChatGPT Deep Research (Prompts 1-3, parallel tabs), Meta Ads Library, Loom, GoFullPage — *[02-research-flow.md, 04-end-to-end-sop.md]*

- **STAGE 3. Hooks** | inputs: winning ad script + 3 research docs + AI Ads Lab slides | gate: 2 hooks chosen that are clear, attract the right avatar, and flow into the existing body (scored /60, then human override) | outputs: 2 new hooks (+ original re-shot = 3 total) | owner/tool: ChatGPT Prompts 1-2 (Hook Generator + Selector) — *[03-angles-hooks-copy.md, 04-end-to-end-sop.md]*

- **STAGE 4. Scenes + video** | inputs: chosen hook line | gate: accepts on prompt-adherence, delivery/tonality, framing, comedic timing, Meta compliance | outputs: ~8s vertical 9:16 hook clips | owner/tool: ChatGPT Prompts 3-5 (Scene Gen/Selector + Sora Scene Builder), Sora 2 / fal.ai — *[04-end-to-end-sop.md]*

- **STAGE 5. Edit + deliver** | inputs: raw hook clips + original ad body | gate: full watch-through with fresh eyes, no audio clipping, watermark gone | outputs: 3 final 1080p mp4 ads in shared Google Drive folder + setup guide | owner/tool: removesorawatermark.online, CapCut — *[04-end-to-end-sop.md]*

- **STAGE 6. Test setup** | inputs: 4 ads (original control + 3 new) | gate: all paused-green before edits, $25/ad-set budget, every Advantage+ enhancement OFF | outputs: 1 campaign / 4 identical ad sets live at $100/day for 7 days | owner/tool: Meta Ads Manager — *[04-end-to-end-sop.md, 07-media-buying-testing-scaling.md]*

- **STAGE 7. Result + upsell** | inputs: 7-day head-to-head data | gate: clear winner determined | outputs: refund $300 (loss) OR close $3k 5x5 package (win) | owner/tool: Stripe, results review call — *[04-end-to-end-sop.md]*

---

## Statics path — image ads (parallel track)

- **STAGE Brief** | inputs: 6C Intel Report OR raw offer/brand material | gate: avatar + VOC + offer + angles present (or run QUICK BRIEF on-ramp, tag guesses [GUESS]) | outputs: tight labelled one-pager brief | owner/tool: Claude — *[06-statics-playbook.md]*

- **STAGE Path A — Swipe Find** | inputs: niche/client | gate: image format + still live + 30+ days + English + FB/IG, sort by longest-running | outputs: swipe board of 10-20 proven winners | owner/tool: Foreplay (Basic $59/mo) or GetHookd / Meta+TikTok Ad Library — *[06-statics-playbook.md]*

- **STAGE Path A — Teardown + Rebuild** | inputs: brand docs + a pasted winning ad | gate: 3 passes complete (Pass1 why-it-wins / Pass2 how-we-rebuild / Pass3 the prompt) | outputs: one copy-paste Nano Banana prompt + 2 alt headlines, tagged to one of 5 formats | owner/tool: Claude — *[06-statics-playbook.md]*

- **STAGE Path B — From-Scratch Concepts** | inputs: brand docs | gate: 25 genuinely-different concepts spanning angle/emotion/awareness, each 3-part (FORMAT / HOOK / PROMPT) | outputs: copy-paste Nano Banana prompts, 4:5, text centered, --ar 4:5 | owner/tool: Claude — *[06-statics-playbook.md]*

- **STAGE Generate** | inputs: Claude prompt + background-stripped product PNG (product shots) | gate: 4:5 canvas, 2K, 4 generations/batch; text legible (regen or Claude/Gemini text-fix if glitched) | outputs: 4 image variations per prompt | owner/tool: Higgsfield (Plus) + Nano Banana Pro; Adobe Express for BG removal — *[06-statics-playbook.md]*

- **STAGE QA before launch** | inputs: generated statics | gate: text legible + spelled, on-brand + product correct, NO graphic weight-loss before/afters (account-kill risk) | outputs: launch-ready labelled creatives (label by format + hook, e.g. INFO 1 / NEWS 3) | owner/tool: manual review — *[06-statics-playbook.md]*

- **STAGE Route the click** | inputs: launched static | gate: direct format -> product page/checkout; indirect format -> advertorial article then product | outputs: matched funnel destination (draft 1-line advertorial angle per native static) | owner/tool: Meta Ads Manager — *[06-statics-playbook.md]*

---

## Launch, iterate, feedback (shared close — Meta-specific)

- **STAGE Economics gate** | inputs: offer + funnel math | gate: none (vibe check) — he sets a Target Cost Per Result and a 3:1 30-day LTV:CAC scale threshold, but it is a judgment call, not a hard stop | outputs: TCPR per campaign | owner/tool: spreadsheet / Meta Ads Manager — *[07-media-buying-testing-scaling.md]*

- **STAGE Test + kill** | inputs: launched ads | gate: let each ad spend 3x TCPR before keep/kill (early-kill only "clear disasters" at ~5x TCPR with no signs of life) | outputs: kept winners, killed losers | owner/tool: Meta Ads Manager — *[07-media-buying-testing-scaling.md]*

- **STAGE Scale** | inputs: ad set at/under TCPR | gate: vertical = raise budget 20-30%/day, once per day; horizontal = duplicate at 50-100% budget | outputs: scaled spend on winners | owner/tool: Meta Ads Manager — *[07-media-buying-testing-scaling.md]*

- **STAGE Fatigue rotation** | inputs: a former winner | gate: rotate when ALL fire — frequency > 3, 7-day CPL/CPA 30%+ worse than prior 30-day, thumbstop/CTR/watch-time down | outputs: 1-3 fresh variations of the same angle | owner/tool: Meta Ads Manager — *[07-media-buying-testing-scaling.md]*

- **STAGE Feedback loop** | inputs: per-ad performance + ad comments | gate: none (vibe check) — weekly he keeps top 3-5, adds 2-3 tests, pauses 2-3 worst; mix next batch 80% proven-iterations / 20% fresh | outputs: next creative batch brief; comment objections feed new copy | owner/tool: Meta Ads Manager, comment mining, Motion (optional) — *[07-media-buying-testing-scaling.md, 03-angles-hooks-copy.md]*

---

## Notes on the gates

His system is creative-led and structure-light. The hard, formal gates cluster early (form complete, 3 research docs accuracy-checked, hook clarity, watch-through, $25/all-green test setup) and in the kill rule (3x TCPR). The economics and feedback stages run on judgment, not a checklist — marked "vibe check" above so nobody invents precision he never gave. No stance exists on CBO vs ABO or bid strategy *[07-media-buying-testing-scaling.md]*.
