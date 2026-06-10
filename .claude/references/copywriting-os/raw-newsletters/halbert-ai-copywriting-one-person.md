---
title: "Halbert Would Have Loved This (And Hated Most of It)"
subtitle: "Halbert Would Have Loved This (And Hated Most of It)"
description: "Gary Halbert's three best ideas — the A-pile/B-pile test, the coat of arms research method, and the \"one person\" rule — rebuilt as a working Claude system for better prompts."
url: https://www.copywriting.ai/p/halbert-ai-copywriting-one-person
published_at: 2026-04-13T10:51:00.000Z
slug: halbert-ai-copywriting-one-person
---

# Halbert Would Have Loved This (And Hated Most of It)

Hey, Mark Masters here.

Gary Halbert would have had opinions about all of this.

He'd have loved the speed. The idea that you can test a hundred subject lines before breakfast would have made him cackle. He would have hated most of the output. The generic benefits. The invented urgency. The "imagine" sentences that describe feelings nobody is actually having.

I've been thinking about what he'd keep and what he'd throw out. The more I looked, the more I realized his three most famous ideas are the exact fix for what's wrong with most LLM-generated copy.

The A-pile/B-pile test. The coat of arms method. The one-person rule.

Each one solves a specific problem you're probably having with Claude right now.

## Halbert Would Have Loved This (And Hated Most of It)

### The Man, Briefly

You know who Gary Halbert was. I'll skip the biography and name the three things that matter here.

He wrote the most-read sales letter in direct mail history. He ran a daily email newsletter in the late 1990s that working copywriters still reference. And he spent forty years developing an obsessive discipline for figuring out exactly who he was writing to before he wrote a single word.

The first two are why people quote him. The third is why his copy worked. And it's the one that matters most for how you use Claude.

Here's how to take the three ideas he's remembered for and turn them into a working system.

## Idea 1: The A-Pile Test

Halbert's A-pile/B-pile concept was about physical mail. When you checked the mailbox, you'd sort letters into two piles without thinking about it. The A-pile was personal correspondence. Handwritten envelopes, letters from people you knew, things that looked like they came from a human. The B-pile was everything else. Business mail, bills, junk. You opened the A-pile first. The B-pile might not get opened at all.

His claim was simple. Most direct mail failed because it looked like B-pile mail. The fix was to make your envelope look like it belonged in the A-pile. Handwritten address. Real stamp. Nothing that screamed "this is a sales piece."

The translation to email is obvious and most people get it wrong.

Your reader sorts their inbox the same way. Not consciously. In the first quarter-second of looking at a subject line and sender name, their brain decides whether this feels like something from a person or something from a marketing department. A-pile or B-pile. The A-pile gets opened. The B-pile gets archived in a batch at the end of the day, if ever.

The reason most LLM-generated email subject lines land in the B-pile is that they sound like subject lines. They have the shape of marketing copy. "Transform Your Workflow Today." "5 Ways to Boost Productivity." "The Ultimate Guide to X."

You've written those. I've written those. Claude will write them by default because the training data is stuffed with them.

Here's a Halbert-flavored prompt that gets you out of B-pile defaults:

I'm writing an email to [specific reader — be granular, one person]. The purpose is [one sentence on what the email needs to do].

Generate 15 subject lines. Every one of them has to pass the A-pile test:

Would this subject line look like something from a person who knows the reader, or like something from a marketing department?

Rules:

- No numbered lists in the subject ("5 ways to...")

- No titles that start with action verbs in imperative mood ("Transform...", "Discover...", "Unlock...")

- No colons separating a setup from a promise

- No words that only appear in marketing copy ("ultimate," "essential," "proven")

- Prefer lowercase where it would feel natural in a personal email

- Length should vary. Some very short. Some longer and more specific.

For each subject line, tell me in one phrase why it passes the test. If you generate something that sounds like marketing copy, throw it out and try again.

The constraint list is the whole trick. Each rule cuts off a category of default behavior that lands copy in the B-pile. Without those constraints, Claude will give you competent, forgettable subject lines because that's what the training data rewards. With them, you force the output into a different shape.

When I run this prompt against a real project, I throw out about half the results. The half I keep are usually better than what I'd have written from scratch. Not because Claude is more creative than me, but because having 15 constrained attempts in front of me breaks the two or three patterns I tend to default to.

## Idea 2: The Coat of Arms

Halbert's research discipline is the one people don't talk about enough. Before he wrote copy for a product, he built what he called a coat of arms for the audience. A detailed portrait of who he was selling to. What they read. What they feared. What they spent money on without thinking. What they lied about at parties. What they'd never admit to wanting but absolutely wanted.

He did this work in an era without customer interviews, surveys at scale, or any of the digital research tools we take for granted. He read magazines his audience read. He studied what advertisers paid to reach them. He hung around in places where his buyers gathered. The coat of arms was the output of that work — a working document he referenced every time he sat down to write.

This is what most LLM-generated copy is missing. Not because the writer doesn't know their audience. Because the audience understanding never makes it into the prompt.

You can describe the coat of arms to Claude in about 200 words and it changes everything the output does.

Here's the template I use:

AUDIENCE COAT OF ARMS: [Name of audience]

Who they are (specific, not demographic): [Not "B2B marketing directors age 35-50." Instead: "Marketing directors at B2B SaaS companies between Series A and Series C, typically the second or third marketing hire, reporting to a founder who doesn't quite understand what they do."]

