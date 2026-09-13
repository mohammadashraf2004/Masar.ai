"""
IDOR/BOLA regression tests for the challenge subsystem.

challenge_controller has no endpoint that takes a client-supplied
attempt_id at all — enroll/submit/hint/attempts all re-derive "which
attempt" from (current_user.id, challenge slug) alone. That is a stronger
position than an id-based lookup (there is no id for an attacker to
substitute), but it still needs a test proving it holds: these exercise
the same attacker-vs-victim shape as the existing mentor-session/exam
IDOR tests in test_security.py, calling the API directly.
"""
import uuid

import pytest

from app.controllers import challenge_controller
from app.models.challenge import ChallengeAttempt, ChallengeDifficulty, ChallengeProject, ChallengeStatus
from app.services.wallet.wallet_service import add_credits
from tests.conftest import verify_registered

STRONG_PASSWORD = "correct-horse-battery-staple-7"
ENROLL_COST = 25

FAKE_GRADE = {
    "criteria_scores": [{"criterion": "dedup", "score": 90, "feedback": "good", "passed": True}],
    "overall_feedback": "Nice work.",
    "strengths": [], "improvements": [],
}
FAKE_HINT = {"hint": "Look at the dates.", "concept": "Normalisation", "next_step": "Normalise them."}


def _register(client):
    email = f"chal-idor-{uuid.uuid4().hex[:12]}@example.com"
    resp = client.post("/api/v1/auth/register", json={
        "email": email, "full_name": "Attacker Or Victim", "password": STRONG_PASSWORD,
    })
    assert resp.status_code == 201, resp.text
    body = resp.json()
    verify_registered(client, body["user"]["id"])
    return body["access_token"], body["user"]["id"]


