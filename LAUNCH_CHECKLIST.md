# Launch checklist

Ordered runbook for taking this platform to production. Companion to
[DEPLOYMENT.md](DEPLOYMENT.md), which is the *specification* — this is the
*sequence*, with what has actually been verified and what has not.

**Do the phases in order.** Phase 2 cannot be verified before Phase 1 is
provisioned, Phase 6 cannot run before Phase 3 deploys, and Phase 7 is
meaningless until Phase 2 exists.

Status legend: ☑ done, with evidence recorded · ☐ not done · ⚠ finding

Last verification pass: **2026-09-09**, against a full production topology
(Caddy + TLS, gunicorn ×4, Alertmanager, scheduled encrypted backups, real
Redis and Postgres 16) run locally under an isolated Compose project.

**Deploy command** (note the overlay — it is what closes :8000/:3000 and
terminates TLS):

```bash
docker compose --env-file /etc/masar/production.env \n  -f docker-compose.yml -f docker-compose.prod.yml up -d
```

---

## What is already done

These need no further action. Evidence is recorded so a reviewer can
re-run each one rather than take it on trust.

| Item | Evidence |
|---|---|
| ☑ Application test suite | 493 passed, 9 skipped — Postgres 16 + full Alembic chain to head |
| ☑ Python dependency audit | `pip-audit --strict` → no known vulnerabilities |
| ☑ Node dependency audit | `npm audit --omit=dev --audit-level=high` → 0 high/critical (⚠ 1 moderate, see F-3) |
| ☑ Production Compose is the default | `docker compose config` → `APP_ENV: production`, gunicorn `-w 4`, no `--reload`, no source bind-mount, 5432/6379 unpublished |
| ☑ Dev Compose is opt-in only | Requires `-f docker-compose.yml -f docker-compose.dev.yml`; no auto-loading override file exists in the repo |
| ☑ Production fail-fast guards | App refuses to boot on default `SECRET_KEY`, dev DSN, `http://` origin, missing `REDIS_URL`, missing `METRICS_TOKEN`, missing `RESEND_API_KEY`, proxy count without allowlist |
| ☑ Backup / restore gate (§4 below) | Real `pg_dump` → `pg_restore` into a separate instance; schema, constraints and data verified |
| ☑ Prometheus scraping + alert rules | 4/4 targets up incl. token-authenticated `api`; 9 rules loaded; controlled alert driven to `firing` and back to `inactive` |
| ☑ Secrets removed from the image | `backend/.dockerignore` added after a live key was found baked in — see F-1. Re-verified: no `.env` in image, no key readable, 0 key-pattern matches in the exported tarball |
| ☑ No secrets in Git, now or ever | `git ls-files` clean; `git log --all` shows `.env` was never committed; 0 key-shaped strings in tracked files |
| ☑ Reverse proxy + TLS topology | Caddy terminating HTTPS; :80→:443 308 redirect; certificate chain validated (`ssl_verify=0`, no `-k`) |
| ☑ :8000 / :3000 closed | Verified closed on the host under `docker-compose.prod.yml`; only :80/:443 public, Prometheus+Grafana loopback-only |
| ☑ Alert delivery | Alertmanager connected (1 active, was 0); `firing` **and** `resolved` notifications both delivered to a receiver |
| ☑ Backup automation | Scheduled, AES-256 encrypted, self-verifying, retention-pruned; restore tested from a real generated artifact |
| ☑ HTTPS smoke test | 30 checks over TLS through the proxy, 0 failures |
| ☑ Secrets presence checker | `deploy/verify-secrets.sh` — reports presence only, never a value |

---

## Phase 1 — Secrets provisioning

Nothing else can be verified until these exist. Provision them through
your platform's secret mechanism (Compose `.env` on the host, Kubernetes
Secrets, SSM/Secrets Manager, Vault) — **never** in Git, the image, or a
Dockerfile.

**Every value below is required in production. The app refuses to boot
without the ones marked (fail-fast).**

- ☐ **`SECRET_KEY`** (fail-fast) — `openssl rand -hex 32`. Must be ≥32 chars
      with real entropy. Rotating it invalidates every live session by design.
- ☐ **`POSTGRES_PASSWORD`** — supplied externally, never the compose default.
      **See F-4: this does not change the password on an existing volume.**
