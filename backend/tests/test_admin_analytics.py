"""
Tests for the admin analytics endpoints.

Two themes:

  1. Authorization. These endpoints read the whole product's data and, in
     the drill-down case, one named learner's record — so the tests are
     written from the attacker's side like test_security.py: anonymous and
     student callers must be refused, and a student must not be able to
     read even their OWN analytics through the admin route.

  2. Arithmetic. The test database accumulates rows across the session, so
     every count is asserted as a DELTA around a known change rather than
     an absolute — an absolute assertion here would pass or fail depending
     on which tests ran first.
"""
import logging
import uuid

import pytest

from app.models.exam import Certificate  # noqa: F401  (kept in the mapper graph)
from app.models.learning import CareerTrack, Quiz, TrackLevel, Topic
from app.models.progress import ProgressStatus, QuizAttempt, UserProgress
from app.models.user import User, UserRole
from app.models.wallet import (
    TransactionStatus, TransactionType, UserWallet, WalletTransaction,
)

OVERVIEW = "/api/v1/admin/analytics/overview"
DRILLDOWN = "/api/v1/admin/analytics/users"
STRONG_PASSWORD = "correct-horse-battery-staple-7"


# ─── helpers ──────────────────────────────────────────────────────────────

def _register(client, full_name="Analytics Tester"):
    email = f"an-{uuid.uuid4().hex[:12]}@example.com"
    resp = client.post("/api/v1/auth/register", json={
        "email": email, "full_name": full_name, "password": STRONG_PASSWORD,
    })
    assert resp.status_code == 201, resp.text
    body = resp.json()
    return email, body["access_token"], body["user"]["id"]


