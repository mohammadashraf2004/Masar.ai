"""
Preflight for scripts that populate an already-migrated database.

Alembic owns the schema. Seed scripts only insert/update rows, so they must
never create tables themselves (`Base.metadata.create_all()` would create a
later revision's table early and `alembic upgrade head` would then die with
DuplicateTable). Call `require_migrated_schema()` instead: it does not touch
the schema, it only refuses to continue when the database is not at head.
"""
from pathlib import Path

from alembic.runtime.migration import MigrationContext
from alembic.script import ScriptDirectory
from sqlalchemy.engine import Engine

from app.db.session import engine as default_engine

_ALEMBIC_DIR = Path(__file__).resolve().parents[2] / "alembic"


def require_migrated_schema(engine: Engine = default_engine) -> None:
    """Exit with a clear message unless the database is at the Alembic head."""
    heads = set(ScriptDirectory(str(_ALEMBIC_DIR)).get_heads())
    with engine.connect() as conn:
        current = set(MigrationContext.configure(conn).get_current_heads())

    if current == heads:
        return

    if not current:
        state = "has no Alembic version (the schema has not been created)"
    else:
        state = f"is at revision {', '.join(sorted(current))}"
    raise SystemExit(
        f"\nRefusing to seed: the database {state}, but the code expects "
        f"{', '.join(sorted(heads))}.\n"
        "Seed scripts do not create or change the schema. Run\n"
        "    alembic upgrade head\n"
        "first, then re-run this script.\n"
    )
