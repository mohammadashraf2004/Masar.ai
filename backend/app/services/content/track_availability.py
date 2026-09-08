"""Which career tracks are open for enrolment.

Only tracks whose content is actually published can be enrolled in. The rest
of the catalogue is seeded as shells — levels with no topics under them — so
an enrolment in one produces a dashboard card that opens onto an empty track.

This module is the authoritative rule. `POST /tracks/enroll` takes a track
*id*, so the slug is always read back from the CareerTrack row that id
resolves to; a slug supplied by a client is never trusted. The frontend keeps
its own list (frontend/src/lib/tracks.ts) to decide what the UI offers, which
is presentation only and must not be relied on as a control.

The set itself is configuration (settings.AVAILABLE_TRACK_SLUGS), so opening
a track is a content seed plus an env change rather than a code change.
"""
from typing import Optional

from fastapi import HTTPException, status

from app.core import security_log
from app.core.config import settings
from app.models.learning import CareerTrack


def is_track_available(slug: Optional[str]) -> bool:
    """Whether the track with this slug may currently be enrolled in."""
    if not slug:
        return False
    return slug.strip().casefold() in settings.available_track_slugs


def require_track_available(track: CareerTrack, *, user_id: Optional[int] = None) -> None:
    """Raise 403 unless `track` is open for enrolment.

    403 rather than 404: the track is real and the catalogue lists it, the
    caller just may not join it yet — the same shape as
    exam_controller._require_paid_exam, which likewise denies an action on a
    resource the caller can see.

    Read-only. Existing enrolments are never touched, and reaching a track
    already enrolled in stays a separate path (GET /tracks/{slug} and
    /tracks/my-enrollments), which this does not gate.
    """
    if is_track_available(track.slug):
        return

    security_log.authz_denied(
        user_id=user_id,
        path=f"/tracks/{track.slug}",
        reason="track_not_available",
    )
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=f"The {track.title} track is not open for enrolment yet.",
    )
