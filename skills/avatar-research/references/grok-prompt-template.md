# Grok Research Prompt Template

> Grok excels at: X/Twitter search, Reddit sentiment, unfiltered social opinions, real language people use.
> Use for: points 2, 3, 6, 7, 8 of the avatar breakdown + language mining for messaging guidance.

---

## Template (fill placeholders, then copy-paste to Grok)

```
Search X/Twitter, Reddit, and social media for real conversations from {avatar_description} in {geography} discussing {problem_domain}.

I need raw, unfiltered data for building an advertising avatar. Don't be polite — give me the brutal truth about what these people actually say, feel, and believe.

**Context:** I'm creating Meta ads for {product_description} targeting {avatar_description} in {geography}.

**What I need:**

1. **Real language they use** — Search for posts, threads, and comments from this audience discussing {problem}. What exact phrases, slang, and expressions do they use? Not marketing language — their actual words.

2. **Frustrations and struggles** — What are they complaining about daily? What posts get the most engagement? What makes them rant?

3. **What image they project** — How does this demographic present themselves publicly on social media in {geography}? What do they brag about, show off, or signal?

4. **Beliefs and objections** — What objections come up repeatedly when people discuss {product_category}? What are the "everyone knows" assumptions that prevent action? Search for phrases like "it's not worth it because...", "the problem with...", "I tried X and..."

5. **Failed solutions discussed** — What solutions has this audience mentioned trying? What were their specific complaints? Search for negative experiences with {competing_solutions}.

6. **Sentiment about {product_category}** — Is the general sentiment positive, negative, or mixed? Are they cynical, hopeful, or frustrated? What's the vibe?

7. **Cultural context** — For {geography} specifically, what cultural factors affect how this audience makes decisions about {problem_domain}? Family pressure, social expectations, religious considerations, economic anxiety?

8. **Language to borrow** — Give me 10-15 exact phrases or sentence fragments from real posts that capture how this audience FEELS about {problem}. These should be raw, emotional, and specific enough to use in ad copy.

9. **Language to avoid** — What words, phrases, or framings trigger a negative reaction from this audience? What makes them scroll past or leave angry comments?

Search r/{relevant_subreddit}, X/Twitter for {search_terms}, and any {geography}-specific forums or communities.

Be brutal. I need the truth, not the sanitised version.
```

## Placeholder Guide

| Placeholder | Fill with | Source |
|------------|-----------|--------|
| `{geography}` | e.g., "Singapore" | icp.md |
| `{avatar_description}` | Avatar hypothesis | Phase 1 |
| `{problem_domain}` | Core problem area | buyer-profile.md |
| `{product_description}` | One-line offer | offer.md |
| `{problem}` | Specific problem | Phase 1 hypothesis |
| `{product_category}` | Industry/category | offer.md |
| `{competing_solutions}` | Known competitors | swipe-file.md or user input |
| `{relevant_subreddit}` | e.g., "singapore, singaporefi" | icp.md → Where They Congregate |
| `{search_terms}` | category-specific search terms — examples: SaaS = "team collaboration tool", ecom = "skincare for sensitive skin", service = "wedding photographer NYC", info = "youtube growth course" | From problem domain |
