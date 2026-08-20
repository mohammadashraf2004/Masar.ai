"""
backend/app/services/payments/paymob_service.py

Thin client for Paymob's Accept API (the dominant Egyptian payment
gateway — cards + mobile wallets via one integration).
Docs: https://docs.paymob.com/docs/accept-standard-redirect
      https://docs.paymob.com/docs/mobile-wallets
      https://docs.paymob.com/docs/transaction-callbacks (HMAC)

Flow used here:
  1. authenticate()          -> short-lived auth token
  2. create_order()          -> paymob order id (correlated to us via
                                 merchant_order_id, which WE generate)
  3. request_payment_key()   -> a payment_token scoped to one order+amount
  4a. card_iframe_url()      -> iframe URL for card checkout
  4b. pay_with_wallet()      -> redirect_url for mobile wallet checkout
                                 (customer approves via OTP on their phone)
  5. verify_webhook_hmac()   -> the ONLY thing that should ever mark a
                                 payment as confirmed and release credits/
                                 access. Card/wallet checkout completion is
                                 asynchronous and must never be trusted from
                                 the browser redirect alone.
"""
import hashlib
import hmac as hmac_lib
from typing import Literal

import httpx

from app.core.config import settings


class PaymobConfigError(RuntimeError):
    """Raised when Paymob credentials aren't configured for the requested
    operation. Callers should turn this into a clean 503, not a 500."""


def _require(*names: str) -> None:
    missing = [n for n in names if not getattr(settings, n, None)]
    if missing:
        raise PaymobConfigError(
            f"Paymob is not configured — missing: {', '.join(missing)}. "
            "Set these env vars before accepting real payments."
        )


def authenticate() -> str:
    _require("PAYMOB_API_KEY")
    resp = httpx.post(
        f"{settings.PAYMOB_BASE_URL}/auth/tokens",
        json={"api_key": settings.PAYMOB_API_KEY},
        timeout=15,
    )
    resp.raise_for_status()
    return resp.json()["token"]


def create_order(auth_token: str, amount_cents: int, merchant_order_id: str) -> int:
    resp = httpx.post(
        f"{settings.PAYMOB_BASE_URL}/ecommerce/orders",
        json={
            "auth_token": auth_token,
            "delivery_needed": False,
            "amount_cents": amount_cents,
            "currency": "EGP",
            "merchant_order_id": merchant_order_id,
            "items": [],
        },
        timeout=15,
    )
    resp.raise_for_status()
    return resp.json()["id"]


def request_payment_key(
    auth_token: str,
    order_id: int,
    amount_cents: int,
    integration_id: str,
    billing_data: dict,
) -> str:
    resp = httpx.post(
        f"{settings.PAYMOB_BASE_URL}/acceptance/payment_keys",
        json={
            "auth_token": auth_token,
            "amount_cents": amount_cents,
            "expiration": 3600,
            "order_id": order_id,
            "billing_data": billing_data,
            "currency": "EGP",
            "integration_id": integration_id,
        },
        timeout=15,
    )
    resp.raise_for_status()
    return resp.json()["token"]


def card_iframe_url(payment_token: str) -> str:
    _require("PAYMOB_IFRAME_ID")
    return f"https://accept.paymob.com/api/acceptance/iframes/{settings.PAYMOB_IFRAME_ID}?payment_token={payment_token}"


def pay_with_wallet(payment_token: str, phone_number: str) -> str:
    """Charges via mobile wallet (Vodafone Cash / Etisalat Cash / Orange
    Money — Paymob routes by the phone number's carrier). Returns a
    redirect_url the customer completes payment at via an OTP prompt on
    their phone — not an iframe."""
    resp = httpx.post(
        f"{settings.PAYMOB_BASE_URL}/acceptance/payments/pay",
        json={
            "source": {"identifier": phone_number, "subtype": "WALLET"},
            "payment_token": payment_token,
        },
        timeout=15,
    )
    resp.raise_for_status()
    data = resp.json()
    return data.get("redirect_url") or data["iframe_redirection_url"]


_DEFAULT_BILLING = {
    "apartment": "NA", "floor": "NA", "street": "NA", "building": "NA",
    "shipping_method": "NA", "postal_code": "NA", "city": "NA",
    "country": "EG", "state": "NA",
}


def init_payment(
    amount_egp: float,
    merchant_order_id: str,
    method: Literal["card", "wallet"],
    full_name: str,
    email: str,
    phone_number: str,
) -> dict:
    """High-level entry point used by the controller.
    Returns {"checkout_url": ..., "paymob_order_id": ...}."""
    integration_id = (
        settings.PAYMOB_INTEGRATION_ID_CARD if method == "card"
        else settings.PAYMOB_INTEGRATION_ID_WALLET
    )
    if not integration_id:
        raise PaymobConfigError(f"No Paymob integration id configured for method={method}")

    amount_cents = round(amount_egp * 100)
    first, _, last = full_name.partition(" ")
    billing = {
        **_DEFAULT_BILLING,
        "first_name": first or full_name,
        "last_name": last or "NA",
        "email": email,
        "phone_number": phone_number,
    }

    token = authenticate()
    order_id = create_order(token, amount_cents, merchant_order_id)
    payment_token = request_payment_key(token, order_id, amount_cents, integration_id, billing)

    checkout_url = (
        card_iframe_url(payment_token) if method == "card"
        else pay_with_wallet(payment_token, phone_number)
    )
    return {"checkout_url": checkout_url, "paymob_order_id": order_id}


# ─── Webhook HMAC verification ──────────────────────────────────────────────
# Paymob's documented field order for the "Transaction Processed Callback".
# Concatenating in any other order produces a different digest — this order
# is not arbitrary, it's exactly what Paymob computes on their side.
_HMAC_FIELDS = [
    "amount_cents", "created_at", "currency", "error_occured",
    "has_parent_transaction", "id", "integration_id", "is_3d_secure",
    "is_auth", "is_capture", "is_refunded", "is_standalone_payment",
    "is_voided", "order", "owner", "pending",
    "source_data.pan", "source_data.sub_type", "source_data.type", "success",
]


def _extract(obj: dict, key: str):
    if key == "order":
        return obj.get("order", {}).get("id")
    if "." in key:
        parent, child = key.split(".")
        return obj.get(parent, {}).get(child)
    return obj.get(key)


def _stringify(value) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if value is None:
        return "None"
    return str(value)


def verify_webhook_hmac(transaction_obj: dict, received_hmac: str) -> bool:
    """`transaction_obj` is the `obj` field of Paymob's webhook payload.
    Returns False (never raises) on any malformed input — a webhook that
    fails verification should be rejected, not crash the endpoint."""
    if not settings.PAYMOB_HMAC_SECRET or not received_hmac:
        return False
    try:
        concatenated = "".join(_stringify(_extract(transaction_obj, f)) for f in _HMAC_FIELDS)
    except (TypeError, AttributeError):
        return False
    computed = hmac_lib.new(
        settings.PAYMOB_HMAC_SECRET.encode(), concatenated.encode(), hashlib.sha512
    ).hexdigest()
    return hmac_lib.compare_digest(computed, received_hmac)
