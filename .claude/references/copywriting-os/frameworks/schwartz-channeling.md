---
name: Schwartz Channeling — Channel Existing Desire, Don't Create It
source: cai #41, raw-newsletters/schwartz-copy-cant-create-desire.md
loaded_by: frameworks/schwartz-channeling.md (referenced by reviewers/teardown-reviewer.md and frameworks/failure-mode-library.md via the channel-vs-create test)
purpose: Eugene Schwartz's diagnostic — copy can't create desire, only channel desire that already exists — turned into a binary pass/fail prompt-time check and a research-first workflow.
---

# Schwartz Channeling — Channel Existing Desire, Don't Create It

## The principle

Eugene Schwartz, *Breakthrough Advertising* (1966):

> "Copy cannot create desire for a product. It can only take the hopes, dreams, fears, and desires that already exist in the hearts of millions of people, and focus those already-existing desires onto a particular product."

People act on desires they already have. Copy can make those desires more vivid, more urgent, more focused on a specific solution. Copy cannot install new ones with a paragraph.

Schwartz quoted at conferences gets treated as philosophy. Treat it as a diagnostic: a binary pass/fail check on every opening section.

## Why it matters for AI copy

Peggy Burnett's audit (cai #41): 34 AI-generated pieces of copy across landing pages, email sequences, and Facebook ad sets — produced by experienced copywriters, not beginners. Scored on a single binary: does the opening section channel an existing desire, or does it attempt to create one?

Split: **23 to 11.** Twenty-three pieces opened by trying to make the reader want something. Eleven opened by naming a want the reader already had. The eleven that channeled had time-on-page roughly 40% higher across landing pages with analytics access (small sample, time-on-page is a proxy, but the direction was consistent).

Why AI defaults to creating desire: when the prompt describes a product and asks AI to sell it, the output centres the product. AI writes toward whatever object you give it. Most prompts are written from the seller's perspective because the person writing the prompt is the seller. So the prompt is about the product. So the copy is about the product. The reader's existing desires never enter the equation.

**Schwartz restated as a prompting problem:** if you don't put the existing desire into the prompt, the AI has no choice but to manufacture one.

## How to apply (writer's checklist)

### The channel-vs-create diagnostic

Before any prompt, answer one question:

> What does this person already want that they'd want whether or not your product existed?

A freelance copywriter wants to take on more clients without working until midnight. That desire exists with or without an AI writing tool. A marketing director wants their team to produce campaign assets faster. That desire exists with or without a project management platform.

If you can't articulate the pre-existing desire, you don't know your audience well enough yet. That's not a prompting problem — it's a research problem. Get customer interviews, read support tickets, scan competitor reviews. The prompt waits.

### Three-step framework (verbatim, from the newsletter)

**Step 1: Identify the existing desire.** Stated in plain language. Must be the desire that exists with or without your product.

**Step 2: Find the language.** The desire stated in the reader's words, not the marketing team's. "Optimise operational efficiency" is the brief. "Stop spending every Monday pulling numbers from four different dashboards" is the buyer. One of those opens a landing page that converts.

Customer interviews are the best source. Feed them to Claude and use the buyer-language extraction prompt below.

**Step 3: Build the prompt around the desire, not the product.** The product enters as the answer, not the subject. Reader's world first, product second.

### Channel-vs-create binary test

Apply to every opening:

- Read the first two paragraphs in isolation.
- Are they describing the reader's existing world (channel) or painting a fantasy / describing the product (create)?
- If the opening uses "imagine…" three times, count the *imagines*. Three sentences in a row telling the reader what to want is desire creation by definition.
- If you can't tell whether it channels or creates, default to fail. Real channeling reads unambiguously like the reader's current inner state.

### Awareness-stage selector (5 levels)

The newsletter focuses on channel-vs-create rather than detailing all five Schwartz awareness levels. The five canonical Schwartz stages — preserved here for reference but **not detailed in this newsletter** — are: Unaware → Problem-Aware → Solution-Aware → Product-Aware → Most Aware.

