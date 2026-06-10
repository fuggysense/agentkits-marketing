---
name: Reddit Research Patterns — Singapore Property
description: ScrapeCreators API patterns and high-signal subreddits for SG property buyer language research
type: feedback
---

ScrapeCreators Reddit API — use `url=` not `post_id=` for the `/v1/reddit/post/comments` endpoint. Using `post_id` returns 400 "You must provide a url". Full Reddit URL works correctly.

The correct comments endpoint path is `/v1/reddit/post/comments` (not `/v1/reddit/post`). Using `/v1/reddit/post` returns "Not Found."

**Why:** Discovered during 260417 neezanizam refresh. `/v1/reddit/post` path tested on 260418 and confirmed still returns Not Found.

**How to apply:** Always use `/v1/reddit/post/comments?url=<full_reddit_url>` when fetching post comments.

### API key location
Key is NOT in environment by default. Find at:
`/Users/jerel/Documents/Jerel's brain/jerel's brain/Marketing/.env`
Key variable: `SCRAPECREATORS_API_KEY`

### High-signal subreddits for SG property buyer language
- `r/singaporefi` — most candid financial math discussions, upgrade decision posts, fear language. Best for Problem-Aware / Solution-Aware buyers. Also good for life-transition (divorce, grief, widow) posts.
- `r/singapore` — broader cultural sentiment, anti-agent narratives, wealth inequality framing. Good for Unaware / counter-narrative buyers.
- `r/askSingapore` — direct question-and-answer format. Best for divorce, inheritance, legal questions about HDB. Very SG-specific.
- `r/SingaporeRaw` — news/commentary on SG property disputes. Good for divorce + ABSD edge cases.
- `r/SingaporeRaw` — searched but low volume for life-transition content.

### Query patterns that surfaced gold
- `subreddit=singaporefi&query=HDB+upgrade+condo+EC+TDSR+CPF` → yields actual upgrade decision posts with real math
- `subreddit=singapore&query=property+agent+bad+experience+pressure` → yields anti-agent sentiment threads
- `subreddit=singaporefi&query=divorce+property+HDB+split` → yields divorce financial posts
- `subreddit=askSingapore&query=divorce+HDB+what+happens+property+split` → yields legal/procedural divorce questions
- `subreddit=singaporefi&query=spouse+died+HDB+sell+alone+financial+planning` → widow/bereavement posts (check for empty results; try `widow` variation)
- Global search (no subreddit) for specific post types tends to return non-SG posts — always filter by subreddit

### Low-signal sources (don't repeat)
- Global Reddit search for riba/halal/Shariah mortgage Singapore — zero results. Not a Reddit conversation.
- r/SingaporeRaw — low volume for life-transition property content.
- Empty-nest / adult children leaving home — zero SG-specific quotes found via Reddit API (260418 cycle). Use HardwareZone instead.
- Global search without subreddit filter for aging-parent HDB — returns non-SG posts only.

### Sophistication-stage diagnostic signal confirmed
When top-voted comments explicitly deconstruct agent-motivated advice ("Upgrading is key to building wealth - FOR THE PROPERTY AGENTS that sell you that spiel"), the category is Stage 3-4. Generic wealth-building claims have zero credibility. Need mechanism transparency or identity-level messaging.

### Life-transition segment — key search patterns (260418)
- `subreddit=singaporefi&query=divorce+property+HDB+split` → 25 posts, 4 SG-specific with text
- `subreddit=askSingapore&query=divorce+HDB+what+happens+property+split` → 25 posts, 5 SG-specific with text
- `subreddit=singaporefi&query=spouse+died+HDB+sell+alone` → 0 relevant (try `widow` or direct FIRE query)
- `subreddit=singaporefi&query=thinking+about+FIRE` → found the widow post via general FIRE search (not bereavement-specific query)
- Best single search for grief: look for FIRE posts that mention widowed/widower in body text

### Reddit search workflow — capped + tiered (260419 directive)

**Hard rule:** never exceed 10 broad `/v1/reddit/search` calls per research session. Yesterday burned ~30 broad search calls + 18 comment fetches = 48 credits, exhausting the ScrapeCreators account and blocking the ad-library work.

**Two-tier protocol:**
1. **Discovery (≤10 calls):** Broad `/v1/reddit/search?subreddit=<sub>&query=<terms>` to identify which subreddits surface SG-relevant content for the topic.
2. **Pause + confirm:** Show the user the unique subreddits found, get explicit confirmation on which ones to lock as canonical for this topic.
3. **Save:** Write the confirmed list to `.claude/agent-memory/buyer-language-researcher/subreddits_<topic>.md` so future sessions don't re-discover.
4. **Deep dive (no fixed cap, but justify each call):** Use the narrower endpoints:
   - `/v1/reddit/subreddit/search?subreddit=<sub>&query=<term>` — search within ONE confirmed subreddit
   - `/v1/reddit/post/comments?url=<full_url>` — only on posts that already showed promising titles in step 1; don't blanket-fetch.

**Why:** Each ScrapeCreators call is 1 credit (~$0.01-0.02). Untargeted broad searches yield mostly non-SG noise (see "Low-signal sources" above). Confirming the subreddit shortlist with the user before deep-diving cuts wasted credits AND keeps the user in the loop on research direction.

### Next recommended sources for Avatar 2 data gaps
1. HardwareZone property forum — empty-nest, aging-parent, Malay-language content
2. Facebook group search via dev-browser — "Singapore HDB/Property" groups for divorce and inheritance posts
3. Direct URL fetch on known HardwareZone threads via WebFetch
