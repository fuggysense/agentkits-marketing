# ChatGPT Research Prompt Template

> ChatGPT excels at: psychological synthesis, expanding from existing data, generating structured frameworks, exploring emotional nuance.
> Use for: points 3, 4, 5, 6, 11, 12 of the avatar breakdown + the Messaging Guidance section.

---

## Template (fill placeholders, then copy-paste to ChatGPT)

```
I'm building a detailed advertising avatar for a specific buyer sub-segment. I already have a deep buyer psychology profile (pasted below). I need you to generate a COMPLETE 12-point avatar breakdown for a specific sub-segment of this buyer.

## Existing Buyer Psychology (foundation layer)

{buyer_profile_excerpt}

## The Specific Avatar I Need You to Build

**Avatar name:** {avatar_name}
**Description:** {avatar_description}
**What makes them different from the general buyer:** {differentiator}
**Their Schwartz awareness level:** {awareness_level}
**Their market sophistication level:** {sophistication_level}

## Product/Service Context

{offer_excerpt}

## Your Task

Generate the complete 12-point avatar breakdown for THIS specific sub-segment. Do NOT just repeat the general buyer profile — go DEEPER and NARROWER for this particular person.

For each point, I need:
- Specificity (not "they're worried about money" but "they check their CPF balance every Sunday night")
- Emotional precision (not "they feel stuck" but "they feel like they're watching everyone else move forward while they stay in the same flat")
- Behavioral detail (not "they research online" but "they have 14 PropertyGuru tabs open and compare the same 3 listings every week")

### The 12 Points:

1. **Demographics** — Age, gender, location, income SPECIFIC to this sub-segment
2. **Day-to-day struggles** — Their concrete daily reality. What they do, think, and feel about {problem_domain} on a Tuesday afternoon
3. **Image they project** — What they want others (spouse, parents, colleagues, friends) to see in them
4. **Status they aspire to** — Concrete markers of the life they want. Material, social, and identity-level
5. **How our product helps them achieve status** — The specific bridge from {product} to their desired status
6. **Beliefs we must overcome** — Top 3 beliefs preventing purchase. For each: the belief, why it exists, and the counter-evidence
7. **Other solutions tried** — What they've actually done to solve this problem. Be specific to {geography}
8. **Why those failed** — The specific failure mechanism for each (not just "it didn't work")
9. **Similar products considered** — What they've looked at or heard about
10. **Why those fell short** — Specific gap between what was promised and what was delivered
11. **Market awareness (Schwartz)** — Level + evidence + what this means for how we open ads targeting them
12. **Market sophistication** — Level (1-5) + evidence + what creative approach breaks through

### ALSO generate:

**Messaging Guidance:**
- Best angle types for this avatar (story, fear-validation, contrarian, data-led, etc.)
- 5-10 specific phrases to use (language that resonates with this sub-segment)
- 5-10 phrases to avoid (triggers, loaded terms)
- Which proof elements from our offer hit hardest for this avatar
- The REAL buying emotion (not the surface desire — the deeper trigger that causes action)
- How to position: what to sell and what NOT to sell to this person

**Characteristic Quote:**
Write a 2-3 sentence quote in this avatar's voice — what they'd say to their spouse at 11pm about this problem. This is the internal monologue our ad must intercept.

Be psychologically precise. Write like a therapist who also happens to be a world-class copywriter.
```

## Placeholder Guide

| Placeholder | Fill with | Source |
|------------|-----------|--------|
| `{buyer_profile_excerpt}` | Paste the Core Problem, Top 5 Emotions, Top 5 Fears, and Schwartz Map sections | buyer-profile.md |
| `{avatar_name}` | Working name from Phase 1 | Phase 1 hypothesis |
| `{avatar_description}` | 1-2 sentence description | Phase 1 hypothesis |
| `{differentiator}` | What makes this avatar distinct | Phase 1 hypothesis |
| `{awareness_level}` | Schwartz level | Phase 1 hypothesis |
| `{sophistication_level}` | 1-5 | Phase 1 hypothesis |
| `{offer_excerpt}` | Core Offer + Value Proposition + Proof Elements sections | offer.md |
| `{problem_domain}` | Core problem area | buyer-profile.md |
| `{product}` | Product/service name | offer.md |
| `{geography}` | Target market | icp.md |

## Tips for Best Results

- Paste the FULL buyer-profile excerpt (emotions, fears, relationships) — ChatGPT needs emotional depth to generate good sub-segments
- If the first output is too generic, reply: "Go deeper on points 2, 3, and 6. I need behavioral specificity, not marketing language."
- If it misses cultural context, reply: "This person lives in {geography}. Factor in {cultural_context} from their perspective."
