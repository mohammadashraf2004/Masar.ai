"""
Security regression tests.

Every test here asserts that an ATTACK FAILS. They are written from the
attacker's side on purpose: a test that only checks the happy path keeps
passing after someone removes an authorization check, whereas these go
red the moment a guard is dropped.

Grouped by the vulnerability class each one covers; see SECURITY.md for
the corresponding report entries.
"""
import secrets
import uuid
from datetime import datetime, timedelta, timezone

import pytest
import jwt

from app.core.config import settings
from app.core.security import (
    create_access_token, get_password_hash, normalize_email, verify_password,
)
from app.models.user import User, UserRole
from tests.conftest import verify_user

STRONG_PASSWORD = "correct-horse-battery-staple-7"


def _unique_email() -> str:
    return f"sec-{uuid.uuid4().hex[:12]}@example.com"


def _register(client, email=None, password=STRONG_PASSWORD, full_name="Sec Tester"):
    email = email or _unique_email()
    resp = client.post("/api/v1/auth/register", json={
        "email": email, "full_name": full_name, "password": password,
    })
    assert resp.status_code == 201, resp.text
    return email, resp.json()["access_token"], resp.json()["user"]["id"]


def _auth(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def _make_admin(db, user_id: int) -> None:
    db.query(User).filter(User.id == user_id).update({User.role: UserRole.admin})
    db.commit()


# ─────────────────────────────────────────────────────────────────────────
# 1. Unauthenticated access to protected endpoints
# ─────────────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("method,path", [
    ("get",   "/api/v1/auth/me"),
    ("patch", "/api/v1/auth/me"),
    ("delete", "/api/v1/auth/me"),
    ("post",  "/api/v1/auth/logout-all"),
    ("get",   "/api/v1/wallet/"),
    ("get",   "/api/v1/wallet/transactions"),
    ("get",   "/api/v1/profile/scorecard"),
    ("get",   "/api/v1/mentor/sessions"),
    ("get",   "/api/v1/community/feed"),
    ("get",   "/api/v1/exams/my-attempts"),
    ("get",   "/api/v1/exams/my-certificates"),
    ("get",   "/api/v1/tracks/my-enrollments"),
    ("get",   "/api/v1/tracks/topics/1"),
    ("post",  "/api/v1/tracks/topics/1/progress"),
    ("get",   "/api/v1/tool-courses/my-enrollments"),
])
def test_protected_endpoints_reject_anonymous(client, method, path):
    call = getattr(client, method)
    resp = call(path) if method in ("get", "delete") else call(path, json={})
    assert resp.status_code == 401, f"{method.upper()} {path} returned {resp.status_code}"


def test_full_course_content_requires_authentication(client):
    """The catalogue is public; the curriculum body is not."""
    assert client.get("/api/v1/tracks/").status_code == 200
    assert client.get("/api/v1/tracks/some-slug").status_code == 401
    assert client.get("/api/v1/tool-courses/some-slug").status_code == 401


# ─────────────────────────────────────────────────────────────────────────
# 2. Token validation: invalid, expired, tampered, wrong type/issuer
# ─────────────────────────────────────────────────────────────────────────

def test_garbage_token_rejected(client):
    assert client.get("/api/v1/auth/me", headers=_auth("not-a-jwt")).status_code == 401


def test_expired_token_rejected(client):
    _, token, user_id = _register(client)
    expired = create_access_token(
        data={"sub": str(user_id), "tv": 0}, expires_delta=timedelta(minutes=-5),
    )
    assert client.get("/api/v1/auth/me", headers=_auth(expired)).status_code == 401


def test_token_signed_with_wrong_secret_rejected(client):
    _, _, user_id = _register(client)
    forged = jwt.encode(
        {
            "sub": str(user_id), "tv": 0, "typ": "access",
            "iss": settings.JWT_ISSUER, "aud": settings.JWT_AUDIENCE,
            "iat": datetime.now(timezone.utc),
            "exp": datetime.now(timezone.utc) + timedelta(hours=1),
        },
        "an-attacker-chosen-secret",
        algorithm="HS256",
    )
    assert client.get("/api/v1/auth/me", headers=_auth(forged)).status_code == 401


def test_tampered_payload_rejected(client):
    """Flipping a character in the payload segment must invalidate the
    signature rather than silently changing who we think the caller is."""
    _, token, _ = _register(client)
    header, payload, sig = token.split(".")
    mutated = payload[:-4] + ("A" if payload[-4] != "A" else "B") + payload[-3:]
    assert client.get("/api/v1/auth/me", headers=_auth(f"{header}.{mutated}.{sig}")).status_code == 401


def test_alg_none_token_rejected(client):
    """The classic algorithm-confusion attack: an unsigned token claiming
    alg=none. Hand-assembled, because the JWT library refuses to mint one
    — the point is what OUR verifier does when handed it."""
    import base64
    import json

    def b64(obj):
        return base64.urlsafe_b64encode(json.dumps(obj).encode()).rstrip(b"=").decode()

    _, _, user_id = _register(client)
    header = b64({"alg": "none", "typ": "JWT"})
    payload = b64({
        "sub": str(user_id), "tv": 0, "typ": "access",
        "iss": settings.JWT_ISSUER, "aud": settings.JWT_AUDIENCE,
        "iat": 0, "nbf": 0, "exp": 9_999_999_999,
    })
    assert client.get("/api/v1/auth/me",
                      headers=_auth(f"{header}.{payload}.")).status_code == 401


def test_token_with_wrong_audience_rejected(client):
    """A token minted by another service that happens to share our signing
    key must not be usable here."""
    _, _, user_id = _register(client)
    other = jwt.encode(
        {
            "sub": str(user_id), "tv": 0, "typ": "access",
            "iss": "some-other-service", "aud": "some-other-api",
            "iat": datetime.now(timezone.utc),
            "exp": datetime.now(timezone.utc) + timedelta(hours=1),
        },
        settings.SECRET_KEY, algorithm=settings.ALGORITHM,
    )
    assert client.get("/api/v1/auth/me", headers=_auth(other)).status_code == 401


def test_non_access_token_type_rejected(client):
    _, _, user_id = _register(client)
    wrong_type = create_access_token(data={"sub": str(user_id), "tv": 0})
    payload = jwt.decode(
        wrong_type, settings.SECRET_KEY, algorithms=[settings.ALGORITHM],
        audience=settings.JWT_AUDIENCE, issuer=settings.JWT_ISSUER,
    )
    payload["typ"] = "refresh"
    reminted = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    assert client.get("/api/v1/auth/me", headers=_auth(reminted)).status_code == 401


def test_non_numeric_subject_does_not_500(client):
    """A malformed `sub` used to reach int() and raise — an unauthenticated
    500 oracle. It must be a clean 401."""
    forged = create_access_token(data={"sub": "not-an-id", "tv": 0})
    assert client.get("/api/v1/auth/me", headers=_auth(forged)).status_code == 401


# ─────────────────────────────────────────────────────────────────────────
# 3. Session invalidation (logout / password change / deletion)
# ─────────────────────────────────────────────────────────────────────────

def test_logout_all_invalidates_previously_issued_token(client):
    _, token, _ = _register(client)
    assert client.get("/api/v1/auth/me", headers=_auth(token)).status_code == 200
    assert client.post("/api/v1/auth/logout-all", headers=_auth(token)).status_code == 200
    assert client.get("/api/v1/auth/me", headers=_auth(token)).status_code == 401


