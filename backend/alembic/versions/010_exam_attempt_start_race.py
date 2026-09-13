"""prevent duplicate concurrent in-progress exam attempts

`POST /exams/{exam_id}/start` (exam_controller.start_exam) reads whether
the caller already has an IN_PROGRESS attempt for this exam, and only if
not, inserts a new ExamAttempt row:

    attempts = db.query(ExamAttempt).filter(
        ExamAttempt.exam_id == exam_id, ExamAttempt.user_id == current_user.id,
    ).all()
    in_progress = next((a for a in attempts if a.status == in_progress), None)
    if in_progress:
        attempt = in_progress   # resume
    else:
        attempt = ExamAttempt(..., status=in_progress)
        db.add(attempt); db.commit()

That SELECT-then-INSERT is the same shape of TOCTOU migration 009 closed
on challenge_attempts, and here it is unguarded by any lock or
constraint at all. Confirmed exploitable, not theoretical: a
barrier-synchronised concurrency test
(tests/test_exam_concurrency.py::test_concurrent_start_requests_produce_at_most_one_in_progress_attempt)
reproducibly opens more than one IN_PROGRESS row for one user+exam from
concurrent /start requests.

Why this matters for more than bookkeeping: `Exam.questions` is a fixed
set for every attempt, and each attempt gets its own independent
`started_at`/deadline. Two simultaneous attempts hand a test-taker two
independent tries at the *same* fixed question set before either is
submitted — effectively a free extra look at the paper before committing
answers, which is exactly the certification-integrity guarantee the
proctoring/violation-tracking machinery around this feature exists to
protect. It also lets attempts_used inflate past what a legitimate
sequence of start→submit→start could produce, since two racing attempts
both count toward `max_attempts`.

Partial, not table-wide: a new attempt after a previous one is
submitted/passed/failed/flagged must stay legal — that is the ordinary
multi-attempt flow. Only "more than one IN_PROGRESS attempt per user per
exam at once" is the invariant being enforced.

`status` is a native Postgres enum (`examstatus`, see migration
001_initial_schema), so the predicate casts the literal explicitly, the
same as migration 009 did for `challengestatus`.

start_exam has no try/except around its insert today. A losing racer's
IntegrityError is caught by main.py's app-wide IntegrityError handler and
returned as a 409 — safe, if slightly less friendly than a bespoke
message; see the controller change alongside this migration for the
follow-up that turns it into the same "someone is already resuming this
attempt" 200/400 the pre-check already produces for the sequential case.

Revision ID: 010_exam_attempt_start_race
Revises: 009_challenge_enrollment_race
Create Date: 2026-09-12

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '010_exam_attempt_start_race'
down_revision: Union[str, None] = '009_challenge_enrollment_race'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_index(
        'uq_exam_attempts_one_in_progress',
        'exam_attempts',
        ['user_id', 'exam_id'],
        unique=True,
        postgresql_where=sa.text("status = 'in_progress'::examstatus"),
    )


def downgrade() -> None:
    op.drop_index('uq_exam_attempts_one_in_progress', table_name='exam_attempts')
