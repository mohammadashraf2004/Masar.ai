# Masar launch release (2026-10-10) — data changes and recovery

For operators deploying this release. Everything here is decided product policy
(2026-10-07); the migration and code enforce it.

## Migration 021 — Free/Pro plans

**Credits: a floor, never a reset.** Eligible free students — role `student`, no
confirmed top-up, no purchased or admin-granted course, no paid course order — are
raised to **at least 40 credits**. A balance at or above 40 is left exactly as it is.

| before | after | ledger |
|---:|---:|---|
| 0 | 40 | `+40` |
| 10 | 40 | `+30` |
| 40 | 40 | none |
| 75 | 75 | none |

Each raised wallet gets one `wallet_transactions` row, `action_type =
'free_plan_40_migration_v1'`, for exactly the credits added. That marker makes the
migration idempotent: running it again changes nothing. A raised wallet's promo window
is closed at the same time, so a later promo expiry cannot pull it back under 40;
wallets already at or above 40 keep their balance and promo terms.

**Courses: the old free flags are kept, and so is access.**

* Before any `courses.is_free` is switched off, every course's previous value is
  copied to **`course_free_legacy(course_id, was_free, recorded_at)`**.
* A learner with an **active** enrollment in a course that **was free** keeps that
  course: the enrollment's `source` changes from `free` to **`legacy_free`**, which the
  access layer treats as an entitlement like `purchase`/`admin_grant`. Each conversion
  is recorded in **`course_enrollment_legacy_free(enrollment_id, user_id, course_id,
  previous_source, granted_at)`**.
* Learners who never enrolled gain nothing; preview (`free`) enrollments in paid
  courses, and revoked/expired enrollments, are not touched.
* `downgrade` of 021 restores `courses.is_free` and every recorded enrollment source
  exactly (balances are not reversed — later spending makes that unknowable — but the
  ledger rows above say what was added).

Read-only checks after deploying:

```sql
SELECT version_num FROM alembic_version;                       -- expect the release head
SELECT count(*) FILTER (WHERE was_free) AS were_free, count(*) FROM course_free_legacy;
SELECT count(*) FROM course_enrollment_legacy_free;             -- learners who kept a course
SELECT count(*), sum(credits) FROM wallet_transactions
 WHERE action_type = 'free_plan_40_migration_v1';               -- wallets raised, credits added
```

Recovering the pre-launch course state by hand, if ever needed (prefer `alembic
downgrade` when possible):

```sql
UPDATE courses c SET is_free = l.was_free FROM course_free_legacy l WHERE l.course_id = c.id;
UPDATE course_enrollments e SET source = l.previous_source
  FROM course_enrollment_legacy_free l WHERE l.enrollment_id = e.id;
```

## Course modules regrouped (consolidated chapter files)

Courses whose manifest sets `consolidated_file_modules` (and COURSE-004) now present
each chapter file as its own module; lesson ids do not change. On import, a learner's
completion of a lesson or exercise that moved to another module is **carried** from
their progress row for the old module to the row for the new one
(`importer._carry_progress`; the import report shows `progress_carried`). Nothing is
dropped. Re-importing is safe: a second import carries nothing.

## Limits and policies introduced with this release

* AI-reviewed project submissions: **10 per account per rolling 24 hours**
  (`PROJECT_REVIEW_LIMIT_PER_DAY`), plus the existing per-IP limit; refusals are
  `429 PROJECT_REVIEW_LIMIT` with `Retry-After`. Requests that fail before the review
  (not found, no access, validation) do not count.
* Shared code runner: one execution per account at a time and 120 runner-seconds per
  10 minutes per account (`RUNNER_USER_SECONDS`, `RUNNER_USER_WINDOW_SECONDS`).
* Mentor: rejected model replies are refunded up to 3 times per account per day
  (`MENTOR_VALIDATION_REFUNDS_PER_DAY`); provider failures are always refunded.
* Quiz translations: only email-verified accounts trigger a model call; a failed
  translation is not retried for 6 hours.
* Subscription refunds: a **partial refund keeps Pro**; a verified **full** refund ends
  only the period that order bought.
* Request bodies over 4 MiB are refused (API and Caddy).
* Walkthrough tours treat accounts created at or after **2026-10-10 00:00 Cairo time
  (2026-10-09T21:00:00Z)** as new signups.

## Before switching traffic

See the production verification list in the release audit: production
`alembic_version` and existing users/enrollments/progress/balances (read-only),
gVisor on the real host, an S3 backup restored into an isolated database, live
Paymob (HMAC, webhook, one small payment, duplicate callback, refund), live Mentor
smoke tests, and DNS/TLS for `masarai.net`, `www.masarai.net`, `api.masarai.net`.
