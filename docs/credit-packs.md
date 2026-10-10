# Additional AI credit packs (migration 039)

Free and Pro accounts can buy extra AI credits. Prices and quantities are server-owned.

| Pack | Credits | Price (EGP, VAT included) |
|---|---:|---:|
| Starter | 50 | 29 |
| Standard | 150 | 69 |
| Plus (most popular) | 400 | 149 |
| Power | 1,000 | 299 |

They live in `credit_packages` (upserted by `code` in migration 039; the old seed's packs are switched
off, not deleted). A request carries only a package id. Changing a price is a database change, never a deploy.

## Ledger model

`user_wallets.credit_balance` is the spendable balance. `user_wallets.purchased_credits` is the part of it that
was bought (always <= balance); the rest is "included" (signup/promo credits). Purchased credits never expire,
and renewal, upgrade, downgrade, cancellation and promo expiry leave them alone.

`wallet_transactions` is the audit trail. New columns: `package_id`, `purchased_delta` (how much of the row
moved in/out of the purchased bucket), `related_tx_id` (the order a reversal answers / the deduction a refund
answers), `reversed_credits`, `settled_at`, `request_key`. Enum `transactiontype` gains `reversal`.

## Spending

* Free account: included credits first (promo first), purchased credits last.
* Pro account: the 50 credits / rolling 4 h allowance first (unchanged). Past it, **purchased credits only** pay
  for AI actions (signup/promo credits stay out of reach, as before), capped by `PURCHASED_CREDITS_DAILY_LIMIT`
  (default 500 / rolling 24 h) so this is not an unbounded way round the allowance. With none to spend: the
  existing 429 `pro_ai_limit_reached`.
* Refunds of a failed action put back what the deduction took from purchased credits into the purchased bucket.
* A retried request with the same `Idempotency-Key` is not charged twice (409) while its charge stands.
* Credit costs per action are **unchanged**. Exercise grading is not credit-dependent (as before).
* Every call site (mentor chat/v2, code review, skill gap, mock interview, roadmap, answer evaluation, challenge
  and project hints/enrolment) already goes through `deduct_credits` / `refund_credits`; both are row-locked.

## Purchase flow

1. `POST /payments/wallet/topup/init {package_id}` (auth, 10/min): creates a **pending** order from the catalogue
   price (max 3 open orders; stale ones expire after 75 min), opens a Kashier hosted session, binds its id.
2. The shopper pays on Kashier. The browser return (`/payments/kashier/return?ref=`) only redirects to
   `/billing/credits?reference=` and grants nothing.
3. Kashier's signed webhook -> signature verified -> the payment is confirmed against Kashier's own record
   (`/v3/payment/sessions/{id}/payment`) -> `settle_wallet_topup` checks provider order, EGP amount and currency
   -> `confirm_pending_topup` locks the order and the wallet and pays out once. One provider transaction settles
   at most one order (unique index). Replays, forged, mismatched, pending, declined: nothing credited.
4. The page polls `GET /payments/status/{ref}` and `GET /wallet/purchases` (server state only).

Refund / chargeback: a verified, provider-confirmed refund webhook, or `POST /wallet/admin/purchases/{ref}/reverse`
(admin, idempotency key), calls `reverse_purchase`: locks the wallet, takes back at most what is still in the
purchased bucket (never negative; the unrecovered part is recorded on the reversal row and logged), proportional
for partial refunds, idempotent on the provider/admin event id.

## Frontend

`/billing/credits` (Buy credits): balance split (purchased vs included), four cards with Plus highlighted,
summary + buy button, purchase history with statuses, return states (confirmed / confirming / failed), EN/AR+RTL.
The header credits panel's "Add credits" goes there; Plans & offers links to it; `WalletContext` now exposes the
whole wallet and `refresh()`.

## Open blockers / decisions

* **Kashier is still SANDBOX-UNVERIFIED** (see `kashier_service.py`): paid session status name, webhook amount unit,
  `refundedAmount` unit. Verify with a real test-mode payment and a real refund before enabling live payments.
* Disputes: Kashier's chargeback notification format is not documented in the integration; chargebacks are reconciled
  by staff through the admin endpoint (kind `chargeback`). Wire a webhook if Kashier provides one.
* VAT: pack prices are shown as VAT-inclusive (same as plans). Confirm with finance.
* Pro copy changed: "your wallet credits are never used" -> bought credits are kept for when the allowance runs out.
  Pro users' *signup/promo* credits are still never used.
* Production: `credit_packages` is probably empty/old there; migration 039 inserts the four packs. No balances are
  rewritten: `purchased_credits` is backfilled as `MIN(balance, lifetime_purchased)`.

## Production deployment checklist

1. Backup the database. Confirm migration head is 038, then `alembic upgrade head` (039 is additive and idempotent).
2. Check: `select code, credits, egp_price, is_popular from credit_packages where is_active order by sort_order` = 4 rows.
3. Check: `select count(*) from user_wallets where purchased_credits > credit_balance` = 0.
4. Kashier: `KASHIER_MODE=live`, all four `KASHIER_*` settings, HTTPS `KASHIER_PUBLIC_API_URL`; webhook URL registered.
5. Do a real test-mode purchase and a refund in staging; confirm credits arrive only after the webhook.
6. Frontend build with `NEXT_PUBLIC_PAYMENTS_PROVIDER=kashier`.
7. Optional: tune `PURCHASED_CREDITS_DAILY_LIMIT`.
8. Monitor `wallet.reversal.unrecovered` warnings and `security_log` payment events.
