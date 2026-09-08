import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# Import all models so Alembic can detect them
from app.db.session import Base
import app.models.user         # noqa
import app.models.learning     # noqa
import app.models.progress     # noqa
import app.models.community    # noqa
import app.models.wallet       # noqa
import app.models.auth_token   # noqa
import app.models.answer_submission  # noqa
import app.models.challenge    # noqa
import app.models.exam         # noqa
import app.models.tool_course  # noqa

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# alembic.ini's sqlalchemy.url is a static default for host-side runs
# (`localhost:5432`, reachable via docker-compose's exposed db port). Inside
# a container there's nothing listening on the container's own localhost --
# prefer the real DATABASE_URL env var (already set correctly by
# docker-compose.yml to point at the `db` service) when it's present, so
# `docker compose exec api alembic upgrade head` and a host-venv run both
# work with the exact same command.
_env_db_url = os.environ.get("DATABASE_URL")
if _env_db_url:
    config.set_main_option("sqlalchemy.url", _env_db_url)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
