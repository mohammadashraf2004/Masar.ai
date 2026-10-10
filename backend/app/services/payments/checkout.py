"""Start a payment: the one place a checkout is opened, for every kind of order.

New payments go to Kashier only (a hosted payment session). Paymob is never
initiated any more; its webhook remains to reconcile the orders it already took.
"""
import logging

import httpx
from fastapi import HTTPException

from app.core.config import settings
from app.services.payments import kashier_service

logger = logging.getLogger("app.payments")

PROVIDER = "kashier"


def require_payments_open() -> None:
    """Refuse before anything is written: a closed checkout must not leave orders behind.

    Used as a route dependency on every endpoint that opens a payment, and again inside
    ``start_checkout`` so no caller can reach the provider while payments are closed."""
    if not settings.payments_open:
        raise HTTPException(status_code=503, detail={
            "code": "PAYMENTS_UNAVAILABLE",
            "message": "Online payments are temporarily unavailable.",
            "message_ar": "الدفع الإلكتروني غير متاح مؤقتًا.",
        })


def language_of(request) -> str:
    accept = (request.headers.get("accept-language") or "") if request is not None else ""
    return "ar" if accept.lower().startswith("ar") else "en"


def start_checkout(*, kind: str, amount_minor: int, currency: str, merchant_order_id: str, user,
                   description: str, language: str = "en") -> dict:
    """Open the hosted checkout. Returns {"provider", "provider_order_id", "checkout_url"}:
    the caller stores `provider_order_id` on its order - it is what binds the
    provider's later webhook to that row. Raises HTTPException 503 (payments not
    configured) or 502 (provider refused or unreachable); the caller marks its
    order failed so it does not block the next attempt."""
    require_payments_open()
    try:
        session = kashier_service.create_session(
            amount_minor=amount_minor, currency=currency, merchant_order_id=merchant_order_id,
            description=description, customer_email=user.email, customer_reference=str(user.id),
            language=language, kind=kind,
        )
    except kashier_service.KashierConfigError as exc:
        raise HTTPException(status_code=503, detail=str(exc))
    except httpx.HTTPStatusError as exc:
        # The upstream body can echo request details; it belongs in our logs only.
        logger.warning("payments.checkout.rejected", extra={"kind": kind, "status": exc.response.status_code})
        raise HTTPException(status_code=502, detail="The payment provider rejected this request.")
    except httpx.HTTPError:
        raise HTTPException(status_code=502, detail="Could not reach the payment provider. Please try again.")
    return {"provider": PROVIDER, "provider_order_id": session["session_id"], "checkout_url": session["checkout_url"]}
