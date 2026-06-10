---
title: "The (AI) Swipe File Engine"
subtitle: "The (AI) Swipe File Engine"
description: "Most copywriters have a swipe file they never use. This Claude Project build turns it into a working resource you can query by problem, audience, or structure in under a minute."
url: https://www.copywriting.ai/p/swipe-file-engine-claude-project
published_at: 2026-04-09T10:37:00.000Z
slug: swipe-file-engine-claude-project
---

# The (AI) Swipe File Engine

Hey, Mark Masters here.

Your swipe file is probably a graveyard.

Mine was for years. A folder full of PDFs, screenshots, bookmarked URLs, and a Google Doc with quotes I promised myself I'd come back to. I never came back to it. I'd start a project, remember the folder existed, open it, scroll for four minutes, close it, and go write the hard way.

The problem isn't that you don't have good reference material. You do. The problem is that a folder of files isn't a working resource. It's a pile.

I rebuilt mine last quarter as a Claude Project with structured metadata and a handful of query prompts I use every time I sit down to write. Now it answers questions like "what have I saved that handles a skeptical B2B audience at the awareness stage of 'knows the problem, hates the usual solutions'" in about thirty seconds.

Here's the full build.

## Turn Your Dusty Reference Pile Into a Working Claude Project

### The Problem With How You're Storing Reference Copy

Most working copywriters have the same broken setup. A folder somewhere with screenshots and saved PDFs. A bookmark collection. Maybe a Notion database that looked promising for a week.

Somewhere in there is two hundred pieces of excellent copy that taught you something when you saved it.

You never reference any of it.

When you sit down to write a cold email for a mid-market SaaS client, you don't scroll back through three years of saved Halbert letters. You write the email from scratch, using whatever patterns are currently in your head. The swipe file might as well not exist.

The issue is retrieval. You can't search a pile of screenshots for "how did anyone handle a price objection in the first 50 words of an email." You can search by filename if you were disciplined about naming, and most of us weren't. So the file sits there, accumulating, earning nothing.

The Swipe File Engine fixes this by doing two things. It turns each piece of reference copy into a structured entry Claude can actually reason about.

And it gives you a set of query prompts you run when you're stuck or starting a new project, so the swipe file gets pulled into the work instead of sitting next to it.

## How the System Works

At a high level: one Claude Project holds your entire swipe file. Each piece of reference copy becomes a short structured entry with the full text plus metadata about what the copy is doing, who it's targeting, and what problem it solves. Your project instructions teach Claude how to read those entries and how to respond when you ask questions. A small set of query prompts handles the retrieval work.

You build it once. After that, every project you start can pull relevant reference material without you doing the work of remembering what you have.

Three components.

Component #1: The Entries. Each piece of saved copy gets an entry in a standard format. This is the piece most people skip. They upload a folder of PDFs to a Claude Project and expect magic. You'll get better results if each entry is structured so Claude knows what it's looking at.

Component #2: The Project Instructions. A system prompt that tells Claude how to use the entries. What questions to expect, how to cite entries when it pulls them, and what to do when there's no good match in the swipe file.

Component #3: The Query Prompts. A few saved prompts you use depending on what you're working on. Headline research. Structural pattern lookup. Objection handling. Opening line pull. These are the prompts that turn the Project into a daily working tool instead of something you built once and forgot.

Let me walk through each.

### Step 1: Set Up the Project

