# Suno Manual Target

Last checked: 2026-05-13.

## Current Decision

Treat Suno as a manual creative target, not an automatable backend.

Video Concept Lab may produce Suno-ready prompts, lyrics, style prompts, and manual generation steps. It must not imply it can call Suno directly unless the user later installs or approves a specific integration.

## Practical Suno Creation Surface

Suno's user-facing creation modes support:
- Simple prompt mode: describe the song.
- Custom mode: supply lyrics, style, title, instrumental toggle, and advanced options.
- Exclude/negative elements for unwanted sounds or instruments.
- Longer model-dependent generations and extension workflows.
- Add Vocals / voice model workflows for eligible paid-account features.

## API Status

No official public Suno developer API or self-service API key flow was found in the research pass. Third-party "Suno API" options appear to be unofficial wrappers or external services. Treat them as risk-bearing integrations that require explicit user approval before use.

## Skill Output Rule

For singing ads, output:
- Lyrics.
- Style prompt.
- Music direction.
- Vocal direction.
- Structure/timeline.
- Negative/exclude list.
- Rights and consent notes.
- Commercial-use checklist.
- Video beat map.
- Manual Suno steps.

Do not output an API request object unless a real integration has been selected.

## Source Pointers

- Suno help center music creation: https://help.suno.com/en/categories/550017
- Suno custom mode: https://help.suno.com/en/articles/3197377
- Suno lyrics rights help: https://help.suno.com/en/articles/2415873
- Suno exclude elements help: https://help.suno.com/en/articles/3161921
- Suno song duration help: https://help.suno.com/en/articles/2409473
- Suno add vocals help: https://help.suno.com/en/articles/6882817
- Suno voices help: https://help.suno.com/en/articles/11362369
- Suno commercial/distribution rights: https://help.suno.com/en/articles/2410177
- Suno ownership help: https://help.suno.com/en/articles/2416769
- Suno terms: https://suno.com/terms