- ☐ **`DATABASE_URL`** (fail-fast) — least-privilege role, not the superuser,
      with `?sslmode=require` appended. SQL for the role is in
      [DEPLOYMENT.md §2](DEPLOYMENT.md).
- ☐ **`REDIS_URL`** (fail-fast) — the app probes reachability at boot and
      refuses to start if it fails. If Redis is reachable off-host at all,
      set `requirepass` and use `rediss://`.
- ☐ **`METRICS_TOKEN`** (fail-fast, when `METRICS_ENABLED=true`) —
      `openssl rand -hex 16`. Without it `/metrics` would be public.
- ☐ **`RESEND_API_KEY`** (fail-fast) — newly load-bearing. Billable features
      now require a verified email address and the mail client fails *soft*;
      without a provider every account would be permanently unable to spend.
- ☐ **`OPENAI_API_KEY`** — **ROTATION IS MANDATORY, SEE F-1.** The existing
      key must be treated as compromised: it was baked into built images.
      Revoke it in the OpenAI dashboard, issue a replacement, and provision
      the new one only through the secret store.
- ☐ **`PAYMOB_API_KEY`**, **`PAYMOB_INTEGRATION_ID_CARD`**,
      **`PAYMOB_INTEGRATION_ID_WALLET`**, **`PAYMOB_IFRAME_ID`**
- ☐ **`PAYMOB_HMAC_SECRET`** — without it `verify_webhook_hmac()` returns
      False and **no payment is ever confirmed**. Silent revenue loss.
- ☐ **`FRONTEND_URL`** (fail-fast) — `https://<your-domain>`. Must be https.
- ☐ **`NEXT_PUBLIC_API_URL`** — `https://api.<your-domain>/api/v1`. This is a
      **build argument**, baked into the client bundle. Changing it requires
      an image rebuild, not a restart.
- ☐ **`EXTRA_CORS_ORIGINS`** — only if you serve additional origins.
- ☐ **`GRAFANA_PASSWORD`** — Grafana ships with `admin`/`admin`.
- ☐ **`TRUSTED_PROXY_COUNT`** / **`TRUSTED_PROXY_IPS`** — see Phase 2.
      Setting the count without the allowlist is a fail-fast error.

**Verify nothing leaked:**

```bash
git ls-files | grep -E '\.env$|\.env\.local$'      # must be empty
docker run --rm --entrypoint sh <your-api-image> -c 'ls -a /app | grep -c "^\.env$"'   # must be 0
```

---

## Phase 2 — Network topology and TLS

```
                    Internet
                        │  :443 HTTPS only
                        ▼
        ┌───────────────────────────────┐
        │  TLS reverse proxy / LB       │  terminates TLS
        │  (nginx, Caddy, Traefik,      │  redirects :80 → :443
        │   ALB, Cloud Load Balancing)  │  sets X-Forwarded-For
        └───────────────┬───────────────┘
                        │  private network
            ┌───────────┴───────────┐
            ▼                       ▼
    ┌───────────────┐       ┌───────────────┐
    │  frontend     │──────▶│  backend      │
    │  :3000        │       │  :8000        │
    └───────────────┘       └───────┬───────┘
                                    │  private network
                        ┌───────────┴───────────┐
                        ▼                       ▼
                ┌───────────────┐       ┌───────────────┐
                │  PostgreSQL   │       │  Redis        │
                │  :5432        │       │  :6379        │
                └───────────────┘       └───────────────┘
```

### 2.1 Exposure matrix

| Component | Port | Public? | How it is enforced |
|---|---|---|---|
| Reverse proxy | 443 | **YES** — the only public entry point | Security group allows 443 |
| Reverse proxy | 80 | **YES**, redirect only | 301/308 → https |
| Frontend | 3000 | **NO** | `docker-compose.prod.yml` removes the publish (`ports: !reset []`) ☑ verified closed; firewall still required |
| Backend API | 8000 | **NO** | Same ☑ verified closed; firewall still required |
| PostgreSQL | 5432 | **NO** | `expose:` only — never bound to a host interface ☑ verified |
| Redis | 6379 | **NO** | `expose:` only — never bound to a host interface ☑ verified |
| postgres-exporter | 9187 | **NO** | `expose:` only ☑ verified |
| redis-exporter | 9121 | **NO** | `expose:` only ☑ verified |
| Prometheus | 9090 | **NO** | Bound to `127.0.0.1` ☑ verified |
| Grafana | 3001 | **NO** | Bound to `127.0.0.1` |

