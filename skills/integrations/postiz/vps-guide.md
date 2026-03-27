# Postiz VPS Maintenance Guide

> Self-hosted Postiz on Contabo VPS — SSH, Caddy, Docker, troubleshooting.

---

## Server Details

| Item | Value |
|------|-------|
| **IP** | `167.86.97.68` |
| **SSH** | `ssh -p 2222 root@167.86.97.68` (port 22 blocked by ISP) |
| **Dashboard** | https://postiz.genflos.com |
| **API** | https://postiz.genflos.com/api |
| **OS** | Ubuntu 24.04 |
| **Docker** | Compose at `/opt/postiz/docker-compose.yml` |
| **Caddy** | `/etc/caddy/Caddyfile` (auto-SSL via Let's Encrypt) |
| **Domain** | `genflos.com` (Cloudflare DNS, proxy OFF for Postiz subdomain) |

---

## Quick Commands

All commands run from `/opt/postiz/` on the VPS.

| Action | Command |
|--------|---------|
| SSH in | `ssh -p 2222 root@167.86.97.68` |
| Check status | `docker compose ps` |
| Restart Postiz | `docker compose restart postiz` |
| Restart all | `docker compose restart` |
| View logs | `docker compose logs --tail 100` |
| View Postiz logs | `docker compose logs postiz --tail 100` |
| Update Postiz | `docker compose pull postiz && docker compose up -d postiz` |
| Update all | `docker compose pull && docker compose up -d` |
| Full restart | `docker compose down && docker compose up -d` |
| Check resources | `docker stats --no-stream` |
| Caddy status | `systemctl status caddy` |
| Caddy restart | `systemctl restart caddy` |
| Caddy logs | `journalctl -u caddy --since '1 hour ago'` |
| Firewall status | `ufw status` |

---

## Services Running

| Container | Purpose | Port |
|-----------|---------|------|
| `postiz` | App (frontend + API) | 4007 → 5000 |
| `postiz-postgres` | Database (PostgreSQL 17) | 5432 (internal) |
| `postiz-redis` | Cache (Redis 7.2) | 6379 (internal) |
| `temporal` | Workflow orchestration | 7233 (internal) |
| `temporal-postgresql` | Temporal database | 5432 (internal) |
| `temporal-elasticsearch` | Temporal search | 9200 (internal) |
| `temporal-ui` | Temporal dashboard | 8080 (localhost only) |

---

## 3 Most Common Failures

### 1. Postiz Dashboard Not Loading

**Symptom:** Browser shows connection error at `https://postiz.genflos.com`

**Fix:**
```bash
ssh -p 2222 root@167.86.97.68
cd /opt/postiz
docker compose ps          # Check if containers are running
docker compose up -d       # Start if stopped
docker compose restart     # Restart if unhealthy
systemctl status caddy     # Check Caddy is running
systemctl restart caddy    # Restart Caddy if needed
```

### 2. TikTok Posts Failing to Schedule

**Symptom:** Postiz shows error when creating TikTok posts

**Fix:**
- Check TikTok integration is still connected: Settings > Integrations
- TikTok OAuth tokens expire — re-authorize if disconnected
- Confirm post format: Photo Mode requires multiple image uploads, not video URL

### 3. Media Upload Fails

**Symptom:** Image upload returns error or timeout

**Fix:**
- Check file size: max 10MB per image (JPG/PNG)
- Check disk space on VPS: `df -h`
- Restart if disk is fine: `docker compose restart postiz`

---

## TikTok OAuth Token Refresh

TikTok tokens expire periodically. When posts start failing:

1. Open https://postiz.genflos.com → Settings → Integrations
2. Find TikTok → click "Reconnect" or "Re-authorize"
3. Log in to TikTok, grant permissions
4. Test with a draft post to confirm connection works

---

## SSL Certificate

Caddy auto-renews Let's Encrypt certificates. If SSL breaks:

```bash
# Check cert status
caddy list-modules | grep tls
journalctl -u caddy --since '1 day ago' | grep -i cert

# Force renewal
systemctl restart caddy
```

---

## Monthly Maintenance Checklist (~5 min)

- [ ] `cd /opt/postiz && docker compose pull && docker compose up -d` (update to latest)
- [ ] Check disk space: `df -h`
- [ ] Check memory: `free -h` (target: <6GB used of 8GB)
- [ ] Verify all social accounts still connected (Settings > Integrations)
- [ ] Check TikTok token — try scheduling a test draft
- [ ] Review Postiz logs for errors: `docker compose logs postiz --tail 50`
- [ ] Check Caddy: `systemctl status caddy`

---

## Emergency: VPS Down

If VPS is completely down and you can't restore quickly:

1. Schedule posts manually in TikTok app (slideshows ready in `assets/tiktok/final/`)
2. Use phone to upload carousels directly to TikTok
3. Fix VPS when time permits — Postiz data persists in Docker volumes
4. Re-schedule any missed posts once Postiz is back

---

## Docker Volume Locations

Postiz stores data in Docker volumes (survives container restarts/updates):
- **Database:** `postgres-volume` (PostgreSQL)
- **Uploaded media:** `postiz-uploads`
- **Config:** `postiz-config`
- **Redis cache:** `postiz-redis-data`
- **Temporal DB:** `temporal-postgres-data`
- **Elasticsearch:** `elasticsearch-data`

**Backup:** Periodically backup `/opt/postiz/docker-compose.yml` and optionally export Docker volumes.

---

## Firewall Rules

```
22/tcp    — SSH standard
2222/tcp  — SSH alternate (used because ISP blocks 22)
80/tcp    — HTTP (Caddy auto-redirects to HTTPS)
443/tcp   — HTTPS (Caddy + Let's Encrypt)
```
