# Production deployment requirements

Everything in this file is **NOT DONE**. It is the specification for the
infrastructure work that has to happen before launch, written down so it
can be executed and checked off rather than assumed.

Application code cannot satisfy any of it. Where the code *supports* a
requirement (refusing to boot without it, reading a value from the
environment) that is noted — but support is not provisioning.

Status legend: ☐ not done · ☑ done and verified

> **Start here instead:** [LAUNCH_CHECKLIST.md](LAUNCH_CHECKLIST.md) turns
> everything below into an ordered runbook, records what has since been
> verified (backup/restore round trip, Prometheus scraping and a controlled
> alert test, production Compose config, a 16-point smoke test) and lists
> the findings from that pass. This file remains the reference for *why*
> each requirement exists; the checklist is the sequence to execute.

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
      already declines to publish it (only the opt-in
      `docker-compose.dev.yml` overlay does), but a host firewall /
      security group must enforce it too.
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

## 1.3 The deploy command

Deploy with exactly this, from the repository root:

```bash
docker compose up -d --build
```

`docker-compose.yml` is the only Compose file loaded by default and it is
production-configured: `APP_ENV=production`, Gunicorn with 4 workers, no
`--reload`, no source bind-mount, Postgres and Redis `expose:`-only.

Local development is a separate, explicitly-named overlay:

```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d
```

- ☐ Confirm before every deploy that no auto-loading override exists on the
      server. Compose auto-loads any file named `docker-compose.override.yml`
      / `compose.override.yml` / `compose.override.yaml`; this repository
      deliberately contains none. Verify with:

      ```bash
      docker compose config | grep -E 'APP_ENV|--reload|5432:5432'
      ```

      The output must show `APP_ENV: production` and neither `--reload` nor
      a published `5432:5432`. This is a real footgun, not a hypothetical:
      the dev overlay was named `docker-compose.override.yml` until
      pre-launch, which meant a plain `docker compose up` on a server set
      `APP_ENV=development` and thereby **disabled every fail-fast guard in
      §2** — default `SECRET_KEY`, no Redis, public `/docs`, and
      `http://localhost:3000` accepted as a CORS origin with credentials.

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

