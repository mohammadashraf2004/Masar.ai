"""
backend/seeds/seed_tool_langchain.py

Adds topic content (lessons/exercises/quiz/project) to the LangChain
tool course, which already exists as a shell (seeded by
seeds/seed_tool_courses.py). Idempotent — safe to re-run.

Run from backend/:
    docker compose exec api python seeds/seed_tool_langchain.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.db.session import SessionLocal, engine, Base
import app.models.user, app.models.learning, app.models.progress    # noqa: F401
import app.models.community, app.models.wallet, app.models.auth_token  # noqa: F401
import app.models.challenge, app.models.exam                         # noqa: F401
from app.models.learning import Lesson, Exercise, Quiz, Project, DifficultyLevel
from app.models.tool_course import ToolCourse, ToolTopic

Base.metadata.create_all(bind=engine)

TOOL_SLUG = "langchain"  # must already exist — created by seed_tool_courses.py

# ---------------------------------------------------------------------------
# Topics (flat — no levels). Add one dict per topic, in the order they
# should appear.
# ---------------------------------------------------------------------------
TOPICS = [
    {
        # ToolTopic fields
        "title":            "LangChain Core Concepts",
        "slug":              "langchain-core-concepts",
        "description":       "Chains, prompts, models, output parsers.",
        "order":             1,
        "difficulty":        DifficultyLevel.beginner,
        "estimated_hours":   3.0,
        "skill_tags":        ["langchain", "llm", "python"],
        "prerequisite_ids":  [],
        # Content
        "lesson": {
            "title":               "LangChain Core Concepts",
            "content":              "...",   # full markdown string
            "order":                1,
            "estimated_minutes":    50,
            "has_code_examples":    True,
        },
        "exercises": [
            {
                "title":         "...",
                "description":   "...",
                "difficulty":    DifficultyLevel.beginner,
                "starter_code":  "...",
                "solution_code": "...",
                "skill_tested":  ["langchain", "chains"],
            },
        ],
        "quiz": {
            "title":         "LangChain Core Concepts Quiz",
            "questions":     [],   # [{"question": "...", "options": [...], "correct": 0, "explanation": "..."}]
            "passing_score": 70,
        },
        "project": {
            "title":            "...",
            "description":      "...",
            "difficulty":       DifficultyLevel.intermediate,
            "tech_stack":       ["LangChain", "Python", "OpenAI"],
            "objectives":       [],
            "rubric":           {},
            "starter_repo_url": None,
            "estimated_hours":  6.0,
        },
    },
    # ... more topics
]

# ---------------------------------------------------------------------------
# Seed logic — do not modify below this line
# ---------------------------------------------------------------------------
TOPIC_FIELDS = ("title", "slug", "description", "order", "difficulty",
                 "estimated_hours", "skill_tags", "prerequisite_ids")


def seed(db):
    course = db.query(ToolCourse).filter(ToolCourse.slug == TOOL_SLUG).first()
    if not course:
        print(f"✗ ToolCourse '{TOOL_SLUG}' not found — run seed_tool_courses.py first")
        return

    for t in TOPICS:
        topic = db.query(ToolTopic).filter(
            ToolTopic.tool_course_id == course.id,
            ToolTopic.order == t["order"],
        ).first()
        if not topic:
            topic = ToolTopic(tool_course_id=course.id, **{k: t[k] for k in TOPIC_FIELDS})
            db.add(topic)
            db.flush()
            print(f"  + ToolTopic: {topic.title}")
        else:
            print(f"  - ToolTopic exists: {topic.title}, skipping")

        if not db.query(Lesson).filter(Lesson.tool_topic_id == topic.id).first():
            db.add(Lesson(tool_topic_id=topic.id, **t["lesson"]))
            print("    + Lesson added")
        else:
            print("    - Lesson exists, skipping")

        if db.query(Exercise).filter(Exercise.tool_topic_id == topic.id).count() == 0:
            for ex in t["exercises"]:
                db.add(Exercise(tool_topic_id=topic.id, **ex))
            print(f"    + {len(t['exercises'])} exercise(s) added")
        else:
            print("    - Exercises exist, skipping")

        if not db.query(Quiz).filter(Quiz.tool_topic_id == topic.id).first():
            db.add(Quiz(tool_topic_id=topic.id, **t["quiz"]))
            print("    + Quiz added")
        else:
            print("    - Quiz exists, skipping")

        if not db.query(Project).filter(Project.tool_topic_id == topic.id).first():
            db.add(Project(tool_topic_id=topic.id, **t["project"]))
            print("    + Project added")
        else:
            print("    - Project exists, skipping")

    db.commit()
    print("Done.")


if __name__ == "__main__":
    db = SessionLocal()
    try:
        seed(db)
    finally:
        db.close()