> ☑ **Resolved in the Compose layer.** `docker-compose.prod.yml` removes the
> `ports` publish for `api` and `frontend`, so only Caddy is bound to a public
> interface. Verified on a running stack: :8000, :3000, :5432, :6379, :9187
> and :9121 all closed on the host; :80 and :443 open; Prometheus :9090 and
> Grafana :3001 loopback-only.
>
> ⚠ **A firewall is still required.** Docker writes its own iptables rules and
> a future compose edit could republish a port. The security group is the
> control that does not depend on getting a YAML file right — see F-9 for how
> nearly this went wrong.

### 2.2 Checklist

- ☐ **Valid TLS certificate, auto-renewing** — `deploy/Caddyfile` obtains and
      renews Let's Encrypt certificates automatically; nothing to schedule.
      **Requires a real domain + DNS pointing at the host.** Verified locally
      with Caddy's internal CA (real TLS, real chain validation, no domain).
- ☑ HTTP :80 redirects to HTTPS :443 — 308, verified
- ☑ Frontend served over HTTPS — verified (307 to its landing route)
- ☑ Backend API served over HTTPS — verified, `/health` 200 through the proxy
- ☐ **Security group / firewall: inbound 443 (and 80 for redirect) only.**
      Requires host/cloud access — not doable from the repository.
- ☑ Backend :8000 not published — verified closed on the host
- ☑ Frontend :3000 not published — verified closed on the host
- ☑ PostgreSQL :5432 not published — verified closed
- ☑ Redis :6379 not published — verified closed
- ☑ Exporters :9187 / :9121 not published — verified closed
- ☑ Prometheus :9090 / Grafana :3001 loopback-only — verified

### 2.3 Trusted proxy configuration

The API derives its rate-limit key from the client address and **ignores**
`X-Forwarded-For` unless told a proxy exists — that header is caller-supplied,
and honouring it without a proxy lets one host rotate it to defeat both the
login rate limit and the per-account lockout.

| Deployment | `TRUSTED_PROXY_COUNT` | `TRUSTED_PROXY_IPS` |
|---|---|---|
| One proxy (nginx / ALB / Caddy) | `1` | that proxy's IP or CIDR |
| CDN in front of a load balancer | `2` | the LB's IP/CIDR |

- ☐ Set both, consistently. Too **high** is the dangerous direction — it
      reads further left, into attacker-controlled entries.
- ☐ The proxy must overwrite or append to `X-Forwarded-For`, never pass a
      client-supplied value through untouched.

---

## Phase 3 — Deploy

- ☐ Check every secret is present first (never prints a value):

      ```bash
      ./deploy/verify-secrets.sh /etc/masar/production.env
      ```

- ☐ Confirm no auto-loading Compose override exists on the server:

      ```bash
      ls docker-compose.override.yml compose.override.yml 2>/dev/null   # must be empty
      docker compose config | grep -E 'APP_ENV|--reload|5432:5432'
      ```

      Must print `APP_ENV: production`, and neither `--reload` nor a
      published `5432:5432`.

- ☐ Deploy with exactly:

      ```bash
      docker compose --env-file /etc/masar/production.env         -f docker-compose.yml -f docker-compose.prod.yml up -d --build
      ```

      The `-f docker-compose.prod.yml` overlay is **not optional**: it is what
      adds Caddy/TLS, removes the public :8000 and :3000 publishes, and starts
      Alertmanager and the backup job. `docker compose up -d` alone gives a
      production-configured app with no proxy and two open ports.

- ☐ Run migrations:

      ```bash
      docker compose exec api alembic upgrade head
      docker compose exec api alembic current    # → 008_exam_payment_ref_squatting (head)
      ```

- ☐ Confirm the app booted (the fail-fast guards passing *is* the config
      verification):

      ```bash
      docker compose logs api | grep -i "Refusing to start"   # must be empty
      docker compose ps                                        # api healthy
      ```

- ☐ Seed the catalogue if this is a first deploy (`backend/seed*.py`).

---

## Phase 4 — Database backup and restore

**Status: the restore *procedure* is proven; the *production schedule* is
not yet configured.**

### 4.1 What was actually verified — 2026-09-09 ☑

A full round trip was executed against disposable Postgres 16 instances:

```
backup created
  pg_dump -Fc, 131,376 bytes, sha256 2d7723bc22e4f48d…
        ↓
restore performed
  pg_restore into a SEPARATE, empty instance
  0 tables before → 37 tables after, exit 0, no errors
        ↓
migration / schema verified
  alembic_version = 008_exam_payment_ref_squatting (head)
  all 4 exam_payments indexes present, including the partial unique index
  predicate preserved verbatim:
    CREATE UNIQUE INDEX uq_exam_payments_confirmed_ref
      ON public.exam_payments USING btree (payment_ref)
      WHERE ((status)::text = 'confirmed'::text)
  constraint still ENFORCES: duplicate confirmed payment_ref rejected
        ↓
representative application data verified
  users 3/3 · user_wallets 3/3 · wallet_transactions 3/3
  exam_payments 1/1 · career_tracks 1/1 · exams 1/1 · certificates 0/0
  balances, roles and is_verified flags identical row by row
  confirmed exam payment (FAWRY-RESTORETEST-001, 150 EGP) intact
  application read the restored DB successfully; content fingerprint
  sha256 1af3707a… matched the source exactly
```

This proves the dump format, the schema (including a partial index that a
naive restore can silently drop) and the data all survive. It does **not**
prove your production backup *schedule* works — that is below.

### 4.2 Automation — implemented and verified ☑

`deploy/backup/pg-backup.sh`, run as the `db-backup` service in
`docker-compose.prod.yml`. It ships with the stack rather than being a host
cron job someone has to reinstall on every new server.

Each cycle: `pg_dump -Fc` → AES-256-CBC encrypt (`-pbkdf2 -iter 200000`) →
**verify by decrypting and listing the archive** → prune by retention →
write a heartbeat plus a Prometheus textfile metric.

| Requirement | Status | Evidence |
|---|---|---|
| Runs automatically | ☑ | `BACKUP_INTERVAL_SECONDS`, default 86400; runs once immediately at start |
| `pg_dump -Fc` format | ☑ | Same format the restore procedure was verified against |
| Encrypted at rest | ☑ | Artifact begins `Salted__`, unreadable without the passphrase |
| Self-verifying | ☑ | "verified: 395 objects in the archive"; a wrong passphrase makes `pg_restore` exit non-zero — tested |
| Retention | ☑ | daily/weekly/monthly tiers, `BACKUP_RETENTION_*`, hard-linked so tiers cost inodes not disk |
| Failure is observable | ☑ | Failure logs `ERROR`, leaves `last_success` stale, and refuses to keep a bad artifact; `DatabaseBackupStale` alert rule added |
| Not in the repo / build context | ☑ | Named volume `backup_data`, never a bind mount into the source tree |
| **Off-host storage** | ☐ | **NOT DONE — requires cloud credentials.** See below. |

**Restore test from a real generated backup — 2026-09-09 ☑**

```
backup created
  db-backup produced ai_career_platform-20260909T010801Z.dump.enc
  131,456 bytes, AES-256 encrypted, self-verified (395 objects)
        ↓
restore performed
  artifact copied off the container, decrypted, pg_restore'd into a
  SEPARATE disposable Postgres 16 instance (0 tables before -> 37 after)
        ↓
migration / schema verified
  alembic_version = 008_exam_payment_ref_squatting (head)
  all 4 exam_payments indexes present including the partial unique index
  constraint still ENFORCES: duplicate confirmed payment_ref rejected
        ↓
representative application data verified
  users=3 wallets=3 wallet_transactions=3, values intact
  the APPLICATION read the restored database successfully (3 user+wallet rows)
```

**Still required — needs credentials this environment does not have:**

- ☐ **Off-host replication.** `backup_data` lives on the same host as the
      database, so it survives a dropped table but not a lost server.
      Add a sidecar or host cron that pushes `/backups` to object storage:

      ```bash
      restic -r s3:s3.amazonaws.com/<bucket> backup /backups
      # or: rclone sync /backups remote:bucket/masar-backups
      ```

      Requires cloud credentials — see the boundaries section.
- ☐ **Write-only credential** for the backup destination; restore rights
      limited to named operators; the app's own credentials must not be able
      to delete backups (ransomware containment).
- ☐ **Store `BACKUP_ENCRYPTION_PASSPHRASE` somewhere reachable when the
      database and the server are gone.** A backup you cannot decrypt is not
      a backup.
- ☐ **RPO/RTO decided and recorded.**
- ☐ **Point node_exporter's textfile collector at `/backups`** so
      `DatabaseBackupStale` has data to evaluate.
