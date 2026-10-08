"""Retired product announcements stay retired for every account."""
import uuid

import pytest

from app.core import releases
from app.models.update_ack import UserUpdateAcknowledgement

from tests.learning_fixtures import *  # noqa: F401,F403
from tests.learning_fixtures import register

ACK = "/api/v1/auth/updates/{}/acknowledge"
ME = "/api/v1/auth/me"
RETIRED = ("2026-09-skill-gap", "2026-09-skill-gap-intro")


def _pending(client, user):
    return client.get(ME, headers=user["headers"]).json()["pending_updates"]


def _rows(db, user_id):
    return sorted(r for (r,) in db.query(UserUpdateAcknowledgement.release_id).filter(
        UserUpdateAcknowledgement.user_id == user_id))


def test_registry_has_no_active_announcements():
    assert releases.KNOWN_RELEASES == set()
    assert releases.pending_updates([]) == []
    assert releases.pending_updates(RETIRED) == []


def test_registration_has_no_retired_announcement(learn_client, learn_db):
    user = register(learn_client)
    assert _rows(learn_db, user["id"]) == []
    assert _pending(learn_client, user) == []


def test_registration_response_has_nothing_pending(learn_client):
    body = learn_client.post("/api/v1/auth/register", json={
        "accept_terms": True,
        "accept_privacy": True,
        "email": f"reg-{uuid.uuid4().hex[:10]}@example.com",
        "full_name": "Reg Tester",
        "password": "correcthorsebatterystaple",
    }).json()
    assert body["user"]["pending_updates"] == []


def test_historical_rows_are_ignored(learn_client, learn_db):
    user = register(learn_client)
    for release_id in RETIRED:
        learn_db.add(UserUpdateAcknowledgement(user_id=user["id"], release_id=release_id))
    learn_db.commit()
    assert _rows(learn_db, user["id"]) == sorted(RETIRED)
    assert _pending(learn_client, user) == []


@pytest.mark.parametrize("release_id", [*RETIRED, "2099-01-future", "whats-new", "0"])
def test_retired_and_unknown_announcements_cannot_be_acknowledged(learn_client, learn_db, release_id):
    user = register(learn_client)
    response = learn_client.post(ACK.format(release_id), headers=user["headers"])
    assert response.status_code == 404
    assert _rows(learn_db, user["id"]) == []
    assert _pending(learn_client, user) == []


def test_acknowledgement_route_requires_authentication(learn_client):
    assert learn_client.post(ACK.format(RETIRED[0])).status_code in (401, 403)


def test_retirement_persists_across_sign_ins(learn_client):
    user = register(learn_client)
    login = learn_client.post("/api/v1/auth/login", json={
        "email": user["email"],
        "password": "correcthorsebatterystaple",
    })
    assert login.status_code == 200, login.text
    assert login.json()["user"]["pending_updates"] == []
