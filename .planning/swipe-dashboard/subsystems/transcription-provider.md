# Subsystem — Transcription Provider Abstraction

Goal: match the embedding-provider pattern. Make the transcription engine a single env-var flip. Default: Groq whisper-large-v3 (fast + cheap). Fallback: faster-whisper local (offline + free).

## Why swap-ability matters
- Current `transcribe` skill uses faster-whisper locally — good but slow on CPU (hours for 1000 ads)
- Groq's whisper-large-v3 API gives ~165x realtime at ~$0.04/hr audio — effectively free at ad-scraping volume
- New transcription providers emerge constantly (OpenAI whisper-1, Deepgram Nova-3, AssemblyAI, Azure Speech, Replicate models). Locking to one is short-sighted.
- LiteLLM supports `litellm.transcription(model=..., file=...)` across OpenAI, Groq, Azure, Anthropic (when they ship it), and local endpoints

## Design: same three-layer pattern as embeddings

### Layer 1 — LiteLLM for provider uniformity
```python
import litellm
with open(audio_path, "rb") as f:
    resp = litellm.transcription(
        model=TRANSCRIPTION_MODEL,
        file=f,
        api_base=TRANSCRIPTION_API_BASE,  # None for hosted, http://localhost:8000 for local
    )
text = resp.text
```

### Layer 2 — Provider identifier in the stored file sidecar
Prepend a provider-tag comment at the top of each transcript file so we know which engine produced it:

```
# provider: groq:whisper-large-v3
# native_duration: 47.2s
# transcribed_at: 2026-04-20T09:42:13Z

[full transcript text here]
```

### Layer 3 — Ghost `transcripts` table gets a provider column
Add to the schema in `schema/tables.md`:
```sql
ALTER TABLE transcripts ADD COLUMN provider TEXT;           -- 'groq:whisper-large-v3', 'faster-whisper:large-v3'
ALTER TABLE transcripts ADD COLUMN audio_hash TEXT;         -- sha256 of audio bytes, skip re-transcribe if matches
ALTER TABLE transcripts ADD COLUMN confidence NUMERIC;      -- avg Whisper logprob if available
```
Queries can filter by provider; A/B testing between providers works the same way as embeddings.

## Env vars
```bash
export TRANSCRIPTION_PROVIDER=groq
export TRANSCRIPTION_MODEL=groq/whisper-large-v3
export GROQ_API_KEY=...

# Alternative: local
export TRANSCRIPTION_PROVIDER=faster-whisper
export TRANSCRIPTION_MODEL=large-v3
# no API key needed

# Alternative: OpenAI
export TRANSCRIPTION_PROVIDER=openai
export TRANSCRIPTION_MODEL=whisper-1
export OPENAI_API_KEY=...
```

## Provider comparison (for ad-scraping workload)

| Provider | Model | Cost | Speed (30s clip) | Accuracy | Offline? |
|---|---|---|---|---|---|
| **Groq** (default) | whisper-large-v3 | $0.04/hr audio | ~0.3s | Excellent | No |
| **Groq** | whisper-large-v3-turbo | $0.02/hr audio | ~0.2s | Very good | No |
| **OpenAI** | whisper-1 | $0.36/hr audio | ~5s | Excellent | No |
| **faster-whisper** local CPU | large-v3 | Free | ~30-60s | Excellent | Yes |
| **faster-whisper** local GPU | large-v3 | Free | ~2-3s | Excellent | Yes |
| **Deepgram** Nova-3 | n/a | $0.43/hr audio | ~1s | Excellent | No |
| **AssemblyAI** | nano | $0.25/hr audio | ~3s | Good | No |

Winner for our use case: **Groq whisper-large-v3 default, faster-whisper fallback.**

## Groq setup
```bash
# Sign up at https://console.groq.com, grab API key
export GROQ_API_KEY=gsk_...

# Test with one ad
python3 -c "
import litellm
with open('test.mp4', 'rb') as f:
    r = litellm.transcription(model='groq/whisper-large-v3', file=f, api_key='$GROQ_API_KEY')
    print(r.text)
"
```

## Integration with existing `transcribe` skill
The `transcribe` skill at `skills/transcribe/` currently uses `yt-dlp + faster-whisper`. Extend it to:

1. Accept a `--provider` flag (`groq` | `faster-whisper` | `openai`)
2. Read `TRANSCRIPTION_PROVIDER` env var as fallback when flag absent
3. Route to the matching engine via LiteLLM
4. Write provider + audio_hash to the sidecar file header

No breaking change — existing `transcribe <url>` invocations still work (default provider).

## Integration with ad-library-scraper Phase 3
`scripts/ad_library/enrich_scraped_ads.py` currently calls:
```python
transcript = transcribe_skill.transcribe(video_path)
```

Change to:
```python
transcript = transcribe_skill.transcribe(
    video_path,
    provider=os.environ.get('TRANSCRIPTION_PROVIDER', 'groq'),
    model=os.environ.get('TRANSCRIPTION_MODEL', 'groq/whisper-large-v3'),
)
```

Effect on current workflow:
- `/ads:scrape-library property-sg` runs as usual
- Phase 3 encounters a winner video → downloads to `assets/<ad_id>.mp4`
- Calls `transcribe` with Groq by default → ~0.3s per clip instead of 30-60s
- Writes sidecar with provider tag → `ghost-sync.py` picks it up and stores provider in `transcripts.provider`

## Integration with ghost-sync.py
Update the sync script (see `subsystems/scraper-sync.md`) to parse the sidecar header and store provider + audio_hash:
```python
text, provider, audio_hash = parse_transcript_sidecar(path)
pg.execute("""
  INSERT INTO transcripts (ad_archive_id, text, provider, audio_hash, duration_sec)
  VALUES (%s, %s, %s, %s, %s)
  ON CONFLICT (ad_archive_id) DO UPDATE SET
    text=EXCLUDED.text,
    provider=EXCLUDED.provider,
    audio_hash=EXCLUDED.audio_hash
  WHERE transcripts.audio_hash IS DISTINCT FROM EXCLUDED.audio_hash
""", (ad_id, text, provider, audio_hash, duration))
```
The `WHERE audio_hash DISTINCT FROM` guards against re-inserting identical content (idempotency + skip re-transcribe if audio unchanged).

## A/B testing providers
Same pattern as embedding A/B:
1. Pick 20 transcripts done with faster-whisper
2. Re-transcribe with Groq, store under `provider='groq:whisper-large-v3'`
3. Diff: `SELECT t1.text, t2.text FROM transcripts t1 JOIN transcripts t2 USING (ad_archive_id) WHERE t1.provider LIKE 'faster%' AND t2.provider LIKE 'groq%'`
4. Eyeball: are they equivalent? Groq should match or exceed faster-whisper (same underlying model).

## Failure modes
- **Groq rate limit:** LiteLLM auto-retries with backoff; if exhausted, fall through to faster-whisper for that clip
- **GROQ_API_KEY missing:** skill warns + falls back to faster-whisper
- **Corrupted audio:** both providers fail similarly; log to `scrape_runs.error_text`, continue rest of pipeline, retry next scrape
- **Network unavailable:** force fallback to faster-whisper (local)

## Default recommendation
Use **Groq whisper-large-v3** as default. Reasons:
1. Effectively free at ad-scraping volume (~$0.30/mo even at 1000 ads/mo)
2. 100-500x faster than local CPU — scales when you add more industries
3. Same model quality (Whisper large-v3 is Whisper large-v3 everywhere)
4. Frees up local compute for other skills that actually need it
5. Fits user's stated preference (raised this in the conversation thread)

Fallback to **faster-whisper local** when:
- Working offline
- Sensitive content you don't want sent to a third-party API
- Groq rate limits hit (rare for ad volumes)
- Testing a specific faster-whisper model variant (distil-whisper, etc.)

## Cost projection
Scenario: 1 industry, 10 advertisers, weekly scrape. Avg 6 winners per advertiser have videos needing transcript. Avg 30s per video.
- Ads needing transcription per week: 60 × 30s = 1800s = 30 min = 0.5 hr
- Groq cost per week: 0.5 × $0.04 = **$0.02**
- Annualized: ~$1/year

Scenario: 10 industries, 50 advertisers each, weekly deep-backfill + weekly shallow refresh. Avg 50 winners × 30s.
- Ads/week: 10 × 50 × 50 × 30s = 750,000s = 208 hr
- Groq cost per week: 208 × $0.04 = **$8.33**
- Annualized: ~$434/year — still trivial vs. manual transcription time saved

Conclusion: cost is never a reason to NOT use Groq for this.
