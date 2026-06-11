# Headline Validation Checklist

Run every headline through ALL checks before presenting to the user. A headline must pass all 5 to be included.

## 1. UK English Spelling & Grammar

Check for common US to UK substitutions:

| US Spelling | UK Spelling |
|-------------|-------------|
| analyze | analyse |
| recognize | recognise |
| realize | realise |
| organize | organise |
| color | colour |
| center | centre |
| favor | favour |
| labor | labour |
| defense | defence |
| license (verb is fine) | licence (noun) |
| fulfill | fulfil |
| enrollment | enrolment |
| canceled | cancelled |
| traveled | travelled |
| aging | ageing |
| jewelry | jewellery |

Also check: -ize to -ise endings, -or to -our endings, -er to -re endings (where applicable).

**Fail condition:** Any US spelling present.

## 2. Factual Accuracy

Every claim in the headline must be verifiable against the client's data:

- [ ] Statistics match client proof elements
- [ ] Timeframes are accurate
- [ ] No invented case study details or fabricated numbers
- [ ] Industry terminology is correct for the market
- [ ] No implied financial guarantees (regulatory compliance)

**Fail condition:** Any unverifiable claim or invented statistic.

## 3. Persona Resonance

The headline must pass the persona identification test:

- [ ] Would this specific persona recognise themselves in the headline?
- [ ] Does it use language they would actually use or relate to?
- [ ] Does it reference a situation, fear, or aspiration documented in the buyer profile?
- [ ] Is the sophistication level right? (Not talking down, not over their heads)
- [ ] Would they share this with their partner?

**Fail condition:** Generic headline that could apply to anyone in any market.

## 4. Cultural Sensitivity

Load the client's locale rules from `clients/<project>/_brand/locale-rules.md` IF PRESENT (template + SG example at `clients/_template/_brand/locale-rules.md`). The old skill-global `sg-cultural-guidelines.md` is archived at `_archive/references-pre-ferres/`. Quick checks:

- [ ] No insensitive references to race, religion, or ethnicity
- [ ] Respects cultural norms of the target demographic
- [ ] No language that could be read as mocking financial struggles
- [ ] Appropriate during any current cultural/religious period
- [ ] No implied criticism of government policy

**Fail condition:** Any cultural insensitivity — even borderline cases get flagged.

## 5. Brand-Voice Compliance

Check against the client's `brand-voice.md`:

- [ ] Matches the documented tone
- [ ] Uses approved terminology
- [ ] Avoids all off-brand patterns listed in brand-voice.md
- [ ] No hard-sell language if brand is anti-pressure
- [ ] No generic industry language if brand differentiates from competitors

**Fail condition:** Headline sounds like it could come from any competitor.

## Anti-AI Slop Check

After all 5 checks pass, run against `overused-ai-patterns.md`:

- [ ] No em-dashes (replace with full stops or commas)
- [ ] No revelation hooks ("Here's the...", "The secret of...")
- [ ] No prohibited words from the overused-ai-patterns list
- [ ] No "It's not X, it's Y" constructions
- [ ] No performative emphasis ("Let that sink in", "Full stop")

## Presentation Format

When presenting validated headlines to the user, show the validation results inline:

```
| Rank | Headline | Type | UK✓ | Fact✓ | Persona✓ | Safe✓ | Brand✓ |
|------|----------|------|-----|-------|----------|-------|--------|
| 1    | "..."    | Question | ✓ | ✓ | ✓ | ✓ | ✓ |
```

Any headline with a failure should include a note explaining what failed and whether it's fixable.