def test_deleted_account_token_stops_working(client):
    _, token, _ = _register(client)
    assert client.delete("/api/v1/auth/me", headers=_auth(token)).status_code == 200
    assert client.get("/api/v1/auth/me", headers=_auth(token)).status_code == 401


# ─────────────────────────────────────────────────────────────────────────
# 4. Password handling
# ─────────────────────────────────────────────────────────────────────────

def test_password_is_hashed_not_stored_in_plaintext(client, db):
    email, _, user_id = _register(client)
    user = db.query(User).filter(User.id == user_id).one()
    assert user.hashed_password != STRONG_PASSWORD
    assert STRONG_PASSWORD not in user.hashed_password
    assert user.hashed_password.startswith("$2")      # bcrypt
    assert verify_password(STRONG_PASSWORD, user.hashed_password)


def test_password_hash_never_returned_by_any_auth_endpoint(client):
    email, token, _ = _register(client)
    for resp in (
        client.get("/api/v1/auth/me", headers=_auth(token)),
        client.post("/api/v1/auth/login", json={"email": email, "password": STRONG_PASSWORD}),
    ):
        body = resp.text.lower()
        assert "hashed_password" not in body
        assert "$2b$" not in body
        assert "token_version" not in body


@pytest.mark.parametrize("weak", [
    "short1",              # below the minimum length
    "password123",         # in the common-password list
    "aaaaaaaaaaaaaa",      # too few distinct characters
    "              ",      # whitespace only
])
def test_weak_passwords_rejected_at_registration(client, weak):
    resp = client.post("/api/v1/auth/register", json={
        "email": _unique_email(), "full_name": "Weak", "password": weak,
    })
    assert resp.status_code == 422


def test_overlong_password_rejected_rather_than_silently_truncated(client):
    """bcrypt ignores everything past 72 bytes; without an explicit cap,
    two different 200-character passwords sharing a prefix would both
    authenticate."""
    resp = client.post("/api/v1/auth/register", json={
        "email": _unique_email(), "full_name": "Long", "password": "A1b2c3d4e5!" * 20,
    })
    assert resp.status_code == 422


# ─────────────────────────────────────────────────────────────────────────
# 5. Account enumeration / login hardening
# ─────────────────────────────────────────────────────────────────────────

def test_login_failure_message_is_identical_for_unknown_and_wrong_password(client):
    email, _, _ = _register(client)
    unknown = client.post("/api/v1/auth/login",
                          json={"email": _unique_email(), "password": STRONG_PASSWORD})
    wrong = client.post("/api/v1/auth/login",
                        json={"email": email, "password": "definitely-not-it-42"})
    assert unknown.status_code == wrong.status_code == 401
    assert unknown.json()["detail"] == wrong.json()["detail"]


def test_forgot_password_response_identical_whether_or_not_account_exists(client):
    email, _, _ = _register(client)
    known = client.post("/api/v1/auth/forgot-password", json={"email": email})
    unknown = client.post("/api/v1/auth/forgot-password", json={"email": _unique_email()})
    assert known.status_code == unknown.status_code == 200
    assert known.json() == unknown.json()


def test_login_is_case_insensitive_on_email(client):
    """Normalization must be consistent, or `Sam@x.com` and `sam@x.com`
    become two accounts the user experiences as one broken one."""
    email, _, _ = _register(client)
    resp = client.post("/api/v1/auth/login",
                       json={"email": email.upper(), "password": STRONG_PASSWORD})
    assert resp.status_code == 200


def test_registration_rejects_case_variant_duplicate(client):
    email, _, _ = _register(client)
    resp = client.post("/api/v1/auth/register", json={
        "email": email.upper(), "full_name": "Twin", "password": STRONG_PASSWORD,
    })
    assert resp.status_code == 400


def test_repeated_failed_logins_lock_the_account_out(client):
    """Per-account throttling, on top of the per-IP rate limit — the
    control that actually bites credential stuffing."""
    email, _, _ = _register(client)
    statuses = [
        client.post("/api/v1/auth/login",
                    json={"email": email, "password": f"wrong-guess-{i}"}).status_code
        for i in range(settings.LOGIN_MAX_FAILURES + 2)
    ]
    assert 429 in statuses, statuses
    # And the lockout holds even once the correct password is supplied.
    blocked = client.post("/api/v1/auth/login",
                          json={"email": email, "password": STRONG_PASSWORD})
    assert blocked.status_code == 429


# ─────────────────────────────────────────────────────────────────────────
# 6. Password-reset token security
# ─────────────────────────────────────────────────────────────────────────

def _issue_reset_token(db, user_id: int, ttl=timedelta(hours=1)) -> str:
    from app.core.security import generate_opaque_token, hash_opaque_token
    from app.models.auth_token import EmailToken, EmailTokenPurpose

    raw = generate_opaque_token()
    db.add(EmailToken(
        user_id=user_id,
        purpose=EmailTokenPurpose.reset_password,
        token_hash=hash_opaque_token(raw),
        expires_at=datetime.now(timezone.utc) + ttl,
    ))
    db.commit()
    return raw


def test_reset_token_is_stored_only_as_a_hash(client, db):
    from app.models.auth_token import EmailToken

    _, _, user_id = _register(client)
    raw = _issue_reset_token(db, user_id)
    stored = [t.token_hash for t in db.query(EmailToken).filter(EmailToken.user_id == user_id)]
    assert raw not in stored, "raw reset token was persisted"


def test_expired_reset_token_rejected(client, db):
    _, _, user_id = _register(client)
    raw = _issue_reset_token(db, user_id, ttl=timedelta(hours=-1))
    resp = client.post("/api/v1/auth/reset-password",
                       json={"token": raw, "new_password": "brand-new-secret-99"})
    assert resp.status_code == 400


def test_reset_token_is_single_use(client, db):
    _, _, user_id = _register(client)
    raw = _issue_reset_token(db, user_id)
    first = client.post("/api/v1/auth/reset-password",
                        json={"token": raw, "new_password": "brand-new-secret-99"})
    assert first.status_code == 200
    second = client.post("/api/v1/auth/reset-password",
                         json={"token": raw, "new_password": "another-new-secret-77"})
    assert second.status_code == 400


def test_password_reset_revokes_existing_sessions(client, db):
    _, token, user_id = _register(client)
    raw = _issue_reset_token(db, user_id)
    assert client.post("/api/v1/auth/reset-password",
                       json={"token": raw, "new_password": "brand-new-secret-99"}).status_code == 200
    assert client.get("/api/v1/auth/me", headers=_auth(token)).status_code == 401


def test_issuing_a_new_reset_token_retires_the_previous_one(client, db):
    """A leaked older link must stop working once a fresh one is requested."""
    email, _, user_id = _register(client)
    stale = _issue_reset_token(db, user_id)
    client.post("/api/v1/auth/forgot-password", json={"email": email})
    resp = client.post("/api/v1/auth/reset-password",
                       json={"token": stale, "new_password": "brand-new-secret-99"})
    assert resp.status_code == 400


def test_verification_token_cannot_be_used_as_a_reset_token(client, db):
    """Purpose confusion: an email-verification link must not reset a
    password, even though both are opaque tokens in the same table."""
    from app.core.security import generate_opaque_token, hash_opaque_token
    from app.models.auth_token import EmailToken, EmailTokenPurpose

    _, _, user_id = _register(client)
    raw = generate_opaque_token()
    db.add(EmailToken(
        user_id=user_id,
        purpose=EmailTokenPurpose.verify_email,
        token_hash=hash_opaque_token(raw),
        expires_at=datetime.now(timezone.utc) + timedelta(hours=1),
    ))
    db.commit()
    resp = client.post("/api/v1/auth/reset-password",
                       json={"token": raw, "new_password": "brand-new-secret-99"})
    assert resp.status_code == 400