- ☐ **Re-run the restore test against a real production backup** once
      off-host storage exists, and record who ran it, when, and how long it
      took.

---

## Phase 5 — Monitoring

**Status: collection and alert evaluation are proven; delivery to a human
is not configured.**

### 5.1 What was actually verified — 2026-09-09 ☑

- ☑ **Prometheus is scraping.** 4/4 targets `up`: `api` (via bearer token),
      `postgres`, `redis`, `prometheus`.
- ☑ **`/metrics` is gated.** No token → 404, wrong token → 404, correct
      token → 200. (404 not 401, deliberately — an unauthenticated caller
      should not learn the endpoint exists.)
- ☑ **Metrics populate from real traffic.** `http_requests_total`,
      `auth_events_total`, `credits_spent_total` all recorded during the
      smoke test.
- ☑ **All 9 alert rules loaded**, all `inactive` against a healthy stack —
      i.e. no rule fires on a normal Tuesday.
- ☑ **Controlled alert test executed end to end.** `redis-exporter` stopped
      at 21:47:05Z:

      ```
      t+15s  ServiceDown  inactive
      t+30s  ServiceDown  pending   (job=redis)
      t+90s  ServiceDown  firing    severity=critical
                          summary: "redis is not being scraped"
      exporter restarted → ServiceDown returned to inactive, 4/4 targets up
      ```

### 5.2 Alert delivery — implemented and verified ☑

The gap was: **0 Alertmanagers**. A firing alert reached the Prometheus web
UI and nobody else. Now wired:

* `monitoring/prometheus/prometheus.yml` — `alerting:` block targeting
  `alertmanager:9093`
* `docker-compose.prod.yml` — the `alertmanager` service (not published;
  reachable only over the Compose network)
* `deploy/alertmanager.yml` — routing, grouping, inhibition, and a webhook
  receiver whose URL is substituted from `$ALERT_RECEIVER_URL` at start, so
  the URL (itself a credential) is never committed

**Controlled end-to-end test — 2026-09-09 ☑**

`redis-exporter` stopped (safe, self-recovering — no production data touched):

```
1. trigger                redis-exporter stopped 00:58:05Z
2. Prometheus detects     t+30s  ServiceDown -> pending
3. becomes firing         t+90s  ServiceDown -> firing (severity=critical, job=redis)
4. Alertmanager receives  1 alert held, status=active, receiver=default
5. RECEIVER NOTIFIED      00:59:33Z  status=firing  alertname=ServiceDown
                                     severity=critical job=redis
                                     summary="redis is not being scraped"
6. recover                redis-exporter restarted -> 4/4 targets up
7. resolves               01:04:32Z  status=resolved delivered to the receiver
                          (5 min later = the configured group_interval)
```

Both halves of the lifecycle were delivered, not just the firing half.

- ☑ Alertmanager deployed and connected (1 active, was 0)
- ☑ Alert rules loaded — now 10 (added `DatabaseBackupStale`)
- ☑ A receiver actually received `firing`
- ☑ A receiver actually received `resolved`
- ☑ Inhibition configured so a down target does not page three times

**Still required — needs a channel credential:**

- ☐ **Set `ALERT_RECEIVER_URL` to the team's real Slack/Discord webhook**
      (or switch to the `email_configs` block in `deploy/alertmanager.yml`).
      The chain was proven against a local sink; the last hop — a person
      seeing it in a channel — cannot be tested without that URL, and a sink
      that always returns 200 cannot tell you Slack would have rejected it.
- ☐ **Re-run the controlled test with the real receiver** and confirm a human
      received it. Stopping `redis-exporter` for two minutes is the cheapest
      safe trigger.
- ☐ **Decide who is on call.**
- ☐ **Ship logs off-host**, retention ≥ 90 days. The app emits structured
      events on a dedicated `security` logger to stdout — **nothing consumes
      them yet.** Parse on `logger name == "security"` and the `event=` field.
      Alert table and per-platform integrations: [DEPLOYMENT.md §4](DEPLOYMENT.md).
- ☐ **Change the Grafana admin password** (`GRAFANA_PASSWORD`).

> Prometheus running is not monitoring. Monitoring is done when an alert has
> demonstrably reached a person — step 5 above, but to a real channel.

---

## Phase 6 — Post-deploy smoke test

