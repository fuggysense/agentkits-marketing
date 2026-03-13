# Voice Profiles (V.O.I.C.E. System)

Voice profiles are **shared across all projects**. Your voice doesn't change — your business context does.

## V.O.I.C.E. Framework

Each person gets a folder with 5 files + 1 optional deep profile:

| File | Letter | Purpose |
|------|--------|---------|
| `brand-voice.md` | **V** — Voice | Tone, vocabulary, sentence structure, writing samples |
| `about-me.md` | **O** — Orientation | Role, audience, priorities, best work as proof |
| `working-style.md` | **I** — Instructions | Collaboration rules, output defaults, quality bar |
| `compound-ideas.md` | **C** — Core Ideas | Beliefs, recurring arguments, what you push back on |
| `voice-examples.md` | **E** — Examples | Real writing samples across formats (most important file) |
| `deep-profile.md` | Bonus | 96-question deep voice questionnaire (filled incrementally) |

## How It Works

```
voice/
├── README.md
├── VOICE_TEMPLATE.md       # Master questionnaire template
├── jerel/                  # Jerel's voice (shared across all projects)
│   ├── brand-voice.md      # V
│   ├── about-me.md         # O
│   ├── working-style.md    # I
│   ├── compound-ideas.md   # C
│   ├── voice-examples.md   # E
│   └── deep-profile.md     # Bonus deep questionnaire
```

## Adding a New Person

1. `mkdir voice/<name>`
2. Copy the 5 V.O.I.C.E. files from an existing profile
3. Fill them in — start with `voice-examples.md` (most impactful)
4. Optionally copy `VOICE_TEMPLATE.md` as `deep-profile.md` for the full 96 questions
