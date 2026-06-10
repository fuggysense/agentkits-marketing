# Subsystem — Embedding Provider Abstraction

Goal: make the embedding model a single env-var flip. Today: Ollama + nomic-embed-text. Tomorrow: Jina v3, Qwen3-Embedding, OpenAI text-embedding-3-large, whatever wins 2027.

## Design: three layers

### Layer 1 — LiteLLM as the provider-uniform interface
[LiteLLM](https://docs.litellm.ai/docs/embedding/supported_embedding) translates between Python and 15+ embedding providers with identical call signatures:
```python
litellm.embedding(model=MODEL, input=[text], api_base=API_BASE)
```
Supported (relevant to us):
- OpenAI: `text-embedding-3-small` (1536), `text-embedding-3-large` (3072)
- Ollama: `ollama/nomic-embed-text` (768), `ollama/mxbai-embed-large` (1024), `ollama/qwen3-embedding` (1024)
- Jina: `jina-embeddings-v3` (1024)
- Cohere: `embed-english-v3.0` (1024)
- HuggingFace: any model in Inference API or local via sentence-transformers
- Voyage, Together, Bedrock — all available if we ever need them

### Layer 2 — Matryoshka truncation to 1024 dims
Modern embedding models are trained with Matryoshka Representation Learning — the first N components of the vector are a valid standalone embedding. Truncating `v[:1024]` from any native-dim output preserves ~95-98% quality at retrieval.

| Native dim | Action |
|---|---|
| 1024 (Jina v3, Qwen3, Cohere v3, mxbai) | Use as-is |
| 768 (Nomic) | Zero-pad to 1024 (log warning, rare case) |
| 1536 (OpenAI v3-small) | Truncate to first 1024 |
| 3072 (OpenAI v3-large) | Truncate to first 1024 |
| 4096 (Qwen3-Embedding 8B) | Truncate to first 1024 |

Post-truncation L2-normalize for cosine-similarity stability (optional but recommended; LiteLLM's responses from OpenAI are pre-normalized, Ollama's are not).

### Layer 3 — Decoupled `ad_embeddings` table with `(ad_archive_id, provider)` primary key
One ad can have multiple provider rows. Only one is `is_active=true`. Swaps preserve history for A/B testing + rollback.

See `schema/tables.md` for DDL. Summary:
```sql
CREATE TABLE ad_embeddings (
  ad_archive_id TEXT REFERENCES ads(ad_archive_id) ON DELETE CASCADE,
  provider TEXT NOT NULL,             -- e.g. 'ollama:ollama/nomic-embed-text'
  model_version TEXT,
  dim INT NOT NULL DEFAULT 1024,
  embedding vector(1024) NOT NULL,
  native_dim INT,
  input_hash TEXT,                    -- sha256 of input text, for skip-if-unchanged
  is_active BOOLEAN DEFAULT true,
  PRIMARY KEY (ad_archive_id, provider)
);
```

## Provider swap workflow
1. Set env vars:
   ```bash
   export EMBEDDING_PROVIDER=jina
   export EMBEDDING_MODEL=jina-embeddings-v3
   export JINA_API_KEY=...
   ```
2. Run:
   ```bash
   python scripts/ghost-sync.py property-sg --reembed-all
   ```
3. Behind the scenes:
   - For every ad: `litellm.embedding(model='jina-embeddings-v3', input=[text])` → 1024 dim vector
   - Upsert into `ad_embeddings` with `provider='jina:jina-embeddings-v3'`, `is_active=true`
   - `UPDATE ad_embeddings SET is_active=false WHERE provider != 'jina:jina-embeddings-v3' AND ad_archive_id = ANY(scraped)`
   - Log a row in `embedding_provider_log` with `deactivated_at` for the prior provider and a new row with the new provider

4. `v_active_embeddings` view now routes all semantic queries to Jina automatically.
5. Dashboard and agents need **zero code changes** — they already query through the view.

## Rollback
```sql
-- Revert to previous provider (e.g. Ollama)
UPDATE ad_embeddings SET is_active = (provider = 'ollama:ollama/nomic-embed-text');
INSERT INTO embedding_provider_log (provider, model_version, activated_at, notes)
VALUES ('ollama:ollama/nomic-embed-text', 'ollama/nomic-embed-text', now(), 'rollback from jina');
UPDATE embedding_provider_log SET deactivated_at = now()
WHERE provider = 'jina:jina-embeddings-v3' AND deactivated_at IS NULL;
```

## A/B testing two providers on the same dataset
Because `ad_embeddings` is keyed on `(ad, provider)`:
1. Run sync once with provider A (`is_active=true`)
2. Flip provider B, run with `--reembed-all` (also `is_active=true` for B, A becomes inactive)
3. Temporarily set BOTH active for a side-by-side query:
   ```sql
   UPDATE ad_embeddings SET is_active=true
   WHERE provider IN ('ollama:...', 'jina:...');
   ```
4. Query each by explicit provider filter:
   ```sql
   SELECT * FROM ad_embeddings WHERE provider = 'jina:...' AND ad_archive_id = $1;
   ```
5. Compare retrieval quality with a scoring rubric

## Semantic search recipe (provider-agnostic)
```sql
WITH seed AS (
  SELECT embedding FROM v_active_embeddings WHERE ad_archive_id = $1
)
SELECT a.headline,
       a.body_text,
       e.embedding <=> seed.embedding AS distance,
       e.provider AS embedding_provider
FROM ads a
JOIN v_active_embeddings e USING (ad_archive_id), seed
ORDER BY distance
LIMIT 5;
```

## Default provider rationale
Starting with **Ollama + nomic-embed-text** because:
- Free, local, no API bills
- Fits user's explicit "100% inside Ghost's hard-cap pricing" requirement
- 768 dims → zero-pad to 1024, no truncation loss
- Good enough quality for semantic search over ad copy (~50-100 tokens each)
- If quality feels off later, swap is one env var + one sync

## When to swap providers (signals)
- **Quality signal:** semantic search returning irrelevant matches → try Jina v3 (strong multilingual, handles ad copy well) or OpenAI text-embedding-3-small (best-in-class English)
- **Scale signal:** > 50k ads → consider Qwen3-Embedding 0.6B (fast, local, competitive with OpenAI on MTEB)
- **Cost signal:** OpenAI bill > $20/mo → swap back to Ollama for free
- **Language signal:** multi-language industries (e.g. `property-jp`, `property-tw`) → Jina v3 or Qwen3

## Ollama setup checklist (first-time)
```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull the embedding model
ollama pull nomic-embed-text

# Verify
ollama list  # should show nomic-embed-text

# Ollama server runs on localhost:11434 by default; set:
export EMBEDDING_API_BASE=http://localhost:11434
```
