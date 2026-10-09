# Guided exercises + mandatory gVisor: deploy with learner Python execution OFF

For the operator deploying release/2026-10-10 with the guided exercises and the gVisor
enforcement, on the production host (SSM session; compose project `app`, checkout in
`/home/ubuntu/app`, env file `/etc/masar/production.env`). Steps marked **CHANGE** modify
production; everything else only reads. Stop at the first failed expectation and roll back
([section 10](#10-rollback)). Do not patch production by hand.

This release does **not** turn learner Python on. It keeps it off, and makes "off" the only
state production can start in until the host passes the gVisor runbook
(`docs/project-lab.md`, "Production host runbook (gVisor)"). The AI Mentor part of the
release is deployed and smoke-tested with `deploy/smoke/README.md`; this checklist says where
its steps go.

## What changes for production

* **Guided exercises**: course content only (no migration). 886 exercises keep their
  importer keys and database ids; 240 get a new starter (229 guided fill-in-the-blank code
  exercises, 11 written), 235 change type (`code_pending`→`code` 221, `legacy`→`code` 3,
  `code_pending`→`legacy` 11). A learner's browser keeps an old draft but shows the new
  scaffold for those 240 (drafts are keyed by starter). Attempts, completion and
  enrolments are untouched.
* **gVisor enforcement**: in production the API refuses to start if
  `PROJECT_LAB_EXECUTION_BACKEND=runner` without the full gVisor contract, and refuses to
  serve until a live runner reports gVisor. The project runner is behind the Compose profile
  `project-lab`, so a normal `up` never starts it.
* **Off by default**: `docker-compose.prod.yml` defaults `PROJECT_LAB_EXECUTION_BACKEND` to
  `disabled` (only `docker-compose.yml` alone, for local development, falls back to
  `runner`). An env file without the variable therefore boots with execution off; only an
  explicit `runner` turns it on, and then the gVisor checks above apply. Step 3 still writes
  `disabled` into the env file so the host records the decision explicitly.
* **Messages**: when execution is off, Run and Check say so in the learner's interface
  language (Arabic or English) on exercises and in the Project Lab.

## 0. Shell setup

```sh
cd /home/ubuntu/app
alias dc='docker compose --env-file /etc/masar/production.env -f docker-compose.yml -f docker-compose.prod.yml'
psqlq() { dc exec -T db sh -c 'psql -X -U "$POSTGRES_USER" -d "$POSTGRES_DB" "$@"' psql "$@"; }
PREV=$(git rev-parse --short HEAD)      # the release running now, for rollback
```

## 1. Preflight (read-only)

Run `deploy/smoke/README.md` section 1, then:

```sh
sudo grep -nE '^(PROJECT_LAB_|PROJECT_RUNNER_)' /etc/masar/production.env
docker ps -a --format '{{.Names}} {{.Status}}' | grep -i runner || echo "no runner container"
docker info --format '{{json .Runtimes}}'          # runsc is NOT expected yet
free -h
```

Expect no runner container (none was running when the host was last inspected) and no
`runsc`. Note whether `PROJECT_LAB_EXECUTION_BACKEND` is present and its value.

## 2. Backup (**CHANGE**)

`deploy/smoke/README.md` section 2. Also keep the env file:

```sh
sudo cp -p /etc/masar/production.env /etc/masar/production.env.pre-exercises
```

## 3. Turn learner execution off explicitly (**CHANGE**: env file only)

Containers read the file only when recreated, so this changes nothing that is running.
With this release's compose files the line is optional (the production default is
`disabled`), but keep it: the previous release's compose files default to `runner` and have
no `project-lab` profile, so after a rollback only this line keeps execution off and a full
`dc up -d` from starting a runc runner.

```sh
if sudo grep -q '^PROJECT_LAB_EXECUTION_BACKEND=' /etc/masar/production.env; then
  sudo sed -i 's/^PROJECT_LAB_EXECUTION_BACKEND=.*/PROJECT_LAB_EXECUTION_BACKEND=disabled/' /etc/masar/production.env
else
  echo 'PROJECT_LAB_EXECUTION_BACKEND=disabled' | sudo tee -a /etc/masar/production.env >/dev/null
fi
sudo grep -c '^PROJECT_LAB_EXECUTION_BACKEND=disabled$' /etc/masar/production.env   # 1
```

Leave `PROJECT_RUNNER_RUNTIME=runc`, `PROJECT_RUNNER_REQUIRE_GVISOR=0`,
`PROJECT_LAB_REQUIRE_GVISOR=false` as they are: with `disabled` none of them is used, and
the runner is never started. Never set `runner` in this release.

## 4. Build the release (no downtime)

`deploy/smoke/README.md` section 3 (fetch, detach at the release commit named in the release
report, tag rollback images, `dc build api frontend`).

## 5. Prove the new image accepts this env file, before swapping anything

```sh
dc run --rm --no-deps -T api python -c "from app.core.config import settings; print('backend =', settings.project_lab_backend)"; echo "rc=$?"
dc config --services | grep -x project-runner || echo "runner not in the default stack (expected)"
dc config | grep -E '^\s+PROJECT_LAB_EXECUTION_BACKEND:'      # PROJECT_LAB_EXECUTION_BACKEND: disabled
```

Expect `backend = disabled` and `rc=0`. `Refusing to start with APP_ENV=production` lists
what is wrong: fix the env file and repeat; do not continue. (This is exactly the check the
API runs at boot, so a pass here means the swap will boot.)

## 6. Migrate (**CHANGE**: schema, AI Mentor only)

`deploy/smoke/README.md` section 4. The exercise work adds no migration; head is
`037_mentor_requests`.

## 7. Backend, then verify execution is off (**CHANGE**)

```sh
dc up -d --no-deps api
until [ "$(docker inspect -f '{{.State.Health.Status}}' "$(dc ps -q api)")" = healthy ]; do sleep 3; done
curl -fsS https://api.masarai.net/health; echo
docker inspect -f '{{range .Config.Env}}{{println .}}{{end}}' "$(dc ps -q api)" | grep -E '^(APP_ENV|PROJECT_LAB_EXECUTION_BACKEND)='
dc ps --services --status running | grep -x project-runner && echo "STOP: a runner is running" || echo "no runner (expected)"
dc logs --since 5m api 2>&1 | grep -E 'Application startup (complete|failed)' | sort | uniq -c
```

Expect `APP_ENV=production`, `PROJECT_LAB_EXECUTION_BACKEND=disabled`, no runner, four
`Application startup complete`. If the container restarts instead, run
`dc logs --since 5m api | grep -m5 -E 'Refusing|gVisor|RuntimeError'` and roll back.

Then show that learner Python cannot run (one-off container with the production settings;
it never touches the running workers):

```sh
dc run --rm --no-deps -T api python - <<'EOF'
import asyncio
import app.main  # noqa: F401
from app.services.project_lab import execution
from app.services.code_execution import IsolatedPythonRunner
print("backend:", type(execution.build_backend()).__name__)
r = asyncio.run(IsolatedPythonRunner().run("print('LEARNER CODE RAN')"))
print("status:", r.status, "| stdout:", repr(r.stdout), "| stderr:", repr(r.stderr))
assert r.status == "execution_error" and "LEARNER CODE RAN" not in r.stdout
EOF
```

Expect `backend: DisabledBackend` and `status: execution_error`, stderr
`Project execution is not available right now.`

## 8. Import the guided exercises (**CHANGE**: catalogue content, one transaction)

After the API swap, so only the new code ever reads the new content. Course files are
baked into the API image, so the one-off container imports exactly this release.

```sh
dc run --rm --no-deps -T api python seeds/import_courses.py --validate-only
dc run --rm --no-deps -T api python seeds/import_courses.py --dry-run | tee /tmp/import-dry.txt | tail -45
```

Expect `Validated 18 courses`, and in the dry run no `retired` and no `stale` lines
(`grep -cE 'retired|stale' /tmp/import-dry.txt` prints 0), exercises only updated or
unchanged, never created. Rehearsed on a database holding the previous release's catalogue
plus learner attempts: every course line reads `exercises +0 ~N =M`, 852 updated and 34
unchanged in total (the briefs were rewritten, so most exercises change), modules and
lessons all unchanged; afterwards every exercise id and every attempt was identical, and a
second import reported `+0 ~0 =886`. If anything is retired, created or stale, stop: the
catalogue on production is not the one this release expects.

```sh
dc run --rm --no-deps -T api python seeds/import_courses.py | tee /tmp/import.txt | tail -45
psqlq -c "select exercise_type, count(*) from exercises where source_key like 'COURSE-%' group by 1 order by 1"
```

Expect `code 239`, `legacy 647`, no `code_pending`.

## 9. Frontend, AI Mentor smoke test, cleanup

`deploy/smoke/README.md` sections 5 (frontend part), 6 and 7. In a browser, open a lesson
with a guided exercise as the smoke learner: the brief has numbered steps, the editor shows
the `___` blanks. On a Python exercise that needs execution, **Run** prints
`Project execution is not available right now.` and **Check** shows "Could not check" with
the same sentence; in the Arabic interface they read `تشغيل الكود غير متاح الآن.` and
"تعذّر التحقق". The attempt does not count towards the 3-attempt solution reveal. Exercises
graded by static checks, and SQL exercises, still grade normally. A Project Lab **Run** shows
the same sentence in the interface language.

## 10. Rollback

* **Application**: `deploy/smoke/README.md` section 8 (retag the rollback images, `dc up -d
  --no-deps --no-build api frontend`, `git checkout --detach "$PREV"`). Keep
  `PROJECT_LAB_EXECUTION_BACKEND=disabled`: the previous release also honours it.
* **Exercise content**: after the image rollback, re-import with the old image (its own
  course files): `dc run --rm --no-deps -T api python seeds/import_courses.py --dry-run`,
  then without `--dry-run`. Rows are updated in place by key, so ids, attempts and progress
  stay attached.
* **Env file**: keep step 3's `PROJECT_LAB_EXECUTION_BACKEND=disabled` when rolling back.
  The previous release's compose files default to `runner`, so restoring
  `/etc/masar/production.env.pre-exercises` without that line would let the old stack select
  the runner (and start it under runc on a full `dc up -d`).
* **Incident switch at any later time** (for example once the runner is enabled): set
  `PROJECT_LAB_EXECUTION_BACKEND=disabled`, `dc up -d --no-deps --force-recreate api`, then
  `dc stop project-runner`. Rehearsed locally: the API is healthy again, and the runner is
  stopped.

## Not in this release: turning learner Python on

Only after `backend/scripts/project_runner_production_check.sh /etc/masar/production.env`
passes **on this host** (runsc installed and registered, the runner container running under
`runsc`, the 96-probe security suite under gVisor, a capstone slice through the API). Before
that, review capacity: the host has 3.8 GB of RAM and the runner alone may use 1.5 GB next
to four API workers, Postgres, Redis, the frontend and monitoring. While execution is
`runner`, an API restart with the runner down or not gVisor takes the whole API down until
the runner is healthy again or the backend is set back to `disabled` (fail-closed by design).
