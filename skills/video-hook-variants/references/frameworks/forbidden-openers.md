# Forbidden Openers

These openers fail the Four Horsemen on contact. If any draft starts with one → redraft immediately. No exceptions.

## The List

| Opener | Failure mode | Why |
|---|---|---|
| "Have you ever wondered…" | Disinterest | Generic curiosity solicitation — no contrast, no tension, no topic |
| "Welcome to [video / channel / episode N of…]" | Delay | Buries value behind a greeting. Beat 1 belongs to the hook, not the intro |
| "Hey guys" / "What's up" / "Hi I'm [name]" as the FIRST line | Delay + Irrelevance | Credentials / greeting before topic |
| "Today we're going to talk about…" | Delay | Meta-narration instead of value delivery |
| "In a [city / country / month / year], a [person]…" | Modern W Order violation | Where + When first = scroll |
| "A year-three media post-production student…" | Delay + Irrelevance | Credentials before topic (the "Tingshan intern" anti-pattern) |
| "[Topic] is super important…" | Disinterest | Telling the viewer to care instead of making them care |

## Exception (rare)

If the concept's body genuinely requires a "Welcome to episode N" framing (only for legitimately serial content), that line goes in beat 2 or beat 3. Never beat 1.

## Auto-Reject Rule

```json
"forbidden_opener_check": "no Have-you-ever-wondered / Welcome-to / Hi-I'm / Today-we're / Where-When / credentials-first openers — pass"
```

If any forbidden opener is present, the check must read:
```json
"forbidden_opener_check": "FAIL — [opener used] — redraft required"
```

Do not deliver a hook with a failed forbidden_opener_check to the orchestrator.
