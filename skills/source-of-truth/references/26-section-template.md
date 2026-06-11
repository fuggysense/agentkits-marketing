# 28-Section Source-of-Truth Template

This is the full template Phase 5 fills in and writes to `clients/<project>/source-of-truth.md`. Variables in `{{...}}` get replaced from research dossiers + Phase 1 intake + HITL answers.

> §1-26 are the original SoT spine. §27 (Says-vs-Addresses Gap Analysis) and §28 (Competitor Opportunity Matrix) are appended Ferres research-flow sections — see `_shared-knowledge/ferres/02-research-flow.md` prompts 1 and 2. They are numbered as 27/28 by design; the rest of the doc is NOT renumbered.

Section synthesis instructions live in `section-synthesis-frameworks.md` (per-section how-to).

---

# Paid Ads Source of Truth — {{project_name}}

> Generated: {{generated_date}} (SGT) | Mode: {{mode_a_b_c}} | Research sources: {{research_sources_count}} | Verbatim buyer quotes: {{quote_count}} | Competitor ads analysed: {{competitor_ad_count}}

**Purpose:** Internal operating reference for strategists, media buyers, copywriters, designers, and creative leads building direct-response paid ads. Aligns offer strategy, audience insight, messaging, creative production, testing, and iteration. Living document — update as new performance data comes in.

**Owners:**
- Strategist: positioning, buyer insight, messaging hierarchy
- Media buyer: paid objective, testing priorities, performance feedback
- Copywriter: hooks, scripts, objections, CTA language
- Designer / Editor / UGC: execution standards, visual patterns, creative adaptation
- Account lead: approvals, missing inputs, asset collection

---

## 1. Brand Snapshot

### Business Overview
- **Brand name:** {{brand_name}}
- **Website / landing page:** {{website_url}}
- **Category / niche:** {{category}}
- **Primary product type:** {{product_type}} (Physical / Digital / Service / Info / Subscription / App / Other)
- **Core offer being advertised:** {{core_offer}}
- **Price point / AOV:** {{price_point}}
- **Primary conversion event:** {{conversion_event}}

### Brand Context
- **What does the brand sell?** {{brand_sells}}
- **What problem does it solve?** {{brand_problem}}
- **What makes it different from alternatives?** {{brand_differentiator}}
- **Why does this offer exist now?** {{offer_timing}}
- **Brand maturity:** {{maturity_level}} (New / Growing / Established)

### Brand Constraints
- **Compliance limitations:** {{compliance}}
- **Platform policy considerations:** {{platform_policy}}
- **Claims we CAN make:** {{can_claims}}
- **Claims we CANNOT make:** {{cannot_claims}}
- **Visual brand rules:** {{visual_rules}}
- **Words / tones to avoid:** {{avoid_words}}

---

## 2. Paid Media Objective

> 🔵 **HITL-decided** — primary KPI confirmed via Phase 4 checkpoint

- **Primary KPI:** {{primary_kpi}} (CPA / ROAS / MER / CAC / CPL / AOV / LTV:CAC)
- **Secondary KPI(s):** {{secondary_kpis}}
- **Target benchmark(s):** {{target_benchmark}}
- **Conversion window:** {{conversion_window}}
- **Platform(s):** {{platforms}}

### Campaign Purpose
{{campaign_purpose}}

### Funnel Stage Focus
- **Cold traffic message priority:** {{cold_priority}}
- **Warm traffic message priority:** {{warm_priority}}
- **Hot traffic message priority:** {{hot_priority}}
- **Retargeting logic:** {{retargeting_logic}}

---

## 3. Product and Offer Details

### Product Snapshot
- **Product / offer name:** {{product_name}}
- **Category:** {{product_category}}
- **Format / delivery:** {{format}}
- **Price:** {{price}}
- **Variants / bundles / plans:** {{variants}}
- **Best-selling version:** {{best_seller}}
- **Margin sensitivity notes:** {{margin_notes}}

### Functional Breakdown
- **What is it?** {{what_is_it}}
- **How does it work?** {{how_it_works}}
- **How is it used / consumed / experienced?** {{usage}}
- **When does the buyer use it?** {{when_used}}
- **How quickly does the buyer perceive value?** {{time_to_value}}
- **What result does it help create?** {{result}}

### Offer Details
- **Core offer:** {{core_offer_detail}}
- **Bonus(es):** {{bonuses}}
- **Discount / promo structure:** {{promo}}
- **Guarantee / refund policy:** {{guarantee}}
- **Shipping / fulfillment:** {{fulfillment}}
- **Trial / freebie / lead magnet terms:** {{trial_terms}}
- **Urgency / scarcity mechanism:** {{urgency}}
- **Offer stack summary:** {{stack_summary}}

