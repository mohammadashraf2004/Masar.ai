# Phase 4 handoff: release candidate 2

Branch `release/2026-10-10-rc2`, draft pull request #2 (base `release/2026-10-10`). The code was tested at
`bbc77a8bb0dd589d7b2701b2b221696ab2d06a6c`; the commits after it add only this document and
`deploy/rehearsal/snapshot.py`. CI results are on the pull request. Nothing here was deployed and
production was not touched. Passing CI is not a statement that the release is ready for production.

The operator runbooks stay authoritative: `docs/release-2026-10-masar-launch.md`,
`deploy/exercise-release-checklist.md`, `deploy/smoke/README.md`, `docs/project-lab.md`.
This page lists what is still open and what the rehearsals showed.

## Open before anything is deployed

| Item | State | What to do |
|---|---|---|
| Production baseline | at `69499c0`, migration 036 | The path is `037 -> 038 -> 039 -> 040`. |
| Learner code execution | the host has no gVisor | Keep `PROJECT_LAB_EXECUTION_BACKEND=disabled`. In production the API refuses to boot with `runner` unless the runtime is `runsc` with the gVisor seccomp profile (tested). Do not enable it until the host passes the gVisor runbook in `docs/project-lab.md`. |
| Payments | provider not configured | Leave `PAYMENTS_ENABLED=false`, every `KASHIER_*` and `PAYMOB_*` empty and `NEXT_PUBLIC_PAYMENTS_PROVIDER` empty. Every checkout then answers `503 PAYMENTS_UNAVAILABLE` and writes nothing. Enabling needs live keys, the switch, and an independent real payment, webhook and refund test. |
| Caddy | the host's Caddyfile differs from the repository's | Do not overwrite it. Diff the active file against `deploy/Caddyfile`, keep the registration protections the host has and the repository lacks, then `caddy validate` and probe registration and login before and after any change. |
| Disk and memory | about 5 GB free, 3.8 GB RAM | Check `docker system df` and `df -h` first. Building the frontend image (`next build`) and pulling new API layers are the risk; build elsewhere or free space before the swap rather than discovering the limit mid-deploy. |
| Backup | an off-server database backup is required | Take it with `deploy/backup/pg-backup.sh`, copy it off the host, and restore it into an isolated database (`deploy/backup/verify-dr-restore.sh`). A restore is the real rollback; see "Rollback" below. |
| Real AI provider | not smoke-tested | Everything mentor-related ran against mocks or with no key. Run `deploy/smoke/mentor_smoke.py` with a valid key and a real request, and record the result. |

## The rehearsal to repeat on the production backup

What was rehearsed here used a development database (28 users, 54 courses, 1,194 exercises) restored into a
disposable container. Production has more learners, so repeat this on a restore of the real backup and
compare the counts below with what you see.

1. **Preflight.** `alembic current` must say `036_pro_ai_usage`, and both of these must exist:
   `select to_regclass('course_enrollment_legacy_free'), to_regclass('course_free_legacy');`.
   The development database was stamped at 038 but lacked those two tables (migration 021 creates
   them), and the backfill inserts into the first. A missing table fails the backfill after the
   migrations have already run.
2. **Snapshot.** `python deploy/rehearsal/snapshot.py save --dsn <restored copy> before.json`.
3. **Migrate.** `alembic upgrade head`; expect `037`, `038`, `039`, `040`, head `040_exercise_example_answers`.
   Then `snapshot.py compare`. Expected findings, and only these: `alembic_version`, `credit_packages`
   (3 old packs kept and switched off, 4 new ones added), and the new table `mentor_requests`.
   Anything else is a defect.
4. **Check 039/040 directly.** Four active packs (starter 50/29, standard 150/69, plus 400/149 popular,
   power 1000/299); every wallet has `purchased_credits = greatest(0, least(credit_balance, lifetime_purchased))`;
   confirmed top-ups have `settled_at` and `purchased_delta`; `exercises.example_answer` columns exist and are empty.
5. **Import.** `python seeds/import_courses.py --validate-only` (18 courses, 210 modules, 214 lessons),
   `--dry-run` (must change nothing), the real import, then a second one. Stable keys must keep their ids and the
   second run must be a no-op; only exercise content changes. Learner tables must not appear in `compare`.
6. **Backfill.** `python seeds/backfill_legacy_enrollments.py --legacy-before <moment the release window began, with offset> --dry-run`,
   then for real, then again (the second reports `grandfathered: 0`). A cutoff in the future is refused.
   Learners who only enrolled in a course by hand, with no earlier tool activity, are not backfilled; that is
   by design (12 of the 21 enrollments in the development copy).

## Rollback

- A database restore from the backup is the rollback. Do not rely on `alembic downgrade`.
- Downgrading 039 and 040 keeps every learner record but drops the purchased-credit bucket, the ledger link
  columns and any example answers entered since, and leaves the four packs in place. Upgrading again then adds four
  inactive duplicate packs; the active catalogue stays correct. Migration 039 matches `main`'s, so it was not edited here.
- Code rollback is the previous image (`69499c0`); the schema has to be restored with it.

## Build and configuration notes

- `NEXT_PUBLIC_MENTOR_V2_LIVE` now defaults to `message,quiz` in `docker-compose.yml`. The first mentor chat
  (`POST /mentor/chat`) is retired (410); a build without the variable would ship the screen that calls it.
- `NEXT_PUBLIC_API_URL` and `NEXT_PUBLIC_SITE_URL` are baked into the client bundle and the production overlay
  refuses to build without them.
- Nine development-only `npm audit` findings remain (the Tailwind 3 and `eslint-config-next` glob chains).
  There is no non-breaking fix; none is in the shipped bundle. The production audit is clean.
- `main` still fails lint on `community/page.tsx`; this branch already contains the corrected effect.
- Browser checks ran on desktop Chromium (1280 px) and a 390 px phone viewport only.
