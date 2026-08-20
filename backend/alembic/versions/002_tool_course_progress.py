"""tool_course_category_and_progress

Adds ToolCourse.category (display grouping for the browse page) and
UserProgress.tool_topic_id (so lesson/exercise completion can be tracked
for tool-course topics the same way it already is for track topics).

Revision ID: 002_tool_course_progress
Revises: 001_initial_schema
Create Date: 2026-08-20 19:29:55.646924

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '002_tool_course_progress'
down_revision: Union[str, None] = '001_initial_schema'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

_FK_NAME = 'fk_user_progress_tool_topic_id_tool_topics'


def upgrade() -> None:
    op.add_column('tool_courses', sa.Column('category', sa.String(), nullable=True))
    op.create_index(op.f('ix_tool_courses_category'), 'tool_courses', ['category'], unique=False)
    op.add_column('user_progress', sa.Column('tool_topic_id', sa.Integer(), nullable=True))
    op.alter_column('user_progress', 'topic_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.create_foreign_key(_FK_NAME, 'user_progress', 'tool_topics', ['tool_topic_id'], ['id'])


def downgrade() -> None:
    op.drop_constraint(_FK_NAME, 'user_progress', type_='foreignkey')
    op.alter_column('user_progress', 'topic_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.drop_column('user_progress', 'tool_topic_id')
    op.drop_index(op.f('ix_tool_courses_category'), table_name='tool_courses')
    op.drop_column('tool_courses', 'category')
