"""Per-account walkthrough (tour) progress — see docs/backend-requests.md §6.

What is pinned here:

  * an unknown tour_id is refused on every route (GET list is unaffected — it
    never takes one), so a typo or a probe cannot create rows forever;
  * PUT upserts and is idempotent; a version bump is stored as given, the
    server never compares it itself;
  * last-write-wins by `at`, not by request arrival order: an incoming `at`
    older than the stored one is a no-op, and the stored row comes back;
  * GET /me/tours/:id 404s until the account has a record, GET /me/tours
    always succeeds and lists everything the account has;
  * every route requires auth, and only ever acts on the caller's own rows.
"""
from datetime import datetime, timedelta, timezone

import pytest

from app.models.user_tour import UserTour

from tests.learning_fixtures import *  # noqa: F401,F403
from tests.learning_fixtures import register

TOURS = "/api/v1/auth/me/tours"
TOUR = "/api/v1/auth/me/tours/{}"


def _put(client, user, tour_id, status="completed", version=1, at=None):
    body = {"status": status, "version": version}
    if at is not None:
        body["at"] = at
    return client.put(TOUR.format(tour_id), headers=user["headers"], json=body)


# ─── Upsert ──────────────────────────────────────────────────────────────────

def test_a_first_put_creates_the_record(learn_client, learn_db):
    user = register(learn_client)
    resp = _put(learn_client, user, "onboarding", status="completed", version=1)
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["tour_id"] == "onboarding"
    assert body["status"] == "completed"
    assert body["version"] == 1
    assert body["at"]

    row = learn_db.query(UserTour).filter(UserTour.user_id == user["id"]).one()
    assert row.tour_id == "onboarding" and row.status.value == "completed" and row.version == 1


def test_a_later_put_updates_the_same_row_not_a_new_one(learn_client, learn_db):
    user = register(learn_client)
    _put(learn_client, user, "onboarding", status="completed", version=1)
    resp = _put(learn_client, user, "onboarding", status="skipped", version=1)
    assert resp.status_code == 200
    assert resp.json()["status"] == "skipped"
    assert learn_db.query(UserTour).filter(UserTour.user_id == user["id"]).count() == 1


def test_repeating_the_same_put_is_idempotent(learn_client, learn_db):
    user = register(learn_client)
    for _ in range(3):
        assert _put(learn_client, user, "onboarding").status_code == 200
    assert learn_db.query(UserTour).filter(UserTour.user_id == user["id"]).count() == 1


def test_a_version_bump_is_stored_as_given(learn_client):
    user = register(learn_client)
    _put(learn_client, user, "onboarding", version=1)
    resp = _put(learn_client, user, "onboarding", version=2)
    assert resp.json()["version"] == 2


def test_in_progress_is_a_valid_status(learn_client):
    user = register(learn_client)
    resp = _put(learn_client, user, "language", status="in_progress", version=1)
    assert resp.status_code == 200
    assert resp.json()["status"] == "in_progress"


def test_an_invalid_status_is_rejected(learn_client, learn_db):
    user = register(learn_client)
    resp = _put(learn_client, user, "onboarding", status="done", version=1)
    assert resp.status_code == 422
    assert learn_db.query(UserTour).filter(UserTour.user_id == user["id"]).count() == 0


# ─── Last-write-wins by `at` ─────────────────────────────────────────────────

def test_a_stale_write_is_ignored_and_the_stored_row_comes_back(learn_client, learn_db):
    user = register(learn_client)
    now = datetime.now(timezone.utc)
    _put(learn_client, user, "onboarding", status="completed", version=1, at=now.isoformat())

    stale = (now - timedelta(minutes=5)).isoformat()
    resp = _put(learn_client, user, "onboarding", status="skipped", version=1, at=stale)
    assert resp.status_code == 200
    assert resp.json()["status"] == "completed"          # unchanged: the stale write lost the race

    row = learn_db.query(UserTour).filter(UserTour.user_id == user["id"]).one()
    assert row.status.value == "completed"


def test_a_newer_at_overwrites_an_older_one(learn_client):
    user = register(learn_client)
    now = datetime.now(timezone.utc)
    _put(learn_client, user, "onboarding", status="completed", version=1, at=now.isoformat())

    later = (now + timedelta(minutes=5)).isoformat()
    resp = _put(learn_client, user, "onboarding", status="skipped", version=1, at=later)
    assert resp.status_code == 200
    assert resp.json()["status"] == "skipped"


def test_an_at_without_a_timezone_is_read_as_utc_not_a_500(learn_client):
    user = register(learn_client)
    _put(learn_client, user, "onboarding", status="completed", version=1)
    naive = (datetime.now(timezone.utc) - timedelta(minutes=5)).replace(tzinfo=None).isoformat()
    resp = _put(learn_client, user, "onboarding", status="skipped", version=1, at=naive)
    assert resp.status_code == 200
    assert resp.json()["status"] == "completed"          # older than the stored row: ignored


