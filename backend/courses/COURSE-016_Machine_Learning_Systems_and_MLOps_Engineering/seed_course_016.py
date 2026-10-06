"""Repository-neutral seed adapter for COURSE-016.

Core lessons are loaded by default. Set MASAR_COURSE016_INCLUDE_OPTIONAL_K8S=true
to include the optional Kubernetes module M016-11.

Map persist_topic_bundle to the production Masar ORM/repository contract.
"""
from __future__ import annotations
import os
from course_data import load_course

def persist_topic_bundle(track_slug: str, bundle: dict) -> None:
    raise NotImplementedError("Map this repository-neutral bundle to the production Masar ORM/repository contract.")

def main() -> None:
    track_slug = os.getenv("MASAR_COURSE016_TRACK_SLUG")
    if not track_slug:
        raise SystemExit("Set MASAR_COURSE016_TRACK_SLUG explicitly; COURSE-016 is reusable across multiple tracks.")
    include_optional = os.getenv("MASAR_COURSE016_INCLUDE_OPTIONAL_K8S", "false").strip().lower() in {"1","true","yes","on"}
    data = load_course(include_optional=include_optional)
    for lesson in data["lessons"]:
        persist_topic_bundle(track_slug, lesson)

if __name__ == "__main__":
    main()
