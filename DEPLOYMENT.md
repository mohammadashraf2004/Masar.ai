# Production deployment requirements

Everything in this file is **NOT DONE**. It is the specification for the
infrastructure work that has to happen before launch, written down so it
can be executed and checked off rather than assumed.

Application code cannot satisfy any of it. Where the code *supports* a
requirement (refusing to boot without it, reading a value from the
environment) that is noted — but support is not provisioning.

Status legend: ☐ not done · ☑ done and verified

---

## 1. Network topology (blocker B-2)

Required:

```
                    Internet
                        │  :443 HTTPS only
                        ▼
        ┌───────────────────────────────┐
        │  TLS reverse proxy / LB       │   terminates TLS
        │  (nginx, Caddy, Traefik,      │   redirects :80 → :443
        │   ALB, Cloud Load Balancing)  │   sets X-Forwarded-For
        └───────────────┬───────────────┘
                        │  private network
            ┌───────────┴───────────┐
            ▼                       ▼
    ┌───────────────┐       ┌───────────────┐
    │  frontend     │       │  backend      │
    │  Next.js      │──────▶│  FastAPI      │
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

Checklist:

- ☐ Valid TLS certificate, auto-renewing
- ☐ HTTP :80 redirects to HTTPS :443
- ☐ Frontend served over HTTPS
- ☐ Backend API served over HTTPS
- ☐ **Backend :8000 not reachable from the public internet** — only via
      the proxy. This is load-bearing: see §1.1.
- ☐ **PostgreSQL :5432 not publicly reachable.** `docker-compose.yml`
      already declines to publish it (only `docker-compose.override.yml`
      does, for local development), but a host firewall / security group
      must enforce it too.
- ☐ **Redis :6379 not publicly reachable.** Same — `expose:` only.
      Redis has no authentication configured; if it is ever reachable
      off-host, add `requirepass` and use `rediss://`.

No deployment provider is assumed here. The values below are what the
application needs; how you inject them (compose `.env`, Kubernetes
Secrets, SSM/Secrets Manager, Vault) is your choice.

### 1.1 Trusted proxy configuration

The API derives the rate-limit key from the client address. It ignores
`X-Forwarded-For` unless explicitly told a proxy exists, because that
header is caller-supplied and honouring it without a proxy lets one host
rotate it to defeat the login rate limit and the account lockout.

| Deployment | `TRUSTED_PROXY_COUNT` | `TRUSTED_PROXY_IPS` |
|---|---|---|
| No proxy (not acceptable for production) | `0` (default) | — |
| One proxy (nginx / ALB / Caddy) | `1` | that proxy's IP or CIDR |
| CDN in front of a load balancer | `2` | the LB's IP/CIDR |

- ☐ Set both, consistently. The app **refuses to start** in production
      with a non-zero count and no allowlist.
- ☐ The proxy must **overwrite or append to** `X-Forwarded-For`, never
      pass a client-supplied value through untouched.
- ☐ Confirm the backend port is unreachable except through the proxy —
      with `TRUSTED_PROXY_COUNT ≥ 1`, a client that can connect directly
      is a client whose address is not in the allowlist, so its header is
      ignored; but direct reachability defeats TLS regardless.

### 1.2 Origins

- ☐ `FRONTEND_URL=https://<your-domain>` — the app refuses to start in
      production with an `http://` origin. This is the **only** allowed
      CORS origin unless the next line adds more.
- ☐ `EXTRA_CORS_ORIGINS=https://staging.example.com,...` — comma
      separated, https only. Leave empty if not needed.
- ☐ `NEXT_PUBLIC_API_URL=https://api.<your-domain>/api/v1` — this is a
      **build argument**, baked into the client bundle at build time
      (see `frontend/Dockerfile`). Rebuild the image to change it.

---

## 2. Secrets (blocker B-3)

- ☐ `SECRET_KEY` — generate with `openssl rand -hex 32`. Rotating it
      invalidates every outstanding session by design.
- ☐ `POSTGRES_PASSWORD` — supplied externally, not the compose default.
- ☐ `DATABASE_URL` — points at a **least-privilege** role, not the
      superuser:

      ```sql
      CREATE ROLE app_rw LOGIN PASSWORD '<from your secret store>';
      GRANT CONNECT ON DATABASE ai_career_platform TO app_rw;
      GRANT USAGE ON SCHEMA public TO app_rw;
      GRANT SELECT, INSERT, UPDATE, DELETE
        ON ALL TABLES IN SCHEMA public TO app_rw;
      GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO app_rw;
      -- No SUPERUSER, CREATEDB, CREATEROLE. Migrations run under a
      -- separate, higher-privilege role during deploy only.
      ```
      Append `?sslmode=require`.
- ☐ `REDIS_URL` — required in production; the app refuses to start
      without it and probes reachability at boot.
- ☐ `PAYMOB_HMAC_SECRET` — without it `verify_webhook_hmac()` returns
      False and **no payment is ever confirmed**.
- ☐ `RESEND_API_KEY` — email is best-effort; unset means verification and
      password-reset mail silently does not send.

Secrets must never appear in source, Git, the Docker image, the frontend
bundle, documentation, or logs. Verified currently: no `.env` has ever
been committed on any branch; the built bundle contains no server-side
secret material; the security logger masks emails and is documented never
to receive tokens or passwords.

### 2.1 MANUAL ACTION REQUIRED — rotate the OpenAI key

