# Cinematography Reference for AI Video Prompts

Model-agnostic quick reference for camera angles, movements, shot types, and lens effects. Use these terms in video prompts for precise control over visual composition.

---

## Shot Types

### By Distance

| Shot Type | Frame | Best For | Prompt Language |
|-----------|-------|----------|----------------|
| **Extreme Close-Up (ECU)** | Single feature (eye, hand, product detail) | Emotion, texture, detail reveal | "extreme close-up of [subject's eyes / product label / texture]" |
| **Close-Up (CU)** | Face fills frame | Dialogue, reactions, testimonials | "close-up, face fills the frame, shoulders barely visible" |
| **Medium Close-Up (MCU)** | Chest and above | Talking head, podcast, interviews | "medium close-up, chest and above, conversational framing" |
| **Medium Shot (MS)** | Waist and above | Product demos, try-ons, gestures | "medium shot from the waist up, hands visible for gestures" |
| **Medium Long Shot (MLS)** | Knees and above | Standing presentations, outfit reveals | "medium long shot, knees and above, full outfit visible" |
| **Full Shot (FS)** | Entire body | Fashion, fitness, full body action | "full body shot, head to toe, environment visible around subject" |
| **Wide Shot (WS)** | Subject + environment | Establishing location, lifestyle, context | "wide shot showing subject in their full environment" |
| **Extreme Wide Shot (EWS)** | Subject small in landscape | Travel, adventure, scale emphasis | "extreme wide shot, subject small in the vast [landscape]" |

### Specialty Shots

| Shot Type | Description | Prompt Language |
|-----------|-------------|----------------|
| **Over-the-Shoulder (OTS)** | Camera behind one person looking at another | "over-the-shoulder shot, camera behind [person A] looking at [person B]" |
| **POV (Point of View)** | Camera = viewer's eyes | "first-person POV, camera is the viewer's eyes, hands occasionally in frame" |
| **Dutch Angle** | Camera tilted on its axis | "dutch angle, camera tilted 15 degrees, creating unease" |
| **Bird's Eye** | Directly overhead | "bird's eye view, directly overhead looking down at [subject/scene]" |
| **Worm's Eye** | Looking up from ground level | "worm's eye view, camera at ground level looking up at [subject]" |
| **Two-Shot** | Two people in frame | "two-shot, both subjects in frame at equal prominence" |
| **Insert Shot** | Close-up of object/detail | "insert shot of [product/phone screen/hand gesture]" |

---

## Camera Angles

| Angle | Effect | Prompt Language |
|-------|--------|----------------|
| **Eye Level** | Neutral, conversational, relatable | "camera at eye level, natural conversational feel" |
| **Low Angle** | Subject appears powerful, dominant | "low angle looking up at subject, conveys authority" |
| **High Angle** | Subject appears smaller, vulnerable | "high angle looking down, creates vulnerability" |
| **45-Degree Overhead** | Food photography, product flat lay | "45-degree overhead angle, product photography style" |
| **Straight Down (Top-Down)** | Flat lay, cooking, crafting | "top-down overhead view, flat lay perspective" |
| **Canted/Dutch** | Tension, unease, energy | "canted angle, 10-20 degrees off-axis, creates tension" |

---

## Camera Movements

### Primary Movements

| Movement | Description | Prompt Language | Best For |
|----------|-------------|----------------|----------|
| **Static** | Camera doesn't move | "static camera, no movement, locked tripod" | Product shots, before/after |
| **Pan** | Horizontal rotation on axis | "slow pan left-to-right, revealing [scene element]" | Reveals, establishing shots |
| **Tilt** | Vertical rotation on axis | "slow tilt up from [feet/product] to [face/full view]" | Reveals, height emphasis |
| **Dolly In** | Camera moves toward subject | "camera slowly dollies in toward subject's face" | Building intimacy, emphasis |
| **Dolly Out** | Camera moves away from subject | "camera pulls back to reveal the full [scene/environment]" | Reveals, context building |
| **Truck** | Camera moves laterally | "camera trucks right, sliding past [scene elements]" | Following action, parallax |
| **Pedestal** | Camera moves vertically | "camera rises/lowers smoothly" | Dramatic reveals |

### Dynamic Movements

| Movement | Description | Prompt Language | Best For |
|----------|-------------|----------------|----------|
| **Follow/Tracking** | Camera follows subject's movement | "camera follows subject as they [walk/move]" | Action, lifestyle, POV |
| **Orbit** | Camera circles around subject | "camera slowly orbits around subject, 180 degrees" | Product showcase, hero shots |
| **Crane Up** | Camera rises while looking down | "camera cranes up and away, revealing the full scene below" | Endings, establishing |
| **Handheld** | Slight natural shake | "handheld camera, subtle natural shake, not stabilized" | UGC, authenticity, energy |
| **Whip Pan** | Very fast pan creating motion blur | "whip pan to the right, fast enough for motion blur" | Transitions, energy |
| **Zoom** | Lens focal length changes | "slow zoom in on [subject/detail]" | Emphasis, documentary feel |
| **Push In** | Combination dolly + slight zoom | "camera pushes in on subject, increasing intensity" | Dramatic moments |

### UGC-Specific Camera Behaviors

| Behavior | Prompt Language |
|----------|----------------|
| **Selfie-arm** | "front-facing camera, arm's length (~18-24 inches), slight shake" |
| **Phone flip** | "camera flips from selfie to rear camera, brief blur transition" |
| **Natural drift** | "camera drifts slightly even when stationary, mimicking handheld" |
| **Fumbled framing** | "subject slightly off-center, occasional partial head cutoff" |
| **Auto-focus hunt** | "brief auto-focus adjustment, slight blur then sharp" |

