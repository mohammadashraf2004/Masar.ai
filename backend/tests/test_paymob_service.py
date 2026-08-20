"""
Verifies app.services.payments.paymob_service against an independently
computed HMAC — not just "does it run without crashing". The field
concatenation order matters: get it wrong and every real webhook from
Paymob would be silently rejected (or worse, a forged one accepted).
"""
import hashlib
import hmac as hmac_lib

from app.services.payments import paymob_service

SECRET = "test-hmac-secret"

SAMPLE_OBJ = {
    "amount_cents": 15000,
    "created_at": "2026-08-20T10:00:00.000000",
    "currency": "EGP",
    "error_occured": False,
    "has_parent_transaction": False,
    "id": 987654321,
    "integration_id": 123456,
    "is_3d_secure": True,
    "is_auth": False,
    "is_capture": False,
    "is_refunded": False,
    "is_standalone_payment": True,
    "is_voided": False,
    "order": {"id": 555111},
    "owner": 42,
    "pending": False,
    "source_data": {"pan": "1234", "sub_type": "MasterCard", "type": "card"},
    "success": True,
}

# Independently computed per Paymob's documented field order — deliberately
# NOT calling _extract/_stringify here, to avoid the test just re-running
# the same (possibly wrong) code it's supposed to check.
_EXPECTED_CONCAT = (
    "15000" "2026-08-20T10:00:00.000000" "EGP" "false"
    "false" "987654321" "123456" "true"
    "false" "false" "false" "true"
    "false" "555111" "42" "false"
    "1234" "MasterCard" "card" "true"
)


def _sign(secret: str, concatenated: str) -> str:
    return hmac_lib.new(secret.encode(), concatenated.encode(), hashlib.sha512).hexdigest()


def test_hmac_field_order_matches_paymob_docs():
    # If this fails, _HMAC_FIELDS / _extract in paymob_service.py has
    # drifted from Paymob's documented concatenation order.
    concatenated = "".join(
        paymob_service._stringify(paymob_service._extract(SAMPLE_OBJ, f))
        for f in paymob_service._HMAC_FIELDS
    )
    assert concatenated == _EXPECTED_CONCAT


def test_verify_webhook_hmac_accepts_correct_signature(monkeypatch):
    monkeypatch.setattr(paymob_service.settings, "PAYMOB_HMAC_SECRET", SECRET)
    correct_hmac = _sign(SECRET, _EXPECTED_CONCAT)
    assert paymob_service.verify_webhook_hmac(SAMPLE_OBJ, correct_hmac) is True


def test_verify_webhook_hmac_rejects_tampered_amount(monkeypatch):
    """Simulates an attacker replaying a genuine webhook but editing the
    amount (or any field) — the signature must no longer match."""
    monkeypatch.setattr(paymob_service.settings, "PAYMOB_HMAC_SECRET", SECRET)
    correct_hmac = _sign(SECRET, _EXPECTED_CONCAT)
    tampered = {**SAMPLE_OBJ, "amount_cents": 1}
    assert paymob_service.verify_webhook_hmac(tampered, correct_hmac) is False


def test_verify_webhook_hmac_rejects_wrong_secret(monkeypatch):
    monkeypatch.setattr(paymob_service.settings, "PAYMOB_HMAC_SECRET", SECRET)
    wrong_hmac = _sign("some-other-secret", _EXPECTED_CONCAT)
    assert paymob_service.verify_webhook_hmac(SAMPLE_OBJ, wrong_hmac) is False


def test_verify_webhook_hmac_rejects_missing_hmac(monkeypatch):
    monkeypatch.setattr(paymob_service.settings, "PAYMOB_HMAC_SECRET", SECRET)
    assert paymob_service.verify_webhook_hmac(SAMPLE_OBJ, "") is False


def test_verify_webhook_hmac_false_when_unconfigured(monkeypatch):
    monkeypatch.setattr(paymob_service.settings, "PAYMOB_HMAC_SECRET", None)
    correct_hmac = _sign(SECRET, _EXPECTED_CONCAT)
    assert paymob_service.verify_webhook_hmac(SAMPLE_OBJ, correct_hmac) is False
