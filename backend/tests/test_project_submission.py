"""
Project submission: code in, review out, hints when stuck.

These cover the contract change from "paste a GitHub URL" to "write the
code", plus the credit-metered hint endpoint that came with it.

The LLM is always stubbed. Nothing here should reach a provider: the tests
assert what the endpoint does with a review, not what a model writes.
"""
import uuid

import pytest

from app.controllers import tracks_controller
from app.models.learning import CareerTrack, Project, Topic, TrackLevel
from app.models.progress import ProjectSubmission
from app.models.wallet import TransactionType, UserWallet, WalletTransaction
from app.services import code_review_service

STRONG_PASSWORD = "correct-horse-battery-staple-7"

FAKE_REVIEW = {
    "overall_quality": "good",
    "score": 82,
    "issues": [],
    "strengths": ["reads clearly"],
    "improvements": ["handle the empty case"],
    "summary": "Solid first pass.",
}

FAKE_HINT = {
    "hint": "Look at how you are joining the two frames.",
    "concept": "pandas.merge",
    "next_step": "Print the row count before and after the merge.",
}


# ─── helpers ──────────────────────────────────────────────────────────────

def _register(client):
    email = f"proj-{uuid.uuid4().hex[:12]}@example.com"
    resp = client.post("/api/v1/auth/register", json={
        "email": email, "full_name": "Project Tester", "password": STRONG_PASSWORD,
    })
    assert resp.status_code == 201, resp.text
    body = resp.json()
    return body["access_token"], body["user"]["id"]


