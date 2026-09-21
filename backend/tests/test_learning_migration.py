"""
Migrations 011 and 012, and how existing learners are carried across.

The rule under test (see the docstring of 012_learning_profile_backfill): a
career goal is inferred from an enrolment ONLY when exactly one track is
involved; a level and fields are never invented; the learner is then asked to
finish the new onboarding. The tests insert real legacy rows and run the
migration's own backfill function, not a copy of its logic.
"""
import importlib.util
import pathlib

import pytest
import sqlalchemy as sa
from alembic import command
from alembic.autogenerate import compare_metadata
from alembic.config import Config
from alembic.migration import MigrationContext
from sqlalchemy.exc import IntegrityError

import app.main  # noqa: F401
from app.db.session import Base, engine
from app.models.learning import CareerTrack
from app.models.learning_path import (
    CareerRole, Course, LearningField, LearningLevel, LearningPath, LearningProfile,
)
from app.models.progress import Enrollment
from tests.learning_fixtures import *  # noqa: F401,F403
from tests.learning_fixtures import register

VERSIONS = pathlib.Path(__file__).resolve().parents[1] / "alembic" / "versions"
LEARNING_TABLES = {
    "learning_levels", "learning_fields", "learning_field_prerequisites", "skills", "career_roles",
    "career_role_fields", "career_role_skills", "courses", "course_fields", "course_roles",
    "course_skills", "course_prerequisites", "path_stages", "path_stage_courses", "path_templates",
    "path_template_stages", "learning_profiles", "learning_paths", "learner_skills",
}


