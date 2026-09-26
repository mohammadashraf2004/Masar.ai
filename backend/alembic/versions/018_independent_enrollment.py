"""independent course enrollment, typed prerequisites, readiness and stable content keys

The learning model stops being "choose a track, then reach its courses" and
becomes "choose any course". This migration adds only what that needs and
touches no existing learner data:

  * `course_enrollments` (created in 017 as the *entitlement* record) gains the
    learning lifecycle - `learning_status`, `started_at`, `completed_at`. It is
    the one enrollment table for a course; progress itself stays derived from
    `user_progress` and is never stored here.
  * `course_prerequisites.kind` separates the prerequisites the path generator
    orders by (`required`, what every existing row already meant) from advice
    (`recommended`), which only readiness and recommendations read.
  * `learning_profiles` records the two onboarding answers (programming and AI
    experience). Neither is required, and no career goal is.
  * `readiness_assessments` stores each short readiness check. The score is
    computed by the server from the stored questions; nothing in it is trusted
    from a client.
  * `source_key` on tool topics, lessons, exercises, quizzes and projects gives
    imported curriculum a stable identity, so re-running the importer updates a
    row in place instead of creating a second one - lesson ids live in learners'
    `user_progress.lessons_completed`, so they must never change.

Existing learners keep everything. Enrollment rows are backfilled for people who
already work in a course - a tool-course enrollment, or any recorded progress -
as `source='free'` (which never grants access to a course that is later made
paid; see `access_service`), so "My courses" is not empty on day one.

Revision ID: 018_independent_enrollment
Revises: 017_course_billing
Create Date: 2026-09-26

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "018_independent_enrollment"
down_revision: Union[str, None] = "017_course_billing"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

_SOURCE_KEYED = ("tool_topics", "lessons", "exercises", "quizzes", "projects")


def upgrade() -> None:
    # ── 017 declared `billing_orders.merchant_order_id` as a unique constraint plus
    # a plain index; the model (and every lookup by it) wants one unique index.
    op.drop_constraint("billing_orders_merchant_order_id_key", "billing_orders", type_="unique")
    op.drop_index("ix_billing_orders_merchant_order_id", table_name="billing_orders")
    op.create_index("ix_billing_orders_merchant_order_id", "billing_orders", ["merchant_order_id"], unique=True)

    # ── stable identity for imported curriculum ────────────────────────────
    for table in _SOURCE_KEYED:
        op.add_column(table, sa.Column("source_key", sa.String(), nullable=True))
        op.create_index(
            f"uq_{table}_source_key", table, ["source_key"], unique=True,
            postgresql_where=sa.text("source_key IS NOT NULL"),
        )

    # ── enrollment lifecycle ───────────────────────────────────────────────
    op.add_column(
        "course_enrollments",
        sa.Column("learning_status", sa.String(length=20), nullable=False, server_default="enrolled"),
    )
    op.add_column("course_enrollments", sa.Column("started_at", sa.DateTime(timezone=True), nullable=True))
    op.add_column("course_enrollments", sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True))
    op.create_check_constraint(
        "ck_course_enrollments_learning_status", "course_enrollments",
        "learning_status IN ('enrolled', 'in_progress', 'completed', 'paused')",
    )

    # ── prerequisite kind ──────────────────────────────────────────────────
    op.add_column(
        "course_prerequisites",
        sa.Column("kind", sa.String(), nullable=False, server_default="required"),
    )
    op.create_check_constraint(
        "ck_course_prerequisites_kind", "course_prerequisites", "kind IN ('required', 'recommended')",
    )

    # ── onboarding answers ─────────────────────────────────────────────────
    op.add_column("learning_profiles", sa.Column("programming_experience", sa.String(), nullable=True))
    op.add_column("learning_profiles", sa.Column("ai_experience", sa.String(), nullable=True))
    op.create_check_constraint(
        "ck_learning_profiles_programming_experience", "learning_profiles",
        "programming_experience IS NULL OR programming_experience IN ('none', 'basic', 'comfortable', 'professional')",
    )
    op.create_check_constraint(
        "ck_learning_profiles_ai_experience", "learning_profiles",
        "ai_experience IS NULL OR ai_experience IN ('none', 'basics', 'projects', 'applications')",
    )

    # ── readiness assessments ──────────────────────────────────────────────
    op.create_table(
        "readiness_assessments",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("course_id", sa.Integer(), nullable=False),
        sa.Column("question_count", sa.Integer(), nullable=False),
        sa.Column("correct_count", sa.Integer(), nullable=False),
        sa.Column("score", sa.Float(), nullable=False),
        sa.Column("skill_results", sa.JSON(), nullable=False),
        sa.Column("answers", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["course_id"], ["courses.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_readiness_assessments_id", "readiness_assessments", ["id"])
    op.create_index(
        "ix_readiness_assessments_user_course", "readiness_assessments", ["user_id", "course_id", "created_at"],
    )

    backfill_course_enrollments(op.get_bind())


def backfill_course_enrollments(bind) -> None:
    """Enroll, as `free`, everyone who already works in a course. Idempotent
    (`ON CONFLICT DO NOTHING`) and additive - it never edits an existing enrollment.
    A function of its own so the migration test can run it against real legacy rows.

    Only *free* courses: a `free` enrollment never grants access (see `access_service`),
    but recording one against a paid course would still be a claim the learner did
    not make."""
    statements = (
        # 1. Existing tool-course enrollments.
        """
        INSERT INTO course_enrollments
            (user_id, course_id, source, status, enrolled_at, learning_status, started_at, completed_at)
        SELECT te.user_id, c.id, 'free', 'active', COALESCE(te.enrolled_at, now()),
               CASE WHEN te.completed_at IS NOT NULL THEN 'completed'
                    WHEN COALESCE(te.progress_pct, 0) > 0 THEN 'in_progress'
                    ELSE 'enrolled' END,
               (SELECT MIN(up.started_at) FROM user_progress up
                  JOIN tool_topics tt ON tt.id = up.tool_topic_id
                 WHERE up.user_id = te.user_id AND tt.tool_course_id = te.tool_course_id),
               te.completed_at
          FROM tool_enrollments te
          JOIN courses c ON c.tool_course_id = te.tool_course_id
         WHERE c.is_free
        ON CONFLICT (user_id, course_id) DO NOTHING
    
        """,
        # 2. Anyone with recorded progress in a course's tool topics ...
        """
        INSERT INTO course_enrollments
            (user_id, course_id, source, status, enrolled_at, learning_status, started_at)
        SELECT up.user_id, c.id, 'free', 'active', COALESCE(MIN(up.started_at), now()), 'in_progress',
               MIN(up.started_at)
          FROM user_progress up
          JOIN tool_topics tt ON tt.id = up.tool_topic_id
          JOIN courses c ON c.tool_course_id = tt.tool_course_id
         WHERE c.is_free
         GROUP BY up.user_id, c.id
        ON CONFLICT (user_id, course_id) DO NOTHING
    
        """,
        # 3. ... and in a track level's topics. (A track enrollment alone is not turned
        # into course enrollments: it already became the learner's career goal in 012,
        # and "every course of the track" was never something they did.)
        """
        INSERT INTO course_enrollments
            (user_id, course_id, source, status, enrolled_at, learning_status, started_at)
        SELECT up.user_id, c.id, 'free', 'active', COALESCE(MIN(up.started_at), now()), 'in_progress',
               MIN(up.started_at)
          FROM user_progress up
          JOIN topics t ON t.id = up.topic_id
          JOIN courses c ON c.track_level_id = t.level_id
         WHERE c.is_free
         GROUP BY up.user_id, c.id
        ON CONFLICT (user_id, course_id) DO NOTHING
    
        """,
    )
    for statement in statements:
        bind.execute(sa.text(statement))


def downgrade() -> None:
    op.drop_index("ix_readiness_assessments_user_course", table_name="readiness_assessments")
    op.drop_index("ix_readiness_assessments_id", table_name="readiness_assessments")
    op.drop_table("readiness_assessments")

    op.drop_constraint("ck_learning_profiles_ai_experience", "learning_profiles", type_="check")
    op.drop_constraint("ck_learning_profiles_programming_experience", "learning_profiles", type_="check")
    op.drop_column("learning_profiles", "ai_experience")
    op.drop_column("learning_profiles", "programming_experience")

    op.drop_constraint("ck_course_prerequisites_kind", "course_prerequisites", type_="check")
    op.drop_column("course_prerequisites", "kind")

    op.drop_constraint("ck_course_enrollments_learning_status", "course_enrollments", type_="check")
    op.drop_column("course_enrollments", "completed_at")
    op.drop_column("course_enrollments", "started_at")
    op.drop_column("course_enrollments", "learning_status")

    for table in reversed(_SOURCE_KEYED):
        op.drop_index(f"uq_{table}_source_key", table_name=table)
        op.drop_column(table, "source_key")

    op.drop_index("ix_billing_orders_merchant_order_id", table_name="billing_orders")
    op.create_index("ix_billing_orders_merchant_order_id", "billing_orders", ["merchant_order_id"])
    op.create_unique_constraint("billing_orders_merchant_order_id_key", "billing_orders", ["merchant_order_id"])
