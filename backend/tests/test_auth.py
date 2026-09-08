import uuid


def _unique_email() -> str:
    return f"test-{uuid.uuid4().hex[:12]}@example.com"


def test_register_grants_starter_credits(client):
    email = _unique_email()
    reg = client.post("/api/v1/auth/register", json={
        "email": email, "full_name": "Test User", "password": "correcthorsebatterystaple",
    })
    token = reg.json()["access_token"]
    wallet = client.get("/api/v1/wallet/", headers={"Authorization": f"Bearer {token}"})
    assert wallet.status_code == 200
    assert wallet.json()["credit_balance"] == 10


def test_register_then_login(client):
    email = _unique_email()
    resp = client.post("/api/v1/auth/register", json={
        "email": email,
        "full_name": "Test User",
        "password": "correcthorsebatterystaple",
    })
    assert resp.status_code == 201
    body = resp.json()
    assert body["user"]["email"] == email
    assert "access_token" in body

    resp = client.post("/api/v1/auth/login", json={
        "email": email,
        "password": "correcthorsebatterystaple",
    })
    assert resp.status_code == 200
    assert "access_token" in resp.json()


def test_register_duplicate_email_rejected(client):
    email = _unique_email()
    payload = {"email": email, "full_name": "Test User", "password": "correcthorsebatterystaple"}
    assert client.post("/api/v1/auth/register", json=payload).status_code == 201
    resp = client.post("/api/v1/auth/register", json=payload)
    assert resp.status_code == 400


def test_login_wrong_password_rejected(client):
    email = _unique_email()
    client.post("/api/v1/auth/register", json={
        "email": email, "full_name": "Test User", "password": "correcthorsebatterystaple",
    })
    resp = client.post("/api/v1/auth/login", json={"email": email, "password": "wrong-password"})
    assert resp.status_code == 401


def test_me_requires_auth(client):
    resp = client.get("/api/v1/auth/me")
    assert resp.status_code == 401


def test_me_returns_current_user(client):
    email = _unique_email()
    reg = client.post("/api/v1/auth/register", json={
        "email": email, "full_name": "Test User", "password": "correcthorsebatterystaple",
    })
    token = reg.json()["access_token"]
    resp = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    assert resp.json()["email"] == email


def test_login_is_rate_limited(client):
    email = _unique_email()
    # 10/minute on /auth/login (see app/controllers/auth_controller.py) —
    # fire more than that and confirm the limiter actually engages.
    for _ in range(10):
        client.post("/api/v1/auth/login", json={"email": email, "password": "x"})
    resp = client.post("/api/v1/auth/login", json={"email": email, "password": "x"})
    assert resp.status_code == 429
