"""Repository-neutral seed adapter for COURSE-015.

The production Masar schema is CareerTrack -> TrackLevel -> Topic -> Lesson / Exercise / Quiz / Project.
This package does not guess ORM IDs. Set MASAR_COURSE015_TRACK_SLUG and replace `persist_topic_bundle`
with the production repository/ORM adapter. The function is intentionally idempotency-friendly by stable IDs/slugs.
"""
from __future__ import annotations
import os
from course_data import load_course

def persist_topic_bundle(track_slug: str, bundle: dict) -> None:
    raise NotImplementedError("Map this repository-neutral bundle to the production Masar ORM/repository contract.")

def main() -> None:
    track_slug = os.getenv("MASAR_COURSE015_TRACK_SLUG")
    if not track_slug:
        raise SystemExit("Set MASAR_COURSE015_TRACK_SLUG explicitly; COURSE-015 is reusable across multiple tracks.")
    data = load_course()
    for lesson in data["lessons"]:
        persist_topic_bundle(track_slug, lesson)

if __name__ == "__main__":
    main()