# ─────────────────────────────────────────────────────────────────────────
# 7. Mass assignment / privilege escalation
# ─────────────────────────────────────────────────────────────────────────

def test_user_cannot_promote_themselves_via_profile_update(client, db):
    """The canonical mass-assignment attack: smuggle a privileged column
    into the profile-update body."""
    _, token, user_id = _register(client)
    resp = client.patch("/api/v1/auth/me", headers=_auth(token), json={
        "full_name": "Legit Name",
        "role": "admin",
        "is_verified": True,
        "is_active": True,
        "overall_readiness_score": 100,
        "token_version": 999,
        "email": "attacker@evil.example",
        "hashed_password": "$2b$12$aaaaaaaaaaaaaaaaaaaaaa",
    })
    assert resp.status_code == 200
    user = db.query(User).filter(User.id == user_id).one()
    assert user.role == UserRole.student
    assert user.is_verified is False
    assert user.overall_readiness_score == 0.0
    assert user.email != "attacker@evil.example"
    assert resp.json()["role"] == "student"


def test_user_cannot_pin_their_own_post(client, db):
    """is_pinned is a moderation field and is absent from PostUpdate."""
    _, token, _ = _register(client)
    created = client.post("/api/v1/community/posts", headers=_auth(token), json={
        "title": "A post", "content": "Some content long enough to pass validation.",
    })
    assert created.status_code == 201
    post_id = created.json()["id"]
    resp = client.patch(f"/api/v1/community/posts/{post_id}", headers=_auth(token),
                        json={"title": "Edited", "is_pinned": True, "likes_count": 9999})
    assert resp.status_code == 200
    assert resp.json()["is_pinned"] is False
    assert resp.json()["likes_count"] == 0


# ─────────────────────────────────────────────────────────────────────────
# 8. Admin authorization
# ─────────────────────────────────────────────────────────────────────────

ADMIN_ROUTES = [
    ("post", "/api/v1/wallet/admin/confirm/some-ref", None),
    ("post", "/api/v1/wallet/admin/grant", {"user_id": 1, "credits": 1000}),
    ("post", "/api/v1/exam-payments/admin/confirm/some-ref", None),
    ("get",  "/api/v1/exam-payments/admin/pending", None),
]


@pytest.mark.parametrize("method,path,body", ADMIN_ROUTES)
def test_admin_routes_reject_anonymous(client, method, path, body):
    call = getattr(client, method)
    resp = call(path) if method == "get" else call(path, json=body or {})
    assert resp.status_code == 401


@pytest.mark.parametrize("method,path,body", ADMIN_ROUTES)
def test_admin_routes_reject_normal_user(client, method, path, body):
    _, token, _ = _register(client)
    call = getattr(client, method)
    resp = (call(path, headers=_auth(token)) if method == "get"
            else call(path, headers=_auth(token), json=body or {}))
    assert resp.status_code == 403, f"{path} returned {resp.status_code}"


def test_admin_route_reachable_for_a_real_admin(client, db):
    """Complement to the two above: proves the 403s are an authorization
    decision, not a route that is simply broken for everyone."""
    _, token, user_id = _register(client)
    _make_admin(db, user_id)
    resp = client.get("/api/v1/exam-payments/admin/pending", headers=_auth(token))
    assert resp.status_code == 200


def test_demotion_takes_effect_without_reissuing_the_token(client, db):
    """Role is read from the database each request, never from a claim
    baked into the token at issuance."""
    _, token, user_id = _register(client)
    _make_admin(db, user_id)
    assert client.get("/api/v1/exam-payments/admin/pending", headers=_auth(token)).status_code == 200
    db.query(User).filter(User.id == user_id).update({User.role: UserRole.student})
    db.commit()
    assert client.get("/api/v1/exam-payments/admin/pending", headers=_auth(token)).status_code == 403


def test_admin_grant_rejects_negative_credits(client, db):
    _, token, user_id = _register(client)
    _make_admin(db, user_id)
    resp = client.post("/api/v1/wallet/admin/grant", headers=_auth(token),
                       json={"user_id": user_id, "credits": -5000})
    assert resp.status_code == 422


# ─────────────────────────────────────────────────────────────────────────
# 9. IDOR / BOLA — one user reaching another user's data
# ─────────────────────────────────────────────────────────────────────────

def test_user_cannot_read_another_users_mentor_session(client, db):
    from app.models.progress import MentorSession

    _, victim_token, victim_id = _register(client)
    _, attacker_token, _ = _register(client)

    session = MentorSession(user_id=victim_id, title="Private", messages=[
        {"role": "user", "content": "my private career worries"},
    ])
    db.add(session)
    db.commit()
    db.refresh(session)

    assert client.get(f"/api/v1/mentor/sessions/{session.id}",
                      headers=_auth(victim_token)).status_code == 200
    stolen = client.get(f"/api/v1/mentor/sessions/{session.id}", headers=_auth(attacker_token))
    assert stolen.status_code == 404
    assert "private career worries" not in stolen.text


def test_user_cannot_read_another_users_exam_attempt(client, db, seeded_exam):
    from app.models.exam import ExamAttempt, ExamStatus

    _, _, victim_id = _register(client)
    _, attacker_token, _ = _register(client)

    attempt = ExamAttempt(
        exam_id=seeded_exam.id, user_id=victim_id, status=ExamStatus.failed, score=41.0,
    )
    db.add(attempt)
    db.commit()
    db.refresh(attempt)

    resp = client.get(f"/api/v1/exams/attempts/{attempt.id}/result", headers=_auth(attacker_token))
    assert resp.status_code == 404


def test_user_cannot_submit_another_users_exam_attempt(client, db, seeded_exam):
    from app.models.exam import ExamAttempt, ExamStatus

    _, _, victim_id = _register(client)
    _, attacker_token, _ = _register(client)

    attempt = ExamAttempt(
        exam_id=seeded_exam.id, user_id=victim_id, status=ExamStatus.in_progress,
        started_at=datetime.now(timezone.utc),
    )
    db.add(attempt)
    db.commit()
    db.refresh(attempt)

    resp = client.post(f"/api/v1/exams/attempts/{attempt.id}/submit",
                       headers=_auth(attacker_token),
                       json={"answers": {}, "time_spent_seconds": 10})
    assert resp.status_code == 404


def test_user_cannot_read_another_users_payment_status(client, db, seeded_exam):
    from app.models.challenge import ExamPayment

    _, _, victim_id = _register(client)
    _, attacker_token, _ = _register(client)

    payment = ExamPayment(
        user_id=victim_id, exam_id=seeded_exam.id, egp_amount=150.0,
        payment_method="fawry", payment_ref=f"ref-{uuid.uuid4().hex[:8]}", status="confirmed",
    )
    db.add(payment)
    db.commit()

    resp = client.get(f"/api/v1/payments/status/{payment.payment_ref}",
                      headers=_auth(attacker_token))
    assert resp.status_code == 404