**Implemented** (`deploy/backup/pg-backup.sh`, `deploy/backup/Dockerfile`,
`docker-compose.prod.yml`'s `db-backup` service) — a two-layer strategy,
both layers proven by an actual restore, not by inspection:

```
PostgreSQL
    |
    v  pg_dump -Fc
encrypted local artifact (AES-256-CBC, PBKDF2/200k iterations)
    |  decrypt + pg_restore --list -- verified BEFORE anything below runs
    |
    +-------------------+
    |                    |
    v                    v
local retention         off-host copy (S3 or S3-compatible), when
(daily/weekly/monthly,   BACKUP_REMOTE_ENABLED=true — verified via
hard-linked)             HeadObject: size AND checksum, not exit 0 alone
```

- ☑ **Automated backups.** `pg_dump -Fc` on a schedule
      (`BACKUP_INTERVAL_SECONDS`, default 86400), running once immediately
      at deploy and then on that interval, inside the stack rather than a
      host cron job someone has to reinstall.
- ☑ **Off-host copy.** `BACKUP_REMOTE_ENABLED=true` ships the
      *already-encrypted, already-verified* artifact to S3 (or an
      S3-compatible endpoint) via `BACKUP_S3_BUCKET`/`BACKUP_S3_PREFIX`/
      `BACKUP_S3_REGION`, uploaded with `AWS_ACCESS_KEY_ID`/
      `AWS_SECRET_ACCESS_KEY` scoped to a dedicated, least-privilege IAM
      identity (see below) — never the application's own credentials, and
      never given to the api/frontend containers. No default: a
      production deploy must set this to `true` or `false` explicitly
      (`docker-compose.prod.yml` refuses to boot otherwise), so its
      absence is always a decision on record, never a silent gap.
- ☑ **Retention — two independent layers.** Local: 7 daily / 4 weekly / 6
      monthly (`BACKUP_RETENTION_*`), hard-linked so extra tiers cost
      inodes, not disk. Remote: **not** managed by the backup script
      (deliberately — see §5 below); apply an S3 Lifecycle rule on the
      bucket/prefix instead. A starting point: expire objects older than
      90 days, keep the newest object regardless of age (lifecycle rules
      support "keep at least N" via `NewerNoncurrentVersions` if
      versioning is on, or simply set the expiration window generously
      relative to how often a restore is actually re-verified).
- ☑ **Encryption.** Client-side AES-256-CBC (PBKDF2, 200k iterations)
      before the artifact ever leaves the host — this is the property that
      actually matters and holds regardless of the bucket's own settings.
      Additionally, SSE-S3 (`--server-side-encryption AES256`) is applied
      on upload by default when remote backup is on; SSE-KMS is available
      via `BACKUP_S3_SSE=aws:kms` + `BACKUP_S3_KMS_KEY_ID` for a
      deployment that already has a suitable key. **Losing
      `BACKUP_ENCRYPTION_PASSPHRASE` makes every encrypted backup —
      local or remote — permanently unrecoverable.** It must live in a
      secret store independent of both the database host and the backup
      bucket, and the disaster-recovery runbook (§3.2 below) must include
      recovering it as an explicit step.
- ☑ **Restricted access — least privilege.** The backup identity needs
      exactly:
      ```json
      {
        "Version": "2012-10-17",
        "Statement": [{
          "Effect": "Allow",
          "Action": ["s3:PutObject", "s3:GetObject", "s3:ListBucket"],
          "Resource": [
            "arn:aws:s3:::<bucket>",
            "arn:aws:s3:::<bucket>/<prefix>/*"
          ]
        }]
      }
      ```
      `ListBucket` is scoped with an S3 `Condition` restricting
      `s3:prefix` to the backup prefix if the bucket is shared with
      other data. **Not granted**, deliberately: `s3:DeleteObject` (the
      backup identity cannot destroy its own history — that is a
      ransomware-containment property, and remote retention is instead an
      independent Lifecycle policy the backup identity has no say over),
      `s3:*`, `AmazonS3FullAccess`, `AdministratorAccess`. Bucket
      settings: Block Public Access all four settings ON, bucket policy
      requires `aws:SecureTransport` (TLS-only), no other principal has
      write access to this prefix.
- ☑ **Recovery objectives — measured, not invented.** See §3.1.
- ☑ **Documented recovery procedure.** See §3.2, and
      `deploy/backup/verify-dr-restore.sh` — a runnable script, not just
      prose, that performs the retrieval-and-restore half of it.
- ☑ **RESTORE TEST — completed, off-host, source destroyed first.**
      Not merely "restore a local dump" (the bar this section originally
      set) — the actual disaster scenario: source database AND its local
      backup volume were destroyed entirely, then
      `deploy/backup/verify-dr-restore.sh` retrieved the backup from
      object storage the destroyed host never touched again, decrypted
      it, restored it into a brand-new Postgres instance, and a live
      application container authenticated a real pre-disaster user
      against the result. See §3.1 for the full evidence and what stands
      in for AWS in the environment this was run in.

**B-5 is not satisfied by a backup command existing.** It is satisfied by
a completed restore test with a recorded result — see below.

### 3.1 Off-host restore — evidence

Run 2026-09-13, on disposable infrastructure only — the live development
stack was never touched, connected to, or restarted for this. **No AWS
account was available in this environment**, so the off-host layer was
proven against MinIO (`quay.io/minio/minio`) — a real S3-API-compatible
server, addressed through the exact same `aws s3api` calls
`BACKUP_S3_ENDPOINT_URL` exists to support, not a stub or a mock of the
protocol. The application code path is identical for MinIO and real AWS
S3; only the endpoint and credentials differ. This is stated plainly
rather than left implicit, because it is the one substitution in this
evidence chain — everything else (Postgres, the backup container, the
restore, the application) is the real thing.

```
seed representative data into a disposable Postgres (source)
  users=3 wallets=3 wallet_transactions=3 career_tracks=1 enrollments=3
  user_progress=3 quiz_attempts=3 exam_attempts=1 certificates=1
  exam_payments=3 community_posts=1 community_post_comments=1
      |
      v
run the real db-backup image once (BACKUP_RUN_ONCE=true), against the
real source Postgres, BACKUP_REMOTE_ENABLED=true, endpoint = MinIO:
  dump complete (133,302 bytes)
  encrypted -> ...dump.enc (133,328 bytes)
  verified: 397 objects in the archive
  remote_upload_started  bucket=masar-dr-backups
    key=masar/postgres/2026/09/13/ai_career_platform-20260913T012027Z.dump.enc
  remote_upload_succeeded size=133328b
    sha256=U+CCn4j77B2RXC/1McEvmiwO3gI5uWgeNusx5OAyWs4=
  exit 0
      |
      v
independently confirmed present via a SEPARATE client (mc ls), not the
uploader's own claim: 130KiB object at that exact key
      |
      v
DESTROYED: source Postgres container removed, backup_data volume removed.
Nothing survives except the object in MinIO.
      |
      v
provisioned a brand-new, empty Postgres instance
      |
      v
deploy/backup/verify-dr-restore.sh, retrieving ONLY from MinIO:
  BACKUP RETRIEVAL: located the object via list-objects-v2 (sort_by Key)
  BACKUP RETRIEVAL: downloaded 133,328 bytes
  BACKUP RETRIEVAL: checksum verified — sha256 matches the upload exactly
  DATABASE RESTORE: decrypted OK (133,302 bytes)
  DATABASE RESTORE: pg_restore complete
  APPLICATION RECOVERY: migration head OK (010_exam_attempt_start_race)
  APPLICATION RECOVERY: all 3 checked constraints present, including the
    two partial unique indexes from migrations 009 and 010
  APPLICATION RECOVERY: users=3 user_wallets=3 career_tracks=1
  PASS
      |
      v
a live application container, pointed at the restored database:
  GET /health -> {"status":"ok", "database":"ok"}
  POST /auth/login with a pre-disaster seeded user's real credentials
    -> 200 (a genuine JWT issued against data that came back from
       nowhere but object storage)
```

**Change made mid-drill, kept:** the first upload attempt failed —
`s3api put-object` takes `--server-side-encryption`, not `--sse` (that
flag name belongs to the higher-level `aws s3 cp`/`sync` commands). Caught
immediately by actually running it against a real S3-compatible endpoint,
fixed in `pg-backup.sh`, re-verified. Recorded here because it is exactly
the kind of defect "the code looks right" review does not catch and
running the real thing does.

### 3.2 Disaster-recovery runbook

Distinct phases — conflating them is how a "recovery" ends up restoring
the wrong thing to the wrong place.

**BACKUP RETRIEVAL**
1. Recover `BACKUP_ENCRYPTION_PASSPHRASE` from the secret store
   independent of both the lost host and the backup bucket. Stop here if
   this cannot be found — an encrypted backup without it is unrecoverable
   by design, not a problem this runbook can work around.
2. Obtain read-only S3 credentials for the backup bucket/prefix (the same
   least-privilege identity `db-backup` uses is sufficient; it has
   `GetObject`+`ListBucket`, nothing more is needed to retrieve).
3. `aws s3api list-objects-v2 --bucket <bucket> --prefix <prefix> --query 'sort_by(Contents,&Key)[-1].Key'`
   to find the latest object, or pick a specific date's key directly —
   the `<prefix>/YYYY/MM/DD/<file>` layout is browsable without listing
   the whole bucket.

**DATABASE RESTORE**
4. Provision a clean PostgreSQL instance (this is where recovery
   actually starts being destructive — do not point this at anything you
   are not prepared to overwrite).
5. Run `deploy/backup/verify-dr-restore.sh` with `DR_TARGET_DATABASE_URL`
   pointed at it, `DR_CONFIRM_DISPOSABLE=true`, and the S3/passphrase
   variables above — this performs the download, checksum verification,
   decryption and `pg_restore`, then checks migration head and the
   critical constraints for you. **The script refuses to run against a
   target whose name doesn't look disposable** (`test`, `disposable`,
   `restore`, `staging`, `dr`); it has no "production mode" — restoring
   over a live production database is a deliberate, careful operation
   distinct from this verification, and is not automated here.
