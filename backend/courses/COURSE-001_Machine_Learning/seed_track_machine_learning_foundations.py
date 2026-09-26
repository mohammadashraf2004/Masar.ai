"""Idempotent, non-destructive adapter for Machine Learning Foundations.

Curriculum data lives alongside this adapter under backend/courses. Run from
backend after the career-track shell and schema already exist. Does not create
or overwrite a track.
"""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.db.session import SessionLocal
from app.models.learning import CareerTrack, TrackLevel, Topic, Lesson, Exercise, Quiz, Project
from lessons import load_levels

TRACK_SLUG = os.environ.get("ML_FOUNDATIONS_TRACK_SLUG", "machine-learning-foundations")
TOPIC_FIELDS = ("title", "slug", "description", "order", "difficulty",
                "estimated_hours", "skill_tags", "prerequisite_ids")


def seed(db):
    track = db.query(CareerTrack).filter(CareerTrack.slug == TRACK_SLUG).first()
    if track is None:
        raise RuntimeError(
            f"Track {TRACK_SLUG!r} not found. Create its shell first, or set "
            "ML_FOUNDATIONS_TRACK_SLUG to the exact existing slug. No data committed."
        )
    levels = load_levels()
    # Check for collisions before writing anything, preserving existing content.
    for definition in levels:
        level = db.query(TrackLevel).filter(
            TrackLevel.track_id == track.id, TrackLevel.order == definition["order"]
        ).first()
        if level is None:
            continue
        for t in definition["topics"]:
            occupying = db.query(Topic).filter(
                Topic.level_id == level.id, Topic.order == t["order"]
            ).first()
            if occupying is not None and occupying.slug != t["slug"]:
                raise RuntimeError(
                    f"Collision at {definition['title']} / position {t['order']}: "
                    f"existing slug {occupying.slug!r}. Resolve manually; no data committed."
                )
            # An existing slug in another level is also unsafe to duplicate.
            elsewhere = db.query(Topic).filter(Topic.slug == t["slug"]).first()
            if elsewhere is not None and elsewhere.level_id != level.id:
                raise RuntimeError(f"Topic slug already belongs to another level: {t['slug']}")
    for definition in levels:
        level = db.query(TrackLevel).filter(
            TrackLevel.track_id == track.id, TrackLevel.order == definition["order"]
        ).first()
        if level is None:
            level = TrackLevel(
                track_id=track.id, title=definition["title"],
                description=definition["description"], order=definition["order"]
            )
            db.add(level)
            db.flush()
            print(f"+ Level: {level.title}")
        else:
            print(f"= Existing level kept unchanged: {level.title}")
        for t in definition["topics"]:
            topic = db.query(Topic).filter(
                Topic.level_id == level.id, Topic.slug == t["slug"]
            ).first()
            if topic is None:
                topic = Topic(level_id=level.id, **{k:t[k] for k in TOPIC_FIELDS})
                db.add(topic)
                db.flush()
                print(f"  + Topic: {topic.slug}")
            else:
                print(f"  = Existing topic kept unchanged: {topic.slug}")
            if not db.query(Lesson).filter(Lesson.topic_id == topic.id).first():
                db.add(Lesson(topic_id=topic.id, order=1, **t["lesson"]))
            if db.query(Exercise).filter(Exercise.topic_id == topic.id).count() == 0:
                for ex in t.get("exercises", []):
                    db.add(Exercise(topic_id=topic.id, **ex))
            if not db.query(Quiz).filter(Quiz.topic_id == topic.id).first():
                db.add(Quiz(topic_id=topic.id, **t["quiz"]))
            project = t.get("project")
            if project and project.get("title"):
                if not db.query(Project).filter(Project.topic_id == topic.id).first():
                    db.add(Project(topic_id=topic.id, **project))
    db.commit()
    print("Done: idempotent insert of missing content only.")


if __name__ == "__main__":
    session = SessionLocal()
    try:
        seed(session)
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
