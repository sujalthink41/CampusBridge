from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool
from sqlalchemy.engine.url import make_url

# Adjusted imports for this project
from campus_bridge.config.settings.app import app_settings
from campus_bridge.data.database.base import Base
# Import all models so they are registered with Base.metadata
from campus_bridge.data.models import *  # noqa: F403

# Construct the URL from settings
url = make_url(app_settings.DATABASE_URL)

# alembic supports only sync engine for this pattern
# Swap asyncpg for psycopg2 if present
if url.drivername.startswith("postgresql+asyncpg"):
    url = url.set(drivername="postgresql+psycopg2")

# async pg supports ssl whereas psycopg supports sslmode
ssl_mode = url.query.get("ssl")
if ssl_mode:
    url = url.set(query={"sslmode": ssl_mode})

url_str = url.render_as_string(hide_password=False)

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config
config.set_main_option("sqlalchemy.url", url_str)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
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