> **MANUAL ACTION REQUIRED:** Rotate the existing OpenAI API key and
> provision the replacement through the production secret mechanism.

The key currently in `backend/.env` is gitignored and has never been
committed, but it has lived on a development machine and must be treated
as exposed. Revoke it in the OpenAI dashboard, issue a new one, and
inject it as `OPENAI_API_KEY`.

The application already reads it from environment/secret configuration
only (`app/core/config.py` → `Settings.OPENAI_API_KEY`); there is no
hardcoded fallback and it is never returned by any endpoint or written to
a log.

---

## 3. Database backup and restore (blocker B-5)

Nothing here is implemented in the application, and it must not be —
backups belong to the platform, not the app.

- ☐ **Automated backups.** Managed Postgres: enable automated backups +
      point-in-time recovery. Self-hosted: a scheduled `pg_dump -Fc`
      (or `pgBackRest` / `wal-g` for PITR) writing to off-host storage.
- ☐ **Retention.** Suggested: 7 daily, 4 weekly, 6 monthly. Match your
      data-retention obligations.
- ☐ **Encryption.** Encrypted at rest in the backup store, and in transit
      to it. The dump contains password hashes, email addresses and
      payment records.
- ☐ **Restricted access.** A dedicated credential with write-only access
      to the backup bucket; restore rights limited to operators. Backup
      storage must not be deletable by the application's own credentials
      (ransomware containment).
- ☐ **Recovery objectives.** Decide and record RPO/RTO. With PITR an RPO
      of minutes is achievable; with nightly dumps it is up to 24h.
- ☐ **Documented recovery procedure**, runnable by someone who did not
      write it.
- ☐ **RESTORE TEST — this is the gate condition.** Restore a real backup
      into a scratch database and verify:
      ```
      psql -d restored -c "SELECT count(*) FROM users;"
      psql -d restored -c "SELECT count(*) FROM certificates;"
      psql -d restored -c "SELECT count(*) FROM wallet_transactions;"
      alembic -c alembic.ini current      # schema at head
      ```
      Record who ran it, when, and the elapsed restore time.

**B-5 is not satisfied by a backup command existing.** It is satisfied by
a completed restore test with a recorded result.

---

## 4. Security monitoring (blocker B-4)

The application already emits structured events on a dedicated `security`
logger (`app/core/security_log.py`) to stdout, which is what container
platforms collect. **Nothing consumes them yet.** Do not change the
logging architecture — wire up a consumer.

Event format:

```
2026-09-05 02:42:45,060 WARNING security event=auth.login.locked email=f***@example.com ip=172.19.0.1 failures=8
```

Parse on `logger name == "security"` and the `event=` field.

### Recommended alerts

| Event | Condition | Severity | Why |
|---|---|---|---|
| `auth.login.locked` | > 10 distinct emails / 5 min | HIGH | Credential-stuffing campaign |
| `auth.login.failure` | > 100 / 5 min from one IP | MEDIUM | Brute force |
| `admin.action` | **any** | HIGH | Only a handful of humans should ever trigger this; every occurrence is worth an eyeball |
| `payment.webhook` `kind=hmac_rejected` | any | HIGH | Someone is forging payment confirmations |
| `authz.denied` | > 50 / 5 min from one user | MEDIUM | Authorization probing |
| `app.error` | rate > 1% of requests, or any spike | MEDIUM | Correlate `error_id` with the traceback |
| `ratelimit.exceeded` | sustained | LOW | Capacity or abuse signal |
| `auth.password.changed` / `auth.sessions.revoked` | any, on an admin account | HIGH | Account takeover indicator |

### Integration points

Pick the one matching your platform; all read stdout, so none require
application changes:

- **AWS** — CloudWatch Logs metric filters → CloudWatch Alarms → SNS
- **GCP** — Cloud Logging log-based metrics → Alerting policies
- **Azure** — Container Insights → KQL alert rules
- **Self-hosted** — Promtail → Loki → Grafana alert rules, or
  Filebeat → Elasticsearch → Kibana/ElastAlert
- **SaaS** — Datadog / Better Stack / Axiom log monitors

Checklist:

- ☐ Logs shipped off-host with retention ≥ 90 days
- ☐ The alerts above configured
- ☐ Alerts route to somebody on call
- ☐ One alert fired end-to-end as a test (trigger `auth.login.locked` by
      failing 8 logins against a test account) and confirmed received

**Do not mark B-4 done because the events exist.** They already did. It is
done when an alert has demonstrably reached a human.

---

## 5. Pre-launch verification

Run against the real production deployment, not a local stack:

```bash
curl -I http://<domain>                     # → 301/308 to https
curl -I https://<domain>                    # → 200 + HSTS header
curl -I https://api.<domain>/health         # → 200, no ai_provider field
curl -I https://api.<domain>/docs           # → 404
nmap -Pn -p 5432,6379 <public-ip>           # → filtered/closed
curl -s -D- -o /dev/null -X OPTIONS https://api.<domain>/api/v1/auth/me \
  -H 'Origin: https://evil.example' -H 'Access-Control-Request-Method: GET' \
  | grep -i access-control-allow-origin      # → absent
```

- ☐ All of the above
- ☐ Restore test completed (§3)
- ☐ Monitoring alert received end-to-end (§4)
- ☐ OpenAI key rotated (§2.1)
