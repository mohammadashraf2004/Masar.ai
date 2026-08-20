"""
Shared pytest fixtures.

Requires DATABASE_URL (see backend/.env / CI env) to point at a real,
disposable Postgres database — these tests run actual migrations and
actual queries against it, not mocks. Never point this at a database
with data you care about; the session-scoped `_migrate` fixture drops
and recreates the entire schema at the start of the run.
"""
import pytest
from sqlalchemy.orm import Session

# Importing app.main pulls in every controller, which pulls in every
# model module — required so SQLAlchemy can resolve every relationship()
# string reference before any test touches the ORM. This import graph
# is also, itself, a regression test: it's exactly what broke earlier
# in this project when new model modules weren't imported everywhere
# they needed to be.
import app.main  # noqa: F401
from app.db.session import engine, SessionLocal
from app.core.limiter import limiter


@pytest.fixture(scope="session", autouse=True)
def _migrate_db():
    """Reset the test database to a clean slate via the real Alembic
    migration chain (not create_all) and leave it at head for the
    whole test session."""
    from alembic.config import Config
    from alembic import command

    cfg = Config("alembic.ini")
    # str(engine.url) masks the password as '***' — need the real DSN.
    cfg.set_main_option("sqlalchemy.url", engine.url.render_as_string(hide_password=False))
    command.downgrade(cfg, "base")
    command.upgrade(cfg, "head")
    yield


@pytest.fixture(autouse=True)
def _reset_rate_limiter():
    """slowapi's Limiter keeps in-memory counters for the life of the
    process — without a reset, hitting /auth/login or /auth/register
    from more than a handful of tests would start returning 429s
    regardless of which test is running."""
    limiter.reset()
    yield


@pytest.fixture()
def db() -> Session:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture()
def client(db):
    """A TestClient wired to the same db session the test uses, so
    assertions can see what the request committed."""
    from fastapi.testclient import TestClient
    from app.main import app
    from app.db.session import get_db

    def _override_get_db():
        yield db

    app.dependency_overrides[get_db] = _override_get_db
    try:
        with TestClient(app) as c:
            yield c
    finally:
        app.dependency_overrides.pop(get_db, None)
