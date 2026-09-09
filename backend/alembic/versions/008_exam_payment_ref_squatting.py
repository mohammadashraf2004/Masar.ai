"""exam payment references cannot be squatted

Before this, `POST /exam-payments/submit` rejected any reference string
that already existed on ANY exam_payments row, in any state, belonging to
anyone:

    dup = db.query(ExamPayment).filter(
        ExamPayment.payment_ref == payload.payment_ref
    ).first()
    if dup: -> 400

The reference is user-supplied — a student pays at a Fawry kiosk / by
InstaPay / from a mobile wallet and then types the reference the provider
gave them into our form. So that check let anyone permanently deny a
reference to its real owner: submit the string first (guessed, shoulder-
surfed, or sprayed), and the person who actually paid can never claim it.
The squatter's row stays `pending` forever and grants them nothing, which
is why this is denial of service rather than theft — but the victim's
money is gone and their exam access is unreachable.

The rule that actually needed enforcing was never "this string has been
seen before". It is:

    at most one CONFIRMED payment may exist per reference

which is what stops two people being granted exam access off one real
payment. That is the constraint created here, as a partial unique index so
it binds only confirmed rows. Pending claims are deliberately left
non-unique: several people may *claim* a reference, and an administrator
adjudicates against the provider's own records (that is already what
`/exam-payments/admin/confirm` is for). The moment one is confirmed, this
index makes every competing confirmation fail at the database level rather
than depending on the admin endpoint's read-then-write staying atomic.

A partial index, not a table constraint, because Postgres has no
`UNIQUE ... WHERE`; and `postgresql_where` is exactly the right tool since
`status` is a plain string column with three known values.

The supporting non-unique index on (payment_ref, status) is what the
submit path now looks up on: "is this reference confirmed by anyone" and
"does this user already hold a row for it".

Revision ID: 008_exam_payment_ref_squatting
Revises: 007_project_submission_code
Create Date: 2026-09-08

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '008_exam_payment_ref_squatting'
down_revision: Union[str, None] = '007_project_submission_code'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Lookup index for the submit-path checks. Not unique: pending claims
    # may legitimately collide while an admin works out which is real.
    op.create_index(
        'ix_exam_payments_ref_status',
        'exam_payments',
        ['payment_ref', 'status'],
        unique=False,
    )

    # The real invariant: one confirmed payment per reference, enforced by
    # the database so a race between two admin confirmations (or a webhook
    # racing an admin) cannot produce two grants from one payment.
    op.create_index(
        'uq_exam_payments_confirmed_ref',
        'exam_payments',
        ['payment_ref'],
        unique=True,
        postgresql_where=sa.text("status = 'confirmed'"),
    )


def downgrade() -> None:
    op.drop_index('uq_exam_payments_confirmed_ref', table_name='exam_payments')
    op.drop_index('ix_exam_payments_ref_status', table_name='exam_payments')
