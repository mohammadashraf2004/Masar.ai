"""
Covers the backend enrolment gate for unpublished career tracks.

The tracks page hides everything but AI Developer, but that is presentation:
POST /tracks/enroll takes a track id, so a client that ignores the UI could
enrol in a track with no content behind it. These tests pin the server-side
rule, including that a rejection writes nothing and that an enrolment made
before a track was closed stays reachable.
"""
import uuid

import pytest

from app.core.config import settings
from app.db.session import SessionLocal
from app.models.learning import CareerTrack
from app.models.progress import Enrollment
from app.services.content.track_availability import is_track_available

AVAILABLE_SLUG = "ai-developer"
COMING_SOON_SLUGS = ["data-analyst", "ml-engineer", "mlops-engineer", "ai-engineer"]

# Titles match seeds/tracks_all.py so the rejection message reads the way it
# would in production.
TRACK_TITLES = {
    "ai-developer": "AI Developer",
    "data-analyst": "Data Analyst",
    "ml-engineer": "ML Engineer",
    "mlops-engineer": "MLOps Engineer",
    "ai-engineer": "AI Engineer",
}


def _register(client) -> str:
    email = f"track-{uuid.uuid4().hex[:12]}@example.com"
    resp = client.post("/api/v1/auth/register", json={
        "email": email, "full_name": "Track Test", "password": "correcthorsebatterystaple",
    })
    assert resp.status_code == 201
    return resp.json()["access_token"]


def _ensure_track(slug: str) -> int:
    """Get-or-create the real track by slug, returning its id.

    Get-or-create rather than create: the seeds may or may not have run
    against the test database, and `slug` is unique.
    """
    setup = SessionLocal()
    try:
        track = setup.query(CareerTrack).filter(CareerTrack.slug == slug).first()
        if track is None:
            track = CareerTrack(
                slug=slug, title=TRACK_TITLES[slug],
                description="Seeded by tests.", icon="*",
                estimated_weeks=12, is_active=True,
            )
            setup.add(track)
            setup.commit()
            setup.refresh(track)
        return track.id
    finally:
        setup.close()


def _enrollment_count(user_id: int, track_id: int) -> int:
    session = SessionLocal()
    try:
        return session.query(Enrollment).filter(
            Enrollment.user_id == user_id,
            Enrollment.track_id == track_id,
        ).count()
    finally:
        session.close()


def _me(client, headers) -> int:
    resp = client.get("/api/v1/auth/me", headers=headers)
    assert resp.status_code == 200
    return resp.json()["id"]


# ─── The rule itself ──────────────────────────────────────────────────────

def test_only_ai_developer_is_available_by_default():
    assert is_track_available(AVAILABLE_SLUG)
    for slug in COMING_SOON_SLUGS:
        assert not is_track_available(slug), slug


def test_availability_is_configuration_not_hardcoded(monkeypatch):
    """The allowlist comes from settings, so opening a track is an env
    change rather than a code change."""
    monkeypatch.setattr(settings, "AVAILABLE_TRACK_SLUGS", "ai-developer, data-analyst")
    assert is_track_available("data-analyst")
    assert is_track_available("ai-developer")
    assert not is_track_available("ml-engineer")


def test_unknown_and_empty_slugs_are_not_available():
    assert not is_track_available("no-such-track")
    assert not is_track_available("")
    assert not is_track_available(None)


# ─── POST /tracks/enroll ──────────────────────────────────────────────────

def test_enroll_available_track_succeeds(client, db):
    headers = {"Authorization": f"Bearer {_register(client)}"}
    track_id = _ensure_track(AVAILABLE_SLUG)

    resp = client.post("/api/v1/tracks/enroll", json={"track_id": track_id}, headers=headers)
    assert resp.status_code == 201
    assert resp.json()["track_id"] == track_id
    assert _enrollment_count(_me(client, headers), track_id) == 1


@pytest.mark.parametrize("slug", COMING_SOON_SLUGS)
def test_enroll_coming_soon_track_is_rejected(client, db, slug):
    headers = {"Authorization": f"Bearer {_register(client)}"}
    track_id = _ensure_track(slug)

    resp = client.post("/api/v1/tracks/enroll", json={"track_id": track_id}, headers=headers)
    assert resp.status_code == 403
    assert "not open for enrolment" in resp.json()["detail"]