def _load(name):
    spec = importlib.util.spec_from_file_location(name, VERSIONS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


BACKFILL = _load("012_learning_profile_backfill")
LEARNER_SKILLS = _load("013_learner_skills")


# ─── Reference vocabulary ───────────────────────────────────────────────────

def test_the_migration_installs_the_controlled_vocabulary(learn_db):
    assert [l.slug for l in learn_db.query(LearningLevel).order_by(LearningLevel.rank)] == \
        ["beginner", "intermediate", "advanced"]
    assert [f.slug for f in learn_db.query(LearningField).order_by(LearningField.position)] == \
        ["data", "machine-learning", "nlp", "computer-vision", "speech", "multimodal"]
    assert [r.slug for r in learn_db.query(CareerRole).order_by(CareerRole.position)] == \
        ["data-analyst", "ml-engineer", "ai-developer", "mlops-engineer", "ai-engineer"]


def test_every_vocabulary_row_has_an_arabic_name_and_multimodal_starts_at_advanced(learn_db):
    assert all(l.name_ar and l.description_ar for l in learn_db.query(LearningLevel))
    assert all(f.name_ar and f.description_ar for f in learn_db.query(LearningField))
    assert all(r.title_ar and r.description_ar for r in learn_db.query(CareerRole))
    multimodal = learn_db.query(LearningField).filter(LearningField.slug == "multimodal").one()
    assert multimodal.min_level.slug == "advanced"
    assert all(f.min_level_id is None for f in learn_db.query(LearningField) if f.slug != "multimodal")


# ─── Constraints the schema promises ────────────────────────────────────────

def _refused(db, *rows):
    with pytest.raises(IntegrityError):
        with db.begin_nested():
            db.add_all(rows)
            db.flush()


def test_a_course_must_point_at_exactly_one_content_source(learn_db, learn_catalog):
    level = learn_db.query(LearningLevel).first()
    from app.models.learning import TrackLevel
    from app.models.tool_course import ToolCourse

    tool = learn_db.query(ToolCourse).first()
    track_level = learn_db.query(TrackLevel).first()
    _refused(learn_db, Course(slug="both", kind="tool_course", tool_course_id=tool.id,
                              track_level_id=track_level.id, level_id=level.id))
    _refused(learn_db, Course(slug="neither", kind="tool_course", level_id=level.id))
    _refused(learn_db, Course(slug="wrong-kind", kind="track_level", tool_course_id=tool.id, level_id=level.id))


def test_one_piece_of_content_is_catalogued_once(learn_db, learn_catalog):
    from app.models.tool_course import ToolCourse

    tool = learn_db.query(ToolCourse).filter(ToolCourse.slug == "langchain").one()
    level = learn_db.query(LearningLevel).first()
    _refused(learn_db, Course(slug="langchain-again", kind="tool_course", tool_course_id=tool.id, level_id=level.id))


def test_a_learner_has_at_most_one_active_path_but_any_number_archived(learn_client, learn_db):
    who = register(learn_client)
    level = learn_db.query(LearningLevel).first()
    role = learn_db.query(CareerRole).first()

    def path(status):
        return LearningPath(user_id=who["id"], level_id=level.id, career_role_id=role.id, status=status)

    learn_db.add_all([path("archived"), path("archived"), path("paused"), path("active")])
    learn_db.flush()
    _refused(learn_db, path("active"))


def test_a_path_status_outside_the_vocabulary_is_refused(learn_client, learn_db):
    who = register(learn_client)
    level = learn_db.query(LearningLevel).first()
    role = learn_db.query(CareerRole).first()
    _refused(learn_db, LearningPath(user_id=who["id"], level_id=level.id, career_role_id=role.id, status="vibing"))


def test_a_learner_has_one_profile(learn_client, learn_db):
    who = register(learn_client)
    learn_db.add(LearningProfile(user_id=who["id"], field_slugs=[], known_skill_slugs=[]))
    learn_db.flush()
    _refused(learn_db, LearningProfile(user_id=who["id"], field_slugs=[], known_skill_slugs=[]))


def test_deleting_a_user_takes_their_learning_data_with_them(learn_db):
    from app.models.user import User

    user = User(email="gone@example.com", full_name="Gone", hashed_password="x")
    learn_db.add(user)
    learn_db.flush()
    level = learn_db.query(LearningLevel).first()
    role = learn_db.query(CareerRole).first()
    learn_db.add_all([
        LearningProfile(user_id=user.id, field_slugs=["nlp"], known_skill_slugs=[]),
        LearningPath(user_id=user.id, level_id=level.id, career_role_id=role.id, status="active"),
    ])
    learn_db.flush()
    learn_db.execute(sa.text("DELETE FROM users WHERE id = :id"), {"id": user.id})
    assert learn_db.query(LearningProfile).filter(LearningProfile.user_id == user.id).count() == 0
    assert learn_db.query(LearningPath).filter(LearningPath.user_id == user.id).count() == 0


def test_the_schema_matches_the_models(learn_db):
    """Migrations are hand-written, so nothing else notices when a model gains
    a column or a NOT NULL that the migration forgot."""
    with engine.connect() as connection:
        diffs = compare_metadata(MigrationContext.configure(connection), Base.metadata)

    def table_of(diff):
        item = diff[1] if isinstance(diff, tuple) and diff[0] in ("add_table", "remove_table") else None
        if item is not None:
            return item.name
        if diff[0] in ("add_column", "remove_column", "modify_nullable", "modify_type"):
            return diff[2]
        if diff[0] in ("add_index", "remove_index", "add_constraint", "remove_constraint"):
            return diff[1].table.name
        return None

    structural = {"add_table", "remove_table", "add_column", "remove_column", "modify_nullable", "modify_type"}
    ours = [d for d in _flatten(diffs) if table_of(d) in LEARNING_TABLES and d[0] in structural]
    assert ours == [], ours


def _flatten(diffs):
    for d in diffs:
        if isinstance(d, list):
            yield from _flatten(d)
        else:
            yield d


# ─── Backfill: who is carried across, and what is deliberately not ──────────

def _track(db, slug):
    row = CareerTrack(slug=slug, title=slug, estimated_weeks=1)
    db.add(row)
    db.flush()
    return row


def _enrol(db, user_id, track, active=True):
    db.add(Enrollment(user_id=user_id, track_id=track.id, is_active=active))
    db.flush()


def _profile_of(db, user_id):
    return db.query(LearningProfile).filter(LearningProfile.user_id == user_id).first()


def test_one_active_track_becomes_a_career_goal_and_nothing_else(learn_client, learn_db):
    who = register(learn_client)
    track = _track(learn_db, "ai-developer")
    _enrol(learn_db, who["id"], track)

    assert BACKFILL.backfill_profiles(learn_db) >= 1

    profile = _profile_of(learn_db, who["id"])
    assert profile.career_role.slug == "ai-developer"
    assert profile.level_id is None                    # not invented
    assert profile.field_slugs == []                    # not invented
    assert profile.known_skill_slugs == []
    assert profile.onboarding_completed_at is None      # so the app asks
    assert profile.source == "migrated"
    assert profile.migrated_from["rule"] == "single_active_enrollment"
    assert profile.migrated_from["track_slug"] == "ai-developer"


def test_a_migrated_learner_is_asked_to_finish_onboarding_and_keeps_their_goal(learn_client, learn_db):
    who = register(learn_client)
    _enrol(learn_db, who["id"], _track(learn_db, "ml-engineer"))
    BACKFILL.backfill_profiles(learn_db)

    profile = learn_client.get("/api/v1/learning/my-profile", headers=who["headers"]).json()
    assert profile["needs_onboarding"] is True and profile["onboarding_completed"] is False
    assert profile["career_goal"]["slug"] == "ml-engineer"       # carried over
    assert profile["level"] is None and profile["fields"] == []  # asked, not guessed
    assert profile["source"] == "migrated"


def test_finishing_onboarding_takes_over_the_row_and_keeps_the_audit_trail(learn_client, learn_db):
    who = register(learn_client)
    _enrol(learn_db, who["id"], _track(learn_db, "ai-developer"))
    BACKFILL.backfill_profiles(learn_db)
    done = learn_client.put("/api/v1/learning/my-profile", headers=who["headers"],
                            json={"level": "intermediate", "fields": ["nlp"]}).json()
    assert done["onboarding_completed"] is True and done["career_goal"]["slug"] == "ai-developer"
    row = _profile_of(learn_db, who["id"])
    assert row.source == "onboarding" and row.migrated_from["track_slug"] == "ai-developer"


def test_two_different_tracks_are_ambiguous_so_no_goal_is_guessed(learn_client, learn_db):
    who = register(learn_client)
    _enrol(learn_db, who["id"], _track(learn_db, "data-analyst"))
    _enrol(learn_db, who["id"], _track(learn_db, "mlops-engineer"))
    BACKFILL.backfill_profiles(learn_db)
    assert _profile_of(learn_db, who["id"]) is None
    assert learn_client.get("/api/v1/learning/my-profile", headers=who["headers"]).json()["needs_onboarding"] is True


def test_repeat_enrolments_in_one_track_are_still_one_track(learn_client, learn_db):
    who = register(learn_client)
    track = _track(learn_db, "ai-developer")
    _enrol(learn_db, who["id"], track)
    _enrol(learn_db, who["id"], track)
    BACKFILL.backfill_profiles(learn_db)
    assert _profile_of(learn_db, who["id"]).career_role.slug == "ai-developer"


def test_inactive_enrolments_do_not_count(learn_client, learn_db):
    who = register(learn_client)
    _enrol(learn_db, who["id"], _track(learn_db, "ai-developer"), active=False)
    BACKFILL.backfill_profiles(learn_db)
    assert _profile_of(learn_db, who["id"]) is None


def test_an_inactive_second_enrolment_does_not_make_the_first_ambiguous(learn_client, learn_db):
    who = register(learn_client)
    _enrol(learn_db, who["id"], _track(learn_db, "ai-developer"))
    _enrol(learn_db, who["id"], _track(learn_db, "ml-engineer"), active=False)
    BACKFILL.backfill_profiles(learn_db)
    assert _profile_of(learn_db, who["id"]).career_role.slug == "ai-developer"


def test_a_track_that_is_not_a_career_goal_is_left_alone(learn_client, learn_db):
    who = register(learn_client)
    _enrol(learn_db, who["id"], _track(learn_db, "some-custom-track"))
    BACKFILL.backfill_profiles(learn_db)
    assert _profile_of(learn_db, who["id"]) is None


def test_a_learner_with_no_enrolment_gets_no_row(learn_client, learn_db):
    who = register(learn_client)
    BACKFILL.backfill_profiles(learn_db)
    assert _profile_of(learn_db, who["id"]) is None


def test_the_experience_level_field_is_deliberately_not_carried_over(learn_client, learn_db):
    """`users.experience_level` defaults to beginner and the sign-up form
    pre-selects it, so a stored value cannot be told from a choice."""
    who = register(learn_client)
    from app.models.user import ExperienceLevel, User

    learn_db.query(User).filter(User.id == who["id"]).update({"experience_level": ExperienceLevel.advanced})
    _enrol(learn_db, who["id"], _track(learn_db, "ai-developer"))
    BACKFILL.backfill_profiles(learn_db)
    assert _profile_of(learn_db, who["id"]).level_id is None


def test_the_backfill_is_idempotent_and_never_clobbers_a_completed_profile(learn_client, learn_db):
    migrated, finished = register(learn_client), register(learn_client)
    track = _track(learn_db, "ai-developer")
    _enrol(learn_db, migrated["id"], track)
    _enrol(learn_db, finished["id"], track)
    learn_client.put("/api/v1/learning/my-profile", headers=finished["headers"],
                     json={"level": "advanced", "fields": ["speech"], "career_goal": "ai-engineer"})

    BACKFILL.backfill_profiles(learn_db)
    assert BACKFILL.backfill_profiles(learn_db) == 0  # nothing left to do

    kept = _profile_of(learn_db, finished["id"])
    assert kept.career_role.slug == "ai-engineer" and kept.field_slugs == ["speech"]  # untouched
    assert _profile_of(learn_db, migrated["id"]).career_role.slug == "ai-developer"


def test_existing_role_enrolments_keep_working_after_the_migration(learn_client, learn_db):
    who = register(learn_client)
    track = _track(learn_db, "ai-developer")
    _enrol(learn_db, who["id"], track)
    BACKFILL.backfill_profiles(learn_db)
    mine = learn_client.get("/api/v1/tracks/my-enrollments", headers=who["headers"])
    assert mine.status_code == 200 and [e["track"]["slug"] for e in mine.json()] == ["ai-developer"]


def test_only_profiles_the_learner_never_touched_are_undone(learn_client, learn_db):
    untouched, touched = register(learn_client), register(learn_client)
    track = _track(learn_db, "ai-developer")
    _enrol(learn_db, untouched["id"], track)
    _enrol(learn_db, touched["id"], track)
    BACKFILL.backfill_profiles(learn_db)
    learn_client.put("/api/v1/learning/my-profile", headers=touched["headers"],
                     json={"level": "beginner", "fields": ["nlp"]})
    BACKFILL.undo_backfill(learn_db)
    assert _profile_of(learn_db, untouched["id"]) is None
    assert _profile_of(learn_db, touched["id"]) is not None


def test_ai_engineer_track_copy_is_replaced_only_where_it_is_still_the_original(learn_db):
    old, new = BACKFILL._OLD_AI_ENGINEER_COPY, BACKFILL._NEW_AI_ENGINEER_COPY
    track = _track(learn_db, "ai-engineer")
    track.description = old
    learn_db.flush()
    BACKFILL._swap_copy(learn_db, old, new)
    learn_db.refresh(track)
    assert track.description == new
    assert "combines" not in new.lower()

    track.description = "Edited by an admin."
    learn_db.flush()
    BACKFILL._swap_copy(learn_db, old, new)
    learn_db.refresh(track)
    assert track.description == "Edited by an admin."


def test_the_backfill_reads_nothing_from_the_fragile_related_track_ids():
    """Those lists hold raw row ids, which depend on seed order (and are already
    wrong in databases where test rows once took the low ids)."""
    assert "related_track_ids" not in BACKFILL._BACKFILL_SQL


# ─── Reversibility ──────────────────────────────────────────────────────────

def test_the_chain_downgrades_and_upgrades_cleanly():
    cfg = Config("alembic.ini")
    cfg.set_main_option("sqlalchemy.url", engine.url.render_as_string(hide_password=False))
    try:
        command.downgrade(cfg, "010_exam_attempt_start_race")
        tables = set(sa.inspect(engine).get_table_names())
        assert not (LEARNING_TABLES & tables)             # every new table is gone...
        assert {"users", "career_tracks", "enrollments", "tool_courses"} <= tables  # ...and nothing else was touched
    finally:
        command.upgrade(cfg, "head")
    tables = set(sa.inspect(engine).get_table_names())
    assert LEARNING_TABLES <= tables
    with engine.connect() as connection:
        assert connection.execute(sa.text("SELECT count(*) FROM learning_levels")).scalar() == 3
        assert connection.execute(sa.text("SELECT count(*) FROM learning_fields")).scalar() == 6
        assert connection.execute(sa.text("SELECT count(*) FROM career_roles")).scalar() == 5


# ─── 013: learner skills ────────────────────────────────────────────────────

def test_declared_skills_on_a_profile_are_copied_as_self_declared_and_known(learn_client, learn_catalog, learn_db):
    from app.models.learning_path import LearnerSkill, Skill

    who = register(learn_client)
    learn_db.add(LearningProfile(user_id=who["id"], field_slugs=[],
                                 known_skill_slugs=["rag", "rag", "llms", "no-such-skill"]))
    learn_db.flush()

    written = LEARNER_SKILLS.copy_declared_skills(learn_db.connection())
    assert written == 2                                              # duplicate collapsed, unknown slug dropped
    rows = learn_db.query(LearnerSkill).filter(LearnerSkill.user_id == who["id"]).all()
    assert {(learn_db.get(Skill, r.skill_id).slug, r.status, r.source) for r in rows} == {
        ("rag", "known", "self_declared"), ("llms", "known", "self_declared"),
    }                                                                # a claim - never "mastered"
    assert LEARNER_SKILLS.copy_declared_skills(learn_db.connection()) == 0   # running it again changes nothing


def test_the_known_skill_migration_leaves_the_old_column_in_place(learn_db):
    columns = {c["name"] for c in sa.inspect(engine).get_columns("learning_profiles")}
    assert "known_skill_slugs" in columns                            # nothing destroyed


def test_existing_accounts_are_not_backfilled_with_an_acceptance(learn_client, learn_db):
    """014 adds the columns and stops: an account created without accepting stays NULL,
    which the API reports as 'acceptance required'."""
    from app.models.user import User

    columns = {c["name"] for c in sa.inspect(engine).get_columns("users")}
    assert {"terms_version", "terms_accepted_at", "privacy_version", "privacy_accepted_at"} <= columns
    legacy = User(email="legacy-legal@example.com", full_name="Legacy", hashed_password="x")
    learn_db.add(legacy)
    learn_db.flush()
    assert legacy.terms_version is None and legacy.privacy_accepted_at is None
    assert legacy.requires_legal_acceptance is True