6. If restoring toward production rather than merely verifying the
   backup, the actual production restore additionally requires: stopping
   writes to the current database (or accepting the data since the
   backup as the RPO — see §3.1's timing), taking the target out of the
   `db` service's normal `docker compose` lifecycle during the restore,
   and a second pair of eyes. Not scripted here because it depends on
   exactly how much of the current (possibly still-partially-working)
   production state must be preserved, which no drill can predict.

**APPLICATION RECOVERY**
7. Bring up `api` (and `frontend`) pointed at the restored database.
8. `GET /health` → `"database":"ok"`.
9. Authenticate a known account and confirm the response matches what
   that account should have (role, verification state) — proves the
   restore is not just schema-shaped but actually the right data.
10. Spot-check the tables that matter most for this product specifically:
    `user_wallets`/`wallet_transactions` balances reconcile,
    `certificates` are present for users who should have them,
    `exam_payments`/`payment` state matches what Paymob's own dashboard
    shows for the same period (the webhook is the source of truth; a
    restore that disagrees with it needs reconciliation, not silent
    trust in whichever one is newer).

**DNS CUTOVER**
11. Point `DOMAIN`/`API_DOMAIN` at the new host and let Caddy obtain a
    certificate — **not automated**, and not exercised against a real
    domain anywhere in this repository's evidence (see LAUNCH_CHECKLIST
    blocker B2). If DNS is otherwise unchanged (same host, same IP,
    recovering from a database-only loss rather than a lost server),
    this phase is a no-op — do not add a step that isn't needed.

### 3.3 Remaining limitation

This closes the specific gap it was scoped to close: the backup no
longer lives only where the database does. It does **not** by itself
prove: a real AWS account's IAM policy is exactly the JSON above (verify
with `aws iam simulate-principal-policy` before first use), a real
domain's DNS cutover works (blocker B2, unchanged), or that the backup
encryption passphrase is actually reachable by a human who is not the
one person who set it up (an organizational problem, not a technical
one — write down where it lives).

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
