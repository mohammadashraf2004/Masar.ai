"""An oversized request body is refused before the API buffers it (release audit: one
unauthenticated 300 MB POST to /auth/login grew a worker by ~300 MB for over a minute)."""
from app.core.config import settings


def test_a_declared_oversized_body_is_refused_before_it_is_read(client):
    body = b"x" * (settings.MAX_REQUEST_BODY_BYTES + 1)
    response = client.post("/api/v1/auth/login", content=body, headers={"Content-Type": "application/json"})
    assert response.status_code == 413


def test_a_streamed_body_without_a_length_is_cut_off_at_the_limit(client):
    def chunks():
        for _ in range(settings.MAX_REQUEST_BODY_BYTES // 65536 + 4):
            yield b"x" * 65536

    response = client.post("/api/v1/payments/paymob/webhook", content=chunks(),
                           headers={"Content-Type": "application/json"})
    assert response.status_code in (400, 413)


def test_an_ordinary_body_is_unaffected(client):
    response = client.post("/api/v1/auth/login", json={"email": "nobody@example.com", "password": "x" * 12})
    assert response.status_code in (400, 401, 422)
