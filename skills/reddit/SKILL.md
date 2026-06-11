---
name: reddit
version: "2.0.0"
brand: AgentKits Marketing by AityTech
category: research
difficulty: intermediate
description: "Reddit CLI: scrape, search, user, subreddit, trending, submission. No API key. 97-100% comment coverage, JSON + markdown output. Anonymous, 60 req/min. For buyer language discovery & competitive intel."
triggers:
  - reddit
  - reddit scrape
  - reddit search
  - reddit user
  - reddit subreddit
  - reddit trending
  - reddit submission
  - scrape reddit
  - reddit json
  - reddit comment tree
prerequisites: []
related_skills:
  - buyer-language-researcher
  - scrapecreators
  - deep-research
  - source-of-truth
agents:
  - researcher
  - buyer-language-researcher
mcp_integrations:
  optional: []
success_metrics:
  - coverage_vs_scrapecreators
  - cost_per_thread_usd
  - verbatim_quote_density
output_schema: reddit-thread-v1
---

# Reddit — Public JSON CLI (Scrape + Search + User + Subreddit + Trending)

> Unified Reddit CLI built on public `.json` endpoints. Six sub-commands cover extraction (deep comment trees with `more` stub resolution for 97-100% coverage), discovery (search), and intelligence (user + subreddit + trending). No API key. 60 req/min anonymous limit. User-Agent header required.

## Graph Links

- Feeds into: `[[buyer-language-researcher]]`, `[[deep-research]]`, `[[source-of-truth]]`
- Related: `[[scrapecreators]]` (paid alternative for Reddit + 70+ other platforms)
- Used by agents: `[[researcher]]`, `[[buyer-language-researcher]]`

## When to Use This Skill

- **Buyer-language extraction** — deep comment-tree scraping with full coverage (use `scrape`)
- **Discovery** — find threads about a topic, Reddit-wide or within a subreddit (use `search`)
- **User intel** — profile + comment/post history for a target Reddit user (use `user`)
- **Subreddit research** — health, size, activity, top posts (use `subreddit`)
- **Trend spotting** — what subreddits are gaining traction (use `trending`)
- **Single post metadata** — fetch one post without comment tree (use `submission`)

## When NOT to Use This Skill

- **Cross-platform** — anything beyond Reddit. Use `scrapecreators` skill.
- **Over-rate-limit runs** — if you need 200+ threads per hour, the 60 req/min anonymous limit is a hard ceiling. Use ScrapeCreators or upgrade to Tier 1 (PRAW, deferred).
- **Private / quarantined / NSFW opt-in subreddits** — anonymous JSON fails on these. Use ScrapeCreators or Tier 1.
- **Posting / replying** — Tier 2 (deferred, see Known Limitations).
- **Real-time streaming** — this is request/response, not push.

## How It Works

All sub-commands hit Reddit's public `.json` endpoints anonymously. No API key, no OAuth.

| Sub-command | Endpoint |
|---|---|
| `scrape` | `/r/{sub}/comments/{id}.json?limit=500&depth=100&sort=top` + `/r/{sub}/comments/{id}/_/{cid}.json` for `more` stub resolution |
| `search` | `/search.json?q=...` (Reddit-wide) or `/r/{sub}/search.json?q=...&restrict_sr=1` |
| `user` | `/user/{name}/about.json` + `/user/{name}/comments.json` + `/user/{name}/submitted.json` |
| `subreddit` | `/r/{name}/about.json` + `/r/{name}/top.json?t={time_filter}` |
| `trending` | `/subreddits/popular.json` |
| `submission` | `/comments/{id}.json` (no recursive tree walk) |

**Stub resolution (scrape only):** Reddit truncates comment trees at `limit=500` / `depth=100`. Anything beyond appears as `{"kind": "more", "data": {"children": [comment_id, ...]}}` stubs. `--resolve-stubs` walks each stub's child IDs recursively. Capped at `--max-stubs 200` by default.

## Invocation (CLI Sub-commands)

All commands from Marketing repo root. All accept `--output-dir <path>` (default: stdout JSON).

**`scrape` — deep comment tree (existing behavior):**
```bash
python3 scripts/reddit.py scrape --url https://www.reddit.com/r/singaporefi/comments/1abcdef/title/
python3 scripts/reddit.py scrape --subreddit singaporefi --post-id 1abcdef,1xyz123 \
    --output-dir "clients/neezanizam/research/raw" \
    --keywords "halal,riba,bto,upgrade" \
    --resolve-stubs --max-stubs 200
```

**`search` — Reddit-wide or per-subreddit:**
```bash
python3 scripts/reddit.py search "halal mortgage" --limit 25
python3 scripts/reddit.py search "bto upgrade" --subreddit singaporefi \
    --sort top --time year --limit 50 \
    --output-dir "clients/fuggysmedia/research/raw"
```
Flags: `--sort {relevance|hot|top|new|comments}` (default relevance), `--time {hour|day|week|month|year|all}` (default all), `--limit N` (default 25, max 100 per page).

**`user` — profile + activity history:**
```bash
python3 scripts/reddit.py user spez                           # about only
python3 scripts/reddit.py user spez --comments --limit 50     # + recent comments
python3 scripts/reddit.py user spez --posts --sort top --time year  # + top posts
python3 scripts/reddit.py user spez --comments --posts        # full dump
```

**`subreddit` — about + top posts:**
```bash
python3 scripts/reddit.py subreddit singaporefi                 # about only (stats)
python3 scripts/reddit.py subreddit singaporefi --top --time week --limit 25
```

