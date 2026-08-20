"""
Guards against the exact class of bug found and fixed in this project:
a new model module added but never imported somewhere SQLAlchemy needs
it (seed scripts, alembic/env.py), which only surfaces the moment some
relationship() string actually gets resolved.
"""
from sqlalchemy.orm import configure_mappers
from sqlalchemy.orm import class_mapper

from app.db.session import Base
from app.models.tool_course import ToolCourse


def test_all_mappers_configure():
    # Raises if any relationship() references a class that was never
    # imported into this process.
    configure_mappers()


def test_migrated_schema_matches_models(db):
    """The live (migrated) schema and the current model metadata must
    describe the same schema — any drift here means a model changed
    without a matching migration, or vice versa."""
    from alembic.autogenerate import compare_metadata
    from alembic.runtime.migration import MigrationContext

    with db.connection() as conn:
        mc = MigrationContext.configure(conn)
        diff = compare_metadata(mc, Base.metadata)
    assert diff == [], f"schema drift between migrations and models: {diff}"


def test_tool_course_mapper_is_registered():
    # Sanity check that the tool-course models specifically are wired
    # into the same registry as everything else, not off on their own.
    class_mapper(ToolCourse)
