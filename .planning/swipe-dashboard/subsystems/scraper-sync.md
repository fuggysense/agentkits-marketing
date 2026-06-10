# Subsystem — `scripts/ghost-sync.py`

Bridges the SQLite canonical DB (`swipe-files/<industry>/ads-db.sqlite`) into the Ghost Postgres mirror. Called as the final step of `/ads:scrape-library` (or `/ads:scrape-advertiser`).

## Contract

### Input
- `<industry>` positional arg (e.g. `property-sg`)
- `--reembed-all` flag: force re-embedding every ad under the active provider (use when swapping providers)
- Env vars:
  - `GHOST_DATABASE_URL` — Postgres connection string from `ghost create`
  - `NETLIFY_BLOBS_TOKEN` — for asset uploads
  - `EMBEDDING_PROVIDER` — `openai` | `ollama` | `jina` | `qwen3` | `cohere` | `huggingface`
  - `EMBEDDING_MODEL` — provider-specific (e.g. `ollama/nomic-embed-text`, `text-embedding-3-small`, `jina-embeddings-v3`, `Qwen/Qwen3-Embedding-0.6B`)
  - `EMBEDDING_API_BASE` — optional (e.g. `http://localhost:11434` for Ollama)
  - `EMBEDDING_TARGET_DIM` = `1024` (Matryoshka target; see `subsystems/embedding-provider.md`)
  - `OPENAI_API_KEY` / `JINA_API_KEY` / etc. — only if that provider is active

### Output
- Upserts into `industries`, `pages`, `ads`, `transcripts`, `classifications`, `ad_embeddings`
- Appends to `scrape_runs`, `embedding_provider_log` (if provider flipped)
- Updates `_agent_readme` content with fresh stats snapshot + active provider
- Idempotent — safe to re-run without side effects (hashed input check prevents unnecessary re-embeds)

## Pseudocode

