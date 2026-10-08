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

### Production comes from before the catalogue existed: run the backfill after seeding

Production is at revision **008**. `courses` is created (empty) by 011 and filled by the
seeds, so when 018 and 021 run inside `alembic upgrade head` there is no catalogue yet:
018 enrolls nobody and 021 grandfathers nobody. Before 011 every course was open to
everyone, so the learners who were already taking a course must keep it — that is what
`seeds/backfill_legacy_enrollments.py` does, once the catalogue exists. For each account
created before `--legacy-before`, every course it was working in before that moment (a
tool-course enrollment, or progress in the course's tool topics or a track level's
topics) gets an active **`legacy_free`** enrollment, recorded in
`course_enrollment_legacy_free` exactly like 021's own (021's downgrade turns it back into
`free`). Purchases, admin grants and inactive enrollments are left alone; no wallet,
progress or legacy row is touched; a second run changes nothing. Activity or accounts from
`--legacy-before` onwards never count.

Deploy order (`--legacy-before` = when the release window began, before the migrations,
with its UTC offset):

```sh
alembic upgrade head
python seed.py
python seeds/seed_tool_courses.py            # + seed_tool_{langchain,langgraph,llamaindex,qdrant,fastapi}.py
python seeds/seed_arabic_first_demo.py
python seeds/seed_learning_paths.py
python seeds/import_courses.py
python seeds/backfill_legacy_enrollments.py --legacy-before 2026-10-09T18:00:00+00:00 --dry-run
python seeds/backfill_legacy_enrollments.py --legacy-before 2026-10-09T18:00:00+00:00
```

Check: `SELECT source, status, count(*) FROM course_enrollments GROUP BY 1, 2;` shows one
active `legacy_free` row per pre-launch learner/course pair, and
`SELECT count(*) FROM course_enrollment_legacy_free;` the same number.

Rehearsed 2026-10-08 on a database built by the 008-era code and seeds with production's
shape (99 learners and promo wallets, 67 track enrollments, 30 tool enrollments over 19
learners, 3 progress rows): every user, wallet, ledger row, enrollment and progress row
unchanged by the upgrade; all 30 learner/course pairs end with `legacy_free` access.

### Launch-promo expiry never goes below 40 (decision 2026-10-08)

Pre-launch accounts hold a 500-credit launch promo that lapses 30 days after signup (the
first on 2026-10-10). Expiry still withdraws unspent promo credits, but never takes a
wallet below the Free plan's **40**: a 500-credit promo wallet ends at 40, not 0; a
balance already under 40 loses nothing; purchased credits are never withdrawn. The
`promo_expiry` ledger row records exactly what was removed.

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

## Pro: all courses plus 50 AI credits per rolling 4 hours (decisions 2026-10-08)

**Courses.** An entitled Pro subscription - paid (active, or cancelled until its paid
period ends) or the 7-day trial - opens every course, unchanged. Free previews,
purchases, `legacy_free` enrollments and admin grants are untouched.

**AI.** A *paid* Pro subscription pays for AI actions from an included allowance instead
of the wallet: **50 credits** (`PRO_AI_CREDITS_PER_WINDOW`) per **rolling 4 hours**
(`PRO_AI_WINDOW_SECONDS=14400`), at the existing per-action prices. The **trial** pays
for AI from the wallet until the first payment (`PRO_AI_INCLUDE_TRIAL=false`); the
billing page says so. Only actions that call the model provider count (mentor chat and
message, code review, skill gap, mock interview, roadmap, exercise feedback, project and
challenge hints); challenge enrolment and everything deterministic stay on the wallet,
and the free AI features with their own limits (quiz translation, AI project review) are
not counted. At the limit the request is refused before the provider is called (`429
pro_ai_limit_reached`, with `remaining`, `next_credit_available_at`, `retry_at`,
`Retry-After`; shown localized everywhere); wallet credits are never used instead.

**Accounting.** One `pro_ai_usage` row per action (migration **036**): reserved under a
per-account advisory lock before the call; consumed when the request answers 2xx/3xx;
released (with `release_reason`) when it fails - every provider error, timeout or
unusable answer is refunded by its endpoint, and any other failed response is released
by `AllowanceRequestMiddleware`. A reservation nobody settled within
`PRO_AI_RESERVATION_TTL_SECONDS` (300; a worker killed mid-request) is released, not
counted. A usage counts for 4 hours from its reservation; the window belongs to the
account, so resubscribing does not refill it. Mentor v2's cap of 3 refunded
(validation-failed) replies per day counts allowance releases too. No AI endpoint
streams; a client that disconnects after the server answered keeps no refund - mentor
chat, Mentor v2 (replayed free by `requestId`) and exercise feedback keep the answer
server-side; code review, mock-interview questions, skill gap, roadmap and hints do not.
`GET /api/v1/billing/ai-allowance` reports plan, allowance, `ai_billing` and `trial`.

## Payments: Kashier (Paymob historical only)

Every new checkout - Pro, course purchases, credit top-ups, exam fees - is a Kashier
hosted payment session (`KASHIER_*` settings; see deploy/production.env.example). The
webhook (`/api/v1/payments/kashier/webhook`, passed to Kashier per session) changes
anything only when its `x-kashier-signature` verifies, the order, amount, currency and
status are covered by that signature, and Kashier's own record agrees: for a payment the
session's payment (`GET /v3/payment/sessions/{id}/payment`) is paid, for this order, and
its amount is the one settled; for a refund, void or reversal the session document
(`GET /v3/payment/sessions/{id}`) is for this order and already shows at least that much
refunded. Otherwise it answers 503 and Kashier retries (up to 10 times over a day). The
browser's return never grants anything. Refunds are made in the Kashier dashboard and
reconciled by the webhook with the existing rules (full refund ends that order's period,
partial keeps Pro). Pro does **not** renew automatically: renewal is a new checkout
before the period ends, which extends from the current end. Paymob is never initiated;
its webhook stays for the orders it already took. Frontend build:
`NEXT_PUBLIC_PAYMENTS_PROVIDER=kashier`.

**Not verified against a live Kashier account - check in test mode before taking money:**

1. the webhook `data.amount` unit (read as pounds; the docs' examples do not say);
2. the paid-session status value (`PAID` or `CAPTURED` accepted; anything else waits);
3. the session document's `refundedAmount` (read as pounds, cumulative) and
   `paymentParams.order` fields;
4. which fields Kashier lists in `signatureKeys` (merchantOrderId, amount, currency and
   status must be among them, or the webhook is refused with 400);
5. the event names for a refund, partial refund and void, and that each arrives as
   its own webhook with its own `transactionId`;
6. a `display=ar` checkout, and the return to `/api/v1/payments/kashier/return`.

Each wrong guess fails closed (no grant, no revocation; Kashier retries, staff reconcile
from the dashboard). Record the raw payloads (`subscription_payment_events.raw_payload`,
`payment_transactions.raw_payload`) of one payment, one full and one partial refund.

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