What they read when nobody's watching: [The newsletters they actually open. The podcasts they listen to in the car. The Twitter accounts they check before sleep.]

What they say they want: [The version they'd give in a formal interview.]

What they actually want: [The underneath version. What would actually make them feel successful.]

What they're afraid of: [Specific fear, not generic "failure." "Getting fired because the CEO wants to see a growth number they can't produce."]

What they've already tried: [Products, approaches, or consultants they've worked with before. This tells the LLM what the reader has already seen.]

The lie they tell themselves: [The thing they know isn't quite true but keep repeating to get through the quarter.]

A specific Tuesday in their life: [Three sentences describing an ordinary, non-dramatic moment. Not the crisis. The background hum of their actual day.]

That last field is the one that makes the biggest difference. Everything above it can come out sounding abstract. The "specific Tuesday" field forces you to put the reader in a real moment. Claude writes differently when the reader exists as a person in a situation instead of as a demographic.

Write the coat of arms once per client or audience. Save it. Load it into the top of any prompt where Claude is going to write to that person. The output stops sounding like it was written for a category and starts sounding like it was written for a human.

A warning: do not use a generic LLM-generated coat of arms. I tested this. If you ask Claude to generate the coat of arms from scratch based on a product description, you get back the same vague portrait Claude was going to write copy for anyway. You have to do the research work yourself. Customer interviews, support tickets, review mining, sales call recordings. The point of the coat of arms is that it contains specifics the LLM doesn't have access to from training data. If you fill it with training-data specifics, you've accomplished nothing.

## Idea 3: The One-Person Rule

Halbert's most repeated piece of advice: "Write to one person."

Not a persona. Not a customer segment. One actual human being with a name, a job, a situation. When he wrote, he'd often pick a real person he knew who fit the audience and write the letter as if he were sending it to them specifically. The copy came out sounding like a real communication because it was aimed at a real target.

This is the single most underused LLM prompting technique I know. It takes one line to add and it changes the output more than almost any other instruction.

Here's the add-on. You slot it into any writing prompt after your other instructions:

Before you write, do this: think of a specific person this copy is being written to. Give them a name, a job, and a one-sentence description of the moment they're in when they read this. Then write as if you were sending this directly to that person.

Do not write for the audience. Write for that one person.

At the end of your response, tell me who you imagined. Name, job, moment.

The "tell me who you imagined" line is the enforcement mechanism. Without it, Claude will nod at the instruction and write to the audience anyway. With it, you get to see whether the one-person framing actually happened. When the imagined person is generic ("Sarah, marketing manager, busy"), the copy will be generic too. When it's specific ("Priya, Head of Growth at a 40-person Series A SaaS, reading this at 7:45pm on a Tuesday with her dinner cooling on the counter because she's trying to finalize next quarter's plan before her 1-on-1 tomorrow"), the copy comes out sharper.

Ask for a rewrite when the imagined person is too generic. "Make the person more specific. Give me a version with a real situation in a real moment." That second pass usually produces noticeably better copy than the first.

## The Build: Halbert's Trio as a Single System

The three ideas work individually. They work better as a system. Here's how they fit together.

Run them in order. Coat of arms first, because everything else depends on it. One-person rule second, because it narrows the coat of arms into a specific target. A-pile test last, because it applies to the surface layer of whatever you produce.

In practical terms, your project setup looks like this. Create a Claude Project for each client or audience. Load the coat of arms as a knowledge file. Put this in the project instructions:

You are writing copy for [audience name]. The coat of arms for this audience is in your knowledge base. Read it before responding to any writing request.

Standard operating procedure for any writing request:

1. Reference the coat of arms specifics before generating any copy.

2. Name the specific person you're writing to (one real moment, not a demographic).

3. Produce the copy aimed at that one person.

4. If the output is a subject line, headline, or anything the reader sees first, apply the A-pile test: does this look like it came from a person or a marketing department?

5. At the end of each response, briefly state which coat of arms specifics you used and who you imagined writing to.

Do not skip step 5. It's how the user checks your work.

That last rule is the quality control. When you look at the output and the "who I imagined" section is vague, you know the copy will be vague. That tells you to push back before you even read the draft. When the imagined person is specific and the coat of arms references are real, the copy is worth reading.

## What Halbert Would Have Hated

Fair is fair. Here's what he would have objected to.

He would have hated the speed without the research. The whole point of the coat of arms is that it took real work. Building a system that lets you skip the research and just prompt your way to output is the thing he spent his career arguing against. The Halbert-flavored LLM workflow only works if you do the research part yourself and feed the specifics into the prompt. Skip that and you get faster garbage.

He would have hated the generic voice. Halbert's copy sounded like him. Sharp, slightly profane, absolutely certain. Claude's default voice is the opposite — smooth, careful, inoffensive. If you want copy that sounds like a person, you have to tell Claude explicitly not to sand the edges off. Halbert would have added a voice constraint to every prompt. So should you.

And he would have hated anyone who treated a prompt as a substitute for understanding the reader. The LLM is a writing speed multiplier. It is not a research shortcut. You still have to know who you're writing to. If you don't, no prompt structure in the world will save you.

# The Master’s Memo

Halbert's three ideas still work because they were never about the medium. They were about the reader.

Put the coat of arms into the prompt, name the one person, and apply the A-pile test to anything the reader sees first.

You'll produce copy that sounds like a human wrote it because a human did the thinking that made it possible.

More clicks, cash, and clients,

Mark Masters
