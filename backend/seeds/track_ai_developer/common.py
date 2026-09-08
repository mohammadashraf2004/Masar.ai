"""
backend/seeds/track_ai_developer/common.py

Shared helpers for the AI Developer track seed files. The track's content is
split one file per level (level_01_foundations.py ... level_10_ai_evaluation.py,
in this same directory) to keep individual files manageable -- this module
holds everything they share:

    - DB session / model imports
    - TRACK_SLUG
    - stub_topic() / build_topics() -- generate TODO-shaped topics from just
      a title, for levels/topics you haven't written real content for yet
    - EXAMPLE_FULL_TOPIC -- reference shape for a fully-written topic dict
    - seed(db, levels) -- the actual DB upsert logic, now taking the
      combined LEVELS list as a parameter instead of a module global

Each level_*.py file imports what it needs like this:

    import sys, os
    sys.path.insert(0, os.path.dirname(__file__))
    from common import DifficultyLevel, build_topics, stub_topic

The top-level orchestrator (seeds/seed_track_ai_developer.py) imports the
LEVEL dict from every level_*.py file, combines them into a single list, and
calls seed(db, LEVELS).

Idempotent -- safe to re-run as you fill in more.
"""
import re
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))  # backend/

from app.db.session import SessionLocal, engine, Base
import app.models.user, app.models.progress, app.models.community          # noqa: F401
import app.models.wallet, app.models.auth_token, app.models.challenge, app.models.exam  # noqa: F401
import app.models.tool_course                                              # noqa: F401
from app.models.learning import CareerTrack, TrackLevel, Topic, Lesson, Exercise, Quiz, Project, DifficultyLevel

Base.metadata.create_all(bind=engine)

TRACK_SLUG = "ai-developer"  # must already exist -- created by seeds/tracks_all.py