def test_wallet_only_ever_returns_the_callers_own_balance(client, db):
    from app.services.wallet.wallet_service import add_credits

    _, _, victim_id = _register(client)
    _, attacker_token, _ = _register(client)
    add_credits(victim_id, 5000, db, description="victim funds")

    resp = client.get("/api/v1/wallet/", headers=_auth(attacker_token))
    assert resp.status_code == 200
    assert resp.json()["credit_balance"] == 10   # only their own starter credits


def test_user_cannot_edit_or_delete_another_users_post(client):
    _, owner_token, _ = _register(client)
    _, attacker_token, _ = _register(client)

    created = client.post("/api/v1/community/posts", headers=_auth(owner_token), json={
        "title": "Owner post", "content": "Content that is definitely long enough.",
    })
    post_id = created.json()["id"]

    assert client.patch(f"/api/v1/community/posts/{post_id}",
                        headers=_auth(attacker_token),
                        json={"title": "Hijacked"}).status_code == 403
    assert client.delete(f"/api/v1/community/posts/{post_id}",
                         headers=_auth(attacker_token)).status_code == 403


# ─────────────────────────────────────────────────────────────────────────
# 10. Progress ownership & integrity
# ─────────────────────────────────────────────────────────────────────────

@pytest.fixture()
def seeded_topic(db):
    """A minimal track → level → topic → lesson chain to exercise the
    progress endpoints against."""
    from app.models.learning import CareerTrack, TrackLevel, Topic, Lesson

    suffix = uuid.uuid4().hex[:8]
    track = CareerTrack(slug=f"sec-track-{suffix}", title="Sec Track", estimated_weeks=1)
    db.add(track)
    db.flush()
    level = TrackLevel(track_id=track.id, title="L1", order=1)
    db.add(level)
    db.flush()
    topic = Topic(level_id=level.id, slug=f"sec-topic-{suffix}", title="T1", order=1)
    db.add(topic)
    db.flush()
    lesson = Lesson(topic_id=topic.id, title="Lesson 1", content="body", order=1)
    other_topic = Topic(level_id=level.id, slug=f"sec-other-{suffix}", title="T2", order=2)
    db.add_all([lesson, other_topic])
    db.flush()
    foreign_lesson = Lesson(topic_id=other_topic.id, title="Elsewhere", content="body", order=1)
    db.add(foreign_lesson)
    db.commit()
    return {"topic_id": topic.id, "lesson_id": lesson.id, "foreign_lesson_id": foreign_lesson.id}


def test_progress_is_scoped_to_the_caller(client, seeded_topic):
    """Two users writing progress on the same topic must not see each
    other's — there is no user id in the request to tamper with, and the
    query is scoped to the token's subject."""
    _, token_a, _ = _register(client)
    _, token_b, _ = _register(client)

    client.post(f"/api/v1/tracks/topics/{seeded_topic['topic_id']}/progress",
                headers=_auth(token_a),
                json={"lesson_id": seeded_topic["lesson_id"], "time_spent_minutes": 30})

    resp = client.get(f"/api/v1/tracks/topics/{seeded_topic['topic_id']}/progress",
                      headers=_auth(token_b))
    assert resp.status_code == 404


def test_progress_rejects_a_lesson_from_a_different_topic(client, seeded_topic):
    """Completion is derived from how many lessons are marked done, so
    accepting arbitrary ids would let a client fabricate course
    completion (and, for tool courses, a completion record)."""
    _, token, _ = _register(client)
    resp = client.post(f"/api/v1/tracks/topics/{seeded_topic['topic_id']}/progress",
                       headers=_auth(token),
                       json={"lesson_id": seeded_topic["foreign_lesson_id"]})
    assert resp.status_code == 400


def test_progress_rejects_nonexistent_lesson_id(client, seeded_topic):
    _, token, _ = _register(client)
    resp = client.post(f"/api/v1/tracks/topics/{seeded_topic['topic_id']}/progress",
                       headers=_auth(token), json={"lesson_id": 99_999_999})
    assert resp.status_code == 400


def test_progress_rejects_absurd_and_negative_study_time(client, seeded_topic):
    _, token, _ = _register(client)
    for minutes in (-60, 10_000_000):
        resp = client.post(f"/api/v1/tracks/topics/{seeded_topic['topic_id']}/progress",
                           headers=_auth(token), json={"time_spent_minutes": minutes})
        assert resp.status_code == 422, minutes


# ─────────────────────────────────────────────────────────────────────────
# 11. Course / exam access control
# ─────────────────────────────────────────────────────────────────────────

@pytest.fixture()
def seeded_exam(db):
    from app.models.learning import CareerTrack
    from app.models.exam import Exam

    suffix = uuid.uuid4().hex[:8]
    track = CareerTrack(slug=f"exam-track-{suffix}", title="Exam Track", estimated_weeks=1)
    db.add(track)
    db.flush()
    exam = Exam(
        track_id=track.id, title="Certification", duration_minutes=60,
        passing_score=70, max_attempts=3,
        questions=[{
            "id": 1, "question": "2+2?", "options": ["3", "4"],
            "correct": 1, "explanation": "arithmetic", "points": 1, "type": "mcq",
        }],
    )
    db.add(exam)
    db.commit()
    db.refresh(exam)
    return exam


def test_unpaid_user_cannot_start_a_certification_exam(client, seeded_exam):
    """The paywall used to live only in the frontend: anyone who skipped
    the UI could start a paid exam, pass it, and be issued a certificate
    for free."""
    _, token, _ = _register(client)
    resp = client.post(f"/api/v1/exams/{seeded_exam.id}/start", headers=_auth(token))
    assert resp.status_code == 402


def test_paid_user_can_start_the_exam(client, db, seeded_exam):
    from app.models.challenge import ExamPayment

    _, token, user_id = _register(client)
    db.add(ExamPayment(
        user_id=user_id, exam_id=seeded_exam.id, egp_amount=150.0,
        payment_method="fawry", payment_ref=f"paid-{uuid.uuid4().hex[:8]}",
        status="confirmed", confirmed_at=datetime.now(timezone.utc),
    ))
    db.commit()
    resp = client.post(f"/api/v1/exams/{seeded_exam.id}/start", headers=_auth(token))
    assert resp.status_code == 200


def test_a_pending_payment_does_not_unlock_the_exam(client, db, seeded_exam):
    """Only a *confirmed* payment counts — submitting a reference number
    is a claim, not a payment."""
    from app.models.challenge import ExamPayment

    _, token, user_id = _register(client)
    db.add(ExamPayment(
        user_id=user_id, exam_id=seeded_exam.id, egp_amount=150.0,
        payment_method="fawry", payment_ref=f"pending-{uuid.uuid4().hex[:8]}",
        status="pending",
    ))
    db.commit()
    resp = client.post(f"/api/v1/exams/{seeded_exam.id}/start", headers=_auth(token))
    assert resp.status_code == 402


def test_exam_session_does_not_include_the_answer_key(client, db, seeded_exam):
    from app.models.challenge import ExamPayment

    _, token, user_id = _register(client)
    db.add(ExamPayment(
        user_id=user_id, exam_id=seeded_exam.id, egp_amount=150.0,
        payment_method="fawry", payment_ref=f"key-{uuid.uuid4().hex[:8]}",
        status="confirmed", confirmed_at=datetime.now(timezone.utc),
    ))
    db.commit()
    resp = client.post(f"/api/v1/exams/{seeded_exam.id}/start", headers=_auth(token))
    assert resp.status_code == 200
    for question in resp.json()["questions"]:
        assert "correct" not in question
        assert "explanation" not in question