```python
import os, sqlite3, psycopg2, hashlib, litellm
from pathlib import Path

INDUSTRY = sys.argv[1]
REEMBED_ALL = '--reembed-all' in sys.argv

# ——— Load config
GHOST_URL = os.environ['GHOST_DATABASE_URL']
PROVIDER = os.environ.get('EMBEDDING_PROVIDER', 'ollama')
MODEL = os.environ.get('EMBEDDING_MODEL', 'ollama/nomic-embed-text')
API_BASE = os.environ.get('EMBEDDING_API_BASE')  # None for hosted APIs
TARGET_DIM = int(os.environ.get('EMBEDDING_TARGET_DIM', 1024))
ACTIVE_PROVIDER_ID = f"{PROVIDER}:{MODEL}"

pg = psycopg2.connect(GHOST_URL)
sq = sqlite3.connect(f"swipe-files/{INDUSTRY}/ads-db.sqlite")

# ——— Industry
stage_md = Path(f"swipe-files/{INDUSTRY}/stage-analysis.md").read_text()
stage_meta = parse_frontmatter(stage_md)  # schwartz_stage, confidence, etc.
pg.execute("""
  INSERT INTO industries (slug, name, emoji, schwartz_stage, stage_confidence, stage_analysis_md)
  VALUES (%s, %s, %s, %s, %s, %s)
  ON CONFLICT (slug) DO UPDATE SET
    name=EXCLUDED.name,
    schwartz_stage=EXCLUDED.schwartz_stage,
    stage_confidence=EXCLUDED.stage_confidence,
    stage_analysis_md=EXCLUDED.stage_analysis_md
""", (INDUSTRY, stage_meta['name'], stage_meta['emoji'],
      stage_meta['stage'], stage_meta['confidence'], stage_md))

# ——— Pages
for page in sq.execute("SELECT * FROM pages"):
    pg.execute("""
      INSERT INTO pages (page_id, industry_slug, name, url, profile_pic_url, category, verified, meta, last_scraped_at)
      VALUES (%s, %s, %s, %s, %s, %s, %s, %s, now())
      ON CONFLICT (page_id) DO UPDATE SET
        name=EXCLUDED.name,
        profile_pic_url=EXCLUDED.profile_pic_url,
        category=EXCLUDED.category,
        verified=EXCLUDED.verified,
        meta=EXCLUDED.meta,
        last_scraped_at=now()
    """, (...))

# ——— Temporal reconciliation: detect newly-stopped ads
previously_active = {r[0] for r in pg.execute(
    "SELECT ad_archive_id FROM ads WHERE industry_slug=%s AND status='ACTIVE'",
    (INDUSTRY,)
)}
currently_seen_active = {
    r['ad_archive_id'] for r in sq.execute(
        "SELECT ad_archive_id FROM ads WHERE status='ACTIVE'"
    )
}
newly_stopped = previously_active - currently_seen_active

# ——— Ads (upsert)
for ad in sq.execute("SELECT * FROM ads"):
    # Upload asset to Netlify Blobs if not already
    asset_url = upload_if_new(ad['local_asset_path'])
    pg.execute("""
      INSERT INTO ads (ad_archive_id, industry_slug, page_id, format, platforms,
                       headline, body_text, cta_text, asset_url, asset_type,
                       status, start_date, first_seen_date, last_seen_active_date,
                       regions, raw, days_running)
      VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
              %s, %s,
              LEAST(COALESCE((SELECT first_seen_date FROM ads WHERE ad_archive_id=%s), CURRENT_DATE), CURRENT_DATE),
              CASE WHEN %s='ACTIVE' THEN CURRENT_DATE ELSE (SELECT last_seen_active_date FROM ads WHERE ad_archive_id=%s) END,
              %s, %s, %s)
      ON CONFLICT (ad_archive_id) DO UPDATE SET
        status=EXCLUDED.status,
        last_seen_active_date=CASE WHEN EXCLUDED.status='ACTIVE' THEN CURRENT_DATE ELSE ads.last_seen_active_date END,
        raw=EXCLUDED.raw,
        asset_url=COALESCE(ads.asset_url, EXCLUDED.asset_url),  -- don't overwrite good URL with NULL
        days_running=EXCLUDED.days_running
    """, (...))

# ——— Mark newly-stopped ads
if newly_stopped:
    pg.execute("""
      UPDATE ads
      SET status='INACTIVE', stopped_date=CURRENT_DATE
      WHERE ad_archive_id = ANY(%s)
        AND stopped_date IS NULL
    """, (list(newly_stopped),))

# ——— Transcripts + classifications
for t in read_transcripts(f"swipe-files/{INDUSTRY}/"):
    pg.execute("INSERT INTO transcripts (...) ON CONFLICT (ad_archive_id) DO UPDATE SET ...")
for c in read_classifications(f"swipe-files/{INDUSTRY}/"):
    pg.execute("INSERT INTO classifications (...) ON CONFLICT (ad_archive_id) DO UPDATE SET ...")

# ——— Embeddings (via LiteLLM)
scraped_ids = [r['ad_archive_id'] for r in sq.execute("SELECT ad_archive_id FROM ads")]

for ad_id in scraped_ids:
    ad = pg.execute("SELECT headline, body_text FROM ads WHERE ad_archive_id=%s", (ad_id,)).fetchone()
    transcript = pg.execute("SELECT text FROM transcripts WHERE ad_archive_id=%s", (ad_id,)).fetchone()
    input_text = f"{ad['headline'] or ''}\n{ad['body_text'] or ''}\n{transcript['text'] if transcript else ''}".strip()
    input_hash = hashlib.sha256(input_text.encode()).hexdigest()

    # Skip if hash matches existing row for active provider (unless --reembed-all)
    if not REEMBED_ALL:
        existing = pg.execute("""
          SELECT input_hash FROM ad_embeddings
          WHERE ad_archive_id=%s AND provider=%s
        """, (ad_id, ACTIVE_PROVIDER_ID)).fetchone()
        if existing and existing['input_hash'] == input_hash:
            continue

    # Call LiteLLM
    resp = litellm.embedding(
        model=MODEL,
        input=[input_text],
        api_base=API_BASE,
    )
    raw_vec = resp['data'][0]['embedding']

    # Matryoshka truncation (if native > target) or zero-pad (if native < target)
    if len(raw_vec) >= TARGET_DIM:
        truncated = raw_vec[:TARGET_DIM]
    else:
        truncated = raw_vec + [0.0] * (TARGET_DIM - len(raw_vec))  # rare; log a warning

    # Upsert
    pg.execute("""
      INSERT INTO ad_embeddings (ad_archive_id, provider, model_version, dim, embedding, native_dim, input_hash, is_active)
      VALUES (%s, %s, %s, %s, %s, %s, %s, true)
      ON CONFLICT (ad_archive_id, provider) DO UPDATE SET
        embedding=EXCLUDED.embedding,
        native_dim=EXCLUDED.native_dim,
        input_hash=EXCLUDED.input_hash,
        is_active=true,
        model_version=EXCLUDED.model_version,
        created_at=now()
    """, (ad_id, ACTIVE_PROVIDER_ID, MODEL, TARGET_DIM, truncated, len(raw_vec), input_hash))

# ——— Deactivate non-active providers for scraped ads (so v_active_embeddings stays clean)
pg.execute("""
  UPDATE ad_embeddings
  SET is_active=false
  WHERE provider != %s
    AND ad_archive_id = ANY(%s)
""", (ACTIVE_PROVIDER_ID, scraped_ids))

# ——— Log scrape run
pg.execute("""
  INSERT INTO scrape_runs (industry_slug, finished_at, pages_scraped, ads_found, ads_new, status)
  VALUES (%s, now(), %s, %s, %s, 'success')
""", (INDUSTRY, len(pages), len(scraped_ids), len(newly_seen)))

# ——— Update _agent_readme snapshot
readme = build_agent_readme(pg, ACTIVE_PROVIDER_ID)  # reads current counts + active provider
pg.execute("""
  INSERT INTO _agent_readme (id, content, updated_at)
  VALUES (1, %s, now())
  ON CONFLICT (id) DO UPDATE SET content=EXCLUDED.content, updated_at=now()
""", (readme,))

pg.commit()
```