@pytest.mark.parametrize("slug", COMING_SOON_SLUGS)
def test_rejected_enrollment_creates_no_row(client, db, slug):
    headers = {"Authorization": f"Bearer {_register(client)}"}
    user_id = _me(client, headers)
    track_id = _ensure_track(slug)

    assert _enrollment_count(user_id, track_id) == 0
    resp = client.post("/api/v1/tracks/enroll", json={"track_id": track_id}, headers=headers)
    assert resp.status_code == 403
    # The gate runs before the Enrollment is constructed, so nothing is
    # written and nothing needs rolling back.
    assert _enrollment_count(user_id, track_id) == 0

    mine = client.get("/api/v1/tracks/my-enrollments", headers=headers)
    assert mine.status_code == 200
    assert all(e["track_id"] != track_id for e in mine.json())


def test_enrolling_by_id_ignores_any_client_supplied_slug(client, db):
    """The slug is read off the row the id resolves to. Extra fields in the
    payload are ignored, so they cannot talk the gate into opening."""
    headers = {"Authorization": f"Bearer {_register(client)}"}
    track_id = _ensure_track("data-analyst")

    resp = client.post(
        "/api/v1/tracks/enroll",
        json={"track_id": track_id, "slug": AVAILABLE_SLUG, "track_slug": AVAILABLE_SLUG},
        headers=headers,
    )
    assert resp.status_code == 403


# ─── Existing enrolments are untouched ────────────────────────────────────

def test_existing_enrollment_in_closed_track_stays_accessible(client, db):
    """Requirement: closing a track must not cut off someone already in it.

    The enrolment is created directly, which is the state a user would be
    left in if a track were closed after they had joined it.
    """
    headers = {"Authorization": f"Bearer {_register(client)}"}
    user_id = _me(client, headers)
    track_id = _ensure_track("data-analyst")

    setup = SessionLocal()
    try:
        setup.add(Enrollment(user_id=user_id, track_id=track_id, is_active=True))
        setup.commit()
    finally:
        setup.close()

    mine = client.get("/api/v1/tracks/my-enrollments", headers=headers)
    assert mine.status_code == 200
    assert any(e["track_id"] == track_id for e in mine.json())

    detail = client.get("/api/v1/tracks/data-analyst", headers=headers)
    assert detail.status_code == 200
    assert detail.json()["slug"] == "data-analyst"

    # And it is still there afterwards — the gate never deletes or
    # deactivates anything.
    assert _enrollment_count(user_id, track_id) == 1


def test_closed_tracks_are_still_listed_and_browsable(client, db):
    """Only enrolment is gated. The catalogue still shows them, which is
    what lets the frontend render them as coming soon."""
    for slug in COMING_SOON_SLUGS:
        _ensure_track(slug)

    listing = client.get("/api/v1/tracks/")
    assert listing.status_code == 200
    slugs = {t["slug"] for t in listing.json()}
    assert set(COMING_SOON_SLUGS) <= slugs


# ─── Unrelated enrolment behaviour is unchanged ───────────────────────────

def test_unknown_track_id_still_404s(client, db):
    headers = {"Authorization": f"Bearer {_register(client)}"}
    resp = client.post("/api/v1/tracks/enroll", json={"track_id": 99_999_999}, headers=headers)
    assert resp.status_code == 404


def test_duplicate_enrollment_still_400s(client, db):
    headers = {"Authorization": f"Bearer {_register(client)}"}
    track_id = _ensure_track(AVAILABLE_SLUG)

    assert client.post("/api/v1/tracks/enroll", json={"track_id": track_id},
                       headers=headers).status_code == 201
    second = client.post("/api/v1/tracks/enroll", json={"track_id": track_id}, headers=headers)
    assert second.status_code == 400
    assert "Already enrolled" in second.json()["detail"]
    assert _enrollment_count(_me(client, headers), track_id) == 1


def test_enrollment_requires_authentication(client, db):
    track_id = _ensure_track(AVAILABLE_SLUG)
    resp = client.post("/api/v1/tracks/enroll", json={"track_id": track_id})
    assert resp.status_code in (401, 403)