Executed **over HTTPS through the reverse proxy**, with full certificate
validation (`--cacert`, never `-k`). 30 checks, 0 failures — 2026-09-09.

No real customer data. No real Paymob transaction: the webhook was exercised
with a synthetic transaction object signed with the deployment's own
`PAYMOB_HMAC_SECRET`, which is what proves our signature verification and
credit-release path without touching the provider.

| # | Check | Result |
|---|---|---|
| 1 | HTTP :80 → HTTPS redirect | ☑ 308 |
| 2 | TLS certificate validates | ☑ `ssl_verify=0` |
| 3 | `/health` through the proxy | ☑ 200 |
| 4 | `/health` leaks no provider info | ☑ no `ai_provider` field |
| 5 | `/docs`, `/redoc`, `/openapi.json` not public | ☑ 404 ×3 |
| 6 | `/metrics` not public | ☑ 404 |
| 7 | Frontend serves over HTTPS | ☑ 307 |
| 8 | Frontend CSP + HSTS present, `x-powered-by` absent | ☑ |
| 9 | Frontend CSP `connect-src` allows the API origin | ☑ |
| 10 | Registration over HTTPS | ☑ 201, token returned |
| 11 | New account starts unverified | ☑ `is_verified:false` |
| 12 | Login | ☑ 200 |
| 13 | `/auth/me` with / without token | ☑ 200 / 401 |
| 14 | Resend verification | ☑ 200, token row created |
| 15 | **Unverified user blocked from billable action** | ☑ 403 `email_verification_required` |
| 16 | **Verified user passes the gate** | ☑ not 403 (provider call then 500 — no `OPENAI_API_KEY`, rotation pending) |
| 17 | Wallet readable | ☑ 200 |
| 18 | Wallet deduction recorded | ☑ ledger: `bonus +10`, `deduction −2 mentor_chat`, `topup +300` |
| 19 | Paymob webhook, valid HMAC | ☑ 200, top-up confirmed, credits released |
| 20 | Paymob **replay** | ☑ 200 `no matching pending transaction` — no second payout |
| 21 | Paymob invalid HMAC | ☑ 401 |
| 22 | Track enrollment — **available** track | ☑ 201 |
| 23 | Track enrollment — **unavailable** track | ☑ 403 blocked |

**Not verifiable here:**

- ☐ **A real verification email arriving.** `RESEND_API_KEY` was a placeholder
      in this run; the send failed soft exactly as designed. Needs the real
      key and a mailbox.
- ☐ **A completed AI action.** Item 16 proves the *gate* opens; the provider
      call then fails because there is no key. Once the rotated key is
      provisioned, item 16 must return 200.
- ☐ **Re-run all 23 against the real production domain** over public DNS.

---

## Phase 7 — External security verification

Run these **from outside** the deployment, against the public domain.

```bash
curl -I http://<domain>                     # → 301/308 to https
curl -I https://<domain>                    # → 200 + Strict-Transport-Security
curl -I https://api.<domain>/health         # → 200, no ai_provider field
curl -I https://api.<domain>/docs           # → 404
curl -I https://api.<domain>/openapi.json   # → 404
curl -I https://api.<domain>/metrics        # → 404 without a token

nmap -Pn -p 5432,6379,8000,3000,9090,9187,9121 <public-ip>   # → filtered/closed

curl -s -D- -o /dev/null -X OPTIONS https://api.<domain>/api/v1/auth/me \
  -H 'Origin: https://evil.example' -H 'Access-Control-Request-Method: GET' \
  | grep -i access-control-allow-origin      # → absent
```

- ☐ All of the above
- ☐ `pip-audit --strict` — ☑ clean as of 2026-09-09, re-run at deploy
- ☐ `npm audit --omit=dev` — ☑ 0 high/critical as of 2026-09-09 (⚠ 1 moderate, F-3)

**Already verified locally on a production-configured stack ☑:**
`/docs`, `/redoc`, `/openapi.json` all 404 · `/metrics` 404 without a valid
token · Postgres and Redis unreachable from the host · all API security
headers present (CSP `default-src 'none'`, `X-Content-Type-Options`,
`X-Frame-Options: DENY`, `Referrer-Policy`, `Permissions-Policy`,
`Cache-Control: no-store`, COOP/CORP, **HSTS**) · frontend headers present
with `x-powered-by` absent.

---

## Findings from the verification pass

### F-1 ⚠ **FIXED** — live secrets were baked into the Docker image

