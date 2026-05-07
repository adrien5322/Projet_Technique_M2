"""Alembic migrations environment."""

from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Import our application config to get DATABASE_URL
from app.config import settings

# Set sqlalchemy.url from our application settings
# This allows Alembic to use the same DATABASE_URL as the app
# Fallback to alembic.ini default (sqlite:///./dev.db) if not set
if settings.DATABASE_URL:
    config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)
else:
    # Use the default from alembic.ini (SQLite for local dev)
    # This allows running migrations without DATABASE_URL set
    print("WARNING: DATABASE_URL not set, using default from alembic.ini")

# add your model's MetaData object here
# for 'autogenerate' support
# Import Base and ALL models to ensure they are registered in Base.metadata
from app.models.user import Base
from app.models.user import User
from app.models.telemetry import TelemetryHeartbeat
from app.models.asset import Asset
from app.models.event import Event
from app.models.alert import Alert
from app.models.audit import AuditLog
from app.models.port_finding import PortFinding
from app.models.correlation import CorrelationGroup, correlation_events

target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


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
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
