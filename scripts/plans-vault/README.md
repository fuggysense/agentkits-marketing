# plans-vault

Self-contained system for publishing per-client HTML plans + onboarding docs + content vaults to a custom subdomain on here.now, with version-controlled tooling and copy-paste CLI workflows.

**Live demo:** `https://plans.genflos.com` (one client per nested URL, e.g. `/michelle-koh/plan`)

---

## What this is

A repeatable foundation for distributing private HTML deliverables to clients. Each client gets a vault at `plans.<your-domain>.com/<client>/...` with arbitrary nested paths (`/plan`, `/onb`, `/content/linkedin`, etc).

Three layers:

| Layer | Where | What |
|---|---|---|
| **1. Repo (this folder)** | `scripts/plans-vault/` in Marketing repo | `sync.sh`, admin UI source, per-client template, this README |
| **2. Working dir** | `~/plans-vault/` (gitignored) | Per-client content folders + state. Edit here; sync to cloud. |
| **3. Live serve** | here.now cloud | The published copies served at `<your-domain>.com` |

---

## One-time setup (any new machine)

```bash
# Clone the Marketing repo (you've done this already)
cd /path/to/Marketing/scripts/plans-vault

# Bootstrap working dir + symlinks
./bootstrap.sh

# Follow the printed instructions to:
#  - get a here.now API key (email magic-code flow)
#  - register your custom domain (POST /api/v1/domains)
#  - add the CNAME at your DNS provider (Cloudflare, Namecheap, etc.)
#  - first-publish the admin UI + mount it at /admin
```

After bootstrap, `~/plans-vault/sync.sh` exists as a symlink to the repo, and `~/plans-vault/_state.json` is initialized.

---

## Daily workflow

### Add a new client

```bash
cd ~/plans-vault
./sync.sh --new acme-corp
# → creates ~/plans-vault/acme-corp/{index.html, plan/index.html, onb/index.html}
#   from _template/, with __CLIENT__ tokens substituted

# Replace the placeholders with real content:
cp ~/work/acme-plan-v1.html  ~/plans-vault/acme-corp/plan/index.html
cp ~/work/acme-onb-v1.html   ~/plans-vault/acme-corp/onb/index.html

# Publish
./sync.sh acme-corp
# → live at https://plans.genflos.com/acme-corp
```

### Update an existing client

```bash
# Just overwrite the files in their vault folder
cp ~/work/acme-plan-v2.html ~/plans-vault/acme-corp/plan/index.html
./sync.sh acme-corp
# → same URL, new content (here.now handles versioning under the hood)
```

### Add a per-platform content vault

```bash
mkdir -p ~/plans-vault/acme-corp/content/linkedin
cp linkedin-content-v1.html ~/plans-vault/acme-corp/content/linkedin/index.html
./sync.sh acme-corp
# → new URL: https://plans.genflos.com/acme-corp/content/linkedin
```

### Remove a client

```bash
./sync.sh --unmount acme-corp   # remove URL mapping, keep the site (recoverable)
./sync.sh --delete acme-corp    # nuke completely (URL + site)
```

### Inspect state

```bash
./sync.sh --list                # local + live mounts side by side
./sync.sh --refresh-admin       # just regenerate /admin manifest

# Or open the admin UI in browser:
open https://plans.genflos.com/admin
```

---

## Architecture details

### Why one site per client (not one per doc)

here.now's `location` API only accepts flat 30-char slugs — no slashes. So you can't directly mount `/acme-corp/plan` as one mount and `/acme-corp/onb` as another. **Instead:** mount one site per client at `/acme-corp` and use a folder structure inside the site. here.now's static server serves all the nested paths.

This gives:
- One mount per client → less administrative noise
- Arbitrary nested paths → `/acme-corp/content/linkedin/v2/` is fine
- Atomic deploys → each `./sync.sh acme-corp` is a complete snapshot

### Admin UI architecture