def _auth(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture()
def challenge(db) -> ChallengeProject:
    ch = ChallengeProject(
        title="IDOR Challenge",
        slug=f"idor-chal-{uuid.uuid4().hex[:8]}",
        description="Clean it.",
        difficulty=ChallengeDifficulty.beginner,
        credit_cost=ENROLL_COST,
        passing_score=70.0,
        max_attempts=3,
        is_active=True,
        dirty_dataset=[{"a": 1}, {"a": 2}],
        dataset_description="Dirty.",
        grading_rubric=[{"criterion": "dedup", "weight": 100}],
        hints=["hint one"],
        tags=[],
    )
    db.add(ch)
    db.commit()
    db.refresh(ch)
    return ch


@pytest.fixture()
def stub_grader(monkeypatch):
    monkeypatch.setattr(challenge_controller, "get_llm", lambda: object())
    monkeypatch.setattr(challenge_controller, "grade_submission", lambda *a, **kw: dict(FAKE_GRADE))


@pytest.fixture()
def stub_hint(monkeypatch):
    monkeypatch.setattr(challenge_controller, "get_llm", lambda: object())
    monkeypatch.setattr(challenge_controller, "get_challenge_hint", lambda **kw: dict(FAKE_HINT))


def _fund(db, user_id, amount=1000):
    add_credits(user_id, amount, db, description="test funds")


# ─────────────────────────────────────────────────────────────────────────
# 1. Enrolling twice (as two different users) never mixes up attempts
# ─────────────────────────────────────────────────────────────────────────

def test_two_users_enrolling_get_independent_attempts(client, db, challenge):
    victim_token, victim_id = _register(client)
    attacker_token, attacker_id = _register(client)
    _fund(db, victim_id)
    _fund(db, attacker_id)

    v = client.post(f"/api/v1/challenges/{challenge.slug}/enroll", headers=_auth(victim_token))
    a = client.post(f"/api/v1/challenges/{challenge.slug}/enroll", headers=_auth(attacker_token))
    assert v.status_code == a.status_code == 200
    assert v.json()["attempt_id"] != a.json()["attempt_id"]

    victim_attempt = db.query(ChallengeAttempt).filter(
        ChallengeAttempt.id == v.json()["attempt_id"]
    ).one()
    attacker_attempt = db.query(ChallengeAttempt).filter(
        ChallengeAttempt.id == a.json()["attempt_id"]
    ).one()
    assert victim_attempt.user_id == victim_id
    assert attacker_attempt.user_id == attacker_id


# ─────────────────────────────────────────────────────────────────────────
# 2. Submitting a solution only ever touches the caller's own attempt
# ─────────────────────────────────────────────────────────────────────────

def test_submitting_a_solution_never_grades_another_users_attempt(client, db, challenge, stub_grader):
    """There is no attempt_id in the submit payload — the attacker's own
    submission must resolve to the attacker's own (freshly enrolled)
    attempt, never the victim's, even though both share a challenge."""
    victim_token, victim_id = _register(client)
    attacker_token, attacker_id = _register(client)
    _fund(db, victim_id)
    _fund(db, attacker_id)

    client.post(f"/api/v1/challenges/{challenge.slug}/enroll", headers=_auth(victim_token))
    client.post(f"/api/v1/challenges/{challenge.slug}/enroll", headers=_auth(attacker_token))

    resp = client.post(
        f"/api/v1/challenges/{challenge.slug}/submit",
        headers=_auth(attacker_token),
        json={"solution_code": "attacker's code", "solution_notes": "mine"},
    )
    assert resp.status_code == 200, resp.text

    victim_attempt = db.query(ChallengeAttempt).filter(
        ChallengeAttempt.user_id == victim_id, ChallengeAttempt.challenge_id == challenge.id,
    ).one()
    attacker_attempt = db.query(ChallengeAttempt).filter(
        ChallengeAttempt.user_id == attacker_id, ChallengeAttempt.challenge_id == challenge.id,
    ).one()

    assert attacker_attempt.solution_code == "attacker's code"
    assert attacker_attempt.status == ChallengeStatus.passed
    # The victim's attempt must be completely untouched by the attacker's
    # submission — still enrolled, no solution recorded.
    assert victim_attempt.solution_code is None
    assert victim_attempt.status == ChallengeStatus.enrolled


def test_submitting_without_enrolling_does_not_reach_or_grade_anyone_elses_attempt(
    client, db, challenge, stub_grader,
):
    """An attacker who never enrolled must be refused outright — not
    silently graded against whichever attempt happens to exist for that
    challenge."""
    victim_token, victim_id = _register(client)
    attacker_token, _ = _register(client)
    _fund(db, victim_id)

    client.post(f"/api/v1/challenges/{challenge.slug}/enroll", headers=_auth(victim_token))

    resp = client.post(
        f"/api/v1/challenges/{challenge.slug}/submit",
        headers=_auth(attacker_token),
        json={"solution_code": "not enrolled"},
    )
    assert resp.status_code == 400

    victim_attempt = db.query(ChallengeAttempt).filter(
        ChallengeAttempt.user_id == victim_id
    ).one()
    assert victim_attempt.solution_code is None


# ─────────────────────────────────────────────────────────────────────────
# 3. Listing "my attempts" never includes another user's rows
# ─────────────────────────────────────────────────────────────────────────

def test_my_attempts_never_lists_another_users_attempts(client, db, challenge, stub_grader):
    victim_token, victim_id = _register(client)
    attacker_token, attacker_id = _register(client)
    _fund(db, victim_id)
    _fund(db, attacker_id)

    client.post(f"/api/v1/challenges/{challenge.slug}/enroll", headers=_auth(victim_token))
    client.post(
        f"/api/v1/challenges/{challenge.slug}/submit", headers=_auth(victim_token),
        json={"solution_code": "victim's secret approach"},
    )
    client.post(f"/api/v1/challenges/{challenge.slug}/enroll", headers=_auth(attacker_token))

    resp = client.get(f"/api/v1/challenges/{challenge.slug}/attempts", headers=_auth(attacker_token))
    assert resp.status_code == 200
    ids = [a["id"] for a in resp.json()]
    victim_attempt_id = db.query(ChallengeAttempt).filter(
        ChallengeAttempt.user_id == victim_id
    ).one().id
    assert victim_attempt_id not in ids
    assert "victim's secret approach" not in resp.text


# ─────────────────────────────────────────────────────────────────────────
# 4. Hints are scoped to the caller's own enrolment
# ─────────────────────────────────────────────────────────────────────────

def test_hint_requires_the_callers_own_enrolment_not_anyone_elses(client, db, challenge, stub_hint):
    """A hint costs a credit and must be attributed to (and paid by) the
    caller — an attacker cannot ride a victim's enrolment to get hints
    without ever enrolling themselves."""
    victim_token, victim_id = _register(client)
    attacker_token, attacker_id = _register(client)
    _fund(db, victim_id)
    _fund(db, attacker_id)

    client.post(f"/api/v1/challenges/{challenge.slug}/enroll", headers=_auth(victim_token))

    resp = client.post(
        f"/api/v1/challenges/{challenge.slug}/hint",
        headers=_auth(attacker_token),
        json={"stuck_on": "x", "previous_hints": []},
    )
    assert resp.status_code == 403, "an unenrolled user must not get hints off someone else's enrolment"


def test_dataset_download_requires_the_callers_own_enrolment(client, db, challenge):
    victim_token, victim_id = _register(client)
    attacker_token, _ = _register(client)
    _fund(db, victim_id)

    client.post(f"/api/v1/challenges/{challenge.slug}/enroll", headers=_auth(victim_token))

    resp = client.get(
        f"/api/v1/challenges/{challenge.slug}/dataset/download", headers=_auth(attacker_token),
    )
    assert resp.status_code == 403
