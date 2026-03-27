# Vertex AI API Reference — Direct Video & Image Generation

Direct API access to Google's Imagen, Nano Banana, and Veo models via Vertex AI / Generative Language API. Cheapest way to access these models programmatically. Use for batch work or pipeline integration — for one-off creative, OpenArt/Kling UIs are faster.

## Account & Config

```
Account: jerel@1upsalesai.com
Project ID: lexical-tide-491204-b4
Location: us-central1
GCS Bucket: gs://1up-genai-output
Free trial: $379 credits, 90 days (activated 2026-03-24)
API Key: AIzaSyDu0tC_EjXLmgDepJAsc2HxBGscG209sVo
```

### Environment Setup

```bash
export PATH="/opt/homebrew/share/google-cloud-sdk/bin:$PATH"
export PROJECT_ID="lexical-tide-491204-b4"
export LOCATION="us-central1"
```

### Auth

gcloud CLI must be authenticated. Tokens expire ~1hr.

```bash
# Check auth
gcloud auth print-access-token | head -c 20

# If expired, re-auth (opens browser)
gcloud auth login

# For ADC (needed for some endpoints)
gcloud auth application-default login
```

## Model Cheat Sheet

| Model | ID | Cost | API |
|-------|-----|------|-----|
| Imagen 4 Fast | `imagen-4.0-fast-generate-001` | $0.02/img | Vertex AI |
| Imagen 4 | `imagen-4.0-generate-001` | $0.04/img | Vertex AI |
| Imagen 4 Ultra | `imagen-4.0-ultra-generate-001` | $0.06/img | Vertex AI |
| Nano Banana 2 (Flash) | `gemini-3.1-flash-image-preview` | $0.067/img | Generative Language |
| Nano Banana Pro | `gemini-3-pro-image-preview` | $0.134/img | Generative Language |
| Veo 3.1 Fast | `veo-3.1-fast-generate-001` | $0.15/s | Vertex AI |
| Veo 3.1 Quality | `veo-3.1-generate-001` | $0.40/s | Vertex AI |

## API Call Templates

### Imagen 4 Fast (Text-to-Image)

```bash
curl -s -X POST \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  -H "Content-Type: application/json" \
  "https://${LOCATION}-aiplatform.googleapis.com/v1/projects/${PROJECT_ID}/locations/${LOCATION}/publishers/google/models/imagen-4.0-fast-generate-001:predict" \
  -d '{
    "instances": [{"prompt": "YOUR PROMPT HERE"}],
    "parameters": {
      "sampleCount": 1,
      "aspectRatio": "16:9",
      "outputOptions": {"mimeType": "image/png"}
    }
  }' > response.json

# Decode
python3 -c "
import json, base64
data = json.load(open('response.json'))
open('output.png','wb').write(base64.b64decode(data['predictions'][0]['bytesBase64Encoded']))
"
```

### Nano Banana 2 / Pro (Text-to-Image with Reference)

Uses Generative Language API with API key (NOT Vertex AI endpoint on free trial).

```bash
API_KEY="AIzaSyDu0tC_EjXLmgDepJAsc2HxBGscG209sVo"
MODEL="gemini-3.1-flash-image-preview"  # NB2 ($0.067) or gemini-3-pro-image-preview for Pro ($0.134)

# Build request with reference image
python3 -c "
import json, base64
ref_b64 = base64.b64encode(open('reference.jpg','rb').read()).decode()
request = {
    'contents': [{'parts': [
        {'inline_data': {'mime_type': 'image/jpeg', 'data': ref_b64}},
        {'text': 'YOUR PROMPT HERE'}
    ]}],
    'generationConfig': {'responseModalities': ['TEXT', 'IMAGE']}
}
json.dump(request, open('request.json','w'))
"

curl -s -X POST \
  -H "Content-Type: application/json" \
  -d @request.json \
  "https://generativelanguage.googleapis.com/v1beta/models/${MODEL}:generateContent?key=${API_KEY}" \
  > response.json

# Extract image
python3 -c "
import json, base64
data = json.load(open('response.json'))
for part in data['candidates'][0]['content']['parts']:
    if 'inlineData' in part:
        open('output.png','wb').write(base64.b64decode(part['inlineData']['data']))
        break
"
```

