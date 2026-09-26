"""
COURSE-010 — AI Service Engineering with FastAPI

Masar seed adapter for the demonstrated application hierarchy:
    CareerTrack -> TrackLevel -> Topic -> Lesson / Exercise / Quiz / Project

IMPORTANT:
- Set MASAR_COURSE010_TRACK_SLUG explicitly.
- This adapter does not overwrite existing lesson/exercise/quiz/project rows.
- Repository-specific integration must be tested in the real Masar backend.
"""
from __future__ import annotations
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BACKEND = ROOT.parent.parent
sys.path.insert(0, str(BACKEND))

from course_data_loader import load_all_lessons

from app.db.session import SessionLocal, engine, Base
import app.models.user, app.models.progress, app.models.community  # noqa: F401
import app.models.wallet, app.models.auth_token, app.models.challenge, app.models.exam  # noqa: F401
import app.models.tool_course  # noqa: F401
from app.models.learning import (
    CareerTrack, TrackLevel, Topic, Lesson, Exercise, Quiz, Project, DifficultyLevel
)

Base.metadata.create_all(bind=engine)

TRACK_SLUG = os.getenv("MASAR_COURSE010_TRACK_SLUG")
if not TRACK_SLUG:
    raise RuntimeError(
        "Set MASAR_COURSE010_TRACK_SLUG to the target CareerTrack slug before seeding."
    )

DIFFICULTY = {
    "beginner": DifficultyLevel.beginner,
    "intermediate": DifficultyLevel.intermediate,
    "advanced": DifficultyLevel.advanced,
}

TOPIC_FIELDS = (
    "title", "slug", "description", "order", "difficulty",
    "estimated_hours", "skill_tags", "prerequisite_ids",
)

def _module_title(row):
    return row["lesson_meta"]["module_title"]

def seed(db):
    track = db.query(CareerTrack).filter(CareerTrack.slug == TRACK_SLUG).first()
    if not track:
        raise RuntimeError(
            f"CareerTrack '{TRACK_SLUG}' not found. Seed the track shell first."
        )

    rows = load_all_lessons()
    grouped = {}
    for row in rows:
        grouped.setdefault(row["module_id"], []).append(row)

    existing_orders = [
        x.order for x in db.query(TrackLevel).filter(TrackLevel.track_id == track.id).all()
        if x.order is not None
    ]
    next_order = (max(existing_orders) + 1) if existing_orders else 1

    level_by_module = {}
    for module_id in sorted(grouped):
        title = _module_title(grouped[module_id][0])
        level = db.query(TrackLevel).filter(
            TrackLevel.track_id == track.id,
            TrackLevel.title == title,
        ).first()
        if not level:
            level = TrackLevel(
                track_id=track.id,
                title=title,
                description=f"COURSE-010 module {module_id}",
                order=next_order,
            )
            next_order += 1
            db.add(level)
            db.flush()
            print(f"+ Level: {title}")
        else:
            print(f"- Level exists: {title}")
        level_by_module[module_id] = level

    for row in rows:
        t = dict(row["topic"])
        t["difficulty"] = DIFFICULTY.get(t["difficulty"], DifficultyLevel.advanced)
        level = level_by_module[row["module_id"]]

        topic = db.query(Topic).filter(
            Topic.level_id == level.id,
            Topic.slug == t["slug"],
        ).first()

        if not topic:
            topic = Topic(level_id=level.id, **{k: t[k] for k in TOPIC_FIELDS})
            db.add(topic)
            db.flush()
            print(f"  + Topic: {topic.title}")
        else:
            print(f"  - Topic exists: {topic.title}")

        if not db.query(Lesson).filter(Lesson.topic_id == topic.id).first():
            db.add(Lesson(topic_id=topic.id, order=1, **t["lesson"]))
            print("    + Lesson added")

        if db.query(Exercise).filter(Exercise.topic_id == topic.id).count() == 0:
            for ex in t.get("exercises", []):
                ex = dict(ex)
                ex["difficulty"] = DIFFICULTY.get(ex["difficulty"], DifficultyLevel.advanced)
                db.add(Exercise(topic_id=topic.id, **ex))
            print(f"    + {len(t.get('exercises', []))} exercise(s) added")

        if not db.query(Quiz).filter(Quiz.topic_id == topic.id).first():
            db.add(Quiz(topic_id=topic.id, **t["quiz"]))
            print("    + Quiz added")

        project = t.get("project")
        if project and project.get("title"):
            if not db.query(Project).filter(Project.topic_id == topic.id).first():
                project = dict(project)
                project["difficulty"] = DIFFICULTY.get(
                    project.get("difficulty", "advanced"), DifficultyLevel.advanced
                )
                db.add(Project(topic_id=topic.id, **project))
                print("    + Project added")

    db.commit()
    print(f"Done. COURSE-010 seeded into track '{TRACK_SLUG}'.")

if __name__ == "__main__":
    db = SessionLocal()
    try:
        seed(db)
    finally:
        db.close()
