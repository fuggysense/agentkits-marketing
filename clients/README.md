# Client Management

## Onboarding a New Client

1. Copy the template: `cp -r clients/_template clients/<client-name>`
2. Fill in `icp.md` — Ideal Customer Profile
3. Fill in `offer.md` — Core offer and value proposition
4. Fill in `brand-voice.md` — Voice and tone guidelines
5. Fill in `channels.json` — Active channels and platforms
6. Add feedback files to `feedback/` as campaigns run

## File Structure

```
clients/<client-name>/
├── icp.md              # Ideal Customer Profile
├── offer.md            # Offer definition and value prop
├── brand-voice.md      # Voice and tone guidelines
├── channels.json       # Active channels and platforms
└── feedback/           # Campaign feedback and learnings
```

## Using Client Context

When working on a client campaign, load their folder first:
- Read `icp.md` to understand the audience
- Read `offer.md` to understand what we're selling
- Read `brand-voice.md` to match their voice
- Check `channels.json` for platform constraints
