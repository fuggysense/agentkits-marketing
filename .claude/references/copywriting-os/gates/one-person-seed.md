# One-Person Seed — Pre-Write Gate

**Source:** Gary Halbert — the One-Person Rule. Named as the "single most underused LLM prompting technique" by Mark Masters (cai #44).

**Core principle:** Write to ONE real human — name, job, situation — not a persona or segment. The copy ends up sounding like real communication because it was aimed at a real target.

**The enforcement trick:** force the writer to DECLARE at the end of its output who it imagined. Without the declaration, the model nods at the instruction and writes to the audience anyway. With the declaration, vague "who I imagined" = vague copy, caught before ship.

## Gate position

After coat-of-arms is loaded. Inject into the final writer prompt.

## Prompt fragment (inject verbatim)

Add this to every copy-generation system instruction:

```
Before you write, do this: think of a specific person this copy is being written to. Use the coat of arms in your context — your imagined person must match it. Give them:

- A real first name (not "Sarah" used as a generic stock name)
- A specific job/role (not "marketing director" but "Head of Growth at a 40-person Series A SaaS reporting to a founder who doesn't understand what she does")
- A one-sentence description of the moment they're in when they read this — time of day, location, what they're doing or feeling, what app or tab they're on

Then write as if you were sending this copy directly to THAT person. Do not write for the audience. Write for that one person.

At the end of your response, include this block VERBATIM (do not skip it — your output will be rejected if you do):

IMAGINED READER
Name: <first name>
Job / role: <specific, with company-stage or situation, not generic title>
Moment they read this: <1 sentence, named moment>
Coat-of-arms specifics I used: <list 3-5 concrete specifics from the coat-of-arms doc that shaped this copy>

This block is how the operator checks your work. Without it, your copy is generic.
```

## Why the declaration matters

Without the forced declaration:
- Model produces copy. Operator can't tell if it was aimed at anyone in particular. Output feels "professional but generic."

With the declaration:
- Generic declaration ("Sarah, marketing manager, busy") → generic copy → caught, re-write
- Specific declaration ("Priya, Head of Growth at 40-person Series A SaaS, 7:45pm Tuesday with dinner in microwave, second tab is a McKinsey report her founder just Slacked her, feeling like she has 20 minutes to figure out if she knows what she's doing") → specific copy → ship

## What the post-write reviewer does

The `reviewers/one-person-enforcement.md` sub-agent verifies the declaration is specific (not generic). See that file for the verification logic and scoring.

## Pair with

This gate ONLY seeds the instruction. Verification is the reviewer's job. Both must fire.
