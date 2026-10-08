"""
AI-reviewed project submissions are capped per ACCOUNT: at most 10 in any rolling 24 hours
(release decision 2026-10-07), on top of the route's per-IP limit. Before this, one verified
account rotating source addresses reached the provider without a ceiling.
"""
import asyncio
import threading
from datetime import datetime, timedelta, timezone

import httpx

from app.core.config import settings
from app.db.session import SessionLocal
from app.models.progress import ProjectSubmission
from app.views.learning import ProjectSubmit
from app.controllers.tracks_controller import _reserve_review_slot
from tests.test_project_submission import _auth, _register, project, stub_review  # noqa: F401

LIMIT = settings.PROJECT_REVIEW_LIMIT_PER_DAY


def _submit_from(client, ip: str, token: str, project_id: int):
    """One submission from a distinct client address, like a learner rotating IPs."""
    async def go():
        transport = httpx.ASGITransport(app=client.app, client=(ip, 40000))
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as http:
            return await http.post(f"/api/v1/tracks/projects/{project_id}/submit",
                                   headers=_auth(token), json={"code": "print('hi')"})
    return asyncio.run(go())


def test_ten_reviews_are_allowed_the_eleventh_is_refused_whatever_the_ip(client, db, project, stub_review):
    token, user_id = _register(client)
    statuses = [_submit_from(client, f"203.0.113.{i}", token, project.id).status_code for i in range(1, LIMIT + 1)]
    assert statuses == [200] * LIMIT

    refused = _submit_from(client, "198.51.100.77", token, project.id)  # a fresh address
    assert refused.status_code == 429
    body = refused.json()["detail"]
    assert body["code"] == "PROJECT_REVIEW_LIMIT" and body["limit"] == LIMIT
    assert 0 < int(refused.headers["Retry-After"]) <= 24 * 3600
    assert db.query(ProjectSubmission).filter_by(user_id=user_id).count() == LIMIT


def test_accounts_are_limited_independently(client, db, project, stub_review):
    token_a, user_a = _register(client)
    token_b, _ = _register(client)
    for i in range(LIMIT):
        db.add(ProjectSubmission(user_id=user_a, project_id=project.id, code="x"))
    db.commit()
    assert _submit_from(client, "203.0.113.200", token_a, project.id).status_code == 429
    assert _submit_from(client, "203.0.113.201", token_b, project.id).status_code == 200


def test_the_window_rolls_after_24_hours(client, db, project, stub_review):
    token, user_id = _register(client)
    old = datetime.now(timezone.utc) - timedelta(hours=24, minutes=1)
    for _ in range(LIMIT):
        db.add(ProjectSubmission(user_id=user_id, project_id=project.id, code="x", submitted_at=old))
    db.commit()
    assert _submit_from(client, "203.0.113.210", token, project.id).status_code == 200


def test_requests_that_fail_before_the_provider_are_not_counted(client, db, project, stub_review):
    token, user_id = _register(client)
    for i in range(LIMIT + 3):
        missing = _submit_from(client, f"203.0.113.{100 + i}", token, 999_999_999)
        assert missing.status_code == 404
    invalid = _submit_from(client, "203.0.113.150", token, project.id)
    assert invalid.status_code == 200  # a real submission still has its full allowance
    assert db.query(ProjectSubmission).filter_by(user_id=user_id).count() == 1


def test_a_refused_request_makes_no_provider_call(client, db, project, monkeypatch):
    from app.controllers import tracks_controller
    from app.services import code_review_service

    calls = []
    monkeypatch.setattr(tracks_controller, "get_llm", lambda: object())
    monkeypatch.setattr(code_review_service, "review_code", lambda **kw: calls.append(1) or {"score": 1})
    token, user_id = _register(client)
    for _ in range(LIMIT):
        db.add(ProjectSubmission(user_id=user_id, project_id=project.id, code="x"))
    db.commit()
    assert _submit_from(client, "203.0.113.220", token, project.id).status_code == 429
    assert calls == []


def test_concurrent_requests_cannot_exceed_the_limit(client, db, project):
    _, user_id = _register(client)
    project_id = project.id  # a plain int: threads must not touch the test's session
    payload = ProjectSubmit(code="print('race')")
    barrier, outcomes = threading.Barrier(LIMIT + 5), []

    def reserve():
        session = SessionLocal()
        try:
            barrier.wait()
            _reserve_review_slot(session, user_id, project_id, payload)
            outcomes.append("ok")
        except Exception as exc:  # noqa: BLE001 - the 429 is the expected refusal
            outcomes.append(getattr(exc, "status_code", repr(exc)))
        finally:
            session.close()

    threads = [threading.Thread(target=reserve) for _ in range(LIMIT + 5)]
    for t in threads:
        t.start()
    for t in threads:
        t.join(30)
    assert outcomes.count("ok") == LIMIT and outcomes.count(429) == 5, outcomes
    db.expire_all()
    assert db.query(ProjectSubmission).filter_by(user_id=user_id).count() == LIMIT
