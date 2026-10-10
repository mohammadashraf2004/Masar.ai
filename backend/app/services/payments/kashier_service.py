"""
Kashier: hosted payment sessions, webhook signatures and server-side confirmation.

Docs (verified 2026-10-08):
  https://developers.kashier.io/docs/accept-payments/payment-sessions
  https://developers.kashier.io/docs/webhooks           (x-kashier-signature)
  https://developers.kashier.io/openapi.yaml            (session payment lookup)

Flow:
  1. create_session()          -> POST /v3/payment/sessions; the shopper pays on
                                  the returned `sessionUrl` (Kashier-hosted).
  2. Kashier POSTs the webhook  -> verify_signature() over data.signatureKeys,
                                  HMAC-SHA256 with the Payment API key.
  3. get_session_payment()     -> GET /v3/payment/sessions/{id}/payment with the
                                  secret key: the authority for a payment's status,
                                  merchant order, amount and currency. A webhook or
                                  a browser redirect alone never grants anything.

Amounts: sessions take a decimal string in pounds ("299.00"); the session lookup
returns one too. Masar stores piasters (integer minor units).

SANDBOX-UNVERIFIED (2026-10-08): the webhook's `data.amount` unit is not
documented (examples show 1 and 11334 EGP). It is read as pounds. A payment is
settled on the server-side lookup's amount, never the webhook's, so a wrong
reading cannot grant. A refund is applied only when the session document already
shows at least that much refunded for this order (its amounts are pounds, like
the session's own `amount`); a webhook amount read in the wrong unit then fails
that check and the refund waits (503, Kashier retries) instead of ending access -
staff reconcile it from the Kashier dashboard. The session document's
`refundedAmount` unit is itself an assumption to confirm in the sandbox.
"""
import hashlib
import hmac as hmac_lib
from datetime import datetime, timedelta, timezone
from decimal import Decimal, InvalidOperation
from typing import Optional
from urllib.parse import quote

import httpx

from app.core.config import settings
from app.services.payments.notice import PaymentNotice

# SANDBOX-UNVERIFIED (2026-10-08): the docs list session statuses only as
# "PENDING, OPENED, PAID, etc."; CAPTURED is a guess for a captured card payment.
# A paid session reported under any other name is never settled - the webhook
# answers 503 and Kashier retries - so a wrong guess delays, it never over-grants.
# Confirm against a real test-mode payment before taking money.
PAID_SESSION_STATUSES = {"PAID", "CAPTURED"}
_REVERSALS = {"refund", "partial_refund", "void", "reversal"}


class KashierConfigError(RuntimeError):
    pass


class PaymentNotConfirmed(RuntimeError):
    """The webhook reports success but Kashier's own record does not (yet) show
    the session paid: settle nothing and let Kashier retry the webhook."""


def _api_base() -> str:
    return "https://api.kashier.io" if settings.KASHIER_MODE == "live" else "https://test-api.kashier.io"


def _require_config() -> None:
    if not settings.kashier_configured:
        raise KashierConfigError("Payments are not configured (KASHIER_* settings).")
    if settings.KASHIER_MODE not in {"test", "live"}:
        raise KashierConfigError("KASHIER_MODE must be test or live.")


def minor_to_major(amount_minor: int) -> str:
    if not isinstance(amount_minor, int) or isinstance(amount_minor, bool) or amount_minor <= 0:
        raise ValueError("amount must be a positive integer number of piasters")
    return f"{Decimal(amount_minor) / 100:.2f}"


def major_to_minor(value) -> int:
    """Pounds (string or number) -> piasters; -1 when unreadable or fractional below a piaster."""
    try:
        amount = Decimal(str(value)) * 100
    except (InvalidOperation, ValueError, TypeError):
        return -1
    return int(amount) if amount == amount.to_integral_value() and amount >= 0 else -1


def public_url(path: str) -> str:
    return f"{(settings.KASHIER_PUBLIC_API_URL or '').rstrip('/')}{path}"


