# Projects & Clients

This folder holds per-project business context. Each project gets its own subfolder with ICP, offer, channels, and optional tone tweaks.

**Voice profiles live in `voice/` — they are shared across all projects.**
A project's `brand-voice.md` only contains project-specific tone tweaks (e.g., "more technical for this audience"), NOT your full voice. Your full voice always loads from `voice/<person>/`.

## Structure

```
clients/
├── _template/              # Copy this to start a new project
├── my-saas-product/        # Example project
│   ├── icp.md              # Ideal Customer Profile
│   ├── offer.md            # What we're selling + value prop
│   ├── brand-voice.md      # Project-specific tone tweaks ONLY
│   ├── channels.json       # Active platforms and channels
│   └── feedback/           # Campaign feedback and learnings
├── my-newsletter/          # Another project
│   ├── ...
```

## Setting Up a New Project

1. Copy the template: `cp -r clients/_template clients/<project-name>`
2. Fill in `icp.md` — Who is the customer?
3. Fill in `offer.md` — What are we selling?
4. Fill in `brand-voice.md` — Any tone tweaks for this project (or leave empty if your default voice works)
5. Fill in `channels.json` — Where do we publish?
6. Start running commands — the context gate will auto-load this project

## Campaign Folders

Each project can have multiple campaigns tracked in `campaigns/`:

```
clients/<project>/campaigns/
├── launch-q2/
│   ├── state.yaml       # Progress tracker ("save file")
│   ├── assets/           # Generated content, images, copy
│   └── metrics/          # Weekly metric snapshots
└── seo-content/
    ├── state.yaml
    └── assets/
```

Create campaigns with `/campaign:new`. State persists across sessions — pick up where you left off with `/campaign:status` or `/campaign:next`.

## How Context Loading Works

When a session starts and you run a skill/agent:
1. Claude asks: "Who is this session for?"
2. You pick a project from this folder
3. Claude loads: `voice/<person>/` (V.O.I.C.E. files) + `clients/<project>/` (business context)
4. All outputs for that session use both layers