`backend/` had no `.dockerignore`, so the Dockerfile's `COPY . .` copied the
developer's `backend/.env` into the image: a **live `OPENAI_API_KEY`**, plus
`SECRET_KEY` and `DATABASE_URL`.

Not merely disclosed — **in use**. `docker-compose.yml` passes
`OPENAI_API_KEY` as a bare passthrough (deliberately, so an unset host
variable doesn't shadow local dev config), so an unset variable in production
fell through to the baked value. A smoke test against a production-configured
stack with **no** `OPENAI_API_KEY` on the host returned a real model
completion — billed to the developer's personal key. That is how this was
found.

It also contradicted the project's own rule (DEPLOYMENT.md §2: *"Secrets must
never appear in source, Git, the Docker image, …"*), which had previously been
recorded as satisfied.

**Fixed:** `backend/.dockerignore` added (build config only — no application
code touched). Verified after rebuild: no `.env` in the image, no key
readable from settings, 0 matches for an API-key pattern in the exported
image tarball, and the app still boots, migrates and serves.

**Still required:** ⚠ **rotate the OpenAI key.** It must be treated as
compromised — it existed in image layers, not just on a dev machine. Revoke,
reissue, and provision only via the secret store.

### F-2 ⚠ `POST /mentor/chat` charges for failed requests

Every other billable handler (roadmap, code review, project hint, challenge
hint, answer evaluation) deducts credits, calls the provider inside a
`try`, and refunds on failure. `/mentor/chat` deducts at
`mentor_controller.py:50` and calls the provider with no refund path.

Observed directly: a provider failure returned 500 and left the ledger at
`deduction −2 mentor_chat` with no reversing entry — the student paid 2
credits for nothing.

**Not changed** — mentor functionality is explicitly out of scope, and the
fix alters billing behaviour. Recorded for a product decision.

### F-3 ⚠ One moderate npm advisory

`baseline-browser-mapping` (`>=2.0.0 <2.11.0`), GHSA-w5vr-8v7q-w6rv — DoS on
invalid input. A **build-time** transitive dependency of the Next.js
toolchain; not shipped to the browser and not on the runtime path. Below the
`--audit-level=high` CI gate, which is why CI is green. `fixAvailable: true`.

- ☐ Optional pre-launch: refresh the lockfile entry and rebuild.

### F-4 ⚠ Deployment trap — `POSTGRES_PASSWORD` on an existing volume

Postgres applies `POSTGRES_USER`/`POSTGRES_PASSWORD` **only when
initialising an empty data directory.** Setting them on a host where the
stack has already run leaves the old credentials in place. Encountered
during this pass: the API could not authenticate (`role "appuser" does not
exist`) while the volume still held the original `postgres` role.

Consequences to avoid: an operator follows Phase 1, sets a strong password,
and either the app cannot connect — or worse, the database is still running
on the default `password` while everyone believes it was changed.

- ☐ On a **first** deploy: set `POSTGRES_PASSWORD` *before* the first `up`.
- ☐ On an **existing** volume: change it inside the database —
      `ALTER ROLE <user> WITH PASSWORD '<new>';` — and update the secret to
      match. Do not assume the env var did it.
- ☐ Confirm afterwards: `docker compose logs api | grep -i "authentication failed"` is empty and `/health` reports `"database":"ok"`.

*(Note: `/health` correctly returned 503 and withheld the database error text
throughout this failure — the fail-safe behaved exactly as designed.)*

### F-6 ⚠ **FIXED** — Compose `ports: []` does not close a port

Closing the public :8000/:3000 publishes looked like a one-line override.
It is not. Compose **merges** the `ports` list across files, so an override
of `ports: []` leaves the inherited publish in place. Verified against
Compose v5.0.2:

```
base 8000:8000 + override `ports: []`        -> STILL PUBLISHED
base 8000:8000 + override `ports: !reset []` -> removed
```

`docker-compose.prod.yml` uses `!reset`. Had it used the obvious `[]`, the
overlay would have reported success while leaving the API bound to
`0.0.0.0` — a security control that silently does nothing. This is the
strongest argument for the firewall in Phase 2 being mandatory rather than
belt-and-braces: it does not depend on getting a YAML merge rule right.

### F-7 ⚠ **FIXED** — Caddy refused to start with an empty `ACME_EMAIL`

`email {$ACME_EMAIL}` with the variable set-but-empty expands to a bare
`email` directive and Caddy exits with *"wrong argument count ... for
'email'"* — taking down the only public entry point, in a crash loop.

Caddy's own `{$VAR:default}` only substitutes when a variable is **unset**,
not when it is empty, so the default has to be applied at the Compose layer
too (`${ACME_EMAIL:-...}`, with `:-` not `-`). Both layers now carry one.

### F-8 ⚠ **FIXED** — two bugs in the backup job, both caught by running it

1. `postgres:16-alpine` ships libssl but **not the `openssl` CLI**, so every
   backup failed at the encryption step (`sh: openssl: not found`). Switched
   to `postgres:16` (Debian), which has both `pg_dump` and `openssl`.
2. `pg_restore --list -` does **not** mean stdin — pg_restore takes `-`
   literally and fails with *"could not open input file"*. With no filename
   it reads stdin correctly.

Worth noting what worked: on both failures the script logged an error,
deleted the unusable artifact rather than keeping it, and left
`last_success` stale. A backup job that fails loudly is the whole point —
these would otherwise have been discovered during a restore.

### F-9 ⓘ Backups are not yet off-host

`backup_data` is a named volume on the same host as the database. It
protects against a dropped table, a bad migration or a corrupted row. It
does **not** protect against losing the server. Off-host replication needs
cloud credentials and is listed in Phase 4.2.

### F-5 ⓘ `Server: uvicorn` header is not suppressed

`http_security.py` intends to replace the server banner
(`if "server" in headers: headers["server"] = "api"`), but uvicorn writes
that header at the transport layer *after* middleware runs, so the rewrite
never applies. Confirmed: production responses carry `server: uvicorn`.

Low severity — it discloses the server software, not a version. **Not
changed** (application code is frozen); the natural fix is at the reverse
proxy you are deploying anyway.

- ☐ Strip or overwrite `Server` at the proxy (nginx: `proxy_hide_header Server;`).

---

## Go / no-go gate

### VERDICT: **NO-GO**

Three blockers remain, all of which need credentials or access that the
repository cannot supply.

**Done — evidence in the phases above**

- ☑ Application: 493 tests green, `pip-audit` clean, `npm audit` 0 high/critical
- ☑ Production Compose posture verified (`APP_ENV=production`, gunicorn ×4,
      no `--reload`, no source bind-mount)
- ☑ Secrets removed from images; nothing secret in Git, now or in history
- ☑ TLS terminating, :80→:443 redirect, chain validated
- ☑ :8000, :3000, :5432, :6379 and both exporters closed on the host
- ☑ Backups scheduled, encrypted, self-verifying, retention-pruned, and
      restore-tested from a real artifact
- ☑ Alertmanager connected; firing **and** resolved notifications delivered
- ☑ 30-check HTTPS smoke test, 0 failures

**Blocking — cannot be closed from here**

- ☐ **B1 · Rotate the OpenAI key.** Only the account owner can. The old key
      was in image layers and must be treated as compromised. Until the
      replacement is provisioned, no AI feature works (verified: the gate
      opens, the provider call 500s).
- ☐ **B2 · Real domain, DNS and firewall.** Caddy's automatic Let's Encrypt
      needs a domain resolving to the host. The security group closing
      everything except :443/:80 needs cloud or host access.
- ☐ **B3 · A real alert channel + off-host backup storage.** Needs the team's
      Slack/Discord webhook (or SMTP), and object-storage credentials.

**Also outstanding, non-blocking:** real verification email tested end to
end, Grafana password set, security logs shipped off-host, RPO/RTO recorded.

---

## Post-launch product decisions

Recorded, not implemented. Each needs explicit product direction.

1. **Should `/tracks/projects/{id}/submit` and `/challenges/{slug}/submit`
   consume credits?** Both call an LLM. Neither is metered by the wallet
   today — project submission is unmetered outright; challenge submission is
   covered by the enrolment fee. Both are protected by a rate limit and the
   email-verification gate, so this is a pricing question, not a security one.

2. **Is `exam_grading = 10` in `CREDIT_COSTS` planned or stale?** The price is
   defined and exposed through `GET /wallet/costs`, but nothing charges it —
   the exam controller makes no LLM call. Either a feature not yet wired up,
   or a leftover that should be removed so the price list stops advertising
   something that does not exist.

3. **F-2: should `/mentor/chat` refund on provider failure?** Every sibling
   endpoint does.
