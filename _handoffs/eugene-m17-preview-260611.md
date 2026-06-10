# M1.7 — Eugene content fixes, PREVIEW (nothing applied yet)

Protected client. Per Gate 1: content-only, each diff approved before applying. Three diffs proposed; the "broken pointers" at CLAUDE.md:148-160 are workspace-relative paths the validator mis-resolves (validator defect A-07, fixed in M3.2) — NOT touched here.

## Diff 1 — CLAUDE.md ~line 76 (avatars/ contradiction, finding E-01)
Current line forbids using `_brand/avatars/` for targeting ("legacy/tooling only"), but `_brand/buyer-profile.md:125` says avatars/ IS the source of truth, the avatar index confirms an active roster (avatar-1 + avatar-2), and the live wave's DCT workspaces are named after those avatars.

OLD:
> - Do not use `_brand/avatars/` as buyer targeting. Use `_brand/visual-characters/` for generated presenters, mascots, recurring faces, and face-lock references; `_brand/avatars/` is legacy/tooling only.

NEW:
> - Buyer targeting source of truth = the per-avatar files under `_brand/avatars/` (active roster: avatar-1 + avatar-2 — see `_brand/avatars/_index.md`). Use `_brand/visual-characters/` for generated presenters, mascots, recurring faces, and face-lock references.

## Diff 2 — CLAUDE.md ~line 185 ("4 micro-personas" row, finding E-02)
buyer-profile's MP1-4 were superseded 2026-06-01; active roster is 2 avatars.

OLD:
> | Buyer psychology + 4 micro-personas | `_brand/buyer-profile.md` |

NEW:
> | Buyer psychology (persona history; targeting moved to avatars/ 260601) | `_brand/buyer-profile.md` |
> | Active targeting avatars (avatar-1 + avatar-2) | `_brand/avatars/_index.md` |

## Diff 3 — campaigns/_campaigns-index.json (live wave missing from registry)
Add to `campaigns[]`:
```json
{
  "campaign_slug": "upgrader-ads",
  "campaign_name": "Upgrader Ads (10-5-5 DCT wave 1)",
  "status": "active",
  "created": "2026-06-09",
  "path": "upgrader-ads/",
  "campaign_index": null,
  "note": "No campaign-index.json yet; workspaces under dcts/. dct-001-cash-anxious PARKED, dct-002-math-blind at phase_5_upload (blocked on launch gates).",
  "primary_persona": "avatar-2",
  "deliverable": "Meta static ads -> letter page"
}
```

## Diff 4 (optional, tiny) — CLAUDE.md folder-map `videos/` row
Append "(created on demand by `/video:new`)" so the row stops pointing at a not-yet-existing folder.

**To approve:** "apply eugene diffs 1-4" (or name the subset).