# ---------------------------------------------------------------------------
# Stub generation helpers
# ---------------------------------------------------------------------------
def _slugify(text: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return s

def stub_topic(level_num, order, title, *, slug=None,
                difficulty=DifficultyLevel.beginner, estimated_hours=1.0,
                skill_tags=None, prerequisite_ids=None):
    """Generate a TODO-shaped topic dict from just a title.

    Slug is auto-derived as ai-developer-l{level_num}-{slugified title} so
    topics with the same title in different levels (e.g. "Function Calling"
    in Level 2 and Level 7) never collide.
    """
    skill_tags = skill_tags if skill_tags is not None else ["ai-developer"]
    prerequisite_ids = prerequisite_ids if prerequisite_ids is not None else []
    slug = slug or f"ai-developer-l{level_num}-{_slugify(title)}"

    return {
        "title": title,
        "slug": slug,
        "description": "TODO",
        "order": order,
        "difficulty": difficulty,
        "estimated_hours": estimated_hours,
        "skill_tags": skill_tags,
        "prerequisite_ids": prerequisite_ids,
        "lesson": {
            "title": title,
            "content": f"# {title}\n\nTODO: write this lesson.\n",
            "estimated_minutes": 20,
            "has_code_examples": False,
        },
        "exercises": [
            {
                "title": "TODO exercise title",
                "description": "TODO -- theory question: leave starter_code out entirely (or None) for a theory/discussion exercise graded conversationally by AnswerChat. Include starter_code for a DataCamp-style code exercise.",
                "difficulty": difficulty,
                "skill_tested": skill_tags,
            },
        ],
        "quiz": {
            "title": f"{title} — Knowledge Check",
            "questions": [
                {
                    "question": "TODO mcq question",
                    "options": ["TODO A", "TODO B", "TODO C", "TODO D"],
                    "correct": 0,
                    "explanation": "TODO -- why this answer is correct, referencing the lesson.",
                },
            ],
            "passing_score": 70,
        },
        # Omit / leave title=None for topics with no capstone project.
        # The seed logic only inserts a Project row when title is filled in.
        "project": {
            "title": None,
            "description": None,
            "difficulty": DifficultyLevel.intermediate,
            "tech_stack": [],
            "objectives": [],
            "rubric": {},
            "starter_repo_url": None,
            "estimated_hours": None,
        },
    }

def build_topics(level_num, titles, start_order=1):
    """Turn a plain list of topic titles into stub topic dicts, in order.

    start_order lets you generate stubs for the *tail* of a level's topic
    list while an earlier topic (e.g. order=1) is hand-written separately --
    see LEVELS[0]["topics"] for the pattern.
    """
    return [stub_topic(level_num, start_order + i, title) for i, title in enumerate(titles)]

# Reference: shape of a fully-written topic (once you send real content for
# a topic, replace its build_topics() list entry with a dict like this one --
# copy this shape, don't need to use stub_topic for it).
EXAMPLE_FULL_TOPIC = {
    "title":            "Example Topic Title",
    "slug":              "ai-developer-l1-example-topic-title",
    "description":       "One-line description of the topic.",
    "order":             1,
    "difficulty":        DifficultyLevel.beginner,
    "estimated_hours":   1.0,
    "skill_tags":        ["ai-developer", "llm"],
    "prerequisite_ids":  [],
    "lesson": {
        "title": "Example Topic Title",
        "content": "# Example Topic Title\n\n...full markdown lesson...\n",
        "estimated_minutes": 20,
        "has_code_examples": False,
    },
    "exercises": [
        {
            "title": "Exercise title",
            "description": "Exercise prompt.",
            # "starter_code": "def solve():\n    pass\n",   # omit for theory-only
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": ["ai-developer"],
        },
    ],
    "quiz": {
        "title": "Example Topic Title — Knowledge Check",
        "questions": [
            {
                "question": "Real MCQ question?",
                "options": ["A", "B", "C", "D"],
                "correct": 0,
                "explanation": "Why A is correct.",
            },
        ],
        "passing_score": 70,
    },
    "project": {
        "title": None,
        "description": None,
        "difficulty": DifficultyLevel.intermediate,
        "tech_stack": [],
        "objectives": [],
        "rubric": {},
        "starter_repo_url": None,
        "estimated_hours": None,
    },
}


# ---------------------------------------------------------------------------
# Seed logic -- do not modify below this line
# ---------------------------------------------------------------------------
TOPIC_FIELDS = ("title", "slug", "description", "order", "difficulty",
                 "estimated_hours", "skill_tags", "prerequisite_ids")

# Exact signatures stub_topic() writes -- used below to detect a row that's
# still a placeholder (safe to upgrade in place) vs. real content (never
# touched once written, same convention as every other seed file this
# project uses).
_STUB_LESSON_MARKER = "TODO: write this lesson."
_STUB_EXERCISE_TITLE = "TODO exercise title"
_STUB_QUIZ_QUESTION = "TODO mcq question"


def seed(db, levels):
    track = db.query(CareerTrack).filter(CareerTrack.slug == TRACK_SLUG).first()
    if not track:
        print(f"✗ CareerTrack '{TRACK_SLUG}' not found — run seeds/tracks_all.py first")
        return

    for lvl in levels:
        level = db.query(TrackLevel).filter(
            TrackLevel.track_id == track.id,
            TrackLevel.order == lvl["order"],
        ).first()
        if not level:
            level = TrackLevel(track_id=track.id, title=lvl["title"],
                                description=lvl.get("description", ""), order=lvl["order"])
            db.add(level)
            db.flush()
            print(f"+ Level: {level.title}")
        else:
            # tracks_all.py already created this level with a placeholder
            # title/description -- keep it in sync with LEVELS above.
            level.title = lvl["title"]
            level.description = lvl.get("description", "")
            print(f"- Level exists: {level.title} (synced title/description)")

        for t in lvl["topics"]:
            topic = db.query(Topic).filter(
                Topic.level_id == level.id,
                Topic.order == t["order"],
            ).first()
            if not topic:
                topic = Topic(level_id=level.id, **{k: t[k] for k in TOPIC_FIELDS})
                db.add(topic)
                db.flush()
                print(f"  + Topic: {topic.title}")
            else:
                # Always sync metadata -- cheap, and it's the only way a
                # stub ("description": "TODO") ever gets upgraded to real
                # text once the lesson/exercises/quiz already exist under it.
                for k in TOPIC_FIELDS:
                    setattr(topic, k, t[k])
                print(f"  - Topic exists: {topic.title} (synced metadata)")

            existing_lesson = db.query(Lesson).filter(Lesson.topic_id == topic.id).first()
            if not existing_lesson:
                db.add(Lesson(topic_id=topic.id, order=1, **t["lesson"]))
                print("    + Lesson added")
            elif _STUB_LESSON_MARKER in (existing_lesson.content or "") \
                    and _STUB_LESSON_MARKER not in t["lesson"]["content"]:
                existing_lesson.title = t["lesson"]["title"]
                existing_lesson.content = t["lesson"]["content"]
                existing_lesson.estimated_minutes = t["lesson"].get("estimated_minutes", existing_lesson.estimated_minutes)
                existing_lesson.has_code_examples = t["lesson"].get("has_code_examples", existing_lesson.has_code_examples)
                print("    ~ Lesson upgraded from stub to real content")
            else:
                print("    - Lesson exists, skipping")

            existing_exercises = db.query(Exercise).filter(Exercise.topic_id == topic.id).all()
            new_exercises = t.get("exercises", [])
            is_stub_exercises = (len(existing_exercises) == 1
                                  and existing_exercises[0].title == _STUB_EXERCISE_TITLE)
            new_is_stub = (len(new_exercises) == 1
                           and new_exercises[0].get("title") == _STUB_EXERCISE_TITLE)
            if not existing_exercises:
                for ex in new_exercises:
                    db.add(Exercise(topic_id=topic.id, **ex))
                print(f"    + {len(new_exercises)} exercise(s) added")
            elif is_stub_exercises and not new_is_stub:
                for row in existing_exercises:
                    db.delete(row)
                db.flush()
                for ex in new_exercises:
                    db.add(Exercise(topic_id=topic.id, **ex))
                print(f"    ~ {len(new_exercises)} exercise(s) upgraded from stub")
            else:
                print("    - Exercises exist, skipping")

            existing_quiz = db.query(Quiz).filter(Quiz.topic_id == topic.id).first()
            new_questions = t["quiz"].get("questions", [])
            new_quiz_is_stub = (len(new_questions) == 1
                                 and new_questions[0].get("question") == _STUB_QUIZ_QUESTION)
            if not existing_quiz:
                db.add(Quiz(topic_id=topic.id, **t["quiz"]))
                print("    + Quiz added")
            elif (existing_quiz.questions and len(existing_quiz.questions) == 1
                    and existing_quiz.questions[0].get("question") == _STUB_QUIZ_QUESTION
                    and not new_quiz_is_stub):
                existing_quiz.title = t["quiz"]["title"]
                existing_quiz.questions = t["quiz"]["questions"]
                existing_quiz.passing_score = t["quiz"].get("passing_score", existing_quiz.passing_score)
                print("    ~ Quiz upgraded from stub")
            else:
                print("    - Quiz exists, skipping")

            project = t.get("project")
            if project and project.get("title"):
                if not db.query(Project).filter(Project.topic_id == topic.id).first():
                    db.add(Project(topic_id=topic.id, **project))
                    print("    + Project added")
                else:
                    print("    - Project exists, skipping")
            else:
                print("    - No project defined for this topic, skipping")

    db.commit()
    print("Done.")
