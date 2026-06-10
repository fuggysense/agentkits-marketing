---
name: Collier Principle — Enter the Conversation Already in Their Head
source: cai #42, raw-newsletters/most-important-prompting-principle-1937.md
loaded_by: reviewers/buyer-language-fidelity-audit.md
purpose: Robert Collier's 1937 rule — "enter the conversation already happening in the customer's mind" — turned into a two-step prompting move that anchors AI output to the reader's existing inner state instead of the product.
---

# Collier Principle — Enter the Conversation Already in Their Head

## The principle

Robert Collier sold millions of dollars worth of products through direct mail in the 1920s and 30s. The principle from *The Robert Collier Letter Book* (1937):

> "Enter the conversation already happening in the customer's mind."

Collier's argument: your prospect isn't sitting around waiting for your message. They're in the middle of something. They have worries, desires, frustrations, and half-formed thoughts that have nothing to do with you. Your copy has to meet them inside that existing conversation or it gets ignored.

A second layer that gets overlooked: he said *enter* the conversation, not *answer* it. The goal isn't to solve the reader's problem in the opening line — it's to demonstrate you understand the world they're living in.

## Why it matters for AI copy

A good copywriter absorbs Collier's principle intuitively after years of writing for real people. They're already imagining the reader's Monday morning when they sit down. AI doesn't have that Monday morning unless you put it there.

When the prompt starts with the product, AI writes from the product. When the prompt starts with the reader's situation, AI writes from there instead. AI doesn't choose one over the other — it follows whatever you anchored it to.

So with a human writer, some of the empathy work happens unconsciously. With AI, all of it has to be explicit. Every structural prompting technique — role assignment, output formatting, few-shot examples — is downstream of one question: do you know where the reader's mind already is?

If the prompt doesn't put the reader's existing inner state into the prompt, AI has no choice but to start the copy from the product.

## How to apply (writer's checklist)

### The two-step process

**Step one: map the mental conversation before writing anything.**

Use a dedicated prompt to extract internal monologue fragments — the prompt is *not* trying to sell, it's modelling a person's inner state. Without a sales objective pulling the output toward convenient pain points, the fragments come back more honest.

**Step two: pick 3–5 specific thoughts and build them into the writing prompt.**

Quote the fragments back at AI as the reader's current internal monologue. Instruct AI to start inside one of those thoughts and not mention the product until the reader feels understood.

### Buyer-language extraction rules

- Use the language the reader would use talking to a friend, not the language a marketer would use describing them.
- Three to five specific thoughts beats ten general ones. Too many fragments dilute the focus — AI starts trying to address all of them.
- The first third of any piece must stay inside the reader's world before introducing the product.
- Source the fragments from real artefacts where possible — customer interviews, support tickets, reviews, sales call recordings. Without real audience data, AI produces "convincing internal monologue fragments that sound right but might not match what your actual readers think."
- If you can't articulate the existing conversation, that's not a prompting problem — it's a research problem. The prompt can wait.

## How to audit (reviewer's checklist)

Pass/fail tests:

1. **Opening location.** Where do the first two paragraphs live — in the reader's world, or on the product? Anything that opens with the product, a statistic, or a rhetorical question fails. Open inside a specific moment the reader will recognise from their own experience.
2. **First-third rule.** Measure the first 33% of the piece. Is it about the reader's situation, frustrations, attempts to fix it? If the product appears before the reader feels understood, fail.
3. **Buyer-language fidelity.** Pull every sentence describing the reader. Does the language match how the reader talks to a friend, or how a marketer describes them? "Optimise operational efficiency" fails. "Stop spending every Monday pulling numbers from four different dashboards" passes.
4. **Three-to-five thoughts ceiling.** Count the distinct internal-monologue fragments referenced. More than five and the focus dilutes; the piece is trying to address all of them at once.
5. **Enter, don't answer.** Does the opening describe the world the reader is living in, or does it leap to the solution? Solution-first openings fail Collier's "enter, not answer" rule.

## Examples from the newsletter

**Product-first prompt vs reader-first prompt.**

Prompt that fails:
> "Write a sales email for a project management tool targeting small business owners."

Output starts from the product, lists features, lists benefits. Competent and completely generic.

Prompt that passes:
> "Write a sales email for a project management tool. The reader is a small business owner who just lost a freelance contractor mid-project and is personally picking up the slack. They're managing tasks across sticky notes, text threads, and a spreadsheet that stopped being useful two weeks ago. They don't want project management software. They want to stop feeling like everything is about to fall through the cracks."
>
> "Start the email inside that feeling. Don't mention the product until the reader feels understood."

Different output. Email opens in the reader's world. Earns the right to talk about the product by demonstrating it understands the problem first.

**Generic audience vs specific reader anchoring.** "Targeting small business owners" pulls from the broadest patterns AI has — output sounds like every other piece of copy addressed to small business owners. Describing a specific person managing tasks across sticky notes after losing a contractor narrows the generation space — output gets specific because the input got specific.

## Anti-patterns

- **Starting from the product.** Most prompts are written from the seller's perspective because the person writing is the seller. They're thinking about their product. So the prompt is about their product. So the copy is about their product. The reader and their existing desires never enter the equation.
- **Answering instead of entering.** Solving the reader's problem in the opening line skips the trust-building work. Demonstrate understanding first, prescribe second.
- **Generic monologue without source data.** Without real audience data, AI produces psychologically plausible text that's really well-structured guessing. Plausible isn't the same as accurate.
- **Too many fragments.** Ten general thoughts pulls the piece in ten directions. Pick three to five sharp ones.
- **Marketer language smuggled in.** "Optimise operational efficiency" is the brief. "Stop spending every Monday pulling numbers from four different dashboards" is the buyer. The first one keeps the prompt's mental model corporate; the second carries the buyer's voice into the output.

## Exact prompts / templates

### Step 1 — Map the mental conversation (verbatim)

```
I'm writing copy for [product/service] targeting [audience]. Before I
write anything, help me map the mental conversation this reader is having
right now.

What are they frustrated about today? What did they try that didn't work?
What are they worried about that they haven't told anyone? What do they
want that feels just out of reach?

Be specific. Use the language they'd use when talking to a friend, not the
language a marketer would use to describe them.
```

### Step 2 — Build the writing prompt around the conversation (verbatim)

```
Write a [format] for [product]. The reader is currently thinking:

- "I've tried three different tools this year and none of them stuck"
- "My team says they want better processes but nobody actually follows
   them"
- "I don't have time to learn another platform"

Start inside one of these thoughts. The reader should feel like you've
been listening to them. Don't mention the product until they feel
understood.
```

### First-third structural constraint (verbatim)

```
Structure: spend the first third of this piece in the reader's world.
Describe their situation, their frustrations, their attempts to fix it.
Only introduce the product after you've earned the reader's attention by
showing you understand their problem.
```

### Buyer-language extraction from interviews (verbatim, from cai #41)

```
Read these customer interviews. Pull out every statement where the
interviewee describes a frustration, a desire, or something they wish
were different about their current situation. Keep their exact phrasing.
Don't paraphrase or clean up the language.
```
