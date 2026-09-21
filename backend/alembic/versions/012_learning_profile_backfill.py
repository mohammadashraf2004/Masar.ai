"""map legacy track enrolments onto learning profiles

Existing learners chose a *role track*; the new model asks for a level, a set
of fields and a career goal. This migration carries over the one thing an
enrolment genuinely tells us — which career goal the learner was working
toward — and refuses to invent the rest.

The rule, and why each half is what it is
-----------------------------------------
* **Career goal** is set only when the learner has active enrolments in
  exactly ONE distinct track. The five career-goal slugs equal the five track
  slugs, so the join is by slug — exact, and independent of row ids. Two or
  more distinct tracks are ambiguous (which one is the goal?), so no profile
  is written and the learner simply meets the new onboarding.
* **Level is left NULL.** `users.experience_level` defaults to `beginner` and
  the registration form pre-selects it, so a stored `beginner` cannot be told
  apart from a learner who never chose. Treating it as an answer would put
  words in their mouth.
* **Fields are left empty.** A track spans fields (the AI Developer track
  covers NLP *and* multimodal), so no single field can be read off it.
* `onboarding_completed_at` stays NULL, which is what makes the app ask them
  to finish onboarding. `source = 'migrated'` and `migrated_from` record
  exactly what the row was derived from.

Nothing here reads `tool_courses.related_track_ids`. That list holds raw row
ids, which depend on seed order and are already wrong in databases where test
rows once occupied the low ids.

The other change is one line of copy. The AI Engineer track's description
told learners it "combines" the other roles; that is the framing this release
retires, so the sentence is replaced — but only where it still holds the
original text, so a description an admin has edited is left alone.

Revision ID: 012_learning_profile_backfill
Revises: 011_learning_paths
Create Date: 2026-09-19

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '012_learning_profile_backfill'
down_revision: Union[str, None] = '011_learning_paths'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


_OLD_AI_ENGINEER_COPY = (
    "The complete path. Combines data analysis, ML engineering, AI development, "
    "and MLOps into a full production AI engineering skillset."
)
_NEW_AI_ENGINEER_COPY = (
    "Design and ship complete AI systems end to end, in the specialization you "
    "choose: NLP, Computer Vision, Speech or Multimodal."
)

# `enrollments.is_active` is nullable; the API only ever treats an explicit
# true as active, so this does too. Idempotent: ON CONFLICT leaves any profile
# that already exists exactly as it is.
_BACKFILL_SQL = """
INSERT INTO learning_profiles
    (user_id, career_role_id, field_slugs, known_skill_slugs, source, migrated_from)
SELECT s.user_id,
       r.id,
       '[]'::json,
       '[]'::json,
       'migrated',
       json_build_object(
           'rule', 'single_active_enrollment',
           'track_slug', t.slug,
           'enrollment_id', s.enrollment_id
       )
FROM (
    SELECT e.user_id,
           MIN(e.track_id) AS track_id,
           MIN(e.id)       AS enrollment_id
    FROM enrollments e
    WHERE e.is_active IS TRUE
    GROUP BY e.user_id
    HAVING COUNT(DISTINCT e.track_id) = 1
) AS s
JOIN career_tracks t ON t.id = s.track_id
JOIN career_roles  r ON r.slug = t.slug
ON CONFLICT (user_id) DO NOTHING
"""

# Removes only rows this migration wrote and nobody has since touched — a
# learner who finished onboarding flipped `source` to 'onboarding'.
_UNDO_SQL = """
DELETE FROM learning_profiles
WHERE source = 'migrated' AND onboarding_completed_at IS NULL
"""


def backfill_profiles(bind) -> int:
    """Create a career-goal-only profile for each learner with exactly one
    active track enrolment. Returns how many rows were inserted."""
    return bind.execute(sa.text(_BACKFILL_SQL)).rowcount


def undo_backfill(bind) -> int:
    return bind.execute(sa.text(_UNDO_SQL)).rowcount


def _swap_copy(bind, old: str, new: str) -> None:
    bind.execute(
        sa.text(
            "UPDATE career_tracks SET description = :new "
            "WHERE slug = 'ai-engineer' AND description = :old"
        ),
        {"old": old, "new": new},
    )


def upgrade() -> None:
    bind = op.get_bind()
    backfill_profiles(bind)
    _swap_copy(bind, _OLD_AI_ENGINEER_COPY, _NEW_AI_ENGINEER_COPY)


def downgrade() -> None:
    bind = op.get_bind()
    _swap_copy(bind, _NEW_AI_ENGINEER_COPY, _OLD_AI_ENGINEER_COPY)
    undo_backfill(bind)