## Idempotency guarantees
1. **Upserts everywhere** — no duplicate rows on re-run
2. **Input-hash skip** — re-embed only when `headline+body+transcript` changed (or `--reembed-all`)
3. **`stopped_date` protected** — never overwritten once set (only `UPDATE ... WHERE stopped_date IS NULL`)
4. **Asset URLs protected** — `COALESCE(ads.asset_url, EXCLUDED.asset_url)` so a missing new URL doesn't blank an existing good one
5. **Provider flipping** — old provider rows get `is_active=false` but stay; no data loss

## Integration with `/ads:scrape-library`
Append to the skill's final phase:
```bash
python scripts/ghost-sync.py "$INDUSTRY"
echo "Ghost sync complete. Dashboard will pick up new ads on next request."
```

Optional `--no-sync` flag on the parent command bypasses this (for debugging / air-gapped runs).

## Failure modes + handling
- **Ghost unreachable:** fail fast, don't partial-write. SQLite remains authoritative.
- **LiteLLM provider error:** log to `scrape_runs.error_text`, continue with rest of pipeline, retry embeddings on next scrape.
- **Netlify Blobs upload fail:** store `asset_url = NULL` for that ad; dashboard shows a placeholder; next sync retries the upload.
- **Schema drift:** Phase 1 pinned the schema; any new generated-column or table needs a migration script in `scripts/migrations/`. `ghost-sync.py` refuses to run if schema version mismatch.
