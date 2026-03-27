## Graph Links
- **Parent skill:** [[paid-media-audit]]
- **Sibling references:** [[audit-checklist]], [[dom-selectors]]
- **Related skills:** [[paid-advertising]], [[analytics-attribution]]

# Creative Analysis Prompts

Multimodal analysis prompts for competitor ad creatives and landing pages. Use with Claude's vision capabilities or Gemini Files API for video analysis.

## Video Ad Analysis Prompt

```
You are an expert ads analyst and media buyer. Analyze this video ad in detail.

1. **Hook (first 3 seconds):** What stops the scroll? What do you see AND hear immediately? Is it pattern-interrupt, curiosity gap, bold claim, or something else?
2. **Script/Voiceover:** Transcribe the full spoken content verbatim. Note tone, pacing, and delivery style.
3. **Visual Approach:** Describe the visual style and how it evolves through the ad. Categories: talking head, UGC/testimonial, b-roll, motion graphics, screen recording, text-on-screen, mixed. Note transitions, text overlays, and any branded elements.
4. **Emotional Angle:** What primary emotion drives this ad? (fear of missing out, aspiration, curiosity, pain/frustration, social proof, urgency, authority, belonging). How is it established?
5. **CTA:** What specific action are they driving? How is it presented (verbal, text overlay, button, end card)? What's the friction level (free vs paid, quiz vs purchase)?
6. **Ad Format:** Aspect ratio (9:16, 1:1, 16:9), estimated duration, platform optimization (captions, safe zones, sound-on vs sound-off friendly).
7. **What Makes It Work:** 2-3 specific tactical takeaways. Why would this ad outperform? What can a marketing team replicate?
8. **Weaknesses:** What could be improved? Be specific and actionable.

Be direct and tactical — this analysis is for a marketing team studying competitor ads, not a general audience.
```

## Image Ad Analysis Prompt

```
You are an expert ads analyst and media buyer. Analyze this image ad in detail.

1. **First Impression:** What's the immediate visual hierarchy? Where does the eye go first? What stops the scroll?
2. **Copy:** Transcribe ALL text in the creative. Note headline vs body vs CTA text hierarchy.
3. **Visual Approach:** Style (photography, illustration, graphic design, UGC, meme-style, screenshot). Color palette, typography choices, use of faces/people, brand elements.
4. **Emotional Angle:** What primary emotion does this creative trigger? How — through imagery, copy, or both?
5. **CTA:** What action is implied or stated? Button text, urgency elements, friction level.
6. **Ad Format:** Dimensions/aspect ratio, platform optimization (text density for Facebook's old 20% rule, safe zones).
7. **What Makes It Work:** 2-3 specific tactical takeaways.
8. **Weaknesses:** What could be improved?

Be direct and tactical — this is for a marketing team, not a general audience.
```

## Comparative Analysis Prompt

Use after analyzing individual ads from the same advertiser. Provide summaries of each ad analyzed, then:

```
You are an expert ads analyst reviewing multiple ads from the same advertiser. Based on the individual analyses provided, identify:

1. **Creative Patterns:** What elements repeat across their ads? (visual style, hooks, emotional angles, CTA types)
2. **Testing Strategy:** What are they likely A/B testing? (different hooks for same offer? different audiences? different formats?)
3. **Funnel Consistency:** Do all ads drive to the same destination/offer, or are they running multiple funnels?
4. **Top Performer Signals:** Based on the creative quality and approach, which ad likely performs best and why?
5. **Lessons for Our Ads:** 3-5 specific, actionable takeaways we can apply to our own ad creative.

Be specific. Reference individual ads by number when making comparisons.
```

## Landing Page Analysis Prompt

Use with full-page screenshot + page snapshot text content:

```
You are an expert CRO specialist and funnel strategist. Analyze this landing page screenshot in detail.

Context: This page is the destination of a paid ad. Analyze it from the perspective of a visitor who just clicked an ad and landed here.

1. **Above the Fold:** What does the visitor see immediately without scrolling? Headline, subheadline, hero image/video, primary CTA. Is it clear what this page is about within 3 seconds?
2. **The Offer:** What exactly is being offered? Type (free resource / quiz / webinar / demo / trial / course / product / consultation). Value proposition. Price/friction level.
3. **Social Proof:** Testimonials, company logos, numbers, case studies, trust badges.
4. **Copy Strategy:** Tone, pain points vs benefits, specificity level, reading level.
5. **CTA Strategy:** Number of CTAs, text, form fields, urgency elements, button color/contrast.
6. **Visual Design:** Layout style, color palette, imagery, whitespace, mobile signals.
7. **Funnel Position:** TOFU / MOFU / BOFU? What's the likely next step after conversion?
8. **What Works:** 2-3 specific well-executed elements.
9. **Weaknesses:** 2-3 specific areas for improvement.

Be direct and tactical — this analysis is for a marketing team studying competitor funnels.
```

## Quick Landing Page Analysis

For faster, lighter analysis:

```
Analyze this landing page in 5 bullet points:
1. What's the offer? (one sentence)
2. What's the CTA? (button text + friction level)
3. What social proof is used?
4. What's the strongest element?
5. What's the weakest element?
```
