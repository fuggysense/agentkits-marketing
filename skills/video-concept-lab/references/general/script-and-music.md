# Script And Music

Use after a concept is selected. In Video Concept Lab this is still a draft pass: it gives the user enough substance to approve the concept at Approval Gate 1. The final production script is created after Approval Gate 1 during script/visual refinement and saved as `final-script.md`.

## Script Types

### Voiceover Script

Use when an unseen narrator or creator VO carries the ad.

Required:
- 0-3s hook.
- Problem or desire.
- Mechanism or reason-to-believe.
- Proof.
- Transformation.
- CTA.
- Visual notes per line.

### Avatar Acting Script

Use when one, two, or three characters appear on screen.

Required:
- Character list.
- Line ownership by character.
- Physical acting beats.
- Eye contact and camera notes.
- Emotional state per beat.
- Timing.

New fictional or realistic avatars are allowed, but reusable avatar personas require user approval before being added to client assets.

### Singing Ad

Use when the ad depends on melody, rhythm, jingle, or musical performance.

Required:
- Lyrics.
- Full music direction.
- Vocal style.
- Genre/style references.
- Tempo/BPM range.
- Structure: intro, verse, pre-chorus, chorus, tag, outro as needed.
- Hook timing: where the product/offer line lands.
- Visual performance direction.
- Music generation brief for Suno or other music tool.

Do not call Suno or any music API from this skill.

### No-Dialogue Ad

Use when the ad should work without spoken words.

Required:
- Silent visual beat script.
- Rendered text plan, if any.
- Explicit `subtitle_policy: none`.
- Music and sound design.
- Camera/action timing.
- Proof/CTA representation through visuals or rendered text.

## Six-Checkpoint Script Analysis

Analyze scripts against:
1. Pain acceptance.
2. Trust building.
3. Curiosity amplification.
4. Value delivery.
5. Emotional transfer.
6. Clear CTA.

For no-dialogue ads, map each checkpoint to a visual beat rather than spoken copy.

## Refinement Handoff

After Approval Gate 1, refine the selected script before any client brief or Video Factory handoff is created.

The refinement pass must produce:

- `final-script.md`: final hook, spoken lines or visual beats, timing, CTA, acting/VO/music/SFX notes.
- `visual-treatment.md`: final visual concept, scene logic, rendered-text policy, style direction, and input asset implications.

Use `script-skill` as the refinement lens when the ad depends on voiceover, dialogue, or acting. For no-dialogue ads, refine the visual beat script instead of adding subtitles.

## Music Brief Shape

```json
{
  "music_use_case": "singing-ad | jingle | background-score | no-dialogue-score",
  "generation_access": "manual_suno_only",
  "suno_mode": "simple | custom | instrumental | add_vocals | voice_model",
  "lyrics": "",
  "genre": "",
  "mood": "",
  "tempo_bpm": "",
  "vocal_style": "",
  "instrumentation": [],
  "structure": [],
  "hook_line": "",
  "brand_words_to_include": [],
  "words_to_avoid": [],
  "duration_target": "",
  "loopable": false,
  "reference_tracks": [],
  "negative_exclude": [],
  "rights_and_consent_notes": [],
  "commercial_use_checklist": [],
  "video_beat_map": [],
  "suno_prompt": "",
  "suno_custom_lyrics": "",
  "suno_style_of_music": "",
  "suno_title": ""
}
```

## Suno Manual Target

As of the current research pass, do not assume Suno API access. Treat Suno as a manual creative target unless the user later installs or approves a specific official or third-party integration.

For Suno-ready outputs, separate:
- Concept.
- Lyrics.
- Style prompt.
- Exclude/negative elements.
- Voice or persona requirements.
- Rights and consent notes.
- Commercial-use checklist.
- Video beat map.
- Manual paste steps.

Recommended YAML shape:

```yaml
music_ad_type: singing_ad | jingle | music_bed | hook_song | product_chant
generation_access: manual_suno_only
suno_mode: simple | custom | instrumental | add_vocals | voice_model
title:
duration_target_sec:
platform_use: paid_social
simple_prompt:
style_prompt:
genre_stack:
mood:
tempo_bpm_or_feel:
vocal_direction:
instrumentation:
instrumental: false
lyrics_brief:
lyrics:
  intro:
  verse:
  pre_chorus:
  chorus_hook:
  bridge:
  outro:
structure_timeline:
negative_exclude:
brand_offer:
cta_line:
must_say:
must_not_say:
voice_or_persona_requirement:
rights_and_consent_notes:
commercial_use_checklist:
video_beat_map:
variant_prompts:
manual_suno_steps:
```
