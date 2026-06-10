# GATED diff proposal — big-angle-spotter `run_pipeline.py` → `--top-n`

**File:** `~/AI workflows/big-angle-spotter/scripts/run_pipeline.py` (GLOBAL — shared by every client)
**Goal:** let the pipeline emit N top angles (5 for 10-5-5) instead of a hardcoded 3.
**Contract:** add `--top-n` (default **3**). Default run is byte-identical to today. JSON key `top_3` and the `10b_top_3.json` filename stay (ad-concept-engine reads that file) — only the COUNT relaxes.
**Status:** NOT APPLIED. Awaiting Jerel's "go". Verify after with the pipeline's own `--dry-run`.

---

### Site 1 — `TOP3_SCHEMA` constant → `topn_schema(n)` (L191-209)
```python
# BEFORE
TOP3_SCHEMA = {
    "type": "object",
    "properties": {
        "top_3": {
            "type": "array", "minItems": 3, "maxItems": 3,
            "items": {"type": "object",
                "properties": {"rank": {"type": "integer", "minimum": 1, "maximum": 3},
                               "headline": {"type": "string"}},
                "required": ["rank", "headline"]}}},
    "required": ["top_3"]}

# AFTER  (key name 'top_3' kept on purpose for downstream compat)
def topn_schema(n: int) -> dict:
    return {
        "type": "object",
        "properties": {
            "top_3": {  # key kept as 'top_3' for back-compat even when n != 3
                "type": "array", "minItems": n, "maxItems": n,
                "items": {"type": "object",
                    "properties": {"rank": {"type": "integer", "minimum": 1, "maximum": n},
                                   "headline": {"type": "string"}},
                    "required": ["rank", "headline"]}}},
        "required": ["top_3"]}
```

### Site 2 — extract block + dry-run stub + log (L688-711)
```python
# BEFORE: dry-run stub hardcodes 3 items; prompt says "top 3 (ranks 1,2,3)"; json_schema=TOP3_SCHEMA
top_3 = [ {"rank":1,...},{"rank":2,...},{"rank":3,...} ]   # dry-run
... "Extract just the top 3 (ranks 1, 2, 3) as JSON ..."
extract_data = run_worker(..., json_schema=TOP3_SCHEMA, ...)
log(f"top 3 headlines: {[h['headline'] for h in top_3]}")

# AFTER
top_3 = [ {"rank": i, "headline": f"(dry-run headline {i})"} for i in range(1, args.top_n + 1) ]
... f"Extract just the top {args.top_n} (ranks 1..{args.top_n}) as JSON ..."
extract_data = run_worker(..., json_schema=topn_schema(args.top_n), ...)
log(f"top {args.top_n} headlines: {[h['headline'] for h in top_3]}")
```

### Site 3 — fan-out concurrency cap (L718, L734)
```python
# BEFORE
with ThreadPoolExecutor(max_workers=3) as pool:          # step 11
with ThreadPoolExecutor(max_workers=3) as pool:          # step 12
# AFTER  (loops already iterate top_3, so they fan out len(top_3); just lift the cap)
with ThreadPoolExecutor(max_workers=max(3, args.top_n)) as pool:
```
Plus the two log lines "fanning out step 11/12 (3 parallel …)" → use `{args.top_n}`.

### Site 4 — STEP_11 prose (L221)
```
# BEFORE: "The other two top-3 headlines are getting their own ads."
# AFTER:  "The other top headlines are getting their own ads."   # drop the hardcoded count
```

### Site 5 — argparse + validation (L557-570)
```python
# ADD a flag (mirrors the existing --headline-count pattern):
ap.add_argument("--top-n", type=int, default=3,
    help="How many top-ranked angles/headlines to turn into ad+image prompts. Default 3 "
         "(3-2-2). Use 5 for 10-5-5. Must be <= --headline-count.")

# BEFORE
if args.headline_count < 3:
    raise SystemExit("--headline-count must be at least 3 (top-3 extraction needs >=3 headlines)")
# AFTER
if args.top_n < 1:
    raise SystemExit("--top-n must be >= 1")
if args.headline_count < args.top_n:
    raise SystemExit(f"--headline-count ({args.headline_count}) must be >= --top-n ({args.top_n})")
```

(`parse_top_3` unchanged — key stays `top_3`. `10b_top_3.json` filename unchanged.)

---

## Backward-compat proof (run after applying)
```
python3 scripts/run_pipeline.py --inputs examples/inputs.example.json --dry-run            # default top-n=3 → 3 stub headlines, 3 fan-out (identical to today)
python3 scripts/run_pipeline.py --inputs examples/inputs.example.json --dry-run --top-n 5   # 5 stub headlines, 5 fan-out
```
For 10-5-5 production: `--top-n 5` gives 5 angles + 5 ad prompts + 5 image prompts. The 2nd image variation per angle (the "×2" in 5×2) is produced downstream at image-gen / ad-concept-engine, not by this pipeline.
