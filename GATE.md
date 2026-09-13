# Pre-launch security gate

Four passes are recorded here. Pass 2 audited the first remediation. Pass 3
executed the Next.js migration and produced the infrastructure
specification in [DEPLOYMENT.md](DEPLOYMENT.md). Pass 4 re-verified every
prior finding against the live code and test suite, closed one
newly-found race condition, and investigated (but did not ship) two
architecture changes flagged as open in earlier passes. Pass 5 (below,
newest) is the final production gate: business-logic/concurrency sweep
across every financially-sensitive operation, verified against the
actual production Docker images rather than approximations.

---

# Pass 5 — final production gate: business logic, concurrency, real images

Scope: every wallet/payment/exam/challenge operation, checked for replay,
double-charge, double-credit, and duplicate-entitlement; concurrency
tests against the operations that touch money or entitlement; then the
full backend test suite run *inside the actual production Docker image*
(Python 3.11, matching CI) against a database migrated from empty by that
same image, plus the production frontend image built and scanned for
secrets — not the venv approximation Pass 4 used for the equivalent
checks.

## FIXED — new finding

### P5-1 (MEDIUM) · Concurrent exam-start requests could open more than one in-progress attempt
- **Component** `POST /exams/{exam_id}/start` (`app/controllers/exam_controller.py`)
- **Why it matters** Same TOCTOU shape as P4-1 (challenge enrolment),
  and worse here because nothing guarded it at all — no row lock, no
  constraint. `start_exam`'s "resume an existing in-progress attempt, or
  open a new one" logic is a plain read-then-write. A first attempt at
  reproducing it with a bare `threading.Thread` race did not trigger
  (threads didn't reliably overlap at the SELECT); adding a
  `threading.Barrier` so every worker reaches "session open, about to
  call `start_exam`" at the same instant reproduced it **on every run**
  — confirmed, not theoretical. Impact: two independent
  `started_at`/deadline windows against the exam's one fixed question
  set is a free extra look at the paper before committing answers,
  undermining exactly the guarantee the proctoring/violation-tracking
  machinery around this feature exists to protect, and both racing
  attempts count toward `max_attempts`.
- **Fix** Same pattern as migration 009: a partial unique index,
  `uq_exam_attempts_one_in_progress` on `(user_id, exam_id) WHERE status
  = 'in_progress'` (`alembic/versions/010_exam_attempt_start_race.py`,
  declared in `ExamAttempt.__table_args__`). `start_exam` now catches the
  losing racer's `IntegrityError` and resolves it to the winner's attempt
  (the same outcome the sequential "resume" path already gives) instead
  of surfacing a bare 409.
- **Test** `tests/test_exam_concurrency.py::test_concurrent_start_requests_produce_at_most_one_in_progress_attempt`
  — the regression test for this fix specifically (10-thread barrier
  race; reproduces the bug pre-fix on every run, passes reliably
  post-fix across repeated runs).

  The same file's second test,
  `test_verifies_preexisting_certificate_uniqueness_survives_concurrent_submit`,
  is **not** part of this fix and is not a second confirmed
  vulnerability — it exercises `/submit` with the same barrier-race
  technique and confirms that the pre-existing `UNIQUE` constraint on
  `Certificate.attempt_id` (present since the original schema, untouched
  by this pass) already prevents a double certificate from a
  concurrent-submit race. Filed as verification, not remediation; see
  "Business-logic sweep" below for why the submit-side race itself
  (real, same shape as P5-1) was not filed as its own finding.

## FIXED — build hygiene

### P5-2 (LOW) · `.dockerignore`'s venv exclusion did not match a differently-named virtualenv
Building `backend/`'s production image while a `.venv-audit/` directory
(this pass's own disposable test environment) was present copied it
straight into the image — `.dockerignore` listed only the literal names
`.venv/` and `venv/`, and lacked the `**/` prefix its own `__pycache__`
rule already documents as necessary for Docker's non-recursive glob
matching. Self-inflicted by this audit's tooling, not a pre-existing
product defect, but the same class of defect as the `.env`-in-image
incident this file already records — a build-context exclusion that
looks like it covers a case it does not. **Fixed:** `**/.venv/`,
`**/.venv*/`, `**/venv/`, `**/*venv/`. **Verified:** rebuilt with a
dummy `.venv-audit-recheck/` present; confirmed absent from the image
this time.

## Business-logic sweep — no new issue found

Read every credit/payment/entitlement code path
(`wallet_service.{deduct_credits,refund_credits,add_credits,
confirm_pending_topup}`, both Paymob webhook branches, both manual admin
confirm endpoints, exam payment submit/confirm, challenge enrol/submit/
hint, project submit/hint, mentor chat/roadmap/code-review/skill-gap/
mock-interview) against the ten questions this pass's brief posed
(replay, double-charge, double-credit, credit-requirement bypass,
payment-requirement bypass, duplicate entitlement, cross-user credit
spend, cross-user financial-state mutation, DB-level invariant where
warranted). Findings:

- **Cost is always server-determined.** Every metered action's price
  comes from `CREDIT_COSTS[action_type]` or, for the two variable-price
  operations (challenge enrolment, certification exam fee), from the
  `ChallengeProject.credit_cost` / `EXAM_PRICE_EGP` server constant — no
  request schema anywhere has a `credits`/`cost`/`amount` field a client
  populates to set what an action costs.
- **Payment confirmation is already idempotent**, by construction and by
  existing test (`test_confirming_twice_pays_out_once`,
  `test_database_refuses_two_confirmed_rows_for_one_reference`):
  `confirm_pending_topup` is a no-op on a non-pending row, and a partial
  unique index (migration 008) makes a second CONFIRMED row for one
  payment reference fail at the database level regardless of which code
  path raced to write it.
- **The client cannot mark its own payment successful.** The only path
  that flips a payment to `confirmed` from an unauthenticated caller is
  the Paymob webhook, gated by HMAC-SHA512 verification
  (`verify_webhook_hmac`); the browser-return `/paymob/callback` route
  reads nothing from its own query string and only redirects to a page
  that polls the authenticated status endpoint.
- **Refunds cannot be triggered twice for one failure.** `refund_credits`
  is called exactly once per caught exception inside each metered
  handler's own except block — reaching it twice requires the underlying
  request to genuinely fail twice, each of which was itself charged
  once. No path exists for a client to invoke it directly or repeatedly
  for one charge.
- **Two new real races, found and fixed above** (P4-1, P5-1) — both
  same-user financial/entitlement duplication via a request race, never
  a cross-user credit spend or cross-user financial-state mutation. No
  attack path was found where User A can spend, refund, or otherwise
  touch User B's wallet, payment, or entitlement state.

## Defense-in-depth (not vulnerabilities)

- **Challenge submission** (`POST /challenges/{slug}/submit`) has the
  same unguarded read-then-write shape as the two fixed races, but its
  consequence is bounded to a lost-update on the *same* attempt row (no
  unique-row duplication is possible post the enrolment fix, since at
  most one ENROLLED attempt can exist) plus a wasted duplicate LLM call
  if two submissions race — a cost/robustness concern, not a
  cross-user or double-entitlement one. Not fixed; flagged for the same
  treatment (an atomic `UPDATE ... WHERE status = 'enrolled'`) if
  provider-cost pressure ever makes it worth the change.
- **Free-enrolment races** (`Enrollment`, `ToolEnrollment`) share the
  shape too, with no financial or cross-user consequence — worst case a
  cosmetic duplicate row. Not fixed, same reasoning as Pass 4's note on
  this.
- **`pip` (24.0) and `setuptools` (79.0.1) inside `python:3.11-slim`**
  carry known advisories per `pip-audit --strict` run *inside the built
  image* (PYSEC-2026-196/1795/1796/2875/2876/3721, PYSEC-2026-3447).
  These are the base image's bundled packaging tools, not an application
  runtime dependency processing attacker input — pip-audit against
  `requirements.txt` itself (the actual app dependency set) reports
  clean, matching Pass 1's M-13 remediation. Worth a `pip install
  --upgrade pip setuptools` line in the Dockerfile on the next image
  rebuild; not urgent.

## Verified against the real production images (not the venv approximation)

```
backend image  (masar-api-audit2, built from backend/Dockerfile, python:3.11-slim):
  docker build                                  — clean
  no .env* file present in the built image      — confirmed (find -iname '*.env*')
  alembic upgrade head, from EMPTY database,
    run from inside the image                   — clean, all 10 migrations apply
  python -c "import app.core.config" with
    APP_ENV=production + unsafe/missing config  — refuses to boot, lists all 6 problems
  gunicorn boot, fully configured, real HTTP:
    GET /health                                 — 200, minimal body
    GET /docs, /openapi.json                    — 404 (disabled in production)
    GET /metrics no token                       — 404 (not 401 — no existence leak)
    GET /metrics correct token                   — 200
    GET /api/v1/wallet/ unauthenticated          — 401
    security headers (CSP/HSTS/X-Frame-Options/
      Referrer-Policy/nosniff)                  — all present
  full test suite, run from inside this image,
    against a database this image itself
    migrated from empty (pytest --collect-only
    -q reports 580 tests collected; pytest -q
    reports the same run's outcome)              — 580 collected, 571 passed,
                                                     9 skipped, 0 failed
  pip-audit --strict inside the image             — 0 findings in application
                                                     dependencies (2 findings in
                                                     pip/setuptools themselves, see above)

frontend image (masar-frontend-audit, built from frontend/Dockerfile):
  docker build                                   — clean
  grep for ANTHROPIC_/OPENAI_/RESEND_/PAYMOB_
    API keys, SECRET_KEY, DATABASE_URL, and
    sk-ant-/sk-proj-/sk-live- patterns across
    .next/static and public                       — 0 matches
  no .env* file present in the built image        — confirmed
  only embedded runtime value found                — the public API URL, as intended
```

All of the above ran against disposable Postgres/Redis containers and a
disposable Docker network created for this pass and torn down
afterward — the live `2helny-*` dev stack (verified `docker ps` before
and after) was never touched, connected to, or restarted.

---

# Pass 4 — re-verification, IDOR sweep, CSP/JWT architecture review

Scope: independently re-verify Pass 1–3's authentication/authorization
conclusions against the actual running code (not just re-reading it —
`backend/tests/` was actually executed, against isolated disposable
Postgres/Redis instances, never the live dev stack); enumerate every
authenticated endpoint for IDOR/BOLA and mass-assignment; extend
regression coverage for the gaps found; and investigate the two items
this document's "Remaining risk" section had left open (token storage,
CSP `unsafe-inline`).

## Re-verified, no new issue found

Read every controller (`auth`, `wallet`, `exam`, `exam_payment`,
`challenge`, `community`, `mentor`, `answer_evaluation`, `tracks`,
`tool_courses`, `admin_analytics`, `payments`, `terminology`, `search`)
and the response schemas in every `views/*.py`, specifically for: a
client-supplied `user_id`/`owner_id` influencing authorization, a
mutation missing an ownership filter, and a response model returning more
than the endpoint needs. All ownership resolution is via
`current_user.id` derived from the verified JWT; no exception found.
Backed by 559 pre-existing tests, all passing (0 failed) against a fresh
isolated database — this document's earlier passes are re-confirmed, not
merely re-asserted.

## FIXED — new finding

### P4-1 (MEDIUM) · Concurrent challenge-enrolment requests could double-charge and double-enrol
- **Component** `POST /challenges/{slug}/enroll`
  (`app/controllers/challenge_controller.py`)
- **Why it matters** The "not already enrolled" check, the credit charge
  (`deduct_credits`), and the `ChallengeAttempt` insert were three
  unserialised steps. `deduct_credits` itself is race-safe (`SELECT ...
  FOR UPDATE` on the wallet row), but nothing serialised the *enrolment
  row* — N concurrent requests for the same user+challenge (a
  double-click, a retried request, a scripted client) could all pass the
  pre-check before any of them inserted, so all N could charge the wallet
  and all N could insert an ENROLLED row. Not a cross-user authorization
  bypass (each racer only ever spends their own credits), but a genuine
  double-spend against the user's own wallet and a duplicate paid
  attempt — explicitly the class of bug Phase 16 of this audit's brief
  asked to be swept for ("duplicate enrollment", "double credit").
- **Fix** A partial unique index, `uq_challenge_attempts_active_enrollment`
  on `(user_id, challenge_id) WHERE status = 'enrolled'`
  (`alembic/versions/009_challenge_enrollment_race.py`, declared in
  `ChallengeAttempt.__table_args__` so the schema-drift guard stays
  green) — the same pattern migration `008` already used to close the
  equivalent race on `exam_payments`. The losing racer's INSERT now fails
  at the database level and is caught by `enroll_challenge`'s existing
  except block, which rolls back and refunds the charge.
- **Test** `tests/test_challenge_enrollment_race.py` —
  10 real concurrent threads (separate DB sessions each, mirroring
  `test_wallet_concurrency.py`'s pattern) against one user+challenge;
  asserts exactly one `ChallengeAttempt` row survives and the wallet is
  net-charged for exactly one enrolment.

## New regression coverage (no defect found, closes a coverage gap)

Pass 1 built its IDOR suite (`test_security.py` §9) around mentor
sessions, exam attempts, exam payments, wallets, and community posts.
Two subsystems with the same shape — per-user conversational state keyed
only by content ids, no attempt/submission id ever appears in a request
— had no dedicated attacker-vs-victim test:

- `tests/test_challenge_idor.py` — two independent users enrolling in and
  submitting to the same challenge get independent attempts; submitting
  never grades or overwrites another user's attempt; `/attempts`,
  `/hint`, and `/dataset/download` never leak or ride on another user's
  enrolment.
- `tests/test_answer_evaluation_idor.py` — an attacker cannot read or
  extend a victim's exercise/open-quiz-question conversation
  (`AnswerSubmission`), for both the read and the write path.

All 11 pass. Combined suite: **570 passed, 8 skipped (opt-in
live-provider tests, unchanged), 0 failed.**

## Investigated, not shipped — CSP `unsafe-inline` removal

The "Accepted risks" section below has long named a nonce-based CSP as
the documented next step for `script-src 'unsafe-inline'`. This pass
actually built and empirically tested it (`src/proxy.ts` minting a
per-request nonce, following Next's documented CSP recipe) rather than
assuming it would work:

- Confirmed **nothing user-facing** requires `unsafe-inline` — the app's
  only two `dangerouslySetInnerHTML` calls are Prism's own escaped
  syntax-highlighting output, never a `<script>` tag.
- What actually needs it is Next.js's own inline hydration/RSC-bootstrap
  scripts (`self.__next_f.push(...)`).
- **The nonce only reaches those scripts on a route that renders
  dynamically.** Verified with a real `next build` + `next start`: on
  this app's current architecture (most routes prerendered `○ Static`),
  zero inline scripts carried the nonce — a strict CSP would have blocked
  Next's own hydration on every page, i.e. broken the app for every
  visitor. Making it work required the root layout to call
  `headers()`, which (confirmed by the build output) flips **every**
  route from `○ Static` to `ƒ Dynamic` app-wide — trading away static
  prerendering/edge-cacheability everywhere to remove one CSP directive.
- That trade is a performance/infrastructure decision, not a "clearly
  safe" security fix, so it was reverted rather than shipped unilaterally.
  `next.config.js` now documents this finding in place. **Recommendation
  left for a deliberate decision:** accept the current `unsafe-inline`
  (status quo, matches every prior pass's posture), adopt nonce +
  force-dynamic-rendering app-wide, or build a hash-based CSP for the
  static bundle's fixed set of inline scripts (more build tooling, no
  rendering-mode trade-off).

## Investigated, not shipped — JWT in `localStorage`

Re-read the full flow (`frontend/src/lib/api.ts`, `lib/store.ts`,
`app/core/security.py`) named in "Accepted risks" below. Conclusion
unchanged from Pass 1, reached independently:

| | Keep Bearer token in `localStorage` (status quo) | Move to `HttpOnly` `SameSite` cookie |
|---|---|---|
| XSS impact | Token readable/exfiltratable by any injected script, for up to 12h | Token not readable by JS at all — the main win |
| CSRF impact | None (no ambient credential attached by the browser) | New requirement: this app has cross-origin frontend↔API, so a cookie needs `SameSite=None; Secure` (widest CSRF exposure) plus a CSRF token on every mutating route |
| Complexity | None — already built | Same-origin deployment (proxy `/api` through the frontend) or cross-site cookies; CSRF middleware on both sides; every mutating endpoint's test needs a CSRF-token fixture |
| Logout / revocation | `token_version` bump, already built, unchanged | Same mechanism still works |
| Multiple tabs | Works today (shared `localStorage`) | Works (shared cookie jar) |
| SSR | N/A — no SSR reads the token today | Would need the cookie forwarded to any SSR fetch |
| Mobile/other clients | Any client can send a bearer header | Cookie-based auth is awkward for non-browser clients |

No new information changes Pass 1's call: this is an auth-contract change
touching every endpoint and every client, not something to fold into a
review pass. Mitigations already in place (12h token life, strict URL
scheme validation on every user-writable field, CSP blocking script
injection from non-self origins) remain the actual controls. Restated
here as a re-confirmed, not re-guessed, recommendation.

---

# Pass 3 — blocker remediation

## FIXED (code)

### B-1 · Next.js 14.2.35 → 16.3.4 — RESOLVED
`npm audit --omit=dev --audit-level=high` now reports **0 vulnerabilities**
(was 1 HIGH covering 21 advisories: RSC DoS, cache poisoning, request
smuggling in rewrites, SSRF via WebSocket upgrades, App Router XSS).

Pre-migration inspection found the surface unusually small: **all 14 pages
are client components** using `useParams()`, so Next 15's async
`params`/`searchParams` change does not apply; there is no middleware, no
server-side `fetch`, no `next/image`, `next/script` or `next/font`, no
custom webpack, and no deprecated APIs (`next/router`, `getServerSideProps`,
`getInitialProps`) anywhere.

Changes made:

| Package | From | To | Reason |
|---|---|---|---|
| `next` | 14.2.35 | 16.3.4 | the advisories |
| `eslint-config-next` | 14.2.35 | 16.3.4 | must match Next |
| `eslint` | ^8 | ^9.39.0 | `eslint-config-next@16` requires ≥9 |

**React was deliberately left at 18.3.1.** `next@16.3.4` declares
`react: "^18.2.0 || ^19.0.0"`, so React 19 is not required, and the brief
asked for the minimum change needed for compatibility and security.
Verified: build, typecheck, lint and full route generation all pass on
React 18.

Two config migrations were forced by Next 16:
* `next lint` was removed → the `lint` script now invokes the ESLint CLI.
* ESLint 9 no longer reads `.eslintrc.json` → replaced with
  `eslint.config.mjs`. `eslint-config-next@16` ships native flat-config
  arrays, so no `FlatCompat` shim was needed. Rule scope deliberately
  matches the previous `.eslintrc.json` (`core-web-vitals` only) — adding
  `eslint-config-next/typescript` would newly enable the full
  `@typescript-eslint` ruleset and surface 34 pre-existing
  `no-explicit-any` findings, which is scope creep during a migration.
  Tracked as a follow-up below.
* A `typecheck` script (`tsc --noEmit`) was added; the project had none.

### Bugs the migration surfaced — fixed, not suppressed

Next 16 enables the React Compiler ESLint rules, which flagged 8 errors in
pre-existing code. **All were fixed properly. No `@ts-ignore`, no
`eslint-disable`, no rule downgrades, no relaxed CSP.** Two were genuine
defects:

* **`react-hooks/immutability` — real bug.** `reportViolation()` in the
  exam page performed side effects *inside* a `setViolations` state
  updater: it posted the warning toast, started a `setTimeout`, and called
  `handleSubmit()` on the fifth violation. State updaters must be pure —
  React may invoke them twice under StrictMode or concurrent rendering,
  which could have **double-submitted the exam**. The count now lives in a
  ref and the side effects run outside the updater. A pre-existing
  `// eslint-disable-line` on that hook was removed rather than kept.

* **`react-hooks/preserve-manual-memoization` + TDZ — real bug.**
  `startTimer` referenced `handleSubmit`, a `const useCallback` declared 43
  lines later. `const` is not hoisted, so this sat in the temporal dead
  zone. It now goes through a ref synced after `handleSubmit` exists, which
  also stops the timer firing a stale closure.

* **`react-hooks/set-state-in-effect` ×6** — the "set loading, then async
  load" pattern in the challenges, community, exam, chat and payment-poll
  flows. Rewritten using React's documented render-phase state adjustment
  and awaited effects so state writes follow an await boundary.

`tsc --noEmit` then caught a real regression in that refactor (a removed
`load` function still referenced by two modal callbacks), which was fixed
by restoring it as a `useCallback` — a good argument for the typecheck
script now existing.

### Security regression after migration — all intact
CSP unchanged and not weakened (`default-src 'self'`, `object-src 'none'`,
`base-uri 'self'`, `form-action 'self'`, `frame-ancestors 'none'`, no
`unsafe-eval` in the production build); all 6 frontend security headers
still emitted by `next.config.js` under Next 16; `x-powered-by` absent;
Prism still 1.30.0 and still the only `dangerouslySetInnerHTML` sink; all
14 routes reachable.

## MANUAL INFRASTRUCTURE ACTION REQUIRED

B-2 (TLS/topology), B-3 (secrets + OpenAI key rotation), B-4 (monitoring)
and B-5 (backup/restore) are **not fixed**. They cannot be fixed in
application code. The full specification — topology diagram, trusted-proxy
matrix, least-privilege SQL, backup retention/encryption/restore-test
procedure, and an alert table with per-platform integration points — is in
**[DEPLOYMENT.md](DEPLOYMENT.md)**, written as an unchecked checklist.

Where code supports these, it fails safe rather than degrading silently —
production refuses to boot without `REDIS_URL`, with an unreachable Redis,
with a default/short/low-entropy `SECRET_KEY`, with dev database
credentials, with an `http://` frontend origin, or with a trusted-proxy
count but no proxy allowlist. All nine of those refusals were verified by
attempting each boot. **Support is not provisioning.**

## Follow-ups (not blockers)

* Enable `eslint-config-next/typescript` and clear the 34 pre-existing
  `@typescript-eslint/no-explicit-any` / unused-import findings.
* Consider React 19 once Next 16 is bedded in; not required by Next 16.

---

# Pass 2 — production-stack gate

Companion to [SECURITY.md](SECURITY.md). The first pass fixed
application-level findings. This pass re-verified every CRITICAL/HIGH/
MEDIUM item and every launch blocker against a **production-configured
stack** — `APP_ENV=production`, gunicorn `-w 4`, a real Redis — rather
than only against the test suite.

Doing that found **six defects in the first pass's own work**, five of
them in the fixes themselves. All are fixed except the one recorded as a
blocker.

---

## Defects found in the first pass

### G-1 (HIGH, fixed) · X-Forwarded-For read from the attacker-controlled position

`client_key` trusted `X-Forwarded-For` whenever `APP_ENV=production`, and
took the **left-most** entry. Proxies APPEND, so the left-most value is
the one the *client* sent; the comment in that file claiming it was "the
entry that proxy appended" was simply wrong.

Verified empirically — one host rotating the header produced four
distinct rate-limit buckets:

```
XFF=1.1.1.1 -> bucket=1.1.1.1      distinct buckets from ONE attacker: 4
XFF=2.2.2.2 -> bucket=2.2.2.2      RESULT: SPOOFABLE
```

Because `login_guard` keys on `(email, ip)`, this defeated the per-IP
login rate limit **and** the per-account lockout simultaneously. There is
also no reverse proxy anywhere in this repository, so trusting the header
at all was unfounded.

**Fixed.** `TRUSTED_PROXY_COUNT` (default **0** — ignore the header
entirely) plus `TRUSTED_PROXY_IPS`. The header is consulted only when the
count is set *and* the TCP peer is inside the allowlist, and then read at
index `-N` from the right, where every attacker-supplied entry sits to
the left of what we read. Production refuses to boot with a proxy count
but no allowlist.

**Tests:** `test_xff_is_ignored_when_no_trusted_proxy_is_configured`,
`test_xff_client_supplied_entries_are_ignored_behind_a_trusted_proxy`,
`test_xff_is_ignored_when_the_peer_is_not_a_trusted_proxy`,
`test_production_refuses_to_start_with_proxy_count_but_no_proxy_allowlist`.

### G-2 (HIGH, fixed) · Production silently fell back to in-memory rate limiting

`storage_uri=settings.REDIS_URL or "memory://"` meant a production deploy
with no Redis started happily on per-process counters — with `-w 4`, every
documented limit admitting 4x. The first pass listed this as an
infrastructure to-do, which is not sufficient: nothing prevented the
misconfiguration.

**Fixed.** `REDIS_URL` is required in production (startup aborts without
it) and `verify_storage_reachable()` probes the backend at import.
**Test:** `test_production_refuses_to_start_without_redis`.

### G-3 (MEDIUM, fixed) · The Redis health probe did not detect a dead Redis

`verify_storage_reachable()` only caught exceptions, but `limits`'
`Storage.check()` signals failure by **returning False**. Verified: the
app booted cleanly against `redis://no-such-host` and printed `BOOTED OK`.

**Fixed.** A falsy return and an exception both abort startup. Re-verified
against an unresolvable host and a dead port — both now refuse to start;
a healthy Redis boots.

### G-4 (MEDIUM, fixed) · Account lockout was per-worker, and could never expire

`login_guard` used a process-local dict, so with four workers the
configured threshold of 8 admitted up to 32, and state reset on every
deploy.

Moving it to the shared backend surfaced two further bugs, both found by
testing rather than by reading the code:

* `get_expiry()` returns the **current time** on RedisStorage, so the
  lock computed as "0 seconds remaining" and never engaged at all.
* Raw `Storage.incr()` sets **no TTL**, so a lockout once engaged would
  have been permanent (`redis-cli TTL` → `-1`).

**Fixed.** Rewritten on `limits`' `FixedWindowRateLimiter`, the same
primitive slowapi uses, which handles expiry consistently across
backends. Verified end-to-end on the 4-worker stack: the lockout engages
at exactly 8 and the key carries an 899s TTL.

**Tests:** `test_login_lockout_state_lives_in_the_shared_rate_limit_backend`,
`test_login_lockout_expires_rather_than_being_permanent`,
`test_login_lockout_counts_up_to_the_configured_threshold`.

### G-5 (HIGH, partially fixed) · Frontend dependencies were never audited

The first pass added `pip-audit` to CI for the backend but no equivalent
for the frontend, and never ran `npm audit`. It reported "dependencies
audited" on that basis, which was only half true.

Running it found **8 vulnerable runtime packages, 5 of them HIGH**. Fixed
by same-major upgrades and `overrides`:

| Package | Was | Now | Issue |
|---|---|---|---|
| `axios` | 1.7.2 | 1.20.0 | prototype pollution, `NO_PROXY` bypass, `maxBodyLength` bypass |
| `prismjs` | 1.29.0 | 1.30.0 | DOM clobbering — directly relevant: Prism's output is the one value passed to `dangerouslySetInnerHTML` |
| `form-data` | 4.0.x | 4.0.6 | CRLF injection via unescaped multipart field names |
| `nanoid` | ≤3.3.17 | 3.3.18 | infinite loop on non-secure generators |
| `postcss` | 8.x | 8.5.28 | path traversal / arbitrary `.map` disclosure |

`npm audit --omit=dev --audit-level=high` now runs in CI.

**Remaining: `next` 14.2.35 — see the blocker below.**

### G-6 (MEDIUM, fixed) · The password policy broke signup, and the error was unreadable

Reported as a live bug during this pass. Registration returned 422 for
passwords the form itself invited: the backend minimum moved 8 → 10 while
`register/page.tsx` still read `placeholder="Min. 8 characters"` and
`minLength={8}`.

Compounding it, `getErrorMessage()` did not handle FastAPI's 422 shape
(`detail` is an **array** of field errors), so the user saw axios's
`"Request failed with status code 422"` with no indication of what to
change. The running frontend container had also never been rebuilt after
the first pass, so it was serving a stale bundle against a stricter API.

**Fixed.** The form states and enforces 10–72 characters;
`getErrorMessage()` renders field-level validation errors
(`"Password: String should have at least 10 characters"`) and gives
specific text for 401 / 429 / network failure; both containers rebuilt.

Existing accounts are unaffected — login applies no strength check, so
only new registrations and password resets see the new minimum.

---

## Re-verification of the first pass

Endpoint inventory taken from the OpenAPI schema, which is authoritative
about which operations require the bearer scheme:

```
87 endpoints | 72 require authentication | 15 public | 4 admin-only
0 endpoints unauthenticated outside the reviewed public allowlist
0 inline role-string comparisons (all 4 admin routes on require_admin)
```

Live results, `APP_ENV=production` + gunicorn `-w 4` + Redis:

| Area | Result |
|---|---|
| AuthN | garbage / tampered / `alg=none` / malformed-`sub` tokens → 401, never 500 |
| Revocation | `logout-all` invalidates the issued token; fresh login then works |
| AuthZ vertical | all 4 admin routes → 403 for a student, 200 for an admin |
| Mass assignment | `role` / `is_verified` / `token_version` / `score` in the body ignored |
| AuthZ horizontal | mentor session, exam attempt/result, payment status, progress, wallet, post edit/delete → 404/403 across users |
| Exams | unpaid → 402, pending payment → 402, confirmed → 200; answer key absent from the session; cross-user submit/result/violation → 404; client-claimed 86000s stored as server-computed 18s; resubmit → 400 |
| Completion | foreign lesson id → 400, unknown lesson → 400, unknown topic → 404, negative/absurd minutes → 422, smuggled `user_id`/`status` ignored |
| Quiz | answer key absent from both `/tracks/{slug}` and `/tracks/topics/{id}` |
| XSS | 6 unsafe-scheme variants × 3 fields = 18/18 → 422; https still accepted |
| Prod config | `/docs`, `/redoc`, `/openapi.json` → 404; health minimal; all 8 headers incl. HSTS; evil origin and `*` not reflected; localhost not allowed; errors carry no internals; DB port unpublished in the prod compose file |
| Rate limiting | 10/min login limit shared across 4 workers; lockout at 8 with a bounded TTL |

**XSS sink audit.** The only `dangerouslySetInnerHTML` is Prism's escaped
output. `react-markdown` 9.1.0 is used with no `rehype-raw`, and its
default `urlTransform` maps `javascript:` and `data:text/html` to `""`
(verified by calling it directly). The remaining dynamic `href`s are a
hardcoded nav constant and `starter_repo_url`, which is now also passed
through `safeUrl()`.

**Secrets.** No `.env` has ever been committed on any branch (verified
with `git log --all --diff-filter=A`). The only secret-shaped literal in
the tree is lesson prose teaching readers *not* to hardcode keys. The
only `NEXT_PUBLIC_*` value is the API URL. A scan of all 1640 built
bundle files for `sk-`, `PAYMOB`, `RESEND`, `SECRET_KEY`,
`postgresql://` and the provider key names found nothing.

---

## Verification commands

```
backend    149 passed  (42 original + 107 security tests)
           alembic upgrade head — clean chain through 004
           pip-audit --strict — no known vulnerabilities
frontend   next lint — 0 errors
           next build — compiled, types valid
           npm audit --omit=dev — 1 HIGH remaining (next, see blocker)
runtime    production stack: gunicorn -w 4 + Redis + Postgres,
           full attack battery per the table above
```

---

# Launch promotion (added 2026-09-06)

Not a security finding — a product change, recorded here because it
touches the credit paywall and therefore had to be built so it cannot
become an authorization bypass.

**Behaviour.** Accounts created before `LAUNCH_PROMO_UNTIL` receive
`LAUNCH_PROMO_CREDITS` (default 500) instead of the usual 10. Unspent
promo credits are withdrawn `LAUNCH_PROMO_DAYS` (default 30) after that
user signed up. Spending draws promo credits down first, so expiry can
never remove credits a user paid for.

**Deliberately unaffected: the certification exam paywall.** Exams are a
separate EGP-only charge enforced by `exam_controller._require_paid_exam`
and never consumed credits. `test_promo_does_not_unlock_paid_exams`
pins that.

**Security properties, each covered by a test**

| Property | Why it matters |
|---|---|
| Amount, eligibility and expiry are server-decided | No request field influences the grant; a signup body carrying `credit_balance` / `promo_credits_remaining` is ignored |
| Promo columns absent from every request schema | A `PATCH /auth/me` naming them cannot extend a user's own promo |
| Blank or malformed `LAUNCH_PROMO_UNTIL` disables the promo | A typo'd date fails closed instead of granting free credits forever |
| Expiry is enforced at spend time, inside the wallet row lock | An expired balance is not merely hidden — the AI action is refused with 402 |
| Expiry only removes *unspent* promo credits | Purchased credits survive |
| Every balance change writes a ledger row | Promo expiry appears as a `expiry` transaction, not a silent adjustment |

The expiry sweep is lazy — it runs whenever a wallet is touched — so
there is no cron to forget and no window in which stale credits are
spendable.

**Abuse note (open).** Free credits per signup means one person can farm
them by registering repeatedly. The only control today is the 5/minute
registration rate limit. Options discussed but not implemented: gating
the promo on a verified email (needs `RESEND_API_KEY`, currently unset,
so verification mail never sends), or a daily per-user AI cap. Self-
hosting inference via `OPENAI_API_URL` changes the calculus — the cost
becomes your own hardware rather than per-token vendor spend.