Go to [claude.ai/projects](https://claude.ai/projects) and create a new Project. Name it "Swipe File Engine" or whatever makes sense to you. The name doesn't matter. What matters is that it has its own Project so the knowledge base is isolated and the instructions apply every time you open it.

Under project instructions, paste this as a starting point:

You are a reference librarian for a working copywriter's swipe file. Your job is to help the copywriter find and apply reference material from their collection when they're working on a new project.

The knowledge base contains structured entries for pieces of copy the copywriter has saved over time. Each entry includes the full copy, plus metadata about:

- Source (where it came from)

- Format (email, landing page, headline, ad, etc.)

- Audience (who it was written for)

- Awareness stage (using Schwartz's framework)

- What it does well (the specific technique or strength)

- Why the copywriter saved it

When the copywriter asks a question, your job is to:

1. Find entries that match the request

2. Quote the relevant section of the copy

3. Explain what the technique is doing and why it fits the request

4. Cite which entry it came from by name

If nothing in the swipe file matches, say so directly. Don't manufacture an example from general knowledge. Tell the copywriter "nothing in your swipe file handles this well" and let them decide what to do.

When the copywriter is drafting new copy and asks for structural inspiration, pull 2-4 relevant entries rather than one. Show them the pattern variations.

Do not rewrite the swipe file copy into new copy unless explicitly asked. Your default role is research, not generation. The copywriter will tell you when to switch modes.

A few notes on why it's structured this way.

The "reference librarian" framing matters. Without it, Claude tends to drift into generating new copy when you ask for examples. You want retrieval first. Generation second, only on request.

The "cite which entry it came from" instruction prevents hallucination. If Claude can't cite an entry, you know it made something up. That's the trust check that makes the system usable under deadline pressure.

The "if nothing matches, say so" rule is the one I spent the most time on. Early versions of this had Claude pulling weak matches and pretending they were strong. It would cite a B2C email when I asked for a B2B example and paper over the mismatch. Adding explicit permission to say "nothing fits" fixed most of that.

### Step 2: Build the Entry Format

This is where the work is. Each piece of reference copy gets an entry that looks like this:

---

ENTRY: [Short name for the piece]

SOURCE: [Where it came from. Brand, writer, or "unknown"]

FORMAT: [email / landing page / headline / ad / sales letter / etc.]

DATE SAVED: [When you added it]

AUDIENCE: [Who the copy was written for. Be specific.]

AWARENESS: [Unaware / Problem-aware / Solution-aware / Product-aware / Most aware]

DOES WELL: [1-2 sentences on the specific thing this piece does that you wanted to remember]

WHY I SAVED IT: [Your note to your future self about what you were thinking]

COPY:

[The full text of the piece, or the relevant section if it's long]

---

You need one of these for every piece in your swipe file. I know. That's the part that sounds tedious.

Here's how to make it less tedious. You don't need to convert your entire swipe file in one sitting. You need to convert the next twenty pieces you reference. Then the next twenty. Within a month you'll have the ones that matter and you'll stop converting the rest because you'll realize you were never going to use them anyway.

To speed up the conversion itself, use Claude to help. Give it the raw copy (paste the text, upload the screenshot) and this prompt:

I'm converting a piece of reference copy into a structured entry for my swipe file. Here's the format I'm using:

[paste the entry format from above]

Here's the raw copy:

[paste or attach the copy]

Fill in everything you can from the format. For the AUDIENCE, AWARENESS, DOES WELL, and WHY I SAVED IT fields, make your best guess and mark it with [GUESS] so I can review and adjust. Be specific about what the copy does — not "good headline" but "reframes a feature as a behavioral change."

That prompt does about eighty percent of the work. You read through, fix the guesses, and save the entry. I can do five or six pieces in ten minutes this way. Over a week of casual work, you'll have a meaningful library.

Save each entry as its own file in a folder. Once you have a batch, upload them to the Claude Project as knowledge files. You can upload up to several hundred documents per Project, which is more than most working copywriters will have in a usable swipe file.

### Step 3: The Query Prompts

This is the part that turns the Project from a static knowledge base into a working tool. Here are the four I use most.

Query Prompt 1: Headline Pattern Lookup

I'm writing a headline for a [audience] piece at the [awareness stage] awareness stage. The core promise is [one-line summary of what I'm trying to say].

Pull 3-4 headlines from the swipe file that handle similar setups. For each one:

- Quote the headline

- Cite the entry name

- Explain the structural move it's making

- Note why it fits (or partially fits) my situation

If nothing in the swipe file is close, tell me so I can write from scratch.

This replaces the thing I used to do when I'd stare at a blank page trying to remember a headline pattern I knew I'd seen somewhere. Now I just run the query. Thirty seconds, and I have three patterns to adapt.

Query Prompt 2: Objection Handling

I'm writing for [audience] and I need to handle the objection: [the specific objection, in the customer's own words if possible].

Find entries in the swipe file where a piece of copy handles the same objection or a close cousin. For each match:

- Quote the section where the objection gets handled

- Cite the entry name

- Explain what the technique is (reframe, proof, concession, pivot, etc.)

- Tell me how I'd adapt it for my context

Prioritize entries where the objection is handled in-line rather than pre-empted. I want to see how the copy recovers, not how it avoids the problem.

Objection handling is the place where my swipe file earns the most for me. I don't have to remember the specific email that handled "your product is too expensive" well. I just ask.

Query Prompt 3: Opening Move

I'm writing a [format] for [audience]. The piece needs to open in a way that [intent — "establishes credibility in one line," "creates curiosity without being clickbait," "enters the conversation in the reader's head," etc.].

Pull 2-4 opening lines or first paragraphs from the swipe file that do this. For each:

- Quote the opening

- Cite the entry name

- Explain what the move is accomplishing

- Rate how close the match is to my situation (exact / close / loose)

Opening moves are pattern-dense. Copywriters who've been around a while have fifteen openings they cycle through without thinking. The Engine gives you access to the ones that aren't already top-of-mind.

Query Prompt 4: Structural Pattern Match

I'm drafting a [format]. The structure I'm considering is [sketch of the structure — "problem, then failed solutions, then new frame, then offer" or similar].

Find 2-3 entries in the swipe file that use a similar structure. For each:

- Cite the entry name

- Outline the structure the piece actually uses

- Note where it diverges from mine

- Tell me what it does at transition points I'm likely to fumble

I want to see how other writers handled the same shape, not validation that my shape is good.

That last line is the one that matters. Without it, Claude will reassure you that your structure is fine. With it, you get actual comparison material. The point of the swipe file is to learn from people who solved the problem before you. Reassurance isn't learning.

### What to Watch For

A few things I had to fix after using this for a few weeks.

Claude will occasionally hallucinate entries. If you ask for something the swipe file doesn't have, and your project instructions aren't tight, it'll make up a plausible example. This happened to me twice before I added the explicit "if nothing fits, say so" rule. Test this deliberately. Ask for something you know isn't in there. If it invents an entry, tighten your instructions.

Metadata quality determines retrieval quality. I added fifty entries in a hurry one weekend and did a lazy job on the DOES WELL field. When I ran my query prompts, Claude couldn't find good matches because my own descriptions were vague. "Strong emotional hook" is useless metadata. "Uses a specific sensory detail in the first 15 words to create scene" is useful. Spend the extra thirty seconds on that field.

The Engine gets better as you add entries, up to a point. Around 80-100 entries, I stopped seeing meaningful improvement in retrieval quality. What I saw instead was Claude pulling redundant examples. If you have three emails that all handle price objections with the same reframe, the Engine will pull all three. You don't need that. Curate as you add. If a new entry is doing something you already have represented, skip it or retire an older one.

You will start saving better reference material. This is the part I didn't expect. Once the Engine existed, I started noticing copy in the wild differently. Instead of "that's a good email, I'll screenshot it," my brain started asking "what would the DOES WELL field say?" The act of articulating why a piece of copy is worth saving makes you read copy more carefully. That's a second-order win I'd pay for on its own.

### What to Expect

If you build this properly, a normal session looks like this. You open a new client project. You read the brief. You run Query Prompt 1 against the Engine to see if anything in your swipe file handles the setup. You get back three headline patterns to adapt. You run Query Prompt 3 for opening lines. You start writing.

The Engine doesn't write for you. It shortens the distance between "staring at a blank page" and "I have three directions I trust." That's the entire value.

First drafts still come from you. The Engine just makes sure you're drawing from the best material you've saved instead of defaulting to the five patterns you can recall under pressure.

# The Master’s Memo

A swipe file that sits in a folder is a museum. A swipe file you can query is infrastructure.

The difference is thirty minutes of metadata work per entry and one Claude Project. Build it this week.

The first time it saves you forty-five minutes on a deadline, you'll wonder why you waited.

More clicks, cash, and clients,

Mark Masters