### Why This Offer Converts
- **Practical reason:** {{practical_reason}}
- **Emotional reason:** {{emotional_reason}}
- **Financial reason:** {{financial_reason}}
- **Why now instead of later:** {{why_now}}
- **Why this instead of alternatives:** {{why_this}}

---

## 4. Audience Profile

### Primary Audience
- **Main buyer:** {{main_buyer}}
- **Awareness level:** {{awareness}} (Problem / Solution / Product / Most aware / Unaware)
- **Why this awareness level:** {{awareness_reason}}
- **Traffic temperature priority:** {{temperature}}
- **Market sophistication level (1-5):** {{sophistication}}
  - {{sophistication_explanation}}

### Schwartz Sophistication Stage Map
| Stage | Market Situation | Prospect Awareness & Sentiment | Marketing Strategy |
|---|---|---|---|
| 1: State the Claim | {{stage_1_market}} | {{stage_1_aware}} | {{stage_1_strategy}} |
| 2: Exaggerate the Claim | {{stage_2_market}} | {{stage_2_aware}} | {{stage_2_strategy}} |
| 3: New Mechanism | {{stage_3_market}} | {{stage_3_aware}} | {{stage_3_strategy}} |
| 4: Elaborate the Mechanism | {{stage_4_market}} | {{stage_4_aware}} | {{stage_4_strategy}} |
| 5: Identification | {{stage_5_market}} | {{stage_5_aware}} | {{stage_5_strategy}} |

### Segment Breakdown (1-5 segments)

| Segment | Who they are | Main problem | Buying trigger | Biggest objection | Best angle |
|---|---|---|---|---|---|
{{segment_table_rows}}

### Audience Reality Notes
- **What are they already trying to achieve?** {{trying_to_achieve}}
- **What have they already tried?** {{already_tried}}
- **How skeptical are they?** {{skepticism}}
- **Language they use to describe the problem:** {{problem_language}}
- **Objections that show up before click:** {{pre_click_objections}}
- **Objections after click:** {{post_click_objections}}
- **What would make them instantly pay attention?** {{attention_trigger}}
- **What makes them scroll past?** {{scroll_trigger}}

---

## 5. Buyer Profile Extraction

> Synthesised using `avatar-research` Phase 1.5 framework applied to research dossiers. Verbatim buyer quotes preserved.

### Source Inputs Used
{{source_inputs_list}}

### Buyer Profile Framework (14 dimensions)

#### 1. Demographic Persona
{{dim_1_demographic}}

#### 2. Core Problem
{{dim_2_problem}}

#### 3. Top Emotions
{{dim_3_emotions}}

#### 4. Fears
{{dim_4_fears}}

#### 5. Relationship Impacts
{{dim_5_relationships}}

#### 6. Past Solutions Tried
{{dim_6_past_solutions}}

#### 7. What They Don't Want to Do
{{dim_7_dont_want}}

#### 8. Perfect Solution Outcome
{{dim_8_perfect_outcome}}

#### 9. Transformation Effects
{{dim_9_transformation}}

#### 10. Market Specifics
{{dim_10_market}}

#### 11. What Success Hinges On
{{dim_11_success_factors}}

#### 12. What They Must Give Up
{{dim_12_give_up}}

#### 13. Who They Blame
{{dim_13_blame}}

#### 14. Top General Objections
{{dim_14_objections}}

### Buyer Profile Summary Table
| Category | Notes |
|---|---|
| Dominant buyer | {{summary_dominant}} |
| Core problem | {{summary_problem}} |
| Top emotions | {{summary_emotions}} |
| Main fears | {{summary_fears}} |
| Relationship impacts | {{summary_relationships}} |
| Past solutions tried | {{summary_past}} |
| What they don't want to do | {{summary_dont_want}} |
| Perfect outcome | {{summary_outcome}} |
| Transformation effects | {{summary_transformation}} |
| Market specifics | {{summary_market}} |
| What success hinges on | {{summary_hinges}} |
| What they must give up | {{summary_give_up}} |
| Who they blame | {{summary_blame}} |
| Top objections | {{summary_objections}} |

### Buyer Language Bank (verbatim)
- **How they describe the problem:** {{lang_problem}}
- **How they describe what they've tried:** {{lang_tried}}
- **What they are tired of:** {{lang_tired}}
- **What they want instead:** {{lang_want}}
- **Why they hesitate:** {{lang_hesitate}}
- **What would convince them:** {{lang_convince}}

### §5.5 Golden Nuggets (curated verbatim — swipe-file ready)