def test_expired_exam_attempt_cannot_be_submitted(client, db, seeded_exam):
    from app.models.challenge import ExamPayment
    from app.models.exam import ExamAttempt, ExamStatus

    _, token, user_id = _register(client)
    db.add(ExamPayment(
        user_id=user_id, exam_id=seeded_exam.id, egp_amount=150.0,
        payment_method="fawry", payment_ref=f"exp-{uuid.uuid4().hex[:8]}",
        status="confirmed", confirmed_at=datetime.now(timezone.utc),
    ))
    attempt = ExamAttempt(
        exam_id=seeded_exam.id, user_id=user_id, status=ExamStatus.in_progress,
        started_at=datetime.now(timezone.utc) - timedelta(hours=5),
    )
    db.add(attempt)
    db.commit()
    db.refresh(attempt)

    resp = client.post(f"/api/v1/exams/attempts/{attempt.id}/submit", headers=_auth(token),
                       json={"answers": {"1": 1}, "time_spent_seconds": 60})
    assert resp.status_code == 400


def test_quiz_answer_key_is_not_exposed_to_the_taker(client, db):
    """Quiz.questions holds the prompt AND the answer key in one JSON
    blob; the response model must strip the key half."""
    from app.models.learning import CareerTrack, TrackLevel, Topic, Quiz

    suffix = uuid.uuid4().hex[:8]
    track = CareerTrack(slug=f"quiz-track-{suffix}", title="Quiz Track", estimated_weeks=1)
    db.add(track)
    db.flush()
    level = TrackLevel(track_id=track.id, title="L1", order=1)
    db.add(level)
    db.flush()
    topic = Topic(level_id=level.id, slug=f"quiz-topic-{suffix}", title="T", order=1)
    db.add(topic)
    db.flush()
    db.add(Quiz(topic_id=topic.id, title="Q", passing_score=70, questions=[{
        "question": "Capital of France?",
        "options": ["Berlin", "Paris"],
        "correct": 1,
        "explanation": "It is Paris.",
    }]))
    db.commit()

    _, token, _ = _register(client)
    resp = client.get(f"/api/v1/tracks/topics/{topic.id}", headers=_auth(token))
    assert resp.status_code == 200
    body = resp.text
    assert "It is Paris." not in body
    for quiz in resp.json()["quizzes"]:
        for question in quiz["questions"]:
            assert "correct" not in question
            assert "explanation" not in question

    track_resp = client.get(f"/api/v1/tracks/quiz-track-{suffix}", headers=_auth(token))
    assert "It is Paris." not in track_resp.text


# ─────────────────────────────────────────────────────────────────────────
# 12. Injection & input validation
# ─────────────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("payload", [
    "' OR '1'='1",
    "admin@example.com'--",
    "x@y.com'; DROP TABLE users; --",
])
def test_sql_injection_in_login_is_treated_as_data(client, db, payload):
    """The ORM parameterizes every query; these must be ordinary failed
    logins (or validation errors), never executed SQL."""
    resp = client.post("/api/v1/auth/login", json={"email": payload, "password": "whatever-123"})
    assert resp.status_code in (401, 422)
    # The table is still there and still queryable.
    assert db.query(User).count() >= 0


@pytest.mark.parametrize("bad_url", [
    "javascript:alert(document.cookie)",
    "JaVaScRiPt:alert(1)",
    "data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg==",
    "vbscript:msgbox(1)",
])
def test_dangerous_url_schemes_rejected_on_posts(client, bad_url):
    """Stored XSS: these values are later rendered as an href/src in
    another user's browser, where they would execute in that user's
    origin — and the access token lives in localStorage."""
    _, token, _ = _register(client)
    resp = client.post("/api/v1/community/posts", headers=_auth(token), json={
        "title": "Check this out", "content": "Long enough content for validation.",
        "github_url": bad_url,
    })
    assert resp.status_code == 422, bad_url


@pytest.mark.parametrize("bad_url", [
    "javascript:alert(1)",
    "data:text/html,<script>alert(1)</script>",
])
def test_dangerous_url_schemes_rejected_on_profile(client, bad_url):
    _, token, _ = _register(client)
    resp = client.patch("/api/v1/auth/me", headers=_auth(token), json={"github_url": bad_url})
    assert resp.status_code == 422, bad_url


def test_https_urls_are_still_accepted(client):
    """The scheme check must not break the legitimate case."""
    _, token, _ = _register(client)
    resp = client.patch("/api/v1/auth/me", headers=_auth(token),
                        json={"github_url": "https://github.com/someone"})
    assert resp.status_code == 200
    assert resp.json()["github_url"] == "https://github.com/someone"


def test_oversized_llm_input_rejected_before_it_reaches_the_provider(client):
    """Prompt size is a direct multiplier on our inference bill."""
    _, token, _ = _register(client)
    resp = client.post("/api/v1/mentor/chat", headers=_auth(token),
                       json={"content": "A" * 200_000})
    assert resp.status_code == 422


def test_pagination_parameters_are_bounded(client):
    _, token, _ = _register(client)
    assert client.get("/api/v1/community/feed?per_page=100000",
                      headers=_auth(token)).status_code == 422
    assert client.get("/api/v1/community/feed?page=0",
                      headers=_auth(token)).status_code == 422
    assert client.get("/api/v1/wallet/transactions?limit=1000000",
                      headers=_auth(token)).status_code == 422


# ─────────────────────────────────────────────────────────────────────────
# 13. CORS
# ─────────────────────────────────────────────────────────────────────────

def test_cors_does_not_reflect_an_arbitrary_origin(client):
    """With credentials enabled, echoing back whatever Origin was sent
    would let any site read authenticated responses."""
    resp = client.options("/api/v1/auth/me", headers={
        "Origin": "https://evil.example",
        "Access-Control-Request-Method": "GET",
    })
    assert resp.headers.get("access-control-allow-origin") != "https://evil.example"
    assert resp.headers.get("access-control-allow-origin") != "*"


def test_cors_allows_the_configured_frontend_origin(client):
    resp = client.options("/api/v1/auth/me", headers={
        "Origin": settings.FRONTEND_URL,
        "Access-Control-Request-Method": "GET",
    })
    assert resp.headers.get("access-control-allow-origin") == settings.FRONTEND_URL


def test_production_cors_config_excludes_localhost():
    """cors_origins is the single source of truth for the allowlist; in
    production it must not carry the dev conveniences."""
    from app.core.config import Settings

    prod = Settings(
        APP_ENV="production",
        FRONTEND_URL="https://app.example.com",
        SECRET_KEY="x" * 64,
        DATABASE_URL="postgresql://u:p@db.internal:5432/app",
    )
    assert prod.is_production is True
    assert all("localhost" not in o and "127.0.0.1" not in o for o in prod.cors_origins)
    assert prod.cors_origins == ["https://app.example.com"]


def test_unknown_app_env_is_treated_as_production():
    """A typo in APP_ENV must fail safe, not silently disable every
    production guard."""
    from app.core.config import Settings

    assert Settings(APP_ENV="prod").is_production is True
    assert Settings(APP_ENV="Production").is_production is True
    assert Settings(APP_ENV="development").is_production is False


# ─────────────────────────────────────────────────────────────────────────
# 14. Security headers & error hygiene
# ─────────────────────────────────────────────────────────────────────────

