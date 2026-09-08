"""project submissions carry code, not a repo link

A project is submitted by writing code into a cell in the reader, the same
way an exercise is answered — not by pasting a GitHub URL and hoping the
reviewer clones it. This adds the column that holds that code.

Additive and nullable, deliberately:

  * Every existing submission keeps its row. Rows written before this
    migration simply have `code IS NULL`, and the API reports them as
    having no code rather than pretending otherwise.

  * `project_submissions.github_url` is NOT dropped. The API and the UI
    stop offering it as of this change, so nothing new is ever written
    there, but the URLs students already submitted are real work and
    dropping the column would destroy them irreversibly. An empty column
    costs nothing; a lost submission cannot be recovered.

Note on the old behaviour: `description` was already what got sent to the
AI code reviewer (tracks_controller.submit_project), so this migration is
mostly making the schema honest about what was being stored. `description`
survives as what its name says — optional notes about the approach.

Revision ID: 007_project_submission_code
Revises: 006_arabic_first_content
Create Date: 2026-09-07

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '007_project_submission_code'
down_revision: Union[str, None] = '006_arabic_first_content'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'project_submissions',
        sa.Column('code', sa.Text(), nullable=True),
    )


def downgrade() -> None:
    # Drops the submitted code. Safe only in the sense that it returns the
    # schema to its previous shape — the code itself is gone.
    op.drop_column('project_submissions', 'code')