> Standalone curated bank of buyer quotes. Different from the Language Bank: these are the *publishable-as-ad-copy* gems. Filtered to ICP relevance, traceable to source.
>
> Categories: Frustration · Skepticism · Humor/sarcasm · Hopelessness · DIY struggle · "Holy grail" descriptions

| # | Quote (verbatim or natural-rewritten) | Category | Source | Ad-copy use |
|---|---|---|---|---|
{{golden_nuggets_table_rows}}

**Rewriting rule:** if the verbatim quote is too clunky for ad copy, rewrite using the tone documented in §5.7 (slang, contractions, emotional phrasing). Never invent quotes. Mark `[verbatim]` or `[rewritten from: <source>]`.

### §5.7 ICP Language Analysis (consolidated)

> Single-source tone/style/vocabulary guide for any copywriter touching this brand. Synthesised from the Language Bank + Golden Nuggets.

- **Tone:** {{icp_tone}} (formal vs informal, polite vs raw, peer-to-peer vs aspirational)
- **Emotional style:** {{icp_emotional_style}} (skeptical / stressed / proud / fed up / hopeful / resigned / etc.)
- **Vocabulary they use:** {{icp_vocab_use}} (specific jargon, slang, brand names they mention)
- **Vocabulary they reject:** {{icp_vocab_reject}} (corporate-register words that signal "marketing slop" to them)
- **Sentence-length default:** {{icp_sentence_length}} (short staccato vs long unspooling vs mixed)
- **Punctuation tells:** {{icp_punctuation}} (lowercase-only? excessive periods? em-dashes? all-caps emphasis?)
- **Copywriting tips (how to speak exactly like them):** {{icp_copywriting_tips}}

### Creative Strategy Implications
- **Best emotional entry points:** {{entry_emotional}}
- **Best practical entry points:** {{entry_practical}}
- **Strongest hooks to test:** {{strongest_hooks}}
- **Most important objections to answer:** {{key_objections}}
- **Most persuasive forms of proof:** {{persuasive_proof}}
- **Best CTA direction:** {{cta_direction}}
- **Biggest messaging mistakes to avoid:** {{messaging_mistakes}}

---

## 6. Pain Points and Emotional Drivers

### Functional Pain Points (ranked by frequency in research)
1. {{pain_1}}
2. {{pain_2}}
3. {{pain_3}}
4. {{pain_4}}
5. {{pain_5}}

### Emotional Pain Points
- **Frustrated because:** {{emo_frustrated}}
- **Embarrassed because:** {{emo_embarrassed}}
- **Anxious because:** {{emo_anxious}}
- **Overwhelmed because:** {{emo_overwhelmed}}
- **Guilty because:** {{emo_guilty}}
- **Skeptical because:** {{emo_skeptical}}

### Desired Emotional States
{{desired_states}}

### Emotional Driver Prioritisation
| Driver | Why it matters | Best use in ads |
|---|---|---|
| Relief | {{relief_why}} | {{relief_use}} |
| Confidence | {{confidence_why}} | {{confidence_use}} |
| Convenience | {{convenience_why}} | {{convenience_use}} |
| Status / identity | {{status_why}} | {{status_use}} |
| Fear of staying stuck | {{stuck_why}} | {{stuck_use}} |
| Saving time | {{time_why}} | {{time_use}} |
| Saving money | {{money_why}} | {{money_use}} |
| Simplicity | {{simplicity_why}} | {{simplicity_use}} |

---

## 7. Objections

### Core Objection Categories (in buyer's real words)
- **Price:** {{obj_price}}
- **Trust:** {{obj_trust}}
- **Fit:** {{obj_fit}}
- **Timing:** {{obj_timing}}
- **Effort / Complexity:** {{obj_effort}}
- **Proof:** {{obj_proof}}
- **Alternative comparison:** {{obj_alt}}

### Objection Handling Table
| Objection | Root cause | Best proof / answer | Where to address |
|---|---|---|---|
{{objection_table_rows}}

### §7.5 Misconceptions

> Wrong beliefs the audience holds (different from objections — objections = "I won't buy because X"; misconceptions = "I think X is true and it's not"). Reframing these is often the highest-leverage copy work.

| Misconception | Clarification (correct understanding, written simply) | Ad use |
|---|---|---|
{{misconceptions_table_rows}}

---

## 8. Proof Assets

### Available Proof Inventory
{{proof_inventory_list}}

### Proof Inventory Table
| Proof Asset | What it proves | Strength | Best ad use |
|---|---|---|---|
{{proof_table_rows}}

