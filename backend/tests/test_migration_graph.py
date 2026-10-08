"""
The Alembic graph must never re-parent a revision that has already been
committed: a database stamped with that revision would treat any migration
inserted before it as applied and silently skip it.

024, 025 and 029 were committed directly on top of 019; 020-023 and 026-028
were committed later and therefore run after 029. These tests pin the committed
ancestry, prove the pin catches a re-parenting, and replay the exact upgrade a
database at 029 would perform.
"""
import re
import shutil
from pathlib import Path

import pytest
import sqlalchemy as sa
from alembic import command
from alembic.config import Config
from alembic.script import ScriptDirectory

import app.main  # noqa: F401
from app.db.session import engine

# Every revision that exists in committed history, with its committed parent.
# Append to this when a new migration is committed; never edit an entry.
RELEASED = {
    "001_initial_schema": None,
    "002_tool_course_progress": "001_initial_schema",
    "003_answer_submissions": "002_tool_course_progress",
    "004_security_constraints": "003_answer_submissions",
    "005_launch_promo_credits": "004_security_constraints",
    "006_arabic_first_content": "005_launch_promo_credits",
    "007_project_submission_code": "006_arabic_first_content",
    "008_exam_payment_ref_squatting": "007_project_submission_code",
    "009_challenge_enrollment_race": "008_exam_payment_ref_squatting",
    "010_exam_attempt_start_race": "009_challenge_enrollment_race",
    "011_learning_paths": "010_exam_attempt_start_race",
    "012_learning_profile_backfill": "011_learning_paths",
    "013_learner_skills": "012_learning_profile_backfill",
    "014_legal_acceptance": "013_learner_skills",
    "015_update_acknowledgements": "014_legal_acceptance",
    "016_course_role_relation": "015_update_acknowledgements",
    "017_course_billing": "016_course_role_relation",
    "018_independent_enrollment": "017_course_billing",
    "019_course_assets": "018_independent_enrollment",
    "024_optional_course_modules": "019_course_assets",
    "025_exercise_lesson_id": "024_optional_course_modules",
    "029_course_asset_arabic": "025_exercise_lesson_id",
    "020_user_tours": "029_course_asset_arabic",
}

# Schema that only the post-029 migrations create; a database at 029 must not
# have it, and `upgrade head` from 029 must add it.
AFTER_029_TABLES = {
    "user_tours", "billing_plans", "user_subscriptions", "subscription_orders",
    "subscription_payment_events", "subscription_refund_events", "vocabulary_terms", "vocabulary_term_relations",
    "vocabulary_term_associations", "mentor_evidence", "mentor_quiz_translations",
    "code_exercise_attempts", "lab_projects", "lab_attempts", "lab_execution_leases",
}
AFTER_029_COLUMNS = {
    ("course_roles", "position"), ("course_roles", "required"), ("course_roles", "section"),
    ("exercises", "exercise_type"), ("exercises", "grading_tests"), ("exercises", "hint_ar"),
    ("user_term_progress", "vocabulary_term_id"), ("mentor_sessions", "context_key"),
    ("subscription_orders", "reference_number"), ("subscription_orders", "refund_status"),
    ("subscription_orders", "provider_transaction_id"),
}
AT_029_COLUMNS = {
    ("tool_topics", "is_optional"), ("tool_topics", "completion_required"),
    ("exercises", "lesson_id"), ("course_assets", "alt_ar"), ("course_assets", "caption_ar"),
}


def _config():
    cfg = Config("alembic.ini")
    cfg.set_main_option("sqlalchemy.url", engine.url.render_as_string(hide_password=False))
    return cfg


def _columns():
    inspector = sa.inspect(engine)
    return {
        (table, column["name"])
        for table in inspector.get_table_names()
        for column in inspector.get_columns(table)
    }


def test_there_is_exactly_one_head_and_no_branch():
    script = ScriptDirectory.from_config(_config())
    assert len(script.get_heads()) == 1
    for rev in script.walk_revisions():
        assert not rev.is_merge_point
        assert len(script.get_revisions(rev.revision)[0].nextrev) <= 1, rev.revision


@pytest.mark.parametrize("revision,parent", sorted(RELEASED.items()))
def test_a_released_revision_keeps_its_committed_parent(revision, parent):
    script = ScriptDirectory.from_config(_config())
    assert script.get_revision(revision).down_revision == parent


def _ancestry_mismatches(script):
    """Released revisions whose ancestor set differs from committed history."""
    mismatches = []
    for revision in RELEASED:
        ancestors = {r.revision for r in script.iterate_revisions(revision, "base")}
        expected, cursor = set(), revision
        while cursor:
            expected.add(cursor)
            cursor = RELEASED[cursor]
        if ancestors != expected:
            mismatches.append(revision)
    return mismatches


def test_a_released_revision_has_exactly_its_committed_ancestors():
    assert _ancestry_mismatches(ScriptDirectory.from_config(_config())) == []


def test_the_ancestry_guard_catches_the_rejected_reparenting(tmp_path):
    # Negative control: the graph once proposed (and rejected) in review put
    # 024 after 023 and 029 after 028, so a database already at 029 would have
    # skipped 020-028. The guard above must flag exactly that.
    versions = Path(_config().get_main_option("script_location")) / "versions"
    shutil.copytree(versions, tmp_path / "versions", ignore=shutil.ignore_patterns("__pycache__"))
    reparent = {
        "020_user_tours": "019_course_assets",
        "024_optional_course_modules": "023_career_track_course_workflow",
        "026_mentor_evidence": "025_exercise_lesson_id",
        "029_course_asset_arabic": "028_deterministic_code_exercises",
        "030_project_lab": "029_course_asset_arabic",
    }
    for revision, parent in reparent.items():
        path = tmp_path / "versions" / f"{revision}.py"
        source = path.read_text(encoding="utf-8")
        patched = re.sub(r'^down_revision: .*$', f'down_revision: Union[str, None] = "{parent}"',
                         source, count=1, flags=re.M)
        assert patched != source, revision
        path.write_text(patched, encoding="utf-8")

    mismatches = _ancestry_mismatches(ScriptDirectory(str(tmp_path)))
    assert {"024_optional_course_modules", "025_exercise_lesson_id",
            "029_course_asset_arabic", "020_user_tours"} <= set(mismatches)


def test_a_database_at_released_029_gains_every_later_object_on_upgrade():
    cfg = _config()
    try:
        command.downgrade(cfg, "029_course_asset_arabic")
        tables = set(sa.inspect(engine).get_table_names())
        columns = _columns()
        assert not (AFTER_029_TABLES & tables)
        assert not (AFTER_029_COLUMNS & columns)
        assert AT_029_COLUMNS <= columns
    finally:
        command.upgrade(cfg, "head")
    tables = set(sa.inspect(engine).get_table_names())
    columns = _columns()
    assert AFTER_029_TABLES <= tables
    assert AFTER_029_COLUMNS <= columns
    assert AT_029_COLUMNS <= columns
    with engine.connect() as connection:
        plans = connection.execute(sa.text("SELECT code FROM billing_plans ORDER BY code")).scalars().all()
    assert plans == ["free", "pro"]
