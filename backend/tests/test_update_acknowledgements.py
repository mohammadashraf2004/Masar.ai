"""
Product announcements: which ones an account still has to see, and acknowledging them.

What is pinned here:

  * the server decides what an announcement is: an unknown one is refused, so an
    account cannot pre-dismiss something that has not shipped;
  * an account that predates the release is asked about it (nothing was
    backfilled), and an account created after it is not - it meets the feature
    in its first roadmap instead;
  * acknowledging is idempotent, per account, and persists;
  * acknowledging touches nothing else: not the roadmap, not the skills.
"""
import uuid

import pytest

from app.core import releases
from app.models.update_ack import UserUpdateAcknowledgement
from app.models.user import User

from tests.learning_fixtures import *  # noqa: F401,F403
from tests.learning_fixtures import register

ACK = "/api/v1/auth/updates/{}/acknowledge"
ME = "/api/v1/auth/me"


def _legacy_account(client, db):
    """An account created before the release: registered, then stripped of the
    acknowledgement registration now writes - which is exactly what every row
    that predates the migration looks like."""
    user = register(client)
    db.query(UserUpdateAcknowledgement).filter(UserUpdateAcknowledgement.user_id == user["id"]).delete()
    db.commit()
    db.expire_all()
    return user


def _pending(client, user):
    return client.get(ME, headers=user["headers"]).json()["pending_updates"]


def _rows(db, user_id):
    return sorted(r for (r,) in db.query(UserUpdateAcknowledgement.release_id).filter(
        UserUpdateAcknowledgement.user_id == user_id))


# ─── The registry (pure) ────────────────────────────────────────────────────

def test_release_identifiers_are_stable_strings_not_dates_or_counters():
    assert releases.WHATS_NEW == "2026-09-skill-gap"
    assert releases.FIRST_ROADMAP_INTRO == "2026-09-skill-gap-intro"
    assert releases.KNOWN_RELEASES == {releases.WHATS_NEW, releases.FIRST_ROADMAP_INTRO}


def test_pending_is_one_announcement_at_a_time_and_in_order():
    assert releases.pending_updates([]) == [releases.WHATS_NEW]
    assert releases.pending_updates([releases.WHATS_NEW]) == [releases.FIRST_ROADMAP_INTRO]
    assert releases.pending_updates([releases.WHATS_NEW, releases.FIRST_ROADMAP_INTRO]) == []
    # The introduction is not due while What's New is: an existing account is asked about one thing.
    assert releases.pending_updates([releases.FIRST_ROADMAP_INTRO]) == [releases.WHATS_NEW]


def test_seeing_whats_new_covers_the_introduction():
    assert releases.with_covered(releases.WHATS_NEW) == [releases.WHATS_NEW, releases.FIRST_ROADMAP_INTRO]
    assert releases.with_covered(releases.FIRST_ROADMAP_INTRO) == [releases.FIRST_ROADMAP_INTRO]


# ─── Who is asked about what ────────────────────────────────────────────────

def test_a_new_account_is_not_shown_whats_new_but_is_due_the_introduction(learn_client, learn_db):
    user = register(learn_client)
    assert _rows(learn_db, user["id"]) == [releases.WHATS_NEW]          # written with the account
    assert _pending(learn_client, user) == [releases.FIRST_ROADMAP_INTRO]


def test_the_registration_response_already_carries_it(learn_client):
    body = learn_client.post("/api/v1/auth/register", json={
        "accept_terms": True, "accept_privacy": True,
        "email": f"reg-{uuid.uuid4().hex[:10]}@example.com", "full_name": "Reg Tester", "password": "correcthorsebatterystaple",
    }).json()
    assert body["user"]["pending_updates"] == [releases.FIRST_ROADMAP_INTRO]


def test_an_existing_account_is_asked_about_whats_new(learn_client, learn_db):
    user = _legacy_account(learn_client, learn_db)
    assert _pending(learn_client, user) == [releases.WHATS_NEW]


# ─── Acknowledging ──────────────────────────────────────────────────────────

def test_acknowledging_whats_new_clears_it_and_the_introduction_with_it(learn_client, learn_db):
    user = _legacy_account(learn_client, learn_db)
    resp = learn_client.post(ACK.format(releases.WHATS_NEW), headers=user["headers"])
    assert resp.status_code == 200, resp.text
    assert resp.json()["pending_updates"] == []                          # the response is the updated account
    assert _rows(learn_db, user["id"]) == sorted([releases.WHATS_NEW, releases.FIRST_ROADMAP_INTRO])
    assert _pending(learn_client, user) == []


def test_a_new_account_acknowledges_the_introduction(learn_client, learn_db):
    user = register(learn_client)
    resp = learn_client.post(ACK.format(releases.FIRST_ROADMAP_INTRO), headers=user["headers"])
    assert resp.status_code == 200
    assert resp.json()["pending_updates"] == []
    assert _rows(learn_db, user["id"]) == sorted([releases.WHATS_NEW, releases.FIRST_ROADMAP_INTRO])


