"""Repository-neutral COURSE-012 seed adapter.

This package intentionally does not import Masar production ORM models because
the exact production repository/model contract was not supplied in this chat.
Map TOPIC/LESSON_META to your actual CareerTrack -> TrackLevel -> Topic ->
Lesson / Exercise / Quiz / Project models before enabling writes.
"""
from __future__ import annotations
import os
from course_data import load_course

COURSE_ID = "COURSE-012"

def build_seed_payload() -> dict:
    return load_course()

def seed_course(repository, *, track_slug: str, dry_run: bool = True):
    """Integration hook.

    `repository` is expected to be an application-specific adapter that exposes
    an idempotent upsert/import API. No database mutation is attempted by this
    repository-neutral package.
    """
    payload = build_seed_payload()
    if dry_run:
        return {
            "course_id": COURSE_ID,
            "track_slug": track_slug,
            "lesson_count": len(payload["lessons"]),
            "status": "dry_run",
        }
    raise NotImplementedError(
        "Map this repository-neutral payload to the production Masar ORM/repository "
        "before enabling writes."
    )

if __name__ == "__main__":
    track_slug = os.getenv("MASAR_COURSE012_TRACK_SLUG")
    if not track_slug:
        raise SystemExit(
            "Set MASAR_COURSE012_TRACK_SLUG explicitly. COURSE-012 is reusable across "
            "multiple tracks and this adapter will not silently choose a destination."
        )
    print(seed_course(None, track_slug=track_slug, dry_run=True))
