---
title: "The Worst AI Sales Page I Read This Month"
subtitle: "The Worst AI Sales Page I Read This Month"
description: "A real AI-generated sales page taken apart element by element. What went wrong at the prompt level, what it reveals about LLM defaults, and the fix you can apply to your own drafts today."
url: https://www.copywriting.ai/p/worst-ai-sales-page-teardown
published_at: 2026-04-16T10:03:00.000Z
slug: worst-ai-sales-page-teardown
---

# The Worst AI Sales Page I Read This Month

Hi, it's Peggy.

I read a lot of sales pages for this job. Some are great. Most are fine. A few are the kind of bad that's actually useful, because the failure mode is so clean you can see exactly what went wrong.

I found one of those last week. A real sales page, live on a real site, for a real product. I'm not going to name the company. I've changed the product details just enough to keep them anonymous. Everything else — the structure, the prompts I'm pretty sure were used, the language patterns — is exactly as I found it.

This piece was written with an LLM. You can tell from about the third paragraph. And the specific ways it fails are the same ways most LLM-generated sales pages fail when the writer trusts the first draft.

Let me walk you through it.

## The Worst AI-Generated Sales Page I Read This Month: A Teardown

### The Product and the Setup

The product is a scheduling tool for independent service providers — think massage therapists, tutors, personal trainers. The kind of solo operator who books appointments, takes payments, and sends reminders. A real category with real competitors.

The sales page is the main conversion page from their ads. I won't reproduce the whole thing. I'll quote specific sections with their originals lightly altered, then show you what the page is doing and why it isn't working.

The reason I picked this one for a teardown: I've seen the same failure modes across at least a dozen LLM-generated sales pages this quarter. This one is a clean example of all of them stacked in a single document. If you've been using Claude or ChatGPT for long-form sales copy, you've probably shipped something that hit at least two of these. I have too. This is the teardown I wish someone had shown me a year ago.

## Element 1: The Hero Section

The page opens with this headline:

❝

Transform Your Booking Experience With The Ultimate All-In-One Scheduling Solution

Four problems in twelve words.

"Transform" is a word Claude reaches for by default when it doesn't know what the product actually does. It signals enormous change without naming any specific change. The reader has no idea what will be different.

"Booking experience" is category-speak. It's what a product manager would write in a user story. It's not how a massage therapist thinks about her Tuesday morning. She thinks about whether she'll get a text from a client saying they can't make it at 10, and whether her Wednesday is full or not.

"Ultimate" and "all-in-one" are the two most overused qualifiers in LLM sales output. Both are generic claims that also happen to be defensive. The writer is trying to preempt "what if it doesn't do X" by promising everything, which tells the reader nothing and signals that the product is probably mediocre at several things.

"Scheduling solution" is the category, not the product. The reader didn't come to this page looking for a scheduling solution. She came looking for something that will stop her from double-booking on Saturdays.

What the headline should do: name a specific person in a specific situation and hint at the outcome. What this headline does: float above the page in a cloud of abstraction.

The subheadline underneath is worse:

❝

Empower your business with cutting-edge technology designed to streamline operations and maximize client satisfaction.

Three verbs Claude falls back on when it doesn't have specifics: empower, streamline, maximize. "Cutting-edge technology" is a phrase that appears nowhere in the reader's actual life. "Client satisfaction" is a category noun, not a feeling. This entire sentence could be pasted onto a sales page for any B2B SaaS product made in the last fifteen years and it would fit.

Diagnosis: The prompt that produced this was almost certainly something like "write a sales page headline and subheadline for a scheduling tool for independent service providers." The LLM was given the product and asked to sell it. So it sold it — in the blandest, most category-standard way possible. No specific reader. No specific moment. No specific promise.

Fix at the prompt level: Don't ask for a headline. Ask for a headline that names a specific person in a specific moment of their week. Example:

Write 10 headlines for the hero section of this sales page. Each headline must do three things:

1. Name a specific moment in the reader's week (not a category like "scheduling" or "booking").

2. Reference an outcome the reader can picture.

3. Use language a solo service provider would actually use when talking about her own business. Not marketing vocabulary.