def test_security_headers_present_on_api_responses(client):
    resp = client.get("/health")
    assert resp.headers["x-content-type-options"] == "nosniff"
    assert resp.headers["x-frame-options"] == "DENY"
    assert resp.headers["referrer-policy"] == "no-referrer"
    assert "frame-ancestors 'none'" in resp.headers["content-security-policy"]
    assert "default-src 'none'" in resp.headers["content-security-policy"]
    assert resp.headers["cache-control"] == "no-store"


def test_health_endpoint_does_not_leak_provider_details_in_production(monkeypatch):
    """A health check is reachable by anyone who can reach the service."""
    from app.core import config as config_module

    monkeypatch.setattr(config_module.settings, "APP_ENV", "production")
    from fastapi.testclient import TestClient
    from app.main import app

    with TestClient(app) as c:
        body = c.get("/health").json()
    assert "ai_provider" not in body
    assert "ai_key_configured" not in body
    assert "database_error" not in body


def test_error_responses_do_not_leak_internals(client):
    """A 404/422 must not carry SQL, file paths, or a traceback."""
    _, token, _ = _register(client)
    for resp in (
        client.get("/api/v1/mentor/sessions/99999999", headers=_auth(token)),
        client.post("/api/v1/auth/login", json={"email": "nope", "password": "x"}),
    ):
        body = resp.text.lower()
        for leak in ("traceback", "sqlalchemy", "psycopg2", "/app/app/", "select ", "site-packages"):
            assert leak not in body, f"{leak!r} leaked in {resp.status_code} body"


# ─────────────────────────────────────────────────────────────────────────
# 15. Sensitive data exposure
# ─────────────────────────────────────────────────────────────────────────

def test_leaderboard_does_not_expose_email_addresses(client, db):
    """A public-ish social surface built from User rows is the classic
    place for over-broad serialization to leak PII."""
    email, token, _ = _register(client)
    resp = client.get("/api/v1/community/leaderboard", headers=_auth(token))
    assert resp.status_code == 200
    assert email not in resp.text
    assert "@example.com" not in resp.text


def test_community_feed_does_not_expose_author_emails(client):
    email, token, _ = _register(client)
    client.post("/api/v1/community/posts", headers=_auth(token), json={
        "title": "Hello world", "content": "Content long enough to be valid.",
    })
    resp = client.get("/api/v1/community/feed", headers=_auth(token))
    assert resp.status_code == 200
    assert email not in resp.text


def test_normalize_email_is_idempotent():
    for raw in ("  Alice@Example.COM ", "alice@example.com", "ALICE@EXAMPLE.COM"):
        assert normalize_email(raw) == "alice@example.com"
        assert normalize_email(normalize_email(raw)) == normalize_email(raw)


def test_bcrypt_hashes_are_salted(client):
    """Two identical passwords must not produce the same hash, or a single
    rainbow table covers every account that reused a password."""
    a = get_password_hash(STRONG_PASSWORD)
    b = get_password_hash(STRONG_PASSWORD)
    assert a != b
    assert verify_password(STRONG_PASSWORD, a)
    assert verify_password(STRONG_PASSWORD, b)


# ─────────────────────────────────────────────────────────────────────────
# 16. Rate-limit integrity: client identity and shared storage
#
# These guard the two ways a rate limit can be real in code and absent in
# production: counting the wrong client, or counting in a place each
# worker keeps to itself.
# ─────────────────────────────────────────────────────────────────────────

class _FakeRequest:
    """Minimal stand-in for a Starlette request for key derivation."""

    def __init__(self, headers, peer):
        self.headers = headers
        self.client = type("C", (), {"host": peer})()
        self.scope = {"client": (peer, 0), "headers": []}


def test_xff_is_ignored_when_no_trusted_proxy_is_configured():
    """Default posture. X-Forwarded-For is a plain request header — with
    no proxy in front, honouring it lets one host mint a fresh rate-limit
    bucket per request and walk straight through the login limit AND the
    per-account lockout (which is keyed on the same address)."""
    from app.core.limiter import client_key

    assert settings.TRUSTED_PROXY_COUNT == 0
    buckets = {
        client_key(_FakeRequest({"x-forwarded-for": spoof}, "203.0.113.9"))
        for spoof in ["1.1.1.1", "2.2.2.2", "1.1.1.1, 2.2.2.2", "a, b, 9.9.9.9"]
    }
    assert buckets == {"203.0.113.9"}, f"spoofable: {buckets}"


def test_xff_client_supplied_entries_are_ignored_behind_a_trusted_proxy(monkeypatch):
    """Proxies APPEND, so with one trusted proxy the real client is the
    RIGHT-most entry and everything left of it is caller-supplied."""
    from app.core import limiter as limiter_mod

    monkeypatch.setattr(settings, "TRUSTED_PROXY_COUNT", 1)
    monkeypatch.setattr(settings, "TRUSTED_PROXY_IPS", "10.0.0.0/8")

    a = limiter_mod.client_key(_FakeRequest({"x-forwarded-for": "9.9.9.9, 198.51.100.7"}, "10.0.0.5"))
    b = limiter_mod.client_key(_FakeRequest({"x-forwarded-for": "8.8.8.8, 198.51.100.7"}, "10.0.0.5"))
    c = limiter_mod.client_key(_FakeRequest({"x-forwarded-for": "198.51.100.7"}, "10.0.0.5"))
    assert a == b == c == "198.51.100.7"


def test_xff_is_ignored_when_the_peer_is_not_a_trusted_proxy(monkeypatch):
    """The case proxy-counting alone misses: an attacker who can reach the
    app port directly sends a one-entry header that satisfies the count."""
    from app.core import limiter as limiter_mod

    monkeypatch.setattr(settings, "TRUSTED_PROXY_COUNT", 1)
    monkeypatch.setattr(settings, "TRUSTED_PROXY_IPS", "10.0.0.0/8")

    buckets = {
        limiter_mod.client_key(_FakeRequest({"x-forwarded-for": spoof}, "203.0.113.9"))
        for spoof in ["1.1.1.1", "2.2.2.2", "1.1.1.1, 2.2.2.2"]
    }
    assert buckets == {"203.0.113.9"}, f"spoofable from a direct connection: {buckets}"


def test_malformed_trusted_proxy_entries_do_not_widen_trust(monkeypatch):
    monkeypatch.setattr(settings, "TRUSTED_PROXY_IPS", "not-an-ip, , 999.999.999.999")
    assert settings.trusted_proxy_networks == []


def _boot_with(**env_overrides):
    """Import app.core.config in a clean subprocess with the given env and
    report whether it refused to start, and why."""
    import os
    import subprocess
    import sys

    env = dict(os.environ)
    env.update({
        "APP_ENV": "production",
        # A realistic key: "x"*64 is long enough but trips the entropy
        # check, which is itself deliberate (see config.py).
        "SECRET_KEY": secrets.token_hex(32),
        # Metrics are on by default and /metrics must not be public, so a
        # complete production config has to carry a token. Listed here so
        # that new required-in-production settings surface as a failure of
        # test_production_starts_with_a_complete_configuration (a helper
        # that needs updating) rather than as a mystery in the checks that
        # assert a *specific* misconfiguration is rejected.
        "METRICS_TOKEN": secrets.token_hex(16),
        # Credit-spending now requires a verified email address, and
        # resend_service fails soft when unconfigured — so without a mail
        # provider every account would be permanently unable to spend.
        # Required in production for that reason; see config.py.
        "RESEND_API_KEY": "re_test_key_not_real",
        "DATABASE_URL": "postgresql://appuser:realpw@db.internal:5432/app",
        "FRONTEND_URL": "https://app.example.com",
        "EXTRA_CORS_ORIGINS": "",
    })
    env.update({k: str(v) for k, v in env_overrides.items()})
    proc = subprocess.run(
        [sys.executable, "-c", "import app.core.config"],
        capture_output=True, env=env, cwd=os.getcwd(),
    )
    return proc.returncode, proc.stderr.decode("utf-8", "replace")


