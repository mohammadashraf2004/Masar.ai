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
from app.core import login_guard
from app.core.limiter import limiter


@pytest.fixture(scope="session", autouse=True)
def _migrate_db():
    """Reset the test database to a clean slate via the real Alembic
    migration chain (not create_all) and leave it at head for the
    whole test session."""
    from alembic.config import Config
    from alembic import command

    from sqlalchemy import text

    # ── Refuse to run against anything but a disposable test database ──
    # This fixture DROPs the entire public schema. backend/.env points at
    # the development database, and pytest picks that up unless
    # DATABASE_URL is overridden — so an ordinary `pytest` in backend/
    # would silently destroy real local data. (Stray "Test Track" /
    # "Test Tool" rows in the dev catalogue are the harmless evidence that
    # this already happened once.)
    #
    # The database NAME must contain "test". CI uses
    # ai_career_platform_test and passes; the dev database
    # ai_career_platform does not, and stops here.
    db_name = engine.url.database or ""
    if "test" not in db_name.lower():
        pytest.exit(
            "\n\n"
            f"Refusing to run: DATABASE_URL points at '{db_name}', which is not a\n"
            "test database, and this fixture DROPs the whole public schema.\n\n"
            "Point it at a disposable database, e.g.\n"
            f"  DATABASE_URL=postgresql://.../{db_name}_test pytest\n",
            returncode=1,
        )

    cfg = Config("alembic.ini")
    # str(engine.url) masks the password as '***' — need the real DSN.
    cfg.set_main_option("sqlalchemy.url", engine.url.render_as_string(hide_password=False))

    # Drop the schema outright rather than `downgrade base`. The downgrade
    # chain can't run against a database that already holds rows from a
    # previous run (002's downgrade restores user_progress.topic_id NOT
    # NULL, which fails once any tool-course progress row exists), so a
    # re-run against a used database would abort during collection with a
    # confusing IntegrityError. This always starts from nothing, and still
    # exercises the entire upgrade chain — which is the half that has to
    # work in production.
    with engine.begin() as conn:
        conn.execute(text("DROP SCHEMA public CASCADE"))
        conn.execute(text("CREATE SCHEMA public"))
    command.upgrade(cfg, "head")
    yield


@pytest.fixture(autouse=True)
def _promo_disabled_by_default(monkeypatch):
    """The launch promotion is OFF unless a test explicitly turns it on.

    pydantic-settings reads backend/.env, and the test container mounts
    the repo — so without this, enabling the promo locally silently
    changes the starting credit balance for every registration test and
    four unrelated tests start failing. Preconditions belong in the test,
    not in whatever the developer happens to have configured.
    """
    from app.core.config import settings

    monkeypatch.setattr(settings, "LAUNCH_PROMO_UNTIL", "")
    yield


@pytest.fixture(autouse=True)
def _reset_rate_limiter():
    """slowapi's Limiter keeps in-memory counters for the life of the
    process — without a reset, hitting /auth/login or /auth/register
    from more than a handful of tests would start returning 429s
    regardless of which test is running."""
    limiter.reset()
    # Same reasoning for the per-account failed-login lockout: its
    # counters outlive a single test, so one test's deliberate bad
    # passwords would lock out an unrelated test's login.
    login_guard.reset()
    yield


def verify_user(db: Session, user_id: int) -> None:
    """Mark a registered account's email as verified.

    Registration deliberately leaves `is_verified` False, and every
    credit-spending path now refuses an unverified account (see
    app.core.authz and wallet_service.deduct_credits). Tests that are about
    something *else* — what a hint costs, whether a refund lands, whether a
    rate limit holds — would otherwise all fail on the verification gate
    instead of exercising what they are named for.

    Tests that are about the gate itself must NOT call this; see
    test_email_verification_gate.py.
    """
    from app.models.user import User

    db.query(User).filter(User.id == user_id).update({"is_verified": True})
    db.commit()


def verify_registered(client, user_id: int) -> None:
    """verify_user() for the many `_register(client)` helpers that never
    took a `db` handle.

    Pulls the *same* Session the request just used back out of the app's
    dependency overrides, rather than opening a second one. That matters:
    a second session's commit would not be reflected in this session's
    identity map, so the next request's get_current_user could read a
    stale is_verified=False off the cached User object and reject a user
    the database says is verified.
    """
    from app.db.session import get_db

    override = client.app.dependency_overrides[get_db]
    session = next(override())
    verify_user(session, user_id)


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
