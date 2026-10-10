"""
Migration 038 repairs `pro_ai_usage.release_reason` on databases that applied an early draft
of 036 without it. On a database whose 036 already created the column (every fresh graph,
and production) it changes nothing, and its downgrade is deliberately a no-op: 036 owns the
column.
"""
import sqlalchemy as sa
from alembic import command
from alembic.script import ScriptDirectory

from app.db.session import engine
from tests.test_migration_graph import _config

REVISION = "038_pro_ai_release_reason"


def _release_reason():
    columns = {c["name"]: c for c in sa.inspect(engine).get_columns("pro_ai_usage")}
    return columns.get("release_reason")


def _current():
    with engine.connect() as connection:
        return connection.execute(sa.text("SELECT version_num FROM alembic_version")).scalar()


def test_038_follows_037_and_is_the_head():
    script = ScriptDirectory.from_config(_config())
    assert script.get_revision(REVISION).down_revision == "037_mentor_requests"
    assert script.get_heads() == [REVISION]


def test_038_restores_the_column_a_drifted_036_left_out():
    cfg = _config()
    try:
        command.downgrade(cfg, "037_mentor_requests")
        # A database that ran the early 036 draft: same revision, no release_reason.
        with engine.begin() as connection:
            connection.execute(sa.text("ALTER TABLE pro_ai_usage DROP COLUMN release_reason"))
        assert _release_reason() is None
        command.upgrade(cfg, "head")
    finally:
        command.upgrade(cfg, "head")
        if _release_reason() is None:  # leave the shared test database usable whatever failed
            with engine.begin() as connection:
                connection.execute(sa.text("ALTER TABLE pro_ai_usage ADD COLUMN release_reason VARCHAR(120)"))
    column = _release_reason()
    assert column is not None and column["nullable"] is True
    assert getattr(column["type"], "length", None) == 120
    assert _current() == REVISION


def test_038_is_a_no_op_on_a_healthy_database_both_ways():
    cfg = _config()
    assert _release_reason() is not None
    try:
        command.downgrade(cfg, "037_mentor_requests")
        # 036 owns the column: stepping back over 038 must not drop it.
        assert _release_reason() is not None
        assert _current() == "037_mentor_requests"
    finally:
        command.upgrade(cfg, "head")
    assert _release_reason() is not None
    assert _current() == REVISION