def test_production_refuses_to_start_without_redis():
    """A rate limit whose counters are per-process is not the rate limit
    it claims to be — gunicorn runs 4 workers, so it would admit 4x."""
    code, err = _boot_with(REDIS_URL="")
    assert code != 0, "booted in production with no shared rate-limit backend"
    assert "REDIS_URL" in err


def test_production_refuses_to_start_with_proxy_count_but_no_proxy_allowlist():
    code, err = _boot_with(REDIS_URL="redis://localhost:6379/0", TRUSTED_PROXY_COUNT="1")
    assert code != 0, "booted trusting X-Forwarded-For from any peer"
    assert "TRUSTED_PROXY_IPS" in err


def test_production_refuses_to_start_without_an_email_provider():
    """Billable features are gated on a verified email address, and
    resend_service returns False rather than raising when RESEND_API_KEY is
    absent. Booting without it would hand every new user an account that
    can never verify and therefore can never spend a credit, with only a
    log warning to show for it."""
    code, err = _boot_with(REDIS_URL="redis://localhost:6379/0", RESEND_API_KEY="")
    assert code != 0, "booted in production with no way to send verification email"
    assert "RESEND_API_KEY" in err


def test_production_starts_with_a_complete_configuration():
    """Complement to the two above — proves they are real checks and not
    a configuration that can never be satisfied."""
    code, err = _boot_with(
        REDIS_URL="redis://localhost:6379/0",
        TRUSTED_PROXY_COUNT="1",
        TRUSTED_PROXY_IPS="10.0.0.0/8",
    )
    assert code == 0, err


def test_login_lockout_state_lives_in_the_shared_rate_limit_backend():
    """Not a process-local dict: with 4 gunicorn workers that would make
    the configured threshold of 8 admit up to 32, and reset on deploy."""
    from app.core import login_guard
    from app.core.limiter import limiter

    assert login_guard._strategy().storage is limiter._storage


def test_login_lockout_expires_rather_than_being_permanent():
    """The counter must carry the lockout window as a TTL. Without one a
    locked-out account stays locked until someone clears it by hand."""
    from app.core import login_guard

    login_guard.reset()
    email, ip = "ttl-probe@example.com", "198.51.100.44"
    for _ in range(settings.LOGIN_MAX_FAILURES):
        login_guard.record_failure(email, ip)

    wait = login_guard.seconds_until_unlocked(email, ip)
    window = settings.LOGIN_LOCKOUT_MINUTES * 60
    assert 0 < wait <= window, f"expected a bounded lockout, got {wait}s"
    login_guard.reset()


def test_login_lockout_counts_up_to_the_configured_threshold():
    from app.core import login_guard

    login_guard.reset()
    email, ip = "count-probe@example.com", "198.51.100.45"
    for expected in range(1, settings.LOGIN_MAX_FAILURES + 1):
        assert login_guard.seconds_until_unlocked(email, ip) == 0
        assert login_guard.record_failure(email, ip) == expected
    assert login_guard.seconds_until_unlocked(email, ip) > 0
    # A correct password clears it.
    login_guard.record_success(email, ip)
    assert login_guard.seconds_until_unlocked(email, ip) == 0
    login_guard.reset()


def test_production_refuses_a_low_entropy_secret_key():
    """Long but not random: "xxxx..." passes a length check and fails a
    real one. Regression guard for the check that caught a bad fixture in
    this very suite."""
    code, err = _boot_with(SECRET_KEY="x" * 64, REDIS_URL="redis://localhost:6379/0")
    assert code != 0
    assert "SECRET_KEY" in err


# ─────────────────────────────────────────────────────────────────────────
# 17. Launch promotion
#
# A giveaway is still an authorization surface: the amount, the
# eligibility and the expiry must all be server-decided, and expiry must
# actually remove credits rather than merely hiding them.
# ─────────────────────────────────────────────────────────────────────────

def _promo_open(monkeypatch, credits=500, days=30):
    monkeypatch.setattr(settings, "LAUNCH_PROMO_UNTIL", "2099-12-31")
    monkeypatch.setattr(settings, "LAUNCH_PROMO_CREDITS", credits)
    monkeypatch.setattr(settings, "LAUNCH_PROMO_DAYS", days)


def test_promo_is_off_when_no_end_date_is_configured(monkeypatch):
    """An unset LAUNCH_PROMO_UNTIL must not mean 'always on'."""
    monkeypatch.setattr(settings, "LAUNCH_PROMO_UNTIL", "")
    assert settings.launch_promo_until is None
    assert settings.promo_is_open() is False


def test_malformed_promo_date_fails_closed(monkeypatch):
    """A typo'd date must disable the promo, not enable it forever."""
    for bad in ["not-a-date", "31-12-2099", "2099/12/31", "  "]:
        monkeypatch.setattr(settings, "LAUNCH_PROMO_UNTIL", bad)
        assert settings.launch_promo_until is None
        assert settings.promo_is_open() is False


def test_expired_promo_date_closes_the_offer(monkeypatch):
    monkeypatch.setattr(settings, "LAUNCH_PROMO_UNTIL", "2020-01-01")
    assert settings.promo_is_open() is False


def test_signup_grants_promo_credits_while_open(client, monkeypatch):
    _promo_open(monkeypatch, credits=500)
    _, token, _ = _register(client)
    body = client.get("/api/v1/wallet/", headers=_auth(token)).json()
    assert body["credit_balance"] == 500
    assert body["promo_credits_remaining"] == 500
    assert body["promo_expires_at"] is not None


def test_signup_falls_back_to_starter_credits_when_closed(client, monkeypatch):
    """Promo closed — the ordinary welcome grant still applies."""
    monkeypatch.setattr(settings, "LAUNCH_PROMO_UNTIL", "")
    _, token, _ = _register(client)
    body = client.get("/api/v1/wallet/", headers=_auth(token)).json()
    assert body["credit_balance"] == 10
    assert body["promo_credits_remaining"] == 0
    assert body["promo_expires_at"] is None


def test_promo_amount_cannot_be_influenced_by_the_request(client, monkeypatch):
    """The grant is server config, not something a signup body can ask for."""
    _promo_open(monkeypatch, credits=500)
    resp = client.post("/api/v1/auth/register", json={
        "email": _unique_email(), "full_name": "Greedy User", "password": STRONG_PASSWORD,
        "credit_balance": 999999, "promo_credits_remaining": 999999,
        "promo_expires_at": "2099-01-01T00:00:00Z",
    })
    assert resp.status_code == 201
    body = client.get("/api/v1/wallet/", headers=_auth(resp.json()["access_token"])).json()
    assert body["credit_balance"] == 500


def test_user_cannot_extend_or_top_up_their_own_promo(client, db, monkeypatch):
    """No request schema exposes the promo columns, so a profile update
    naming them must be dropped rather than applied."""
    from app.models.wallet import UserWallet

    _promo_open(monkeypatch, credits=500)
    _, token, user_id = _register(client)
    resp = client.patch("/api/v1/auth/me", headers=_auth(token), json={
        "full_name": "Legit Name", "promo_credits_remaining": 999999,
        "promo_expires_at": "2099-01-01T00:00:00Z", "credit_balance": 999999,
    })
    assert resp.status_code == 200
    wallet = db.query(UserWallet).filter(UserWallet.user_id == user_id).one()
    db.refresh(wallet)
    assert wallet.credit_balance == 500
    assert wallet.promo_credits_remaining == 500


