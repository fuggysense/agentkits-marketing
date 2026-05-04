# Obsidian Brain Context

This repo lives inside the Obsidian vault "Jerel's Brain" at:
`/Users/jerel/Documents/Jerel's brain/jerel's brain/Marketing/`

The vault root contains personal knowledge (Life/, Business/, Voice/, Profile/).
This Marketing/ subfolder contains the full agent kit.

## When loading context

- **Voice files:** `../../Voice/` (vault root) or `voice/jerel/` (symlink in Marketing/)
- **Personal profile:** `../../Personal and professional profile/`
- **Skill graph:** Follow `[[wiki-links]]` in SKILL.md files OR `.claude/skill-graph.json` for inferred edges
- **Master map:** `../../index.md`
- **Consolidated learnings:** `learnings/` (10 domain files: campaign, content, copywriting, cro, email, paid-media, sales, seo, social, video)

## Two-layer context model

- **Voice = the person** (how Jerel writes) — stays the same across projects → `voice/jerel/`
- **Project = the business** (who we serve, what we sell) — changes per client → `clients/<slug>/`

V.O.I.C.E. files in `voice/jerel/`:
- `brand-voice.md` (V) — voice
- `about-me.md` (O) — operator background
- `working-style.md` (I) — interaction patterns
- `compound-ideas.md` (C) — accumulated thinking
- `voice-examples.md` (E) — sample copy in voice
