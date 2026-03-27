# Unslop Profile: pSEO Templates

Generated: 260319 | Samples: 50 | Model: Claude (default) | Type: text
Deduped against: overused-ai-patterns.md (3 patterns removed: em-dash overuse, "Not X, Y" contrast, "here's the/what")

**Constraint level: SOFT** (prefer to avoid; overused-ai-patterns.md is HARD)

---

## Meta-conversational scaffolding to eliminate

- No "Here's the complete template" / "Here's the full template" pivots
- No "I'll walk through it" / "I'll break down the key parts" narration
- No "Want me to..." closing menus
- No file-write status lines ("Template written to...")
- No permission error reporting before delivering the template

## Structural patterns to avoid

- Do not use the same section sequence every time. The canonical skeleton (Variable Reference -> Template Structure -> HTML -> Schema -> Uniqueness Levers -> SEO Notes -> Internal Linking -> Page Count Math -> Content Rules) is a dead giveaway. Vary the order. Omit sections that aren't needed.
- Do not default to "### Variable Reference" with a three-column markdown table.
- Do not use these section headings verbatim: "Variable Reference", "Template Structure", "Uniqueness Levers", "SEO Notes", "Schema Markup", "Page Count Math", "Key design decisions", "Data Sources", "Content Rules"
- Do not use three-tier variable architecture ("Global config -> per-dimension -> per-page combination") as the standard.
- Do not default to markdown tables for everything.
- Do not include a "Page Count Math" section that multiplies dimensions ("~15 types x ~500 cities = 7,500 pages"). Integrate naturally if needed.

## Phrases to never use

- "uniqueness levers" (AI-coined jargon, not real terminology)
- "mirrored in FAQPage JSON-LD" / any "mirrored in" construction
- "the variables that prevent thin/duplicate content"
- "just swapping a city name into identical text" / "city-name-swap thin content"
- "reading like one page with swapped names"
- "genuinely different" / "genuinely distinct"
- "eligible for [X] rich results"
- "signals a real directory, not a thin affiliate page"
- "'[specific claim]' says more than '[vague claim]'"
- "per combination" / "per pair" as reflexive scope descriptors
- "anti-slop" (no meta-commentary about slop avoidance inside templates)

## Technical defaults to break

- Do not automatically include FAQPage schema in every template (84% inclusion rate = reflexive, not considered). Only when FAQ content genuinely fits.
- Do not default to FAQPage + `<details>` + "mirrored" trinity.
- Do not default to BreadcrumbList + FAQPage + [domain type] as your three-schema stack. Consider what schemas actually serve the specific domain.
- Do not assume a static site generation / build pipeline workflow. Ask or infer from context.
- Do not prescribe "3-axis internal linking" or "multi-axis linking" as standard. Linking strategy should be domain-specific.
- Do not default to top CTA + bottom CTA structure in every template.
- Do not list government/public data APIs (BLS, NOAA, Census, EPA) unless specifically relevant.

## Tonal habits to avoid

- Do not adopt the same confident-expert declarative voice for every domain. Match tone to subject.
- Do not use "[good thing], not [bad thing]" contrast constructions reflexively.
- Do not use **`variable_name`** em-dash explanation format for every variable.
- Do not use italics for contrastive emphasis as a tic.
- Do not include "Content Rules" or writing quality meta-commentary inside the template itself.

## The matrix habit

Do not frame every pSEO project as a "matrix" (service x city, breed x product). Consider hub-and-spoke, hierarchical, network, sequential, or other structures depending on the domain.

---

Every pSEO template should feel like it was designed for its specific domain from scratch, not stamped from a master template with the nouns swapped out.
