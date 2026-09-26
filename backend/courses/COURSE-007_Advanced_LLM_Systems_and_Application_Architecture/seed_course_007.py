"""Master seed adapter for COURSE-007.

Supplied Masar schema: CareerTrack -> TrackLevel -> Topic -> Lesson/Exercise/Quiz/Project.
COURSE-007 is reusable across tracks, while that schema does not expose a reusable Course model.
Therefore this adapter does NOT silently duplicate COURSE-007 into every career track.

Set MASAR_COURSE007_TRACK_SLUG to the one target track you intentionally want to seed,
then run from backend/. Module folders map to TrackLevels and lesson files map to Topics.

Example:
    MASAR_COURSE007_TRACK_SLUG=ai-developer python COURSE-007_Advanced_LLM_Systems_and_Application_Architecture/seed_course_007.py

Review the mapping against your current repository before production use.
"""
import importlib.util, os, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BACKEND = ROOT.parent.parent
sys.path.insert(0, str(BACKEND))

from app.db.session import SessionLocal, engine, Base
import app.models.user, app.models.progress, app.models.community  # noqa: F401
import app.models.wallet, app.models.auth_token, app.models.challenge, app.models.exam  # noqa: F401
import app.models.tool_course  # noqa: F401
from app.models.learning import CareerTrack, TrackLevel, Topic, Lesson, Exercise, Quiz, Project

Base.metadata.create_all(bind=engine)
TRACK_SLUG = os.environ.get("MASAR_COURSE007_TRACK_SLUG")
TOPIC_FIELDS = ("title", "slug", "description", "order", "difficulty", "estimated_hours", "skill_tags", "prerequisite_ids")

def load_topic(path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.TOPIC

def seed(db):
    if not TRACK_SLUG:
        raise RuntimeError("Set MASAR_COURSE007_TRACK_SLUG explicitly; this reusable course is not auto-duplicated across tracks.")
    track = db.query(CareerTrack).filter(CareerTrack.slug == TRACK_SLUG).first()
    if not track:
        raise RuntimeError(f"CareerTrack {TRACK_SLUG!r} not found")

    module_dirs = sorted((ROOT / "modules").glob("M007_*"))
    for module_order, module_dir in enumerate(module_dirs, start=1):
        namespace = {}
        exec((module_dir / "module.py").read_text(encoding="utf-8"), namespace)
        m = namespace["MODULE"]
        level = db.query(TrackLevel).filter(TrackLevel.track_id == track.id, TrackLevel.title == m["title"]).first()
        if not level:
            level = TrackLevel(track_id=track.id, title=m["title"], description=f"{m['id']} — COURSE-007", order=module_order)
            db.add(level); db.flush()
        for path in sorted(module_dir.glob("L007_*.py")):
            t = load_topic(path)
            topic = db.query(Topic).filter(Topic.level_id == level.id, Topic.slug == t["slug"]).first()
            if not topic:
                topic = Topic(level_id=level.id, **{k:t[k] for k in TOPIC_FIELDS})
                db.add(topic); db.flush()
            if not db.query(Lesson).filter(Lesson.topic_id == topic.id).first():
                db.add(Lesson(topic_id=topic.id, order=1, **t["lesson"]))
            if db.query(Exercise).filter(Exercise.topic_id == topic.id).count() == 0:
                for ex in t.get("exercises", []): db.add(Exercise(topic_id=topic.id, **ex))
            if not db.query(Quiz).filter(Quiz.topic_id == topic.id).first():
                db.add(Quiz(topic_id=topic.id, **t["quiz"]))
            p = t.get("project")
            if p and p.get("title") and not db.query(Project).filter(Project.topic_id == topic.id).first():
                db.add(Project(topic_id=topic.id, **p))
    db.commit()

if __name__ == "__main__":
    db = SessionLocal()
    try: seed(db)
    finally: db.close()