The admin UI at `/admin` is **manifest-driven**. `sync.sh` queries the here.now API server-side after every operation, writes the state into `_admin/manifest.json`, and re-publishes the admin site. The browser fetches the manifest (same-origin = no CORS issues) and renders state.

For any CRUD action, the admin UI **generates a copy-paste CLI command** instead of calling the here.now API directly. This is by design — here.now's API doesn't send CORS headers, so browser-side calls fail. Plus, your API key never enters the browser.

### State file

`~/plans-vault/_state.json` tracks:
- `domain` — your custom domain
- `admin_slug` — the here.now slug serving the admin UI
- `clients` — per-client metadata: `{slug, mounted_at, last_published}`

`sync.sh` reads/writes this on every operation. If you nuke `_state.json`, run `./sync.sh --refresh-admin` and it'll partly recover from the live here.now state.

### Privacy / noindex

Every HTML file synced gets `<meta name="robots" content="noindex,nofollow,nosnippet,noarchive,noimageindex">` injected if missing. Search engines won't index the URLs, and since no sitemap is published and URLs aren't linked from any public page, paths stay private.

The root site at `/` is a decoy "private docs portal" page with no listing of valid paths.

---

## File layout

```
scripts/plans-vault/                # in git
├── README.md                       # ← you're here
├── sync.sh                         # the CLI tool
├── bootstrap.sh                    # one-time setup for new machines
├── _admin/                         # admin UI source
│   ├── index.html                  # the UI
│   └── manifest.json               # regenerated by sync.sh (gitignored if you want)
└── _template/                      # per-client vault scaffold
    ├── index.html                  # __CLIENT__ token substituted
    ├── plan/index.html
    └── onb/index.html

~/plans-vault/                      # working directory, gitignored
├── sync.sh                         # → symlink to repo
├── _admin                          # → symlink to repo
├── _state.json                     # local state (your slugs)
└── <client>/                       # per-client content
    ├── index.html
    ├── plan/index.html
    ├── onb/index.html
    └── content/<platform>/index.html
```

---

## Operations cheat sheet

| Goal | Command |
|---|---|
| New client | `./sync.sh --new <slug>` then edit, then `./sync.sh <slug>` |
| Update content | edit files, `./sync.sh <slug>` |
| Add nested page | `mkdir -p <slug>/path/foo && drop index.html`, `./sync.sh <slug>` |
| Take a client offline | `./sync.sh --unmount <slug>` |
| Permanently delete | `./sync.sh --delete <slug>` |
| List state | `./sync.sh --list` |
| Refresh admin UI | `./sync.sh --refresh-admin` |
| View admin in browser | https://plans.genflos.com/admin |

---

## Cost

$0/month on here.now free tier (500 sites cap, 10 GB total, 1 custom domain). Cloudflare DNS is free. No backend, no Workers, no cron jobs.

If you outgrow the free tier:
- 500 sites cap → here.now Hobby plan
- Multiple custom domains needed → upgrade for additional custom-domain slots
- Need API-driven Cloudflare Worker proxy → re-issue your CF token with `Workers Scripts:Edit` scope

---

## Troubleshooting

**`Missing $CRED — run here.now signup first.`** → No `~/.herenow/credentials`. Get an API key from here.now and save to that file (chmod 600).

**`Missing $VAULT_HOME — run bootstrap.sh first.`** → `~/plans-vault/` doesn't exist. Run `./bootstrap.sh`.

**`Publish failed`** → check `~/.herenow/credentials` is valid; check internet; check here.now status.

**`error: 2 file(s) failed to upload` but the URLs still work** → cosmetic bug in `publish.sh` when re-publishing unchanged content. `sync.sh` already tolerates this; if you see it, you can ignore.

**Admin UI shows "manifest unavailable"** → run `./sync.sh --refresh-admin`.

**A new client's URL returns 404** → check `./sync.sh --list` matches `https://here.now/api/v1/domains/<your-domain>` mounts. Try `./sync.sh <client>` again.