def test_acknowledging_twice_is_harmless_and_creates_no_duplicate(learn_client, learn_db):
    user = _legacy_account(learn_client, learn_db)
    for _ in range(3):
        assert learn_client.post(ACK.format(releases.WHATS_NEW), headers=user["headers"]).status_code == 200
    assert _rows(learn_db, user["id"]) == sorted([releases.WHATS_NEW, releases.FIRST_ROADMAP_INTRO])


def test_the_unique_constraint_is_the_real_arbiter(learn_db):
    from sqlalchemy.exc import IntegrityError

    u = User(email=f"u-{uuid.uuid4().hex[:8]}@example.com", full_name="Unique Test", hashed_password="x")
    learn_db.add(u)
    learn_db.flush()
    learn_db.add(UserUpdateAcknowledgement(user_id=u.id, release_id=releases.WHATS_NEW))
    learn_db.flush()
    learn_db.add(UserUpdateAcknowledgement(user_id=u.id, release_id=releases.WHATS_NEW))
    with pytest.raises(IntegrityError):
        learn_db.flush()
    learn_db.rollback()


def test_two_racing_acknowledgements_resolve_to_one_row(learn_client, learn_db):
    """The SELECT is only a fast path. If a concurrent request wrote the row between it and the
    INSERT, the constraint refuses the second write and that is treated as success."""
    from app.services import update_service

    user = register(learn_client)
    learn_db.query(UserUpdateAcknowledgement).filter(UserUpdateAcknowledgement.user_id == user["id"]).delete()
    learn_db.add(UserUpdateAcknowledgement(user_id=user["id"], release_id=releases.WHATS_NEW))
    learn_db.flush()

    class BlindQuery:                      # a session whose SELECT has not seen the other request's row yet
        def __init__(self, real): self._real = real
        def query(self, *_a, **_k): return _Empty()
        def __getattr__(self, name): return getattr(self._real, name)

    class _Empty:
        def filter(self, *_a, **_k): return []

    update_service.acknowledge(BlindQuery(learn_db), user["id"], releases.WHATS_NEW)   # must not raise
    assert _rows(learn_db, user["id"]) == sorted([releases.WHATS_NEW, releases.FIRST_ROADMAP_INTRO])


def test_it_persists_across_sign_ins(learn_client, learn_db):
    """A different device is a fresh token against the same server-side record."""
    user = _legacy_account(learn_client, learn_db)
    learn_client.post(ACK.format(releases.WHATS_NEW), headers=user["headers"])
    login = learn_client.post("/api/v1/auth/login", json={"email": user["email"], "password": "correcthorsebatterystaple"})
    assert login.status_code == 200, login.text
    assert login.json()["user"]["pending_updates"] == []


# ─── What it refuses ────────────────────────────────────────────────────────

def test_it_requires_authentication(learn_client):
    assert learn_client.post(ACK.format(releases.WHATS_NEW)).status_code in (401, 403)


@pytest.mark.parametrize("release_id", ["2099-01-future", "2026-09-skill-gap-x", "whats-new", "0", "2026-09-SKILL-GAP"])
def test_an_unknown_announcement_is_refused_and_records_nothing(learn_client, learn_db, release_id):
    user = _legacy_account(learn_client, learn_db)
    resp = learn_client.post(ACK.format(release_id), headers=user["headers"])
    assert resp.status_code == 404
    assert _rows(learn_db, user["id"]) == []
    assert _pending(learn_client, user) == [releases.WHATS_NEW]


# ─── Isolation ──────────────────────────────────────────────────────────────

def test_one_account_acknowledging_does_not_touch_another(learn_client, learn_db):
    a = _legacy_account(learn_client, learn_db)
    b = _legacy_account(learn_client, learn_db)
    learn_client.post(ACK.format(releases.WHATS_NEW), headers=a["headers"])
    assert _pending(learn_client, a) == []
    assert _pending(learn_client, b) == [releases.WHATS_NEW]
    assert _rows(learn_db, b["id"]) == []


def test_there_is_no_way_to_acknowledge_for_someone_else(learn_client, learn_db):
    a = _legacy_account(learn_client, learn_db)
    b = _legacy_account(learn_client, learn_db)
    # The route takes no user id, and a body naming one is ignored: it is always the caller.
    learn_client.post(ACK.format(releases.WHATS_NEW), headers=a["headers"], json={"user_id": b["id"]})
    assert _rows(learn_db, b["id"]) == []


# ─── It changes nothing else ────────────────────────────────────────────────

def test_the_account_response_is_otherwise_unchanged(learn_client, learn_db):
    user = _legacy_account(learn_client, learn_db)
    before = learn_client.get(ME, headers=user["headers"]).json()
    after = learn_client.post(ACK.format(releases.WHATS_NEW), headers=user["headers"]).json()
    assert {k: v for k, v in after.items() if k != "pending_updates"} == {k: v for k, v in before.items() if k != "pending_updates"}
