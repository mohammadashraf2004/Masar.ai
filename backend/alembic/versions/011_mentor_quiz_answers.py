"""mentor quiz answers: evidence log for skill state and recent mistakes

Mentor v2 grades single in-chat quiz questions on the server
(POST /mentor/quiz/answer). Each answer is evidence for one skill, and a
wrong one is a mistake /mentor/message should be able to bring up later.

A new table rather than QuizAttempt: that row is a whole-quiz submission
and feeds `quizzes_passed` on the scorecard, so logging single questions
there would inflate it. Chat history itself still lives in
mentor_sessions.messages; nothing parallel to it is added.
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = '011_mentor_quiz_answers'
down_revision: Union[str, None] = '010_exam_attempt_start_race'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'mentor_quiz_answers',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('quiz_id', sa.Integer(), sa.ForeignKey('quizzes.id'), nullable=False),
        sa.Column('question_index', sa.Integer(), nullable=False),
        sa.Column('lesson_id', sa.Integer(), sa.ForeignKey('lessons.id'), nullable=True),
        sa.Column('skill_name', sa.String(), nullable=False),
        sa.Column('chosen_index', sa.Integer(), nullable=False),
        sa.Column('is_correct', sa.Boolean(), nullable=False),
        sa.Column('question_text', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index('ix_mentor_quiz_answers_id', 'mentor_quiz_answers', ['id'])
    op.create_index('ix_mentor_quiz_answers_user_id', 'mentor_quiz_answers', ['user_id'])
    op.create_index('ix_mentor_quiz_answers_created_at', 'mentor_quiz_answers', ['created_at'])
    # The skill-state read: "this learner's last N answers on this skill".
    op.create_index(
        'ix_mentor_quiz_answers_user_skill', 'mentor_quiz_answers', ['user_id', 'skill_name', 'created_at'],
    )


def downgrade() -> None:
    op.drop_index('ix_mentor_quiz_answers_user_skill', table_name='mentor_quiz_answers')
    op.drop_index('ix_mentor_quiz_answers_created_at', table_name='mentor_quiz_answers')
    op.drop_index('ix_mentor_quiz_answers_user_id', table_name='mentor_quiz_answers')
    op.drop_index('ix_mentor_quiz_answers_id', table_name='mentor_quiz_answers')
    op.drop_table('mentor_quiz_answers')