### Proof Gaps
- **What we still need:** {{proof_gaps}}
- **What proof would most improve conversion:** {{proof_priority}}
- **What weak claims need stronger evidence:** {{proof_weak_claims}}
- **What objections currently lack proof support:** {{proof_unsupported_objections}}

---

## 9. Messaging Hierarchy

> 🔵 **HITL-decided** — core message confirmed via Phase 4 checkpoint

### Core Message
{{core_message}}

### Supporting Messages
1. {{supporting_1}}
2. {{supporting_2}}
3. {{supporting_3}}
4. {{supporting_4}}
5. {{supporting_5}}

### Message Prioritisation by Funnel Stage
| Funnel Stage | Message Priority | Goal |
|---|---|---|
| Cold | {{cold_msg}} | Stop scroll + create relevance |
| Warm | {{warm_msg}} | Build belief + reduce skepticism |
| Hot | {{hot_msg}} | Remove final friction + convert |
| Retargeting | {{retarget_msg}} | Reopen consideration + resolve objection |

### Message Ladder
1. **Attention:** {{ladder_attention}}
2. **Problem relevance:** {{ladder_problem}}
3. **Solution mechanism:** {{ladder_mechanism}}
4. **Proof:** {{ladder_proof}}
5. **Offer:** {{ladder_offer}}
6. **CTA:** {{ladder_cta}}

---

## 10. Ad Angles

> 🔵 **HITL-decided** — top 3 priority angles confirmed via Phase 4 checkpoint

### Angle Categories

**Problem-Aware Angles**
{{problem_aware_angles}}

**Desire-Led Angles**
{{desire_angles}}

**Product-Led Angles**
{{product_angles}}

**Offer-Led Angles**
{{offer_angles}}

**Proof-Led Angles**
{{proof_angles}}

**Contrarian / Pattern Interrupt Angles**
{{contrarian_angles}}

### Angle Development Table
| # | Angle Name | Core idea | Buyer segment | Best format | Risk / note | Priority |
|---|---|---|---|---|---|---|
{{angle_table_rows}}

**Top 3 priority angles to test first** (from Phase 4 checkpoint):
1. {{priority_angle_1}}
2. {{priority_angle_2}}
3. {{priority_angle_3}}

---

## 11. Hook Library

### Hook Types

**Direct Problem Hooks**
{{direct_hooks}}

**Desire Hooks**
{{desire_hooks}}

**Proof Hooks**
{{proof_hooks}}

**Contrarian Hooks**
{{contrarian_hooks}}

**Offer Hooks**
{{offer_hooks_list}}

### Hook Writing Grid
| Hook | Angle | Awareness level | Funnel stage | Format |
|---|---|---|---|---|
{{hook_grid_rows}}

---

## 12. Format-Specific Structures

> Static reference — loaded from `paid-advertising` + `ad-concept-engine` knowledge.

### Static Image Ads
**Best for:** Fast message testing · Offer-led ads · Problem/solution framing · Simple proof snapshots
**Structure:** Hook headline → Visual proof / product relevance → 1 core benefit → Optional trust element → CTA

### Carousel Ads
**Best for:** Education · Objection handling · Step-by-step transformation · Product comparisons · Testimonial storytelling
**Card flow:** Scroll-stopping opener → Problem → Why alternatives fail → Solution / mechanism → Proof → Offer → CTA

### UGC Video Ads
**Best for:** Relatability · Buyer-language resonance · Native platform feel · Objection handling
**Structure:** Hook (1-3 sec) → Problem recognition → Personal context → Discovery / solution intro → Why different → Results → CTA

### Founder / Expert Video Ads
**Best for:** Trust · Authority · Mechanism explanation · Reframing · Market education
**Structure:** Pattern interrupt → Core problem / false belief → Explanation → Solution → Proof → CTA

### Demo / Product Showcase Ads
**Best for:** E-commerce · Functional products · Visual proof · "How it works" · Use-case clarity
**Structure:** Show product in action → Overlay problem/benefit → Demonstrate differentiators → Trust proof → CTA

### VSL / Long-Form Direct Response
**Best for:** Info products · Higher-ticket offers · Complex products · Strong objection-handling needs
**Structure:** Big promise / problem → Empathy + credibility → Reframe → Mechanism → Offer → Proof + objection handling → Urgency / CTA

---

## 13. Script Framework

### Universal Direct-Response Script
1. **Hook:** stop the scroll fast
2. **Identify the problem:** make the viewer feel seen
3. **Agitate / contextualise:** why this matters now
4. **Introduce solution:** present the product/offer clearly
5. **Differentiate:** why this is not the same as alternatives
6. **Proof:** show evidence
7. **Outcome:** make the result tangible
8. **CTA:** tell them exactly what to do next

