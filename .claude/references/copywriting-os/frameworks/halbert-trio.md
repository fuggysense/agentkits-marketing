---
name: Halbert Trio — A-Pile, Coat of Arms, One-Person Rule
source: cai #44, raw-newsletters/halbert-ai-copywriting-one-person.md
loaded_by: gates/coat-of-arms-generator.md, gates/one-person-seed.md, reviewers/one-person-enforcement.md
purpose: Three Halbert disciplines — A-pile sort test, audience coat of arms, one-person rule — applied as the canonical fix for generic LLM copy.
---

# Halbert Trio — A-Pile, Coat of Arms, One-Person Rule

## The principle

Gary Halbert's three most-quoted ideas — the A-pile/B-pile test, the coat of arms research method, and the one-person rule — are the exact fix for what's wrong with most LLM-generated copy. They run as a system, in order: coat of arms first (everything else depends on it), one-person rule second (narrows the coat of arms to a target), A-pile test last (applies to the surface layer the reader sees first).

Halbert's most-repeated piece of advice: **"Write to one person."** Not a persona. One actual human being with a name, a job, a situation.

## Why it matters for AI copy

Each of the three ideas solves a specific AI failure mode:

- **A-pile test** fixes B-pile defaults — Claude's training data is stuffed with marketing-shaped subject lines ("Transform Your Workflow Today," "5 Ways to Boost Productivity"), so the default output reads like a marketing department wrote it. The test forces output into a different shape.
- **Coat of arms** fixes generic output — most LLM copy is missing audience understanding not because the writer doesn't know their audience, but because the audience understanding never makes it into the prompt.
- **One-person rule** fixes the "writing for a category" problem — without it, Claude writes to "the audience" and produces audience-shaped copy.

The three only work if the human does the research. The LLM is a writing speed multiplier, not a research shortcut.

## How to apply (writer's checklist)

### Sub-checklist 1 — Coat of Arms (do once per audience, save it)

Build a working document of audience specifics. Templated fields:

- **Who they are (specific, not demographic).** Not "B2B marketing directors age 35–50." Instead: "Marketing directors at B2B SaaS companies between Series A and Series C, typically the second or third marketing hire, reporting to a founder who doesn't quite understand what they do."
- **What they read when nobody's watching.** Newsletters they actually open. Podcasts they listen to in the car. Twitter accounts they check before sleep.
- **What they say they want.** Formal-interview version.
- **What they actually want.** Underneath version. What would actually make them feel successful.
- **What they're afraid of.** Specific fear, not generic "failure." E.g. "Getting fired because the CEO wants to see a growth number they can't produce."
- **What they've already tried.** Products, approaches, consultants. Tells the LLM what the reader has already seen.
- **The lie they tell themselves.** The thing they know isn't quite true but keep repeating to get through the quarter.
- **A specific Tuesday in their life.** Three sentences describing an ordinary, non-dramatic moment. Not the crisis. The background hum of their actual day.

The "specific Tuesday" field is the one that makes the biggest difference. Everything else can come out abstract. Tuesday forces the reader into a real moment.

### Sub-checklist 2 — One-Person Rule (apply per writing prompt)

- Pick a real person (or specific composite) who fits the audience.
- Give them a name, a job, and a one-sentence description of the moment they're in when they read this.
- Write as if sending the piece directly to that person. Not for the audience. For that person.
- At the end of the response, surface who you imagined — name, job, moment.
- If the imagined person comes back generic ("Sarah, marketing manager, busy"), force a rewrite: "Make the person more specific. Give me a version with a real situation in a real moment."

### Sub-checklist 3 — A-Pile Test (apply to anything the reader sees first)

For every subject line, headline, ad hook, or first-screen element, ask: would this look like something from a person who knows the reader, or something from a marketing department?

Hard rules to bolt onto the prompt:

- No numbered lists in the subject ("5 ways to…")
- No imperative-mood action verbs to open ("Transform…", "Discover…", "Unlock…")
- No colons separating a setup from a promise
- No marketing-only words ("ultimate," "essential," "proven")
- Prefer lowercase where it would feel natural in a personal email
- Vary length — some very short, some longer and specific

## How to audit (reviewer's checklist)

Pass/fail tests for the three layers:

1. **Coat of arms specifics check.** Does the draft reference at least 2–3 concrete fields from the coat of arms (specific Tuesday, what they've already tried, the lie they tell themselves)? If the copy could be sent to any audience in the same category, fail.
2. **One-person trace.** Did the writer name the imagined person at the end? Is the moment specific (with a 7:45pm Tuesday level of detail) or generic ("busy professional")? Generic imagined person = generic copy. Fail.
3. **A-pile sort.** Take the subject line / headline. Strip context. Would a human looking at it for a quarter-second sort it into A-pile (looks personal, sounds like one human writing to another) or B-pile (looks like marketing)? If B-pile, fail.
4. **Voice constraint check.** Did the prompt include a "do not sand the edges off" instruction? Halbert's voice was sharp, slightly profane, certain. Claude's default is smooth and inoffensive. Fail any draft that reads like default Claude voice.

## Examples from the newsletter

**B-pile vs A-pile subject lines.** B-pile examples Halbert would have hated: "Transform Your Workflow Today," "5 Ways to Boost Productivity," "The Ultimate Guide to X." Each starts with an imperative or a number, signals marketing department, gets archived in the end-of-day batch.

**Generic vs specific imagined person.**
- Generic (fail): "Sarah, marketing manager, busy."
- Specific (pass): "Priya, Head of Growth at a 40-person Series A SaaS, reading this at 7:45pm on a Tuesday with her dinner cooling on the counter because she's trying to finalize next quarter's plan before her 1-on-1 tomorrow."

**Demographic vs coat-of-arms audience description.**
- Demographic (fail): "B2B marketing directors age 35–50."
- Coat of arms (pass): "Marketing directors at B2B SaaS companies between Series A and Series C, typically the second or third marketing hire, reporting to a founder who doesn't quite understand what they do."

## Anti-patterns

- **LLM-generated coat of arms.** If you ask Claude to generate the coat of arms from a product description, you get back the same vague portrait Claude was going to write copy for anyway. The coat of arms must contain specifics the LLM doesn't have access to from training data — customer interviews, support tickets, review mining, sales calls.
- **Persona instead of person.** A "persona" is a category in disguise. The one-person rule fails the moment the imagined target is a composite type rather than a single human in a real moment.
- **Skipping step 5 (the trace).** Without "tell me who you imagined" at the end, Claude nods at the one-person instruction and writes to the audience anyway. The trace is the enforcement mechanism.
- **Speed without research.** A workflow that lets the writer skip the research and prompt their way to output is exactly what Halbert spent his career arguing against. Fast garbage is still garbage.
- **Default Claude voice.** Smooth, careful, inoffensive. Halbert would have added a voice constraint to every prompt.

## Exact prompts / templates

### A-pile subject-line prompt (verbatim)

```
I'm writing an email to [specific reader — be granular, one person]. The
purpose is [one sentence on what the email needs to do].

Generate 15 subject lines. Every one of them has to pass the A-pile test:

Would this subject line look like something from a person who knows the
reader, or like something from a marketing department?

Rules:
- No numbered lists in the subject ("5 ways to...")
- No titles that start with action verbs in imperative mood
  ("Transform...", "Discover...", "Unlock...")
- No colons separating a setup from a promise
- No words that only appear in marketing copy ("ultimate," "essential,"
  "proven")
- Prefer lowercase where it would feel natural in a personal email
- Length should vary. Some very short. Some longer and more specific.

For each subject line, tell me in one phrase why it passes the test. If you
generate something that sounds like marketing copy, throw it out and try
again.
```

### Coat of Arms template (verbatim)

```
AUDIENCE COAT OF ARMS: [Name of audience]

Who they are (specific, not demographic): [...]
What they read when nobody's watching: [...]
What they say they want: [...]
What they actually want: [...]
What they're afraid of: [...]
What they've already tried: [...]
The lie they tell themselves: [...]
A specific Tuesday in their life: [Three sentences describing an ordinary,
  non-dramatic moment.]
```

### One-Person Rule add-on (verbatim)

```
Before you write, do this: think of a specific person this copy is being
written to. Give them a name, a job, and a one-sentence description of the
moment they're in when they read this. Then write as if you were sending
this directly to that person.

Do not write for the audience. Write for that one person.

At the end of your response, tell me who you imagined. Name, job, moment.
```

### Project-level system prompt (verbatim)

```
You are writing copy for [audience name]. The coat of arms for this
audience is in your knowledge base. Read it before responding to any
writing request.

Standard operating procedure for any writing request:
1. Reference the coat of arms specifics before generating any copy.
2. Name the specific person you're writing to (one real moment, not a
   demographic).
3. Produce the copy aimed at that one person.
4. If the output is a subject line, headline, or anything the reader sees
   first, apply the A-pile test: does this look like it came from a person
   or a marketing department?
5. At the end of each response, briefly state which coat of arms specifics
   you used and who you imagined writing to.

Do not skip step 5. It's how the user checks your work.
```