Ban the following words and phrases: transform, empower, streamline, maximize, ultimate, all-in-one, solution, platform, cutting-edge, seamless, effortless.

If you write a headline that feels like it could also sell a different product, throw it out and try again.

The bans are the lever. Without them, Claude will reach for the same five words every time.

## Element 2: The "Problem" Section

After the hero, the page has a section headed "The Problems You're Facing." It lists five bullet points:

- Lost bookings due to inefficient scheduling

- Time wasted on manual appointment management

- Frustrated clients who can't book at their convenience

- Missed revenue opportunities

- Inability to scale your business

Each of these is what I'd call a category abstraction. It names a problem shape without naming any actual problem.

"Lost bookings due to inefficient scheduling" is the kind of sentence you'd write if you'd never actually talked to a massage therapist. A massage therapist doesn't think about "lost bookings due to inefficient scheduling." She thinks about Grace, who texted to say she had to cancel, and the fact that Grace paid through Venmo last time and now she has to remember to not charge her for this appointment and also try to fill the slot before it's too late.

That specific moment is what a real problem section would open with. Instead, this section lists five generic problem shapes that every scheduling tool on the market could claim to solve.

Every bullet point has the same structural pattern: [negative state] + [generic cause]. Every one. That uniformity is a tell. Real problems don't all have the same shape. When every bullet in a list has the same grammar, it was written by an LLM pattern-matching on "list of problems."

Diagnosis: The prompt that produced this asked the LLM to "list the problems this product solves." The LLM returned a symmetrical, category-level list because that's what that prompt produces. The writer didn't push back.

Fix at the prompt level: Never ask for a list of problems the product solves. Ask for specific moments in the reader's week where the problem shows up. Example:

I'm writing the problem section of a sales page for [specific audience]. Instead of listing problems, I want to describe 3-4 specific moments from this person's week where the problem shows up.

For each moment:

- Name the day and approximate time

- Describe what the reader is doing in one sentence

- Describe what goes wrong or what they're worried about

- Use their internal language, not marketing vocabulary

Constraint: Do not write the moments with parallel structure. Each one should feel like a different kind of bad moment. A missed notification is different from a double-booking is different from a client who keeps rescheduling.

Draw on this audience research if I provide it: [paste your research]. If I haven't provided any, tell me what you need before you write.

That last sentence is the one most people skip. Telling Claude to ask for research before writing is how you stop it from inventing details.

## Element 3: The Benefits Section

This is the section where the page gave up pretending a human wrote it. Eight benefit statements, all in the same shape:

- Save Hours Every Week — Our intelligent scheduling system automatically handles appointment booking so you can focus on what matters most: your clients.

- Boost Your Revenue — With advanced features that optimize your calendar, you'll maximize every available slot and grow your business effortlessly.

- Enhance Client Satisfaction — Deliver a premium booking experience that keeps clients coming back and referring their friends.

And so on. Five more of these. All the same shape. Bold benefit headline, dash, one-sentence explanation using the words "intelligent," "advanced," "premium," "effortlessly," or "seamlessly."

Four problems.

First, the benefits are stated at the level of category outcomes. "Save hours every week" is true of every automation product ever sold. It communicates no specific value.

Second, the explanations use the exact same sentence structure eight times. That uniformity is soothing to write and exhausting to read. The reader's eyes start skipping after the third one.

Third, every explanation uses the word "you" in exactly the same position. "So you can focus." "You'll maximize." "That keeps clients coming back." This is a common LLM tell. Claude reaches for "you" as a rhythm stabilizer when it runs out of specifics.

Fourth, and this is the big one: every benefit is stated as a promise the product makes, not as a change in the reader's life. "Save hours" is what the product claims to do. "Stop scrambling every Sunday night to figure out if Monday is actually going to work" is what the reader experiences. One of those sells. The other decorates the page.

Diagnosis: The prompt was "write 8 benefit statements for this product." The LLM produced what that prompt produces: symmetrical, category-level promises in parallel structure.

Fix at the prompt level:

Write 5 benefit statements for this sales page. Rules:

1. Do not write in parallel structure. Each benefit should have a different sentence shape, a different length, and a different rhythm.

2. Each benefit must describe a specific change in the reader's actual life, not a capability the product has. Think "stop doing X on Sunday nights" rather than "save time."

3. Use the reader's voice. If the phrase sounds like it came from a product manager, rewrite it.

4. Do not use: seamlessly, effortlessly, intelligent, advanced, premium, streamline, empower, maximize.

5. Do not start more than one benefit with a verb. Vary the openings.

Before writing, tell me what audience research you're working from. If you don't have enough, ask me for it before writing.

The parallel-structure ban is the single most effective change you can make to benefit sections. It breaks the LLM's default rhythm and forces it to find different sentence shapes. Different shapes force different thinking.

## Element 4: The Testimonials Section

Three testimonials. All three start with the same move: a superlative, then a specific but interchangeable detail, then a generic endorsement.

"This is the best scheduling tool I've ever used. It saved me 10 hours a week and my clients love it." — Sarah M., Personal Trainer

"I can't imagine running my business without it. The automated reminders alone have cut my no-shows by 30%." — Michael R., Massage Therapist

"Absolutely life-changing for my practice. Everything just works." — Jennifer L., Yoga Instructor

I want to be careful here. I don't know whether these testimonials are real or invented. What I do know is that they read exactly like testimonials the LLM generates when you ask it to "write three customer testimonials for this product."

Real testimonials usually have one specific detail the writer didn't plan for — a brand name, a family member, a moment of frustration that resolved. These have none of that.

The numbers are suspicious too. "10 hours a week" and "30% fewer no-shows" are the kind of round, even numbers LLMs produce when asked for believable statistics. Real testimonials have odd numbers. "It saved me about six hours most weeks, maybe seven on a good week." "My no-shows went from three a week to about one."

Diagnosis: I can't prove these were LLM-generated from the copy alone. But the tells are stacked. If they're real, they were heavily edited into LLM shape. If they're not, they were fabricated and the writer should pull them immediately. Fake testimonials are a legal problem and an ethical one. I'm not going to pretend otherwise.

Fix at the prompt level: Don't ask an LLM to write testimonials. Ever. If you have real customer quotes, use Claude to help you format or shorten them. If you don't have customer quotes, get them before you publish. There's no shortcut here and no prompt that makes fake testimonials acceptable.

The one legitimate use I'd endorse: feed Claude a raw, long customer interview and ask for the 2-3 sentences that would work as a pullout quote, preserving the exact language. That's editing, not generation. It's fine.

### What This Page Should Have Done

Across all four sections, the problems have a common root cause. The writer gave Claude the product and asked it to sell the product. Claude sold the product — in the smoothest, most category-standard way it knew how. Every section was symmetrical, every sentence was inoffensive, every word was the word the training data expected.

The missing ingredient was the reader. Not a demographic. A specific person in a specific week with specific problems that don't all have the same shape. If the prompt had started from the reader's Sunday night and built outward, the page would have had specifics. Specifics are what separate copy that works from copy that fills a page.

Here's the single prompt change that would have rescued this whole document, applied at the start of every section:

Before you write this section, describe the reader to me. I want to know:

- A specific person (name, situation, one sentence on their business)

- What their Sunday night looks like when things are going badly

- What they're trying to do better, in their own language

- One sentence of something they've tried that didn't work

Do not write the section until you've done this. If I haven't given you enough information to fill this in, tell me what's missing.

Every section of that sales page would have been different if that prompt had run first. Not because the LLM would have written better — because the writer would have been forced to either answer the questions or admit they didn't know the answers.

That's the whole teardown in one sentence: the problem isn't Claude. The problem is that Claude lets you skip the thinking that used to happen before you wrote.

# The Burnett Matrix

The tells were all structural. Parallel bullets. Category abstractions. The same verbs in the same positions.

Those patterns are signs of a prompt that didn't specify a reader. Fix the prompt upstream and the structural tells disappear downstream.

Test this on your next draft — run a section through a "describe the reader to me first" prompt and see how differently it comes out.

More clicks, cash, and clients,

Peggy Burnett