### Short-Form Script Template
- Hook: {{short_hook}}
- Problem callout: {{short_problem}}
- Relatable context: {{short_context}}
- Solution intro: {{short_solution}}
- Why it works / key differentiator: {{short_differentiator}}
- Proof: {{short_proof}}
- Outcome: {{short_outcome}}
- CTA: {{short_cta}}

### UGC Testimonial Script Template
"I was dealing with..." → "I had already tried..." → "What made me skeptical was..." → "What was different about this was..." → "After using it..." → "What I noticed most was..." → "If you're struggling with [problem], try [offer]."

### Founder Script Template
"Here's the mistake most people make when it comes to [problem]." → "The real issue is..." → "That's exactly why we created [product]." → "It's designed to..." → "What makes it different is..." → "Here's proof..." → "If you want [result], [CTA]."

---

## 14. Motion and Visual Guidance

### Visual Priorities
- Show product / offer relevance immediately
- Make problem recognisable
- Visuals support the claim, not distract from it
- Clarity over polish for native/direct-response feel
- Movement in first seconds to earn attention

### E-Commerce Visual Guidance
{{ecom_visual_guidance}}

### Info Product / Service / Offer Visual Guidance
{{info_visual_guidance}}

### Editing Notes
- Strong first-frame movement · Fast pacing early · On-screen text for core message · Captions always · Cut filler · Intentional zooms / punch-ins / pattern interrupts · Show proof at moment belief is needed

### Visual Do / Don't
**Do:** Make product obvious · Use buyer-relevant environments · Highlight transformation/utility · Match platform behaviour · Use text overlays that reinforce the hook
**Don't:** Hide product too long · Lead with abstract branding · Overstuff with claims · Use beautiful-but-irrelevant footage · Let editing overpower comprehension

---

## 15. CTA Library

### CTA Types
**Direct Purchase:** Shop now · Get yours today · Try it now · Order now · Choose your bundle · Start now
**Lead Generation:** Get the guide · Take the quiz · Book your call · Apply now · Get instant access · Reserve your spot
**Trial / Low-Friction:** Start your free trial · See how it works · Test it for yourself · Claim your offer · Get started today

### CTA Guidance by Funnel Stage
- **Cold:** low-friction, curiosity + relevance
- **Warm:** action-oriented + proof-supported
- **Hot:** direct-conversion CTA
- **Retargeting:** objection-resolving CTA

### CTA Testing Table
| CTA | Best for | Funnel stage | Notes |
|---|---|---|---|
{{cta_table_rows}}

---

## 16. Testing Framework

> 🔵 **HITL-decided** — first variable to test confirmed via Phase 4 checkpoint

### Testing Priorities (test biggest levers first)
1. Hook
2. Angle
3. Offer framing
4. Proof type
5. Format
6. CTA
7. Visual style
8. Script body variation

**First variable to test (Phase 4):** {{first_variable}}

### Creative Testing Matrix
| Variable | Test A | Test B | Test C | Success metric |
|---|---|---|---|---|
{{testing_matrix_rows}}

### Test Planning Table
| Test Name | Hypothesis | Variable | Audience | Platform | Funnel stage | KPI | Notes |
|---|---|---|---|---|---|---|---|
{{test_plan_rows}}

### Testing Rules
- Test one major variable at a time
- Don't judge winners early without enough spend
- Distinguish: scroll-stop problem · click problem · landing page problem · conversion problem
- Separate creative fatigue from offer breakdown
- Document why something won, not just that it won

### Interpreting Early Signals
- **Low thumbstop / hold rate:** hook or first-frame problem
- **Good CTR, weak CVR:** ad-promise vs page/offer mismatch
- **Strong engagement, weak qualified action:** interesting but not conversion-oriented
- **Strong post-click, weak scale:** needs broader angle variants or audience adaptation
- **Sharp drop after initial success:** fatigue / frequency / loss of novelty

---

## 17. Iteration Rules

### When to Iterate
{{when_to_iterate}}

### Iteration Levers
Rewrite hook · Change angle entry point · Swap proof type · Tighten pacing · Clarify product earlier · Reorder script beats · Strengthen CTA · Add comparison · Add objection handling · Improve visual evidence · Adjust first frame · Simplify message

### What NOT to Change All at Once
If an ad shows promise, avoid changing hook + angle + proof + offer + visual style at the same time.

### Iteration Decision Guide
| Scenario | Likely issue | Best next move |
|---|---|---|
| Low hold rate | Weak hook / first frame | Rewrite opening + change first visual |
| Good CTR, poor CVR | Message-to-offer mismatch | Align promise, strengthen proof, review page |
| Good CVR, weak CTR | Relevance problem | Test sharper hooks + broader entry points |
| Good performance, rising frequency | Fatigue | Refresh hook, visuals, creator angle |
| Strong saves/comments, weak conversions | Interest without buying intent | Clarify offer + shift CTA direction |