def test_a_far_future_at_cannot_freeze_the_record(learn_client):
    user = register(learn_client)
    future = (datetime.now(timezone.utc) + timedelta(days=3650)).isoformat()
    _put(learn_client, user, "onboarding", status="completed", version=1, at=future)

    resp = _put(learn_client, user, "onboarding", status="skipped", version=1)
    assert resp.status_code == 200
    assert resp.json()["status"] == "skipped"


def test_a_missing_at_defaults_to_the_servers_own_time(learn_client):
    user = register(learn_client)
    past = (datetime.now(timezone.utc) - timedelta(days=1)).isoformat()
    _put(learn_client, user, "onboarding", status="completed", version=1, at=past)

    resp = _put(learn_client, user, "onboarding", status="skipped", version=1)   # no `at`: defaults to now
    assert resp.status_code == 200
    assert resp.json()["status"] == "skipped"


# ─── Reading ──────────────────────────────────────────────────────────────────

def test_get_one_404s_until_the_account_has_a_record(learn_client):
    user = register(learn_client)
    assert learn_client.get(TOUR.format("onboarding"), headers=user["headers"]).status_code == 404
    _put(learn_client, user, "onboarding")
    resp = learn_client.get(TOUR.format("onboarding"), headers=user["headers"])
    assert resp.status_code == 200
    assert resp.json()["tour_id"] == "onboarding"


def test_get_all_lists_every_tour_the_account_has_in_one_call(learn_client):
    user = register(learn_client)
    assert learn_client.get(TOURS, headers=user["headers"]).json() == []
    _put(learn_client, user, "onboarding")
    _put(learn_client, user, "language")
    body = learn_client.get(TOURS, headers=user["headers"]).json()
    assert sorted(r["tour_id"] for r in body) == ["language", "onboarding"]


# ─── What it refuses ──────────────────────────────────────────────────────────

def test_it_requires_authentication(learn_client):
    assert learn_client.get(TOURS).status_code in (401, 403)
    assert learn_client.get(TOUR.format("onboarding")).status_code in (401, 403)
    assert learn_client.put(TOUR.format("onboarding"), json={"status": "completed", "version": 1}).status_code in (401, 403)


@pytest.mark.parametrize("tour_id", ["not-a-tour", "Onboarding", "onboarding ", "0"])
def test_an_unknown_tour_id_is_refused_on_every_route(learn_client, learn_db, tour_id):
    user = register(learn_client)
    assert learn_client.get(TOUR.format(tour_id), headers=user["headers"]).status_code == 404
    resp = _put(learn_client, user, tour_id)
    assert resp.status_code == 404
    assert learn_db.query(UserTour).filter(UserTour.user_id == user["id"]).count() == 0


# ─── Isolation ────────────────────────────────────────────────────────────────

def test_one_account_never_sees_or_touches_another_accounts_tours(learn_client, learn_db):
    a = register(learn_client)
    b = register(learn_client)
    _put(learn_client, a, "onboarding", status="completed")

    assert learn_client.get(TOUR.format("onboarding"), headers=b["headers"]).status_code == 404
    assert learn_client.get(TOURS, headers=b["headers"]).json() == []
    assert learn_db.query(UserTour).filter(UserTour.user_id == b["id"]).count() == 0


def test_there_is_no_way_to_write_for_someone_else(learn_client, learn_db):
    a = register(learn_client)
    b = register(learn_client)
    # The route takes no user id, and a body naming one is ignored: it is always the caller.
    learn_client.put(TOUR.format("onboarding"), headers=a["headers"], json={"status": "completed", "version": 1, "user_id": b["id"]})
    assert learn_db.query(UserTour).filter(UserTour.user_id == b["id"]).count() == 0


def test_a_future_at_stored_before_clamping_cannot_freeze_the_record(learn_client, learn_db):
    """A row written by an older build (no clamp) may already hold a far-future `at`; a real
    write with a current timestamp must still win."""
    from app.models.user_tour import TourRecordStatus

    user = register(learn_client)
    learn_db.add(UserTour(user_id=user["id"], tour_id="language", status=TourRecordStatus.completed, version=1,
                          at=datetime.now(timezone.utc) + timedelta(days=3650)))
    learn_db.commit()
    resp = _put(learn_client, user, "language", status="skipped", version=2,
                at=datetime.now(timezone.utc).isoformat())
    assert resp.status_code == 200
    assert resp.json()["status"] == "skipped" and resp.json()["version"] == 2


def test_an_at_with_an_offset_is_compared_as_the_same_instant(learn_client):
    user = register(learn_client)
    now = datetime.now(timezone.utc)
    earlier_in_cairo = (now - timedelta(minutes=5)).astimezone(timezone(timedelta(hours=3))).isoformat()
    _put(learn_client, user, "onboarding", status="in_progress", version=1, at=now.isoformat())
    stale = _put(learn_client, user, "onboarding", status="completed", version=1, at=earlier_in_cairo)
    assert stale.status_code == 200 and stale.json()["status"] == "in_progress"
