"""Migration 040 adds the two nullable example-answer columns to exercises and
removes exactly them on downgrade."""
import sqlalchemy as sa
from alembic import command
from alembic.script import ScriptDirectory

from app.db.session import engine
from tests.test_migration_graph import _config

REVISION = "040_exercise_example_answers"


def _columns():
    return {c["name"]: c for c in sa.inspect(engine).get_columns("exercises")}


def test_040_follows_039_and_is_the_head():
    script = ScriptDirectory.from_config(_config())
    assert script.get_revision(REVISION).down_revision == "039_additional_credit_packs"
    assert script.get_heads() == [REVISION]


def test_040_adds_and_removes_only_the_example_answer_columns():
    cfg = _config()
    before = set(_columns())
    assert {"example_answer", "example_answer_ar"} <= before
    try:
        command.downgrade(cfg, "039_additional_credit_packs")
        assert set(_columns()) == before - {"example_answer", "example_answer_ar"}
    finally:
        command.upgrade(cfg, "head")
    columns = _columns()
    assert set(columns) == before
    assert columns["example_answer"]["nullable"] and columns["example_answer_ar"]["nullable"]
