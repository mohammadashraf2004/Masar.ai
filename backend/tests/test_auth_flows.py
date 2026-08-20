"""
Covers the new auth hardening: email verification, password reset, and
token_version-based session revocation (logout-all, password reset, and
account deletion should all invalidate previously issued tokens even
though JWTs are otherwise stateless).
"""
import uuid

from app.db.session import SessionLocal
from app.models.user import User


def _unique_email() -> str:
    return f"test-{uuid.uuid4().hex[:12]}@example.com"


def _register(client, email=None, password="correcthorsebatterystaple"):
    email = email or _unique_email()
    resp = client.post("/api/v1/auth/register", json={
        "email": email, "full_name": "Test User", "password": password,
    })
    assert resp.status_code == 201
    return resp.json()


def test_register_creates_unverified_user(client):
    data = _register(client)
    assert data["user"]["is_verified"] is False


def test_verify_email_flow(client, db, monkeypatch):
    sent = {}
    import app.controllers.auth_controller as auth_mod
    monkeypatch.setattr(auth_mod, "send_verification_email", lambda to, name, token: sent.update(token=token) or True)

    data = _register(client)
    email = data["user"]["email"]
    raw_token = sent["token"]

    resp = client.post("/api/v1/auth/verify-email", json={"token": raw_token})
    assert resp.status_code == 200

    check = SessionLocal()
    user = check.query(User).filter(User.email == email).first()
    assert user.is_verified is True
    check.close()

    # Re-using the same (now-consumed) token must fail.
    resp2 = client.post("/api/v1/auth/verify-email", json={"token": raw_token})
    assert resp2.status_code == 400


def test_verify_email_rejects_garbage_token(client):
    resp = client.post("/api/v1/auth/verify-email", json={"token": "not-a-real-token"})
    assert resp.status_code == 400


def test_forgot_password_does_not_leak_whether_email_exists(client):
    resp_real = client.post("/api/v1/auth/forgot-password", json={"email": _unique_email()})
    resp_fake = client.post("/api/v1/auth/forgot-password", json={"email": "definitely-not-registered@example.com"})
    assert resp_real.status_code == 200
    assert resp_fake.status_code == 200
    assert resp_real.json()["message"] == resp_fake.json()["message"]


def test_reset_password_flow_and_old_sessions_revoked(client, monkeypatch):
    sent = {}
    import app.controllers.auth_controller as auth_mod
    monkeypatch.setattr(auth_mod, "send_password_reset_email", lambda to, name, token: sent.update(token=token) or True)

    email = _unique_email()
    reg = _register(client, email=email, password="original-password-123")
    old_token = reg["access_token"]

    # Old token works before reset.
    assert client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {old_token}"}).status_code == 200

    resp = client.post("/api/v1/auth/forgot-password", json={"email": email})
    assert resp.status_code == 200
    raw_reset_token = sent["token"]

    resp = client.post("/api/v1/auth/reset-password", json={"token": raw_reset_token, "new_password": "brand-new-password-456"})
    assert resp.status_code == 200

    # Old token must now be rejected — password reset revokes every
    # previously issued session, not just this one.
    resp = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {old_token}"})
    assert resp.status_code == 401

    # New password logs in fine; old password no longer works.
    assert client.post("/api/v1/auth/login", json={"email": email, "password": "brand-new-password-456"}).status_code == 200
    assert client.post("/api/v1/auth/login", json={"email": email, "password": "original-password-123"}).status_code == 401


def test_logout_all_revokes_existing_token(client):
    email = _unique_email()
    reg = _register(client, email=email)
    token = reg["access_token"]

    assert client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"}).status_code == 200

    resp = client.post("/api/v1/auth/logout-all", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200

    # The very token used to call logout-all is itself now invalid.
    resp = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 401


def test_delete_account_anonymizes_and_revokes(client, db):
    email = _unique_email()
    reg = _register(client, email=email)
    token = reg["access_token"]
    user_id = reg["user"]["id"]

    resp = client.delete("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200

    # Old token revoked.
    assert client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"}).status_code == 401

    # Row still exists (not hard-deleted) but PII is scrubbed.
    check = SessionLocal()
    user = check.query(User).filter(User.id == user_id).first()
    assert user is not None
    assert user.email != email
    assert user.full_name == "Deleted User"
    assert user.is_active is False
    check.close()

    # The original email is free to re-register.
    resp = client.post("/api/v1/auth/register", json={
        "email": email, "full_name": "New Owner", "password": "another-password-789",
    })
    assert resp.status_code == 201
