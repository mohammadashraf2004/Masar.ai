"""answer_submissions

Conversational, LLM-graded answer threads for exercises and open-ended
quiz questions (see app/models/answer_submission.py).

Revision ID: 003_answer_submissions
Revises: 002_tool_course_progress
Create Date: 2026-08-21 01:26:55.618998

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '003_answer_submissions'
down_revision: Union[str, None] = '002_tool_course_progress'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('answer_submissions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('exercise_id', sa.Integer(), nullable=True),
    sa.Column('quiz_id', sa.Integer(), nullable=True),
    sa.Column('question_index', sa.Integer(), nullable=True),
    sa.Column('messages', sa.JSON(), nullable=True),
    sa.Column('is_correct', sa.Boolean(), nullable=True),
    sa.Column('score', sa.Float(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['exercise_id'], ['exercises.id'], ),
    sa.ForeignKeyConstraint(['quiz_id'], ['quizzes.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_answer_submissions_id'), 'answer_submissions', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    op.drop_index(op.f('ix_answer_submissions_id'), table_name='answer_submissions')
    op.drop_table('answer_submissions')
