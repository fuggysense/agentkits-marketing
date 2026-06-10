# Cold-reader pass — fresh eyes, default to delete

Load this reference when the user invokes *"final pass," "fresh eyes," "kill the babies,"* or any equivalent — and also before any final delivery you make on your own.

## PART 15 — The cold-reader pass

After stylizing — and before any final delivery — run this pass. Not as a polish step. As a structural re-read by someone who isn't invested.

**Why this matters.** You read your own writing inside the writer's frame. The reader doesn't have that frame. Everything slightly off — a number that doesn't match their reality, a place name that's not theirs, a word slightly heavier than the rest — registers as friction.

The cold-reader pass is the discipline of forcibly switching frame. The LLM default — to anchor on the previous turn — must be deliberately broken.

### What the pass flags

- Orphan references (a callback to a section that got cut three passes ago)
- Stacked chorus inside a single section
- Fabricated specifics (a number, place, or name that wasn't in the source material)
- Contradictions (the loop section says X, the proof section assumes not-X)
- Fragments-as-drumbeat where flow was needed
- Words too heavy for the audience's register
- Sentences the named speaker wouldn't actually say
- Abstract benefits where a sensory picture should be
- Words put in the reader's mouth without a release valve
- A section that doesn't earn its place — cut the whole section, don't polish it

### When the pass fires (mandatory, not optional)

- **Before every draft delivery** — never deliver without running this
- **After every structural change** — changes orphan references
- **When the user invokes "final pass" / "fresh eyes" / "kill the babies"** — use the verbatim prompt below
- **As the final pre-render gate** — page isn't ready until this passes clean

### Default to delete

If a flag fires, the question isn't *"how do I polish this?"* The question is *"does this earn its place at all?"* If no — cut it. Polish is the second move, not the first.

### Sub-agent dispatch for long copy (>800 words)

The whole point of cold-reader is breaking previous-turn anchoring. Running it in the same context defeats the discipline. For pages over ~800 words, dispatch the pass as a **fresh sub-agent** via the `Agent` tool:

- Hand the agent the artifact file path (never paste contents — pasting loads your anchoring into the sub-agent)
- Hand the agent the PART 16 verbatim prompt below
- Ask for a structured cuts list back: `{cuts: [{location, current_text, principle, recommendation}]}`
- Apply the cuts in the main thread

Short critiques (single line, single section) can stay inline.

## PART 16 — The fresh-eyes prompt (load verbatim)

When the user asks for a final pass, fresh eyes, *"kill our babies,"* or any equivalent — and ALSO before any final delivery you make on your own — load this prompt verbatim into your operating mind. Don't paraphrase, don't soften.

> **Final pass. Fresh eyes.**
>
> Now, let's start killing our babies. Forget "best practices." Look at the page itself — it should be a self-contained experience.
>
> Firstly, reflect:
>
> **1. Is it a complete sales argument?** Someone reading from top to bottom will understand it fully? Are there elements that don't belong there, that might throw them off?
>
> **2. How simple is the language?** Most of these readers are [native English speakers / non-native ESL / industry insiders] who use [third-grade language / professional register / technical vocabulary] familiar to [Singaporeans / Australians / US east-coast]. We need structural simplification, then language simplification.
>
> **3. Does every sentence still want the next?** Tug on rope, or slack? Where the tug breaks, the page breaks.
>
> **4. Does every section still earn its place?** Or did an earlier pass leave a section orphaned, ground covered, advancing nothing?
>
> **5. Are the chorus restates spread, not stacked?** Big Idea once per costume across 5–7 sections. Two restates inside one section = one too many.
>
> **6. Does every chorus restate carry proof?** Hype gets cut.
>
> **7. Has the cold-reader test been run on every sentence?** Read in reader-frame. Anything that registers as friction — flag it. Default to delete.
>
> Now — what comes out of the page? List the cuts.

## Output

Return a structured cuts list:

```
Cut #1 — [location] — "<original text>"
  Principle: [tug / flow not chop / kill list X / orphan / stacked chorus / abstract benefit / words in mouth / section doesn't earn / fabricated specific]
  Recommendation: [delete | rewrite as: "..." | merge into section X]
```

If the pass surfaces nothing to cut or change — you didn't actually run it. Go back. Re-load the prompt. The pass that finds nothing to cut is the pass that wasn't run.
