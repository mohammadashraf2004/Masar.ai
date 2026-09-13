"""prevent duplicate concurrent challenge enrolments

`POST /challenges/{slug}/enroll` (challenge_controller.enroll_challenge) reads
whether the caller already holds an ENROLLED attempt, and only if not,
charges the challenge's credit_cost through wallet_service.deduct_credits()
and inserts a new ChallengeAttempt row:

    active = db.query(ChallengeAttempt).filter(
        ChallengeAttempt.user_id == current_user.id,
        ChallengeAttempt.challenge_id == ch.id,
        ChallengeAttempt.status == ChallengeStatus.enrolled,
    ).first()
    if active: -> 400

    charge = deduct_credits(...)          # commits immediately
    attempt = ChallengeAttempt(..., status=enrolled)
    db.add(attempt); db.commit()

That SELECT-then-charge-then-INSERT is a classic TOCTOU: two concurrent
requests for the same user+challenge (a double-click, a retried request, a
scripted client) can both pass the "not already enrolled" check before
either has inserted its row. deduct_credits() itself is race-safe — it
takes SELECT ... FOR UPDATE on the wallet row — so it correctly serialises
the two charges and each one lands (as long as the balance covers both);
what was missing is anything serialising the *enrolment row*, so both
charges could succeed and both inserts could land, leaving the user paying
credit_cost twice for one enrolment and two ENROLLED attempts consuming
their max_attempts budget.

Fixed here the same way migration 008 closed the equivalent race on
exam_payments: a partial unique index that makes the second INSERT fail at
the database level rather than depending on the read-then-write staying
atomic in application code. enroll_challenge's existing try/except around
the insert (added for "insert failed after the charge landed") already
rolls back and calls refund_credits() on any exception — so a racer that
loses the index collision gets its credits refunded automatically and sees
"Could not start this challenge right now. Your credits were refunded."
rather than a duplicate charge.

Partial, not a table-wide unique constraint, because re-enrolling in a new
ATTEMPT after a previous one is submitted/graded/passed/failed must stay
legal (that's the multi-attempt flow `attempts_used < max_attempts` — see
enroll_challenge). Only the invariant "at most one active (ENROLLED, i.e.
not yet submitted) attempt per user per challenge" needs enforcing.

`status` is a native Postgres enum (`challengestatus`, see migration
001_initial_schema), so the predicate casts the literal explicitly —
`status = 'enrolled'` alone is not a valid comparison against an enum
column in a partial-index predicate.

Revision ID: 009_challenge_enrollment_race
Revises: 008_exam_payment_ref_squatting
Create Date: 2026-09-12

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '009_challenge_enrollment_race'
down_revision: Union[str, None] = '008_exam_payment_ref_squatting'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_index(
        'uq_challenge_attempts_active_enrollment',
        'challenge_attempts',
        ['user_id', 'challenge_id'],
        unique=True,
        postgresql_where=sa.text("status = 'enrolled'::challengestatus"),
    )


def downgrade() -> None:
    op.drop_index('uq_challenge_attempts_active_enrollment', table_name='challenge_attempts')
