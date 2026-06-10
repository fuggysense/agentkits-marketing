# Operator actions — things only Jerel can do (M1.9)

Tick these off in any order. None block the rebuild's machine work except where marked.

- [ ] **Move the live Google key out of the synced vault** (finding E-11). `credentials/gsheets-service-account.json` holds a real RSA private key; `oauth_token.json` a live refresh token. They are git-ignored but sit in the Obsidian-synced tree. Move to macOS Keychain or an encrypted store, update the two scripts that read them (paths in `docs/audit-v2-260610/D-stakeholders.md`).
- [ ] **DCT008 composite testimonial** — your own ledger flags it pause/replace (`clients/neezanizam/output/sales-letters/firsttime-buyers/foundation-packet/claim-evidence-ledger.md:51`). Check Ads Manager: still spending on act_837789749619954?
- [ ] **Eugene M1.7 diffs** — approve in `_handoffs/eugene-m17-preview-260611.md` ("apply eugene diffs 1-4" or subset). Blocks only that task.
- [ ] **Neezanizam unsourced persona quote** — decision note landing at `_handoffs/neezanizam-quote-flag-260611.md` (M1.2 agent writing it): capture a real source for "mental burden off my shoulders", or reword + re-render affected assets.
- [ ] **Roster triage** — five skeleton client folders (1up-sales-ai, aura, fuggysmedia, propwise-sg, stackworks): onboard properly or archive? One word each is enough.
- [ ] **School/shame angles** — you flagged keep-or-kill in the original brief; the audit crawl never located them. Point me at the folder if they still exist.
- [ ] **propwise-sg canonical call** (M4.5, not urgent): root `propwise-sg/` is its own git repo; `clients/propwise-sg` is a thin symlink pointing outside the repo. Which is canonical — client or internal product?
- [ ] **Daily campaign-check cron** (M4.7): it is the only disabled cron while two money-adjacent pipelines are in flight. Re-enable, and at what cadence?

Done already: ~~Meta token rotation~~ (confirmed 260611).