---

## 18. Performance Feedback Loop

### Review Cadence
- **Daily:** spend, CTR, thumbstop, hold rates, CPC, CPA
- **Weekly:** angle winners/losers, format trends, proof effectiveness, fatigue signals
- **Biweekly / monthly:** messaging shifts, audience saturation, new insight collection

### Feedback Questions per Cycle
- Which hooks earn attention? · Which angles drive qualified clicks? · Which ads convert best post-click? · Which proof improves trust? · Which objections keep repeating? · Which audience segments respond differently? · What patterns appear by format/platform? · What to scale, cut, rework?

### Learning Log Template
| Date | Creative | What happened | Why it likely happened | Next action |
|---|---|---|---|---|
{{learning_log_rows}}

### Scale / Cut / Rework Framework
| Outcome | Meaning | Action |
|---|---|---|
| Scale | Strong efficiency + clear signal | Increase spend + build variants |
| Rework | Promise but weak execution | Keep strategy, adjust creative |
| Cut | Low signal after sufficient testing | Stop, redirect budget |
| Hold | Inconclusive data | Gather more spend / isolate variable |

---

## 19. Client Asset Request Checklist

### Core Strategic Inputs
- [ ] Product / sales page · [ ] Offer details · [ ] Pricing & promo · [ ] Audience notes · [ ] Top FAQs · [ ] Customer reviews · [ ] Competitor references · [ ] Brand guidelines · [ ] Existing ad-account insights · [ ] Top past creatives · [ ] Claims/compliance guardrails

### Creative Assets
- [ ] Product footage · [ ] Lifestyle footage · [ ] UGC / raw customer videos · [ ] Testimonial screenshots · [ ] Founder videos · [ ] Product photos · [ ] Demo content · [ ] Packaging visuals · [ ] Logos / design files · [ ] Before/after assets (if compliant)

### Proof Assets
- [ ] Review exports · [ ] Survey data · [ ] Case studies · [ ] Press mentions · [ ] Expert validation · [ ] Certifications · [ ] Performance data · [ ] User-generated proof

### Asset Gap Table
| Missing asset | Why it matters | Impact on creative | Owner | Due date |
|---|---|---|---|---|
{{asset_gap_rows}}

---

## 20. AI Prompt for Creative Development

Reusable prompt for ad-concept-engine (Conductor Mode) or `/content:ads` runs against this doc:

```
You are a direct-response paid social copywriter.

Using the source-of-truth at clients/{{project_slug}}/source-of-truth.md, generate paid ad creative for a [PLATFORM] campaign.

INPUTS:
- Brand: {{brand_name}}
- Product / Offer: {{core_offer}}
- Primary objective: {{primary_kpi}}
- Funnel stage: [Cold / Warm / Hot / Retargeting]
- Target audience: see §4 + §5
- Buyer profile summary: see §5 Summary Table
- Top pain points: see §6
- Top desires: see §5 Perfect Outcome
- Main objections: see §7
- Key proof assets: see §8
- Core message: see §9
- Priority angles: {{priority_angle_1}}, {{priority_angle_2}}, {{priority_angle_3}}
- CTA goal: see §15
- Format requested: [STATIC / CAROUSEL / UGC / FOUNDER / DEMO / VSL]

OUTPUT:
1. 10 hooks
2. 5 angles
3. 3 high-converting scripts in the requested format
4. 5 CTA options
5. 10 objection-handling lines
6. Visual direction notes for each script

RULES:
- Write for conversion, not entertainment only
- Make the buyer feel recognised quickly
- Introduce product/offer early
- Use specificity over generic claims
- Reflect realistic buyer language (see §5 Buyer Language Bank — verbatim)
- Include proof naturally
- Match the funnel stage
- Avoid compliance-risky phrasing
- UK English spelling
```

---

## 21. Script QA Checklist

### Pre-Production QA
- [ ] Buyer is clear · [ ] Problem clear in first seconds · [ ] Offer understandable · [ ] Hook specific enough · [ ] Product introduced early · [ ] Angle distinct from other ads · [ ] Real proof present · [ ] At least one objection addressed · [ ] CTA clear · [ ] Aligned with funnel stage

### Production / Edit QA
- [ ] First frame strong · [ ] Movement early · [ ] Captions included · [ ] Key claims visually supported · [ ] Visual cuts help comprehension · [ ] Product visible enough · [ ] Pacing tight · [ ] Fluff removed

