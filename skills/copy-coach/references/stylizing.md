# Stylizing — line-level discipline

Load this reference when invoked for stylizing help, single-line critique, or any *"make it read clean"* request.

The Big Idea is what you say. Stylizing is how every sentence carries it. Even a perfect Big Idea dies line by line if the cadence is wrong.

## PART 6 — Every sentence is a hand on a rope

**The only question that matters on every line: does this sentence make the reader want the next sentence?**

If yes, keep it. If no, kill it or rewrite it. There is no in-between. A sentence is either a tug on the reader's hand, or it's slack rope.

The most common slack-rope failure: the writer has told the reader the same thing three times, and the fourth time has nothing left to want. Slack rope is usually a structure problem, not a style problem.

When you stylize, scan for slack rope first. Mark it. Then fix it.

## PART 7 — Flow not chop

Fragments as stylistic drumbeat — *"It's brutal. Painful. Exhausting."* — feel punchy in isolation but read as posturing across a page. They become a tell. The reader stops registering individual sentences and starts registering "this is the part where they're doing the punchy thing."

One sentence, flowing, lands harder when surrounded by other flowing sentences. Use the fragment when it earns its place — a single mic-drop, not a beat pattern.

## PART 8 — Person before pitch

The standard direct-response opener — *"It's 11pm. The Excel sheet is open again."* — is the line every page about indecisive couples opens with. No debt in it.

A better opener is a character. A scene. No *"you"* yet. Three paragraphs in, *then* pull the camera back: *"You know this scene because you live it."*

**Caveat — only real people belong in real positions on a real page.** If the user has given you a named client from a transcript or a verified quote, use them. If not, the cleanest alternative is an aggregated agency-voice observation that doesn't name anyone: *"By the time most couples reach us, they've been doing this every Sunday for months."* Fabricated characters in real positions erode trust faster than no character at all.

## PART 9 — Read every sentence aloud as the actual named speaker

For every sentence, ask: would the actual person — the founder, the consultant, the named agent whose name is on this page — say these words to a real client across their desk?

If they wouldn't, the words don't belong on the page. This catches the MBA register, the consultant jargon, the abstract nouns:

- *"derived live"* → *"worked out with you, in the room"*
- *"convergence"* → *"agreement"* or *"one answer"*
- *"map out your exact financial situation"* → *"look at your numbers together"*
- *"structured questions"* → *"simple questions"*

## PART 10 — Register must match the audience's cultural context

Wrong register at any point sends a *"this is foreign to me"* signal that costs trust. Imported US tropes that misfire in non-US markets:

- **Anti-government framing** — works in the US, kills in Singapore / Switzerland / Nordics / much of East Asia
- **Name-dropping foreign elite institutions** (Harvard, Stanford) as authority — use the most local trust signal available, not the most prestigious global one
- **Loud seller-side scarcity** (*"Stock running low,"* *"price may double"*) — reads as scammy in low-hype markets. Personal-future framing (*"six months from now, one of two things will be true"*) does the same work without the smell.
- **ALL-CAPS** — reads as shouting or scam-WhatsApp in many cultures. Bold sparingly, or trust the sentence.
- **American folksy openers** (*"See, ..."*, *"Here's why..."*) — register mismatch outside the US. *"So,"* or nothing.

Calibrate to the user's stated audience. Singaporean Malay couples in their 30s = short, direct, conversational English with local cultural texture (in-laws, MOP, PropertyGuru, HFE) and zero imported US tropes.

## PART 11 — Specificity discipline

World-specific specifics build credibility (*"District 10,"* *"HFE,"* *"$847 a month"*). Reader-life specifics put words in the reader's mouth (*"You hate your Excel sheet,"* *"Your mother-in-law judges you"*) and trigger immediate rejection the moment they don't match.

Use world-specific specifics liberally. Use reader-life specifics only with a release valve (*"By the time most couples reach us, the Sunday-night Excel session has become its own ritual — for some it's relief, for others it's the trigger for another argument"*).

## PART 12 — Metaphor where heavy lifting needs it

Look for places where prose is doing explanatory lifting. If you can replace three sentences of explanation with one metaphor that lands, do it.

- *"A Goldilocks economy — not too hot, not too cold."*
- *"Small leaks sink great ships."*
- *"The sale before the sale is a monkey's fist."*

**Caveat:** strained metaphors are worse than no metaphor. If you have to explain the comparison, it doesn't work. Same test as the Big Idea — instant comprehension or cut it.

## PART 13 — Sensory word-pictures create desire

Abstract benefits (*"dramatically increase your revenue"*) conjure nothing. Concrete sensory language creates a picture, and the picture creates the desire.

Halbert didn't say *"financial freedom."* He said *"waking up on a Tuesday morning with nowhere you have to be, walking to a café, ordering whatever you want without checking the price."*

**The benefit must be experienced in the reader's imagination, not merely understood by their intellect.**

## PART 14 — The kill list

**Canonical kill list is `.claude/references/copywriting-os/reviewers/forbidden-content-audit.md`** (loaded by the `/copy` pipeline) plus `unslop` (empirical per-domain detector) and `copy-editing` Sweep 8. When stylizing interactively, load that file via `ctx_search` rather than duplicating the table here.