### Veo 3.1 — Text-to-Video

Async — submit then poll.

```bash
# Submit
curl -s -X POST \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  -H "Content-Type: application/json" \
  "https://${LOCATION}-aiplatform.googleapis.com/v1/projects/${PROJECT_ID}/locations/${LOCATION}/publishers/google/models/veo-3.1-fast-generate-001:predictLongRunning" \
  -d '{
    "instances": [{"prompt": "YOUR PROMPT"}],
    "parameters": {
      "storageUri": "gs://1up-genai-output/your-folder/",
      "sampleCount": 1,
      "durationSeconds": 8,
      "aspectRatio": "16:9",
      "resolution": "720p",
      "generateAudio": true
    }
  }' > submit.json

# Get operation name
OPERATION=$(python3 -c "import json; print(json.load(open('submit.json'))['name'])")

# Poll (repeat until done)
curl -s -X POST \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  -H "Content-Type: application/json" \
  "https://${LOCATION}-aiplatform.googleapis.com/v1/projects/${PROJECT_ID}/locations/${LOCATION}/publishers/google/models/veo-3.1-fast-generate-001:fetchPredictOperation" \
  -d "{\"operationName\": \"${OPERATION}\"}"

# Download when done
gcloud storage cp "gs://1up-genai-output/your-folder/*/sample_0.mp4" ./output.mp4
```

### Veo 3.1 — Image-to-Video (I2V)

Same as above but add `image` field to the instance:

```json
{
  "instances": [{
    "prompt": "YOUR MOTION DIRECTION",
    "image": {
      "bytesBase64Encoded": "BASE64_IMAGE_DATA",
      "mimeType": "image/jpeg"
    }
  }],
  "parameters": {
    "storageUri": "gs://1up-genai-output/folder/",
    "sampleCount": 1,
    "durationSeconds": 4,
    "aspectRatio": "9:16",
    "resolution": "720p"
  }
}
```

## Gotchas & Learnings

- **Veo durations:** Only 4, 6, or 8 seconds. Anything else errors.
- **Veo returns 0 predictions but files exist in GCS.** Always check the bucket even when predictions array is empty.
- **Veo videos stored 2 days server-side** then deleted — download promptly.
- **Safety filters:** The quality model (`veo-3.1-generate-001`) is stricter than fast. Heights, danger, falling = likely filtered. Reframe as comedic/playful to bypass. If both models filter, the IMAGE itself is the trigger — prompt changes won't help.
- **Auth tokens expire ~1hr.** Re-run `gcloud auth login` when you get reauthentication errors.
- **Nano Banana on free trial:** Must use Generative Language API with API key, NOT Vertex AI endpoint. The Vertex AI endpoint doesn't recognize Gemini image models on free trial projects.
- **First-time Veo on new project:** Service agents need provisioning. First call may fail — wait 1 min and retry.
- **HEIC images:** Convert to JPEG first with `sips -s format jpeg input.heic --out output.jpg`
- **Image orientation:** Use PIL `ImageOps.exif_transpose()` to auto-rotate before sending.
- **NB2 vs NB Pro:** NB2 (Flash) is half the cost and comparable quality for reference-based generation. Default to NB2 unless you need extra fidelity.
- **generateAudio: true** on Veo adds speech/sound but costs more ($0.15/s → higher for audio).
- **Free trial caps:** ~100 requests/day, 10 concurrent.

## When to Use This vs Platforms

| Use Case | Best Option |
|----------|-------------|
| One-off creative video | OpenArt / Kling UI |
| Batch 10+ images | Vertex API (this) |
| Automated I2V pipeline | Vertex API (this) |
| Character consistency testing | Vertex API (cheaper iterations) |
| Safety-sensitive content | Kling / Sora (less restrictive) |
