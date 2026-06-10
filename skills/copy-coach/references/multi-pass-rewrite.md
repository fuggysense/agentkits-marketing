# Multi-pass rewrite — versioned, one focused change per pass

Load this reference when the user wants a structured multi-pass rewrite with audit trail on disk.

Most copy help is inline — single-line critiques, section rewrites, finding a Big Idea, mapping its expansion. That's the everyday work.

For a **full multi-pass structured rewrite** — tearing down and rebuilding a sales page across numbered versions with audit trail on disk — run the iteration discipline below.

## Triggers

- User says *"rewrite this in passes,"* *"iterate on this landing page,"* *"v2 this copy,"* *"tear it down and rebuild it"*
- User hands you source copy + an edit brief and wants structured revision
- More than 2–3 structural changes are needed, each deserving its own pass
- The user wants version files on disk for audit trail

## V4 path convention

Multi-pass rewrites live under the client folder so they're discoverable by downstream `/copy` runs and Phase B/C reviewers:

```
clients/<slug>/copy-system/rewrites/<page>/
├── <page>-copy.txt              # v1, source
├── <page>-edit-brief.md         # 5–7 named principles
├── <page>-rewrite-v2.md         # one focused change
├── <page>-rewrite-v3.md
├── ...
└── <page>-rewrite-v<final>.md   # fresh-eyes pass
```

## Prereqs

Two files on disk before passes begin:

1. **Source copy** — `<page>-copy.txt`. The current version, verbatim. If the source is a live URL, scrape via `dev-browser` first and save.
2. **Edit brief** — `<page>-edit-brief.md`. A self-contained document of 5–7 named, project-specific principles that localize the substance of `references/big-idea.md` + `references/stylizing.md` to this page's audience, voice, and register. The brief is the spine of the iteration; without it you are polishing without direction.

If the edit brief is missing, generate it first. Diagnose the source copy against the substance above. Surface 5–7 named principles. Save to disk. **Hold for user read before starting passes** — the principles become the pass queue.

## Plan the pass queue

Translate the brief's principles into a numbered queue of focused single-change passes — one principle ≈ one pass. Order structural changes before line-level ones (don't unchop fragments inside paragraphs about to be cut). Surface the planned queue to the user:

> Proposed passes:
> v2 — [pass name from brief]
> v3 — [pass name from brief]
> v4 — [pass name from brief]
> …
> v\<final\> — fresh-eyes reflection pass
>
> Proceed?

Wait for confirmation.

## Per pass

Each pass produces one file: `<page>-rewrite-v<N>.md`. Each pass is a **full re-draft, not a patch** — copy lives or dies whole; partial edits accumulate weird seams.

After each pass, deliver:

- The full rewritten copy
- **What changed from v\<N-1\>** — specific changes, each grounded in a named principle from the brief or the substance in `references/big-idea.md` / `references/stylizing.md`
- **Principles applied** — which sections of copy-coach this pass enforces
- **Flags / risks** — anything that touches a previously-locked element (headline, case study, CTA)

## One focused change per pass

Resist the urge to fix three things while you're in there. The audit trail is the point — if v6 introduces a regression, you want to know which pass to back out. Mixing changes kills that.

## Hold between passes

The user reads each pass. Don't auto-advance. They nudge direction; the queue advances. If they accept v\<N\>, run v\<N+1\>. If they reject, revert (v\<N-1\> is still on disk).

## The final pass is the fresh-eyes pass

Use the verbatim PART 16 prompt from `references/cold-reader-pass.md`. Re-anchor to principles, not to previous passes. Default to delete, not polish. Be willing to cut sections you wrote in earlier passes.

**If the fresh-eyes pass surfaces nothing to cut or change — you didn't actually run it.** Go back. Re-load the prompt. The pass that finds nothing to cut is the pass that wasn't run.

## After v\<final\>

Hand off to `eval-halbert` + `eval-sales-letter` for a cold independent verdict, run via the `Agent` tool with fresh context. The multi-pass discipline gives you a clean rewrite; the eval agents tell you whether the rewrite holds.
