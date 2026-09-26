# Course billing and lifetime access

Course commerce reuses Masar's existing Paymob client and the single
`POST /api/v1/payments/paymob/webhook` HMAC-verified callback. It does not have
a second gateway integration.

## Lifecycle

1. An admin creates an EGP offer through `POST /api/v1/admin/course-offers`.
   Activating an offer marks the course as paid. Existing courses remain free
   after migration until this happens.
2. `POST /api/v1/billing/checkout` resolves the active offer on the server and
   snapshots its integer minor-unit amount into a pending `billing_orders` row.
3. The shared Paymob client creates the provider order and hosted checkout.
4. The verified server webhook checks the provider order id, amount and
   currency, stores one `payment_transactions` row, marks the order paid, and
   creates exactly one lifetime `course_enrollments` row in the same database
   transaction.
5. Learning authorization reads `course_enrollments`, never Paymob state.

Order statuses are `pending`, `paid`, `failed`, `cancelled`, and `refunded`.
Only `paid` creates purchase access. Provider callbacks are idempotent through
the `(provider, provider_transaction_id)` and `(user_id, course_id)` database
constraints.

## Access rules

- A course with `courses.is_free = true` is accessible without an enrollment.
- A lesson with `lessons.is_preview = true` is readable without ownership.
- Other content in a paid course requires an active, unexpired enrollment.
- Purchases create lifetime access (`expires_at IS NULL`, source `purchase`).
- `POST /api/v1/admin/enrollments` creates an auditable `admin_grant` without a
  payment or a fake transaction.
- Locked curriculum metadata remains visible, but lesson bodies, exercises,
  quizzes, projects, progress writes, grading, submissions, and topic-scoped
  mentor context are enforced by the backend.

## Paymob configuration

No new secrets are required. Configure the existing variables:

- `PAYMOB_API_KEY`
- `PAYMOB_INTEGRATION_ID_CARD`
- `PAYMOB_INTEGRATION_ID_WALLET` (when wallet checkout is enabled)
- `PAYMOB_IFRAME_ID`
- `PAYMOB_HMAC_SECRET`
- `PAYMOB_BASE_URL` (normally the default)
- `FRONTEND_URL`

In Paymob, set the processed-transaction callback to
`https://<api-host>/api/v1/payments/paymob/webhook` and the browser response
callback to `https://<api-host>/api/v1/payments/paymob/callback`. Browser
redirect parameters never grant access; the return page polls Masar's own order
endpoint until the webhook has confirmed the order.

## Applying and testing

From `backend/`:

```text
alembic upgrade head
pytest tests/test_course_billing.py tests/test_paymob_service.py tests/test_payments_controller.py
pytest
```

From `frontend/`:

```text
npm run test
npm run lint
npm run typecheck
```

Tests require the repository's disposable PostgreSQL test database; the test
fixture intentionally refuses to run against a database whose name does not
contain `test`.
