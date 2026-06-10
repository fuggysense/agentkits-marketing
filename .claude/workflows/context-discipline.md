# Context Discipline Workflow

**Purpose:** Keep sessions lean so you can work longer per client without bloat-driven compacts. Move heavy operations out of your session window into subagents and the persistent ctx index.

**Applies to:** Every client-work session.

---

## The One Rule

**Your session window is for decisions and drafts. Raw data lives outside it.**

If an operation will produce >5KB of output, it goes to:
- A subagent with `run_in_background` (for multi-step research)
- `ctx_execute` (for single commands — DB queries, URL fetches, scrapes)
- Never directly into your active session context.

---

## Session Start (client work)

Run once per client-session, before any actual task:

1. **Identify client** — confirm who this session is for
2. **Load lean core only**:
   - `clients/<slug>/context-profile.json` (structured, ~2KB)
   - `voice/<person>/brand-voice.md` (if writing copy)
   - Any corrections.md for skills you know you'll use
3. **Skip blanket reads** — do NOT pre-load icp.md, offer.md, learnings.md, buyer-profile.md
4. **Query on demand instead** — when you need ICP detail, run `ctx_search("ICP pain points fuggysmedia")` — returns the chunk, not the file
5. **If the client's docs aren't in the index yet**, offer to index them as a one-time cost (adds ~1 minute, saves 15KB per future session)

---

## Within-Session Rhythm

Structure your work in blocks, not linear task-hopping:

| Block | Pattern | Context hit |
|-------|---------|-------------|
| **Research** | Delegate to subagent (`researcher`, `deep-research`, `ad-library-scraper`) with `run_in_background`. Keep working on other things. | ~2KB summary returns |
| **Creative** | Load brand voice + reference copy verbatim. Draft inline. | 8-15KB, ephemeral |
| **Review/decide** | Pure taste calls. Minimal file loads. | Near-zero |

**Between blocks:**
- If context usage >50% → next heavy op MUST go to subagent
- If context usage >70% → distill + `/compact` before auto-fires

---

## Heavy Operation Checklist (ALWAYS subagent or ctx_execute)

- `/research:deep` runs
- `/ads:scrape-library` or `/ads:scrape-advertiser`
- `ad-library-scraper` invocations
- `psql`/`sqlite3` queries against swipe-ads, analytics, or any DB (except with LIMIT ≤10 or `| head`)
- `curl`/`wget` to any URL (landing pages, API responses, HTML fetches)
- `yt-dlp` / video transcriptions
- `firecrawl` / `scrapecreators` calls
- `notebooklm ask` responses
- Competitor page scrapes
- Wide `grep -r` across the whole repo
- Reading any file >5KB that you don't need verbatim (summaries, logs, JSON blobs)

**Exempt (use normal tools):**
- Code editing (Read → Edit needs exact content)
- Reading brand-voice/copy files when the nuance matters
- Small config files (<5KB)
- Git operations
- Short listings (`ls`, `find | head`)

The `smart-ctx-guard.sh` PreToolUse hook nudges you on the Bash side. It's a reminder, not a block — ignore it when precision work actually needs the full output.

---

## Session End (replaces ad-hoc handoffs)

Before closing:

1. **Distill decisions** — what did we conclude this session? Append 3-5 bullets to `clients/<slug>/learnings.md`
2. **Index new research** — any research output from this session gets added to the ctx index with tag `client:<slug>`:
   ```
   ctx_execute(language: "shell", code: "cat <research-output> | ctx-index --tag client:<slug>")
   ```
3. **Note open threads** — unfinished work → `clients/<slug>/open-threads.md` or the Open Threads section of CLAUDE.md
4. **Do NOT write a handoff summary into the next session's prompt** — that's what the index is for. Next session queries the index.

---

## Why This Works For You Specifically

- **Your pattern:** one client per session, bouncing between research/copy/ads/review
- **Your pain:** context fills from skill-hopping + research dumps; handoffs lose momentum
- **This fixes it by:** keeping research out of your session entirely (subagent summary only), and making past research queryable so "gone" becomes "retrievable"

**Expected payoff:**
- Sessions run 3-4x longer before compact
- Research you did weeks ago stays accessible
- Client onboarding scales past 6-10 clients without breaking

---

## Enforcement

- `smart-ctx-guard.sh` hook: nudges heavy Bash commands toward ctx_execute
- `skill-router.sh` hook: ensures skill activation (existing)
- Self-discipline: when you see the hook warning, actually route through ctx_execute — don't ignore and bash through

---

## Client folder auto-detect (cwd-based)

Before any client work, establish WHO this is for. Auto-detect first, ask second.

1. **Check cwd.** Run `pwd`. If the cwd contains a `_brand/` subfolder, that IS the client folder. Auto-load all `_brand/*.md` and announce: *"Detected client: `<folder-name>`. Loaded brand voice + offer + ICP + buyer profile."*
2. **Walk up parents.** If no `_brand/` in cwd, climb parent directories. If any ancestor sits under `Marketing/clients/<name>/`, that's the client. Load its `_brand/` files and announce the detection.
3. **Fall through to ask.** If auto-detect fails, list `Marketing/clients/` (excluding `_template/`) and ask once: *"Which client?"*

**What to load on a hit:**
- `_brand/brand-voice.md` — verbatim (for any copy work)
- `_brand/offer.md` — verbatim (sales/landing/email)
- `_brand/icp.md` — for targeting
- `_brand/buyer-profile.md` — for awareness mapping
- `context-profile.json` — fast structured context

**Mid-session client switch.** If the user says "actually let's work on <other client>," restart the gate with that name and drop the previously loaded context. Never blend two clients' voices in one piece.

**Missing brand files.** If `_brand/*.md` is empty or absent, offer to scaffold from `Marketing/clients/_template/`. Pause for the user to populate `brand-voice.md`, `offer.md`, `buyer-profile.md` before writing copy. Never invent voice.
