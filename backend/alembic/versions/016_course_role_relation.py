"""a course's role in a career goal: core, supporting or optional

`course_roles` says *which* career goals a course serves, and nothing about how
much. The same course is central to one goal and background reading for another
(FastAPI serving is core for MLOps, supporting for AI Developer), and cloning
the course per goal would split its lessons, progress and prerequisites.

`relation` is that per-goal importance, kept on the existing many-to-many row:
`core`, `supporting` or `optional`. Every existing row becomes `core` - which is
what a tag has always meant - so nothing changes for anyone until a relation is
set deliberately. It is descriptive metadata: path generation, course states
and progress do not read it.

Additive and reversible; the running application keeps working against the new
column because the server default covers any insert that does not name it.

Revision ID: 016_course_role_relation
Revises: 015_update_acknowledgements
Create Date: 2026-09-25

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '016_course_role_relation'
down_revision: Union[str, None] = '015_update_acknowledgements'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'course_roles',
        sa.Column('relation', sa.String(), nullable=False, server_default='core'),
    )
    op.create_check_constraint(
        'ck_course_roles_relation', 'course_roles',
        "relation IN ('core', 'supporting', 'optional')",
    )


def downgrade() -> None:
    op.drop_constraint('ck_course_roles_relation', 'course_roles', type_='check')
    op.drop_column('course_roles', 'relation')