def create_session(
    *, amount_minor: int, currency: str, merchant_order_id: str, description: str,
    customer_email: str, customer_reference: str, language: str = "en", kind: str,
) -> dict:
    """Open a Kashier-hosted checkout for one order. Returns {"session_id", "checkout_url"}."""
    _require_config()
    if currency != "EGP":
        raise ValueError("Only EGP payments are supported")
    expire_at = datetime.now(timezone.utc) + timedelta(minutes=settings.KASHIER_SESSION_MINUTES)
    body = {
        "expireAt": expire_at.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
        "maxFailureAttempts": 3,
        "paymentType": "credit",
        "amount": minor_to_major(amount_minor),
        "currency": currency,
        "order": merchant_order_id,
        "merchantRedirect": public_url(f"/api/v1/payments/kashier/return?ref={quote(merchant_order_id, safe='')}"),
        "display": "ar" if language == "ar" else "en",
        "type": "one-time",
        "allowedMethods": settings.KASHIER_ALLOWED_METHODS,
        "failureRedirect": True,
        "merchantId": settings.KASHIER_MERCHANT_ID,
        "serverWebhook": public_url("/api/v1/payments/kashier/webhook"),
        "enable3DS": True,
        "manualCapture": False,
        "interactionSource": "ECOMMERCE",
        "description": description[:120],
        "customer": {"email": customer_email, "reference": customer_reference},
        "metaData": {"kind": kind, "merchantOrderId": merchant_order_id},
    }
    response = httpx.post(
        f"{_api_base()}/v3/payment/sessions", json=body, timeout=settings.KASHIER_TIMEOUT_SECONDS,
        headers={"Authorization": settings.KASHIER_SECRET_KEY, "api-key": settings.KASHIER_API_KEY,
                 "Content-Type": "application/json"},
    )
    response.raise_for_status()
    data = response.json()
    session = data.get("data") if isinstance(data.get("data"), dict) else data
    session_id, url = session.get("_id"), session.get("sessionUrl")
    if not session_id or not url:
        raise KashierConfigError("Kashier returned no session id or URL.")
    return {"session_id": str(session_id), "checkout_url": str(url)}


def get_session_payment(session_id: str) -> dict:
    """The session's current payment, straight from Kashier (secret-key authenticated)."""
    _require_config()
    response = httpx.get(
        f"{_api_base()}/v3/payment/sessions/{quote(session_id, safe='')}/payment",
        headers={"Authorization": settings.KASHIER_SECRET_KEY}, timeout=settings.KASHIER_TIMEOUT_SECONDS,
    )
    response.raise_for_status()
    body = response.json()
    return body.get("data") if isinstance(body.get("data"), dict) else body


def get_session(session_id: str) -> dict:
    """The session document (status, order, captured and refunded amounts). The docs
    say this read takes no credential, so none is sent."""
    _require_config()
    response = httpx.get(
        f"{_api_base()}/v3/payment/sessions/{quote(session_id, safe='')}",
        timeout=settings.KASHIER_TIMEOUT_SECONDS,
    )
    response.raise_for_status()
    body = response.json()
    return body.get("data") if isinstance(body.get("data"), dict) else body


def needs_confirmation(event: str, data: dict) -> Optional[str]:
    """Which of Kashier's own records a verified webhook must be checked against before
    it may change anything: "payment" (the session's payment) for a successful payment,
    "session" (the session document) for a successful refund, void or reversal, None
    for anything that changes no access (declines, pending, authorizations)."""
    if str(data.get("status") or "").upper() != "SUCCESS":
        return None
    event = str(event or "").lower()
    if event in _REVERSALS:
        return "session"
    return None if event == "authorize" else "payment"


def _js_string(value) -> str:
    """How the `query-string` package Kashier's reference code uses renders a value."""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value)


