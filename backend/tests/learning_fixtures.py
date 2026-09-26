"""
Shared fixtures for the learning-path tests.

Import with `from tests.learning_fixtures import *  # noqa: F401,F403`.

Isolation
---------
Every test here runs inside one outer transaction that is rolled back at the
end, with the app's session joined to it through a SAVEPOINT
(`join_transaction_mode="create_savepoint"`). Services call `db.commit()` for
real, and that commit only releases the savepoint — so nothing a test writes
survives it, and nothing another test file left behind is visible to it
beyond the migration's reference vocabulary. That is what lets these tests
build a full realistic catalogue per test without polluting (or being
polluted by) the shared test database the rest of the suite uses.

Realism
-------
`learn_catalog` builds the same *content sources* the production database has
— the AI Developer track with ten levels and the tool courses, some with
lessons and most as shells — and then runs the real seed script over them. The
tests therefore exercise the shipped configuration, not a hand-made stand-in.
"""
import uuid
from typing import Dict, List, Tuple

import pytest
from sqlalchemy.orm import Session

import app.main  # noqa: F401 — imports every model so relationships resolve
from app.db.session import engine, get_db
from app.models.learning import (
    CareerTrack, DifficultyLevel, Exercise, Lesson, Topic, TrackLevel,
)
from app.models.progress import UserProgress
from app.models.tool_course import ToolCourse, ToolTopic

PASSWORD = "correcthorsebatterystaple"

# (order, title, [(topic title, difficulty, skill_tags)]) — modelled on the
# real ai-developer track: same shape, same tag vocabulary.
_D = DifficultyLevel
TRACK_LEVELS = [
    (1, "Level 1: AI Engineering Foundations", [(_D.beginner, ["llm", "system-design"])] * 2),
    (2, "Level 2: LLM Integration", [(_D.beginner, ["llm-integration", "api"])] * 2),
    (3, "Level 3: RAG & Knowledge Systems", [(_D.intermediate, ["rag", "retrieval"])] * 2),
    (4, "Level 4: Prompt Engineering", [(_D.intermediate, ["prompt-engineering"])] * 2),
    (5, "Level 5: Embeddings & Semantic Search", [(_D.intermediate, ["embeddings", "semantic-search"])] * 2),
    (6, "Level 6: Advanced RAG", [(_D.intermediate, ["rag", "embeddings", "retrieval"])] * 2),
    (7, "Level 7: AI Agents & Orchestration", [(_D.intermediate, ["ai-agents"])] * 2),
    (8, "Level 8: Deployment & Integration Frameworks", [(_D.advanced, ["fastapi", "production", "architecture"])] * 2),
    (9, "Level 9: Multimodal AI", [(_D.advanced, ["multimodal", "vlm"])] * 2),
    (10, "Level 10: AI Evaluation & Observability", [(_D.intermediate, ["evaluation", "observability"])] * 2),
]

# (slug, difficulty, has_lessons, skill_tags)
TOOL_COURSES = [
    ("langchain", _D.intermediate, True, ["langchain", "llm"]),
    ("langgraph", _D.advanced, True, ["langgraph"]),
    ("llamaindex", _D.intermediate, True, ["llamaindex", "rag"]),
    ("qdrant", _D.intermediate, True, ["qdrant", "vector-database"]),
    ("fastapi-serving", _D.intermediate, True, ["fastapi", "api-design"]),
    ("openai-api", _D.beginner, False, []),
    ("hugging-face", _D.beginner, False, []),
    ("pinecone", _D.intermediate, False, []),
    ("weaviate", _D.intermediate, False, []),
    ("mlflow", _D.intermediate, False, []),
    ("dvc", _D.intermediate, False, []),
    ("wandb", _D.intermediate, False, []),
    ("airflow", _D.advanced, False, []),
    ("dbt", _D.intermediate, False, []),
    ("great-expectations", _D.intermediate, False, []),
    ("streamlit", _D.beginner, False, []),
]


# Placeholder legacy tracks, as seeded by seeds/tracks_all.py: five levels each,
# every one a single empty topic. The directory-course registry uses these as
# stable, empty navigation sources until its local adapters load lesson content.
PLACEHOLDER_TRACKS = {
    "data-analyst": ["Python & SQL foundations", "Data analysis with Pandas", "Data visualisation",
                     "Statistics for analysts", "BI dashboards & reporting"],
    "ml-engineer": ["ML fundamentals", "Feature engineering", "Deep learning with PyTorch",
                    "Model evaluation", "Transformers & fine-tuning"],
}