### Final Approval QA
- [ ] Matches strategy doc · [ ] On-brief · [ ] Compliance checked · [ ] CTA correct · [ ] Spelling/text overlays correct · [ ] Correct landing page mapped · [ ] Tests a clear hypothesis

### QA Failure Flags
- First line could apply to any product · Buyer implied but not obvious · Ad delays offer too long · Proof weak/vague/missing · CTA doesn't match funnel stage · Polished but not persuasive · Visual plan doesn't support core claim · Interesting but not conversion-driven

---

## 22. Strategy Summary (One-Pager)

> 🔵 **HITL-finalised** — review/edit pass after Phase 4

- **Brand / offer:** {{summary_brand}}
- **Primary objective:** {{primary_kpi}}
- **Main buyer:** {{summary_buyer}}
- **Main problem:** {{summary_main_problem}}
- **Core desire:** {{summary_desire}}
- **Top emotional driver:** {{summary_top_emotion}}
- **Primary objection:** {{summary_top_objection}}
- **Best proof asset:** {{summary_top_proof}}
- **Primary message:** {{core_message}}
- **Top 3 angles to test:**
  1. {{priority_angle_1}}
  2. {{priority_angle_2}}
  3. {{priority_angle_3}}
- **Top 3 hooks to test:**
  1. {{top_hook_1}}
  2. {{top_hook_2}}
  3. {{top_hook_3}}
- **Top format(s):** {{top_formats}}
- **Main CTA:** {{main_cta}}
- **Immediate asset gaps:** {{immediate_gaps}}
- **Next creative sprint focus:** {{next_sprint}}

### Strategy Alignment Check
- [ ] Buyer profile supports the messaging
- [ ] Messaging supports the angles
- [ ] Angles support the hooks and scripts
- [ ] Proof supports the claims
- [ ] CTA supports the funnel stage
- [ ] Landing page supports the ad's promise
- [ ] Test plan supports the current business objective

---

## 23. Quick-Start Fill Section

For team members who need just enough to act:

### Offer
- **Selling:** {{qs_selling}}
- **Price:** {{qs_price}}
- **Conversion goal:** {{primary_kpi}}
- **Why attractive now:** {{qs_now}}

### Buyer
- **Buying:** {{qs_buyer}}
- **Problem:** {{qs_problem}}
- **Already tried:** {{qs_tried}}
- **Want instead:** {{qs_want}}
- **Don't want to do:** {{qs_dont_want}}
- **Biggest objection:** {{qs_objection}}

### Messaging
- **Primary message:** {{core_message}}
- **Top 3 pain points:** {{qs_pains}}
- **Top 3 desires:** {{qs_desires}}
- **Top 3 objections:** {{qs_objections}}
- **Top 3 proof assets:** {{qs_proofs}}

### Creative Direction
- **Top 3 hooks:** {{top_hook_1}}, {{top_hook_2}}, {{top_hook_3}}
- **Top 3 angles:** {{priority_angle_1}}, {{priority_angle_2}}, {{priority_angle_3}}
- **Recommended format(s):** {{top_formats}}
- **Visual must-have(s):** {{qs_visual_musthave}}
- **CTA:** {{main_cta}}

### Testing
- **First variable to test:** {{first_variable}}
- **Second variable to test:** {{second_variable}}
- **Success metric:** {{primary_kpi}}
- **Kill / iterate rule:** {{kill_rule}}

---

## 24. Recommended Workflow for Teams

1. **Gather inputs** — product/offer, audience research, reviews, past performance, competitive context, visual assets, compliance constraints
2. **Complete Buyer Profile Extraction** (§5) — buyer reality, emotional drivers, fears, failed alternatives, objections, proof needs, messaging implications
3. **Build Messaging Hierarchy** (§9) — core message, supporting claims, priority angles, hook directions, proof-backed differentiators
4. **Create Test Plan** (§16) — formats, hypotheses, variables, KPIs, creative volume by angle
5. **Produce and Launch** — each ad maps to a clear hypothesis, tracking + naming clean, landing-page alignment checked
6. **Review and Iterate** — feed performance back into buyer understanding, objection map, proof requirements, angle prioritisation, new creative rounds

---

## 25. Naming Convention

**Format:** `Brand | Offer | Audience | Angle | HookType | Format | Stage | Version`

**Example:** `BrandX | Starter Bundle | New Customers | Problem-Aware | Contrarian | UGC | Cold | V3`

---

## 26. Final Notes

This document is not static. It functions as a living paid creative operating system.

**Used properly, it helps teams:**
- Reduce vague briefs
- Produce sharper direct-response creative
- Test with more intention
- Learn faster from performance
- Build stronger ad-to-offer alignment
- Scale what works with less guesswork