The channel-vs-create check applies regardless of awareness stage: you're channeling whatever desire is already at that stage of awareness, not creating new desire higher up the ladder.

## How to audit (reviewer's checklist)

Pass/fail tests:

1. **Opening binary.** Read the first two paragraphs. Channel or create? No gray area. If the first two paragraphs describe the reader's world, channel. If the first two paragraphs describe the product or paint a fantasy, create. Create = fail.
2. **Imagine count.** Count occurrences of "imagine" in the opening. More than one consecutive *imagine* sentence = creating desire = fail.
3. **Pre-existing desire articulation.** Can the writer state in one sentence what the reader would want with or without the product? If no, the piece was written without research. Fail.
4. **Reader-language fidelity.** Is the desire stated in the reader's words or the marketing team's? Marketing-team phrasing fails.
5. **Default-opening filter.** Does the piece open with the product name, a statistic, or a rhetorical question? Each is a default AI opening that signals creating-desire. Fail.

## Examples from the newsletter

**Prompt A (product-centred — fails):**

```
Write a landing page for [product]. Target audience: [audience].
Key benefits: [benefits]. Tone: conversational, professional.
```

Output: opens with the product's value proposition every time. The kind of first draft you rewrite entirely.

**Prompt B (desire-centred — passes, 6 for 6 in testing):**

```
The reader is a [audience] who is currently dealing with [specific
frustration from research]. They've tried [what they've already
attempted]. What they want is [existing desire in their own language].

Write a landing page that starts inside that desire. Show the reader you
understand what they're already feeling before you introduce [product]
as the way to get there.
```

**Creating desire — what it sounds like in AI output:**

> "Imagine producing twice the copy in half the time. Imagine never staring at a blank page again. Imagine scaling your freelance business without working longer hours."

Three "imagines" in a row telling the reader what to want. The copywriting equivalent of a doctor diagnosing you before asking where it hurts.

**Channeling existing desire — what the reader actually has:**

> They want to stop losing entire mornings to first drafts that should take an hour. They want to stop rewriting the same benefit statement four times because it's not landing. They want the Thursday afternoon panic when two deadlines overlap to stop happening.

Those desires exist right now. They don't need to be installed.

**Marketer language vs buyer language:**
- Marketer (fail): "Optimise operational efficiency."
- Buyer (pass): "Stop spending every Monday pulling numbers from four different dashboards."

## Anti-patterns

- **The "imagine" stack.** Multiple consecutive "imagine…" sentences in the opening. Painting a fantasy instead of naming an existing desire. Lazy prompting that produces lazy copy.
- **Product-first prompts.** Prompt structure that puts the product, target audience, and benefits up front, with the reader's situation either absent or as an afterthought. Output centres the product because the prompt did.
- **Pushing instead of pulling.** Schwartz's term. Telling the reader what to want rather than focusing what they already want.
- **Plausible psychology without source data.** AI is good at producing text that reads as psychologically plausible. That's a language pattern skill, not an empathy skill. Without real audience data, the output is well-structured guessing.
- **Speed without the desire check.** AI produces something in seconds. It sounds professional. Good structure. You ship it without catching that it started from the product instead of the reader. Schwartz's binary is the check.

## Exact prompts / templates

### Buyer-language extraction (verbatim)

```
Read these customer interviews. Pull out every statement where the
interviewee describes a frustration, a desire, or something they wish
were different about their current situation. Keep their exact phrasing.
Don't paraphrase or clean up the language.
```

### Desire-centred writing prompt (verbatim)

```
The reader is [specific person] dealing with [specific situation].
They want [existing desire in their language].

Write [format] that opens inside that desire. The first third of the
piece should be entirely about the reader's world. [Product] enters as
the solution after the reader feels understood.

Do not open with the product name, a statistic, or a rhetorical question.
Open with a specific moment the reader will recognize from their own
experience.
```

### Channel-vs-create gut check (one question to answer before any prompt)

> Am I channeling a desire that exists, or trying to create one? If you're creating, stop. Go find the real one. The prompt can wait.