**`trending` — popular subreddits:**
```bash
python3 scripts/reddit.py trending --limit 25
```

**`submission` — single post metadata (no comment tree):**
```bash
python3 scripts/reddit.py submission 1abcdef
python3 scripts/reddit.py submission https://www.reddit.com/r/sub/comments/1abcdef/title/
```

**From an agent (via Bash tool):** same invocation, `cd` into repo root first. Agent reads `-flat.md` outputs for synthesis; `-raw.json` is the full API response for re-filtering.

## Output Shape

Per post, two files:

**`{post_id}-raw.json`** — full API response trees:
```json
{
  "post": { "title": "...", "author": "...", "selftext": "...", "score": 42, ... },
  "comments": [
    { "kind": "t1", "data": { "author": "...", "body": "...", "replies": { ... } } },
    ...
  ]
}
```

**`{post_id}-flat.md`** — human-readable dump:
```markdown
# {Post title}

- **Subreddit:** r/{sub}
- **Author:** u/{author}
- **Posted:** YYYY-MM-DD HH:MM UTC
- **Score:** N · **Comments:** N
- **URL:** https://www.reddit.com/...

## Post Body
...

## Comments

- **u/{author}** · score {N} · YYYY-MM-DD HH:MM UTC
  > verbatim comment body line 1
  > verbatim comment body line 2

  - **u/{replier}** · score {N} · YYYY-MM-DD HH:MM UTC
    > nested reply verbatim

---
_Comments in output: {kept} / {total} total_
_Keyword filter: halal, riba, ..._
```

## Cost and Coverage vs ScrapeCreators

| Dimension | Reddit direct JSON (this skill) | ScrapeCreators Reddit |
|---|---|---|
| Cost per thread | Free | ~1 credit (~$0.01) |
| Rate limit | 60 req/min anonymous | Higher (authenticated) |
| Depth control | Full with `--resolve-stubs` | Limited — may truncate |
| Private subs | ❌ | ✓ if account has access |
| Cross-platform | ❌ Reddit only | ✓ 70+ platforms |
| Setup | None | API key |

**Break-even heuristic:** use ScrapeCreators when you need >60 threads/hour OR private-sub access OR cross-platform. Use this skill for focused per-thread research on public SG subreddits.

## Rate Limiting

Script sleeps 1.1s between requests (safely under the 60/min ceiling). Exponential backoff on 429/503 with up to 4 retries. For a thread with 200 `more` stubs resolved, expect ~4 minutes end-to-end. For a typical SG thread with 5-20 stubs, expect 30-90 seconds.

If multiple posts are scraped in sequence (batch mode), the total time = sum of per-post times + ~1s per request overhead. A 10-thread batch with modest stub resolution runs in ~8-15 minutes.

## Integration with buyer-language-researcher

The `buyer-language-researcher` agent (at `~/.claude/agents/buyer-language-researcher.md`) should prefer this scraper for Reddit-only research on SG subreddits (r/singapore, r/singaporefi, r/SingaporeRaw). Example prompt snippet for the agent:

```
For each target thread on public SG subreddit:
    cd "/Users/jerel/Documents/Jerel's brain/jerel's brain/Marketing" && \
    python3 scripts/reddit.py scrape \
        --url "<thread-url>" \
        --output-dir "clients/<project>/research/raw" \
        --keywords "<dimension-keywords>" \
        --resolve-stubs

Then read the {post_id}-flat.md files for verbatim quote extraction.
Fall back to ScrapeCreators for: private subs, discovery queries, cross-platform.
```

## Reference Files

- `references/rate-limits-and-etiquette.md` — Reddit API etiquette, robots.txt notes, ban-avoidance
- `references/response-shapes.md` — detailed JSON schema for post + comment + more-stub
- `references/keyword-strategies.md` — dimension-based keyword lists for buyer-language extraction

## Self-Annealing

Per Marketing CLAUDE.md:
- Log corrections to `corrections.md`
- If Reddit changes its JSON shape or rate limits, update `scripts/reddit.py scrape` + log the version bump in `docs/changelog.md`

## Known Limitations (v2.0.0)

- **Anonymous only (Tier 0)** — no OAuth. Private subs, quarantined subs, and NSFW opt-in content may return empty / truncated.
- **Tier 1 deferred (PRAW read with client_id+secret)** — higher rate limits (100 QPM), access to some otherwise-rate-limited endpoints, user-targeted OAuth. Add when we hit the 60 req/min ceiling regularly.
- **Tier 2 deferred (write ops: post/reply)** — requires username+password on top of Tier 1, plus HITL gate per CLAUDE.md "Publishing to live platforms". Not enabled.
- **No streaming** — entire JSON is buffered in memory. Fine for 99% of SG threads; mega-threads (100k+ comments) would need a streaming parser.
- **No de-duplication across runs** — re-scraping the same post overwrites the prior output. Keep dated subfolders (e.g. `raw/260417/`) if you need time-series comparison.
- **No sentiment/emotion tagging** — scraper is extraction only. Synthesis (tagging, quote ranking, verbatim-quote-bank assembly) happens downstream in buyer-language-researcher or source-of-truth Phase 3.

<!-- skill-graph:start -->

## Related
<!-- auto-generated by scripts/link-skills.py — do not edit by hand -->

- [[scrapecreators]] (skill, 0.26)

<!-- skill-graph:end -->