**Rule:** If a creative decision cannot be traced back to audience insight, offer logic, proof, or performance learning, it likely does not belong in the next testing round.

---

## 27. Says-vs-Addresses Gap Analysis

> What customers actually say in their own words vs what the client's current messaging actually addresses. The gap is the opportunity. Ferres bakes this into his ICP Deep Dive prompt — the deep-research run reads the client's sales page and ad scripts FIRST, then mines Reddit, reviews, and comment sections, then reports where the two diverge (`_shared-knowledge/ferres/02-research-flow.md` prompt 1; 04_part-3-how-to-create-winning-ads [00:20:13]).

Build this row by row from §5 Buyer Language Bank and §6 Pain Points (the "says" column) cross-checked against the client's live messaging — sales page copy, current ad scripts, landing page headlines (the "addresses" column). Pull the "says" side verbatim; never paraphrase a buyer into the gap table.

### Gap Table
| # | What customers say (verbatim + source) | What client messaging currently says | Gap type | Why it matters | Where to use it |
|---|---|---|---|---|---|
{{gap_analysis_rows}}

**Gap types:** `unaddressed` (customers raise it, client says nothing) · `mismatched` (client addresses it, but in different language than buyers use) · `over-indexed` (client leans hard on something buyers barely mention) · `buried` (client mentions it, but below the fold / late in the funnel).

### Top 3 Gaps to Close First
1. {{top_gap_1}}
2. {{top_gap_2}}
3. {{top_gap_3}}

> The "read their mind" bar (§Ferres operating principle 5): an ad earns the click when it repeats the buyer's exact phrasing back to them. Every `unaddressed` or `mismatched` gap is a hook waiting to be written. Feed the top 3 into §10 Ad Angles and §11 Hook Library on the next wave.

---

## 28. Competitor Opportunity Matrix

> Per-competitor read of where the category leaves room. Ferres' Competitor Analysis prompt outputs per-competitor profiles, saturation analysis, an opportunity matrix, and differentiation strategies — then he extends it with "give me a strategy to differentiate... a unique mechanism" (`_shared-knowledge/ferres/02-research-flow.md` prompt 2; 04_part-3-how-to-create-winning-ads [00:25:35]). His payoff: competitor reviews expose their weaknesses (big claims, thin proof) AND surface client advantages they aren't yet marketing — both go straight into the ads (06_part-5 [00:24:15], [00:24:35]).

Build from §7 Objections + the competitor-ads research (Phase 2 `scrapecreators` output) + competitor review mining. If an industry `stage-analysis.md` exists (from `ad-library-scraper`), pull its blue-box / blue-ocean findings into the matrix rather than re-deriving them.

### Per-Competitor Profile
| Competitor | Their core claim | Proof they show | Awareness/sophistication they target | Their weakness (from reviews) | Our counter |
|---|---|---|---|---|---|
{{competitor_profile_rows}}

### Opportunity Matrix
| Opportunity | Type | Who owns it now | Why it's open | Our angle to take it |
|---|---|---|---|---|
{{opportunity_matrix_rows}}

**Opportunity types:** `blue-box` (a claim every competitor makes — table stakes, match it, don't lead with it) · `blue-ocean` (a claim or mechanism NO competitor makes — lead here) · `weak-proof` (a claim competitors make but can't back — out-prove them) · `unmarketed-advantage` (something the client genuinely has that no competitor mentions).

### Differentiation Strategy
- **Unique mechanism to claim:** {{unique_mechanism}}
- **Strongest blue-ocean gap:** {{strongest_gap}}
- **Where every competitor is weak (out-prove them here):** {{shared_weakness}}
- **Client advantage to start marketing now:** {{unmarketed_advantage}}

> Saturation note: in a Stage 4-5 (exhausted) market, plain claims are dead — lead with the unique mechanism from this matrix, not the claim. Cross-check §4 sophistication before picking the differentiation lane.

---

## Appendix: Research Provenance

**Generated:** {{generated_date}}
**Skill version:** source-of-truth v1.0.0
**Mode:** {{mode_a_b_c}}

**Research sources:**
{{research_provenance_list}}

**Verbatim buyer quote count:** {{quote_count}}
**Competitor ads analysed:** {{competitor_ad_count}}
**Strategic checkpoint decisions (Phase 4):**
- §2 Primary KPI: {{primary_kpi}}
- §9 Core Message: {{core_message_summary}}
- §10 Priority angles: {{priority_angles_summary}}
- §16 First test variable: {{first_variable}}

**Refresh recommendation:** {{refresh_date}} (90 days from generation)
