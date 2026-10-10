# AI Mentor release (migration 037): deploy, verify, roll back

For the operator deploying the AI Mentor hardening release on the production host (an SSM
session on the instance). Steps marked **CHANGE** modify production; everything else only
reads. Stop at the first failed expectation and use [Rollback](#8-rollback): do not patch
production by hand. Background: `docs/release-2026-10-masar-launch.md`, section "AI Mentor
hardening (migration 037)".

## 0. Shell setup

```sh
cd <the checkout docker compose runs from>
alias dc='docker compose --env-file /etc/masar/production.env -f docker-compose.yml -f docker-compose.prod.yml'
psqlq() { dc exec -T db sh -c 'psql -X -U "$POSTGRES_USER" -d "$POSTGRES_DB" "$@"' psql "$@"; }
PREV=$(git rev-parse --short HEAD)      # the release running now, for rollback
```

## 1. Preflight (read-only): do not deploy onto an unhealthy host

```sh
git log -1 --format='%h %s'; git status --short | head
docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Image}}'
docker stats --no-stream
df -h /; free -h; uptime
docker inspect -f '{{.Name}} restarts={{.RestartCount}} oom={{.State.OOMKilled}} started={{.State.StartedAt}}' $(docker ps -q)
sudo dmesg -T | grep -i -E 'out of memory|oom-kill|killed process' | tail -5
dc logs --since 24h api 2>&1 | grep -c 'WORKER TIMEOUT'
curl -fsS https://api.masarai.net/health; echo
psqlq -c "select version_num from alembic_version"
psqlq -c "select pg_size_pretty(pg_database_size(current_database())) as db_size, (select count(*) from pg_stat_activity) as connections"
```

Expect `036_pro_ai_usage`. If it is `035_subscription_refunds` or older, stop: the Pro/Kashier
release steps were not completed. Also stop if a container is restarting or unhealthy, an OOM
kill appears since the last deploy, `WORKER TIMEOUT` appears in the last hour, the root disk has
less than 4 GB free (the image build needs it), or less than 1 GB of memory is available.

## 2. Backup (**CHANGE**: writes one backup file)

```sh
dc restart db-backup                    # the backup service runs one full cycle when it starts
sleep 60; dc logs --since 5m db-backup | grep -E 'dump complete|verified:|remote_upload_(succeeded|skipped)|ERROR|FAILED'
dc exec -T db-backup sh -c 'ls -l /backups/daily | tail -3; cat /backups/last_success'
```

Required before continuing: `verified: N objects in the archive`, a daily file stamped now,
and `remote_upload_succeeded`. If the log says `remote_upload_skipped`, copy that encrypted
file off the host yourself first. Record the time, the database size from step 1, the file
name and where the off-host copy is. Restoring is DEPLOYMENT.md §3.2. This release should
never need it: 037 only adds a table, and step 8 removes it.

## 3. Build the release (no downtime)

```sh
git fetch origin
git checkout --detach origin/release/2026-10-10
git log -1 --format='%h %s'             # must be the release commit named in the release report
for s in api frontend; do docker tag "$(dc images -q $s)" "masar-rollback-$s:$PREV"; done
dc build api frontend
```

## 4. Migrate 036 to 038 (**CHANGE**: schema)

037 creates `mentor_requests`. 038 only adds `pro_ai_usage.release_reason` where an early
draft of 036 left it out; production's 036 already created it, so 038 changes nothing here.

```sh
dc run --rm --no-deps api alembic current        # 036_pro_ai_usage
dc run --rm --no-deps api alembic upgrade head
dc run --rm --no-deps api alembic current        # 038_pro_ai_release_reason (head)
psqlq -c '\d mentor_requests'
```

Expect `uq_mentor_requests_user_action_request` (unique user, action, request id),
`ck_mentor_requests_status`, `ix_mentor_requests_updated_at`, and the foreign key to `users`
with `ON DELETE CASCADE`. No existing row is touched. The API that is still running ignores
the new table, so migrating before the swap is safe.

## 5. Backend, then frontend (**CHANGE**)

```sh
dc up -d --no-deps api
until [ "$(docker inspect -f '{{.State.Health.Status}}' "$(dc ps -q api)")" = healthy ]; do sleep 3; done
curl -fsS https://api.masarai.net/health; echo
dc up -d --no-deps frontend
until [ "$(docker inspect -f '{{.State.Health.Status}}' "$(dc ps -q frontend)")" = healthy ]; do sleep 3; done
curl -s -o /dev/null -w '%{http_code}\n' https://masarai.net/
dc ps; docker stats --no-stream
dc logs --since 10m api 2>&1 | grep -E -i 'traceback|error|worker timeout|exception' | tail -20
```

## 6. Smoke test with controlled accounts

Two test learners, never a real learner's account. **CHANGE**: creates or refreshes
`smoke-wallet@example.com` (80 credits granted through the ledger, course-001 and course-013)
and `smoke-pro@example.com` (a Pro subscription that ends by itself 24 h later). A one-off
container is used rather than `exec` into the API, so the workers' metrics directory is never
touched.

```sh
read -rs SMOKE_PASSWORD                  # pick one for the two test accounts
dc run --rm --no-deps -T -e SMOKE_PASSWORD="$SMOKE_PASSWORD" -e SMOKE_PRO=1 api python - < deploy/smoke/make_smoke_learners.py
```

Then run the smoke test from any machine with Python 3.8 or later. It uses only the public API
and the standard library:

```sh
SMOKE_EMAIL=smoke-wallet@example.com SMOKE_PRO_EMAIL=smoke-pro@example.com \
SMOKE_PASSWORD=... SMOKE_PRO_PASSWORD=... python3 deploy/smoke/mentor_smoke.py
```

It makes about 16 model calls, which costs the wallet learner about 22 credits and the Pro
learner 2 allowance credits. Exit code 0 means all 23 checks passed: grounding A to E, hint,
code review, weekly plan, interview, wallet cost, three idempotency checks, the five
security probes, and the Pro allowance. Then read `mentor_smoke_report.json` yourself for
English and Arabic quality, a hint that guides without the solution, and an interview
question about the completed lesson. If the locked-lesson probe reports `no data to build the
probe`, course-016 is free on this deployment: set `SMOKE_LOCKED_COURSE` to a paid course slug
the wallet learner is not enrolled in, and run again.

While it runs, watch the host:

```sh
docker stats --no-stream; dc logs -f --since 1m api 2>&1 | grep --line-buffered -E 'mentor_event|ERROR|TIMEOUT'
```

If every send fails with 503 and the balance does not move, the provider key is being
rejected (each send is charged and refunded). Check `dc logs api | grep -m3 openai` before
anything else.

## 7. After the smoke test

```sh
dc logs --since 30m api 2>&1 | grep -c 'Explain this more simply'          # 0: learner text is never logged
dc logs --since 30m api 2>&1 | grep mentor_event | tail -5                  # mode, lesson, provider, tokens, credits, outcome
psqlq -c "select action, status, count(*) from mentor_requests group by 1, 2 order by 1, 2"
psqlq -c "select count(*) from mentor_requests where status = 'processing' and updated_at < now() - interval '2 minutes'"
dc run --rm --no-deps -T -e SMOKE_CLEANUP=1 api python - < deploy/smoke/make_smoke_learners.py
```

The stale `processing` count can only be non-zero until that learner's next mentor request:
that request refunds the charge (`refund_abandoned`). This was verified before release by
killing workers mid-request. Do not repeat that on production. Such a refund is not logged
(only a failed one is, at CRITICAL: `abandoned-request refund FAILED`). It shows in the ledger:

```sh
psqlq -c "select count(*), sum(credits) from wallet_transactions where description like 'Refund: % never answered'"
dc logs --since 24h api 2>&1 | grep -c 'abandoned-request refund FAILED'                 # must be 0
```

## 8. Rollback

Roll back on a failed migration, unexpected credit loss, an answer from another account's
data or from the wrong lesson, repeated 500s, a worker crash loop, or an authentication or
billing regression.

```sh
psqlq -c "select count(*) from mentor_requests where status = 'processing'"   # wait until 0, so no charge is stranded
dc run --rm --no-deps api alembic downgrade 036_pro_ai_usage                   # with the NEW image: it knows 037 and 038
dc config --images                                                             # the api and frontend image names
docker tag "masar-rollback-api:$PREV" <api image name>
docker tag "masar-rollback-frontend:$PREV" <frontend image name>
dc up -d --no-deps --no-build api frontend
git checkout --detach "$PREV"
```

The downgrade drops only `mentor_requests`. Wallets, the Pro allowance ledger and every other
table are untouched.
