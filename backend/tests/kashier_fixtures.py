"""
A stand-in for Kashier in tests: no network, no real keys.

`kashier` (fixture) configures test-mode settings, replaces session creation and
the server-side session lookup, and signs webhooks the way Kashier documents it
(https://developers.kashier.io/docs/webhooks) - computed here independently of
kashier_service, so a mistake there cannot also hide here.
"""
import hashlib
import hmac as hmac_lib
import itertools
from urllib.parse import quote

import httpx
import pytest

from app.core.config import settings
from app.services.payments import kashier_service

API_KEY = "kashier-test-payment-api-key"
SECRET_KEY = "kashier-test-secret-key"
_ids = itertools.count(1)


def sign(data: dict, key: str = API_KEY) -> str:
    keys = sorted(data["signatureKeys"])
    payload = "&".join(f"{k}={quote(str(data[k]), safe='')}" for k in keys)
    return hmac_lib.new(key.encode(), payload.encode(), hashlib.sha256).hexdigest()


class FakeKashier:
    def __init__(self):
        self.sessions: dict[str, dict] = {}      # session id -> what create_session was asked
        self.lookups: dict[str, dict] = {}       # session id -> what get_session_payment answers
        self.documents: dict[str, dict] = {}     # session id -> what get_session answers
        self.lookup_fails = False
        self.create_fails: Exception | None = None

    # -- the two calls Masar makes ------------------------------------------------
    def create_session(self, **kwargs):
        if self.create_fails is not None:
            raise self.create_fails
        session_id = f"sess-{next(_ids):06d}"
        self.sessions[session_id] = kwargs
        return {"session_id": session_id, "checkout_url": f"https://checkout.kashier.test/{session_id}"}

    def get_session_payment(self, session_id):
        if self.lookup_fails:
            raise httpx.ConnectError("kashier unreachable")
        if session_id not in self.lookups:
            raise httpx.HTTPStatusError("404", request=httpx.Request("GET", "https://x"),
                                        response=httpx.Response(404))
        return self.lookups[session_id]

    def get_session(self, session_id):
        if self.lookup_fails:
            raise httpx.ConnectError("kashier unreachable")
        if session_id not in self.documents:
            raise httpx.HTTPStatusError("404", request=httpx.Request("GET", "https://x"),
                                        response=httpx.Response(404))
        return self.documents[session_id]

    # -- test helpers -------------------------------------------------------------
    def session_of(self, merchant_order_id: str) -> str:
        return next(sid for sid, s in self.sessions.items() if s["merchant_order_id"] == merchant_order_id)

    def record(self, session_id: str, merchant_order_id: str, amount_major: str, *, status="PAID", currency="EGP"):
        """What Kashier's own record of the session says (the authority for a payment)."""
        self.lookups[session_id] = {
            "sessionId": session_id, "status": status, "merchantOrderId": merchant_order_id,
            "amount": amount_major, "currency": currency, "orderId": f"ko-{session_id}",
        }

    def refunded(self, session_id: str, merchant_order_id: str, refunded_major: str):
        """Kashier's session document after refunds totalling `refunded_major` pounds."""
        self.documents[session_id] = {
            "_id": session_id, "status": "PAID", "refundedAmount": refunded_major,
            "paymentParams": {"order": merchant_order_id, "currency": "EGP"},
        }

    @staticmethod
    def data(merchant_order_id, amount_major, *, status="SUCCESS", transaction_id=None, currency="EGP",
             signed=("amount", "currency", "merchantOrderId", "status", "transactionId", "kashierOrderId")):
        data = {
            "amount": amount_major, "currency": currency, "merchantOrderId": merchant_order_id,
            "status": status, "transactionId": transaction_id or f"TX-{next(_ids):09d}",
            "kashierOrderId": f"ko-{merchant_order_id}", "method": "card", "channel": "online | e-commerce",
            "transactionResponseCode": "00",
        }
        data["signatureKeys"] = list(signed)
        return data

    def post(self, client, data, *, event="pay", signature=None):
        return client.post(
            "/api/v1/payments/kashier/webhook",
            json={"event": event, "data": data},
            headers={"x-kashier-signature": signature if signature is not None else sign(data)},
        )


@pytest.fixture()
def kashier(monkeypatch):
    for name, value in (("KASHIER_MODE", "test"), ("KASHIER_MERCHANT_ID", "MID-TEST-1"),
                        ("KASHIER_API_KEY", API_KEY), ("KASHIER_SECRET_KEY", SECRET_KEY),
                        ("KASHIER_PUBLIC_API_URL", "https://api.masar.test"), ("PAYMENTS_ENABLED", True)):
        monkeypatch.setattr(settings, name, value)
    fake = FakeKashier()
    monkeypatch.setattr(kashier_service, "create_session", fake.create_session)
    monkeypatch.setattr(kashier_service, "get_session_payment", fake.get_session_payment)
    monkeypatch.setattr(kashier_service, "get_session", fake.get_session)
    return fake