Coach additions to flag in-context (don't wait for the audit):

- MBA / consultant abstract nouns (*convergence, alignment, optimisation, leverage, synergy, ecosystem, bandwidth*) → concrete verb-and-object (*"one answer," "the parts agree," "work better"*)
- Capitalised performative phrases (*DERIVED LIVE*, *the REAL BOTTLENECK*) → drop the capitals; let the sentence carry the weight
- Generic self-positioning (*consultative not sales-driven, we listen first*) → show with specific action; every consultant on Earth says this
- Anti-platitudes used as positioning (*we don't scale on volume, we don't tell you what you want to hear*) → the fact alone, plainly stated
- Folksy American openers (*"See, ..."* *"Here's why..."*) outside US markets → *"So,"* or nothing
- Trailing ellipses (*"Take a look..."*) → full stop and a paragraph break
- AI-triplets (*"clear, concise, and compelling"*) → pick the strongest; cut the others
- Premature payoff snatched back (*"imagine the relief of..."* mid-letter, before earning it) → hold the payoff until near the close
- Stacked chorus inside one section → spread across the page
- Abstract benefit where a sensory picture would do more work → concrete sensory picture
- Words put in reader's mouth (*"You hate your job"*) → describe a pattern; use release valves

## How to deliver a stylizing pass

1. **Read the prose top to bottom as the target buyer would.** Switch into reader-hat before line-editing.
2. **Run every line through the cadence and voice checks** — tug, flow not chop, person before pitch, read aloud as named speaker, register match, specificity discipline, metaphor where heavy lifting needs it, sensory picture where abstract benefit sits, kill list.
3. **Run the cold-reader pass** (load `references/cold-reader-pass.md`).
4. **Propose specific rewrites with the principle behind each change.** Quote the original line, show the rewrite, name the principle (*"flow not chop," "kill list: convergence," "fabricated reader-life specific," "metaphor opportunity"*).
5. **Cold-reader pass on your rewrite** before delivering it.

## Single-line critique (headline, opening, P.S., button copy)

1. Run the line against tug + cadence + voice + register + kill-list.
2. If it fails any check, name which.
3. Propose 3–5 alternates. Each named with what it fixes.
4. Recommend the strongest. Explain why.

## PART 17 — Slippery slide flow tools

Sugarman's "slippery slide": every line's only job is to get the reader to read the next one. These are the cadence devices that keep them sliding.

- **Bucket brigades** — short connector phrases between paragraphs (*"Here's the thing:" / "Truth is:" / "Now—"*). They reset attention without restarting the argument.
- **Seeds of curiosity** — end paragraphs with *"But there's more"* / *"Here's why that matters"*. Max 3-4 per page; they lose force when stacked.
- **Stutter** — repeat a word from the last sentence in the first sentence of the next paragraph. Invisible glue.
- **Vary length** — short. Then medium that breathes. Then short again. A page of same-length paragraphs reads as a wall.
- **Rule of one** — one point per paragraph. Two points = neither lands.

Stylize for the slide, not for the sentence-as-trophy. A line that's beautiful in isolation but doesn't pull into the next one is slack rope (see PART 6).

## PART 18 — The So-What chain

The diagnostic tool that turns features into consequences. For every feature, ask *"so what?"* until you hit emotional or financial. Go 3 levels deep.

- *"Saves 4 hours"* → *"close your laptop at 5pm instead of 9pm"* → *"have dinner with your kids while it's still warm"*
- *"Automates outreach"* → *"wake up to replies instead of a blank inbox"* → *"stop dreading Monday morning"*

If a benefit on the page stops at *"saves time"* or *"increases efficiency,"* the chain isn't done. Two more *"so what?"*s and you'll hit the line that actually moves the reader.

## PART 19 — Pain quantification

Vague problems feel overwhelming. Quantified problems feel solvable. Vague pain doesn't sell — it just depresses.

Two techniques, used singly or together:

- **Do the math.** *"22+ hours of setup"* gives the reader a number they can weigh against your price. *"A lot of time"* gives them nothing to weigh.
- **Paint the scenario.** Superhuman's *"you and your team both reply to the urgent email"* puts the pain in motion. Concrete, sensory, specific to the reader's day.

When a paragraph describes pain, check: is there a number, a scene, or both? If neither, the pain isn't selling — it's just sitting there.

## PART 20 — Internet-native voice markers

The internet-native voice (Marc Lou, Codie Sanchez, Justin Welsh) trades polish for credibility. Readers smell the curated MBA register and trust the rough-but-honest more.

- **Revenue transparency** — *"$45K/month"*, not *"significant revenue"*
- **Honest limitations** — *"3D generation isn't great yet"*, not *"continuously improving across modalities"*
- **Strategic emoji** — sparingly, where a human would use one, not as decoration
- **In-group language** — your audience's words, not the category's marketing words
- **Specific over rounded** — *"$47,329"* not *"lots"*; *"3 weeks and 4 days"* not *"a few weeks"*

When stylizing for a founder voice or a creator brand, audit for these markers. If everything reads round and polished and limitation-free, you've drifted into the corporate register and the trust signal is gone.
