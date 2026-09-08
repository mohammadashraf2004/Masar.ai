# Pre-launch security gate

Two passes are recorded here. Pass 2 audited the first remediation. Pass 3
(below) executed the Next.js migration and produced the infrastructure
specification in [DEPLOYMENT.md](DEPLOYMENT.md).

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