def _auth(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture()
def project(db) -> Project:
    track = CareerTrack(slug=f"pt-{uuid.uuid4().hex[:8]}", title="Project Track")
    db.add(track)
    db.flush()
    level = TrackLevel(track_id=track.id, title="Level 1", order=1)
    db.add(level)
    db.flush()
    topic = Topic(level_id=level.id, title="Topic", slug=f"pts-{uuid.uuid4().hex[:8]}", order=1)
    db.add(topic)
    db.flush()
    proj = Project(
        topic_id=topic.id,
        title="Build an ETL pipeline",
        description="Clean the dataset and load it.",
        objectives=["Deduplicate rows", "Write to Postgres"],
        tech_stack=["Python", "pandas"],
    )
    db.add(proj)
    db.commit()
    db.refresh(proj)
    return proj


@pytest.fixture()
def stub_review(monkeypatch):
    """Stub the reviewer and the provider factory. Both are needed: the
    controller calls get_llm() before review_code()."""
    monkeypatch.setattr(tracks_controller, "get_llm", lambda: object())
    monkeypatch.setattr(code_review_service, "review_code", lambda **kw: dict(FAKE_REVIEW))
    return FAKE_REVIEW


@pytest.fixture()
def stub_hint(monkeypatch):
    monkeypatch.setattr(tracks_controller, "get_llm", lambda: object())
    monkeypatch.setattr(tracks_controller, "get_project_hint", lambda **kw: dict(FAKE_HINT))
    return FAKE_HINT


def _balance(db, user_id: int) -> int:
    wallet = db.query(UserWallet).filter(UserWallet.user_id == user_id).first()
    return wallet.credit_balance if wallet else 0


# ─────────────────────────────────────────────────────────────────────────
# 1. Submitting code
# ─────────────────────────────────────────────────────────────────────────

def test_submit_stores_code_and_returns_the_review(client, db, project, stub_review):
    token, user_id = _register(client)
    resp = client.post(
        f"/api/v1/tracks/projects/{project.id}/submit",
        headers=_auth(token),
        json={"code": "import pandas as pd\ndf = pd.read_csv('x.csv')", "description": "Used pandas."},
    )
    assert resp.status_code == 200, resp.text
    body = resp.json()

    assert body["code"].startswith("import pandas")
    assert body["description"] == "Used pandas."
    assert body["score"] == 82
    assert body["ai_review"]["summary"] == "Solid first pass."

    row = db.query(ProjectSubmission).filter(ProjectSubmission.id == body["id"]).one()
    assert row.code.startswith("import pandas")
    assert row.user_id == user_id
    assert row.reviewed_at is not None


def test_submitted_code_is_what_gets_reviewed(client, project, monkeypatch):
    """Regression on the actual bug this change fixes: the reviewer used to
    be handed the description, so the code was never read."""
    seen = {}

    def _capture(**kwargs):
        seen.update(kwargs)
        return dict(FAKE_REVIEW)

    monkeypatch.setattr(tracks_controller, "get_llm", lambda: object())
    monkeypatch.setattr(code_review_service, "review_code", _capture)

    token, _uid = _register(client)
    client.post(
        f"/api/v1/tracks/projects/{project.id}/submit",
        headers=_auth(token),
        json={"code": "def solve(): return 42", "description": "my notes"},
    )

    assert seen["code"] == "def solve(): return 42"
    # Notes ride along as context, never as the thing reviewed.
    assert "my notes" in seen["context"]
    assert project.title in seen["context"]


def test_submit_requires_code(client, project, stub_review):
    token, _uid = _register(client)
    base = f"/api/v1/tracks/projects/{project.id}/submit"

    assert client.post(base, headers=_auth(token), json={}).status_code == 422
    assert client.post(base, headers=_auth(token), json={"code": ""}).status_code == 422
    # Whitespace is not code.
    assert client.post(base, headers=_auth(token), json={"code": "   \n  "}).status_code == 422
    # Notes alone are not a submission.
    assert client.post(
        base, headers=_auth(token), json={"description": "I did it, trust me"}
    ).status_code == 422


def test_github_url_is_no_longer_part_of_the_contract(client, db, project, stub_review):
    """The field is gone from the request and the response. A client still
    sending one must not have it stored."""
    token, _uid = _register(client)
    resp = client.post(
        f"/api/v1/tracks/projects/{project.id}/submit",
        headers=_auth(token),
        json={"code": "print(1)", "github_url": "https://github.com/someone/repo"},
    )
    assert resp.status_code == 200, resp.text
    assert "github_url" not in resp.json()

    row = db.query(ProjectSubmission).filter(ProjectSubmission.id == resp.json()["id"]).one()
    assert row.github_url is None


def test_submission_survives_a_reviewer_outage(client, db, project, monkeypatch):
    """A provider failure must not cost the student their work."""
    monkeypatch.setattr(tracks_controller, "get_llm", lambda: object())

    def _boom(**kwargs):
        raise RuntimeError("provider down")

    monkeypatch.setattr(code_review_service, "review_code", _boom)

    token, _uid = _register(client)
    resp = client.post(
        f"/api/v1/tracks/projects/{project.id}/submit",
        headers=_auth(token),
        json={"code": "print('still saved')"},
    )
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["ai_review"] is None
    assert body["score"] is None
    assert body["code"] == "print('still saved')"


def test_oversized_code_is_rejected(client, project, stub_review):
    token, _uid = _register(client)
    resp = client.post(
        f"/api/v1/tracks/projects/{project.id}/submit",
        headers=_auth(token),
        json={"code": "x" * 20_001},
    )
    assert resp.status_code == 422


def test_submit_requires_authentication(client, project):
    resp = client.post(
        f"/api/v1/tracks/projects/{project.id}/submit", json={"code": "print(1)"}
    )
    assert resp.status_code == 401


def test_submissions_list_is_scoped_to_the_caller(client, project, stub_review):
    """Unchanged by this work, asserted because the response shape changed."""
    mine, _uid = _register(client)
    theirs, _uid2 = _register(client)
    client.post(f"/api/v1/tracks/projects/{project.id}/submit",
                headers=_auth(mine), json={"code": "print('mine')"})

    seen = client.get(f"/api/v1/tracks/projects/{project.id}/submissions",
                      headers=_auth(theirs))
    assert seen.status_code == 200
    assert seen.json() == []

    own = client.get(f"/api/v1/tracks/projects/{project.id}/submissions",
                     headers=_auth(mine)).json()
    assert len(own) == 1
    assert own[0]["code"] == "print('mine')"
    assert "github_url" not in own[0]


# ─────────────────────────────────────────────────────────────────────────
# 2. Hints
# ─────────────────────────────────────────────────────────────────────────

def test_hint_returns_guidance_and_charges_one_credit(client, db, project, stub_hint):
    token, user_id = _register(client)
    before = _balance(db, user_id)

    resp = client.post(
        f"/api/v1/tracks/projects/{project.id}/hint",
        headers=_auth(token),
        json={"stuck_on": "my merge duplicates rows", "code": "df.merge(other)"},
    )
    assert resp.status_code == 200, resp.text
    assert resp.json() == FAKE_HINT

    db.expire_all()
    assert _balance(db, user_id) == before - 1

    tx = (
        db.query(WalletTransaction)
        .join(UserWallet, WalletTransaction.wallet_id == UserWallet.id)
        .filter(UserWallet.user_id == user_id,
                WalletTransaction.transaction_type == TransactionType.deduction)
        .one()
    )
    assert tx.action_type == "project_hint"
    assert tx.credits == -1


def test_hint_passes_the_students_code_to_the_tutor(client, project, monkeypatch):
    seen = {}
    monkeypatch.setattr(tracks_controller, "get_llm", lambda: object())
    monkeypatch.setattr(
        tracks_controller, "get_project_hint",
        lambda **kw: (seen.update(kw), dict(FAKE_HINT))[1],
    )

    token, _uid = _register(client)
    client.post(
        f"/api/v1/tracks/projects/{project.id}/hint",
        headers=_auth(token),
        json={"stuck_on": "stuck", "code": "df.merge(other)", "previous_hints": ["earlier one"]},
    )

    assert seen["code"] == "df.merge(other)"
    assert seen["stuck_on"] == "stuck"
    # The request field is `previous_hints`; the service parameter it feeds
    # is `hints_already_given` (same name the challenge hint uses).
    assert seen["hints_already_given"] == ["earlier one"]
    assert seen["project_title"] == project.title
    assert seen["objectives"] == ["Deduplicate rows", "Write to Postgres"]


def test_hint_works_before_any_code_is_written(client, project, stub_hint):
    token, _uid = _register(client)
    resp = client.post(
        f"/api/v1/tracks/projects/{project.id}/hint",
        headers=_auth(token),
        json={"stuck_on": "where do I even start"},
    )
    assert resp.status_code == 200, resp.text


def test_hint_requires_something_to_be_stuck_on(client, project, stub_hint):
    token, _uid = _register(client)
    resp = client.post(
        f"/api/v1/tracks/projects/{project.id}/hint",
        headers=_auth(token), json={"stuck_on": ""},
    )
    assert resp.status_code == 422


def test_hint_requires_authentication(client, project):
    resp = client.post(
        f"/api/v1/tracks/projects/{project.id}/hint", json={"stuck_on": "help"}
    )
    assert resp.status_code == 401


def test_hint_on_unknown_project_is_404_and_costs_nothing(client, db, project, stub_hint):
    token, user_id = _register(client)
    before = _balance(db, user_id)
    resp = client.post(
        "/api/v1/tracks/projects/99999999/hint",
        headers=_auth(token), json={"stuck_on": "help"},
    )
    assert resp.status_code == 404
    db.expire_all()
    assert _balance(db, user_id) == before


def test_hint_refuses_when_the_wallet_is_empty(client, db, project, stub_hint):
    token, user_id = _register(client)
    wallet = db.query(UserWallet).filter(UserWallet.user_id == user_id).one()
    wallet.credit_balance = 0
    db.commit()

    resp = client.post(
        f"/api/v1/tracks/projects/{project.id}/hint",
        headers=_auth(token), json={"stuck_on": "help"},
    )
    assert resp.status_code == 402
    assert resp.json()["detail"]["error"] == "insufficient_credits"


def test_failed_hint_refunds_the_credit(client, db, project, monkeypatch):
    """A student must not pay for a hint the provider never returned."""
    monkeypatch.setattr(tracks_controller, "get_llm", lambda: object())

    def _boom(**kwargs):
        raise RuntimeError("provider down")

    monkeypatch.setattr(tracks_controller, "get_project_hint", _boom)

    token, user_id = _register(client)
    before = _balance(db, user_id)

    resp = client.post(
        f"/api/v1/tracks/projects/{project.id}/hint",
        headers=_auth(token), json={"stuck_on": "help"},
    )
    assert resp.status_code == 503
    db.expire_all()
    assert _balance(db, user_id) == before