def test_unspent_promo_credits_are_removed_after_the_window(client, db, monkeypatch):
    from app.models.wallet import UserWallet
    from app.services.wallet.wallet_service import expire_promo_credits_if_due

    _promo_open(monkeypatch, credits=500)
    _, _, user_id = _register(client)
    wallet = db.query(UserWallet).filter(UserWallet.user_id == user_id).one()
    wallet.promo_expires_at = datetime.now(timezone.utc) - timedelta(days=1)
    db.commit()

    assert expire_promo_credits_if_due(wallet, db) == 500
    db.refresh(wallet)
    assert wallet.credit_balance == 0
    assert wallet.promo_credits_remaining == 0
    assert wallet.promo_expires_at is None


def test_expiry_never_takes_purchased_credits(client, db, monkeypatch):
    """A user who bought credits must keep them when the promo lapses."""
    from app.models.wallet import UserWallet
    from app.services.wallet.wallet_service import add_credits, expire_promo_credits_if_due

    _promo_open(monkeypatch, credits=500)
    _, _, user_id = _register(client)
    add_credits(user_id, 200, db, description="purchased")

    wallet = db.query(UserWallet).filter(UserWallet.user_id == user_id).one()
    assert wallet.credit_balance == 700
    wallet.promo_expires_at = datetime.now(timezone.utc) - timedelta(days=1)
    db.commit()

    expire_promo_credits_if_due(wallet, db)
    db.refresh(wallet)
    assert wallet.credit_balance == 200, "expiry ate credits the user paid for"


def test_spending_draws_down_promo_credits_first(client, db, monkeypatch):
    from app.models.wallet import UserWallet
    from app.services.wallet.wallet_service import add_credits, deduct_credits

    _promo_open(monkeypatch, credits=500)
    _, _, user_id = _register(client)
    verify_user(db, user_id)   # deduct_credits refuses unverified accounts
    add_credits(user_id, 200, db, description="purchased")

    deduct_credits(user_id, "mentor_chat", db)   # costs 2
    wallet = db.query(UserWallet).filter(UserWallet.user_id == user_id).one()
    db.refresh(wallet)
    assert wallet.credit_balance == 698
    assert wallet.promo_credits_remaining == 498, "spend should hit promo credits first"


def test_expired_promo_credits_are_not_spendable(client, db, monkeypatch):
    """The balance must not merely display as zero — an AI action after
    expiry has to be refused."""
    from fastapi import HTTPException
    from app.models.wallet import UserWallet
    from app.services.wallet.wallet_service import deduct_credits

    _promo_open(monkeypatch, credits=500)
    _, _, user_id = _register(client)
    verify_user(db, user_id)   # deduct_credits refuses unverified accounts
    wallet = db.query(UserWallet).filter(UserWallet.user_id == user_id).one()
    wallet.promo_expires_at = datetime.now(timezone.utc) - timedelta(days=1)
    db.commit()

    with pytest.raises(HTTPException) as exc:
        deduct_credits(user_id, "mentor_chat", db)
    assert exc.value.status_code == 402


def test_promo_does_not_unlock_paid_exams(client, monkeypatch, seeded_exam):
    """Credits and the certification fee are separate paywalls. A promo
    that quietly granted exam access would give away the paid product."""
    _promo_open(monkeypatch, credits=500)
    _, token, _ = _register(client)
    resp = client.post(f"/api/v1/exams/{seeded_exam.id}/start", headers=_auth(token))
    assert resp.status_code == 402


def test_promo_expiry_is_recorded_in_the_ledger(client, db, monkeypatch):
    """Balance must never change without a matching transaction row."""
    from app.models.wallet import UserWallet, WalletTransaction
    from app.services.wallet.wallet_service import expire_promo_credits_if_due

    _promo_open(monkeypatch, credits=500)
    _, _, user_id = _register(client)
    wallet = db.query(UserWallet).filter(UserWallet.user_id == user_id).one()
    wallet.promo_expires_at = datetime.now(timezone.utc) - timedelta(days=1)
    db.commit()
    expire_promo_credits_if_due(wallet, db)

    tx = (
        db.query(WalletTransaction)
        .filter(WalletTransaction.wallet_id == wallet.id,
                WalletTransaction.action_type == "promo_expiry")
        .one()
    )
    assert tx.credits == -500
    assert tx.balance_after == 0


# ─────────────────────────────────────────────────────────────────────────
# 18. Retired content must not linger on a dashboard
#
# GET /tracks/{slug} and GET /tool-courses/{slug} both filter on
# is_active, so an enrollment card for a retired track is a card that
# 404s when clicked. The enrollment row is deliberately kept — this is
# about what the dashboard shows, not about destroying history.
# ─────────────────────────────────────────────────────────────────────────

def test_my_enrollments_hides_retired_tracks(client, db):
    from app.models.learning import CareerTrack
    from app.models.progress import Enrollment

    suffix = uuid.uuid4().hex[:8]
    track = CareerTrack(slug=f"retire-{suffix}", title="Retiring Track", estimated_weeks=1)
    db.add(track)
    db.commit()
    db.refresh(track)

    _, token, user_id = _register(client)
    db.add(Enrollment(user_id=user_id, track_id=track.id, is_active=True))
    db.commit()

    listed = client.get("/api/v1/tracks/my-enrollments", headers=_auth(token)).json()
    assert any(e["track_id"] == track.id for e in listed), "active track should be listed"

    track.is_active = False
    db.commit()

    listed = client.get("/api/v1/tracks/my-enrollments", headers=_auth(token)).json()
    assert not any(e["track_id"] == track.id for e in listed), \
        "retired track still shows on the dashboard"

    # And the detail route agrees, so there is no card pointing at a 404.
    assert client.get(f"/api/v1/tracks/retire-{suffix}", headers=_auth(token)).status_code == 404

    # The enrollment row itself survives — re-activating restores the card.
    track.is_active = True
    db.commit()
    listed = client.get("/api/v1/tracks/my-enrollments", headers=_auth(token)).json()
    assert any(e["track_id"] == track.id for e in listed), \
        "re-activating a track should bring the existing enrollment back"


def test_my_enrollments_hides_retired_tool_courses(client, db):
    from app.models.tool_course import ToolCourse, ToolEnrollment

    suffix = uuid.uuid4().hex[:8]
    course = ToolCourse(slug=f"retire-tool-{suffix}", title="Retiring Tool")
    db.add(course)
    db.commit()
    db.refresh(course)

    _, token, user_id = _register(client)
    db.add(ToolEnrollment(user_id=user_id, tool_course_id=course.id))
    db.commit()

    listed = client.get("/api/v1/tool-courses/my-enrollments", headers=_auth(token)).json()
    assert any(e["tool_course_id"] == course.id for e in listed)

    course.is_active = False
    db.commit()

    listed = client.get("/api/v1/tool-courses/my-enrollments", headers=_auth(token)).json()
    assert not any(e["tool_course_id"] == course.id for e in listed), \
        "retired tool course still shows on the dashboard"
    assert client.get(f"/api/v1/tool-courses/retire-tool-{suffix}",
                      headers=_auth(token)).status_code == 404