def create_content_sources(db: Session) -> Dict[str, object]:
    """The existing content the catalogue points at. Returns the ids tests need
    to record progress against."""
    track = CareerTrack(slug="ai-developer", title="AI Developer", estimated_weeks=14)
    db.add(track)
    db.flush()

    for slug, title in (("mlops-engineer", "MLOps Engineer"), ("ai-engineer", "AI Engineer")):
        db.add(CareerTrack(slug=slug, title=title, estimated_weeks=12))
    db.flush()

    lessons_of_level: Dict[int, List[Tuple[int, int]]] = {}
    for order, title, topics in TRACK_LEVELS:
        level = TrackLevel(track_id=track.id, title=title, order=order)
        db.add(level)
        db.flush()
        lessons_of_level[order] = []
        for i, (difficulty, tags) in enumerate(topics, start=1):
            topic = Topic(level_id=level.id, title=f"Topic {order}.{i}", slug=f"t-{order}-{i}",
                          order=i, difficulty=difficulty, estimated_hours=2.0, skill_tags=tags)
            db.add(topic)
            db.flush()
            lesson = Lesson(topic_id=topic.id, title="L", content="c", order=1)
            db.add(lesson)
            db.flush()
            lessons_of_level[order].append((topic.id, lesson.id))

    tool_ids: Dict[str, ToolCourse] = {}
    lessons_of_tool: Dict[str, List[Tuple[int, int]]] = {}
    for slug, difficulty, has_lessons, tags in TOOL_COURSES:
        course = ToolCourse(slug=slug, title=slug.title(), category="Test", difficulty=difficulty,
                            estimated_hours=6.0, related_track_ids=[], is_active=True)
        db.add(course)
        db.flush()
        tool_ids[slug] = course
        lessons_of_tool[slug] = []
        if has_lessons:
            topic = ToolTopic(tool_course_id=course.id, title="Only", slug=f"{slug}-1", order=1,
                              difficulty=difficulty, estimated_hours=6.0, skill_tags=tags,
                              prerequisite_ids=[])
            db.add(topic)
            db.flush()
            lesson = Lesson(tool_topic_id=topic.id, title="L", content="c", order=1)
            db.add(lesson)
            db.flush()
            lessons_of_tool[slug].append((topic.id, lesson.id))
    # The other tracks exist in production only as placeholders: levels with one
    # empty topic and no lessons (seeds/tracks_all.py). The catalogue's shell
    # and directory courses point at these, so the fixture has to have them.
    for track_slug, level_titles in PLACEHOLDER_TRACKS.items():
        shell_track = CareerTrack(slug=track_slug, title=track_slug, estimated_weeks=12)
        db.add(shell_track)
        db.flush()
        for order, title in enumerate(level_titles, start=1):
            level = TrackLevel(track_id=shell_track.id, title=title, order=order)
            db.add(level)
            db.flush()
            db.add(Topic(level_id=level.id, title=title, slug=f"{track_slug}-{order}", order=1,
                         difficulty=_D.intermediate, estimated_hours=8.0, skill_tags=[]))
            db.flush()
    db.commit()
    return {"track": track, "level_lessons": lessons_of_level, "tool_lessons": lessons_of_tool}


def complete_level(db: Session, user_id: int, content: Dict[str, object], order: int) -> None:
    """Finish every lesson of one track level for a user."""
    for topic_id, lesson_id in content["level_lessons"][order]:
        db.add(UserProgress(user_id=user_id, topic_id=topic_id, lessons_completed=[lesson_id],
                            exercises_completed=[]))
    db.commit()


def complete_tool(db: Session, user_id: int, content: Dict[str, object], slug: str) -> None:
    for topic_id, lesson_id in content["tool_lessons"][slug]:
        db.add(UserProgress(user_id=user_id, tool_topic_id=topic_id, lessons_completed=[lesson_id],
                            exercises_completed=[]))
    db.commit()


# ─── Fixtures ───────────────────────────────────────────────────────────────

@pytest.fixture()
def logs_enabled():
    """Turn application loggers back on for the duration of a test.

    The session's migration fixture runs Alembic in-process, and `alembic/env.py`
    calls `logging.config.fileConfig`, whose default is to *disable every logger
    that already exists* - which by then includes `security` and every `app.*`
    logger. In production Alembic runs in its own process, so nothing is lost;
    in the test session it silently mutes every log line, and a test asserting
    on one would fail for a reason unrelated to the code under test.
    """
    import logging

    touched = []
    for name, logger in list(logging.root.manager.loggerDict.items()):
        if isinstance(logger, logging.Logger) and logger.disabled and (name == "security" or name.startswith("app")):
            logger.disabled = False
            touched.append(logger)
    yield
    for logger in touched:
        logger.disabled = True


@pytest.fixture()
def learn_db():
    connection = engine.connect()
    outer = connection.begin()
    session = Session(bind=connection, autoflush=False, join_transaction_mode="create_savepoint")
    try:
        yield session
    finally:
        session.close()
        outer.rollback()
        connection.close()


@pytest.fixture()
def learn_client(learn_db, logs_enabled):
    # Depends on `logs_enabled` so that every request in these tests actually
    # executes the application's log statements. With loggers muted (see that
    # fixture), a malformed `extra=` in a log call is invisible - and it would
    # 500 in production, where logging is on.
    from fastapi.testclient import TestClient
    from app.main import app

    def _override():
        yield learn_db

    app.dependency_overrides[get_db] = _override
    try:
        with TestClient(app) as client:
            yield client
    finally:
        app.dependency_overrides.pop(get_db, None)


@pytest.fixture()
def learn_catalog(learn_db):
    """Content sources + the real seed. Returns the content handles."""
    from seeds.seed_learning_paths import seed_learning_catalog

    content = create_content_sources(learn_db)
    seed_learning_catalog(learn_db)
    return content


def register(client, *, verified: bool = False) -> Dict[str, object]:
    email = f"learn-{uuid.uuid4().hex[:12]}@example.com"
    resp = client.post("/api/v1/auth/register", json={"accept_terms": True, "accept_privacy": True, 
        "email": email, "full_name": "Learner Test", "password": PASSWORD,
    })
    assert resp.status_code == 201, resp.text
    body = resp.json()
    return {
        "id": body["user"]["id"],
        "email": email,
        "headers": {"Authorization": f"Bearer {body['access_token']}"},
    }


def make_admin(db: Session, user_id: int) -> None:
    from app.models.user import User, UserRole

    db.query(User).filter(User.id == user_id).update({"role": UserRole.admin})
    db.commit()
