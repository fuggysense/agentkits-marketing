# Research Calibration Interview

This is the instrument that sets your *standing* research floor — the bar `research_gate.py`
holds every client to before avatar, angle, or ad work runs. It is not the per-client builder
interview (that one lives in each client's `_brand/research-brief.md` under `## Builder interview`
and tunes one niche). This one is for you, the operator, across the whole roster you serve:
SG property strategy, DTC wellness, coaching, agency lead-gen, and whatever comes next.

The reason it exists: the gate ships with the Ferres floor as its default — three named research
docs, at least 20 verbatim customer phrases, a gap analysis, a human read-through, re-run if thin
(`_shared-knowledge/ferres/02-research-flow.md`). That floor is a borrowed opinion. It is Sean
Ferres's bar for his clients, not yet yours. Until you answer question 1 below, every brief that
reads `floor_profile: ferres-default` is running on his judgment. The whole point of the
gate is to encode *your* "good enough," then enforce it the same way every time so a thin research
pack can never quietly become an ad.

Answer these in order. Most answers either confirm a default or move one knob in the YAML. Where an
answer applies to a single niche, write it into that client's `research-brief.md`. Where it applies
to everything you do, change the default in `clients/_template/_brand/research-brief.md` so every new
client inherits it.

---

## The questions

**1. What does good-enough research look like before you'd let copy ship?**
The one you still owe. Forget the framework for a second. Picture the last time you read a research
pack and thought "yes, write from this" — and the last time you thought "this isn't enough, I'd be
guessing." What was different between the two? Name the thing that flipped it. That sentence is your
real floor; everything below is just turning it into knobs the gate can check. If you genuinely don't
have an answer yet, say so, keep `ferres-default`, and come back after the next campaign — the gate
still protects you at the borrowed bar in the meantime.

**2. Which is the wound you research toward — the same one every niche, or does it move?**
For Meridian it was trust ("whose side is the advice on"), not the fee. For a supplement it might be
"I've tried three things and none worked." The gate can't read for the wound, but knowing it tells
you whether a pack that's technically complete is actually pointed at the right pain. If the wound is
stable across a niche, note it in that client's brief so a reviewer knows what "on target" means.

**3. Twenty verbatim quotes — too few, about right, or too many for the work you do?**
Ferres's floor is 20 (`min_verbatim_phrases`). It exists so the copy can "feel like you read their
mind": exact phrasing, not paraphrase. Consumer and ESL niches usually need more raw quotes to find
the register; a narrow B2B niche with few public voices may justify fewer. Give me one number you'd
defend as your default, and the niches that should override it up or down.

**4. Where do your buyers actually talk, and which of those sources is non-negotiable?**
The gate's `required_sources` list is voice-of-customer, competitor intel, market context, client
assets. Ferres weights Reddit highest — "where people are the most brutally honest." But your SG
property buyers might live in Telegram groups and PropertyGuru reviews, and a wellness buyer in
Amazon reviews and TikTok comments. If a niche genuinely cannot supply one source type, that's a
real answer. But the gate will fail it silently unless you delete that source from the brief and
write down why. Which sources are mandatory, and which are allowed to be absent?

**5. What counts as a verbatim quote in your book?**
Right now the gate counts any quoted span of four or more words inside a research or buyer-profile
file. That's a heuristic, and it has a known leak: it cannot tell a real customer line from a
competitor's ad slogan sitting in your competitor notes. On the smoke client it counted 120 quotes,
most of them advertiser copy, when the honest VOC dump alone holds enough to pass. Do you want the
count restricted to designated VOC files only? Your answer decides whether that leak gets closed or
stays a known, accepted limitation.

**6. The four named artifacts — are they the right four for your pipeline?**
The gate checks for an ICP-equivalent, a competitor doc, a market doc, and a gap analysis, each
resolved against this repo's real filenames (`required_artifacts`). Ferres ships three PDFs; the
fourth, gap analysis, is broken out as its own checkable thing. Is anything missing for how you work
— a compliance dossier, an offer doc, a swipe file — that should be its own required artifact rather
than buried inside one of these?

**7. When research comes back thin, what's your real recovery — in order?**
The gate never auto-fixes a thin pack. It surfaces a ladder and you pick a rung
(`thin_data_fallback`): lean on competitors, reuse existing vault research, run the quick-brief
shortcut, re-run with more context, or record an override. The default order is Ferres's. For a niche
where you already have a fresh vault dossier, reuse should be rung one. For a brand-new niche with no
client data, competitors come first. Reorder the ladder per niche so the most viable move is at the
top — otherwise the operator under pressure picks the wrong rung.

**8. Who reads the research before it's used, and where do they record it?**
Ferres reads his docs himself and re-ran the prompts the time output came back thin. The gate cannot
verify a human read — it only reminds. So this is a process you own, not a check. Is the read-through
always you, or does it delegate? Where does the date-plus-verdict get written so the next person
knows it happened (`human_read_through.record_in`)? If the answer is "nobody, in practice," that's
the honest answer and the gate's reminder is doing nothing — decide if that's acceptable.

**9. What are the compliance landmines, and which research must surface them?**
Each niche carries its own ad-platform tripwires: income claims for money offers, health claims and
personal-attribute call-outs for wellness, CEA-licensing language for SG property. The gate checks
these are *named* in the brief (`compliance_constraints`), not that they're enforced — claim
enforcement is `claim_gate.py`'s job downstream. Which landmines repeat across your roster (set them
in the template) and which are niche-specific (set them per client)?

**10. Is the gate's PASS a hard stop, or advisory?**
The avatar-research skill now treats PASS as required and FAIL as a stop, with one escape: an
operator-recorded `research_gate_override` (with a reason) in the campaign's `pipeline-state.json`.
That's a real decision. A hard stop protects you from your own optimism but will block you at 11pm
when you "know" the research is fine. Do you want override to stay easy and logged, or harder: a
second name, a cooling-off, a required reason longer than one word? Right now it's easy and logged.

**11. When do you re-research a market you've already covered?**
The vault check treats a dossier under 60 days old as fresh and reusable. Is 60 the right staleness
line for your markets, or does fast-moving demand (a property cooling measure, a viral wellness
trend) need a shorter one? This isn't a gate knob yet — it lives in the avatar-research Phase 0 check
— but your answer tells me whether to make freshness configurable per niche.

**12. What's the one thing you've shipped from thin research and regretted?**
If there's a real example — an ad that missed because the pack guessed at the buyer — describe it.
That story is worth more than any default. It tells me which knob was actually wrong, and it's the
thing to re-read the next time the gate feels like friction instead of protection.

---

## What happens to your answers

- Niche-specific answers (2, 4 per-niche, 7, 9 per-niche) get written into that client's
  `_brand/research-brief.md` YAML and its `## Builder interview` notes.
- Roster-wide answers (1, 3, 5, 6, 8, 10) change the default in
  `clients/_template/_brand/research-brief.md` and, where the machine reads them, the
  `FERRES_FLOOR` block in `scripts/research_gate.py` — so every new client inherits your bar, not
  the borrowed one.
- Answers that point at gate behavior the code doesn't yet support (5's quote-source restriction,
  11's freshness line) become the next change to the gate, not a brief edit.

Until question 1 is answered, the floor is Sean Ferres's. The gate works either way. It just can't
be *yours* until you say what yours is.