---

## Lens Effects

### Focal Length Equivalents

| Lens | Field of View | Distortion | Best For | Prompt Language |
|------|--------------|------------|----------|----------------|
| **14-16mm (Ultra Wide)** | Very wide | Heavy barrel distortion | GoPro/action, POV adventure | "ultra-wide angle, GoPro-style barrel distortion" |
| **24mm (Wide)** | Wide | Noticeable distortion | Establishing shots, interiors | "wide 24mm, slight perspective distortion at edges" |
| **35mm (Normal Wide)** | Natural-wide | Minimal | Street photography, lifestyle | "35mm equivalent, natural perspective, minimal distortion" |
| **50mm (Normal)** | Closest to human eye | None | General, conversations | "50mm equivalent, natural human-eye perspective" |
| **85mm (Portrait)** | Narrow | Compression | Portraits, headshots, product | "85mm portrait lens, beautiful background compression and bokeh" |
| **135mm (Telephoto)** | Narrow | Heavy compression | Compressed backgrounds, intimacy | "telephoto compression, subject isolated from blurred background" |
| **Macro** | Very close | Minimal | Product detail, food, texture | "macro lens, extreme close-up of [surface/texture/detail]" |

### Depth of Field

| Setting | Effect | Prompt Language |
|---------|--------|----------------|
| **Shallow (f/1.4-2.8)** | Background heavily blurred, subject isolated | "shallow depth of field, background melts into smooth bokeh" |
| **Moderate (f/4-5.6)** | Background recognizable but soft | "moderate depth of field, background visible but soft" |
| **Deep (f/8-16)** | Everything in focus | "deep focus, everything from foreground to background sharp" |
| **Portrait mode (phone)** | Simulated bokeh with edge artifacts | "smartphone portrait mode, simulated bokeh with slight edge artifacts" |

### Optical Artifacts (for realism)

| Artifact | When to Use | Prompt Language |
|----------|-------------|----------------|
| **Lens flare** | Outdoor, sun in frame | "subtle natural lens flare from sunlight, not cinematic" |
| **Chromatic aberration** | Phone cameras, edges | "slight chromatic aberration at frame edges, phone camera artifact" |
| **Vignetting** | Phone/vintage feel | "subtle vignetting darkening at corners" |
| **Barrel distortion** | Wide angle, action cam | "barrel distortion consistent with action camera / wide angle phone lens" |
| **Rolling shutter** | Fast pans, phone camera | "slight rolling shutter wobble on fast movement" |

---

## Lighting Quick Reference

### Types

| Lighting | Effect | Prompt Language |
|----------|--------|----------------|
| **Natural daylight** | Authentic, outdoor, UGC | "natural daylight, sun at [position]" |
| **Golden hour** | Warm, flattering, aspirational | "golden hour, warm low-angle sunlight, long shadows" |
| **Overcast** | Soft, even, no harsh shadows | "overcast sky, soft diffused light, no harsh shadows" |
| **Ring light** | Even face illumination, catchlights | "ring light, even face illumination, circular catchlights in eyes" |
| **Window light** | Directional soft light, natural | "soft window light from [direction], natural shadows" |
| **Fluorescent** | Cool, institutional, unflattering | "overhead fluorescent, slight green cast, institutional feel" |
| **Mixed** | Multiple sources, realistic | "mixed lighting: window daylight + overhead warm bulb" |
| **Practical lights** | Visible light sources in scene | "practical lighting from [lamp/neon sign/screen glow]" |

### Direction Shorthand

| Direction | Effect |
|-----------|--------|
| **Front** | Flat, even, few shadows (ring light, flash) |
| **Side (Rembrandt)** | Dramatic, dimensional, triangle shadow under eye |
| **Back** | Silhouette, halo, separation from background |
| **Overhead** | Natural/institutional, under-eye shadows |
| **Under** | Dramatic, horror, unnatural (rarely used in marketing) |

---

## Audio Cues for Scene Comprehension

Even when models can't generate audio, describing sounds helps them understand what's happening in the scene.

### Dialogue Format

```
Speaker speaks [delivery style: confidently / hesitantly / excitedly]:
"[Dialogue in quotes]"
[Beat/pause description]
"[Continuation]"
```

### Ambient Sound Descriptions

| Environment | Sound Cues |
|-------------|------------|
| Street | "traffic hum, distant conversation, footsteps on concrete" |
| Kitchen | "sizzling pan, knife on cutting board, running water" |
| Office | "keyboard typing, air conditioning hum, distant phone" |
| Cafe | "espresso machine, quiet conversation, cup on saucer" |
| Outdoor nature | "birdsong, wind through leaves, distant water" |
| Gym | "weights clanking, sneakers on floor, music from speakers" |

### Sound Effect Cues

| Action | SFX Description |
|--------|----------------|
| Unboxing | "cardboard sliding, tissue paper rustle, product click" |
| Product reveal | "satisfying snap, gentle thud on surface" |
| Eating/drinking | "crunch, sip, glass set down" |
| Walking | "footsteps matching pace, surface-appropriate sound" |
| Typing | "keyboard clicks, mechanical or membrane" |

---

*Source: Cinematography patterns generalized from snubroot Veo 3.1 Meta Framework (GitHub snubroot/Veo-3-Meta-Framework). Adapted as model-agnostic reference for all AI video generation.*