def signature_payload(data: dict) -> str:
    """data.signatureKeys sorted, each key=value with the value URL-encoded, joined by '&'."""
    keys = sorted(str(k) for k in data.get("signatureKeys") or [])
    parts = []
    for key in keys:
        if key not in data or data[key] is None:
            continue
        parts.append(f"{key}={quote(_js_string(data[key]), safe='')}")
    return "&".join(parts)


def verify_signature(data: dict, received: str) -> bool:
    """x-kashier-signature: HMAC-SHA256 of signature_payload(data) with the Payment API key.
    Never raises; a malformed payload simply does not verify."""
    if not settings.KASHIER_API_KEY or not received or not isinstance(data, dict):
        return False
    try:
        payload = signature_payload(data)
    except (TypeError, AttributeError):
        return False
    if not payload:
        return False
    computed = hmac_lib.new(settings.KASHIER_API_KEY.encode(), payload.encode(), hashlib.sha256).hexdigest()
    return hmac_lib.compare_digest(computed, str(received).strip().lower())


SIGNED_FIELDS_REQUIRED = ("merchantOrderId", "amount", "currency", "status")


def unsigned_required_fields(data: dict) -> list[str]:
    """Fields settlement relies on that this webhook's signature does not cover."""
    signed = set(data.get("signatureKeys") or [])
    return [f for f in SIGNED_FIELDS_REQUIRED if f not in signed]


def notice_from_webhook(event: str, data: dict, *, session_id: Optional[str],
                        confirmed: Optional[dict] = None) -> PaymentNotice:
    """The provider-neutral notice for a verified webhook.

    `session_id` is the session bound to our order at checkout. `confirmed` is
    Kashier's own record, required for whatever needs_confirmation() names: for a
    payment, get_session_payment() - its status, merchant order, amount and currency
    are the ones that count; for a refund, void or reversal, get_session() - it must
    be for this order and already show at least this much refunded, so a webhook
    amount read in the wrong unit can never end someone's access."""
    status = str(data.get("status") or "").upper()
    event = str(event or "").lower()
    kind = "reversal" if event in _REVERSALS else "authorization" if event == "authorize" else "payment"
    amount = major_to_minor(data.get("amount"))
    currency = str(data.get("currency") or "").upper()
    success = status == "SUCCESS"
    pending = status == "PENDING"
    binding = session_id
    if kind == "payment" and success and not pending:
        if confirmed is None:
            raise ValueError("A Kashier payment must be confirmed server-side before it can settle")
        same_order = str(confirmed.get("merchantOrderId") or "") == str(data.get("merchantOrderId") or "")
        if not same_order:
            binding = None              # this session paid for another order: never binds
        elif str(confirmed.get("status") or "").upper() not in PAID_SESSION_STATUSES:
            raise PaymentNotConfirmed(str(confirmed.get("status") or "unknown"))
        amount = major_to_minor(confirmed.get("amount"))
        currency = str(confirmed.get("currency") or currency).upper()
    elif kind == "reversal" and success and not pending:
        if confirmed is None:
            raise ValueError("A Kashier refund must be confirmed server-side before it can apply")
        params = confirmed.get("paymentParams") if isinstance(confirmed.get("paymentParams"), dict) else {}
        if str(params.get("order") or "") != str(data.get("merchantOrderId") or ""):
            binding = None              # a refund on another order's session: never binds
        elif amount < 0 or major_to_minor(confirmed.get("refundedAmount") or 0) < amount:
            raise PaymentNotConfirmed("refund not visible in the session record")
    code = data.get("transactionResponseCode")
    return PaymentNotice(
        provider="kashier", event_id=str(data.get("transactionId") or ""),
        merchant_order_id=str(data.get("merchantOrderId") or ""), provider_order_id=binding,
        amount=amount, currency=currency, success=success, pending=pending, kind=kind,
        response_code=(str(code)[:100] if code else (event if kind != "payment" else None)),
        raw={"event": event, "data": data, "confirmed": confirmed},
    )