def _auth(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def _make_admin(db, user_id: int) -> None:
    db.query(User).filter(User.id == user_id).update({User.role: UserRole.admin})
    db.commit()


@pytest.fixture()
def security_logger():
    """Re-enable the "security" logger for the duration of one test.

    Test-harness artifact, not a product bug: the session-scoped migration
    fixture runs Alembic, whose env.py calls logging.config.fileConfig(),
    and that disables every logger that already existed — including the one
    app.core.security_log created when conftest imported app.main. The
    running application never migrates in-process, so its audit log is
    unaffected; this fixture just undoes the collateral damage so the audit
    line is actually observable here.
    """
    logger = logging.getLogger("security")
    was_disabled = logger.disabled
    logger.disabled = False
    yield logger
    logger.disabled = was_disabled


@pytest.fixture()
def admin(client, db):
    """A registered admin plus their auth header."""
    _email, token, user_id = _register(client, full_name="Analytics Admin")
    _make_admin(db, user_id)
    return {"id": user_id, "token": token, "headers": _auth(token)}


def _overview(client, admin) -> dict:
    resp = client.get(OVERVIEW, headers=admin["headers"])
    assert resp.status_code == 200, resp.text
    return resp.json()


def _wallet_for(db, user_id: int) -> UserWallet:
    """Registration already creates a wallet; reuse it rather than racing
    the unique constraint on user_wallets.user_id."""
    wallet = db.query(UserWallet).filter(UserWallet.user_id == user_id).first()
    if not wallet:
        wallet = UserWallet(user_id=user_id, credit_balance=0)
        db.add(wallet)
        db.commit()
        db.refresh(wallet)
    return wallet


def _spend(db, user_id: int, action_type: str, cost: int) -> None:
    """Mirror what wallet_service.deduct_credits writes: a deduction row
    with negative credits and the action that caused it."""
    wallet = _wallet_for(db, user_id)
    db.add(WalletTransaction(
        wallet_id=wallet.id,
        transaction_type=TransactionType.deduction,
        status=TransactionStatus.confirmed,
        credits=-cost,
        description=f"Used {action_type}",
        action_type=action_type,
        balance_after=wallet.credit_balance,
    ))
    db.commit()


def _make_topic(db, title: str) -> Topic:
    track = CareerTrack(slug=f"t-{uuid.uuid4().hex[:8]}", title="Analytics Track")
    db.add(track)
    db.flush()
    level = TrackLevel(track_id=track.id, title="Level 1", order=1)
    db.add(level)
    db.flush()
    topic = Topic(level_id=level.id, title=title, slug=f"s-{uuid.uuid4().hex[:8]}", order=1)
    db.add(topic)
    db.commit()
    db.refresh(topic)
    return topic


# ─────────────────────────────────────────────────────────────────────────
# 1. Authorization
# ─────────────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("path", [OVERVIEW, f"{DRILLDOWN}/1"])
def test_analytics_rejects_anonymous(client, path):
    assert client.get(path).status_code == 401


@pytest.mark.parametrize("path", [OVERVIEW, f"{DRILLDOWN}/1"])
def test_analytics_rejects_student(client, path):
    _email, token, _uid = _register(client)
    assert client.get(path, headers=_auth(token)).status_code == 403


def test_analytics_rejects_mentor_role(client, db):
    """Only `admin` passes require_admin — `mentor` is still a non-admin."""
    _email, token, user_id = _register(client)
    db.query(User).filter(User.id == user_id).update({User.role: UserRole.mentor})
    db.commit()
    assert client.get(OVERVIEW, headers=_auth(token)).status_code == 403


def test_student_cannot_read_their_own_analytics_via_admin_route(client, db):
    """The drill-down takes a user_id in the path, which is exactly the
    shape an IDOR takes. Being the subject of the record grants nothing:
    authorization is the admin role, not ownership."""
    _email, token, user_id = _register(client)
    resp = client.get(f"{DRILLDOWN}/{user_id}", headers=_auth(token))
    assert resp.status_code == 403


def test_admin_reaches_both_endpoints(client, admin):
    assert client.get(OVERVIEW, headers=admin["headers"]).status_code == 200
    assert client.get(
        f"{DRILLDOWN}/{admin['id']}", headers=admin["headers"]
    ).status_code == 200


def test_demoting_an_admin_revokes_access_immediately(client, db, admin):
    """The role is read from the database row on every request, so a
    demotion takes effect without waiting for the token to expire."""
    assert client.get(OVERVIEW, headers=admin["headers"]).status_code == 200
    db.query(User).filter(User.id == admin["id"]).update({User.role: UserRole.student})
    db.commit()
    assert client.get(OVERVIEW, headers=admin["headers"]).status_code == 403


# ─────────────────────────────────────────────────────────────────────────
# 2. Overview — shape, arithmetic, and what it must NOT contain
# ─────────────────────────────────────────────────────────────────────────

def test_overview_shape(client, admin):
    body = _overview(client, admin)
    assert set(body) == {
        "generated_at", "users", "activation", "learning", "ai_usage", "retention",
    }
    assert set(body["users"]) >= {
        "total", "new_today", "new_last_7_days", "new_last_30_days", "verified",
    }
    assert set(body["learning"]) == {
        "lessons_completed", "exercises_completed",
        "most_started_topics", "most_completed_topics",
    }


def test_overview_counts_new_signups(client, admin, db):
    before = _overview(client, admin)["users"]
    _register(client)
    _register(client)
    after = _overview(client, admin)["users"]

    assert after["total"] == before["total"] + 2
    assert after["new_today"] == before["new_today"] + 2
    assert after["new_last_7_days"] == before["new_last_7_days"] + 2
    assert after["new_last_30_days"] == before["new_last_30_days"] + 2


def test_overview_activation_and_learning_totals(client, admin, db):
    before = _overview(client, admin)
    _email, _token, user_id = _register(client)

    db.add(UserProgress(
        user_id=user_id,
        status=ProgressStatus.in_progress,
        lessons_completed=[1, 2, 3],
        exercises_completed=[7],
    ))
    db.commit()

    after = _overview(client, admin)
    assert after["activation"]["started_learning"] == \
        before["activation"]["started_learning"] + 1
    assert after["activation"]["completed_first_lesson"] == \
        before["activation"]["completed_first_lesson"] + 1
    assert after["learning"]["lessons_completed"] == \
        before["learning"]["lessons_completed"] + 3
    assert after["learning"]["exercises_completed"] == \
        before["learning"]["exercises_completed"] + 1
    # signed_up is the same population as users.total.
    assert after["activation"]["signed_up"] == after["users"]["total"]


def test_started_learning_does_not_imply_completed_first_lesson(client, admin, db):
    """A progress row with an empty lesson list counts as started, not as
    a first lesson completed — otherwise the funnel could not narrow."""
    before = _overview(client, admin)["activation"]
    _email, _token, user_id = _register(client)
    db.add(UserProgress(user_id=user_id, status=ProgressStatus.in_progress))
    db.commit()

    after = _overview(client, admin)["activation"]
    assert after["started_learning"] == before["started_learning"] + 1
    assert after["completed_first_lesson"] == before["completed_first_lesson"]


def test_null_json_columns_do_not_break_the_overview(client, admin, db):
    """Rows predating the JSON defaults carry NULL. json_array_length would
    raise on those; the endpoint must simply count them as zero."""
    _email, _token, user_id = _register(client)
    db.add(UserProgress(
        user_id=user_id, status=ProgressStatus.in_progress,
        lessons_completed=None, exercises_completed=None,
    ))
    db.commit()
    assert client.get(OVERVIEW, headers=admin["headers"]).status_code == 200


def test_overview_topic_leaderboards(client, admin, db):
    title = f"Analytics Topic {uuid.uuid4().hex[:6]}"
    topic = _make_topic(db, title)
    _e1, _t1, u1 = _register(client)
    _e2, _t2, u2 = _register(client)

    db.add(UserProgress(user_id=u1, topic_id=topic.id, status=ProgressStatus.in_progress,
                        lessons_completed=[1]))
    db.add(UserProgress(user_id=u2, topic_id=topic.id, status=ProgressStatus.completed,
                        lessons_completed=[1]))
    db.commit()

    learning = _overview(client, admin)["learning"]
    started = {row["topic"]: row["count"] for row in learning["most_started_topics"]}
    completed = {row["topic"]: row["count"] for row in learning["most_completed_topics"]}

    assert started[title] == 2
    assert completed[title] == 1
    # Bounded — the dashboard shows a leaderboard, not the catalogue.
    assert len(learning["most_started_topics"]) <= 10
    assert len(learning["most_completed_topics"]) <= 10


def test_overview_ai_credit_burn(client, admin, db):
    before = _overview(client, admin)["ai_usage"]
    _email, _token, user_id = _register(client)
    _spend(db, user_id, "mentor_chat", 2)
    _spend(db, user_id, "mentor_chat", 2)
    _spend(db, user_id, "code_review", 5)

    after = _overview(client, admin)["ai_usage"]
    assert after["total_credits_burned"] == before["total_credits_burned"] + 9

    delta_chat = (after["credits_by_feature"].get("mentor_chat", 0)
                  - before["credits_by_feature"].get("mentor_chat", 0))
    delta_review = (after["credits_by_feature"].get("code_review", 0)
                    - before["credits_by_feature"].get("code_review", 0))
    assert delta_chat == 4
    assert delta_review == 5


def test_signup_credit_grant_is_not_counted_as_burn(client, admin, db):
    """Registration grants starter credits (a topup/bonus row). Only
    deductions are AI spend; counting the grant would invert the sign."""
    before = _overview(client, admin)["ai_usage"]["total_credits_burned"]
    _register(client)
    after = _overview(client, admin)["ai_usage"]["total_credits_burned"]
    assert after == before


def test_overview_exposes_no_user_identifiers(client, admin, db):
    """The aggregate endpoint is identity-free by design: no email, no
    name, no user id anywhere in the payload."""
    email, _token, user_id = _register(client, full_name="Zaphod Beeblebrox")
    _spend(db, user_id, "mentor_chat", 2)
    db.add(UserProgress(user_id=user_id, status=ProgressStatus.in_progress,
                        lessons_completed=[1]))
    db.commit()

    resp = client.get(OVERVIEW, headers=admin["headers"])
    raw = resp.text
    assert email not in raw
    assert "Zaphod" not in raw
    assert "@" not in raw

    # No identity-shaped field anywhere in the tree, at any depth.
    def _keys(node):
        if isinstance(node, dict):
            for key, value in node.items():
                yield key
                yield from _keys(value)
        elif isinstance(node, list):
            for item in node:
                yield from _keys(item)

    forbidden = {"user_id", "email", "full_name", "name", "users_list", "id"}
    assert not (set(_keys(resp.json())) & forbidden)


def test_overview_reports_retention_as_unavailable(client, admin):
    retention = _overview(client, admin)["retention"]
    assert retention["available"] is False
    assert retention["reason"]
    # Never a fabricated number.
    assert retention["d1"] is None and retention["d7"] is None and retention["d30"] is None


def test_overview_flags_verification_when_email_is_unconfigured(client, admin, monkeypatch):
    from app.core.config import settings

    monkeypatch.setattr(settings, "RESEND_API_KEY", None)
    users = _overview(client, admin)["users"]
    assert users["verification_reliable"] is False
    assert "RESEND_API_KEY" in users["verification_note"]

    monkeypatch.setattr(settings, "RESEND_API_KEY", "re_test_key")
    users = _overview(client, admin)["users"]
    assert users["verification_reliable"] is True
    assert users["verification_note"] is None


# ─────────────────────────────────────────────────────────────────────────
# 3. User drill-down
# ─────────────────────────────────────────────────────────────────────────

def test_drilldown_unknown_user_is_404(client, admin):
    resp = client.get(f"{DRILLDOWN}/99999999", headers=admin["headers"])
    assert resp.status_code == 404


def test_drilldown_for_a_user_with_no_activity(client, admin):
    """Missing data must read as zero, not as a crash."""
    email, _token, user_id = _register(client, full_name="Quiet Learner")
    body = client.get(f"{DRILLDOWN}/{user_id}", headers=admin["headers"]).json()

    assert body["user_id"] == user_id
    assert body["email"] == email
    assert body["full_name"] == "Quiet Learner"
    assert body["role"] == "student"
    assert body["signed_up_at"]
    assert body["topics_started"] == 0
    assert body["lessons_completed"] == 0
    assert body["exercises_completed"] == 0
    assert body["study_minutes"] == 0
    assert body["quiz_attempts"] == 0
    assert body["exam_attempts"] == 0
    assert body["certificates"] == 0
    assert body["credits_spent"] == 0
    assert body["credits_by_feature"] == {}
    assert body["recent_activity"] == []


def test_drilldown_aggregates_one_users_activity(client, admin, db):
    _email, _token, user_id = _register(client)
    topic = _make_topic(db, f"Drilldown Topic {uuid.uuid4().hex[:6]}")

    db.add(UserProgress(
        user_id=user_id, topic_id=topic.id, status=ProgressStatus.completed,
        lessons_completed=[1, 2], exercises_completed=[3], time_spent_minutes=45,
    ))
    quiz = Quiz(topic_id=topic.id, title="Analytics Quiz", questions=[])
    db.add(quiz)
    db.flush()
    db.add(QuizAttempt(user_id=user_id, quiz_id=quiz.id, answers={}, score=90.0, passed=True))
    db.add(QuizAttempt(user_id=user_id, quiz_id=quiz.id, answers={}, score=40.0, passed=False))
    db.commit()
    _spend(db, user_id, "mentor_chat", 2)
    _spend(db, user_id, "roadmap", 5)

    body = client.get(f"{DRILLDOWN}/{user_id}", headers=admin["headers"]).json()
    assert body["topics_started"] == 1
    assert body["topics_completed"] == 1
    assert body["lessons_completed"] == 2
    assert body["exercises_completed"] == 1
    assert body["study_minutes"] == 45
    assert body["quiz_attempts"] == 2
    assert body["quizzes_passed"] == 1
    assert body["credits_spent"] == 7
    assert body["credits_by_feature"] == {"roadmap": 5, "mentor_chat": 2}

    kinds = {item["type"] for item in body["recent_activity"]}
    assert kinds == {"quiz_attempt", "ai_usage"}
    assert all(item["at"] and item["detail"] for item in body["recent_activity"])


def test_drilldown_scopes_to_the_requested_user_only(client, admin, db):
    """Two learners with activity: each drill-down reports only its own."""
    _e1, _t1, u1 = _register(client)
    _e2, _t2, u2 = _register(client)
    _spend(db, u1, "mentor_chat", 2)
    _spend(db, u2, "code_review", 5)
    _spend(db, u2, "code_review", 5)

    first = client.get(f"{DRILLDOWN}/{u1}", headers=admin["headers"]).json()
    second = client.get(f"{DRILLDOWN}/{u2}", headers=admin["headers"]).json()

    assert first["credits_spent"] == 2
    assert first["credits_by_feature"] == {"mentor_chat": 2}
    assert second["credits_spent"] == 10
    assert second["credits_by_feature"] == {"code_review": 10}


def test_drilldown_recent_activity_is_bounded(client, admin, db):
    _email, _token, user_id = _register(client)
    topic = _make_topic(db, f"Bounded Topic {uuid.uuid4().hex[:6]}")
    quiz = Quiz(topic_id=topic.id, title="Bounded Quiz", questions=[])
    db.add(quiz)
    db.flush()
    for _ in range(30):
        db.add(QuizAttempt(user_id=user_id, quiz_id=quiz.id, answers={},
                           score=50.0, passed=False))
    db.commit()

    default = client.get(f"{DRILLDOWN}/{user_id}", headers=admin["headers"]).json()
    assert len(default["recent_activity"]) == 20

    smaller = client.get(f"{DRILLDOWN}/{user_id}?limit=5", headers=admin["headers"]).json()
    assert len(smaller["recent_activity"]) == 5

    # The cap is enforced server-side, not by client good manners.
    assert client.get(f"{DRILLDOWN}/{user_id}?limit=5000",
                      headers=admin["headers"]).status_code == 422


def test_drilldown_is_audited(client, admin, db, caplog, security_logger):
    _email, _token, user_id = _register(client)

    with caplog.at_level(logging.WARNING, logger="security"):
        resp = client.get(f"{DRILLDOWN}/{user_id}", headers=admin["headers"])
    assert resp.status_code == 200

    lines = [r.getMessage() for r in caplog.records if r.name == "security"]
    audit = [ln for ln in lines if "admin.action" in ln and "analytics.view_user" in ln]
    assert len(audit) == 1, lines
    # Who looked, who was looked at, and what happened. The timestamp is
    # the log record's own.
    assert f"admin_id={admin['id']}" in audit[0]
    assert f"user={user_id}" in audit[0]
    # Never the subject's credentials or contact details.
    assert "password" not in audit[0].lower()
    assert "@" not in audit[0]


def test_overview_is_not_audited_as_individual_access(client, admin, caplog, security_logger):
    """Aggregates name nobody, so they must not fill the audit log with
    noise that would drown the accesses that do matter."""
    with caplog.at_level(logging.WARNING, logger="security"):
        assert client.get(OVERVIEW, headers=admin["headers"]).status_code == 200
    lines = [r.getMessage() for r in caplog.records if r.name == "security"]
    assert not [ln for ln in lines if "analytics.view_user" in ln]
